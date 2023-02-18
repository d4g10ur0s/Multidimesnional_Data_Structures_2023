import sys
import pandas as pd
import numpy as np
from gensim.models import Word2Vec as w2v
import gensim.downloader as api
import gensim
import time
import os
import csv
import logging
import inspect
import random as rnd

from data_structures.cosQuadTree import cosQuadTree as cqt
from data_structures.quadTree import QuadTree as qt
from data_structures.rTree import Rtree as rt
from data_structures.kdTree import KDTree as kdtree
from data_structures.kdTree import printNode
from data_structures.cosineLSH import CosineLSH as clsh

path = os.getcwd()
sys.path.append(path)

global gmax
global gdim
global gmean
global gawmax

def preprocessQuery(dim,qv,model):
    qvectors = {}
    i = 0
    qvectors[str(i)] = []
    for k in qv:
        try:
            qvectors[str(i)].append(model.wv[k].mean())
        except:
            qvectors[str(i)].append(np.nan)

    df_query = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in qvectors.items() ]))
    df_query.fillna(value=0.0,inplace=True)

    if dim-len(df_query) > 0:
        d = pd.DataFrame(data=np.zeros((dim, 1)))
        df_query = pd.concat([d,df_query], axis=1, join='outer', ignore_index=False)
        df_query.fillna(value=0.0,inplace=True)

    return df_query[str(0)]

def rTreeSearchInput(quad = False):
    global gmax
    global gdim
    global gmean
    global gawmax

    name = input('Insert a name : ')
    name, max = vectorize(name, gmax)
    d = 0
    if input("Search By Award \n(y/n)\n")=="y":
        d = 1
    for i in range(gdim-d):
        if i < len(name):
            name[i] = (name[i]-gmean)/gmax
            #name[i]=name[i]/gmax#akurh prospa8eia
        else:
            #name.append((ord(' ')-gmean)/gmax)#1. RTREE
            name.append(-gmean/gmax)#2. QUADTREE
    if d==1:
        if quad :
            name.append(-gmean/gmax)#2. QUADTREE
            #name.append((ord(' ')-gmean)/gmax)#1. RTREE
        name.append(int(input("Number of Awards : "))/gawmax)#isws na parw meso oro
    else:
        # no awards
        name.append(rnd.uniform(0, 1))

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
        nname.append(ord(str(i)))
        if max < ord(str(i)):
            max = ord(str(i))
    return [nname, max]


def MainMenu():
    print("\nMENU")
    print("0 - KD Tree")
    print("1 - RTree")
    print("2 - Quad Tree")
    print("3 - Cosine Quad Tree")
    print("-1 - Exit Program\n")

