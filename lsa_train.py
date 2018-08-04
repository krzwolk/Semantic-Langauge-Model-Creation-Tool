#!/usr/bin/env python
#coding=utf-8

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from morfeusz2 import Morfeusz
import string
import re
from os import listdir
from sys import argv, exit
#other imports

corpus_filename = 'pl.txt'
try:
	filename = argv[1]
	if filename in listdir('.'):
		corpus_filename = filename
	else:
		print ('File %s not found in the current directory' % filename)
		exit(-1)
except IndexError:
	pass

exclude = string.digits #unicode(string.digits) #
morph = Morfeusz()
def lemm(line):
	sentence = re.split('\d+|\W+|_', line.lower(), flags=re.UNICODE) #re.split('\W+', line.lower(), flags=re.UNICODE) #line.split()
	norm_sentence = []
	for i in xrange(0, len(sentence)):
		if sentence[i] != u'':
			#print 'sen: ', sentence[i], 'len: ', len(sentence[i])
			w_desc = morph.analyse(sentence[i])
			if len(w_desc) > 0:
				norm_sentence.append(w_desc[0][2][1].split(':')[0])
	return norm_sentence
	
#load data
f = open('stopwords_pl.txt', 'r')
stopwords = f.readlines()
f.close()

f = open(corpus_filename, 'r')
lines = f.readlines()
f.close()

#Document-Term Matrix
cv = CountVectorizer(input='content',strip_accents='ascii', stop_words = stopwords, analyzer = 'word',tokenizer = lemm)
del stopwords
dtMatrix = cv.fit_transform(lines)#.titles
print 'dtMatrix.shape: ', dtMatrix.shape
featurenames = cv.get_feature_names()

f = open('dict.txt', 'w')
for lemma in featurenames:
	f.write(lemma.encode('utf-8') + '\n')
f.close()

#Tf-idf Transformation
tfidf = TfidfTransformer()
tfidfMatrix = tfidf.fit_transform(dtMatrix.transpose())
print "tfidfMatrix.shape: ", tfidfMatrix.shape

#SVD
#n_components is recommended to be 100 by Sklearn Documentation for LSA
#http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
svd = TruncatedSVD(n_components = 120) # 100
svdMatrix = svd.fit_transform(tfidfMatrix)

#print type(svdMatrix)
print 'svdMatrix.shape: ', svdMatrix.shape
svdMatrix.tofile('svdMat.svd')
#f_in = featurenames.index('market')
#print 'f-in type: ', type(svdMatrix[f_in]), ' shape: ', svdMatrix[f_in].shape
#dists = []
#for v in svdMatrix:
#	print 'v type: ', type(v), ' shape: ', v.shape
#	dists.append(cosine_similarity(svdMatrix[f_in].reshape(1,-1), v.reshape(1,-1)))
#for d in dists:	print(d)
#print (featurenames[dists.index(max(dists))])
#print sorted(dists)
#print len(svdMatrix)

