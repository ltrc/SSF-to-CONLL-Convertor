#!/usr/bin/python
import os,sys,re

def INTER(fp):
	istChunk = None
	sentence = str()
	word_list = list()
	chunk_list = list()
	fpo = open(fp).readlines()
	dummyDependency = 'drel="dummy:'
	for line in fpo:
		line = line.rstrip()
		if line.startswith("</Sentence>"):
			sentence += line+"\n"
			word_list = list()
			chunk_list = list()
			continue
		if line.startswith("<Sentence id="):
			flag = True
			sentence += line+"\n"

		elif line.split("\t")[0].isdigit():
			chunk_list.append(line.split("\t")[2])
			if chunk_list.count(line.split("\t")[2]) == 1:
				new_chunk = 'name="'+line.split("\t")[2]
			else:
				new_chunk = 'name="'+line.split("\t")[2]+\
										str(chunk_list.count(line.split("\t")[2]))
			if re.search("<.*?>",line):
				if "name=" not in line:
					new_l = line.strip()[:-1]+" "+new_chunk+'">'
				else:
					new_l = line
			else:
					new_l = line.strip()+"\t<fs "+new_chunk+'">'
			if flag:
				flag = False
				istChunk = new_l.split("\t")[2]
				sentence += new_l+"\n"
			else:
				new_line = new_l.strip()[:-1]+" "+\
							dummyDependency+istChunk+'">'
				#new_line = line
				sentence += new_line+"\n"

		else:
			if line.split("\t")[0].replace('.','',1).isdigit():
				word_list.append(line.split("\t")[1].strip())	
				if word_list.count(line.split("\t")[1]) == 1:
					new_word = 'name="'+line.split("\t")[1]
				else:
					new_word = 'name="'+line.split("\t")[1]+\
											str(word_list.count(line.split("\t")[1]))
				if re.search("<.*?>",line):
					if "name=" not in line:
						new_l = line.strip()[:-1]+" "+new_word+'">'
					else:
						new_l = line
				else:
						new_l = line.strip()+"\t<"+new_word+'">'
				sentence += new_l+"\n"
			elif line.strip() == "))":
				sentence += line+"\n"
			else:
				pass; 'meta data'
	return sentence.strip()

def INTRA(fp):
	istNode = None
	sentence = str()
	word_list = list()
	fpo = open(fp).readlines()
	dummyDependency = 'drel="dummy:'
	for line in fpo:
		line = line.rstrip()

		if line.startswith("</Sentence>"):
			sentence += line+"\n"
			word_list = list()
			continue

		if line.startswith("<Sentence id="):
			flag = True
			sentence += line+"\n"

		elif line.split("\t")[0].isdigit():
			word_list.append(line.split("\t")[1].strip())	

			if word_list.count(line.split("\t")[1]) == 1:
				new_word = 'name="'+line.split("\t")[1]
			else:
				new_word = 'name="'+line.split("\t")[1]+\
						str(word_list.count(line.split("\t")[1]))

			if re.search("<.*?>",line):
				if "name=" not in line:
					new_l = line.strip()[:-1]+" "+new_word+'">'
				else:
					new_l = line
			else:
					new_l = line.strip()+"\t<"+new_word+'">'

			if flag:
				flag = False
				istNode = line.split("\t")[1]
				sentence += new_l+"\n"
			else:
				new_line = new_l.strip()[:-1]+" "+\
						dummyDependency+istNode+'">'
				sentence += new_line+"\n"
		else:
			pass; 'meta data'
	return sentence.strip()


def main ():
	s = INTRA(sys.argv[1])
	#s = INTER(sys.argv[1])
	for x in s.split("\n"):
		print x
if __name__ =="__main__":
	main()

