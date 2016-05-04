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

	try :
		with open(args.training_file,'r') as training_file :
			lines = training_file.readlines()
	except FileNotFoundError :
		print("Training file not found : " + args.training_file) 
		sys.exit(0)

	tagIndex = -1
	if args.cpostag :
		tagIndex = 3
	elif args.postag :
		tagIndex = 4
	else :
		print("Select cpostag (--cpostag) or postag (--postag) !")
		sys.exit(0)

	prevTag = ""
	prevWord = ""
	for line in lines:
		if not line.strip():											# End of a sentence.
			postags.setdefault("end",Postag("end"))						# end added as a tag
			postags["end"].addPrevTag(prevTag)
			postags["end"].addWord(prevWord)
			prevTag = ""
			prevWord = ""
			continue

		tokens = line.split()

		word 	= tokens[1]
		# lemma	= tokens[2]												# lemmas ignored.
		tag 	= tokens[tagIndex]

		postags.setdefault(tag,Postag(tag))

		if not prevTag :												# if there is no tag before, then
			postags.setdefault("start",Postag("start"))					# current tag is added into next tag list of start tag.
			postags["start"].addNextTag(tag)

		if prevTag and word != "_" :									# if there is a prevtag and the word is not empty, then
			postags[tag].addPrevTag(prevTag)							# previous tag added to prev tag list of current tag.
			postags[prevTag].addNextTag(tag)							# and current tag added to next tag list of previous tag. 

		if word != "_" :												# if the word is not empty, then
			postags[tag].addWord(word)									# the word added to word list of current tag.
			prevTag = tag 												# previous tag and previous word variables are updated.
			prevWord = word

			vocabulary.setdefault(word, 0)								# the word added to vocabulary.
			vocabulary[word] += 1

		# if word.lower() != lemma and lemma != "_" :
		# 	postags[tag].addWord(lemma)

	for tag, postag in postags.items():									# all statistics related to a postag object are computed.
		postag.computeStats()

	model = {}																			# a dictionary is constructed
	model["postags"] = json.dumps(postags, default = to_JSON, ensure_ascii=False)		# in order to store trained model into a file.
	model["vocabulary"] = json.dumps(vocabulary, ensure_ascii=False)

	with open("hmm_model", "w") as output :												# the model is written into file.
		output.write(json.dumps(model))
