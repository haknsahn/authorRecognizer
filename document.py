#!/usr/bin/env python
# -*- coding: UTF-8-*-
from tokenizer import tokenize

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
	def constructBOW(self):
		if self.bow is not None:
			return self.bow

		self.bow = {}
		self.tokenize()
		for token in self.tokens:
			self.bow.setdefault(token, 0)
			self.bow[token] += 1
		return self.bow
