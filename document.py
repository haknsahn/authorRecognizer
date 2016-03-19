#!/usr/bin/env python
# -*- coding: UTF-8-*-
from tokenizer import tokenize, split_sentence, find_question_mark
from locale import setlocale, LC_ALL
setlocale(LC_ALL, 'tr_TR.UTF-8')

class document:
	def __init__(self, id, author, text):
		self.id = id
		self.author = author
		self.text = text
		self.tokens = None
		self.bow = None

	# Tokenizes the text.
	def tokenize(self):
		if self.tokens is None:
			self.tokens = tokenize(self.text)
		return self.tokens

	# Tokenizes the text and constructs 'Bag of Words' representation. 
	def construct_bow(self):
		if self.bow is not None:
			return self.bow

		self.bow = {}
		self.tokenize()
		for token in self.tokens:
			self.bow.setdefault(token, 0)
			self.bow[token] += 1
		return self.bow

	def count_sentence(self):
		return len(split_sentence(self.text))

	def compute_word_average(self):
		sentences = split_sentence(self.text)
		average = 0
		for sentence in sentences:
			average += len(tokenize(sentence))
		average /= 1.0 * len(sentences)
		return average

	def count_question_mark(self):
		return len(find_question_mark(self.text))
