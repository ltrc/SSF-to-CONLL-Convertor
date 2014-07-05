#!/usr/local/bin/python
import os, sys, re

rel = re.compile(r"(?<=rel=)(.*?)\s|(?<=rel=)(.*)\b")
name = re.compile('(?<=name=)".*?"')


def recursion(Node):
	global listDone,cycle,child

	if Node in listDone:
		cycle = True
		return
	listDone.append(Node)

	for value in child[Node]:

		if value in child:
			recursion(value)


def Checker(Strbuffer):
	heads = list()
	line_number = 0
	chunks = list();
	Sentence = list();
	AllSentences = list();
	ErrorSentences = list();
	global listDone,cycle,child
	try:
		sentList = Strbuffer.split("\n")
	except:
		sentList = Strbuffer.readlines()

	for line in sentList:
		line_number +=1
		line = line.strip()

		if line.startswith("<Sentence id="):
			Root = 0;
			cycle = False
			child = dict()
			heads = list()
			chunks = list()
			Sentence = list()
			sent_id = line.replace("\'",'\"');
			Sentence.append(sent_id);
	
		elif line.startswith("</Sentence>"):
			Sentence.append(line+"\n")
			
			if Root > 1:
				sent_id = sent_id+" Error::Forest |"	
			elif Root == 0:
				sent_id = sent_id+" Error::Check for Forest No node with in-degree 0 |"
			if len(chunks) < 2:
				sent_id = sent_id+" Error::Single Chunk |"
			cycle = False
			
			for Head in heads:
				listDone = []

				if Head.strip() not in chunks:
					sent_id = sent_id+" Error::Check for Forest Alien parent in drel/dmrel -> "+Head+" |"
					break
				recursion(Head)

				if cycle:
					sent_id = sent_id+" Error::Check for Forest Cyclic Node -> "+Head+" |"
					break
			
			if "Error::" in sent_id:
				ErrorSentences.append(sent_id.strip("|"))
			else:
				AllSentences.append("\n".join(Sentence))
		
		else:
			tokens = line.split("\t")

			if line == "))":
				Sentence.append("\t"+line)

			elif tokens[0].isdigit(): ### Matches Non-terminal nodes in SSF (Non-terminals start with a digit)###

				if len(tokens) < 4:
					sent_id = sent_id+" Error::Check for Forest | Non-terminal coloums < 4 "+str(line_number)+" |"
				else:
					Sentence.append(line)

					try:
						Name = re.sub("[\"\']",'',name.search(line).group())
					except:
						Name = "Noname"
						sent_id = sent_id+" Error::Name Attribute Missing "+str(line_number)+" |"

					try:
						re.search("probsent_id",line,re.I).group()
						sent_id = sent_id+" Error::Problem Sentence "+str(line_number)+" |"
					except:
						pass
					
					if rel.search(line):
						items = re.sub("[\"\']",'',rel.search(line).group()).split(":")
						
						if len(items) < 2 or '' in items:
							sent_id = sent_id+" Error::Incomplete drel/dmrel value | Check for Forest"+str(line_number)+" |"
						else:
							karaka,head = items[0],items[-1].strip()
							heads.append(head)
							
							if head in child:
								child[head].append(Name)
							else:
								child[head] = [Name]
					else:
						Root += 1
					chunks.append(Name)

			elif (tokens[0].replace('.','',1)).isdigit(): ## Matches terminal nodes in SSF (terminals start with a float)###

				if len(tokens) < 4:
					sent_id = sent_id+" Error::Check for Forest | Non-terminal coloums < 4 "+str(line_number)+" |"
				else:

					if tokens[1] == "" or \
						tokens[2] == "" or tokens[3] == '' or \
								"af=" not in tokens[3] or \
								"name=" not in tokens[3]:
						sent_id = sent_id+" Error::Incomplete Terminal Node "+str(line_number)+" |"
				Sentence.append(line)

			else:
				pass

	return AllSentences, ErrorSentences
###	Call the function as : x,y = SanityChecker.Checker(filepointer)    ###

'''
if __name__ == "__main__":
	x,y = Checker(open(sys.argv[1]))
'''
