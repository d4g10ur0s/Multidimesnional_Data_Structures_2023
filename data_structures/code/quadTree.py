import time
import math
import random as rd

class QuadNode :
    def __init__(self,dim,parent=None,leaf = True):
        self._dim = dim
        ''' tree controlling '''
        self._parent = parent
        self._leaf = leaf
        self._empty = True
        self._info = None
        ''' intervals for parsing '''
        #(intervals , child) || info
        self.nw = None
        self.ne = None
        self.se = None
        self.sw = None

    ''' Utility '''
    def printNode(self):
        if self._empty :
            print("Empty Node")
        else:
            print("Name : " + str(self._info[len(self._info)-1]))
            print("Awards : "+ str(self._info[len(self._info)-2]))
    def getCoordinates(self):
        return [self.nw,self.ne,self.se,self.sw]
    def isLeaf(self):
        return self._leaf
    def isEmpty(self):
        return self._empty
    def getInfo(self):
        return self._info
    ''' Information is installed at node '''
    def setInfo(self,info):
        if info==None:
            self._empty = True
        else:
            self._empty = False
        self._info = info
    ''' go to next node '''
    def getDirections(self,info):
        ''' its only 2-d '''
        x1 = 0
        ''' name coordinate '''
        for i in range(0,self._dim):
            x1 += info[i]
        ''' award coordinate '''
        y1 = info[self._dim-2]
        tinfo = (x1,y1)

        if tinfo[0] + self._info[0] <= 0 and tinfo[1]+self._info[1] > 0 :
            return self.nw
        elif tinfo[0] + self._info[0] > 0 and tinfo[1]+self._info[1] >= 0 :
            return self.ne
        elif tinfo[0] + self._info[0] >= 0 and tinfo[1]+self._info[1] < 0 :
            return self.se
        elif tinfo[0] + self._info[0] < 0 and tinfo[1]+self._info[1] <= 0 :
            return self.sw

    def newIntervals(self, info, linfo,new_kids):
        self.nw = new_kids[0]
        self.ne = new_kids[1]
        self.se = new_kids[2]
        self.sw = new_kids[3]
        self._leaf = False
        self._empty = False
        ''' its only 2-d '''
        x1 = 0
        x2 = 0
        ''' name coordinate '''
        for i in range(0,self._dim):
            x1 += info[i]
            x2 += linfo[i]
        ''' award coordinate '''
        y1 = info[self._dim-2]
        y2 = linfo[self._dim-2]
        '''
        everything is under midpoint's control
        '''
        self._info = ( (x1-x2)/2, (y1+y2)/2)
        '''#get a random point , that is on the line that info and linfo create
        y0 = 0
        x0 = 0
        if x1 < x2:
            x0 = rd.uniform(x1, x2)
            y0 = (y2-y1)/(x2-x1) * (x0-x1) + y1
        elif x2 < x1 :
            x0 = rd.uniform(x2, x1)
            y0 = (y1-y2)/(x1-x2) * (x0-x2) + y2
        else:
            x0 = rd.uniform(x1-1, x2+1)
            y0 = (y1+y2)/2

        if y2==y1 :
            y0 = rd.uniform(y1 - y1*2, y1 + y1*2)
        self._info = ( x0, y0)'''


class QuadTree :
    _nodes = None
    def __init__(self,dim,info=None):
        self._dim = dim
        if info != None :
            for i in info :
                self.insert(i)

    def printQTree(self,i=0):
        print("Node : " + str(i))
        if self._nodes[i].isLeaf():
            self._nodes[i].printNode()
        else:
            kids = self._nodes[i].getCoordinates()
            for j in kids:
                self.printQTree(j)

    def insert(self,info):
        #0. tree has not been formed
        if self._nodes == None :
            #1. create new QuadNode
            n = QuadNode(self._dim)
            n.setInfo(info)
            self._nodes = []
            self._nodes.append(n)
        #0. tree has been formed
        else:
            #1. find appropriate leaf node
            lindx = self.findLeaf(info)
            #2. is lindx empty ?
            if self._nodes[lindx].isEmpty() :
                self._nodes[lindx].setInfo(info)
            else:
                #3. node is not empty , set it to be internal node
                linfo = self._nodes[lindx].getInfo()
                new_kids = []
                for i in range(4):
                    self._nodes.append(QuadNode(self._dim , parent=lindx))
                    new_kids.append(len(self._nodes)-1)
                self._nodes[lindx].newIntervals(info,linfo,new_kids)
                #4. insert elements info and linfo
                self.insert(linfo)
                self.insert(info)

    def findLeaf(self,info):
        #1. start from root
        lindx = 0
        #2. if lindx is leaf, return
        while not self._nodes[lindx].isLeaf():
            lindx = self._nodes[lindx].getDirections(info)
            if not self._nodes[lindx].isEmpty():
                for i in self._nodes[lindx].getCoordinates():
                    if i==lindx or i == None :
                        pass
                    else:
                        if self._nodes[i].isEmpty():
                            return i
        return lindx
