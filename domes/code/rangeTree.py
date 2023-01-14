import pandas as pd


class Node:
    def __init__(self, point,left,right,split_axis,height=0):
        self.point = point
        self.left = left
        self.right = right
        self.split_axis = split_axis
        self.height = height
        self.name = point[len(point)-1]
        self.award = point[len(point)-2]


class RangeTree:

    _height = 0

    def __init__(self,info):
        self.root=self.build(info)

    def build(self, points, dim=0):
        if len(points) == 0 :
            return
        if dim == len(points[0])-1:
            dim = 0
        if len(points) == 1:
            return Node(points[0],None,None,dim)
        points=self.sort_dimension(points,dim)
        mid = len(points) // 2
        median = points[mid]
        left_points = points[:mid]
        right_points = points[mid+1:]
        left_subtree = self.build(left_points,dim=dim+1)
        right_subtree = self.build(right_points,dim=dim+1)
        self._height+=1
        return self.insert(median, left_subtree, right_subtree,dim)

    def insert(self, point, left, right, dim):
        node = Node(point, left, right, dim,self._height)
        node.height = 1 + max(self.height(left), self.height(right))
        balance = self.balance(left) - self.balance(right)
        if balance > 1 and point[0] < left.point[0]:
            return self.right_rotate(node)
        if balance < -1 and point[0] > right.point[0]:
            return self.left_rotate(node)
        if balance > 1 and point[0] > left.point[0]:
            node.left = self.left_rotate(left)
            return self.right_rotate(node)
        if balance < -1 and point[0] < right.point[0]:
            node.right = self.right_rotate(right)
            return self.left_rotate(node)
        return node

    def height(self, node):
        if not node:
            return 0
        return node.height

    def right_rotate(self, z):
        y = z.left
        t = y.right
        y.right = z
        z.left = t
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def left_rotate(self, z):
        y = z.right
        t = y.left
        y.left = z
        z.right = t
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)
    
    def sort_dimension(self,points,dim):
        arr = []
        i=0
        max = 0
        c = 0
        while len(points)>0:
            if i == len(points):
                arr.append(points.pop(c))
                max=0
                i=0
                if len(points) == 1:
                    break
            point = points[i] 
            if max < point[dim]:
                c=i
                max=point[dim]
            i+=1
        return arr


            
def printNode(node, string=""):
    if node is not None:
        # printNode(node.left)
        # print(node.point)
        # printNode(node.right)
        print(string + "|Name:" + str(node.name))
        printNode(node.left, "\t" + string + "-left-")
        printNode(node.right, "\t" + string + "-right-")

# String to Float
def string2float(arr):
    t= []
    for i in range(0,len(arr)-1):
        t.append(float(arr[i]))
    t.append(arr[len(arr)-1])
    return t

def main():
    filename = 'data.csv'
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = pd.read_csv(csv_file, sep=';')
        arr = []
        for i in csv_reader.values.tolist():
            arr.append(string2float(i[0].split(',')))
        a = RangeTree(arr)
        printNode(a.root)

if __name__ == "__main__" :
    main()