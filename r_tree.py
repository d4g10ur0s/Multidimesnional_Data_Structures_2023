import math

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
    for i in range(0,len(I)):
        sum += (i[1] - i[0])**2
    return math.sqrt(sum)

def computeValidArea(area, info):
    dim = len(info)
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

    def installEntry(self, info) :
        #0. create intervals
        I = []
        for i in range(0,self._dim):
            I.append( (info[i] - self._min , info[i] + self._min  ) )
        '''                 intervals  ,  data                 '''
        self._entries.append( (I , info) )

    def hasRoom(self):
        return ( self._max > len(self._entries) )
    def getParent(self):
        return self._parent
    '''2 get the new rectangle'''
    def getTightRectangle(self):
        tI = []
        for i in range(0,self._dim):
            min = None
            max = None
            #compute tight interval
            for j in self._entries :
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

    def adjustIntervals(self,kid,rect):
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
    ''' Get smallest rectangle '''
    def smallestRectangle(self, info):
        min = None
        min_child = None
        indx = 0
        #0. for each entry
        for e in self._entries :
            tmin = computeValidArea(e[0], info)
            if min==None or tmin < min:
                min = tmin
                min_child = e[1]
            else:
                pass
            indx+=1
        #1. return pointer of child
        return min_child
    ''' Pick Seeds , a.k.a. choose 2 nodes that consist the largest area '''
    def pickSeeds(self):
        d = 0
        e1 = 0
        e2 = 0
        for i in range(0,len(self._entries))
            for j in range(0,len(self._entries))
                #if i == j pass
                if i==j or i<j:
                    pass
                else:
                    #compute d = area(J) - area(E1.I) - area(E2.I)
                    #0. construct J
                    J = getJ(self._entries[i] , self._entries[j])
                    #1. compute td
                    td = area(J) - area(self._entries[i]) - area(self._entries[j])
                    if d < td:
                        #2. get max d
                        d = td
                        e1 = i
                        e2 = j
        #d has been computed, return indexes
        return (e1, e2)

    ''' Node splitting '''
    def nodeSplit(self,info):
        #0. pick seeds
        e = self.pickSeeds()

        #1. form intervals
        I1 = []
        I2 = []
        for i,j in e[0],e[1]:
            I1.append( (i-self._min, i+self._min) )
            I2.append( (j-self._min, j+self._min) )

        e1 = []
        e2 = []

        l = len(self._entries)#metavlhth
        #0. insert new element
        min = computeValidArea(I1, info)
        tmin = computeValidArea(I2, info)
        if tmin < min:
            choose = 2

        if choose == 1:
            e1.append(info)
        else:
            e2.append(info)
        #1. choose sides
        while l>0:
            choose = 1
            #   se poio tairiazei kalutera ?
            #2. pickNext
            min = computeValidArea(I1, self._entries[0])
            tmin = computeValidArea(I2, self._entries[0])
            if tmin < min:
                choose = 2
            #chose side
            if choose == 1:
                e1.append(self._entries.pop(0))
            else:
                e2.append(self._entries.pop(0))

            l = len(self._entries)
        return (I1 , e1, I2 , e2)

#the Rtree
class Rtree :

    _nodes = []
    _dim = 0
    _min = 2
    _max = 4

    def __init__(self,dim=1,min = 2, max = 4):
        self._dim = dim
        self._min = min
        self._max = max

    def insert(self,info):

        #0. Check if tree has root
        if len(self._nodes) == 0 :
            #1. if not add first element
            a = Rnode(self._dim,self._min,self._max)
            a.installEntry(info)
            self._nodes.append(a)
        else:
            #1. Find Leaf
            indx = self.chooseLeaf(info)
            lnode = self._nodes[indx]
            #2. If has room
            if lnode.hasRoom():
                #3. install E
                self._nodes[indx].installEntry(info)
                #4. adjust tree
                self.adjustTree(indx)
            else:
                #3. split Node
                new_entries = lnode.nodeSplit()
                p = lnode.getParent()#old parent is new parent
                self._nodes.pop(indx)
                #4. create 2 new nodes
                n1 = Rnode(self._dim,self._min,self._max,parent = p, leaf = True)
                n2 = Rnode(self._dim,self._min,self._max,parent = p, leaf = True)
                #5. install entries
                for i , j in new_entries[1], new_entries[3]:
                    n1.installEntry(i)
                    n2.installEntry(j)
                #6. insert into nodes
                self._nodes.append(n1)
                self._nodes.append(n2)

                #loop for parents till root


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
    def chooseLeaf(self, info):#DONE
        indx = 0
        #1. choose root
        node = self._nodes[indx]
        #2. is leaf?
        while not node.isLeaf():
            indx = node.smallestRectangle()
            node = self._nodes[indx]
        #3. return index to leaf
        return indx
