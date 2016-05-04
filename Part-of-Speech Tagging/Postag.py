import json

class Postag:
	def __init__(self, tag):
		self.tag 			= tag
		self.words			= {}
		self.wordStats		= {}
		self.nextTags		= {}
		self.nextTagStats 	= {}
		self.prevTags		= {}
		self.prevTagStats 	= {}

	def add_objects(self, words, wordStats, nextTags, nextTagStats, prevTags, prevTagStats):
		self.words			= words
		self.wordStats		= wordStats
		self.nextTags		= nextTags
		self.nextTagStats 	= nextTagStats
		self.prevTags		= prevTags
		self.prevTagStats 	= prevTagStats

	def addWord(self, word):
		self.words.setdefault(word, 0)
		self.words[word] += 1

	def addPrevTag(self, tag):
		self.prevTags.setdefault(tag, 0)
		self.prevTags[tag] += 1

	def addNextTag(self, tag):
		self.nextTags.setdefault(tag, 0)
		self.nextTags[tag] += 1

	def computeStatsForDict(self, dictionary):
		total = 0
		for _, value in dictionary.items():
			total += value
		for _, value in dictionary.items():
			dictionary[_] = 1.0 * value / total
		return dictionary

	def computeStats(self):
		self.wordStats 		= self.computeStatsForDict(self.words)
		self.nextTagStats 	= self.computeStatsForDict(self.nextTags)
		self.prevTagStats 	= self.computeStatsForDict(self.prevTags)

	def to_JSON(self) :
		return json.dumps(self, default = lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)