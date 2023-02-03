import sys
import pandas as pd
import numpy as np
from gensim.models import Word2Vec as w2v
import gensim.downloader as api
import gensim
import time
import os
import csv

path = os.getcwd()
sys.path.append(path)

from data_structures.quadTree import QuadTree as qt
from data_structures.rTree import Rtree as rt
from data_structures.rangeTree import RangeTree as ranget
from data_structures.rangeTree import printNode
from data_structures.cosineLSH import CosineLSH

#from data_structures.quadTree import QuadTree as qt
#from data_structures.rTree import Rtree as rt
#from data_structures.rangeTree import RangeTree as ranget
#from data_structures.rangeTree import printNode

global gmax
global gdim
global gmean


def rTreeSearchInput():
    global gmax
    global gdim
    global gmean

    name = input('Insert a name : ')
    name, max = vectorize(name, gmax)
    for i in range(gdim):
        if i < len(name):
            name[i] = (name[i]-gmean)/gmax
        else:
            name.append(0)
    return name

# String to Float


def string2float(arr):
    t = []
    for i in range(0, len(arr)-1):
        t.append(float(arr[i]))
    t.append(arr[len(arr)-1])
    return t


def vectorize(name, max):
    nname = []
    for i in name:
        nname.append(ord(i))
        if max < ord(i):
            max = ord(i)
    return [nname, max]


def MainMenu():
    print("\nMENU")
    print("0 - Range Tree")
    print("1 - RTree")
    print("2 - Quad Tree")
    print("3 - KD Tree")
    print("-1 - Exit Program\n")


def Menu():
    # menu gia tis diadikasies tou dentrou
    print("\nMENU")
    print("0 - Print Tree")
    print("1 - Range Search")
    print("2 - Insert Node")
    print("3 - Delete Node")
    print("4 - Update Node")
    print("5 - kNN")
    print("-1 - Exit Program\n")


def vectorize_input(input_text, model, max):
    processed_sentences = gensim.utils.simple_preprocess(input_text)
    vector = []
    for k in processed_sentences:
        try:
            vector.append(model.wv[k].mean())
        except:
            vector.append(np.nan)
    print(max - len(vector))
    for i in range(max - len(vector)):

        vector.append(0)
    return vector


def writeCsv(input_text,input_text2):
    word2vecNames = input_text2
    # Write the dataframe to a CSV file
    word2vecNames.to_csv('processedText.csv', index=False)

    scientists = input_text
    scientists.to_csv('scientists.csv', index=False)

def readCsv() :
    scientists = pd.read_csv("scientists.csv",converters={"processed_name": lambda x: x.strip("[]").split(", ")})
    df_input = pd.read_csv("processedText.csv")
    return scientists,df_input

