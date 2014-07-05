#!/usr/bin/python
#-*- coding:utf-8 -*-

import re
import os
import sys
import ssfBlock
import modifySSF
import SanityChecker
import convert_inter
import convert_intra
import add_dummy_dependencies

def intra_chunk(inp_obj):
	global sent_id
	if tree is True:
		sentenceBlocks = ssfBlock.blockize(inp_obj, errorfile)
	else:
		sentenceBuffer = add_dummy_dependencies.INTRA(inp_obj)
		sentenceBlocks = ssfBlock.blockize(sentenceBuffer, errorfile)
	for block in sentenceBlocks:
		sentc=re.search('<Sentence id=\'[0-9]+\'>|<Sentence id=\"[0-9]+\">',block)
		cpSent = sentc.group()
		sent_id += 1
		sentNum.write(inp_obj+"  "+cpSent+"\t"+str(sent_id)+"\n")
		try:
			convert_intra.convertconll(block, tree)
		except:
			continue
		tflp=open('temp.conll','r');
		cont=tflp.read();
		tflp.close();
		os.system("rm temp.conll")
		outfilepointer.write(cont+"\n")
		errorConllfp.write(open("conllErrors.txt").read())

def read(inp):
	global sent_id
	#print inp,"opened for processing"
	if parseType is False:
		intra_chunk(inp)
	else:
		if tree is True:
			fp = open(inp,'r')
			errfreeSentences, errorSentences =  SanityChecker.Checker(fp)
		else:
			sentenceBuffer = add_dummy_dependencies.INTER(inp)
			errfreeSentences, errorSentences =  SanityChecker.Checker(sentenceBuffer)
		
		for line in errorSentences:
			errorfile.write(line+" "+inp+"\n")
		
		for sentence in errfreeSentences:
			sentc=re.search('<Sentence id=\'[0-9]+\'>|<Sentence id=\"[0-9]+\">',sentence)
			cpSent = sentc.group()
			temp1 = open("tempoutput1.txt","w")
			temp1.write(sentence+"\n")
			temp1.close()
			
			if (headAndVibFlag):			
				os.system("ulimit -t 10;sh $setu/src/sl/headcomputation-1.8/headcomputation_run.sh tempoutput1.txt > tempoutput2.txt")
				#os.system("rm tempoutput1.txt")
				os.system("ulimit -t 10;sh $setu/src/sl/vibhakticomputation-2.3.2/vibhakticomputation_run.sh tempoutput2.txt > tempoutput3.txt")
				#os.system("rm tempoutput2.txt")
				fpointer = open("tempoutput3.txt")
			elif (headAndVibFlag == False):
				fpointer = open("tempoutput1.txt")
			
			sent_id += 1
			try:
				sent = modifySSF.modify(fpointer)
			except Exception,e:
				print "Erroneous Sentence:",e
				print >> sys.stderr, sentence
				continue
			try:
				if convert_inter.convertconll(sent,tree) is False:
					#sent_id -= 1
					continue
				else:
					convert_inter.convertconll(sent,tree)
			except:
				print "Error File", inp,cpSent
				#sent_id -= 1
				continue
			
			tflp=open('temp.conll','r');
			cont=tflp.read();
			tflp.close(); 
			os.system("rm temp.conll")
			outfilepointer.write(cont)
			errorConllfp.write(open("conllErrors.txt").read())
			fpointer.close()
			#os.system("rm tempoutput3.txt")
			sentNum.write(inp+"  "+cpSent+"\t"+str(sent_id)+"\n")

def process(inp):
	if os.path.isfile(inp):
		read(inp)	
	else:
		for root,sub,files in os.walk(inp):
			for file in files:
				if file.endswith(".bak") or \
						file.startswith("task-"):continue
				#elif file.endswith(".posn"):
				Path = os.path.join(root,file)
				try:
					read(Path)
				except:
					print Path,"file has some error."

def main():
	global tree 
	global sent_id
	global parseType
	global headAndVibFlag
	global outfilepointer
	sent_id = int()
	parser = argparse.ArgumentParser(description="SSF to CONLL Convertor!")
	parser.add_argument('--input' , required=True  , help='Input in ssf format (file/folder)')
	parser.add_argument('--output-file' , dest='output', required=True  , help='Output conll file')
	parser.add_argument('--annotation', default='annotated', choices=['annotated', 'un-annotated'], help='(default: %(default)s), Specify whether input data is dependency annotated or not.')
	parser.add_argument('--annotation_type', default='inter-chunk', choices=['inter-chunk', 'intra-chunk'], help='(default: %(default)s), Specify whether input data has dependency annotation inter-chunk or intra-chunk.')
	parser.add_argument('--headAndVib_flag', default='Yes', choices=['Yes', 'No'], help='(default: %(default)s), Specify whether head and vibhakti computation is required or not.')
	args = parser.parse_args()

	tree = True
	if args.annotation == "un-annotated":
		tree = False
	
	parseType = True
	if args.annotation_type == "intra-chunk":
		parseType = False

	headAndVibFlag = True
	if args.headAndVib_flag == "No":
		headAndVibFlag = False

	outfilepointer = open(args.output,'w');
	data = process(args.input)

if __name__ == "__main__":
	import argparse
	errorfile    = open("errors.txt","a")
	sentNum      = open("sentence_num.log","w")
	errorConllfp = open("conllErrors.txt",'w')
	main()
	
	errorfile.close()
	outfilepointer.close()
	sentNum.close()
	os.system("rm conllErrors.txt")
