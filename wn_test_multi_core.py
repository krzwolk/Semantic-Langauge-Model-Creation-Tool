#!/usr/bin/env python
#coding = utf-8

from multiprocessing import Pool, cpu_count
import xml.etree.ElementTree as ET
from contextlib import closing
from morfeusz2 import Morfeusz
from nltk.util import ngrams
from sys import argv, exit
import os, gc, sys
import codecs
import re



os.chdir(os.path.dirname(os.path.abspath(__file__)))

corpus_filename = 'pl.txt'
max_n = 3
morph = Morfeusz()

try:
    filename = argv[1]
    if filename in os.listdir('.'):
        corpus_filename = filename
    else:
        print ('File %s not found in the current directory' % filename)
        exit(-1)
except IndexError:
    pass


def get_xml_line():
    file_name = "plwordnet-3.0-visdisc.xml"
    with codecs.open(file_name, encoding='utf-8', mode='r') as f:
        for xml_line in f:
            yield xml_line



def extract_syns(xml_line):
    idx = xml_line[0]
    xml_line = xml_line[1]
    sys.stdout.write('\r')
    sys.stdout.write('Processing line {}'.format(idx))
    sys.stdout.flush()
    syns_set = []    
    try:
        syns = ET.fromstring(xml_line.encode('utf-8'))        
        for word in syns.iter('LITERAL'):
            syns_set.append(unicode(word.text))
        
        if len(syns_set) > 1:
            return syns_set
    
    except ET.ParseError:
        print('\nxml.etree.ElementTree.ParseError!!!')
        return None



def get_syns(word, synsets):
    word_u = unicode(word.decode('utf8'))
    for synset in synsets:
        for term in synset:
            if term == word_u:
                return synset


def get_form_similarity(form, form_test):
    similarity = 0
    l = min(len(form), len(form_test))
    for n_feature in xrange(0, l):
        if form[n_feature] == form_test[n_feature]:
            similarity += 1
    return similarity / l



def find_syns(word, form, synsets):
    syns_in_form = []
    syns = get_syns(word, synsets) # vector of synonyms
    if syns is None:
        return
    syns.remove(word)
    for i in xrange(0, len(syns)):
        if len(syns[i].split()) > 1:
            continue
        full_desc = morph.generate(syns[i])
        if 'ign' == full_desc[0][2]: # if morph does not contain the word
            continue
        form_similarities = []
        for form_test in full_desc:
            form_similarities.append(get_form_similarity(form, form_test))
        index_of_best_form = form_similarities.index(max(form_similarities))
        syns_in_form.append(full_desc[index_of_best_form][0])
    return syns  




def get_corpus_line():            
        with codecs.open(corpus_filename, encoding = 'utf-8') as f:    
            for raw_line in f:
                yield raw_line



def get_ngrams(raw_line):
    idx = raw_line[0]
    raw_line = raw_line[1]
    sys.stdout.write('\r')
    sys.stdout.write('Processing line {}'.format(idx))
    sys.stdout.flush()
    sentence = re.split('\W+', raw_line.lower(), flags = re.UNICODE)
    ngrams2file = []
    for ngram_tuple in ngrams(sentence, min(len(sentence[:-1]), max_n)): # [:-1] because sentence has empty word as the last element
        ngram = list(ngram_tuple)
        ngrams2file.append(ngram) # initial form of ngram
        for c in xrange(0, len(ngram)):    # step by word in ngram
            w_desc = morph.analyse(ngram[c])
            if len(w_desc) > 0:
                init_form = w_desc[0][2][1].split(':')[0]
                try:
                     syns = find_syns(init_form, w_desc[0][2][2].split(':'), synsets)
                     if syns is None:
                        break
                    
                     for syn in syns:
                         ngram2file = ngram[:]
                         ngram2file[c] = syn
                         ngrams2file.append(ngram2file)
                except ValueError:
                    continue
    return ngrams2file
                        



if __name__ == "__main__" :
    # set the number of cores you want to utilize
    num_cores = cpu_count()
    with closing(Pool(processes = num_cores)) as pool:
        lines = list(get_xml_line())
        lines = zip(list(range(len(lines))), lines)
        print('Starting to extract synonyms...')
        print('Lines are not being processed squentially! ')
        synsets = pool.map(extract_syns, lines)
        synsets = filter(None, synsets)
        pool.terminate()
        print('\nCorpus extraction completed.')
        print('The size of corpus is {}'.format(len(synsets)))
        gc.collect()
    
    
    # remove previous result
    if 'generated_with_wn.txt' in os.listdir('.'):
            os.remove('generated_with_wn.txt')
    
    
    with closing(Pool(processes = num_cores)) as pool:
        print('Reading corpus lines...')
        lines = list(get_corpus_line())
        lines = zip(list(range(len(lines))), lines)
        print('Starting to extract ngrams...')
        print('Lines are not being processed squentially! ')
        ngram2file = pool.map(get_ngrams, lines)
        ngram2file = filter(None, ngram2file)
        pool.terminate()
        print('\nngram extraction completed.')
        gc.collect()
    
            
    
    print('Writing ngrams to file...')
    generated = open('generated_with_wn.txt', mode = 'a')
    
    for ngrams_ in ngram2file:    
        for ngrams__ in ngrams_:
            generated.write(u' '.join(ngrams__).encode('utf8') + '\n')
    
    generated.close()