class TreeNode:
    def __init__(self, value):
        self.previous = None
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None
        self.depth = 0
        self.tree_arr = []
    
    def build_empty_tree(self, depth, previous=None):
        if depth == 0:
            return
        node = TreeNode(0)
        if previous:
            node.previous = previous
        else:
            self.depth = depth
            self.root = node
        node.left = self.build_empty_tree(depth - 1, node)  # type: ignore
        node.right = self.build_empty_tree(depth - 1, node) # type: ignore
        return node
    
    def save_tree_as_array(self, node):
        self.tree_arr = [[] for i in range(self.depth)]
        self.__traverse_tree(node)
        return self.tree_arr

    def __traverse_tree(self, node):
        self.tree_arr[self.depth - self.depth * 2].append(node)
        self.depth -= 1
        if node.left:
            self.__traverse_tree(node.left)
        if node.right:
            self.__traverse_tree(node.right)
        self.depth += 1
        # this should be looking at nodes not the values at the nodes (NOTE COPIED IN "bracket.py")
    
# move functions outside of class