
import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import collections
from nltk.stem import WordNetLemmatizer


#data preprocessing
def data_preprocessing(file_name):
    fp=codecs.open(f'F:/MTECH1/NLP/Assignment3/combine/{file_name}','r',encoding='utf-8',errors='ignore')
    text=fp.read()
    #print(text)
    text=text.lower()
    text=re.sub(r'\d+','',text)
    text=text.split()
    token=[word.strip(string.punctuation) for word in text]
    #print(token)

    #tokenize into word
    tokens=word_tokenize(str(token))
    lemmatizer = WordNetLemmatizer() 
    lematized_tokens = [lemmatizer.lemmatize(t) for t in token]


    #remove stopwords
    stopword=set(stopwords.words('english'))
    word=[]
    for w in lematized_tokens:
    	if w not in stopword:
    		word.append(w)
    #remove blank_space
    word=[s for s in word if s]
 
    outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles/test_pickle','wb')
    pickle.dump(word,outfile)
    outfile.close()

def user_input():

	case=input("Enter your choice of input data")

	if case=='1':
		sample=input("Enter your data")
		fp=codecs.open(f'F:/MTECH1/NLP/Assignment3/combine/Development_Set1.txt','w',encoding='utf-8',errors='ignore')
		fp.write(sample)
		data_preprocessing("Development_Set1.txt")
	if case=='2':
		filename=input("Enter the filename")
		data_preprocessing("Development_Set.txt")
user_input()

def calculate_prob_test_task1():

	k=input("Enter the value of k for task 1")
	k=int(k)

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/seperate_word_count_list','rb')
	word_list=pickle.load(infile)
	infile.close()

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/word_count_each_class','rb')
	word_count=pickle.load(infile)
	infile.close()
	#print(word_count)

	merge=word_list[8]+word_list[9]
	
	merge1=[]
	for i in merge:
		if i not in merge1:
			merge1.append(i)
	vocab=len(merge1)
	#print(vocab)

	new_list=[]
	count=-1
	for i in word_list:
		count+=1
		prob_dict={}
		value1=0
		for key, value in i.items():
			value1=math.log(((value+k)/((k*vocab)+word_count[count])),10)
			prob_dict.update({key:value1})
		#print(prob_dict)	
		new_list.append(prob_dict)
	#print(new_list[8])

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/test_pickle','rb')
	word=pickle.load(infile)
	infile.close()

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/count_files_each_class','rb')
	total_files=pickle.load(infile)
	infile.close()
	
	total_doc=total_files[8]+total_files[9]
	#print(total_doc)

	rec_motorcycle_prob=math.log((total_files[8]/total_doc),10)
	rec_sportbase_prob=math.log((total_files[9]/total_doc),10)


	sum1=rec_sportbase_prob
	for i in word:
		if i in new_list[9].keys():
			sum1+=new_list[9].get(i)
		
		if i not in new_list[9].keys():
			sum1+=math.log((k/((k*vocab)+(word_count[9]))),10)
		
	sum2=rec_motorcycle_prob
	for i in word:
		if i in new_list[8].keys():
			sum2+=new_list[8].get(i)
		if i not in new_list[8].keys():
			sum2=sum2+math.log((k/((k*vocab)+(word_count[8]))),10)
	print("probability of rec.motorcyle",sum2)
	print("probability of rec.sport.baseball",sum1)

	print("TASK1 START")

	if sum1>sum2:
		print(f"rec.sport.baseball",sum1)
	if sum2>sum1:
		print(f"rec.motorcycles",sum2)
	print("TASK1 END \n")
    	
calculate_prob_test_task1()

def calculate_prob_test_task2():
	k=input("Enter the value of k for task 2")
	k=int(k)

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/seperate_word_count_list','rb')
	word_list=pickle.load(infile)
	infile.close()

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/word_count_each_class','rb')
	word_count=pickle.load(infile)
	infile.close()
	
	new_list=[]
	j=-1	
	for i in word_list:
		j+=1
		prob_dict={}
		for key, value in i.items():
			value1=math.log(((value+k)/((k*word_count[20])+word_count[j])),10)
			prob_dict.update({key:value1})
		new_list.append(prob_dict)

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/test_pickle','rb')
	word=pickle.load(infile)
	infile.close()

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/count_files_each_class','rb')
	total_files=pickle.load(infile)
	infile.close()

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/class20_prob','rb')
	class_prob=pickle.load(infile)
	infile.close()
	#print(class_prob)

	max_class=[]
	count=-1


	for i in new_list:
		count+=1
		sum1=class_prob[count]
		for j in word:
			if j in i.keys():
				sum1+=i.get(j)
				#print(sum1)
			if j not in i.keys():
				sum1+=math.log((k/(k*(1+word_count[20])+(word_count[count]))),10)
				#print(sum1)
		max_class.append(sum1)

	maxpos=max_class.index(max(max_class))

	class_list=['alt.atheism','comp.graphics','comp.os.ms-windows.misc','comp.sys.ibm.pc.hardware','comp.sys.mac.hardware','comp.windows.x','misc.forsale',
	'rec.autos','rec.motorcycles','rec.sport.baseball','rec.sport.hockey','sci.crypt','sci.electronics','sci.med','sci.space','soc.religion.christian','talk.politics.guns',
	'talk.politics.mideast','talk.politics.misc','talk.religion.misc']
	print("TASK2 START")
	for i in range(0,20):
		print(class_list[i],end=" ")
		print(max_class[i])
	print("\n")
	print(class_list[maxpos]) 
	print(max(max_class))
	print("TASK2 END") 
calculate_prob_test_task2()



    








