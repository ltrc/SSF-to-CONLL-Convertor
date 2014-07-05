# This script converts the input ssf format data into conll format
# This script takes input the ssf-file name which has to be converted
# as a command line argument and outputs the conll format into temp.conll
#by Jayend Rakesh and Vishnu

import os,sys,re

def convertconll(block,drel_flag):
	fw = open("temp.conll",'w')
	errfp = open("conllErrors.txt",'w')
	lines = block.split('\n')
	lines = lines[1:-2]
	names = []
	wforms =[]
	linenum = []
	fpos = []
	lex = []
	cpos = []
	gen = []
	num = []
	pers = []
	case = []
	vib = []
	tam = []
	chunkId = []
	chunkType = []
	drel = []
	err = 0
	ents = []
	stype = []
	voice = []
	for j in range(len(lines)):
		chunk_flag = 0
		af = ''
		#print lines[j]
		linenum.append(lines[j].split('\t')[0])
		wforms.append(lines[j].split('\t')[1])
		fpos.append(lines[j].split('\t')[2])
		ents = lines[j].split('\t')[3][4:-1].split(' ')
		flag_stype = 0
		flag_voice = 0
		for m in range(len(ents)):
			if ((ents[m].find('af='))+1):
				af = ents[m]
			if ((ents[m].find('name='))+1):
				names.append(ents[m].split('=')[1].split("'")[1])
				#print names;
			if ((ents[m].find('chunkType='))+1):
				chunkType.append(ents[m].split('=')[1].split("'")[1].split(":")[0])
#				print chunkType
				chunk_flag = 1
				chunkId.append(ents[m].split('=')[1].split("'")[1].split(":")[1])
			if ((ents[m].find('stype='))+1):
				stype.append(ents[m].split('=')[1].strip("'"))
				flag_stype = 1
			if ((ents[m].find('voicetype='))+1):
				voice.append(ents[m].split('=')[1].strip("'"))
				flag_voice = 1
#			elif(ents[m].find('chunkType') == -1):
#				chunkType.append('')
#				chunkId.append('')
		if (chunk_flag == 0):
			chunkType.append('')
			chunkId.append('')

		if (flag_stype == 0):
			stype.append('')

		if (flag_voice == 0):
			voice.append('')

		if (af != ''):
			lex.append(af.split('=')[1].split(',')[0].strip("'"))
			cpos.append(af.split('=')[1].split(',')[1])
			gen.append(af.split('=')[1].split(',')[2])
			num.append(af.split('=')[1].split(',')[3])
			pers.append(af.split('=')[1].split(',')[4])
			case.append(af.split('=')[1].split(',')[5])
			vib.append(af.split('=')[1].split(',')[6])
			tam.append(af.split('=')[1].split(',')[7].strip("'"))
		else:
			lex.append('')
			cpos.append('')
			gen.append('')
			num.append('')
			pers.append('')
			case.append('')
			vib.append('')
			tam.append('')
	head = []
	label = []
#	print names;
	for k in range(len(lines)):
		if ((lines[k].find('drel'))+1 or (lines[k].find('dmrel'))+1):
			attrs = lines[k].split('\t')[3][4:-1].split(' ');
			for m in range(len(attrs)):
				if ((attrs[m].find('name='))+1):
					name=attrs[m].split('=')[1].strip("'");
					nameIndex=names.index(name)+1;
				if ((attrs[m].find('drel='))+1 or (attrs[m].find('dmrel='))+1):
					label.append(attrs[m].split('=')[1].split(':')[0].strip("'"))
					if (len(attrs[m].split('=')[1].split(':')) == 2):
						word = attrs[m].split('=')[1].split(':')[1].strip("'")

					elif (len(attrs[m].split('=')[1].split(':')) > 2):
						word = ':'
					
					else:
						#print '\t',i+1,k+1
						label = '_'
						word = '_'
					if (names.count(word)):
						head.append(names.index(word)+1)
						temp=names.index(word)+1;
						#print '\t',word,names[temp-1];
					else:
						listenc={",":"_COMMA_" , "'":"_QUOTE_" , ":":"_COLON_" , "-":"_HYPHEN_" , "=":"_EQUAL_" , "<":"_LESSER_" , ">":"_GREATER_"}
						#print '\t',lines[k]
						print '\t',word
						if(word in listenc):
							if(names.count(listenc[word])):
								head.append(names.index(listenc[word])+1);
						#print sys.argv[1],i+1,k+1
						#print 'problem in sentence '+str(i+1)
						else:
							print '\t',k+1
							#err = 1
							#break
		else:
			label.append('main')
			head.append(0)

		if (err == 1):
			break
		if(linenum[k]==head[-1]):
			print '\t',i+1,k+1
	if (err == 1):
		print block
		errfp.write(block+"\n")
		errfp.close()
	#if (len(head) != len(linenum)):
	#	print len(head)
	#	print len(linenum)

	if(len(linenum)!=len(head)):
		print '\t#',len(linenum),len(head);
#	print names;
	for k in range(len(linenum)):
		if (lex[k] == '' and names[k] != ''):
			lex[k] = '_'
		elif (lex[k] != '' and names[k] == ''):
			names[k] = lex[k]
		elif (lex[k] == '' and names[k] == ''):
			lex[k] = '_'
			names[k] = '_'
		if(fpos[k] == ''):
			fpos[k] = '_'
		if(cpos[k] == ''):
			cpos[k] = '_'
		#if(linenum[k]==str(head[k])):
		#	print '\t',linenum[k],head[k];
		uscore = "_"
		if drel_flag is True:
			fw.write(linenum[k]+'\t'+wforms[k]+'\t'+lex[k]+'\t'+fpos[k]+'\t'+cpos[k]+'\t'+'lex-'+lex[k]+'|cat-'+cpos[k]+'|gen-'+gen[k]+'|num-'+num[k]+'|pers-'+pers[k]+'|case-'+case[k]+'|vib-'+vib[k]+'|tam-'+tam[k]+'|chunkId-'+chunkId[k]+'|chunkType-'+chunkType[k]+'|stype-'+stype[k]+'|voicetype-'+voice[k]+'\t'+str(head[k])+'\t'+label[k]+'\t_\t_\n')
		else:
			fw.write(linenum[k]+'\t'+wforms[k]+'\t'+lex[k]+'\t'+fpos[k]+'\t'+cpos[k]+'\t'+'lex-'+lex[k]+'|cat-'+cpos[k]+'|gen-'+gen[k]+'|num-'+num[k]+'|pers-'+pers[k]+'|case-'+case[k]+'|vib-'+vib[k]+'|tam-'+tam[k]+'|chunkId-'+chunkId[k]+'|chunkType-'+chunkType[k]+'|stype-'+stype[k]+'|voicetype-'+voice[k]+'\t'+uscore+'\t'+uscore+'\t_\t_\n')
    #fw.write(linenum[k]+'\t'+wforms[k]+'\t'+uscore+'\t'+fpos[k]+'\t'+uscore+'\t'+uscore+'\t'+str(head[k])+'\t'+label[k]+'\t_\t_\n')
    #fw.write(linenum[k]+'\t'+wforms[k]+'\t'+uscore+'\t'+fpos[k]+'\t'+uscore+'\t'+uscore+'\t'+uscore+'\t'+uscore+'\t_\t_\n')
	
	#fw.write('\n')
	fw.close()
