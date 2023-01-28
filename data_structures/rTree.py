import time
import math
import pandas as pd

def getJ(e1, e2,l):
    tI = []
    for i in range(l):
        interval_1 = e1[i]
        interval_2 = e2[i]
        #1. to 2 mesa sto 1 h isa
        if interval_2[1] <= interval_1[1] and interval_2[0]>=interval_1[0]:
            tI.append( (interval_1[0], interval_1[1]) )
        #2. to 1 mesa sto 2
        elif interval_1[1] <= interval_2[1] and interval_1[0]>=interval_2[0]:
            tI.append( (interval_2[0], interval_2[1]) )
        #3. to 1 mikrotero mikrotero meros kai to 2 megalutero megalutero
        elif interval_1[0] <= interval_2[0] and interval_1[1] <= interval_2[1]:
            tI.append( (interval_1[0], interval_2[1]) )
        #4. to 2 mikrotero mikrotero meros kai to 1 megalutero megalutero
        elif interval_2[0] <= interval_1[0] and interval_2[1] <= interval_1[1]:
            tI.append( (interval_2[0], interval_1[1]) )
    #return tI
    return tI

def area(interval):
    s=0
    for i in interval:
        s+=(i[1]-i[0])**2
    return math.sqrt(s)

class Rnode :
    _entries = []# entries are type of ( [set of intervals] , cp || information )
    def __init__(self,dim,min,max,mval,parent=None,leaf=True):
        self._dim = dim
        self._min = min
        self._max = max
        self._mval = mval
        self._parent = parent
        self._leaf = leaf
    def setEntries(self,entries):
        self._entries = entries[:]
    def getEntries(self):
        return self._entries
    def clearEntries(self):
        self._entries=[]
    def clearRoot(self):
        self._leaf = False
        self._entries = []
    def setParent(self,p):
        self._parent=p
    def getParent(self):
        return self._parent
    def hasRoom(self):
        return (self._max >= len(self._entries))
    ''' Insert New Information '''
    def insertEntry(self,entry):
        self._entries.append(entry)
    def installEntry(self,info):
        I = []
        for d in range(self._dim):
            I.append( (info[d]-self._mval,info[d]+self._mval) )
        self._entries.append( (I,info) )
    ''' Gia Choose Leaf '''
    def isLeaf(self):
        return self._leaf
    def childLeastEnlargement(self,info):
        min=None
        child=None
        for i in self._entries:
            interval = i[0]#1. get interval
            tI = []#2. create canditate rectangle
            for d in range(self._dim):
                dinterval = interval[d]#3. interval at dimension d
                if info[d] < 0:#4. make the enlargement
                    tI.append( (dinterval[0]+info[d], dinterval[1]-info[d] ) )
                else:
                    tI.append( (dinterval[0]-info[d], dinterval[1]+info[d] ) )
                #compute area
                a = area(tI)
                if min == None or min < a:
                    min = a
                    child = i[1]
            #end for d in dimension range
        #end for i in self._entries
        return child
    ''' tightest rectangle '''
    def getTightRectangle(self):
        tI = []
        for i in range(self._dim):
            min = None
            max = None
            for j in self._entries:
                interval = j[0]
                current_interval = interval[i]
                if max==None or max<current_interval[1]:
                    max=current_interval[1]
                if min==None or min>current_interval[0]:
                    min=current_interval[0]
            #end for j in self._entries
            if min==max :
                tI.append((min-self._mval,max+self._mval))
            else:
                tI.append((min,max))
        return tI
        #end for i in range(self._dim)
    def setTightRectangle(self,rectangle,kid):
        t_entries = []
        for i in self._entries:
            if kid==i[1]:
                t_entries.append( (rectangle,kid) )
            else:
                t_entries.append(i)
        self._entries = t_entries
    def insertTightRectangle(self,rectangle,kid):
        self._entries.append((rectangle,kid))
    ''' split node '''
    def nodeSplit(self):
        #1. pickSeeds
        n1=None
        n2=None
        indx1,indx2 = self.pickSeeds()
        if self._parent==None:
            n1 = Rnode(self._dim,self._min,self._max,self._mval,0,self._leaf)
            n2 = Rnode(self._dim,self._min,self._max,self._mval,0,self._leaf)
        else:
            n1 = Rnode(self._dim,self._min,self._max,self._mval,self._parent,self._leaf)
            n2 = Rnode(self._dim,self._min,self._max,self._mval,self._parent,self._leaf)
        n1.clearEntries()
        n2.clearEntries()
        n1.insertEntry(self._entries[indx1])
        #2. pop elements
        self._entries.pop(indx1)
        if indx1 < indx2:
            n2.insertEntry(self._entries[indx2-1])
            self._entries.pop(indx2-1)
        else:
            n2.insertEntry(self._entries[indx2])
            self._entries.pop(index2)
        #3. invoke pick next as long as self._entries has entries
        l = len(self._entries)
        while l>0:
            next=self.pickNext(n1,n2)
            node=self.pickNode(n1,n2,next)
            if node==1:
                n1.insertEntry(self._entries[next])
            else:
                n2.insertEntry(self._entries[next])
            self._entries.pop(next)
            l=len(self._entries)
        return n1,n2
    ''' pick seeds '''
    def pickSeeds(self):
        i=0
        j=0
        d=None
        n1=0
        n2=0
        while i<len(self._entries):
            j=i+1
            while j<len(self._entries):
                e1=self._entries[i]
                e2=self._entries[j]
                td = area(getJ(e1[0],e2[0],self._dim))-area(e1[0])-area(e2[0])
                if d==None or td>d:
                    d=td
                    n1=i
                    n2=j
                j+=1
            #end while j
            i+=1
        #end while i
        return n1,n2
    ''' pick next '''
    def pickNext(self,node1,node2):
        maxdiff = None
        indx = 0
        tindx=0
        for i in self._entries:
            ''' edw ginetai h malakeia '''
            t1=Rnode(self._dim,self._min,self._max,self._mval)
            t1.setEntries(node1.getEntries())
            t2=Rnode(self._dim,self._min,self._max,self._mval)
            t2.setEntries(node2.getEntries())

            t1.insertEntry(i)
            t2.insertEntry(i)
            diff = ( area(t1.getTightRectangle())-area(t2.getTightRectangle()) )**2
            if maxdiff==None or maxdiff < diff:
                maxdiff=diff
                indx=tindx
            tindx+=1
        #end for entries
        return indx
    ''' pick node '''
    def pickNode(self,n1,n2,indx):
        tn1=Rnode(self._dim,self._min,self._max,self._mval)
        tn1.setEntries(n1.getEntries())
        tn2=Rnode(self._dim,self._min,self._max,self._mval)
        tn2.setEntries(n2.getEntries())

        tn1.insertEntry(self._entries[indx])
        tn2.insertEntry(self._entries[indx])
        if not tn1.hasRoom():
            return 2
        elif not tn2.hasRoom():
            return 1
        elif area(tn1.getTightRectangle()) > area(tn2.getTightRectangle()):
            return 2
        else:
            return 1
    def printNode(self):
        print(str(self._entries))
    def adjustPointer(self,indx):
        #1. parent
        if self._parent==None:
            pass
        elif self._parent>indx:
            self._parent-=1

        if not self._leaf:
            tentries = []
            for i in self._entries:
                if indx < i[1]:
                    tentries.append( (i[0],i[1]-1) )
                elif indx==i[1]:
                    pass
                else:
                    tentries.append(i)
            self._entries=tentries
    def getChildren(self):
        ch = []
        for i in self._entries:
            ch.append(i[1])
        return ch
    def delEntry(self,indx):
        self._entries.pop(indx)
    def toDelete(self):
        return (len(self._entries)<self._min)
    def delKid(self,kid):
        i=0
        while i <len(self._entries):
            if kid==self._entries[i][1]:
                self._entries.pop(i)
                break
            i+=1
