#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os, argparse
from math import log
from author import author
from document import document
from fnmatch import filter
from locale import setlocale, LC_ALL

setlocale(LC_ALL, 'tr_TR.UTF-8')

alpha 				= 0.021
word_coef 			= -18
sentence_coef 		= -3
quatation_coef 		= -5
exclamation_coef 	= -8

HEADER 	= "\033[95m"
CLEAR 	= "\033[92m"
FAIL 	= "\033[91m"
ENDC 	= "\033[0m"

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
		auth.compute_ave_sentence_count()
		auth.compute_ave_words_in_sentence()
		auth.compute_ave_quatation_mark()
		auth.compute_ave_exclamation_mark()
	return vocabulary

# Performs 'Naive Bayes' in order to determine which author has written the given text.
def determine_author(text, author_list, vocabulary, tot_doc_count):
	auth_res = {}
	doc = document("","",text)
	doc.count_sentence()
	doc.compute_ave_words_in_sentence()
	doc.count_quatation_mark()
	doc.count_exclamation_mark()
	bow = doc.construct_bow()
	for auth in author_list:
		auth_res[auth.name] = log(1.0 * auth.doc_count / tot_doc_count)
		for token, count in bow.items():
			token_pos = log((auth.vocabulary.get(token,0) + alpha) / (auth.tot_token_count + alpha * len(vocabulary)))
			auth_res[auth.name] += token_pos * count
		auth_res[auth.name] += abs(auth.ave_words_in_sentence - doc.ave_words_in_sentence) * word_coef
		auth_res[auth.name] += abs(auth.ave_sentence_count - doc.sentence_count) * sentence_coef
		auth_res[auth.name] += abs(auth.ave_quatation_mark - doc.quatation_mark_count) * quatation_coef
		auth_res[auth.name] += abs(auth.ave_exclamation_mark - doc.exclamation_mark_count) * exclamation_coef

	return sorted(auth_res, key=auth_res.get,reverse=True)[0]

# Returns a list of all files in given directory.
def traverse_dir(path):
	doc_list = []
	for root, dir, files in os.walk(path):
		for items in filter(files, "*"):
			doc_list.append(root + "/" + items)
	return doc_list

if __name__ == "__main__":
		
	# Read command line args
	parser = argparse.ArgumentParser(prog="author_recognizer", usage="./author_recognizer.py [options] ... [-r | -ns] [args] ... [training_path, test_path]", description='The script recognizes authors of the given article by using Naive Bayes.')
	parser.add_argument('-r','--result', action="store_false", default="True", help="Prints the result of the recognizer.",required=False)
	parser.add_argument('-c','--comparison', action="store_true", help="Prints the result of the recognizer with author of the document. (If parent directories of the articles are named as authors' names, it gives rational results. If this is in process, then not prints the results.)",required=False)
	parser.add_argument('-ns','--nostatistics', action="store_false", help="Does not print the statistics about recognition process.", required=False)
	parser.add_argument('training_path', nargs="?", default="training_dataset/", metavar='/path/to/training/set', help='Path to training dataset.')
	parser.add_argument('test_path', nargs="?", default="test_dataset/", metavar='/path/to/test/set', help='Path to test dataset.')
	args = parser.parse_args()

	print("training...")

	tot_doc_count = 0
	author_list = []
	for author_dir in os.listdir(args.training_path):
		auth = read_documents(args.training_path + author_dir)
		tot_doc_count += auth.doc_count
		author_list.append(auth)

	print("constructing vocabulary...")

	vocabulary = construct_vocabulary(author_list)

	if not args.result and not args.comparison:
		print("determining the author...")

	tp_total 	= 0
	tp_author 	= 0
	fp_total 	= 0
	fp_author 	= 0
	author_cnt 	= 0
	micro_ave_precision = 0
	macro_ave_precision = 0
	last_author = ""
	test_doc_list = traverse_dir(args.test_path)
	for doc_path in test_doc_list:
		if doc_path.endswith('.txt'):
			doc_text = open(doc_path,'r').read()
			author_name = os.path.basename(os.path.dirname(doc_path))
			determined_author_name = determine_author(doc_text, author_list, vocabulary, tot_doc_count)

			if args.result and not args.comparison:
				print("%-50s : %s%s%s" %(doc_path, HEADER, determined_author_name, ENDC))

			if last_author != "" and last_author != author_name:				
				macro_ave_precision += 1.0 * tp_author / (tp_author + fp_author)
				tp_author = 0
				fp_author = 0
				article_cnt_author = 0			
				author_cnt += 1

			if author_name == determined_author_name:
				tp_total += 1 
				tp_author += 1	
				sys.stdout.write("%s %-20s : %s %s \n" % (CLEAR, author_name, determined_author_name, ENDC) if args.comparison else ("." if not args.result else ""))
			else: 
				fp_total += 1
				fp_author += 1
				sys.stdout.write("%s %-20s : %s %s \n" % (FAIL, author_name, determined_author_name, ENDC) if args.comparison else ("." if not args.result else ""))

			last_author = author_name
			sys.stdout.flush()

	if not args.result and not args.comparison:
		sys.stdout.write("\ndone.\n")

	macro_ave_precision += 1.0 * tp_author / (tp_author + fp_author)
	macro_ave_precision /= (author_cnt+1)
	micro_ave_precision = 1.0 * tp_total / (tp_total + fp_total)
	if args.nostatistics:
		print("\n" + 94 * "-")
		print("|%s|%s|%s|" %(30 * " ", "{:^30}".format("Micro-averaged"), "{:^30}".format("Macro-averaged")))
		print(94 * "-")
		print("|%s|%s|%s|" %("{:^30}".format("Recall"),"{:^30.2f}".format(micro_ave_precision), "{:^30.2f}".format(macro_ave_precision)))
		print(94 * "-")
		print("|%s|%s|%s|" %("{:^30}".format("Precision"),"{:^30.2f}".format(micro_ave_precision), "{:^30.2f}".format(macro_ave_precision)))
		print(94 * "-")
		print("|%s|%s|%s|" %("{:^30}".format("F-Score"),"{:^30.2f}".format(micro_ave_precision), "{:^30.2f}".format(macro_ave_precision)))
		print(94 * "-")