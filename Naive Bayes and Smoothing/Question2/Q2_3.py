import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import collections

def data_preprocessing():
    sample=input("Enter the sentence")
    text=sample.split()
    if len(text) >=3:
        sample=sample.lower()
        sample=re.sub(r'\d+','',sample)
        sample=sample.split()
        token=[word.strip(string.punctuation) for word in sample]
        table=str.maketrans('','',string.punctuation)
        token=[w.translate(table) for w in token]
        token=[s for s in token if s]
        #print(token)
        return token
    else:
        print("enter the string of length greater or equal to 3")
        quit()
stoken=data_preprocessing()

def cal_unigram_perplexity(stoken,filename1,filename2):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    tokens=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','rb')
    tokens_count=pickle.load(infile)
    infile.close()

    total_unigram=0

    for i in tokens_count.keys():
        total_unigram+=tokens_count.get(i)
    
    vocab=len(tokens_count)
    total_prob=0

    for i in stoken:
        if i in tokens_count.keys():
            count=tokens_count.get(i)
        if i not in tokens_count.keys():
            count=0
        total_prob+=math.log((count+1)/(total_unigram+vocab),10)

    length_sentence=len(stoken)
    #print(length_sentence)
    perplexity=total_prob
    perplexity=pow(10,perplexity)
    perplexity=(1/perplexity)
    perplexity=pow(perplexity,(1/length_sentence))

    hold=filename1[:8]

    print(f"The unigram log probability of the class {hold} is",round(total_prob,6))
    print(f"The unigram perplexity of the given sentence in {hold} class is",round(perplexity,6))
    print("*******")

cal_unigram_perplexity(stoken,'motorcycle_combine_word_tokenize','motorcycle_combine_word_tokenize_unigram')
cal_unigram_perplexity(stoken,'baseball_combine_word_tokenize','baseball_combine_word_tokenize_unigram')


def cal_bigram_perplexity(stoken,filename1,filename2):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    bigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','rb')
    unigram_count=pickle.load(infile)
    infile.close()

    vocab=len(unigram_count)

    total_bigram=0
    total_unigram=0

    for key,value in bigram_count.items():
        total_bigram+=value

    for key,value in unigram_count.items():
        total_unigram+=value
    length_sentence=len(stoken)
    count=0
    total_prob=0

    if stoken[0] in unigram_count.keys():
        count=unigram_count.get(stoken[0])
    else:
        count=0
        value=0
    total_prob=math.log((count+1)/(total_unigram+vocab),10)

    for j in range(length_sentence-1):
        s=str(stoken[j])+" "+str(stoken[j+1])

        if s in bigram_count.keys():
            count=bigram_count.get(s)
        else:
            count=0

        if stoken[j] in unigram_count.keys():
            value=unigram_count.get(stoken[j])
        else:
            value=0
        total_prob+=math.log(((count+1)/(value+vocab)),10)

    perplexity=total_prob
    perplexity=pow(10,perplexity)
    perplexity=(1/perplexity)
    perplexity=pow(perplexity,(1/length_sentence))
    hold=filename1[:8]
    

    print(f"The bigram log probability of the class {hold} is",round(total_prob,6))
    print(f"The bigram perplexity of the given sentence in {hold} class is",round(perplexity,6))
    print("*******")

cal_bigram_perplexity(stoken,'motorcycle_bigram','motorcycle_combine_word_tokenize_unigram')
cal_bigram_perplexity(stoken,'baseball_bigram','baseball_combine_word_tokenize_unigram')


def cal_trigram_perplexity(stoken,filename1,filename2,filename3):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    trigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','rb')
    bigram_count=pickle.load(infile)
    infile.close()

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','rb')
    unigram_count=pickle.load(infile)
    infile.close()

    vocab=len(unigram_count)
    

    total_unigram=0
    total_bigram=0
    total_trigram=0

    for key,value in unigram_count.items():
        total_unigram+=value

    for key,value in bigram_count.items():
        total_bigram+=value

    for key,value in trigram_count.items():
        total_trigram+=value

    length_sentence=len(stoken)
    count=0
    value=0
    total_prob=0

    if stoken[0] in unigram_count.keys():
        count=unigram_count.get(stoken[0])
    else:
        count=0
    total_prob=math.log((count+1)/(total_unigram+vocab),10)

    s=str(stoken[0])+" "+str(stoken[1])

    if s in bigram_count.keys():
        count=bigram_count.get(s)
    else:
        count=0
    if stoken[0] in unigram_count.keys():
        value=unigram_count.get(stoken[0])
    else:
        value=0
    total_prob+=math.log((count+1)/(value+vocab),10)


    for j in range(length_sentence-2):
        s=str(stoken[j])+" "+str(stoken[j+1])+" "+str(stoken[j+2])
        #print(s)

        if s in trigram_count.keys():
            count=trigram_count.get(s)
        else:
            count=0
        s=str(stoken[j])+" "+str(stoken[j+1])
        if s in bigram_count.keys():
            value=bigram_count.get(s)
        else:
            value=0
        total_prob+=math.log((count+1)/(value+vocab),10)

    perplexity=total_prob
    perplexity=pow(10,perplexity)
    perplexity=(1/perplexity)
    perplexity=pow(perplexity,(1/length_sentence))
    hold=filename1[:8]

    print(f"The trigram log probability of the class {hold} is",round(total_prob,6))
    print(f"The trigram perplexity of the given sentence in {hold} class is",round(perplexity,6))
    print("*******")

cal_trigram_perplexity(stoken,'motorcycle_trigram','motorcycle_bigram','motorcycle_combine_word_tokenize_unigram')
cal_trigram_perplexity(stoken,'baseball_trigram','baseball_bigram','baseball_combine_word_tokenize_unigram')


























