import math
import time


def getJ(e1, e2):
    tI = []
    for i in range(0, len(e1)):
        interval_1 = e1[i]
        interval_2 = e2[i]
        #1. to 2 mesa sto 1 h isa
        if interval_2[1] <= interval_1[1] and interval_2[0]>=interval_1[0]:
            tI.append( (interval_1[0], interval_1[1]) )
        #2. to 1 mesa sto 2
        elif interval_1[1] <= interval_2[1] and interval_1[0]>=interval_2[0]:
            tI.append( (interval_2[0], interval_2[1]) )
        #3. to 1 mikrotero mikrotero meros
        elif interval_1[0] <= interval_2[0] and interval_1[1] <= interval_2[1]:
            tI.append( (interval_1[0], interval_2[1]) )
        #4. to 2 mikrotero mikrotero meros
        elif interval_2[0] <= interval_1[0] and interval_2[1] <= interval_1[1]:
            tI.append( (interval_2[0], interval_1[1]) )
        #5. to 1 megalutero megalutero meros
        elif interval_1[1] >= interval_2[1] and interval_1[0]>= interval_2[0]:
            tI.append( (interval_2[0], interval_1[1]) )
        #6. to 2 megalutero megalutero meros
        else:
            tI.append( (interval_1[0], interval_2[1]) )
    #return tI
    return tI

''' a.k.a. l2norm '''
def area(I):
    sum = 0
    for i in I:
        sum += (i[1] - i[0])**2
    return math.sqrt(sum)

class Rnode :

    _entries = []

    def __init__(self,dim,min,max,parent = None, leaf = True):
        self._dim = dim
        self._min = min
        self._max = max
        self._parent = parent
        self._leaf = leaf
    def setEntries(self,entries):
        self._entries=entries
    def clearRoot(self):
        self._leaf = False
        self._entries = []
    ''' NOT ROOT '''
    def getParent(self):
        return self._parent
    def hasRoom(self):
        return (len(self._entries) <= self._max)
    def isLeaf(self):
        return self._leaf
    ''' install new entry , info must be list           LEAF                    '''
    def installEntry(self, info) :
        #0. create intervals
        I = []
        for i in range(0,self._dim):
            I.append( (info[i] - self._min , info[i] + self._min  ) )
        '''                 intervals  ,  data                                  '''
        self._entries.append( (I , info) )
    '''     set new tight rectangle             NOT LEAF                        '''
    def setTightRectangle(self,kid,rectangle):
        for i in range(0,len(self._entries)):
            #find kid and set it
            if self._entries[i][1] == kid:
                self._entries[i] = (rectangle,kid)
                break
    '''     new tight rectangle                 LEAF                            '''
    def getTightRectangle(self):
        tI = []
        for i in range(0,self._dim):
            min = None
            max = None
            #compute tight interval
            for j in self._entries :
                #get all intervals a.k.a. I
                intrv = j[0]
                #i is current dimension
                intrv = intrv[i]
                #compute min
                if min == None or intrv[0]<min:
                    min = intrv[0]
                #compute max
                if max == None or intrv[1] > max:
                    max = intrv[1]
            #set tight interval for dimension i
            tI.append( (min , max) )
        #return tight Rectangle
        return tI
    ''' get the child that needs the least enlargement            NOT LEAF      '''
    def getLeastEnlargement(self,info):
        min_child = None
        min = None
        for i in self._entries:
            if min==None:
                min_child = i[1]
                min = area(i[0])
            elif min>area(i[0]):
                min_child = i[1]
        return min_child

    ''' Pick Seeds , a.k.a. choose 2 nodes that consist the largest area '''
    def pickSeeds(self):                                                        #DONE
        d = None
        e1 = 0
        e2 = 1
        for i in range(0,len(self._entries)):
            for j in range(i+1,len(self._entries)):
                #compute d = area(J) - area(E1.I) - area(E2.I)
                #0. construct J
                i1 = self._entries[i]
                i2 = self._entries[j]
                J = getJ(i1[0] , i2[0])
                #1. compute td
                td = area(J) - area(i1[0]) - area(i2[0])
                if d==None or d < td:
                    #2. get max d
                    d = td
                    e1 = i
                    e2 = j
        #d has been computed, return indexes
        return (e1, e2)
    '''      pick next for assignment                                   ANY     '''
    def pickNext(self,c1,c2):
        indx = 0
        tindx = 0
        diff = None
        tc1 = None
        tc2 = None
        for i in self._entries:
            ttc1 = getJ(c1,i[0])
            ttc2 = getJ(c2,i[0])
            if diff == None or diff < ( area(ttc1) - area(ttc2) )**2 :
                diff = ( area(ttc1) - area(ttc2) )**2
                tc1 = ttc1
                tc2 = ttc2
                indx = tindx
            tindx+=1
        return tc1,tc2,indx
    ''' Node splitting '''
    def nodeSplit(self):                                                        #DONE
        #0. pick seeds
        e = self.pickSeeds()
        #1. create 2 groups
        e1 = [self._entries[e[0]]]
        c1 = e1[0]#covering rectangle
        c1 = c1[0]
        e2 = [self._entries[e[1]]]
        c2 = e2[0]#covering rectangle
        c2 = c2[0]
        #pop the elements, no doubles
        self._entries.pop(e[0])
        if e[1]<e[0]:
            self._entries.pop(e[1])
        else:
            self._entries.pop(e[1]-1)
                #2. fill groups with entries

        while len(self._entries)>0:
            tc1,tc2,indx = self.pickNext(c1,c2)
            #select entry for assignment
            s=self._entries.pop(indx)
            if len(e1)==self._max:
                #append e2
                e2.append(s)
                c2 = tc2
            elif len(e2)==self._max:
                #append e1
                e1.append(s)
                c1=tc1
            else:
                #append to least enlargement
                if area(tc1)<area(tc2):
                    #append e1
                    e1.append(s)
                    c1 = tc1
                else:
                    #append e2
                    e2.append(s)
                    c2 = tc2
        #returns information for 2 nodes and their covering rectangles
        return (c1, e1,c2, e2)
    '''     adjust pointers after splitting                                     '''
    def adjustPointer(self,indx):
        if not self._leaf:
            temp = []
            for i in self._entries:
                if i[1] < indx:
                    temp.append( (i[0],i[1]) )
                elif i[1] == indx :
                    pass
                else:
                    temp.append( (i[0],i[1]-1) )
            self._entries = temp

    def updateParent(self,c1,k1,c2,k2):
        self._entries.append((c1,k1))
        self._entries.append((c2,k2))

    def printNode(self):
        for i in self._entries:
            print(str(i[0]))

    def getChildren(self):
        ch = []
        for i in self._entries:
            ch.append(i[1])
        return ch

