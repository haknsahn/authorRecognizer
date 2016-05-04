#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os, argparse, json
from Postag import Postag
from locale import setlocale, LC_ALL

setlocale(LC_ALL, 'tr_TR.UTF-8')

epsilon = 0.1 ** 4

def as_postag(dct):
	postag = Postag(dct["tag"])
	postag.add_objects(dct["words"],dct["wordStats"],dct["nextTags"],dct["nextTagStats"],dct["prevTags"],dct["prevTagStats"])
	return postag

def find_best_path(output, words, postags, vocabulary):
	viterbi_prob_matrix = [[0 for x in range(len(words))] for y in range(len(postags) + 2)] 	# A matrix with size N+2, T (N : # of postags, T : # of words) 
	back_pointer		= [[0 for x in range(len(words))] for y in range(len(postags) + 2)] 	# A matrix with size N+2, T (N : # of postags, T : # of words) 
	viterbi_indeces		= {}																	# A dictionary stores viterbi indeces of postags.

	index = 0
	for tag, _ in postags.items() :
		viterbi_indeces[tag] = index
		index += 1

	for tag, _ in postags.items() :
		viterbi_index = viterbi_indeces[tag]
		word_not_exist_stat = epsilon
		if words[0] in vocabulary :
			word_not_exist_stat = 0
		viterbi_prob_matrix[viterbi_index][0] = postags["start"].nextTagStats.get(tag,0) * postags[tag].wordStats.get(words[0],word_not_exist_stat)
		back_pointer[viterbi_index][0] = 0

	# for tag, index in viterbi_indeces.items() :
	# 	print(tag + " (" + str(index) + "): " + str(viterbi_prob_matrix[index]))

	for i in range(1,len(words)) :
		word = words[i]
		word_not_exist_stat = epsilon
		if word in vocabulary :
			word_not_exist_stat = 0
		for tag, _ in postags.items() :
			viterbi_index = viterbi_indeces[tag]
			max_prob, max_index = 0, 0
			for prev_tag, _ in postags.items() :
				prev_viterbi_index = viterbi_indeces[prev_tag]
				prob = viterbi_prob_matrix[prev_viterbi_index][i-1] * postags[prev_tag].nextTagStats.get(tag,0) * postags[tag].wordStats.get(word,word_not_exist_stat)
				if prob > max_prob :
					max_prob = prob
					max_index = prev_viterbi_index
			viterbi_prob_matrix[viterbi_index][i] 	= max_prob
			back_pointer[viterbi_index][i] 			= max_index

	viterbi_index = viterbi_indeces["end"]
	for prev_tag, _ in postags.items() :
		prev_viterbi_index = viterbi_indeces[prev_tag]
		prob =  viterbi_prob_matrix[prev_viterbi_index][i-1] * postags[prev_tag].nextTagStats.get("end",0)
		if prob > max_prob :
			max_prob = prob
			max_index = prev_viterbi_index

	viterbi_prob_matrix[viterbi_index][len(words)-1] = max_prob
	back_pointer[viterbi_index][len(words)-1] = prev_viterbi_index

	# for tag, index in viterbi_indeces.items() :
	# 	print(tag + " (" + str(index) + "): " + str(viterbi_prob_matrix[index]))

	for i in range(0, len(words)):
		max_prob = 0
		max_tag = ""
		for tag, index in viterbi_indeces.items() :
			if viterbi_prob_matrix[index][i] > max_prob :
				max_prob = viterbi_prob_matrix[index][i]
				max_tag = tag
		output.write(words[i] + " : " + max_tag + "\n")

postags = {}
vocabulary = {}
if __name__ == "__main__":

	# Read command line args
	parser = argparse.ArgumentParser(prog="hmm_tagger", usage="./hmm_tagger.py [args] ... [test_file_path | output_file_path]", description='')
	parser.add_argument('test_file', nargs="?", default="./blind_file.conll", metavar='/path/to/test/file', help='Path to test file.')
	parser.add_argument('output_file', nargs="?", default="./output.txt", metavar='/path/to/output/file', help='Path to output file.')
	args = parser.parse_args()

	try :
		with open("hmm_model", "r") as model_file :
			model_string = model_file.read()
	except FileNotFoundError :
		print("Model file not found : \"hmm_model\"") 
		sys.exit(1)

	model = json.loads(model_string)

	postag_json = model["postags"]
	vocabulary_json = model["vocabulary"]

	postags = json.loads(postag_json)
	vocabulary = json.loads(vocabulary_json)

	for tag , postag_dict in postags.items() :
		postag = as_postag(json.loads(postag_dict))
		postags[tag] = postag

	# for tag, postag in postags.items():
	# 	print(tag)
	# 	for word, _ in postag.words.items():
	# 		print("\t-> " + word + " : " + str(_))
	# 	print("--- prev ---")
	# 	for _tag, _ in postag.prevTagStats.items():
	# 		print("\t->" + _tag + " : " + str(_))
	# 	print("--- next ---")
	# 	for _tag, _ in postag.nextTagStats.items():
	# 		print("\t->" + _tag + " : " + str(_))

	try :
		with open(args.test_file,'r') as input_file :
			lines = input_file.readlines()
	except FileNotFoundError :
		print("Input file not found : " + args.output_file)

	sentences, words = [], []
	for line in lines:
		if not line.strip():
			if len(words) > 0 : 
				sentences.append(words)
				words = []
			continue
		tokens = line.split()
		if tokens[1] != "_" :
			words.append(tokens[1])
	
	if len(words) > 0 :
		sentences.append(words)

	with open(args.output_file, "w") as output :
		for sentence in sentences :
			find_best_path(output, sentence, postags, vocabulary)
			output.write("\n")