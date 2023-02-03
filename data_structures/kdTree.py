import pandas as pd


# class Node:
#     def __init__(self, point,left,right,split_axis,height=0):
#         self.point = point
#         self.left = left
#         self.right = right
#         self.split_axis = split_axis
#         self.height = height
#         self.name = point[len(point)-1]
#         self.award = point[len(point)-2]


# class RangeTree:

#     _height = 0

#     def __init__(self,info):
#         self.root=self.build(info)

#     def build(self, points, dim=0):
#         if len(points) == 0 :
#             return
#         if dim == len(points[0])-1:
#             dim = 0
#         if len(points) == 1:
#             return Node(points[0],None,None,dim)
#         points=self.sort_dimension(points,dim)
#         mid = len(points) // 2
#         median = points[mid]
#         left_points = points[:mid]
#         right_points = points[mid+1:]
#         left_subtree = self.build(left_points,dim=dim+1)
#         right_subtree = self.build(right_points,dim=dim+1)
#         self._height+=1
#         return self.insert(median, left_subtree, right_subtree,dim)

#     def insert(self, point, left, right, dim):
#         # print('Point',point)
#         node = Node(point, left, right, dim,self._height)
#         node.height = 1 + max(self.height(left), self.height(right))
#         balance = self.balance(left) - self.balance(right)
#         if balance > 1 and point[0] < left.point[0]:
#             return self.right_rotate(node)
#         if balance < -1 and point[0] > right.point[0]:
#             return self.left_rotate(node)
#         if balance > 1 and point[0] > left.point[0]:
#             node.left = self.left_rotate(left)
#             return self.right_rotate(node)
#         if balance < -1 and point[0] < right.point[0]:
#             node.right = self.right_rotate(right)
#             return self.left_rotate(node)
#         return node

#     def height(self, node):
#         if not node:
#             return 0
#         return node.height

#     def right_rotate(self, z):
#         y = z.left
#         t = y.right
#         y.right = z
#         z.left = t
#         z.height = 1 + max(self.height(z.left), self.height(z.right))
#         y.height = 1 + max(self.height(y.left), self.height(y.right))
#         return y

#     def left_rotate(self, z):
#         y = z.right
#         t = y.left
#         y.left = z
#         z.right = t
#         z.height = 1 + max(self._height(z.left), self._height(z.right))
#         y.height = 1 + max(self._height(y.left), self._height(y.right))
#         return y

#     def balance(self, node):
#         if not node:
#             return 0
#         return self.height(node.left) - self.height(node.right)
    
#     def sort_dimension(self,points,dim):
#         arr = []
#         i=0
#         max = 0
#         c = 0
#         while len(points)>0:
#             if i == len(points):
#                 arr.append(points.pop(c))
#                 max=0
#                 i=0
#                 c=0
#                 if len(points) == 1:
#                     break
#             point = points[i] 
#             if max < point[dim]:
#                 c=i
#                 max=point[dim]
#             i+=1
#         return arr


    # def delete(self, node, point):
    #     if not node:
    #         return None
    #     if point < node.point[:-2]:
    #         print('Point',point)
    #         print('NodePoint',node.point[:-2])
    #         node.left = self.delete(node.left, point)
    #     elif point > node.point[:-2]:
    #         node.right = self.delete(node.right, point)
    #     else:
    #         if not node.left:
    #             return node.right
    #         elif not node.right:
    #             return node.left

    #         min_val = self.find_min(node.right)
    #         node.point = min_val.point
    #         node.right = self.delete(node.right, min_val.point)

    #     node.height = 1 + max(self.height(node.left), self.height(node.right))
    #     balance = self.balance(node)

    #     if balance > 1 and self.balance(node.left) >= 0:
    #         return self.right_rotate(node)
    #     if balance < -1 and self.balance(node.right) <= 0:
    #         return self.left_rotate(node)
    #     if balance > 1 and self.balance(node.left) < 0:
    #         node.left = self.left_rotate(node.left)
    #         return self.right_rotate(node)
    #     if balance < -1 and self.balance(node.right) > 0:
    #         node.right = self.right_rotate(node.right)
    #         return self.left_rotate(node)

    #     return node

    # def find_min(self, node):
    #     while node.left:
    #         node = node.left
    #     return node

   
    # def delete(self, node, point):
    #     if not node:
    #         return None
    #     print('Point',point)
    #     print('Node_Point',node.point)
    #     if point < node.point[:-2]:
    #         print("<",point)
    #         print("<",node.point)
    #         node.left = self.delete(node.left, point)
    #     elif point > node.point[:-2]:
    #         print(">",point)
    #         print(">",node.point)
    #         node.right = self.delete(node.right, point)
    #     else:
    #         if not node.left:
    #             return node.right
    #         elif not node.right:
    #             return node.left

    #         min_val = self.find_min(node.right)
    #         node.point = min_val.point
    #         node.right = self.delete(node.right, min_val.point[:-2])

    #     node.height = 1 + max(self.height(node.left), self.height(node.right))
    #     balance = self.balance(node)

    #     if balance > 1 and self.balance(node.left) >= 0:
    #         return self.right_rotate(node)
    #     if balance < -1 and self.balance(node.right) <= 0:
    #         return self.left_rotate(node)
    #     if balance > 1 and self.balance(node.left) < 0:
    #         node.left = self.left_rotate(node.left)
    #         return self.right_rotate(node)
    #     if balance < -1 and self.balance(node.right) > 0:
    #         node.right = self.right_rotate(node.right)
    #         return self.left_rotate(node)

    #     return node



class RangeTree:
    def __init__(self, points):
        self.root = self.build(points)
        
        
    def build(self, points, dim=0):
        if not points:
            return None
        
        # Sort the points by the current dimension
        points.sort(key=lambda point: point[dim])
        
        # Get the median point
        mid = len(points) // 2
        median = points[mid][:-1]
        
        # Recursively build the left and right subtrees
        left_subtree = self.build(points[:mid], (dim + 1) % len(points[0]))
        right_subtree = self.build(points[mid + 1:], (dim + 1) % len(points[0]))
        
        # Return the current node
        return Node(median, left_subtree, right_subtree,points[mid][-1])

    def delete(self, root, point):
        if not root:
            return None
        print('point',point)
        if point[0] < root.point[0]:
            root.left = self.delete(root.left, point)
        elif point[0] > root.point[0]:
            root.right = self.delete(root.right, point)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            else:
                inorder_successor = self.find_min(root.right)
                root.point = inorder_successor.point
                root.right = self.delete(root.right, inorder_successor.point)
        return root

    def find_min(self, root):
        while root.left:
            root = root.left
        return root

    def searching(self,name):
        self.root.range_search(name)


class Node:
    def __init__(self, point, left=None, right=None,name=''):
        self.point = point
        self.left = left
        self.right = right
        self.name = name
    
    def range_search(self,name,dim=0):
        if dim+1==self.dim:
            dim = 0
        else:
            dim = dim+1
        arr = []
        if self.left == None and self.right == None:
            return self.point
        if self.point[dim] < name[dim]:
            a=self.left.range_search(name,dim)
            arr.append(a)  
        else:
            a=self.right.range_search(name,dim)
            arr.append(a)
        return arr
        
def printNode(node, string=""):
    if node is not None:
        print(string + "|Name:" + str(node.name))
        printNode(node.left, "\t" + string + "-left-")
        printNode(node.right, "\t" + string + "-right-")

