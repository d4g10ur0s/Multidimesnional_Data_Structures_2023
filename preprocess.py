import os
import json
import pandas as pd
import numpy as np

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
        temp.append(pd.DataFrame(scientists.iloc[i]["processed_name"])/max)
    temp = pd.concat(temp,axis=1, ignore_index=True)
    temp.fillna(0,inplace=True)#opou nan vazw 0

    '''   epanatopo8ethsh se arxiko DataFrame   '''
    for i in range(0,indx):
        scientists.at[i,"processed_name"] = temp.iloc[:][i]

    print(scientists.iloc[10])

if __name__ == "__main__" :
    main()
