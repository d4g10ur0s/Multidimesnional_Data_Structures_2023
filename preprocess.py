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


def vectorize(name,max):
    nname = []
    for i in name :
        nname.append(ord(i))
        if max < ord(i):
            max = ord(i)
    return [nname, max]

def main():
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

    model = w2v.load('readyvocab.model')

    scientists['education_vector'] = np.nan
    processed_sentences = []
    for i in range(0,indx):
        if pd.isnull(scientists.iloc[i]["education_text"]):
            processed_sentences.append(gensim.utils.simple_preprocess(" "))
        else:
            processed_sentences.append(gensim.utils.simple_preprocess(scientists.iloc[i]["education_text"]))
    i=0
    for k in processed_sentences:
        arr = []
        for v in k :
            try :
                arr.append(model.wv[v])
            except KeyError :
                arr.append(np.nan)
        scientists.iloc[i]["education_vector"]=arr
        print(str(arr))
        input('a')
        i+=1

    '''
    '''to model.wv exei to vector'''

    for i in range(0,indx):
        temp.append(pd.DataFrame(scientists.iloc[i]["processed_name"]))#normalization
    temp = pd.concat(temp,axis=1, ignore_index=True)
    temp.fillna(0,inplace=True)#opou nan vazw 0
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

    ''' QuadTree '''
    #a = qt(dim = len(temp[0])-1, info = temp[:24])
    #a.printQTree()

    #choice = input("Select : " + "\n" + "1. RTree"+ "\n")
    #if int(choice)==1 :
    #len(temp[0]) - 1
    a = rt(dim = 5, info = temp[:],min=2 , max=10)
    a.printRTree()
    #print(str(a.getInfoNum()))

if __name__ == "__main__" :
    main()
