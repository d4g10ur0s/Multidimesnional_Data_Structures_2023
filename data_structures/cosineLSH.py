from sklearn.metrics.pairwise import pairwise_distances

import pandas as pd
import numpy as np

import logging
import inspect

import time
import os
import sys

from collections import defaultdict

class CosineLSH:
    model=None
    def __init__(self,vdoc,doc,dim):
        self.LSH(vdoc,doc,dim)

    def lshQuery(self,query,search_result,df_input,window=None):
        #1. make index for query
        qbin = query.to_numpy(dtype='float32').dot(self.model["random_vectors"])>=0
        powers_of_two = 1 << np.arange(self.model["bnum"] - 1, -1, step=-1)
        bin_indx = qbin.dot(powers_of_two)
        #get the names
        names = self.model["table"][bin_indx]
        #get the vectors
        dvec = []
        distance = []
        for i in names :
            dvec.append(df_input.loc[:,i])
            distance.append(pairwise_distances(df_input.loc[:,i].to_numpy(dtype='float32').reshape(1,-1), query.to_numpy(dtype='float32').reshape(1,-1), metric='cosine').flatten())
        print(str(dvec))
        #calc cosine similarity

        distance_col = 'distance'
        nearest_neighbors = pd.DataFrame({
            'id': df_input.loc[:,names].columns, distance_col: distance
        }).sort_values(distance_col).reset_index(drop=True)
        print(str(nearest_neighbors))

    def LSH(self,vdoc,doc,dim):
        np.random.seed(0)
        inp = None
        names=vdoc.columns
        clen = len(vdoc.columns)
        buckets = {}
        inp = int(input("Percentage : "))
        bnum = 4#round((inp/100)*clen)
        rvec = np.random.randn(dim, bnum)#create random vectors

        vdoc = vdoc.transpose().to_numpy(dtype='float32')
        bin_vectors = vdoc.dot(rvec) >= 0
        powers_of_two = 1 << np.arange(bnum - 1, -1, step=-1)
        bin_indices = bin_vectors.dot(powers_of_two)
        bin_vectors = pd.DataFrame(data=bin_vectors).astype(int).transpose()
        bin_vectors.columns=names

        table = defaultdict(list)
        for idx, bin_index in zip(list(bin_vectors.columns.values),bin_indices):
            table[bin_index].append(idx)

        self.model = {
             'bnum' : bnum,
             'table': table,
             'random_vectors': rvec,
             'bin_indices': bin_indices,
             'bin_indices_bits': bin_vectors,
             }
