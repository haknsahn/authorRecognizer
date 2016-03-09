#!/usr/bin/env python
# -*- coding: UTF-8-*-
from re import findall

# Uses an regex in  order to match all tokens of given text. 
# Before tokenization, text is converted to lower case.
def tokenize(text):
	return findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", text.lower())