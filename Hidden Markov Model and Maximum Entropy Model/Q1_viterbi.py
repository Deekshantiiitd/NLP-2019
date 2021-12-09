import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import collections
from nltk.stem import WordNetLemmatizer
from itertools import islice

def make_dictionary():
    word_tag_list=[]
    fp=codecs.open(f'F:/MTECH1/NLP/Assignment4/test_data.txt','r',encoding='utf-8',errors='ignore')
    
    for line in fp:
        word_tag_list.append(line.split())
    #print(word_tag_list)

    merge_list=[]
    sentence_tag=[]
    
    for i in range(len(word_tag_list)):
        #print(word_tag_list[i])
        if word_tag_list[i] == ["."]:
            merge_list+=word_tag_list[i]
            sentence_tag.append(merge_list)
            #print(merge_list)
            merge_list=[]
        else:
            merge_list+=word_tag_list[i]
            #print(merge_list)

    sentence_tag=[s for s in sentence_tag if s]
    #print((sentence_tag))
    return sentence_tag
sentence_tag=make_dictionary()
def viterbi_algo(sentence_tag):

    infile=open('F:/MTECH1/NLP/Assignment4/pickle/first_tag_count','rb')
    first_tag_count=pickle.load(infile)
    infile.close()

    infile=open('F:/MTECH1/NLP/Assignment4/pickle/unigram_tag_count','rb')
    unigram_tag_count=pickle.load(infile)
    infile.close()

    infile=open('F:/MTECH1/NLP/Assignment4/pickle/tag_tag_count','rb')
    tag_tag_count=pickle.load(infile)
    infile.close()

    infile=open('F:/MTECH1/NLP/Assignment4/pickle/word_tag_count','rb')
    word_tag_count=pickle.load(infile)
    infile.close()



    first_tag_sort={}
    unigram_tag_sort={}

    sorted_keys=sorted(first_tag_count, key=first_tag_count.get, reverse=True)

    sorted_keys1=sorted(unigram_tag_count, key=unigram_tag_count.get, reverse=True)

    for i in sorted_keys:
            first_tag_sort.update({i:first_tag_count[i]})

    for i in sorted_keys1:
            unigram_tag_sort.update({i:unigram_tag_count[i]})
    tag_list=[]
    for key in unigram_tag_sort.keys():
        tag_list.append(key)
    tag_list.remove('.')

    total_first_tag=0
    for key,value in first_tag_sort.items():
        total_first_tag+=value

    total_word_tag=0

    for key,value in word_tag_count.items():
        total_word_tag+=value
    first_tag_prob={}

    for i in tag_list:
        if i in first_tag_sort.keys():
            value1=(first_tag_sort.get(i))/(13641+36)
            first_tag_prob.update({i:value1})
        if i not in first_tag_sort.keys():
            value1=0
            first_tag_prob.update({i:value1})
    #print(tag_list)
    
    #print(len(tag_list))

    first_tag_prob_list=[]
    for key,value in first_tag_prob.items():
        first_tag_prob_list.append(value)
    counter=0
    
    for i in range(len(sentence_tag)):

        rows,cols=(35,len(sentence_tag[i])-1)
        max_ent=[[0]*cols for i in range(35)]
        back_pointer=[[0]*cols for i in range(35)]
        best_path_pointer=0
        #print(sentence_tag[i])

        if(len(sentence_tag[i]))>2:
 
            for t in range(len(tag_list)):
                back_pointer[t][0]=0
                bigram=str(sentence_tag[i][0])+" "+str(tag_list[t])
                if bigram in word_tag_count.keys():
                    value=(word_tag_count.get(bigram)+36)/(unigram_tag_count.get(tag_list[t])+36)
                    max_ent[t][0]=(first_tag_prob_list[t]*value)
                if bigram not in word_tag_count.keys():
                    value=(1)/(unigram_tag_count.get(tag_list[t])+1)
                    max_ent[t][0]=(first_tag_prob_list[t]*value)
                #print(max_ent[t][0])
            #print(sentence_tag[i])

            for l in range(1,len(sentence_tag[i])-1):
                for t in range(len(tag_list)):
                    bigram=str(sentence_tag[i][l])+" "+str(tag_list[t])
                    if bigram in word_tag_count.keys():
                        value=(word_tag_count.get(bigram)+1)/(unigram_tag_count.get(tag_list[t])+36)
                    if bigram not in word_tag_count.keys():
                        value=(1)/(unigram_tag_count.get(tag_list[t])+36)

                    max_value=0

                    for m in range(len(tag_list)):
                        bigram_tag=tag_list[m]+" "+tag_list[t]
                        if bigram_tag in tag_tag_count.keys():
                            tag_prob=(tag_tag_count.get(bigram_tag))/(unigram_tag_count.get(tag_list[m]))
                        else:
                            tag_prob=0
                        cal_value=max_ent[m][l-1]*value*tag_prob
                        #print(cal_value)

                        if cal_value>max_value:
                            max_value=cal_value
                            #print(l)
                            back_pointer[t][l]=m
                            best_path_pointer=m
                            #print(best_path_pointer)
                    max_ent[t][l]=max_value
                    
            #print(max_ent)
            #print(back_pointer)

            
            value=best_path_pointer
            #print(value)
            backtrack=[]
            word=[]
            count=len(sentence_tag[i])-2
            #print(count)
            #print(back_pointer[0][count])
            
            j=len(sentence_tag[i])-2
            #print(sentence_tag[i][j])
            while value>-1 and count>-1:
                backtrack.append(tag_list[value])
                word.append(sentence_tag[i][j])
                #print(backtrack)
                #print(count)
                #print(back_pointer[0][count])
                value=back_pointer[value][count]

                count=count-1
                j=j-1

            k=len(backtrack)-1
            while(k>-1):
                print(word[k],end="\t")
                print(backtrack[k])
                k=k-1
            print(".",end="\t\t")
            print(".")
            print()

        if (len(sentence_tag[i])>=1 and len(sentence_tag[i])<=2) or (len(sentence_tag[i])==1):
            max_value=[]
            for t in range(len(tag_list)):
                back_pointer[t][0]=0
                bigram=str(sentence_tag[i][0])+" "+str(tag_list[t])
                if bigram in word_tag_count.keys():
                    value=(word_tag_count.get(bigram)+1)/(unigram_tag_count.get(tag_list[t])+1)
                    max_ent[t][0]=(first_tag_prob_list[t]*value)
                    max_value.append(max_ent[t][0])
                if bigram not in word_tag_count.keys():
                    value=(1)/(unigram_tag_count.get(tag_list[t])+1)
                    max_ent[t][0]=(first_tag_prob_list[t]*value)
                    max_value.append(max_ent[t][0])
            index=max_value.index(max(max_value))
            print(sentence_tag[i][0],end="\t ")
            print(tag_list[index])
            print(".",end="\t ")
            print(".")
            print()
            
    

viterbi_algo(sentence_tag)

