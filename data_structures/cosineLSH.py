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

    def lshQuery(self,search_result,query,window=None,alt=0):
        #1. make index for query
        qbin = query.transpose().to_numpy(dtype='float32').dot(to_numpyself.model["random_vectors"])>=0
        print(str(qbin))

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

        self.model = {'table': table,
             'random_vectors': rvec,
             'bin_indices': bin_indices,
             'bin_indices_bits': bin_vectors}
