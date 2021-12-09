import nltk,re,codecs
from nltk.tokenize import word_tokenize,sent_tokenize
from backNode import BackNode
from nltk import Tree

def trace_tree(trace):
	if trace.left==None and trace.right==None:
		return str(trace.root)+" "+str(trace.word)
			
	return "("+str(trace.root)+"("+str(trace_tree(trace.left))+")"+" "+"("+str(trace_tree(trace.right))+")"+")"


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

def grammer_parse():
	grammer=(nltk.data.load("grammars/large_grammars/atis.cfg"))
	grammar=grammer.chomsky_normal_form(new_token_padding='#',flexible=False)
	grammar_dict={}

	for production in grammar.productions():
		prod=list(production.rhs())

		prod_rhs=" "
		for i in prod:
			prod_rhs=prod_rhs+" "+str(i)
		prod_rhs=prod_rhs.strip()


		if prod_rhs in grammar_dict.keys():
			temp1=production.lhs()
			grammar_dict[prod_rhs].append(temp1)
		else:
			temp1=production.lhs()
			grammar_dict[prod_rhs]=[temp1]
	#print(len(grammar_dict))
	return grammar_dict
		
grammar=grammer_parse()


def parse(lines,grammar):

	line=[]
	line=lines[56].split()
	line.insert(0," ")
	#x="i need a flight from pittsburgh to newark on monday ."
	#line=x.split()
	#line.insert(0," ")
	length=len(line)
	print(line)
	tree_set=set()
	parse_table=[[ set()  for col in range(length+1)] for row in range(length+1)]
	back_table=[[ []  for col in range(length+1)] for row in range(length+1)]
	#grammer=(nltk.data.load("grammars/large_grammars/atis.cfg"))
	#print((grammar))
	#grammar=(nltk.data.load("grammars/sample_grammars/toy.cfg"))
	#print(type(grammer))

	#grammar=grammer.chomsky_normal_form(new_token_padding='#',flexible=False)
	#print(grammar)

	
	for k in range(1,len(line)):
		if line[k] in grammar.keys():
			lhs=grammar[line[k]]
			for l in lhs:
				parse_table[k][k].add(l)
				back_table[k][k].append(BackNode(None,None,l,line[k]))

	for w in range(2,length):
		#print("*")
		for s in range(1,length-w+1):
			#print("**")
			end=w+s
			for m in range(s,end-1):
				#print("***")

				for p in parse_table[s][m]:
					for q in parse_table[m+1][end-1]:
						#print(q)

						x=str(p)+" "+str(q)
						#print(x)
						if x in grammar.keys() and (len(x.split())==2):
							lhs=grammar[x]
							#print(s,m)
							for l in lhs:
								parse_table[s][end-1].add(l)

								prod=x.split()
								for r1 in back_table[s][m]:
									for r2 in back_table[m+1][end-1]:
										#print(s,m)
										#print(m+1,end-1)
										if(str(r1.root)==prod[0] and str(r2.root)==prod[1]):
											back_table[s][end-1].append(BackNode(r1,r2,l,None))
												#print(back_table[s][end-1])
	#print(back_table)
	if ("SIGMA" in str(parse_table[1][length-1])):
		#print(back_table)
		for pointer in back_table[1][length-1]:
			if(str(pointer.root)=="SIGMA"):
				value=trace_tree(pointer)
				tree_set.add(value)
		print(tree_set)	
		print(len(tree_set))

		for result in tree_set:
			trees=Tree.fromstring(value)
			trees.draw()

				
	else:
		print("No parse tree exist")

parse(lines,grammar)
