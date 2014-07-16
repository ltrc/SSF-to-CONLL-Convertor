#!/usr/bin/env python -*- coding: utf-8 -*-

__Author__ = "Riyaz Ahmad Bhat"
__Email__  = "riyaz.ah.bhat@gmail.com"


from ssfReader import SSFReader
from sanityChecker import SanityChecker

class ConllConvertor (SanityChecker):

	def __init__(self, sentence):
		super(ConllConvertor, self).__init__(sentence)
		self.check_ = self.treeSanity()
		
		""" Super Class Methods and Attributes
		self.modifierModified = dict()
    self.nodeList = list()
    self.node = namedtuple('node',
    ('wordForm', 'posTag', 'lemmaFeatures', 'chunkType', 'depRel', 'parent', 'stype','voicetype'))
    self.features = namedtuple('features',
    ('lemma','cat','gen','num','per','case','vib','tam'))
		getAnnotations()
		treeSanity()
		"""

	def convert (self):
		""" 															--- Conll Formatt	---
		1	kAmU	kAmU	n	NNP	lex-kAmU|cat-n|gen-m|num-sg|pers-3|case-d|vib-0|tam-0|chunkId-NP|stype-|voicetype-	2	spr	_	_
		"""
		if self.check_:
			yield "#Error :: "+self.check_
		else:
			for idx, node in enumerate(self.nodeList):

				if node.parent is None and node.depRel is None:
					head_ = "0"
					relation_ = "main"
				else:
					head_ = [str(idy+1) for idy, nodey in enumerate(self.nodeList) if nodey.chunkType == node.parent][0]
					relation_ = node.depRel

				if node.lemmaFeatures.lemma is None:
					lemma_ = node.wordForm.lower()
				else:
					lemma_ = node.lemmaFeatures.lemma

				if node.lemmaFeatures.cat in [None,'']:
					cat_ = node.posTag.lower()
				else:
					cat_ = node.lemmaFeatures.cat

				features = "lex-%s|cat-%s|gen-%s|num-%s|pers-%s|case-%s|vib-%s|tam-%s|chunkId-%s|stype-%s|voicetype-%s" \
										% (node.wordForm,node.lemmaFeatures.cat,node.lemmaFeatures.gen,\
										node.lemmaFeatures.num,node.lemmaFeatures.per,node.lemmaFeatures.case,\
										node.lemmaFeatures.vib,node.lemmaFeatures.tam,node.chunkType,node.stype,node.voicetype)
				features_ = re.sub("None",'',features)
				yield "\t".join((str(idx+1),node.wordForm,lemma_,cat_,node.posTag,features_,head_,relation_.lower(),"_","_"))

if __name__ == "__main__":

	import os
	import re
	import sys
	import argparse
	
	parser = argparse.ArgumentParser(description="SSF to CONLL Convertor!")
	parser.add_argument('--input-file' , dest='input', required=True  , help='Input file in ssf format')
	parser.add_argument('--output-file' , dest='output', required=True  , help='Output conll file')
	parser.add_argument('--log-file' , dest='log', required=True  , help='will contain processing details')
	
	args = parser.parse_args()

	if os.path.isfile(args.output):
		outputFile = open(args.output,'a')
	else:
		outputFile = open(args.output,'w')
	
	if os.path.isfile(args.log):
		logFile = open(args.log,'a')
	else:
		logFile = open(args.log,'w')

	inputFile = open(args.input).read()
	
	sentence_ids = re.findall('<Sentence id=(.*?)>', inputFile)
	sentences = re.findall("<Sentence id=.*?>(.*?)</Sentence>",inputFile, re.S)

	filePath = os.path.abspath(args.input)
	for idx,sentence in enumerate(sentences):
		try:
			convertor_object = ConllConvertor(sentence.strip())
			output_ = "\n".join(convertor_object.convert())
		except:
			#logFile.write(filePath+" "+sentence_ids[idx]+" #Error :: Wrong ssf formatt!\n")
			logFile.write("<Sentence id='"+sentence_ids[idx]+"'>"+" #Error :: Wrong ssf formatt!\n")
		else:
			if output_.startswith("#Error"):
				logFile.write("<Sentence id='"+sentence_ids[idx]+"'>"+" "+output_+"\n")
			else:
				outputFile.write(output_+"\n\n")
				logFile.write("<Sentence id="+sentence_ids[idx]+"'>"+" converted\n")


logFile.close()
outputFile.close()		
