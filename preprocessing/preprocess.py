import pandas as pd
import numpy as np
import sys
from gensim.models import Word2Vec as w2v
import gensim.downloader as api
import gensim
import time
import os
import csv

path = os.getcwd()
sys.path.append(path)
from data_structures.rTree import Rtree as rt
from data_structures.rangeTree import RangeTree as ranget
from data_structures.rangeTree import printNode

from data_structures import quadTree as qt


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

# String to Float
def string2float(arr):
    t= []
    for i in range(0,len(arr)-1):
        t.append(float(arr[i]))
    t.append(arr[len(arr)-1])
    return t


def vectorize(name,max):
    nname = []
    for i in name :
        nname.append(ord(i))
        if max < ord(i):
            max = ord(i)
    return [nname, max]

def MainMenu() : 
    print("\nMENU")
    print("0 - Range Tree")
    print("1 - RTree")
    print("2 - Quad Tree")
    print("3 - KD Tree")
    print("-1 - Exit Program\n")

def Menu(): 
    #menu gia tis diadikasies tou dentrou
    print("\nMENU")
    print("0 - Print Tree")
    print("1 - Range Search")
    print("2 - Insert Node")
    print("3 - Delete Node")
    print("4 - Update Node")
    print("5 - kNN")
    print("-1 - Exit Program\n")

def main():

    global gmax
    global gdim
    global gmean

    path = os.getcwd()
    path+="\\data\\scientists"
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
    AYTA MONO STHN ARXH
    '''
    
    '''
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus = api.load('text8')
    print(inspect.getsource(corpus.__class__))
    print(inspect.getfile(corpus.__class__))
    model = w2v(corpus)
    model.save('.\\readyvocab.model')
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

    print(df_input)
    
    
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


    temp2 = []
    with open('data/data.csv', 'w', newline="",encoding="utf-8" ) as myfile:
        wr = csv.writer(myfile)
        for i in range(0,indx):
            tdf = scientists.loc[i,"processed_name"]
            temp2 = np.concatenate( (tdf, scientists.loc[i,["awards","name"]].values.tolist()),axis=0 )
            wr.writerows([temp2])


    
    #menu gia epilogi domis
    #menu gia tis diadikasies tou dentrou

    MainMenu()
    choice = int(input())

    while choice != -1:
        ''' Range Tree '''
        if choice == 0:
            # Diavasma arxeiou
            filename = 'data/data.csv'
            with open(filename, mode='r', encoding="utf-8") as csv_file:
                csv_reader = pd.read_csv(csv_file, sep=';')
                arr = []
                for i in csv_reader.values.tolist():
                    arr.append(string2float(i[0].split(','))) 
                # Gia na ftiaksoume to tree
                max = csv_reader.max().max()
                mean = csv_reader.mean().mean()
                rangeTree = ranget(arr)
            Menu()
            choice2 = int(input())
            while choice2!= -1: 
                    # Print Tree
                if choice == 0:
                    print('-----------------------')
                    print('Root1',rangeTree.root)
                    # printNode(rt.root)
                    printNode(rangeTree.root)
                    print('-----------------------')

                if choice == 1:
                    a = rangeTree.root
                    print('------RIGHT---------')
                    printNode(a.right)
                    print('-----------------------')
                    print('------Left---------')
                    printNode(a.Left)
                    print('-----------------------')
                # Delete Node
                elif choice == 3:
                    name = input("Give the name of the scientist you want to delete: ")
                    temp = []
                    max = 0 
                    vectorizeName, max = vectorize(name,max)
                    temp.append(pd.DataFrame(vectorizeName))#normalization
                    temp = pd.concat(temp,axis=1, ignore_index=True)
                    temp = np.pad(temp, ((0, 43 - len(temp)),(0,0)), 'constant')
                    temp = pd.DataFrame(temp)
                    max = 31215
                    mean = 35.54227033911798
                    temp = temp.subtract(mean)/max
                    temp_list = temp.values.tolist()
                    merged_list = []
                    for l in temp_list:
                        merged_list += l
                    # print('TempList',merged_list)

                    Adi = [0.000943704,0.00206496,0.00222514,-0.00011348,0.00152035,0.002193104,0.001968852,0.002353283,0.00222514,0.002513462,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,6]
                    print('Root1',rangeTree.root)
                    Vincent = [0.001232027,0.002417355,0.002193104,0.002385319,-0.00011348,0.001616458,0.00222514,0.002385319,0.002032924,0.002096996,0.002385319,0.002577534,-0.00011348,0.000943704,0.002577534,0.001968852,0.002385319,0.001968852,0.002545498,0.002417355,0.002129032,0.002129032,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628]
                    rt.root = rangeTree.delete(rangeTree.root,Adi)
                    printNode(rangeTree.root)
                    print('Root2',rangeTree.root)
                    
                    print('-----------------------')
                Menu()
                choice2 = int(input())
        
        elif choice == 1:
            Menu()
            choice2 = int(input())
            while choice2 != -1 :
                if choice2 == 0:
                    ''' RTree '''
                    gdim = int(input("How many dimensions ? (<="+str(len(temp[0]) - 2)+")"))
                    a = rt(dim = gdim, info = temp[:],min=2 , max=4,mval=gmean/gmax)
                    a.printRTree()#1.1
                    search_result = a.rTreeSearch(rTreeSearchInput())
                    for s in search_result:
                        if len(s)>0:
                            print(str(s[len(s)-1]))
                Menu()
                choice2 = int(input())

        MainMenu()
        choice = int(input())

    ''' QuadTree '''
    #a = qt(dim = len(temp[0])-1, info = temp[:24])#2.0
    #a.printQTree()#2.1

if __name__ == "__main__" :
    main()
