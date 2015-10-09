#!/usr/bin/env python -*- coding:utf-8 -*-

import re
import os
import sys
import tempfile
import commands

def run_dependencies(input_):
	ssfSentences = re.finditer("(<Sentence id=.*?>)(.*?)</Sentence>", input_, re.S)
	headPath = "$ssf2conll/dependencies/headcomputation-1.8/"
	vibPath = "$ssf2conll/dependencies/vibhakticomputation/"

	for sentence in ssfSentences:
		sentenceId = sentence.group(1).replace("'", '"')
		sentence = re.sub(r"<fs name='NULL(.*?)'>",r"<fs af='null,unk,,,,,,' name='NULL\1'>",\
			   sentenceId+sentence.group(2)+"</Sentence>\n") 
			   # add af='' to null nodes.
		temp = tempfile.NamedTemporaryFile()
		try:
			temp.write(sentence)
			temp.seek(0)
			head=commands.getstatusoutput(\
				"ulimit -t 20;sh "+" "+ headPath+"headcomputation_run.sh "+" " + temp.name+" > head.txt")
			vib=commands.getstatusoutput(\
				"ulimit -t 20;sh "+" "+ vibPath+"vibhakticomputation_run.sh head.txt " + " >> " + output_)
		finally:
			temp.close()

		if "Killed" in [head[-1], vib[-1]]:
			print "Process killed! Something wrong either with head or vibhakhti computation!"	
			log_.write(sentencId.strip()+"#Error in head or vibhakhti computation\n")


if __name__ == "__main__":
	
	try:
		assert sys.argv[1] and sys.argv[2] and sys.argv[3]
	except Exception, error:
		print error, "in sys.argv, please specify the required arguments!"
		sys.exit()
	else:
		input_ = sys.argv[1]
		output_ = sys.argv[2]
		log_ = open(sys.argv[3],'a')
		if os.path.isfile(os.path.abspath(input_)):
			with open(input_) as inputFile: run_dependencies(inputFile.read())
		else:
			for root,sub,files in os.walk(input_):
				for file_ in files:
					path_ = os.path.join(root,file_)
					with open(path_) as inputFile: run_dependencies(inputFile.read())
	if os.path.isfile(os.path.abspath("head.txt")):
		os.remove(os.path.abspath("head.txt"))
	log_.close()
