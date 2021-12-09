import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import collections,operator
from nltk.corpus import stopwords 

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

def unigram_adv_smooth(stoken,filename1):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    unigram_count=pickle.load(infile)
    infile.close()

    total_unigram=0
    for i in unigram_count.keys():
        total_unigram+=unigram_count.get(i)

    new_freq_count={}
    for key,value in unigram_count.items():
        if value in new_freq_count.keys():
            new_freq_count[value]+=1
        else:
            new_freq_count[value]=1
    sorted_new_freq_count={}

    for i in sorted(new_freq_count.keys()):
        sorted_new_freq_count.update({i:new_freq_count[i]})
    #print(sorted_new_freq_count)

    k=5
    total_prob=0
    temp=((k+1)*sorted_new_freq_count[k+1])/(sorted_new_freq_count[1])
    #print(temp)

    for i in stoken:
        if i in unigram_count.keys():
            c=unigram_count.get(i)
        if i not in unigram_count.keys():
            c=0
        if c==0:
            total_prob+=math.log((sorted_new_freq_count.get(1)/total_unigram),10)
        if c>k:
            total_prob+=math.log((c/total_unigram),10)
        if 0<c<=k:
            s=(((c+1)*sorted_new_freq_count[c+1]/sorted_new_freq_count[c])-c*(temp))/(1-temp)
            #print(s)
            total_prob+=math.log((s/total_unigram),10)
    hold=filename1[:8]
    print(f"the unigram prob. of class {hold}",total_prob)

unigram_adv_smooth(stoken,'motorcycle_combine_word_tokenize_unigram')
unigram_adv_smooth(stoken,'baseball_combine_word_tokenize_unigram')

def bigram_adv_smooth(stoken,filename1):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    bigrams_count=pickle.load(infile)
    infile.close()
    #print(bigrams_count)

    bigram_count={}

    for key in bigrams_count.keys():
        s=key.split()
        if len(s)==2:
            bigram_count.update({key:bigrams_count[key]})
    #print(bigram_count)

    total_bigram=0

    for i in bigram_count.keys():
        total_bigram+=bigram_count.get(i)

    new_freq_count={}
    for key,value in bigram_count.items():
        if value in new_freq_count.keys():
            new_freq_count[value]+=1
        else:
            new_freq_count[value]=1
    new_freq_count.update({1:1})

    sorted_new_freq_count={}
    for i in sorted(new_freq_count.keys()):
        sorted_new_freq_count.update({i:new_freq_count[i]})
    #print(sorted_new_freq_count)

    k=5
    total_prob=0
    temp=((k+1)*sorted_new_freq_count[k+1])/(sorted_new_freq_count[2])
    #print(temp)

    for i in range(len(stoken)-1):
        s=str(stoken[i])+" "+str(stoken[i+1])

        if s in bigram_count.keys():
            c=bigram_count.get(i)
        if i not in bigram_count.keys():
            c=0
        if c==0:
            total_prob+=math.log((sorted_new_freq_count.get(2)/total_bigram),10)
        if c>k:
            total_prob+=math.log((c/total_bigram),10)
        if 0<c<=k:
            s=(((c+1)*sorted_new_freq_count[c+1]/sorted_new_freq_count[c])-c*(temp))/(1-temp)
            #print(s)
            total_prob+=math.log((s/total_bigram),10)
    hold=filename1[:8]
    print(f"the bigram prob. of class {hold}",total_prob)

bigram_adv_smooth(stoken,'motorcycle_bigram')
bigram_adv_smooth(stoken,'baseball_bigram')

def trigram_adv_smooth(stoken,filename1):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    trigrams_count=pickle.load(infile)
    infile.close()
    #print(bigrams_count)

    trigram_count={}

    for key in trigrams_count.keys():
        s=key.split()
        if len(s)==3:
            trigram_count.update({key:trigrams_count[key]})
    #print(bigram_count)

    total_trigram=0

    for i in trigram_count.keys():
        total_trigram+=trigram_count.get(i)

    new_freq_count={}
    for key,value in trigram_count.items():
        if value in new_freq_count.keys():
            new_freq_count[value]+=1
        else:
            new_freq_count[value]=1
    new_freq_count.update({1:1})

    sorted_new_freq_count={}
    for i in sorted(new_freq_count.keys()):
        sorted_new_freq_count.update({i:new_freq_count[i]})
    #print(sorted_new_freq_count)

    k=5
    total_prob=0
    temp=((k+1)*sorted_new_freq_count[k+1])/(sorted_new_freq_count[1])
    #print(temp)

    for i in range(len(stoken)-2):
        s=str(stoken[i])+" "+str(stoken[i+1])+" "+str(stoken[i+2])

        if s in trigram_count.keys():
            c=trigram_count.get(i)
        if i not in trigram_count.keys():
            c=0
        if c==0:
            total_prob+=math.log((sorted_new_freq_count.get(2)/total_trigram),10)
        if c>k:
            total_prob+=math.log((c/total_trigram),10)
        if 0<c<=k:
            s=(((c+1)*sorted_new_freq_count[c+1]/sorted_new_freq_count[c])-c*(temp))/(1-temp)
            #print(s)
            total_prob+=math.log((s/total_trigram),10)
    hold=filename1[:8]
    print(f"the trigram prob. of class {hold}",total_prob)
trigram_adv_smooth(stoken,'motorcycle_trigram')
trigram_adv_smooth(stoken,'baseball_trigram')





