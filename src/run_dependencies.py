#!/usr/bin/env python -*- coding:utf-8 -*-


def run_dependencies(inputFile):
	sentencIds = re.findall('<Sentence id=(.*?)>', inputFile) 
	ssfSentences = re.findall("<Sentence id=.*?>(.*?)</Sentence>", inputFile,re.S)
	headPath = "/home/riyaz/Tools/ssf2conllconverter/ssf2conll_convertor/dependencies/headcomputation-1.8/"
	vibPath = "/home/riyaz/Tools/ssf2conllconverter/ssf2conll_convertor/dependencies/vibhakticomputation-2.3.4/"

	for idx, sentence in enumerate(ssfSentences):
		sentence = re.sub(r"<fs name='NULL(.*?)'>",r"<fs af='null,unk,,,,,,' name='NULL\1'>",\
								 '<Sentence id="'+str(sentencIds[idx])[1:-1]+'">\n'+sentence.strip()+"\n</Sentence>\n") # add af='' to null nodes.
		temp = tempfile.NamedTemporaryFile()
		try:
			temp.write(sentence)
			temp.seek(0)
			head=commands.getstatusoutput("ulimit -t 20;sh "+" "+ headPath+"headcomputation_run.sh "+" " + temp.name+" > head.txt")
			vib=commands.getstatusoutput("ulimit -t 20;sh "+" "+ vibPath+"vibhakticomputation_run.sh head.txt >> " + output_)
		finally:
			temp.close()

		if "Killed" in [head[-1], vib[-1]]:
			print "Process killed! Something wrong either with head or vibhakhti computation!"	
			log_.write("<Sentence id="+str(sentencIds[idx])+">"+"#Error in head or vibhakhti computation\n")


if __name__ == "__main__":
	
	import re
	import os
	import sys
	import tempfile
	import commands

	try:
		assert sys.argv[1] and sys.argv[2] and sys.argv[3]
	except Exception, error:
		print error, "in sys.argv, please specify the required arguments!"
	else:
		input_ = sys.argv[1]
		log_ = open(sys.argv[3],'a')
		output_ = sys.argv[2]
		if os.path.isfile(input_):
			run_dependencies(open(input_).read())
		else:
			for root,sub,files in os.walk(input_):
				for file_ in files:
					path = os.path.join(root,file_)
					run_dependencies(open(path).read())
	if os.path.isfile("head.txt"):
		os.remove("head.txt")
	log_.close()
