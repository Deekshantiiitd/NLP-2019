import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import collections
from nltk.stem import WordNetLemmatizer
from itertools import islice

def new_train_file():
    fp=codecs.open(f'F:/MTECH1/NLP/Assignment4/Training_update_set_HMM.txt','w+',encoding='utf-8',errors='ignore')
    fp1=codecs.open(f'F:/MTECH1/NLP/Assignment4/Training_update1_set_HMM.txt','w+',encoding='utf-8',errors='ignore')
    
    with open('F:/MTECH1/NLP/Assignment4/Training set_HMM.txt') as lines:
        for line in islice(lines, 0, 139997):
            fp.write(line)

    with open('F:/MTECH1/NLP/Assignment4/Training set_HMM.txt') as lines:
        for line in islice(lines, 139997,165833):
            fp1.write(line)

new_train_file()

def make_dictionary():
    word_tag_list=[]
    fp=codecs.open(f'F:/MTECH1/NLP/Assignment4/Training set_HMM.txt','r',encoding='utf-8',errors='ignore')
    
    for line in fp:
        word_tag_list.append(line.split())
    #print(word_tag_list)
    
    merge_list=[]
    sentence_tag=[]
    
    for i in range(len(word_tag_list)):
        if len(word_tag_list[i])==0:
            sentence_tag.append(merge_list)
            merge_list=[]
        else:
            merge_list+=word_tag_list[i]

    sentence_tag=[s for s in sentence_tag if s]
    print(len(sentence_tag))

    outfile =open(f'F:/MTECH1/NLP/Assignment4/pickle/sentence_tag_list','wb')
    pickle.dump(sentence_tag,outfile)
    outfile.close()

    word_tag_count={}
    tag_tag_count={}
    first_tag_count={}
    unigram_tag={}
    s=""
    s1=""
    k1=""
    value=0

    for i in range(len(sentence_tag)):
        j=0
        while(j<len(sentence_tag[i])-1):
            k1=str(sentence_tag[i][1])
            s=str(sentence_tag[i][j])+" "+str(sentence_tag[i][j+1])
            #print(len(sentence_tag[i]))
            if s in word_tag_count.keys():
                value=word_tag_count.get(s)
                value+=1
                word_tag_count.update({s:value})
            if s not in word_tag_count.keys():
                value=1
                word_tag_count.update({s:value})
            j=j+2

        if k1 in first_tag_count.keys():
            value=first_tag_count.get(k1)
            value+=1
            first_tag_count.update({k1:value})
        if k1 not in first_tag_count.keys():
            value=1
            first_tag_count.update({k1:value})
        k=1 
        while(k<(len(sentence_tag[i])-2)):
            if k%2==1:
                s1=str(sentence_tag[i][k])+" "+str(sentence_tag[i][k+2])
                #print(s1)
                if s1 in tag_tag_count.keys():
                    value=tag_tag_count.get(s1)
                    value+=1
                    tag_tag_count.update({s1:value})
                if s1 not in tag_tag_count.keys():
                    value=1
                    tag_tag_count.update({s1:value})
            k=k+2
    for i in range(len(sentence_tag)):
        j=1
        while(j<len(sentence_tag[i])):
            if sentence_tag[i][j] not in unigram_tag.keys():
                value=0
                unigram_tag.update({sentence_tag[i][j]:value})
            if sentence_tag[i][j] in unigram_tag.keys():
                value=unigram_tag.get(sentence_tag[i][j])
                value+=1
                unigram_tag.update({sentence_tag[i][j]:value})
            j=j+2
    #print((unigram_tag))

    #print(word_tag_count)
    outfile =open(f'F:/MTECH1/NLP/Assignment4/pickle/tag_tag_count','wb')
    pickle.dump(tag_tag_count,outfile)
    outfile.close()
    outfile =open(f'F:/MTECH1/NLP/Assignment4/pickle/word_tag_count','wb')
    pickle.dump(word_tag_count,outfile)
    outfile.close()
    outfile =open(f'F:/MTECH1/NLP/Assignment4/pickle/first_tag_count','wb')
    pickle.dump(first_tag_count,outfile)
    outfile.close()
    outfile =open(f'F:/MTECH1/NLP/Assignment4/pickle/unigram_tag_count','wb')
    pickle.dump(unigram_tag,outfile)
    outfile.close()
    #print(word_tag_count)

make_dictionary()






        
