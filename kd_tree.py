class KDNode:
    def init(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree:
    def init(self, points):
        self.root = build_kdtree(points, 0)

    def build_kdtree(points, depth):
         if not points:
             return None

         # Select axis based on depth so that axis cycles through all valid values
         k = len(points[0]) - 1 # Assumes all points have the same dimension
         axis = depth % k

         # Sort point list and choose median as pivot element
         points.sort(key=lambda point: point[axis])
         median = len(points) // 2 # Choose median

         # Create node and construct subtrees
         return KDNode(
                points[median],
                build_kdtree(points[:median], depth + 1),
                build_kdtree(points[median + 1:], depth + 1)
            )

         
