import json
import pandas as pd
import numpy as np
from domes.code.rTree import Rtree as rt
from domes.code.quadTree import QuadTree as qt

import logging
import inspect

from gensim.models import Word2Vec as w2v
import gensim.downloader as api
import gensim

import time
import os
import sys

global gmax
global gdim
global gmean

def rTreeSearchInput():
    global gmax
    global gdim
    global gmean

    name = input('Insert a name : ')
    name, max = vectorize(name,gmax)
    for i in range(gdim):
        if i < len(name):
            name[i] = (name[i]-gmean)/gmax
        else:
            name.append(0)
    return name


def vectorize(name,max):
    nname = []
    for i in name :
        nname.append(ord(i))
        if max < ord(i):
            max = ord(i)
    return [nname, max]

def main():
    print(pd.__version__)
    global gmax
    global gdim
    global gmean

    path = os.getcwd()
    path+="\\tutorial\\scientists"
    max = 0#epilegw thn megisth timh apo encoding gia na yparxei sto diasthma [0,1]
    indx = 1
    first = True
    scientists = None
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

    '''     dhmiourgia dianusmatwn       '''
    temp = []

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


    model = w2v.load('readyvocab.model')

    scientists['education_vector'] = np.nan
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
    ''' Allagh apo indx se onomata '''
    i=0
    for i in range(0,len(df_input.axes[1])):
        df_input.rename(columns = {str(i):scientists.iloc[i]["name"]}, inplace = True)

    '''to model.wv exei to vector'''
    for i in range(0,indx):
        temp.append(pd.DataFrame(scientists.iloc[i]["processed_name"]))#normalization
    temp = pd.concat(temp,axis=1, ignore_index=True)
    temp.fillna(0,inplace=True)#opou nan vazw 0
    gmean = temp.mean().mean()
    temp = temp.subtract(temp.mean().mean())/max
    #temp = temp/max
    '''   epanatopo8ethsh se arxiko DataFrame   '''
    for i in range(0,indx):
        scientists.at[i,"processed_name"] = temp.iloc[:][i]

    ''' from dataframe to list '''
    temp = []
    for i in range(0,indx):
        tdf = scientists.loc[i,"processed_name"]
        temp.append( tdf.iloc[:].values.tolist() + scientists.loc[i,["awards","name"]].values.tolist() )

    ''' RTree '''
    gdim = int(input("How many dimensions ? (<="+str(len(temp[0]) - 2)+")"))
    a = rt(dim = gdim, info = temp[:],min=2 , max=6,mval=gmean/gmax)
    a.printRTree()#1.1
    search_result = a.rTreeSearch(rTreeSearchInput())
    for s in search_result:
        if len(s)>0:
            print(str(s[len(s)-1]))

    ''' QuadTree '''
    #a = qt(dim = len(temp[0])-1, info = temp[:24])#2.0
    #a.printQTree()#2.1

if __name__ == "__main__" :
    main()
