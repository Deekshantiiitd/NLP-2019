import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import collections,operator
from nltk.corpus import stopwords 

def generate_uni_sent(filename1):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    unigram_count=pickle.load(infile)
    infile.close()

    stop_words = set(stopwords.words('english'))

    value1=0
    vocab=len(unigram_count)

    for i in unigram_count.keys():
        value1+=unigram_count.get(i)

    unigram_prob={}

    for key,value in unigram_count.items():
        value2=math.log((value+1)/(value1+vocab),10)
        unigram_prob.update({key:value2})

    new_dict={}
    sorted_keys=sorted(unigram_prob, key=unigram_prob.get, reverse=True)

    for i in sorted_keys:
        if i not in stop_words:
            new_dict.update({i:unigram_prob[i]})
    new_key=[]
    for key in new_dict:
        new_key.append(key)
    #print(new_dict)
    sentence=""
    for i in range(6):
            sentence=sentence+" "+new_key[i]
    for i in range(6,10):
        sentence=sentence+" "+new_key[i]
        print(sentence)
    print("***unigram***")

generate_uni_sent('motorcycle_combine_word_tokenize_unigram')
generate_uni_sent('baseball_combine_word_tokenize_unigram')

def generate_bi_sent(filename1,filename2,filename3):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    first_word=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','rb')
    bigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename3}','rb')
    unigram_count=pickle.load(infile)
    infile.close()

    vocab=len(unigram_count)
    value1=0

    first_word.pop('')

    for key in first_word.keys():
        value1+=first_word.get(key)
    #print(value1)

    first_word_prob={}

    for key,value in first_word.items():
        value2=math.log((value)/(value1),10)
        first_word_prob.update({key:value2})
    #print(first_word_prob)

    sorted_first_word_dict={}
    sorted_keys=sorted(first_word_prob, key=first_word_prob.get, reverse=True)

    for i in sorted_keys:
            sorted_first_word_dict.update({i:first_word_prob[i]})
    #print(sorted_first_word_dict)

    bigram_prob={}
    new_bigram_count={}

    for key,value in bigram_count.items():
        s=key.split()
        if len(s) == 2:
            new_bigram_count.update({key:value})
    #print(len(new_bigram_count))

    for key,value in new_bigram_count.items():
        s=key.split()
        if s[0] in unigram_count.keys():
            value2=math.log((value+1)/(unigram_count.get(s[0])+vocab),10)
            bigram_prob.update({key:value2})
    #print(bigram_prob)

    sorted_bigram_dict={}
    sorted_keys1=sorted(bigram_prob, key=bigram_prob.get, reverse=True)

    for i in sorted_keys1:
            sorted_bigram_dict.update({i:bigram_prob[i]})

    sentence=sorted_keys[0]
    sentence=sentence.split()
    count=0

    for key in sorted_bigram_dict:
        s=key.split()
        if s[0]==sentence[len(sentence)-1] and count<10:
            sentence.append(s[1])
            count+=1
            s=""
            if count >5 and count<10:
                for i in range(0,count):
                    s=s+" "+sentence[i]
                print(s)
    print("***bigram***")

generate_bi_sent('motorcycle_count_first_word','motorcycle_bigram','motorcycle_combine_word_tokenize_unigram')
generate_bi_sent('baseball_count_first_word','baseball_bigram','baseball_combine_word_tokenize_unigram')


