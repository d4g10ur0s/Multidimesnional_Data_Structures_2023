import pandas as pd


class KDTree:
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
        return Node(median, left_subtree, right_subtree,points[mid][-2],points[mid][-1])

    def delete(self, root, point):
        if not root:
            return None

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
        self.root.kd_search(name)


class Node:
    def __init__(self, point, left=None, right=None,name='',awards=0):
        self.point = point
        self.left = left
        self.right = right
        self.name = name
        self.awards = awards

    def kd_search(self,name,dim=0):
        if dim+1==self.dim:
            dim = 0
        else:
            dim = dim+1
        arr = []
        if self.left == None and self.right == None:
            return self.point
        if self.point[dim] < name[dim]:
            a=self.left.kd_search(name,dim)
            arr.append(a)
        else:
            a=self.right.kd_search(name,dim)
            arr.append(a)
        return arr

def printNode(node, string=""):
    if node is not None:
        print(string + "|Name:" + str(node.name) + "|Awards:" + str(node.awards))
        printNode(node.left, "\t" + string + "-left-")
        printNode(node.right, "\t" + string + "-right-")
