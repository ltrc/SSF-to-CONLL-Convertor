#!/usr/bin/env python -*- coding: utf-8 -*-

__Author__ = "Riyaz Ahmad Bhat"
__Email__  = "riyaz.ah.bhat@gmail.com"

from ssfReader import SSFReader


class SanityChecker (SSFReader) :

	def __init__(self, sentence, annotation):
		super(SanityChecker, self).__init__(sentence, annotation)
		self.getAnnotations()

		""" Super Class Methods and Attributes
		self.modifierModified = dict()
    self.nodeList = list()
    self.node = namedtuple('node',
    ('wordForm', 'posTag', 'lemmaFeatures', 'chunkType', 'depRel', 'parent', 'stype','voicetype'))
    self.features = namedtuple('features',
    ('lemma','cat','gen','num','per','case','vib','tam')) """

	def ifCycle_ (self, node_):	
		parent_ = self.modifierModified[node_]
		if parent_ is None:
			return
		else:
			self.ifCycle_(parent_)

	def treeSanity(self):
		if (self.nodeList) < 2:
			return "#single chunk sentence"
		else:
			if self.modifierModified.values().count(None) is 0:
				return "#Root-less tree"
			elif self.modifierModified.values().count(None) > 1 or len(\
					[None for i in self.nodeList if i.depRel is None]) > 1:
				return "#Forest, mulitple roots"
			elif len(set(self.modifierModified.values()) - set(self.modifierModified.keys())) > 1:
				difference = set(self.modifierModified.values()) - set(self.modifierModified.keys())
				difference.remove(None)
				return "#Unknown head(s) as "+"\t".join(difference)
			else:# cycle
				for node_ in self.modifierModified.keys():
					try:
						self.ifCycle_(node_)
					except Exception,e:
						return "#cycle in "+node_+"\t"+self.modifierModified[node_]


'''
if __name__ == "__main__":

	import re
	import sys

	inputFile = open(sys.argv[1]).read()
	
	sentences = re.findall("<Sentence id=.*?>(.*?)</Sentence>",inputFile, re.S)

	for idx,sentence in enumerate(sentences):
		try:
			obj=SanityChecker(sentence.strip())
			check_ = "".join(obj.treeSanity())
			print check_
			print sentence
		except:pass
		
		#if check_:print check_
'''
