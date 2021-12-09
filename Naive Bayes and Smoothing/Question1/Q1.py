import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
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
    print(word)
    return word


#count the unigram and store in the pickle file
def vocabs(word,pickle_name):
	word_counts = collections.Counter(word)
	outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles/{pickle_name}','wb')
	pickle.dump(word_counts,outfile)
	outfile.close()


#combine the files of each class in big doc file of each class(1-20)
def combine_files():
	#store all folders in a list
	folder=[f for f in glob.glob(f'F:/MTECH1/NLP/20_newsgroups' + "**/*", recursive=True)]
	
	for i in folder:
		files = [f for f in glob.glob(f'{i}' + "**/*", recursive=True)]
		hold=i[28:]
		with open(f'F:/MTECH1/NLP/Assignment3/combine/{hold}.txt', 'w') as outfile:
			for fname in files:
				with open(fname) as infile:
					for line in infile:
						outfile.write(line)

#combine_files()


def list_files():
	folder=[f for f in glob.glob(f'F:/MTECH1/NLP/20_newsgroups' + "**/*", recursive=True)]
	total_files=[]
	
	for i in folder:
		files = [f for f in glob.glob(f'{i}' + "**/*", recursive=True)]
		total_files.append(len(files))

	#store file count of each class in a pickle file containing list
	outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles/count_files_each_class','wb')
	pickle.dump(total_files,outfile)
	outfile.close()

	#now each bigdoc will be preprocessed here and making a pickle file of all classes and store in a list 
	files = [f for f in glob.glob(f'F:/MTECH1/NLP/Assignment3/combine' + "**/*", recursive=True)]
	word=[]
	for f in files:
		hold=f[34:]
		print(hold)
		print(f)
		word.append(data_preprocessing(hold))
	outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles/combine_wordlist','wb')
	pickle.dump(word,outfile)
	outfile.close()

	#now making pickle file of each class with word count
	infile=open('F:/MTECH1/NLP/Assignment3/pickles/combine_wordlist','rb')
	word=pickle.load(infile)
	infile.close()
	count=-1
	for i in word:
		count+=1
		hold=folder[count]
		hold=hold[28:]
		print(hold)
		vocabs(i,hold)
	word_count=[]
	for i in word:
		word_count.append(len(i))
	outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles/word_count_each_class','wb')
	pickle.dump(word_count,outfile)
	outfile.close()

	#Now combine all pickle file of word count file into single pickle file combine_List
	files = [f for f in glob.glob(f'F:/MTECH1/NLP/Assignment3/pickles' + "**/*", recursive=True)]
	print(files)
	combine_list=[]
	for f in files:
		hold=f[34:]
		print(hold)
		infile=open(f'F:/MTECH1/NLP/Assignment3/pickles/{hold}','rb')
		word=pickle.load(infile)
		combine_list.append(word)
		infile.close()
	print(len((combine_list)))    
	outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles/seperate_word_count_list','wb')
	pickle.dump(combine_list,outfile)
	outfile.close()
#list_files()

def calculate_prob_Taks2():
	infile=open(f'F:/MTECH1/NLP/Assignment3/pickle/count_files','rb')
	total_files=pickle.load(infile)
	infile.close()

	total_doc=0

	for i in total_files:
		total_doc=total_doc+i

	total_files_prob=[]

	for i in total_files:
		total_files_prob.append(math.log((i/total_doc),10))
	
	outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles/class20_prob','wb')
	pickle.dump(total_files_prob,outfile)
	outfile.close()
calculate_prob_Taks2()

def word_vocab_class():

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/combine_wordlist','rb')
	word=pickle.load(infile)
	infile.close()

	merge=[]
	for i in word:
		merge=merge+i
	print(len(merge))
	merge1=[]
	for i in merge:
		if len(merge1)==0:
			merge1.append(i)
		if i not in merge1:
			merge1.append(i)
	print(len(merge1))

	infile=open('F:/MTECH1/NLP/Assignment3/pickles/word_count_each_class','rb')
	word_count=pickle.load(infile)
	infile.close()
	word_count.append(len(merge1))
	outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles/word_count_each_class','wb')
	pickle.dump(word_count,outfile)
	outfile.close()

#word_vocab_class()

