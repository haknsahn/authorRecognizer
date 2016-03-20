#!/usr/bin/env python
# -*- coding: UTF-8-*-
import tokenizer
from locale import setlocale, LC_ALL
setlocale(LC_ALL, 'tr_TR.UTF-8')

class document:
	def __init__(self, id, author, text):
		self.id = id
		self.author = author
		self.text = text
		self.tokens = None
		self.bow = None
		self.sentence_count = 0
		self.ave_words_in_sentence = 0
		self.quatation_mark_count = 0
		self.exclamation_mark_count = 0

	# Tokenizes the text.
	def tokenize(self):
		if self.tokens is None:
			self.tokens = tokenizer.tokenize(self.text)
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
		self.sentence_count = len(tokenizer.split_sentence(self.text))
		return self.sentence_count

	def compute_ave_words_in_sentence(self):
		sentences = tokenizer.split_sentence(self.text)
		average = 0
		for sentence in sentences:
			average += len(tokenizer.tokenize(sentence))
		self.ave_words_in_sentence = 1.0 * average / len(sentences)
		return self.ave_words_in_sentence

	def count_quatation_mark(self):
		self.quatation_mark_count = len(tokenizer.find_quatation_mark(self.text))
		return self.quatation_mark_count

	def count_exclamation_mark(self):
		self.exclamation_mark_count = len(tokenizer.find_exclamation_mark(self.text))
		return self.exclamation_mark_count