def generate_tri_sent(filename1,filename2,filename3,filename4,filename5):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    trigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','rb')
    bigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename3}','rb')
    unigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename4}','rb')
    first_word=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename5}','rb')
    first_second_word=pickle.load(infile)
    infile.close()

    vocab=len(unigram_count)
    value1=0
    value3=0

    first_word_prob={}

    for key in first_word.keys():
        value1+=first_word.get(key)

    for key in first_second_word.keys():
        value3+=first_second_word.get(key)

    for key,value in first_word.items():
        value2=math.log((value)/(value1),10)
        first_word_prob.update({key:value2})

    sorted_first_word_dict={}
    sorted_keys=sorted(first_word_prob, key=first_word_prob.get, reverse=True)


    for i in sorted_keys:
            sorted_first_word_dict.update({i:first_word_prob[i]})
    sorted_first_word_dict.pop('')
    

    first_second_word_prob={}

    for key in first_second_word.keys():
        value1+=first_second_word.get(key)

    for key,value in first_second_word.items():
        value2=math.log((value)/(value3),10)
        first_second_word_prob.update({key:value2})

    sorted_first_second_word_dict={}
    sorted_keys1=sorted(first_second_word_prob, key=first_second_word_prob.get, reverse=True)

    for i in sorted_keys1:
        s=i.split()
        if len(s)==2:
            sorted_first_second_word_dict.update({i:first_second_word_prob[i]})

    trigram_prob={}
    new_trigram_count={}

    for key,value in trigram_count.items():
        s=key.split()
        if len(s) == 3:
            new_trigram_count.update({key:value})
    #print(len(new_trigram_count))

    for key,value in new_trigram_count.items():
        s=key.split()
        s=str(s[0])+" "+str(s[1])
        if s in bigram_count.keys():
            value2=math.log((value+1)/(bigram_count.get(s)+vocab),10)
            trigram_prob.update({key:value2})
    #print(trigram_prob)

    sorted_trigram_dict={}
    sorted_keys2=sorted(trigram_prob, key=trigram_prob.get, reverse=True)

    for i in sorted_keys2:
            sorted_trigram_dict.update({i:trigram_prob[i]})

    sentence=sorted_keys[4]
    sentence=sentence.split()
    #print(sentence)

    for i in sorted_first_second_word_dict.keys():
        #print(i)
        s=i.split()
        if s[0] == sentence[len(sentence)-1]:
            sentence.append(s[1])
            break


    count=0
    for key in sorted_trigram_dict:
        s=key.split()
        s1=str(s[0])+" "+str(s[1])
        s2=str(sentence[len(sentence)-2])+" "+str(sentence[len(sentence)-1])
        #print(s2)
        if s1==s2 and len(sentence)<10:
            sentence.append(s[2])
            #print(len(sentence))
            s=""
            if len(sentence) >5 and len(sentence)<10:
                for i in range(0,len(sentence)):
                    s=s+" "+sentence[i]
            print(s)
    print("***trigram***")

generate_tri_sent('motorcycle_trigram','motorcycle_bigram','motorcycle_combine_word_tokenize_unigram','motorcycle_count_first_word','motorcycle_count_first_second_word')

def generate_tri_sent(filename1,filename2,filename3,filename4,filename5):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    trigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','rb')
    bigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename3}','rb')
    unigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename4}','rb')
    first_word=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename5}','rb')
    first_second_word=pickle.load(infile)
    infile.close()

    vocab=len(unigram_count)
    value1=0
    value3=0

    first_word_prob={}

    for key in first_word.keys():
        value1+=first_word.get(key)

    for key in first_second_word.keys():
        value3+=first_second_word.get(key)

    for key,value in first_word.items():
        value2=math.log((value)/(value1),10)
        first_word_prob.update({key:value2})

    sorted_first_word_dict={}
    sorted_keys=sorted(first_word_prob, key=first_word_prob.get, reverse=True)


    for i in sorted_keys:
            sorted_first_word_dict.update({i:first_word_prob[i]})
    sorted_first_word_dict.pop('')
    

    first_second_word_prob={}

    for key in first_second_word.keys():
        value1+=first_second_word.get(key)

    for key,value in first_second_word.items():
        value2=math.log((value)/(value3),10)
        first_second_word_prob.update({key:value2})

    sorted_first_second_word_dict={}
    sorted_keys1=sorted(first_second_word_prob, key=first_second_word_prob.get, reverse=True)

    for i in sorted_keys1:
        s=i.split()
        if len(s)==2:
            sorted_first_second_word_dict.update({i:first_second_word_prob[i]})

    trigram_prob={}
    new_trigram_count={}

    for key,value in trigram_count.items():
        s=key.split()
        if len(s) == 3:
            new_trigram_count.update({key:value})
    #print(len(new_trigram_count))

    for key,value in new_trigram_count.items():
        s=key.split()
        s=str(s[0])+" "+str(s[1])
        if s in bigram_count.keys():
            value2=math.log((value+1)/(bigram_count.get(s)+vocab),10)
            trigram_prob.update({key:value2})
    #print(trigram_prob)

    sorted_trigram_dict={}
    sorted_keys2=sorted(trigram_prob, key=trigram_prob.get, reverse=True)

    for i in sorted_keys2:
            sorted_trigram_dict.update({i:trigram_prob[i]})

    sentence=sorted_keys[1]
    sentence=sentence.split()
    #print(sentence)

    for i in sorted_first_second_word_dict.keys():
        #print(i)
        s=i.split()
        if s[0] == sentence[len(sentence)-1]:
            sentence.append(s[1])
            break


    count=0
    for key in sorted_trigram_dict:
        s=key.split()
        s1=str(s[0])+" "+str(s[1])
        s2=str(sentence[len(sentence)-2])+" "+str(sentence[len(sentence)-1])
        #print(s2)
        if s1==s2 and len(sentence)<10:
            sentence.append(s[2])
            #print(len(sentence))
            s=""
            if len(sentence) >5 and len(sentence)<10:
                for i in range(0,len(sentence)):
                    s=s+" "+sentence[i]
            print(s)
    print("***trigram***")
generate_tri_sent('baseball_trigram','baseball_bigram','baseball_combine_word_tokenize_unigram','baseball_count_first_word','baseball_count_first_second_word')










