#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os, argparse, json
from Postag import Postag
from locale import setlocale, LC_ALL

setlocale(LC_ALL, 'tr_TR.UTF-8')

epsilon = 0.1 ** 4

# Constructs a POSTAG object from given dictionary.
def as_postag(dct):
	postag = Postag(dct["tag"])
	postag.add_objects(dct["words"],dct["wordStats"],dct["nextTags"],dct["nextTagStats"],dct["prevTags"],dct["prevTagStats"])
	return postag

# Offers postag sequence with best score by using hmm.  
def find_best_path(output, words, postags, vocabulary):
	viterbi_prob_matrix = [[0 for x in range(len(words))] for y in range(len(postags) + 2)] 	# A matrix with size N+2, T (N : # of postags, T : # of words) 
	back_pointer		= [[0 for x in range(len(words))] for y in range(len(postags) + 2)] 	# A matrix with size N+2, T (N : # of postags, T : # of words) 
	viterbi_indeces		= {}																	# A dictionary stores viterbi indeces of postags.

	index = 0
	for tag, _ in postags.items() :																# Determines viterbi indeces of each tag, to use for viterbi probability matrix. 
		viterbi_indeces[tag] = index
		index += 1

	for tag, _ in postags.items() :																# Computes initial scores for each tag.
		viterbi_index = viterbi_indeces[tag]													# -> Possibility of a tag's being first tag of a sentence. 
		word_not_exist_stat = epsilon if words[0] not in vocabulary else 0						# If the word is not exist in vocabulary, then its scores becomes epsilon for all tags.
		viterbi_prob_matrix[viterbi_index][0] = postags["start"].nextTagStats.get(tag,0) * postags[tag].wordStats.get(words[0],word_not_exist_stat)
		back_pointer[viterbi_index][0] = 0

	for i in range(1,len(words)) :																# for each words other than the first word.
		word = words[i]
		word_not_exist_stat = epsilon if word not in vocabulary else 0							# If the word is not exist in vocabulary, then its scores becomes epsilon for all tags.
		for tag, _ in postags.items() :															# Computations related to HMM.
			viterbi_index = viterbi_indeces[tag]												# For each tag, computes the probability with using probability of previous sequences.
			max_prob, max_index = 0, 0
			for prev_tag, _ in postags.items() :
				prev_viterbi_index = viterbi_indeces[prev_tag]
				prob = viterbi_prob_matrix[prev_viterbi_index][i-1] * postags[prev_tag].nextTagStats.get(tag,0) * postags[tag].wordStats.get(word,word_not_exist_stat)
				if prob > max_prob :
					max_prob = prob
					max_index = prev_viterbi_index
			viterbi_prob_matrix[viterbi_index][i] 	= max_prob									# For each tag, stores maximum probability scores in order to continue computation.
			back_pointer[viterbi_index][i] 			= max_index


	# End tag is not used for this version, since while determing postag of a word, previous postag is used only.
	# viterbi_index = viterbi_indeces["end"]
	# for prev_tag, _ in postags.items() :
	# 	prev_viterbi_index = viterbi_indeces[prev_tag]
	# 	prob =  viterbi_prob_matrix[prev_viterbi_index][i-1] * postags[prev_tag].nextTagStats.get("end",0)
	# 	if prob > max_prob :
	# 		max_prob = prob
	# 		max_index = prev_viterbi_index

	# viterbi_prob_matrix[viterbi_index][len(words)-1] = max_prob
	# back_pointer[viterbi_index][len(words)-1] = prev_viterbi_index

	# for tag, index in viterbi_indeces.items() :
	# 	print(tag + " (" + str(index) + "): " + str(viterbi_prob_matrix[index]))

	# Iterates over viterbi probability matrix and gives the best result for each word.
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
		sys.exit(0)

	model = json.loads(model_string)								# constructs a dictionary from model string.

	postag_json = model["postags"]									# gets postag and vocabulary strings from the dictionary.
	vocabulary_json = model["vocabulary"]

	postags = json.loads(postag_json)								# contructs postags and vocabulary dictionaries from related strings.
	vocabulary = json.loads(vocabulary_json)

	for tag , postag_dict in postags.items() :						# converts string values of postags dictionary into POSTAG objects.
		postag = as_postag(json.loads(postag_dict))
		postags[tag] = postag

	try :
		with open(args.test_file,'r') as input_file :
			lines = input_file.readlines()
	except FileNotFoundError :
		print("Input file not found : " + args.output_file)

	sentences, words = [], []
	for line in lines:												# gets all words from test file and constructs sentences
		if not line.strip():										# and stores them into related lists.
			if len(words) > 0 : 
				sentences.append(words)
				words = []
			continue
		tokens = line.split()
		if tokens[1] != "_" :
			words.append(tokens[1])
	
	if len(words) > 0 :												# after the process if word list still contains some words,
		sentences.append(words)										# adds them into sentences list.

	with open(args.output_file, "w") as output :
		for sentence in sentences :
			find_best_path(output, sentence, postags, vocabulary)	# finds postags for each words in the sentences list and writes them into output file.
			output.write("\n")