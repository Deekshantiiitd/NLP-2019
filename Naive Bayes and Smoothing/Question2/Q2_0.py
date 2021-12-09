import glob
import codecs
import string, re, pickle, math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import collections

#data preprocessing
def data_comine(folder_name,file_name):
    files = [f for f in glob.glob(f'F:/MTECH1/NLP/20_newsgroups/{folder_name}' + "**/*", recursive=True)]
    fp1=codecs.open(f'F:/MTECH1/NLP/Assignment3/combine2/{file_name}','w+',encoding='utf-8',errors='ignore')
    for i in files:
        fp=codecs.open(f'{i}','r',encoding='utf-8',errors='ignore')
        text=fp.read()
        text=text.lower()
        text=re.sub(r'\n','.',text)
        text=re.sub(r'.*[lL]ines: \d+','',text)
        fp1.write(text)
#data_comine('rec.motorcycles','motorcycle_combine')
#data_comine('rec.sport.baseball','baseball_combine')

def data_preprocessing(filename):
    fp1=codecs.open(f'F:/MTECH1/NLP/Assignment3/combine2/{filename}','r',encoding='utf-8',errors='ignore')
    text=fp1.read()

    #remove digits
    text=re.sub(r'\d+','',text)

    #sentence tokenization
    stokens=sent_tokenize(text)
    print(len(stokens))

    text=text.split()
    tokens=[word.strip(string.punctuation) for word in text]
    table=str.maketrans('','',string.punctuation)
    tokens=[w.translate(table) for w in tokens]

    outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename}_sent_tokenize','wb')
    pickle.dump(stokens,outfile)
    outfile.close()
    
    #remove blank_space
    tokens=[s for s in tokens if s]
    print((tokens))

    outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename}_word_tokenize','wb')
    pickle.dump(tokens,outfile)
    outfile.close()

#data_preprocessing('motorcycle_combine')
#data_preprocessing('baseball_combine')

def unigram(filename):
    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename}','rb')
    tokens=pickle.load(infile)
    infile.close()

    count_dict={}
    for i in tokens:
        if i in count_dict.keys():
            count_dict[i]+=1
        if i not in count_dict.keys():
            count_dict[i]=1

    outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename}_unigram','wb')
    pickle.dump(count_dict,outfile)
    outfile.close()
    print(len(count_dict))
#unigram('motorcycle_combine_word_tokenize')#
#unigram('baseball_combine_word_tokenize')# 



def bigram(filename1,filename2,filename3):
    
    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    stokens=pickle.load(infile)
    infile.close()

    sent_word_tokens=[]
    for i in stokens:
        text=i.split()
        tokens=[word.strip(string.punctuation) for word in text]
        table=str.maketrans('','',string.punctuation)
        tokens=[w.translate(table) for w in tokens]
        sent_word_tokens.append(tokens)

    count_first_word={}
    count_bigram={}
    for i in sent_word_tokens:
    
        for j in range(len(i)-1):
                
                if i[0] not in count_first_word.keys():
                    count_first_word[i[0]]=1
                    break
                if i[0] in count_first_word.keys():
                    count_first_word[i[0]]+=1
                    break
    #print(count_first_word)
                
    for i in sent_word_tokens:
        
        for j in range(len(i)-1):
                s=str(i[j])+" "+str(i[j+1])

                if s not in count_bigram.keys():
                    count_bigram[s]=1
                if s in count_bigram.keys():
                    count_bigram[s]+=1
    print(count_bigram)

    outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','wb')
    pickle.dump(count_first_word,outfile)
    outfile.close()

    outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename3}','wb')
    pickle.dump(count_bigram,outfile)
    outfile.close()

#bigram('motorcycle_combine_sent_tokenize','motorcycle_count_first_word','motorcycle_bigram')
#bigram('baseball_combine_sent_tokenize','baseball_count_first_word','baseball_bigram')

def trigram(filename1,filename2,filename3):

    infile=open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename1}','rb')
    stokens=pickle.load(infile)
    infile.close()
    
    sent_word_tokens=[]
    for i in stokens:
        text=i.split()
        tokens=[word.strip(string.punctuation) for word in text]
        table=str.maketrans('','',string.punctuation)
        tokens=[w.translate(table) for w in tokens]
        sent_word_tokens.append(tokens)
    #print(sent_word_tokens)

    count_first_second_word={}
    for i in sent_word_tokens:
        for j in range(len(i)-1):
            s=str(i[j])+" "+str(i[j+1])
            if s not in count_first_second_word.keys():
                count_first_second_word[s]=1
                break
            if s in count_first_second_word.keys():
                count_first_second_word[s]+=1
                break

    count_trigram={}
    for i in sent_word_tokens:
        #print(i)
        for j in range(len(i)-2):
                s=str(i[j])+" "+str(i[j+1])+" "+str(i[j+2])
                if s not in count_trigram.keys():
                    count_trigram[s]=1
                if s in count_trigram.keys():
                    count_trigram[s]+=1
    print(count_trigram)

    outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename2}','wb')
    pickle.dump(count_trigram,outfile) 
    outfile.close()

    outfile =open(f'F:/MTECH1/NLP/Assignment3/pickles2/{filename3}','wb')
    pickle.dump(count_first_second_word,outfile)
    outfile.close()

#trigram('motorcycle_combine_sent_tokenize','motorcycle_trigram','motorcycle_count_first_second_word')
#trigram('baseball_combine_sent_tokenize','baseball_trigram','baseball_count_first_second_word')


