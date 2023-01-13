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

def area(I):
    sum = 0
    for i in I:
        sum += (i[1] - i[0])**2
    return math.sqrt(sum)

def computeValidArea(area, info):                                               #DONE
    dim = len(info)-1
    sum = 0
    for i in range(0,dim) :
        interval = area[i]
        if info[i] < interval[0] :
            #an einai mikrotero
            sum += (interval[0] - info[i] )**2
        elif info[i] > interval[1]:
            #an einai megalutero
            sum += (info[i] - interval[1])**2
        else:
            #an einai anamesa den uparxei suneisfora
            pass
    return math.sqrt(sum)

class Rnode :

    _entries = []
    _dim = 0
    _min = 0
    _max = 0
    _parent = None
    _leaf = True

    def __init__(self,dim,min,max,parent = None, leaf = True):
        self._dim = dim
        self._min = min
        self._max = max
        self._parent = parent
        self._leaf = leaf

    def getNodes(self):
        for i in self._entries:
            print(str(i))
    def clearRoot(self):
        self._entries = []
    def hasParentRoom(self):
        return ( self._max-1 > len(self._entries) )
    def hasRoom(self):
        return ( self._max >= len(self._entries) )
    def getParent(self):
        return self._parent
    def isLeaf(self):
        return self._leaf
    def setNotLeaf(self):
        self._leaf=False
    def appendEntry(self,entry):
        self._entries.append(entry)

    '''2 get the new rectangle'''
    def getTightRectangle(self):                                                #DONE
        tI = []
        for i in range(0,self._dim):
            min = None
            max = None
            #compute tight interval
            for j in self._entries :
                '''provlhma einai pws exei info ke oxi tuple'''
                intrv = j[0]
                intrv = intrv[i]
                #compute min
                if min == None or intrv[0]<=min:
                    min = intrv[0]
                #compute max
                if max == None or intrv[1] >= max:
                    max = intrv[1]
            tI.append( (min , max) )
        #return tight Rectangle
        return tI
    '''    New kid entry      '''
    def adjustIntervals(self,kid,rect):                                         #DONE
        tI = None
        indx = 0
        #0. choose kid's entry
        for i in self._entries:
            if i[1] == kid:
                tI = i[0]
                break
            else:
                indx+=1
        #1. update entry
        self._entries[indx] = (rect , kid)

    '''    set kid interval    '''
    def newKid(self,kid):
        self._entries.append(kid)
        print(str(kid))

    def installEntry(self, info) :
        #0. create intervals
        I = []
        for i in range(0,self._dim):
            I.append( (info[i] - self._min , info[i] + self._min  ) )
        '''                 intervals  ,  data                 '''
        self._entries.append( (I , info) )

    ''' Get smallest rectangle '''
    def smallestRectangle(self, info):                                          #DONE
        min = None
        min_child = None
        indx = 0
        #0. for each entry
        for e in self._entries :
            tmin = computeValidArea(e[0], info)#l2 norm of starting point ,  ending point
            if min==None or tmin < min:
                min = tmin
                min_child = e[1]
            else:
                pass
            indx+=1
        #1. return pointer of child
        return min_child

    ''' Pick Seeds , a.k.a. choose 2 nodes that consist the largest area '''
    def pickSeeds(self):                                                        #DONE
        d = 0
        e1 = 0
        e2 = 1
        for i in range(0,len(self._entries)):
            for j in range(1,len(self._entries)):
                #if i == j pass
                if i==j or i<j:
                    pass
                else:
                    #compute d = area(J) - area(E1.I) - area(E2.I)
                    #0. construct J
                    i1 = self._entries[i]
                    i2 = self._entries[j]
                    J = getJ(i1[0] , i2[0])
                    #1. compute td
                    td = area(J) - area(i1[0]) - area(i2[0])
                    if d < td:
                        #2. get max d
                        d = td
                        e1 = i
                        e2 = j
        #d has been computed, return indexes
        return (e1, e2)

    ''' Node splitting '''
    def nodeSplit(self):                                                        #DONE
        #0. pick seeds
        e = self.pickSeeds()
        e1 = self._entries[e[0]]
        e2 = self._entries[e[1]]
        #pop the elements, no doubles
        self._entries.pop(e[0])
        self._entries.pop(e[1]-1)
        #1. form intervals
        I1 = []
        I2 = []
        for i in e1[0]:
            I1.append( (i[0]-self._min, i[1]+self._min) )
        for i in e2[0]:
            I2.append( (i[0]-self._min, i[1]+self._min) )

        e1 = [e1[1], ]
        e2 = [e2[1] , ]
        l = len(self._entries)#metavlhth

        #1. choose sides
        while l>0:
            #   se poio tairiazei kalutera ?
            #2. pickNext
            t = self._entries.pop(0)
            min = area(getJ(I1, t[0]))
            tmin = area(getJ(I2, t[0]))
            '''
                to provlhma einai otan spaw parent
                8a prepei na mpoun (I , cp)
                to install entry den mporei na ginei gia cp
            '''

            if self._leaf :
                if (tmin <= min and len(e1)<=self._max) or len(e2)==self._max:
                    e1.append(t[1])
                else:
                    e2.append(t[1])
            else:
                if (tmin <= min and len(e1)<=self._max) or len(e2)==self._max:
                    e1.append(t[0])
                else:
                    e2.append(t[0])

            l = len(self._entries)
        return (I1 , e1, I2 , e2)

    '''    Adjust Pointers    '''
    def adjustPointers(self, indx):
        if not(self._parent==None) and indx <= self._parent :
            self._parent -=1
        if not self._leaf :
            te = []
            for i in self._entries :
                if i[1] >= indx :
                    e = (i[0] , i[1] - 1)
                else:
                    e = (i[0] , i[1])
                te.append(e)
            self._entries = te

    def printNode(self):
        for i in self._entries:
            print(str(i[0]))
    def getChildren(self):
        return self._entries

