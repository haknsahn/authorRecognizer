#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os, argparse, json
from Postag import Postag
from locale import setlocale, LC_ALL

setlocale(LC_ALL, 'tr_TR.UTF-8')

def splitSentences(lines, isGold):

	sentences, words = [], []
	for line in lines :
		if not line.strip() :
			if len(words) > 0 :
				sentences.append(words)
				words = []
			continue

		tokens = line.split()

		(word, tag) = (tokens[1], tokens[3]) if isGold else (tokens[0], tokens[2])

		if word != "_" :
			words.append((word, tag))
	if len(words) > 0 :
		sentences.append(words)

	return sentences  

if __name__ == "__main__":

	# Read command line args
	parser = argparse.ArgumentParser(prog="evaluate_hmm_tagger", usage="./evaluate_hmm_tagger.py [args] ... [output_file_path | gold_standard_file_path]", description='')
	parser.add_argument('output_file', nargs="?", default="./output.txt", metavar='/path/to/output/file', help='Path to output file.')
	parser.add_argument('gold_file', nargs="?", default="./gold_file.conll", metavar='/path/to/gold/standard/file', help='Path to gold standard file.')
	args = parser.parse_args()

	output_lines, gold_lines = [], []

	# Reads all lines from output and gold files.
	try :
		with open(args.output_file, "r") as outf :
			output_lines = outf.readlines()
	except FileNotFoundError :
		print("Output file not found : \"" + args.output_file + "\"") 
		sys.exit(0)

	try :
		with open(args.gold_file, "r") as goldf :
			gold_lines = goldf.readlines()
	except FileNotFoundError :
		print("Gold standard file not found : \"" + args.gold_file + "\"") 
		sys.exit(0)

	# Constructs sentences for each file.
	output_sentences = splitSentences(output_lines, False)
	gold_sentences = splitSentences(gold_lines, True)

	# Reads hmm_model in order to compute statistics of unknown words.
	try :
		with open("hmm_model", "r") as model_file :
			model_string = model_file.read()
	except FileNotFoundError :
		print("Model file not found : \"hmm_model\"") 
		sys.exit(0)

	model = json.loads(model_string)								# constructs a dictionary from model string.
	vocabulary_json = model["vocabulary"]
	vocabulary = json.loads(vocabulary_json)

	# first element is number of correct matching, second is number of wrong ones
	unknown_word_results = [0, 0]
	known_word_results = [0, 0]

	all_tags = []
	tag_results = {}
	tp, fp = 0, 0
	for output_sentence, gold_sentence in zip(output_sentences, gold_sentences) :							# Iterates over each sentences. 
		for (output_word, output_tag), (gold_word, gold_tag) in zip(output_sentence, gold_sentence) :		# Iterates over each word of a sentence.
			tag_results.setdefault(gold_tag, {})
			tag_results[gold_tag].setdefault(output_tag,0)
			tag_results[gold_tag][output_tag] += 1															# Increments the value of result table cell "gold_tag, output_tag"
			if output_word == gold_word and output_tag == gold_tag :										# So that we can see, our results for each tag separately.
				tp += 1
				if gold_word in vocabulary :
					known_word_results[0] += 1
				else :
					unknown_word_results[0] += 1
			else :																							# Computes "true positive" and "false positive" values.
				fp += 1
				if gold_word in vocabulary :
					known_word_results[1] += 1
				else :
					unknown_word_results[1] += 1

			if gold_tag not in all_tags :
				all_tags.append(gold_tag)																	# Gets all tags of gold file in order to print the results.

	print("General Statistics")
	print(" * True Matching : " + str(tp))
	print(" * False Matching : " + str(fp))
	print(" * Accuracy : " + str(1.0 * tp / (tp + fp)) + "\n")

	unknown_tp = unknown_word_results[0]
	unknown_fp = unknown_word_results[1]
	print("Unknown Word Statistics")
	print(" * True Matching : " + str(unknown_tp))
	print(" * False Matching : " + str(unknown_fp))
	print(" * Accuracy : " + str(1.0 * unknown_tp / (unknown_tp + unknown_fp)) + "\n")

	known_tp = known_word_results[0]
	known_fp = known_word_results[1]
	print("Known Word Statistics")
	print(" * True Matching : " + str(known_tp))
	print(" * False Matching : " + str(known_fp))
	print(" * Accuracy : " + str(1.0 * known_tp / (known_tp + known_fp)) + "\n")

	# Prints Confusion Matrix
	print("-" * 10 * (len(all_tags) + 1))
	print("{:>60}".format("Confusion Matrix"))
	print("-" * 10 * (len(all_tags) + 1))
	print("{:>60}".format("Output Tags"))
	print("-" * 10 * (len(all_tags) + 1))

	# First line of the result table.
	first_line = " " * 10
	for tag in all_tags :
		first_line += "{:10}".format(tag)
	print(first_line)
	print("-" * 10 * (len(all_tags) + 1))

	# Cells of the result table.
	for tag in all_tags :
		line = "{:10}".format(tag)
		for res_tag in all_tags :
			line += "{:10}".format(str(tag_results[tag].get(res_tag, 0)))
		print(line)
		print("-" * 10 * (len(all_tags) + 1))
	