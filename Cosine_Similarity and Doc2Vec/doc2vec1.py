import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from tqdm import tqdm
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import json
import warnings

warnings.filterwarnings("ignore")

sent=[]
with open('F:/MTECH1/NLP/Assignment6/Challenge.jsonl') as f:
	for i in f:
		data=json.loads(i)
		sent.append(data)

f = codecs.open(f'F:/MTECH1/NLP/Assignment6/data.txt', encoding='utf-8')
sentence_list1=[]

for line in f:
	line=re.sub(r'\b\d+\b','',line)
	line=line.lower().split()
	token=[word.strip(string.punctuation) for word in line]
	sentence_list1.append(token)
#print(sentence_list1)
tagged_document=[TaggedDocument(sentence,tags=[str(i)]) for i,sentence in enumerate(sentence_list1)]

#print(tagged_document)
model =Doc2Vec(tagged_document, size = 200, window = 400, min_count = 1, workers = 10)
vocab=model.wv

print(vocab.vocab)
score=0
answer_list=[]
for i in range(0,len(sent)):
	if(sent[i]['answerKey']=="A"):
		answer_list.append(0)
	elif(sent[i]['answerKey']=="B"):
		answer_list.append(1)
	elif(sent[i]['answerKey']=="C"):
		answer_list.append(2)
	elif(sent[i]['answerKey']=="D"):
		answer_list.append(3)
	else:
		answer_list.append(sent[i]['answerKey'])

for i in tqdm(range(0,len(sent))):
	query1=''
	query1=sent[i]['question']['stem']
	temp_list1=query1.lower().split()
	token1=[word.strip(string.punctuation) for word in temp_list1]
	"""stopword=set(stopwords.words('english'))
	for w in token1:
		if w not in stopword:
			temp_list1.append(w)"""
	temp_list1=[]
	temp_list1=token1.copy()
	similarity_list=[]
	for j in range(len(sent[i]['question']['choices'])):
		
		query2=''
		query2=sent[i]['question']['choices'][j]['text']
		temp_list2=query2.lower().split()
		token2=[word.strip(string.punctuation) for word in temp_list2]
		"""stopword=set(stopwords.words('english'))
		temp_list2=[]
		for w in token2:
			if w not in stopword:
				temp_list2.append(w)"""
		temp_list2=[]
		temp_list2=token2.copy()
		temp_list3=temp_list1+temp_list2
		new_list=[]
		for word in temp_list3:
			if word not in vocab.vocab:
				pass
			else:
				new_list.append(word)
		#print(new_list)
		similar_doc = model.wv.most_similar(new_list)
		print(len(new_list))

		similarity_list.append(similar_doc)
	predicted_answer=[]
	max_value=max(similarity_list)
	for a in range(0,len(similarity_list)):
		if(max_value==similarity_list[a]):
			predicted_answer.append(a)

	if(len(predicted_answer)==0):
		score=score+0
	else:
		if(answer_list[i]) in predicted_answer:
			score=score+(1/(len(predicted_answer)))
print()
print("Similarity Score is:",score)
print("Accuracy:",score/500)
		



