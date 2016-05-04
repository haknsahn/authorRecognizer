#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os, argparse, json
from Postag import Postag
from pprint import pprint
from locale import setlocale, LC_ALL

setlocale(LC_ALL, 'tr_TR.UTF-8')

def to_JSON(obj):
    return obj.to_JSON()

tag_cnts = {}
postags = {}
vocabulary = {}
if __name__ == "__main__":
		
	# Read command line args
	parser = argparse.ArgumentParser(prog="train_hmm_tagger", usage="./train_hmm_tagger.py [options] ... [--cpostag | --postag] [args] ... [training_file_path]", description='')
	parser.add_argument('--cpostag', action="store_true", default=False, help="",required=False)
	parser.add_argument('--postag', action="store_true", default=False, help="", required=False)
	parser.add_argument('training_file', nargs="?", default="./training_file.conll", metavar='/path/to/training/file', help='Path to training file.')
	args = parser.parse_args()

	lines = open(args.training_file,'r').readlines()

	tagIndex = -1
	if args.cpostag :
		tagIndex = 3
	elif args.postag :
		tagIndex = 4
	else :
		print("Select cpostag or postag !")
		sys.exit(0)

	prevTag = ""
	prevWord = ""
	for line in lines:
		if not line.strip():
			postags.setdefault("end",Postag("end"))
			postags["end"].addPrevTag(prevTag)
			postags["end"].addWord(prevWord)
			prevTag = ""
			prevWord = ""
			continue

		tokens = line.split()

		word 	= tokens[1]
		# lemma	= tokens[2]
		tag 	= tokens[tagIndex]

		postags.setdefault(tag,Postag(tag))

		if not prevTag :
			postags.setdefault("start",Postag("start"))
			postags["start"].addNextTag(tag)

		if prevTag and word != "_" :
			postags[tag].addPrevTag(prevTag)
			postags[prevTag].addNextTag(tag)

		if word != "_" :
			postags[tag].addWord(word)
			prevTag = tag
			prevWord = word

			vocabulary.setdefault(word, 0)
			vocabulary[word] += 1

		# if word.lower() != lemma and lemma != "_" :
		# 	postags[tag].addWord(lemma)

	for tag, postag in postags.items():
		postag.computeStats()

	model = {}
	model["postags"] = json.dumps(postags, default = to_JSON, ensure_ascii=False)
	model["vocabulary"] = json.dumps(vocabulary, ensure_ascii=False)

	with open("hmm_model", "w") as output :
		output.write(json.dumps(model))
















		



