# undirected binary tree
class TreeNode:
    def __init__(self, value):
        self.previous = None
        self.value = value
        self.left = None
        self.right = None

# specific tree class for this project
class Tree:
    def __init__(self):
        self.root = None
        self.depth = 0
        self.tree_arr = []
    
    # builds an tree filled with nodes that have no value, previous is not called in initial calling of function
    def build_empty_tree(self, depth, previous=None):
        # base case
        if depth == 0:
            return
        # initialize empty node
        node = TreeNode(0)
        # this will never be called on the first pass, ensuring that root has no previous node 
        if previous:
            node.previous = previous
        # this will only be called on the first
        else:
            # saves the current node as the root
            self.depth = depth
            # sets tree's depth to the user requested depth
            self.root = node
        # sets node.left and node.right to empty node if depth > 0
        node.left = self.build_empty_tree(depth - 1, node)  # type: ignore
        node.right = self.build_empty_tree(depth - 1, node) # type: ignore
        return node
    
    # saves current tree as an array for accessibilty
    def save_tree_as_array(self, node):
        # creats a list of size self.depth with each index holding an empty list
        self.tree_arr = [[] for i in range(self.depth)]
        self.__traverse_tree(node)
        return self.tree_arr

    # traveses tree and saves each node to a 2d array for ease of access
    def __traverse_tree(self, node):
        # this will find the negative index and work up to -1
        # ex. if depth is 5, this will append a node to self.tree[-5]
        # which if 5 is max depth, it will be the same as self.tree[0]
        self.tree_arr[self.depth - self.depth * 2].append(node)
        # subtract 1 from self.depth to make sure the child nodes dont save in the same index
        self.depth -= 1
        if node.left:
            self.__traverse_tree(node.left)
        if node.right:
            self.__traverse_tree(node.right)
        # add 1 to self.depth to make sure it has proper depth going back up the tree
        self.depth += 1