def main():
    global gmax
    global gdim
    global gmean

    path = os.getcwd()
    path+="\\data\\scientists"
    if not(os.path.exists("processedText.csv") or os.path.exists("scientists.csv")) :
        max = 0#epilegw thn megisth timh apo encoding gia na yparxei sto diasthma [0,1]
        indx = 1
        first = True
        scientists = None
        ''' anoigw json file me scientists '''
        for sc in os.listdir(path):
            scient = pd.read_json(path + "\\"+sc)
            #scient = json.load(f)
            pname , max = vectorize(scient.iloc[0]['name'], max)
            m = pd.DataFrame(pname).mean()
            scient.insert(3,"processed_name", [pname], True)
            if first == True :
                scientists = scient
                first = False
            else:
                scientists.loc[indx] = scient.loc[0]
                indx+=1
        gmax = max
        input(str(gmax))

    '''     dhmiourgia dianusmatwn       '''

    '''
    word2vec
    '''
    '''
    AYTA MONO STHN ARXH

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus = api.load('text8')
    print(inspect.getsource(corpus.__class__))
    print(inspect.getfile(corpus.__class__))
    model = w2v(corpus)
    model.save('.\\readyvocab.model')

    AYTA MONO STHN ARXH
    '''
    #w2v start
    model = w2v.load('readyvocab.model')

    if not(os.path.exists("processedText.csv") or os.path.exists("scientists.csv")) :
        processed_sentences = []
        for i in range(0,indx):
            if pd.isnull(scientists.iloc[i]["education_text"]):
                processed_sentences.append(gensim.utils.simple_preprocess("No Information"))
            else:
                processed_sentences.append(gensim.utils.simple_preprocess(scientists.iloc[i]["education_text"]))

        vectors = {}
        i = 0
        for v in processed_sentences:
            vectors[str(i)] = []
            for k in v:
                try:
                    vectors[str(i)].append(model.wv[k].mean())
                except:
                    vectors[str(i)].append(np.nan)
            i+=1

        df_input = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in vectors.items() ]))
        for i in range(0,len(vectors)):
            df_input.fillna(value=0.0,inplace=True)
            df_input[str(i)].replace(to_replace=0,value=df_input[str(i)].mean(),inplace=True )

        temp = []
        for i in range(0,indx):
            temp.append(pd.DataFrame(scientists.iloc[i]["processed_name"]))#normalization
        temp = pd.concat(temp,axis=1, ignore_index=True)
        temp.fillna(0,inplace=True)#opou nan vazw 0
        gmean = temp.mean(axis=1).mean()
        input(str(gmean))
        temp = temp/gmax#1
        #w2vec end
        '''   epanatopo8ethsh se arxiko DataFrame   '''
        for i in range(0,indx):
            scientists.at[i,"processed_name"] = temp.iloc[:][i].values.tolist()

        df_input.columns=scientists.loc[:]["name"]

        ''' RTree '''
        gdim = int(input("How many dimensions ? (<="+str(len(temp[0]) - 2)+")"))
        '''
            >Possible parameter values
            1. polwsh mean diairesh me max, max = 8, mval=gmean/gmax, _mval=mval
            2. anti gia 0 pairnw (ord(space)-gmean)/gmax, mval=gmean/gmax, _mval=mval*1.5, max=8
        '''
        ''' to scientists paei gia save '''
        # lsh = clsh(df_input,scientists.iloc[:]["education_text"],len(df_input))
        writeCsv(scientists,df_input)

    scientists,df_input = readCsv()

    temp = []
    ''' from dataframe to list '''
    for i in range(0,len(scientists)):
        tdf = list(np.float64(scientists.loc[i,"processed_name"]))
        temp.append( tdf + scientists.loc[i,["awards","name"]].values.tolist() )
    # menu gia epilogi domis
    # menu gia tis diadikasies tou dentrou
    print(temp[0])



    MainMenu()
    choice = int(input())

    while choice != -1:
        # Range Tree
        if choice == 0:
            # Diavasma arxeiou
           
            Menu()
            choice2 = int(input())
            while choice2 != -1:
                # Print Tree
                if choice == 0:
                  
                    Menu()
                    choice2 = int(input())



        elif choice == 1:
            Menu()
            gmax = 31215
            gmean = 35.2353000948381
            choice2 = int(input())
            while choice2 != -1:
                if choice2 == 0:
                    ''' RTree '''
                    gdim = int(
                        input("How many dimensions ? (<="+str(len(temp[0]) - 2)+")"))
                    a = rt(dim=gdim, info=temp[:],
                           min=2, max=4, mval=gmean/gmax)
                    a.printRTree()  # 1.1

                elif choice2 == 1:
                    gdim = 44
                    a = rt(dim=gdim, info=temp[:],
                           min=2, max=4, mval=gmean/gmax)
                    search_result = a.rTreeSearch(rTreeSearchInput())

                Menu()
                choice2 = int(input())

        #  QuadTree 
        elif choice == 2:
                

            MainMenu()
            choice = int(input())

    
    # a = qt(dim = len(temp[0])-1, info = temp[:24])#2.0
    # a.printQTree()#2.1


if __name__ == "__main__":
    main()