def Menu():
    # menu gia tis diadikasies tou dentrou
    print("\nMENU")
    print("0 - Print Tree")
    print("1 - Search+LSH")
    print("2 - Delete Node")
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
    global gawmax

    path = os.getcwd()
    path+="\\data\\scientists"
    if not(os.path.exists("processedText.csv") or os.path.exists("scientists.csv")):
        max = 0#epilegw thn megisth timh apo encoding gia na yparxei sto diasthma [0,1]
        indx = 1
        first = True
        scientists = None
        ''' anoigw json file me scientists '''
        gmean = 0
        for sc in os.listdir(path):
            scient = pd.read_json(path + "\\"+sc)
            #scient = json.load(f)
            pname , max = vectorize(scient.iloc[0]['name'], max)
            gmean += pd.DataFrame(pname).mean()
            scient.insert(3,"processed_name", [pname], True)
            if first == True :
                scientists = scient
                first = False
            else:
                scientists.loc[indx] = scient.loc[0]
                indx+=1
        gmax = max
        gmean = gmean/indx

    '''   word2vec   '''
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
        gmean = gmean.loc[0]
        temp = (temp-gmean)/gmax#1. RTree
        #w2vec end
        '''   epanatopo8ethsh se arxiko DataFrame   '''
        for i in range(0,indx):
            scientists.at[i,"processed_name"] = temp.iloc[:][i].values.tolist()
        df_input.columns=scientists.loc[:]["name"]
        ''' to scientists paei gia save '''
        writeCsv(scientists,df_input)
        ''' save gmean and gmax '''
        f = open(path+"\\var.txt","w+")
        f.write(str(gmean)+'\n')
        f.write(str(gmax)+'\n')
        f.close()

    #read and start
    f = open(path+"\\var.txt","r+")
    lines= f.readlines()
    gmean = np.float64(lines[0])
    gmax = np.float64(lines[1])
    f.close()

    scientists,df_input = readCsv()

    temp = []
    ''' kanonikopoihsh awards '''
    gawmax = 0
    for i in scientists.loc[:]["awards"]:
        if gawmax < int(i):
            gawmax = i
    tawards = scientists.loc[:,["awards"]]
    scientists.loc[:,["awards"]] = scientists.loc[:,["awards"]]/gawmax
    ''' kanonikopoihsh awards '''

    ''' from dataframe to list '''
    for i in range(0,len(scientists)):
        tdf = list(np.float64(scientists.loc[i,"processed_name"]))
        temp.append( tdf + scientists.loc[i,["awards","name"]].values.tolist() + [tawards.loc[i]["awards"]] )
    ''' from dataframe to list gia na pernaei se domh '''

    ''' lsh model '''
    lsh = clsh(df_input,scientists.iloc[:]["education_text"],len(df_input))

    MainMenu()
    choice1 = int(input())
    # Main Menu choice
    while choice1 != -1:
        if choice1 == 0:
            ''' gia na douleuei pio euelikta '''
            gdim = int(input("How many dimensions ? (<="+str(len(temp[0]) - 2)+")"))
            if gdim == len(temp[0]) - 2 :
                pass
            else:
                ttemp = []
                for i in temp:
                    ttemp.append( i[:gdim] + i[len(i)-2:] )
                    temp = ttemp
            # Kd Tree
            kd = kdtree(temp[:])
            Menu()
            choice2 = int(input())
            while choice2 != -1:
                # Print Tree
                if choice2 == 0:
                    printNode(kd.root)
                # Search + LSH
                elif choice2 == 1:
                    search_result = kd.searching(rTreeSearchInput())
                    for s in search_result :
                        print(str(s))
                # Delete Node
                elif choice2 == 2:
                  print()
                Menu()
                choice2 = int(input())
        # Rtree
        elif choice1 == 1:
            ''' tree creation '''
            gdim = int(input("How many dimensions ? (<="+str(len(temp[0]) - 2)+")"))
            if gdim == len(temp[0]) - 2 :
                pass
            else:
                ttemp = []
                for i in temp:
                    ttemp.append( i[:gdim] + i[len(i)-2:] )
                temp = ttemp
            a = rt(dim=gdim, info=temp[:],min=2, max=4, mval=gmean/gmax)
            Menu()
            choice2 = int(input())
            while choice2 != -1:
                # Print Tree
                if choice2 == 0:
                    ''' RTree '''
                    a.printRTree()  # 1.1
                # Search + LSH
                elif choice2 == 1:
                    search_result = a.rTreeSearch(rTreeSearchInput())
                    to_del = {}
                    names = []
                    awards = []
                    i = 0
                    for s in search_result:
                        if len(s) > 0:
                            print(str(s[0][len(s[0])-2:len(s[0])]))
                            names.append(str(s[0][len(s[0])-2]))
                            awards.append(str(s[0][len(s[0])-1]))
                            to_del[str(i)]=s[1]
                            i = +1
                    while 1 :
                        try :
                            if input("Delete Entry \n(y\\n)\n")=="y":
                                choice = int(input('Delete entry : '))
                                dvec = search_result[choice-1][0]#h malakeia ginetai apo to choice-1
                                a.deleteNode(to_del[str(choice-1)],dvec[:gdim])
                            if input("Education Similarity Query\n(y\\n)\n") == "y":
                                qv = gensim.utils.simple_preprocess(input("Query : \n"))
                                df_query = preprocessQuery(len(df_input),qv,model)
                                sres = lsh.lshQuery2(df_query,names,df_input,window=1)
                        except ValueError:
                            print("Error !")
                        finally:
                            if str(input())=="break":
                                break
                # Delete Node
                elif choice2 == 2:
                    print(a)
                Menu()
                choice2 = int(input())

        #  QuadTree
        elif choice1 == 2:
            gdim = int(input("How many dimensions ? (<="+str(len(temp[0]) - 3)+")"))
            rnd.shuffle(temp[:])
            a = qt(dim = gdim, info = temp[:] ,max=4)#2.0
            a.printQTree()#2.1
            while 1:
                try :
                    arr = a.qSearch(rTreeSearchInput(quad=True))
                    names = []
                    count = 0
                    for i in arr :
                        print("*"*10+" " + str(count)+ " " + "*"*10)
                        print(str("Name : " + str(i[0]) + "\nAwards : " + str(i[1])))
                        count+=1
                        names.append(i[0])
                    if input("Education Similarity Query\n(y\\n)\n") == "y":
                        qv = gensim.utils.simple_preprocess(input("Query : \n"))
                        df_query = preprocessQuery(len(df_input),qv,model)
                        sres = lsh.lshQuery2(df_query,names,df_input,window=1)
                except ValueError:
                    print("Error !")
                finally:
                    if str(input())=="break":
                        break
        elif choice1 == 3:
            gdim = int(input("How many dimensions ? (<="+str(len(temp[0]) - 2)+")"))
            rnd.shuffle(temp[:])
            a = cqt(dim = gdim, info = temp[:] ,max=32)#2.0
            a.printQTree()#2.1

        MainMenu()
        choice1 = int(input())

if __name__ == "__main__":
    main()