#the Rtree
class Rtree :
    infolen = 0
    def __init__(self,dim=1,info = None,min = 2, max = 4):
        self._dim = dim
        self._min = min
        self._max = max
        self._nodes = None
        ''' info must be a list '''
        if not(info==None):
            indx = 0
            for i in info :
                indx+=1
                print("*"*5 + " " + str(indx) + " " + "*"*5)
                self.insert(i)
                #self.printRTree()

    def printRTree(self,i=0):
        print("* "*10 + " Node : " + str(i) + " " + " *"*10)
        #self._nodes[i].printNode()
        print("\n")
        for j in self._nodes[i].getChildren():
            if not(isinstance(j,int)):
                print(str(j))
                self.infolen+=1
            else:
                self.printRTree(j)
        if i ==0:
            print("There are : " + str(self.infolen) + " \n")
    def insert(self,info):
        #0. if tree has not formed
        if self._nodes==None :
            self._nodes = []
            self._nodes.append(Rnode(dim=self._dim,min=self._min,max=self._max))
            self._nodes[0].installEntry(info)
        else:
            #1. invoke choose leaf, returns index
            lindx = self.chooseLeaf(info)
            self._nodes[lindx].installEntry(info)
            #2. if has room just adjust
            if self._nodes[lindx].hasRoom():
                self.adjustTree(lindx)
            #2. if has not room , split
            else:
                p=None
                while p==None or not(self._nodes[p].hasRoom()):
                    lnode = None
                    if lindx > 0 :
                        lnode=self._nodes.pop(lindx)
                    else:
                        lnode=self._nodes[lindx]

                    p=lnode.getParent()
                    tobeleaf = lnode.isLeaf()
                    c1,e1,c2,e2 = lnode.nodeSplit()
                    if not(p==None) and p >= lindx :
                        p=p-1
                    if p==None:
                        p=0
                        #root is not leaf any more
                        self._nodes[p].clearRoot()
                    #adjust index because of pop
                    self.adjustPointers(lindx)
                    #3. create 2 new nodes
                    n1 = Rnode(dim=self._dim,min=self._min,max=self._max,parent=p,leaf=tobeleaf)
                    n1.setEntries(e1)
                    n2 = Rnode(dim=self._dim,min=self._min,max=self._max,parent=p,leaf=tobeleaf)
                    n2.setEntries(e2)
                    #update parent with covering rectangles
                    self._nodes[p].updateParent(c1,len(self._nodes),c2,len(self._nodes)+1)
                    self._nodes.append(n1)
                    self._nodes.append(n2)
                    #meta paw se parent an den exei xwro
                    lindx = p

    ''' returns index to leaf node '''
    def chooseLeaf(self,info):                                                  #DONE
        #1. set node to be root
        indx = 0
        #2. select a leaf node
        while not(self._nodes[indx].isLeaf()):
            indx = self._nodes[indx].getLeastEnlargement(info)
        #3. return index to leaf node
        return indx

    ''' adjust tree '''
    def adjustTree(self,indx1):
        #if no split
        #1. if root stop
        if indx1==0:
            pass
        else:
            #2. get parent
            p = self._nodes[indx1].getParent()
            #2. set tight rectangle
            self._nodes[p].setTightRectangle(indx1, self._nodes[indx1].getTightRectangle())

    ''' adjust pointers after splitting '''
    def adjustPointers(self,indx):
        for i in self._nodes:
            i.adjustPointer(indx)
