#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os 
from math import log
from author import author
from document import document
from fnmatch import filter
from locale import setlocale, LC_ALL

setlocale(LC_ALL, 'tr_TR.UTF-8')
alpha = 0.021

# Read documents in given path, returns author and list of document objects.
def read_documents(author_dir):
	document_list = []
	auth = author(os.path.basename(author_dir))					# Constructs 'author' object with given name.
	for doc_name in os.listdir(author_dir):
		if doc_name.endswith('.txt'):
			doc_text = open(author_dir + "/" + doc_name,'r').read()						
			document_list.append(document(auth.name + doc_name[:-4], auth.name, doc_text))		# Constructs documents with given file and author,
	auth.doc_list = document_list
	auth.doc_count = len(document_list)
	return auth																# adds them into a list. Then returns author object.

# Constructs vocabulary for all documents and for each author seperately. 
def construct_vocabulary(author_list):
	vocabulary = {}
	for auth in author_list:
		auth_vocabulary = {}
		for doc in auth.doc_list:
			bow = doc.construct_bow()						# Constructs bag of words representation for documents.
			for token, count in bow.items():
				auth_vocabulary.setdefault(token, 0)		# Adds tokens to vocabularies of each author.
				auth_vocabulary[token] += count
				vocabulary.setdefault(token, 0)				# Adds tokens to vocabulary.
				vocabulary[token] += count
		auth.vocabulary = auth_vocabulary
		auth.compute_tot_token_count()
	return vocabulary

# Performs 'Naive Bayes' in order to determine which author has written the given text.
def determine_author(text, author_list, vocabulary, tot_doc_count):
	auth_res = {}
	doc = document("","",text)
	bow = doc.construct_bow()
	for auth in author_list:
		auth_res[auth.name] = log(1.0 * auth.doc_count / tot_doc_count)
		for token, count in bow.items():
			token_pos = log((auth.vocabulary.get(token,0) + alpha) / (auth.tot_token_count + alpha * len(vocabulary)))
			auth_res[auth.name] += token_pos * count

	return sorted(auth_res, key=auth_res.get,reverse=True)[0]

# Returns a list of all files in given directory.
def traverse_dir(path):
	doc_list = []
	for root, dir, files in os.walk(path):
		for items in filter(files, "*"):
			doc_list.append(root + "/" + items)
	return doc_list

# Default paths.
training_path = 'training_dataset/'
test_path = 'test_dataset/'

if __name__ == "__main__":

		#  If the paths of the datasets are given as parameters.
		if len(sys.argv) > 1:
			training_path 	= os.path.normpath(sys.argv[1]) + "/"
			test_path 		= os.path.normpath(sys.argv[2]) + "/"

		tot_doc_count = 0
		author_list = []
		for author_dir in os.listdir(training_path):
			auth = read_documents(training_path + author_dir)
			tot_doc_count += auth.doc_count
			author_list.append(auth)

		vocabulary = construct_vocabulary(author_list)

		pos = 0
		neg = 0

		test_doc_list = traverse_dir(test_path)
		for doc_path in test_doc_list:
			if doc_path.endswith('.txt'):
				doc_text = open(doc_path,'r').read()
				author_name = os.path.basename(os.path.dirname(doc_path))
				determined_author_name = determine_author(doc_text, author_list, vocabulary, tot_doc_count)
				if author_name == determined_author_name:
					pos += 1 
				else: 
					neg += 1
				print(author_name + " : " + determined_author_name)
		print("alpha : " + str(alpha) + ", pos : " + str(pos) + ", neg : " + str(neg) + ", res : " + str(1.0 * pos / (neg+pos)))


