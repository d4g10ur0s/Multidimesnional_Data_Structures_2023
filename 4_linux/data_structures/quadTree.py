import time
import math
import random as rd
import pandas as pd
import numpy as np

class QuadNode :
    def __init__(self,dim,max=4,parent=None,leaf = True):
        self._dim = dim
        self._max = max
        ''' tree controlling '''
        self._parent = parent
        self._leaf = leaf
        self._empty = True
        self._info = []
        ''' intervals for parsing '''
        #child
        self.nw = None
        self.ne = None
        self.se = None
        self.sw = None
        self.cname = None
        self.cawards = None
    def isLeaf(self):
        return self._leaf
    def getChildren(self):
        return [self.nw,self.ne,self.se,self.sw]
    ''' go to next node '''
    def getDirections(self,info,toret=True):
        arr=[]
        m = pd.DataFrame(data=info[:self._dim]).mean().loc[0]

        if m-self.cname >= 0 and info[self._dim]-self.cawards >=0 :# y >= 0 , x >= 0
            if toret:
                return self.nw
            else:
                arr.append(self.nw)
        elif m-self.cname >= 0 and info[self._dim]-self.cawards <= 0 :# y <= 0 , x >= 0
            if toret:
                return self.ne
            else:
                arr.append(self.ne)
        elif m-self.cname <= 0 and info[self._dim]-self.cawards <= 0 :# y =< 0 , x <= 0
            if toret:
                return self.se
            else:
                arr.append(self.se)
        elif m-self.cname <= 0 and info[self._dim]-self.cawards >= 0 :# y >= 0 , x =< 0
            if toret:
                return self.sw
            else:
                arr.append(self.sw)
        if toret:
            return None
        else:
            return arr

    def insertInfo(self,info):
        self._info.append(info)
    def hasRoom(self):
        return self._max>len(self._info)
    def getParent(self):
        return self._parent

    def getSplit(self,parent):
        self._leaf = False
        ''' info is an array of (x,y,information) elements '''
        #1. se center to b the mean of x and y
        tmean = []
        self.cawards = 0
        self.cname = 0
        for i in self._info:
            m = pd.DataFrame(data=i[:self._dim]).mean().loc[0]
            tmean.append(m)
            self.cname += m
            self.cawards += i[self._dim]
        # get the means
        self.cname /= len(self._info)
        self.cawards /= len(self._info)
        #2. create nodes
        #a. NW node
        nw = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        nw.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if tmean[i]-self.cname >= 0 and t[self._dim]-self.cawards >=0 :# y >= 0 , x >= 0
                nw.insertInfo(t)
                self._info.pop(i)
                tmean.pop(i)
            else:
                i+=1
        #b. NE node
        ne = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        ne.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if tmean[i]-self.cname >= 0 and t[self._dim]-self.cawards <=0 :# y <= 0 , x > 0
                ne.insertInfo(t)
                self._info.pop(i)
                tmean.pop(i)
            else :
                i+=1
        #c. SE node
        se = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        se.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if tmean[i]-self.cname <= 0 and t[self._dim]-self.cawards <= 0 :# y < 0 , x <= 0
                se.insertInfo(t)
                self._info.pop(i)
                tmean.pop(i)
            else:
                i+=1
        #d. SW node
        sw = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        sw.clearNode()
        i=0
        while i < len(self._info) :# y > 0 , x < 0
            t = self._info[i]
            sw.insertInfo(t)
            self._info.pop(i)
            tmean.pop(i)
            i+=1
        return nw,ne,se,sw
    def rmEntry(self,entry):
        i=0
        while i < len(self._info):
            if self._info[i][len(self._info[i])-2]==entry:
                self._info.pop(i)
                break
            i+=1
    def nodeSplitted(self,kids):
        self._leaf=False
        temp = self._info
        self._info=None
        self.nw=kids
        self.ne=kids+1
        self.se=kids+2
        self.sw=kids+3
        return temp
    def clearNode(self):
        self._info = []
    def isEmpty(self):
        return (self._info==None or len(self._info) == 0)
    def getCoordinates(self):
        return [self.nw,self.ne,self.se,self.sw]
    def printNode(self):
        if self._leaf:
            for i in self._info:
                print(str(i[len(i)-2:len(i)]))
        else:
            print(str(self.nw))
            print(str(self.ne))
            print(str(self.se))
            print(str(self.sw))
    def getInfo(self,indx):
        arr = []
        for i in self._info:
            arr.append(i[len(i)-2:len(i)]+indx)
        return arr
    def adjustPointer(self,indx):
        #1. parent
        if self._parent==None:
            pass
        elif self._parent>=indx:
            self._parent-=1

        if not self._leaf:
            if self.nw > indx:
                self.nw-=1
            if self.ne > indx:
                self.ne-=1
            if self.se > indx:
                self.se-=1
            if self.sw > indx:
                self.sw-=1