class Rtree:
    _sresult=None
    _nodes = None
    infolen = 0
    def __init__(self,dim,min,max,mval,info=None):
        self._dim = dim
        self._min = min
        self._max = max
        self._mval = mval*1.5#+mval*max/min

        #if info not None , then insert
        if info!=None:
            j = 0
            for i in info:
                print("*"*10)
                print(str(j))
                j+=1
                self.insert(i)
            print("*"*10)
    '''Print Tree'''
    def printRTree(self,i=0):
        print("* "*10 + " Node : " + str(i) + " " + " *"*10)
        print("Parent of node "+str(i)+" : " + str(self._nodes[i].getParent()))
        if not self._nodes[i].isLeaf():
            print("Kids : " + str(self._nodes[i].getChildren()))
        print("\n")
        #self._nodes[i].printNode()
        for j in self._nodes[i].getChildren():
            if self._nodes[i].isLeaf():
                print(str(j[len(j)-1]))
                self.infolen+=1
            else:
                print("kid : "+str(j))
                self.printRTree(j)
        if i==0:
            print("There are : " + str(self.infolen)+" info and "+str(len(self._nodes))+" nodes" + " \n")
            self.infolen=0
    '''Insert New Nodes'''
    def insert(self,info):
        if self._nodes==None:#0. tree has not been formed
            self._nodes=[]#1. create nodes
            n = Rnode(self._dim,self._min,self._max,self._mval)#2. create node
            n.installEntry(info)#3. insert info
            self._nodes.append(n)#4. append nodes
        else:#0. tree has been formed
            lindx = self.chooseLeaf(info)#1.invoke choose leaf
            self._nodes[lindx].installEntry(info)#2. install new entry
            if self._nodes[lindx].hasRoom():#3. if has room
                self.adjustTree(lindx)#4. invoke adjust tree on lindx
            else:#2. if has not room
                n1,n2 = self._nodes[lindx].nodeSplit()#3. invoke split node
                #3.1 . vazw neous komvous
                self._nodes.append(n1)
                self._nodes.append(n2)
                #3.2 petaw palio komvo
                if lindx==0:
                    self._nodes[0].clearRoot()
                else:
                    self._nodes.pop(lindx)
                    self.adjustPointers(lindx)
                #3.3 prepei na ftiaksw tous pointers
                self.adjustTree(len(self._nodes)-2,len(self._nodes)-1)
                #4. root 2 split ??

    def chooseLeaf(self,info):
        lindx = 0#1. set n to be the root
        while not(self._nodes[lindx].isLeaf()):#2. is n a leaf
            lindx = self._nodes[lindx].childLeastEnlargement(info)#3. select the kid with the least enlargement
        return lindx#4. return lindx

    def adjustTree(self,indx1,indx2=None):
        if indx2==None:#0. if no splits
            if indx1==0:#1. if indx1 == 0 , i am at root, stop
                pass
            else:#1. node is not root
                p = self._nodes[indx1].getParent()#2. get parent
                self._nodes[p].setTightRectangle(self._nodes[indx1].getTightRectangle(), indx1)#3. set parent's rectangle to be tight
        else:#0. split has happened
            p = self._nodes[indx2].getParent()#2. get parent
            self._nodes[p].insertTightRectangle(self._nodes[indx1].getTightRectangle(), indx1)#3. insert tight rectangle and kid
            self._nodes[p].insertTightRectangle(self._nodes[indx2].getTightRectangle(), indx2)#3. insert tight rectangle and kid
            while not(self._nodes[p].hasRoom()):#4. if there is no room , parent has to split
                n1,n2 = self._nodes[p].nodeSplit()#4.1 split parent
                self._nodes.append(n1)#4.2 insert new nodes at self._nodes
                self._nodes.append(n2)#4.2 insert new nodes at self._nodes
                #these nodes are not leaves
                for ch in n1.getChildren():
                    self._nodes[ch].setParent(len(self._nodes)-2)
                for ch in n2.getChildren():
                    self._nodes[ch].setParent(len(self._nodes)-1)
                #4.2 set parent at child
                if p == 0:
                    #if parent is root, then clear root and insert new entries
                    self._nodes[0].clearRoot()
                    self._nodes[0].insertTightRectangle(self._nodes[len(self._nodes)-2].getTightRectangle(), len(self._nodes)-2)#4.3 insert tight rectangle and kid
                    self._nodes[0].insertTightRectangle(self._nodes[len(self._nodes)-1].getTightRectangle(), len(self._nodes)-1)#4.3 insert tight rectangle and kid
                else:
                    self._nodes.pop(p)#4.3 pop parent, if not root
                    #4.4 adjust pointers
                    self.adjustPointers(p)
                    p = self._nodes[len(self._nodes)-1].getParent()#4.5
                    self._nodes[p].insertTightRectangle(self._nodes[len(self._nodes)-2].getTightRectangle(), len(self._nodes)-2)#4.5 insert tight rectangle and kid
                    self._nodes[p].insertTightRectangle(self._nodes[len(self._nodes)-1].getTightRectangle(), len(self._nodes)-1)#4.5 insert tight rectangle and kid

    def adjustPointers(self,indx):
        for i in self._nodes:
            i.adjustPointer(indx)

    def rTreeSearch(self,vector,indx=0):
        if indx==0:
            self._sresult=[]

        res = []#temp storage
        for entry in self._nodes[indx].getEntries():
            #apo to entry 8elw mono to interval
            intervals = entry[0]
            d=0
            while d < self._dim:
                interval = intervals[d]
                if vector[d] <= interval[1] and vector[d]>=interval[0]:
                    d+=1
                else:
                    break#if it doesn't overlap , then continue with next entry
                if d==self._dim:
                    if not self._nodes[indx].isLeaf():
                        self._sresult+=self.rTreeSearch(vector,entry[1])
                    else:
                        res.append((entry[1],indx))
            #endwhile
        #endfor
        if indx==0:
            t = self._sresult
            self._sresult=None#reset to none
            return t
        else:
            return res

    def denseTree(self,lindx,eindx):
        Q=[]#set of eliminated nodes
        while 1:
            lnode = self._nodes[lindx]
            lnode.delEntry(eindx)#1. delete entry from node
            p=lnode.getParent()#2. get parent node
            if lnode.toDelete():#3. node has fewer than self._min
                Q=Q+lnode.getEntries()#4. append lnode's entries to Q
                self._nodes[p].delKid(lindx)#5. delete entry from parent
            else:
                self._nodes[p].setTightRectangle(self._nodes[lindx].getTightRectangle(),lindx)#4. no elimination, then just set set Tight Rectangle
                return Q

    ''' delete a node '''
    def deleteNode(self,indx,vname):
        #1. find lnode
        lnode = self._nodes[indx]
        #2. find entry
        v1 = pd.DataFrame(data=vname[:self._dim])
        eindx = 0
        for i in self._nodes[indx].getEntries():
            v2 = pd.DataFrame(data=i[1][:self._dim])
            tm=(v1-v2)
            if tm.mean().iloc[0]==0:
                for i in self.denseTree(indx,eindx):
                    self.insert(i)
            eindx+=1