#the Rtree
class Rtree :

    _nodes = []
    _dim = 0
    _min = 2
    _max = 4


    def __init__(self,dim=1,info = None,min = 2, max = 4):                      #DONE
        self._dim = dim
        self._min = min
        self._max = max
        if not (info==None):#if info insert
            it=0
            for i in info :
                st = time.time()
                self.insert(i)
                et = time.time()
                elapsed_time = et - st
                print("*"*5 +" "*2 + "Item : " + str(it) +" " * 2 + "*"*5+"\n" * 2)
                print('Execution time:', elapsed_time, 'seconds')
                print("*"*5 +" "*2 + "      " + " " * 2 + "*"*5+"\n" * 2)
                it+=1

    def printRTree(self,i=0):
        print("* "*10 + " Node : " + str(i) + " " + " *"*10)
        #self._nodes[i].printNode()
        print("\n"*3)
        print(len(self._nodes[i].getChildren()))
        for j in self._nodes[i].getChildren():
            if not(isinstance(j,int)):
                print(str(j))
            else:
                self.printRTree(j)

    def insert(self,info):

        #0. Check if tree has root
        if len(self._nodes) == 0:                                               #DONE
            #1. if not add first element
            a = Rnode(self._dim,self._min,self._max)
            a.installEntry(info)
            self._nodes.append(a)
        else:
            #1. Find Leaf
            indx = self.chooseLeaf(info)
            lnode = self._nodes[indx]
            #3. install E
            self._nodes[indx].installEntry(info)
            #2. If has room
            if lnode.hasRoom():                                                 #DONE
                #4. adjust tree
                self.adjustTree(indx)
            else:
                #3. split Node
                k = True
                p = lnode.getParent()#old parent is new parent
                while k or not(self._nodes[p].hasRoom()) :
                    if p==None and not k:
                        break
                    new_entries = lnode.nodeSplit()'''den allazei kapou to lnode'''
                    if indx == 0 :
                        self._nodes[0].clearRoot()
                    else:
                        self._nodes.pop(indx)#prepei oloi oi komvoi na meiwsoun kata 1 to num tous

                    for i in self._nodes:
                        i.adjustPointers(indx)
                    #4. create 2 new nodes
                    if p == None :                                              #if is root
                        p=0
                    else:
                        if p>=indx:
                            p=p-1
                    #ke kapws etsi to 1o spasimo 8a exei leaf, ta alla profanws oxi
                    n1 = Rnode(self._dim,self._min,self._max,parent = p, leaf = k)
                    n2 = Rnode(self._dim,self._min,self._max,parent = p, leaf = k)
                    self._nodes[p].setNotLeaf()
                    #5. install entries
                    #if not k -- > den einai leaf
                    print(str(new_entries[1]))
                    print(str(new_entries[3]))
                    print(str(k))
                    input('a')
                    if not k :
                        for i in new_entries[1]:
                            n1.appendEntry(i)
                        for i in new_entries[3]:
                            n2.appendEntry(i)
                    else:
                        for i in new_entries[1]:
                            n1.installEntry(i)
                        for i in new_entries[3]:
                            n2.installEntry(i)
                    k = False#vasikh metavlhth gia elegxo
                    #6. insert into nodes
                    self._nodes.append(n1)
                    self._nodes.append(n2)

                    self._nodes[p].newKid( (new_entries[0], len(self._nodes)-1) )
                    self.adjustTree(len(self._nodes)-1)
                    self._nodes[p].newKid( (new_entries[2], len(self._nodes)-1) )
                    self.adjustTree(len(self._nodes)-1)

    def adjustTree(self, indx):
        #2. if root stop
        if indx == 0:
            return 0
        else:
            #3. vres patera
            p = self._nodes[indx].getParent()
            #3. adjust rectangles
            self._nodes[p].adjustIntervals(indx, self._nodes[indx].getTightRectangle() )

    '''    returns index       '''
    def chooseLeaf(self, info):                                                 #DONE
        indx = 0
        #1. choose root
        node = self._nodes[indx]
        #2. is leaf?
        while not node.isLeaf():
            print("den kollhse")
            indx = node.smallestRectangle(info)
            node = self._nodes[indx]
        #3. return index to leaf
        return indx
