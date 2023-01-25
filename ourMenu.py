import csv
import random
import string
from rangeTree import RangeTree,printNode
import pandas as pd
import numpy as np


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
        # print(nname)
        if max < ord(i):
            max = ord(i)
    return [nname, max]

# Diavasma arxeiou
filename = 'data.csv'
my_root = None
with open(filename, mode='r', encoding="utf-8") as csv_file:
    csv_reader = pd.read_csv(csv_file, sep=';')
    arr = []
    for i in csv_reader.values.tolist():
        arr.append(string2float(i[0].split(','))) 
    # Gia na ftiaksoume to tree
    max = csv_reader.max().max()
    mean = csv_reader.mean().mean()
    rt = RangeTree(arr)

#menu gia tis diadikasies tou dentrou
print("\nMENU")
print("0 - Print Tree")
print("1 - Range Search")
print("2 - Insert Node")
print("3 - Delete Node")
print("4 - Update Node")
print("5 - kNN")
print("-1 - Exit Program\n")


choice = int(input())

while choice != -1:
    # Print Tree
    if choice == 0:
        print('-----------------------')
        printNode(rt.root)
        print('-----------------------')

    if choice == 1:
        a = rt.root
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

        Adi = [0.000943704,0.00206496,0.00222514,-0.00011348,0.00152035,0.002193104,0.001968852,0.002353283,0.00222514,0.002513462,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628]
        print('Root1',rt.root)
        Vincent = [0.001232027,0.002417355,0.002193104,0.002385319,-0.00011348,0.001616458,0.00222514,0.002385319,0.002032924,0.002096996,0.002385319,0.002577534,-0.00011348,0.000943704,0.002577534,0.001968852,0.002385319,0.001968852,0.002545498,0.002417355,0.002129032,0.002129032,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628,-0.001138628]
        rt.root = rt.delete(rt.root,Adi)
        printNode(rt.root)
        print('Root2',rt.root)
        
        print('-----------------------')

    print("\nMENU")
    print("0 - Print Tree")
    print("1 - Range Search")
    print("2 - Insert Node")
    print("3 - Delete Node")
    print("4 - Update Node")
    print("5 - kNN")
    print("-1 - Exit Program\n")
    choice = int(input())
