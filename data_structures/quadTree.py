import time
import math
import random as rd
import pandas as pd

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
        #(intervals , child) || info
        self.nw = None
        self.ne = None
        self.se = None
        self.sw = None

    def isLeaf(self):
        return self._leaf
    ''' go to next node '''
    def getDirections(self,info,toret=True):
        if not(toret):
            print(str(self.nw))
            print(str(self.ne))
            print(str(self.se))
            print(str(self.sw))
            input('a')
        arr=[]
        tinfo = (info[0],info[1])
        if (tinfo[0] >= self.nw[0][0]) and (tinfo[1] >= self.nw[1][0] ) :
            if toret:
                return self.nw[2]
            else:
                arr.append(self.nw[2])
        elif (tinfo[0] >= self.ne[0][0] ) and (tinfo[1] <= self.ne[1][0] )  :
            if toret:
                return self.ne[2]
            else:
                arr.append(self.ne[2])
        elif (tinfo[0] <= self.se[0][0] ) and (tinfo[1] <= self.se[1][0] )  :
            if toret:
                return self.se[2]
            else:
                arr.append(self.se[2])
        elif (tinfo[0] <= self.sw[0][0] ) and (tinfo[1] >= self.sw[1][0])  :
            if toret:
                return self.sw[2]
            else:
                arr.append(self.sw[2])
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
    def get1Coord(self,coord):
        arr = []
        for i in self._info:
            arr.append(i[coord])
        return arr
    def getSplit(self,parent):
        self._leaf = False
        ''' info is an array of (x,y,information) elements '''
        #1. se center to b the mean of x and y
        x = pd.DataFrame(data=self.get1Coord(0)).mean().iloc[0]
        y = pd.DataFrame(data=self.get1Coord(1)).mean().iloc[0]
        #2. create nodes
        #a. NW node
        self.nw = [(x-x*1e-2,x*2+0.5), (y+y*1e-2,y*2+0.5)]
        nw = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        nw.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if (t[0] >= self.nw[0][0] ) and (t[1] >= self.nw[1][0]) :
                nw.insertInfo(t)
                self._info.pop(i)
            i+=1
        #b. NE node
        self.ne = [(x-x*1e-2,x*2+0.5), (y-y*1e-2,y*(-2)-0.5)]
        ne = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        ne.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if (t[0] >= self.ne[0][0] ) and (t[1] <= self.ne[1][0]) :
                ne.insertInfo(t)
                self._info.pop(i)
            i+=1
        #c. SE node
        self.se = [(x+x*1e-2,x*(-2)-0.5), (y-y*1e-2,y*(-2)-0.5)]
        se = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        se.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if (t[0] <= self.se[0][0] ) and (t[1] <= self.se[1][0]) :
                se.insertInfo(t)
                self._info.pop(i)
            i+=1
        #d. SW node
        self.sw = [(x+x*1e-2,x*(-2)-0.5), (y+y*1e-2,y*2+0.5)]
        sw = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        sw.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if (t[0] <= self.sw[0][0] ) and (t[1] >= self.sw[1][0]) :
                sw.insertInfo(t)
                self._info.pop(i)
            i+=1
        return nw,ne,se,sw
    def nodeSplitted(self,kids):
        self._leaf=False
        temp = self._info
        self._info=None
        self.nw.append(kids)
        self.ne.append(kids+1)
        self.se.append(kids+2)
        self.sw.append(kids+3)
        return temp
    def clearNode(self):
        self._info = []
    def getCoordinates(self):
        return [self.nw[2],self.ne[2],self.se[2],self.sw[2]]
    def printNode(self):
        if self._leaf:
            for i in self._info:
                print(str(i[2]))
        else:
            print(str(self.nw))
            print(str(self.ne))
            print(str(self.se))
            print(str(self.sw))
    def getInfo(self):
        arr = []
        for i in self._info:
            arr+=i[2]
        return arr

class QuadTree :
    _nodes = None
    def __init__(self,dim,max,info=None):
        self._dim = dim
        self._max = max
        if info != None :
            k=0
            for i in info :
                print(10*"*"+" " +str(k)+" "+"*"*10)
                self.insert(self.fromDim2D(i))
                k+=1
    ''' to transform from dim to 2d '''
    def fromDim2D(self,info,ins=True):
        x=0
        for i in range(self._dim-1):
            x+=info[i]
        if ins:
            return (x/(self._dim-1),info[self._dim-1],info[self._dim])
        else:
            print(str(info))
            try :
                return (x/(self._dim-1),info[self._dim-1])#epeidh den pernw ta awards
            except :
                return (x/(self._dim-1),0)#epeidh den pernw ta awards
    def printQTree(self,i=0):
        print("Node : " + str(i))
        #input(str(self._nodes[i].printNode()))
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
        input(str(info))
        arr = []
        if self._nodes[indx].isLeaf():
            return indx
        else:
            kids = self._nodes[indx].getDirections(info,toret=False)
            input(str(kids))
            if not(kids==None):
                for k in kids:
                    self._nodes[k].printNode()
                    dinfo = self.findLeaves(info,indx=k)
                    try :
                        arr+=dinfo
                    except:
                        arr.append(dinfo)
        return arr

    def qSearch(self,info):
        search_for = self.fromDim2D(info,ins=False)
        indx = self.findLeaves(search_for)
        arr = []
        for i in indx:
            arr+=self._nodes[i].getInfo()

        print(str(i))
        return arr
