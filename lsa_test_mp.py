#!/usr/bin/env python
#coding=utf-8
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool, cpu_count
from morfeusz2 import Morfeusz
from contextlib import closing
from nltk.util import ngrams
from sys import argv, exit
from numpy import fromfile
import numpy as np
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


print('Loading dictionary...')
dictionary = []
with codecs.open('dict.txt', encoding = 'utf-8') as f:  
    dictionary = f.read().splitlines()
    f.close()


print('Loading SVD file...')
svdMat = fromfile('svdMat.svd')
svdMat = svdMat.reshape(len(dictionary), int(svdMat.shape[0] / len(dictionary)))


print('Calculating distances...')
distances = cosine_similarity(svdMat, svdMat)
np.fill_diagonal(distances, -1)
distances = distances.tolist()
gc.collect()
print('Distances are calculated!')


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


def find_syns(index, form):
	dists = distances[index] # vector of dists between each word and the current word
	syns = [] # vector of synonyms
	for i in xrange(0, 2):
		index_of_max = dists.index(max(dists))
		dists[index_of_max] = -1
		full_desc = morph.generate(dictionary[index_of_max])
		if 'ign' == full_desc[0][2]: # if morph does not contain the word
			continue
		form_similarities = []
		for form_test in full_desc:
			form_similarities.append(get_form_similarity(form, form_test))
		index_of_best_form = form_similarities.index(max(form_similarities))
		syns.append(full_desc[index_of_best_form][0])
	return syns


def get_corpus_line_batch():            
        with codecs.open(corpus_filename, encoding = 'utf-8') as f:
            line_set = []
            batch_size = 1000
            for raw_line in f:
                line_set.append(raw_line)
                if len(line_set) == batch_size:
                    yield line_set
                    line_set = []
            else:
                if len(line_set) != 0:
                    yield line_set


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
                     index = dictionary.index(init_form)##                     
                     syns = find_syns(index, w_desc[0][2][2].split(':'))##
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
    
    # remove previous result
    if 'generated_with_wn.txt' in os.listdir('.'):
            os.remove('generated_with_wn.txt')
    
    line_batch_gen = get_corpus_line_batch()
    min_line = 0
    max_line = 0
    for line_batch in line_batch_gen:
        max_line = max_line + len(line_batch)
        print('Processing lines {} - {}...'.format(min_line, max_line))
        with closing(Pool(processes = num_cores)) as pool:
            pool = Pool(processes = num_cores)
            print('Reading corpus lines...')
            lines = line_batch
            lines = zip(list(range(len(lines))), lines)
            print('Starting to extract ngrams...')
            print('Lines are not being processed squentially! ')
            ngram2file = pool.map(get_ngrams, lines)
            ngram2file = filter(None, ngram2file)
            pool.terminate()
            print('\nngram extraction completed.')
            gc.collect()
        
        print('Writing ngrams to file...')
        generated = open('generated_with_lsa.txt', mode = 'a')
        
        for ngrams_ in ngram2file:    
            for ngrams__ in ngrams_:
                generated.write(u' '.join(ngrams__).encode('utf8') + '\n')
        
        generated.close()
        min_line = max_line
