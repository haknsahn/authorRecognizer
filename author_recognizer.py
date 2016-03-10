#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os 
from author import author
from document import document
from fnmatch import filter

# Read documents in given path, returns author and list of document objects.
def read_documents(author_dir):
	document_list = []
	auth = author(os.path.basename(author_dir))					# Constructs 'author' object with given name.
	for doc_name in os.listdir(author_dir):
		if doc_name.endswith('.txt'):
			doc_text = open(author_dir + "/" + doc_name,'r').read()						
			document_list.append(document(auth.name + doc_name[:-4], auth.name, doc_text))		# Constructs documents with given file and author,
	return (auth, document_list)																# adds them into a list. Then returns author object and document list as a tuple.

# Constructs vocabulary for all documents and for each author seperately. 
def construct_vocabulary(doc_dict):
	vocabulary = {}
	for auth, doc_list in doc_dict.iteritems():
		auth_vocabulary = {}
		for doc in doc_list:
			bow = doc.construct_bow()						# Constructs bag of words representation for documents.
			for token, count in bow.iteritems():
				auth_vocabulary.setdefault(token, 0)		# Adds tokens to vocabularies of each author.
				auth_vocabulary[token] += count
				vocabulary.setdefault(token, 0)				# Adds tokens to vocabulary.
				vocabulary[token] += count
		auth.vocabulary = auth_vocabulary
		auth.compute_tot_token_count()
	return vocabulary

# Performs 'Naive Bayes' in order to determine which author has written the given text.
def determine_author(text, training_doc_dict, vocabulary, tot_doc_count):
	auth_res = {}
	bow = document("","",text).construct_bow()
	for auth in training_doc_dict.iterkeys():
		auth_res[auth.name] = 1.0 * auth.doc_count / tot_doc_count
		
		cnt = 0
		for token, count in bow.iteritems():
			if cnt > 30:
				break
			cnt += 1
			token_pos = (auth.vocabulary.get(token,0) + 1) / (1.0 * (auth.tot_token_count + len(vocabulary)))
			auth_res[auth.name] *= token_pos ** count

	sorted_auth_res = sorted(auth_res, key=auth_res.get)
	return sorted_auth_res[-1]

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

	# If the paths of the datasets are given as parameters.
	if len(sys.argv) > 1:
		training_path 	= os.path.normpath(sys.argv[1]) + "/"
		test_path 		= os.path.normpath(sys.argv[2]) + "/"

	tot_doc_count = 0
	training_doc_dict = {}
	for author_dir in os.listdir(training_path):
		(auth, doc_list) = read_documents(training_path + author_dir)
		auth.doc_count = len(doc_list)
		tot_doc_count += auth.doc_count
		training_doc_dict[auth] = doc_list

	vocabulary = construct_vocabulary(training_doc_dict)

	test_doc_list = traverse_dir(test_path)
	for doc_path in test_doc_list:
		if doc_path.endswith('.txt'):
			doc_text = open(doc_path,'r').read()
			print os.path.basename(os.path.dirname(doc_path)) + " : " + determine_author(doc_text, training_doc_dict, vocabulary, tot_doc_count)
		


