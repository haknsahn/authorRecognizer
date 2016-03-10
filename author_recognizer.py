#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os 
from author import author
from document import document

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
	return vocabulary

# Default paths.
training_path = 'training_dataset/'
test_path = 'test_dataset/'

if __name__ == "__main__":

	# If the paths of the datasets are given as parameters.
	if len(sys.argv) > 1:
		training_path 	= os.path.normpath(sys.argv[1]) + "/"
		test_path 		= os.path.normpath(sys.argv[2]) + "/"


	training_doc_dict = {}
	for author_dir in os.listdir(training_path):
		(auth, doc_list) = read_documents(training_path + author_dir)
		training_doc_dict[auth] = doc_list

	vocabulary = construct_vocabulary(training_doc_dict)
