# This script converts the input ssf format data into conll format
# This script takes input the ssf-file name which has to be converted
# as a command line argument and outputs the conll format into temp.conll

import os,sys,re

def convertconll(block,drel_flag):
	fw = open("temp.conll",'w')
	errfp = open("conllErrors.txt",'w')
	lines = block.split('\n')
	wforms = []
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
	drel = []
	err = 0
	fstr = []
	stype = []
	voice = []
	
	for j in range(len(lines)):
		af = ''
		linenum.append(lines[j].split('\t')[0])
		wforms.append(lines[j].split('\t')[1])
		fpos.append(lines[j].split('\t')[2])
		fstr = lines[j].split('\t')[3][4:-1].split(' ')
		flag_stype = 0
		flag_voice = 0

		for m in range(len(fstr)):
			if ((fstr[m].find('af='))+1):
				af = fstr[m]
			if ((fstr[m].find('chunkId='))+1):
				chunkId.append(fstr[m].split('=')[1].strip("'"))
			if ((fstr[m].find('stype='))+1):
				stype.append(fstr[m].split('=')[1].strip("'"))
				flag_stype = 1
			if ((fstr[m].find('voicetype='))+1):
				voice.append(fstr[m].split('=')[1].strip("'"))
				flag_voice = 1
		
		if (flag_stype == 0):
			stype.append('')

		if (flag_voice == 0):
			voice.append('')

		if (af != ''):
			feats = af.split("=")[1].strip("'").split(",")
			if len(feats) >= 8:
				lex.append(feats[0])
				cpos.append(feats[1])
				gen.append(feats[2])
				num.append(feats[3])
				pers.append(feats[4])
				case.append(feats[5])
				vib.append(feats[6])
				tam.append(feats[7])

			else:
				reverseFeats = feats; reverseFeats.reverse()
				feats.extend(reverseFeats)
				lex.append(feats[0])
				cpos.append(feats[1])
				gen.append(feats[2])
				num.append(feats[3])
				pers.append(feats[4])
				case.append(feats[5])
				vib.append(feats[6])
				tam.append(feats[7])
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
	for k in range(len(lines)):
		if ((lines[k].find('drel'))+1 or (lines[k].find('dmrel'))+1):
			attrs = lines[k].split('\t')[3][4:-1].split(' ');
			for m in range(len(attrs)):
				if ((attrs[m].find('chunkId='))+1):
					name=attrs[m].split('=')[1].strip("'");
					#nameIndex=chunkId.index(name)+1;
				if ((attrs[m].find('drel='))+1 or (attrs[m].find('dmrel='))+1):
					
					label.append(attrs[m].split('=')[1].replace("'","").split(':')[0].strip("'"))
					if (len(attrs[m].split('=')[1].replace("'","").split(':')) == 2):
						headC = attrs[m].split('=')[1].replace("'","").split(':')[1].strip("'")
					else:
						err = 1,attrs[m],"\tWrong formatt"
					if (chunkId.count(headC)):
						head.append(chunkId.index(headC)+1)
					else:
						print '\t',headC,"\tchunk Missing in Vibhakhti Computed SSF data"
						err = 1
		else:
			label.append('main')
			head.append(0)

	if(len(linenum)!=len(head)):
		print '\t#', len(linenum), len(head);
		err = 1
	if err:
		print block
		errfp.write(block+"\n")
		errfp.close()
		return False
	
	for k in range(len(linenum)):
		if (lex[k] == ''):
			lex[k] = '_'
		if(fpos[k] == ''):
			fpos[k] = '_'
		if(cpos[k] == ''):
			cpos[k] = '_'
		uscore = "_"
		
		##### GOLD FEATURES WITH DEPENDENCY INFO ######
		if drel_flag is True:
			fw.write(linenum[k]+'\t'+wforms[k]+'\t'+lex[k]+ \
				'\t'+cpos[k]+'\t'+fpos[k]+'\t'+'lex-'+lex[k]+ \
				'|cat-'+cpos[k]+'|gen-'+gen[k]+'|num-'+num[k]+ \
				'|pers-'+pers[k]+'|case-'+case[k]+'|vib-'+vib[k]+ \
				'|tam-'+tam[k]+'|chunkId-'+chunkId[k]+'|stype-'+ \
				stype[k]+'|voicetype-'+voice[k]+'\t'+str(head[k])+ \
				'\t'+label[k]+'\t_\t_\n')
		
				## WITHOUT DEPENDENCY INFO ##
		else:
			fw.write(linenum[k]+'\t'+wforms[k]+'\t'+lex[k]+'\t'+fpos[k]+ \
			'\t'+cpos[k]+'\t'+'vib-'+vib[k]+ \
			'|tam-'+tam[k]+'|chunkId-'+chunkId[k]+'\t'+uscore+'\t'+uscore+'\t_\t_\n')
			#fw.write(linenum[k]+'\t'+wforms[k]+'\t'+lex[k]+'\t'+fpos[k]+ \
			#'\t'+cpos[k]+'\t'+'lex-'+lex[k]+'|cat-'+cpos[k]+'|gen-'+gen[k]+ \
			#'|num-'+num[k]+'|pers-'+pers[k]+'|case-'+case[k]+'|vib-'+vib[k]+ \
			#'|tam-'+tam[k]+'|chunkId-'+chunkId[k]+'|stype-'+stype[k]+'|voicetype-'+ \
			#voice[k]+'\t'+uscore+'\t'+uscore+'\t_\t_\n')
		
	##### FEATURES AUTOMATICALLY GENERATED WITH DSI ######

		#fw.write(linenum[k]+'\t'+wforms[k]+'\t'+uscore+'\t'+fpos[k]+ \
		#'\t'+uscore+'\t'+uscore+'\t'+str(head[k])+'\t'+label[k]+'\t_\t_\n')
		
		## WITHOUT DSI ##

		#fw.write(linenum[k]+'\t'+wforms[k]+'\t'+uscore+'\t'+fpos[k]+ \
		#'\t'+uscore+'\t'+uscore+'\t'+uscore+'\t'+uscore+'\t_\t_\n')
	
	fw.write('\n')
	fw.close()