class QuadTree :
    _nodes = None
    def __init__(self,dim,max,info=None):
        self._dim = dim
        self._max = max
        if info != None :
            k=0
            for i in info :
                print(10*"*"+" " +str(k)+" "+"*"*10)
                self.insert(i)
                k+=1

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
            n = QuadNode(self._dim,self._max)
            n.insertInfo(info)
            self._nodes = []
            self._nodes.append(n)
        #0. tree has been formed
        else:
            #1. find appropriate leaf node
            lindx = self.findLeaf(info)#not done
            #2. has room ?
            if self._nodes[lindx].hasRoom():
                self._nodes[lindx].insertInfo(info)#3 insert info to node.
            else:
                #3. leaf node has not room , split it
                rn1,rn2,rn3,rn4 = self._nodes[lindx].getSplit(lindx)
                #insert nodes to tree
                snode_info = self._nodes[lindx].nodeSplitted(len(self._nodes))
                self._nodes+=[rn1,rn2,rn3,rn4]
                snode_info.append(info)
                #4. insert again
                for ninfo in snode_info:
                    self.insert(ninfo)

    def findLeaf(self,info):
        #1. start from root
        lindx = 0
        #2. if lindx is leaf, return
        while not self._nodes[lindx].isLeaf():
            lindx = self._nodes[lindx].getDirections(info)
        return lindx

    def findLeaves(self,info,indx=0):
        arr = []
        if self._nodes[indx].isLeaf():
            return indx
        else:
            kids = self._nodes[indx].getDirections(info,toret=False)
            if not(kids==None):
                for k in kids:
                    dinfo = self.findLeaves(info,indx=k)
                    try :
                        arr+=dinfo
                    except:
                        arr.append(dinfo)
        return arr

    def qSearch(self,info):
        indx = self.findLeaves(info)
        arr = []
        for i in indx:
            arr=arr+self._nodes[i].getInfo(indx)
        return arr

    def qDelete(self,indx,entry):
        self._nodes[indx].rmEntry(entry)
        while self._nodes[indx].isEmpty():
            for i in self._nodes[self._nodes[indx].getParent()].getChildren():
                if i==None or not (self._nodes[i].isEmpty()):
                    return False
            #prepei na svhsw nodes ke na kanw merge me parent
            for i in self._nodes[self._nodes[indx].getParent()].getChildren():
                for k in self._nodes:
                    k.adjustPointer(i)
            a,b,c,d = self._nodes[self._nodes[indx].getParent()].getChildren()
            self._nodes.pop(a)
            if a > b :
                b-=1
            if a > c:
                c-=1
            if a>d:
                d-=1
            self._nodes.pop(b)
            if b>c:
                c-=1
            if b>d:
                d-=1
            self._nodes.pop(c)
            if c>d:
                d-=1
            self._nodes.pop(d)

            #lets check parent
            indx = self._nodes[indx].getParent()
