#!/usr/bin/env python
# -*- coding: UTF-8-*-

class author:
	def __init__(self, name):
		self.id = id
		self.name = name
		self.document_list = []
		self.vocabulary = {}
		self.doc_count = 0
		self.tot_token_count = 0

	def compute_tot_token_count(self):
		for count in self.vocabulary.itervalues():
			self.tot_token_count += count

	def add_document(self, id):
		self.document_list.append(id)		