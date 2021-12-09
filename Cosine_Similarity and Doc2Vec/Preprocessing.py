import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from tqdm import tqdm
import numpy as np

f = codecs.open(f'F:/MTECH1/NLP/Assignment6/data.txt', encoding='utf-8')
sentence_list1=[]

for line in f:
    line=line.lower()
    sentence_list1.append(line)

sentence_list2=[]
for i in sentence_list1:
    #print(i)
    #s=re.sub(r'\([^()]*\)', '', i)
    #s=re.sub(r'\[[^()]*\]', '', s)
    s=re.sub(r'\b\d+\b','',i)
    sentence_list2.append(s)
    #print(s)

word_dict=[]
sentence_list=[]
for i in range(0,len(sentence_list2)):
    temp_list=sentence_list2[i].split()
    token=[word.strip(string.punctuation) for word in temp_list]
    sentence_list.append(token)
    """stopword=set(stopwords.words('english'))
    word=[]
    for w in token:
        if w not in stopword:
            word.append(w)
    sentence_list.append(word)"""

    for w in token:
        if w not in word_dict:
            word_dict.append(w)
print(len(word_dict))
outfile =open(f'F:/MTECH1/NLP/Assignment6/wordlist','wb')
pickle.dump(word_dict,outfile)
outfile.close()

cols=1000
rows=len(word_dict)
tfidf_matrix_count=[[0 for i in range(cols)] for j in range(rows)]
#print(tfidf_matrix_count)
temp_list=[]
for i in tqdm(range(0,rows)):
    for j in (range(0,cols)):
        temp_list=sentence_list[j]
        for w in temp_list:
            if word_dict[i]==w:
                tfidf_matrix_count[i][j]=tfidf_matrix_count[i][j]+1
        temp_list=[]
nt_list=[]
for i in range(0,rows):
    nt=0
    for j in range(0,cols):
        if(tfidf_matrix_count[i][j]!=0):
            nt=nt+1
    nt_list.append(nt)
print(len(nt_list))

outfile =open(f'F:/MTECH1/NLP/Assignment6/nt_list','wb')
pickle.dump(nt_list,outfile)
outfile.close()

magnitude_value=[]
for i in range(0,cols):
    value=0
    for j in range(0,rows):
        value=value+(tfidf_matrix_count[j][i]*tfidf_matrix_count[j][i])
    magnitude_value.append(math.sqrt(value))

outfile =open(f'F:/MTECH1/NLP/Assignment6/magnitude_value','wb')
pickle.dump(magnitude_value,outfile)
outfile.close()

tfidf_matrix_score=[[0 for i in range(cols)] for j in range(rows)]

for i in tqdm(range(0,rows)):
    for j in range(0,cols):
        tfidf_matrix_score[i][j]=(1+math.log(1+tfidf_matrix_count[i][j],10))*math.log(1000/(1+nt_list[j]),10)

outfile =open(f'F:/MTECH1/NLP/Assignment6/tfidf_score','wb')
pickle.dump(tfidf_matrix_score,outfile)
outfile.close()







