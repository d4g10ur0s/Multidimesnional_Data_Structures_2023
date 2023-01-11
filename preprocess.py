import os
import json
import pandas as pd

fr = {
    'A' : 8.496,
    'B'	: 2.072,
    'C'	: 4.538,
    'D'	: 3.384,
    'E'	: 11.160,
    'F'	: 1.812,
    'G'	: 2.470,
    'H'	: 3.003,
    'I'	: 7.544,
    'J'	: 0.196,
    'K'	: 1.101,
    'L'	: 5.489,
    'M'	: 3.012,
    'N'	: 6.654,
    'O'	: 7.163,
    'P'	: 3.167,
    'Q'	: 0.196,
    'R'	: 7.580,
    'S'	: 5.735,
    'T'	: 6.950,
    'U'	: 3.630,
    'V'	: 1.007,
    'W'	: 1.289,
    'X'	: 0.290,
    'Y'	:1.777,
    'Z'	: 0.272,
}


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
    max = 0
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

    print(scientists.iloc[:])

if __name__ == "__main__" :
    main()
