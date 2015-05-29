#!/usr/bin/python -*- coding:utf-8 -*-

__Author__ = "Riyaz Ahmad Bhat"
__Email__ = "riyaz.ah.bhat@gmail.com"


import re
from collections import namedtuple

class SSFReader (object):
	
	def __init__ (self, sentence, annotation):

		self.sentence = sentence
		self.modifierModified = dict()
		self.nodeList = list()
		self.tokens = list()
		self.annotation = annotation
		self.node = namedtuple('node', 
					('wordForm', 'posTag', 'lemmaFeatures','headType','chunkId','projection',
							'depRel','parent','stype','voicetype'))
		self.features = namedtuple('features',
		('lemma','cat','gen','num','per','case','vib','tam'))

	def getAnnotations (self):

		wordForm_,posTag_,headType_,chunkId_,projection_,depRel_,parent_,stype_,voicetype_,\
		lemma_,cat_,gen_,num_,per_,case_,vib_,tam_, = [None]*17

		for line in self.sentence.split("\n"):
			if line.split("\t")[0].isdigit():
				assert len(line.split("\t")) is 4 # no need to process trash! FIXME
				keyValue_pairs = self.FSPairs(line.split("\t")[3][4:-1])
				for key,value in keyValue_pairs.items():
					if key == "af":
						lemma_,cat_,gen_,num_,\
						per_,case_,vib_,tam_ = \
								self.morphFeatures (value) 
					elif key == "name":
						if self.annotation == "inter":
							headType_ = re.sub("'|\"",'',value) #NOTE chunk id
							chunkId_ = re.sub("'|\"",'',value) #NOTE chunk name + counter
						elif self.annotation == "intra":
							headType_ = re.sub("'|\"",'',value) #NOTE word is used as word in deprel
						else:
							assert self.annotation in ["inter", "intra"]
					elif key == "chunkType":
						assert len(value.split(":")) is 2 # no need to process trash! FIXME
						projection_, chunkId_ = re.sub("'|\"",'',value).split(":")
						assert projection_ and chunkId_ != "" # no need to process trash! FIXME
					elif key == "head":
						wordForm_ = value
					elif key == "drel":
						assert len(value.split(":")) is 2 # no need to process trash! FIXME
						depRel_, parent_ = re.sub("'|\"",'',value).split(":")
						assert depRel_ and parent_ != "" # no need to process trash! FIXME
					elif key == "stype":
						stype_ = re.sub("'|\"",'',value)
					elif key == "voicetype":
						voicetype_ = re.sub("'|\"",'',value)
					else:pass
				if self.annotation == "intra":
					wordForm_,posTag_ = line.split("\t")[1:3]
					assert wordForm_.strip() and posTag_.strip() != ''
					if wordForm_ is not None: ## Ignore nodes whose head is not computed!
						self.nodeList.append(self.node(wordForm_,posTag_.decode("ascii",'ignore').encode(\
						"ascii"),self.features(lemma_,cat_,gen_,num_,per_,case_,vib_,tam_),\
						headType_,chunkId_,projection_,depRel_,parent_,stype_,voicetype_))
						self.modifierModified[headType_] = parent_
					wordForm_,posTag_,headType_,chunkId_,projection_,depRel_,parent_,stype_,voicetype_,\
					lemma_,cat_,gen_,num_,per_,case_,vib_,tam_, = [None]*17
					
					
			elif line.split("\t")[0].replace(".",'',1).isdigit():
				attributeValue_pairs = self.FSPairs(line.split("\t")[3][4:-1])
				#if re.search(re.escape(wordForm_), line):
                                if attributeValue_pairs['name'] == wordForm_:# NOTE head word of the chunk
					wordForm_,posTag_ = line.split("\t")[1:3]
					assert wordForm_.strip() and posTag_.strip() != '' # no need to process trash! FIXME
					self.tokens.append(('\t'.join(line.split("\t")[1:3]+[chunkId_])))
			else:
				if wordForm_ is not None: ## Ignore nodes whose head is not computed!
					self.nodeList.append(self.node(wordForm_,posTag_.decode("ascii",'ignore').encode("ascii"),\
					self.features(lemma_,cat_,gen_,num_,per_,case_,vib_,tam_),\
					headType_,chunkId_,projection_,depRel_,parent_,stype_,voicetype_))
					self.modifierModified[headType_] = parent_
				wordForm_,posTag_,headType_,chunkId_,projection_,depRel_,parent_,stype_,voicetype_,\
				lemma_,cat_,gen_,num_,per_,case_,vib_,tam_, = [None]*17
			
		return self

	def FSPairs (self, FS) :

		feats = dict()
		for feat in FS.split():
			if "=" not in feat:continue
			feat = re.sub("af='+","af='",feat.replace("dmrel=",'drel='))
			attribute,value = feat.split("=")
			feats[attribute] = value

		return feats

	def morphFeatures (self, AF):
		"LEMMA,CAT,GEN,NUM,PER,CASE,VIB,TAM"
		assert len(AF[:-1].split(",")) is 8 # no need to process trash! FIXME
		lemma_,cat_,gen_,num_,per_,case_,vib_,tam_ = AF.split(",")

		if len(lemma_.decode("utf-8")) > 1:
			lemma_ = lemma_.strip("'")
		else:
			lemma_ = lemma_
		
		return lemma_,cat_,gen_,num_,per_,case_,vib_,tam_.strip("'")

'''	
if __name__ == "__main__":

	import re
	import sys

	inputFile = open(sys.argv[1]).read()
	
	sentences = re.findall("<Sentence id=.*?>(.*?)</Sentence>",inputFile, re.S)
	for idx,sentence in enumerate(sentences):
		obj=SSFReader(sentence.strip(), 'inter').getAnnotations()
		for token in obj.tokens:print token
		#sys.exit()
#'''
