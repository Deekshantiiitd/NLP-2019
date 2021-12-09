import json
import string,pickle,math
from nltk.corpus import stopwords
import numpy as np
from tqdm import tqdm

sent=[]
with open('F:/MTECH1/NLP/Assignment6/Challenge.jsonl') as f:
	for i in f:
		data=json.loads(i)
		sent.append(data)

infile=open('F:/MTECH1/NLP/Assignment6/wordlist','rb')
word_list=pickle.load(infile)
infile.close()

infile=open('F:/MTECH1/NLP/Assignment6/tfidf_score','rb')
tfidf_score=pickle.load(infile)
infile.close()

infile=open('F:/MTECH1/NLP/Assignment6/nt_list','rb')
nt_list=pickle.load(infile)
infile.close()

infile=open('F:/MTECH1/NLP/Assignment6/magnitude_value','rb')
magnitude_value=pickle.load(infile)
infile.close()


tfidf_matrix_score=np.array(tfidf_score)

cols=1
rows=len(word_list)
#print(rows)
tfidf_matrix_score=tfidf_matrix_score.T

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
score=0
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
	tfidf_matrix_count=[[0 for m in range(len(sent[i]['question']['choices']))] for n in range(rows)]
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

		for k in range(0,rows):
			ft=0
			for w in temp_list3:
				if word_list[k]==w:
					ft=ft+1
					#print(word_list[k],w,ft)
			tfidf_matrix_count[k][j]=((1+math.log(1+ft,10))*math.log(1000/nt_list[k],10))
			#print(ft)
	temp_value=[]
	for p in range(0,len(sent[i]['question']['choices'])):
		value=0
		for q in range(0,rows):
			value=value+tfidf_matrix_count[q][p]
		temp_value.append(math.sqrt(value))
	#print(temp_value)

	tfidf_matrix=np.array(tfidf_matrix_count)	
	multiply_matrix=np.dot(tfidf_matrix_score,tfidf_matrix)
	multiply_matrix=multiply_matrix.T
	max_value_list=[]

	for x in range(0,len(sent[i]['question']['choices'])):
		max_score=0
		for y in range(0,1000):
			max_score=max(max_score,multiply_matrix[x][y]/(temp_value[x]*magnitude_value[y]))
		max_value_list.append(max_score)
	max_value=max(max_value_list)

	predicted_answer=[]
	for a in range(0,len(max_value_list)):
		if(max_value==max_value_list[a]):
			predicted_answer.append(a)

	if(len(predicted_answer)==0):
		score=score+0
	else:
		if(answer_list[i]) in predicted_answer:
			score=score+(1/(len(predicted_answer)))
print("similarity score is:",score)
print("Accuracy:",score/500)




	









		










        






	
