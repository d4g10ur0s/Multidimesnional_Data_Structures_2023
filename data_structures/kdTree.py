import math


class KDTreeNode:

    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree:

    def __init__(self, data):
         self.root=self.build(info)


    def build_tree(points, depth):
            if not points:
                return None
            axis = depth % len(points[0])
            points.sort(key=lambda point: point[axis])
            median = len(points) // 2
            return KDTreeNode(points[median],
            build_tree(points[:median], depth+1),
            build_tree(points[median+1:], depth+1))

        self.root = build_tree(data, 0)

    def insert(self, point, node=None, depth=0):
        if node is None:
            node = self.root
        if node is None:
            return KDTreeNode(point)

        axis = depth % len(point)
        next_node = None
        if point[axis] < node.point[axis]:
            next_node = self.insert(point, node.left, depth + 1)
            if node.left is None:
                node.left = next_node
        else:
            next_node = self.insert(point, node.right, depth + 1)
            if node.right is None:
                node.right = next_node
        return node

    def delete(self, point, node=None, depth=0):
        if node is None:
            node = self.root
        if node is None:
            return None

        axis = depth % len(point)
        if point[axis] < node.point[axis]:
            node.left = self.delete(point, node.left, depth + 1)
        elif point[axis] > node.point[axis]:
            node.right = self.delete(point, node.right, depth + 1)
        else:
            if node.right and node.left:
                replacement = self.find_min(node.right, depth + 1)
                node.point = replacement.point
                node.right = self.delete(replacement.point, node.right, depth + 1)
            else:
                if node.left:
                    return node.left
                else:
                    return node.right
        return node

    def find_min(self, node, depth):
        if node is None:
            return None
        axis = depth % len(node.point)
        if node.left is None:
            return node
        return self.find_min(node.left, depth + 1)

    def search(self, point, node=None, depth=0):
        if node is None:
            node = self.root
        if node is None:
            return None

        axis = depth % len(point)
        if point[axis] == node.point[axis]:
            return node.point
        elif point[axis] < node.point[axis]:
            return self.search(point, node.left, depth + 1)

    def range_search(self, low, high, node=None, depth=0):
        if node is None:
            node = self.root
                if node is None:
                    return []

                axis = depth % len(low)
                in_range = []
                if low[axis] <= node.point[axis]:
                    in_range += self.range_search(low, high, node.left, depth + 1)
                if high[axis] > node.point[axis]:
                    in_range += self.range_search(low, high, node.right, depth + 1)
                if all(low[i] <= node.point[i] <= high[i] for i in range(len(low))):
                    in_range.append(node.point)
                return in_range

    def nearest_neighbor(self, point, best=None, node=None, depth=0):
                if node is None:
                    node = self.root
                if node is None:
                    return best

                axis = depth % len(point)
                next_best = None
                if best is None or self.distance(point, node.point) < self.distance(point, best):
                    next_best = node.point
                else:
                    next_best = best

                if point[axis] < node.point[axis]:
                    best = self.nearest_neighbor(point, next_best, node.left, depth + 1)
                    if best is None or abs(point[axis] - node.point[axis]) < self.distance(point, best):
                        best = self.nearest_neighbor(point, next_best, node.right, depth + 1)
                else:
                    best = self.nearest_neighbor(point, next_best, node.right, depth + 1)
                    if best is None or abs(point[axis] - node.point[axis]) < self.distance(point, best):
                        best = self.nearest_neighbor(point, next_best, node.left, depth + 1)
                return best

    def distance(self, a, b):
                return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
