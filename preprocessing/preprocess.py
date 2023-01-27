import os
import json
import pandas as pd
import numpy as np
import time
import csv
# from domes.code.rTree import Rtree as rt

def vectorize(name,max):
    nname = []
    for i in name :
        nname.append(ord(i))
        if max < ord(i):
            max = ord(i)
    return [nname, max]

def main():
    path = os.getcwd()
    path+="\\data\\scientists"
    max = 0#epilegw thn megisth timh apo encoding gia na yparxei sto diasthma [0,1]
    indx = 1
    first = True
    scientists = None
    for sc in os.listdir(path):
        scient = pd.read_json(path + "\\"+sc)
        #scient = json.load(f)
        # print('Test',scient.iloc[0]['name'])
       
        pname , max = vectorize(scient.iloc[0]['name'], max)
        scient.insert(3,"processed_name", [pname], True)
        if first == True :
            scientists = scient
            first = False
        else:
            scientists.loc[indx] = scient.loc[0]
            indx+=1

    '''     dhmiourgia dianusmatwn       '''
    temp = []
    for i in range(0,indx):
        temp.append(pd.DataFrame(scientists.iloc[i]["processed_name"]))#normalization
    temp = pd.concat(temp,axis=1, ignore_index=True)
    temp.fillna(0,inplace=True)#opou nan vazw 0
    temp = temp.subtract(temp.mean().mean())/max

    '''   epanatopo8ethsh se arxiko DataFrame   '''
    for i in range(0,indx):
        scientists.at[i,"processed_name"] = temp.iloc[:][i]

    ''' from dataframe to list '''
    temp = []
    with open('data/data.csv', 'w', newline="",encoding="utf-8" ) as myfile:
        wr = csv.writer(myfile)
        for i in range(0,indx):
            tdf = scientists.loc[i,"processed_name"]
            temp = np.concatenate( (tdf, scientists.loc[i,["awards","name"]].values.tolist()),axis=0 )
            wr.writerows([temp])

    # df = pd.read_csv('data.csv')
    # df.transpose()
    # df = df.T
    # df.to_csv('data1.csv',header=False)


    # choice = input("Select : " + "\n" + "1. RTree"+ "\n")
    # if int(choice)==1 :
    #     a = rt(dim = len(temp[0]) - 1, info = temp)
    #     a.printRTree()

if __name__ == "__main__" :
    main()