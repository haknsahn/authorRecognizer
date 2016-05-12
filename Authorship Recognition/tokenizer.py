#!/usr/bin/env python
# -*- coding: UTF-8-*-
from re import findall, sub, compile, I
from locale import setlocale, LC_ALL
from sys import version_info
setlocale(LC_ALL, 'tr_TR.UTF-8')

# Uses an regex in  order to match all tokens of given text. 
# Before tokenization, text is converted to lower case.
def tokenize(text):

	# Seems to be not working.
	# if version_info >= (3,0):
		# text = text.lower()												# Lowers the all characters.
	# else:	
	# 	text = text.decode("utf8").lower().encode("utf8")				# In python2, it is needed to decode UTF-8 characters in order to lower them.

	text = text.lower()													# Lowers the all characters.

	text = sub("['’`][\wçğıöşü]+(?=[^\wçğıöşü'’`])","",text)			# removes additions with apostrophe(',’,`) mark. Ex. İstanbul('un)
	text = sub("-","",text)												# removes '-' marks.
	text = sub("[^\w\d\sçğıöşü]"," ",text)								# substitutes remaining punctuation marks with space(" ").
	return findall("[\wçğıöşü]{3,}", text)								# finds all words with 3 or more characters.


def split_sentence(text):
	return findall("(?=[A-Z0-9ÇĞİÖŞÜ“])(?:.|\n)*?[.!?:](?![.!?'\"”0-9])",text)

def find_quatation_mark(text):
	return findall("\"",text)

def find_exclamation_mark(text):
	return findall("!",text)
