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
        #child
        self.nw = None
        self.ne = None
        self.se = None
        self.sw = None
        self.c = None
    def isLeaf(self):
        return self._leaf
    ''' go to next node '''
    def getDirections(self,info,toret=True):

        arr=[]
        tinfo = pd.DataFrame(data=info[:self._dim])
        if (pd.DataFrame(data=tinfo).transpose()-self.c).mean(axis=1).iloc[0] >= 0  :
            if toret:
                return self.nw
            else:
                arr.append(self.nw)
        elif (pd.DataFrame(data=tinfo).transpose()-self.c).mean(axis=1).iloc[0] <= 0   :
            if toret:
                return self.ne
            else:
                arr.append(self.ne)
        elif (pd.DataFrame(data=tinfo).transpose()+self.c).mean(axis=1).iloc[0] <= 0   :
            if toret:
                return self.se
            else:
                arr.append(self.se)
        elif (pd.DataFrame(data=tinfo).transpose()+self.c).mean(axis=1).iloc[0] >= 0   :
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
        temp = []
        for i in self._info:
            temp.append(i[:self._dim])#den pairnw ta teleutaia
        self.c = pd.DataFrame(data=temp).transpose().mean().mean()
        #print(str(self.c))
        #2. create nodes
        #a. NW node
        nw = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        nw.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            print(str((pd.DataFrame(data=t[:self._dim]).transpose()-self.c).mean(axis=1)))
            if (pd.DataFrame(data=t[:self._dim]).transpose()-self.c).mean(axis=1).iloc[0] > 0 :
                nw.insertInfo(t)
                self._info.pop(i)
            i+=1
        #b. NE node
        ne = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        ne.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if (pd.DataFrame(data=t[:self._dim]).transpose()-self.c).mean(axis=1).iloc[0] <= 0 :
                ne.insertInfo(t)
                self._info.pop(i)
            i+=1
        #c. SE node
        se = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        se.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if (pd.DataFrame(data=t[:self._dim]).transpose()+self.c).mean(axis=1).iloc[0] < 0:
                se.insertInfo(t)
                self._info.pop(i)
            i+=1
        #d. SW node
        sw = QuadNode(self._dim,self._max,parent=parent,leaf=True)
        sw.clearNode()
        i=0
        while i < len(self._info) :
            t = self._info[i]
            if (pd.DataFrame(data=t[:self._dim]).transpose()+self.c).mean(axis=1).iloc[0] >= 0 :
                sw.insertInfo(t)
                self._info.pop(i)
            i+=1
        nw.printNode()
        ne.printNode()
        se.printNode()
        sw.printNode()
        return nw,ne,se,sw
    def rmEntry(self,entry):
        i=0
        while i < len(self._info):
            if self._info[i]==entry:
                self._info.pop(i)
                break
            i+=1
    def nodeSplitted(self,kids):
        self._leaf=False
        temp = self._info
        self._info=None
        self.nw=(kids)
        self.ne=(kids+1)
        self.se=(kids+2)
        self.sw=(kids+3)
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
    def getInfo(self):
        arr = []
        for i in self._info:
            arr.append(i[-1])
        if isinstance(arr,str):
            return [arr]
        return arr
    def adjustPointer(self,indx):
        #1. parent
        if self._parent==None:
            pass
        elif self._parent>indx:
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
    ''' to transform from dim to 2d
    def fromDim2D(self,info,ins=True):
        x=0
        for i in range(self._dim-1):
            x+=info[i]
        if ins:
            return (x/(self._dim-1),info[-2],info[-1])
        else:
            try :
                return (x/(self._dim-1),info[self._dim-1])#epeidh den pernw ta awards
            except :
                return (x/(self._dim-1),0)#epeidh den pernw ta awards
    Vghke Akuro!
    '''
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
        #input(str(info))
        arr = []
        if self._nodes[indx].isLeaf():
            return indx
        else:
            kids = self._nodes[indx].getDirections(info,toret=False)
            #input(str(kids))
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
            arr+=self._nodes[i].getInfo()
        return [arr]

    def qDelete(self,indx,entry):
        self._nodes[indx].rmEntry(entry)
        while self._nodes[indx].isEmpty():
            for i in self._nodes[self._nodes[indx].getParent()].getChildren():
                if not self._nodes[i].isEmpty():
                    return False
            #prepei na svhsw nodes ke na kanw merge me parent
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

            for i in self._nodes[self._nodes[indx].getParent()].getChildren():
                for k in self._nodes:
                    k.adjustPointer(i)
            #lets check parent
            indx = self._nodes[indx].getParent()
