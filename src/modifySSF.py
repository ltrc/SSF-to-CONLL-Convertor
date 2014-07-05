import re
def modify(block):
	#lines = block.split('\n')
	#lines = lines[1:-2]
	node = []
	AllNodes = []
	line_id = 0
	headNotComputed = False
	lexTake = False
	FRAGP = False
	for item in block:
		if item.strip()=='':
			continue
		
		if item.startswith("<Sentence id=") or \
			item.startswith("</Sentence>"):continue

		if "name=FRAGP" in re.sub("[\'\"]",'',item):
			FRAGP = True
			continue
		
		if item.split("\t")[1] == "((":	
			line_id = line_id+1 
			features = "<fs "

			for attributes in  item.strip().split("\t")[3][1:-1].split()[1:]:
				attributes = re.sub("[\'\"]", '', attributes)
				fs = attributes.replace("=","=\'")+"'"
				features +=fs+" "

			features = features.strip()+">"
			if re.search('head="NULL"', item):
				headNotComputed = True
				word = "NULL"
				fSt = "af='Null,unk,,,,,,'"
			else:
				word = [i.split("=")[-1] for i in features.split() \
				       if "head=" in i][0].strip(">").strip("'")
			changehead = features.replace("name=", "chunkId=")
			changename = changehead.replace("head=", "name=")
			node.append(str(line_id))#node.append(item.split("\t")[0])
			
			if re.search('head="NULL"', item):
				node.append("<fs"+" "+fSt+" "+"name="+"'"+word+"'"+changename.strip()[3:])
			else:
				Fl = False
				for f in item.split("\t")[3].split():
					if "genitive" in f:
						Fl = True
						gen_af = ",".join(f.split("=")[1].split(",")[2:])
				if Fl:
					temp_af = ",".join(re.search("af='.*?'",changename).group().split("=")[1].strip("'").split(",")[:2])
					modified_af = "af=\'"+temp_af+","+gen_af
					modified_fs = re.sub("af='.*?_", modified_af,changename)
					node.append(modified_fs.strip()[:-1]+">")
				else:
					node.append(changename.strip()[:-1]+">")

		elif len(item.strip().split()) == 1:
			if not lexTake and not FRAGP:
				featS = node.pop()
				node.insert(1, "-")
				node.insert(2, "UNK")
				try:
					FeatS = re.sub("<fs af='.*?'", "<fs af='Null,unk,,,,,,'",featS)
				except:
					FeatS = featS.replace("<fs", "<fs af='Null,unk,,,,,,'")
				node.append(FeatS)
				AllNodes.append("\t".join(node))
			node = []
			FRAGP = False
			lexTake = False
			headNotComputed = False

		else:
			if lexTake or FRAGP:continue
			try:
				if ([w.split("=")[-1] for w in item.strip().split("\t")[3][4:-1].split() \
					if "name=" in w][0].strip("'").strip('"') == word) or headNotComputed:
					lexTake = True
					wform = item.split("\t")[1]
					tag = item.split("\t")[2]
					node.insert(1, wform)
					node.insert(2, tag)
					AllNodes.append("\t".join(node))
			except:
				return
	return "\n".join(AllNodes)
