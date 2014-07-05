#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Aim: Aim of this code is to check the sanity and format of ssf blocks in the 
#
# This code intends to check validity of several formats, features and attributes and their relations.
#
# The working of code is simple - 
#	1) Check if the file can be divided into ssf blocks
#	2) Check for errors in the ssf format of the block.
#	3) run several sanity checks based on the features.
#	4) Report errors for all descripancies
#
# Contact: Jayendra Rakesh, jayendra.rakesh@gmail.com
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import re, os, sys

#///////////////////////////////////////////////////////////////////
#   Blockize creates text segments that contain an ssf sentence
#///////////////////////////////////////////////////////////////////

def blockize(fl,erflp):
	try:
		lines = open(fl).readlines()
	except:
		lines = [i.strip()+"\n" for i in fl.split("\n")]
	#erflp=open(erfl,"a");
	
	tempBlock='';
	state=0;
	blocks=[];
	blockID=[];
	for i in lines:
		if(i[0:10]=='<Sentence ' or i[0:10]=='<sentence '):
			state=1;
			tempBlock+=i;
			#
			# Check if block id is consistent
			#
			'''group=re.search('(id=\'[0-9]+\')|(id=\"[0-9]+\")',i);
			if(not group):
				print '\t\t'+i
			strnum=group.group();
			num=strnum.split('=');
			num=num[1][1:-1];
			sid=int(num);
			if sid not in blockID:
				if(len(blockID)==0):
					blockID.append(sid);
				elif(blockID[-1]==sid-1):
					blockID.append(sid);
				else:
					Error="\tBlock id inconsistent between "+str(blockID[-1])+' - '+str(sid)+'\n';
					#print '\t'+Error[:-1];
					#erflp.write(Error);
					blockID.append(sid);
			else:
				Error="\tBlock id="+str(sid)+" repeated after "+str(blockID[-1])+'\n';
				#erflp.write(Error);
				#print '\t'+Error[:-1];'''
		elif(state==1 and (i[0:10]=='</Sentence' or i[0:10]=='</sentence')):
			state=0;
			tempBlock+=i;
			blocks.append(tempBlock);
			tempBlock='';
		elif(state==1):
			tempBlock+=i;
	erflp.close();
	return blocks;

def ssfCheck(text,erfl):
	erflp=open(erfl,"a");
	lines=text.split('\n');
	group=re.search('(id=\'[0-9]+\')|(id=\"[0-9]+\")',lines[0]);
	strnum=group.group();
	num=strnum.split('=');
	num=num[1][1:-1];
	sid=int(num);
	lines=lines[1:-2];
	chunkCount=0;

	# Check for chunk bracket matching
	
	for line in lines:					
		split=line.split('\t');
		if(split[1]=='(('):
			chunkCount+=1;
		elif(split[1]=='))'):
			chunkCount-=1;
			if(chunkCount<0):
				Error="\tChunk Count missing in sentence:"+str(sid)+'\n';
				print '\t'+Error[:-1];
				erflp.write(Error);
				return [False,sid,''];

	# Check for addresses based on expected addresses.

	chunkID=0;
	state=0;
	counter=1;
	subCounter=0;
	for line in lines:					
		split=line.split('\t');
		if(split[1]=='(('):
			state=1;
			expID=str(counter);
			if(split[0]!=expID):			# Check if Chunk addresss is valid
				Error="\tChunk Address not as expected in sentence:"+str(sid)+'\n';
				print '\t'+Error[:-1];
				erflp.write(Error);
				return [False,sid,''];
			else:
				counter+=1;
				subCounter+=1;
				chunkID=split[0];
		elif(state==1):
			if(split[1]=='))'):
				state=0;
				subCounter=0;
			else:
				expID=chunkID+'.'+str(subCounter);
				if(split[0]!=expID):		# Check if Node address is valid
					Error="\tNode Address not as expected in sentence: "+str(sid)+'\n';
					print '\t'+Error[:-1];
					erflp.write(Error);
					return [False,sid,''];
				else:
					subCounter+=1;

	# Check for 4 field entries exception is ending chunk bracket

	# Check if fs field is structured as the format <fs x='y' p='q'>
	flag=0;
	sentence='';
	for line in lines:
		split=line.split('\t');
		if(split[1]!='((' and split[1]!='))' and split[1]!='-JOIN'):
			sentence+=split[1]+' ';
		if(split[1]=='))'):
			if(len(split)!=2):
				Error="\tExtra fields in sentence: "+str(sid)+" in chunk at Close bracket\n";
				#print '\t'+Error[:-1];
				#erflp.write(Error);
				flag=1;
		else:
			if(len(split)!=4 or ('' in split)):
				Error="\tMissing or extra fields in sentence: "+str(sid)+"  in chunk: "+split[0]+"\n";
				#print '\t'+Error[:-1];
				#erflp.write(Error);
				flag=1;
			else:       # check if <fs> tag is in structure
				fs=split[3];
				cid=split[0];
				if(fs[0:3]!='<fs' or fs[-1]!='>'):
					Error="\tWrong feature structure in sentence: "+str(sid)+" in chunk: "+cid+'\n';
					#print '\t'+Error[:-1];
					#erflp.write(Error);
					flag=1;
				else:
					fs=fs[3:-1];
					fsSplit=fs.split(' ');
					for i in fsSplit:
						if(i!=''):
							if(re.search('.+=\'.*\'',i)):
								do="nothing"
							else:
								Error="\tWrong feature structure attributes in sentence: "+str(sid)+" in chunk: "+cid+'\n';
								#print '\t'+Error[:-1];
								#erflp.write(Error);
								flag=1;
	
	if(flag==1):
		return [False,sid,sentence[:-1]];
	return [True,sid,sentence[:-1]];

#if(len(sys.argv)>2):
#	fl=sys.argv[1];
#	erfl=sys.argv[2];
#else:
#	print "Args missing";
#	sys.exit(0);

#for block in blockize(fl,erfl):
#	ssfCheck(block,erfl);
