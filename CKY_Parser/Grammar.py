import nltk,re,codecs
from nltk.tokenize import word_tokenize,sent_tokenize
from backNode import BackNode


def data_preprosessing():
	#fp=codecs.open(f'F:/MTECH1/NLP/Assignment5/Training_set.txt','r',encoding='utf-8',errors='ignore')
	#=nltk.data.load("grammars/large_grammars/atis_sentences.txt")
	with open('F:/MTECH1/NLP/Assignment5/Training_set.txt') as f:
	    lines = f.readlines()

	for i in range(0,len(lines)):
		lines[i]=re.sub(r'\d+\s:\s',"",lines[i])
		#print(lines[i])
	lines = [line.rstrip('\n') for line in lines]
	#print(lines)

	#list_sentences=sent_tokenize(s)

	"""parser = nltk.parse.BottomUpChartParser(grammer)

	for i in list_sentences:
		i=word_tokenize(i)
		for tree in parser.parse(i):
			result=list(tree)
			print(result)
		for tree in result:
			tree.draw()"""
	#print(lines)
	return lines
lines=data_preprosessing()


def parse(lines):

	#line=[]
	#line=lines[14].split()
	#line.insert(0," ")
	x="the dog chased the cat"
	line=x.split()
	line.insert(0," ")
	length=len(line)
	print(line)

	parse_table=[[ []  for col in range(length+1)] for row in range(length+1)]
	back_table=[[ []  for col in range(length+1)] for row in range(length+1)]
	#grammer=(nltk.data.load("grammars/large_grammars/atis.cfg"))
	#print(type(grammer))
	grammar=(nltk.data.load("grammars/sample_grammars/toy.cfg"))
	#print(type(grammer))

	#grammar=grammer.chomsky_normal_form(new_token_padding='#',flexible=False)
	print(grammar)
	for k in range(1,len(line)):
		for i in grammar.productions():
			prod=(i.rhs())
			if (len(prod)==1):
				if(prod[0]==line[k]):
					parse_table[k][k].append(i.lhs())
					back_table[k][k].append(BackNode(None,None,i.lhs(),line[k]))

	for w in range(2,length):
		#print("*")
		for s in range(1,length-w+1):
			#print("**")
			end=w+s
			for m in range(s,end):
				#print("***")
				for p in parse_table[s][m]:
					for q in parse_table[m+1][end-1]:
						#print(q)
						x=str(p)+" "+str(q)
						#print(x)
						for r in grammar.productions():
							prod=list(r.rhs())
							if(len(prod)==2):
								y=str(prod[0])+" "+str(prod[1])
								if(y==x):
									parse_table[s][end-1].append(r.lhs())
									back_table[s][end-1].append(BackNode(prod[0],prod[1],r.lhs(),None))

	if ("S" in str(parse_table[1][length-1])):
		print("YES")

		for BackNodes in back_table[1][length-1]:
			print(str(BackNodes.root))
			if((BackNodes.root)=="S" ):
				print(back_track(BackNodes))
				
	else:
		print("NO")



	#print(parse_table)
parse(lines)
