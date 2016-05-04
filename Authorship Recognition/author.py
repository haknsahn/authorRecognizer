#!/usr/bin/env python
# -*- coding: UTF-8-*-
from locale import setlocale, LC_ALL
setlocale(LC_ALL, 'tr_TR.UTF-8')

class author:
	def __init__(self, name):
		self.id = id
		self.name = name
		self.doc_list = []
		self.vocabulary = {}
		self.doc_count = 0
		self.tot_token_count = 0
		self.ave_sentence_count = 0
		self.ave_words_in_sentence = 0
		self.ave_quatation_mark = 0
		self.ave_exclamation_mark = 0

	def compute_tot_token_count(self):
		for count in self.vocabulary.values():
			self.tot_token_count += count

	def get_doc_list(self):
		return doc_list

	def compute_ave_sentence_count(self):
		total_sentence_count = 0
		for doc in self.doc_list:
			total_sentence_count += doc.count_sentence()
		self.ave_sentence_count = 1.0 * total_sentence_count / self.doc_count
		return self.ave_sentence_count

	def compute_ave_words_in_sentence(self):
		total_ave_word = 0
		for doc in self.doc_list:
			total_ave_word += doc.compute_ave_words_in_sentence()
		self.ave_words_in_sentence = 1.0 * total_ave_word / self.doc_count
		return self.ave_words_in_sentence

	def compute_ave_quatation_mark(self):
		total_quatation_mark = 0
		for doc in self.doc_list:
			total_quatation_mark += doc.count_quatation_mark()
		self.ave_quatation_mark = 1.0 * total_quatation_mark / self.doc_count
		return self.ave_quatation_mark

	def compute_ave_exclamation_mark(self):
		total_exclamation_mark = 0
		for doc in self.doc_list:
			total_exclamation_mark += doc.count_exclamation_mark()
		self.ave_exclamation_mark = 1.0 * total_exclamation_mark / self.doc_count
		return self.ave_exclamation_mark