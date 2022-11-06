import numpy as np
from tree import Tree
from entrant import PlaceHolder

class Bracket:
    def __init__(self, entrants: list):
        self.tree = Tree()
        self.entrants = entrants
        self.size = len(entrants)
        self.depth = int(np.ceil(np.log2(self.size)) + 1)
        self.remainder = 0
        self.place_holder_tbd = PlaceHolder("TBD")
        self.__build_bracket()

    # updates the values of the empty tree to match the values given in entrants
    def __build_bracket(self):
        self.tree.build_empty_tree(self.depth)
        # finds how many empty nodes are on the bottom row of the bracket
        n = (2 ** (self.depth - 1))
        # finds how many entrant nodes are on the bottom and how many need to be one tier up
        # used to dynamically draw the bracket based on how many entrants there are
        self.remainder = n - self.size
        self.__traverse_bracket(self.tree.root, 1)
    
    # sepcial traverse function that adds entrants to the bottom tier of the bracket
    # this builds the bracket from right to left
    def __traverse_bracket(self, node, level):
        # checks if bracket branch is at the max depth based on how many entrants need to be on an upper tier
        if (self.remainder > 0) and (level == self.depth - 1):
            self.remainder -= 1
            # removes both node.left and node.right from current node
            node.left, node.right = None, None
            # assigns the node an Entrant object as its value
            node.value = self.entrants.pop()
        # checks if bracket branch is at the max depth if remainder == 0
        elif (level == self.depth):
            node.value = self.entrants.pop()
        # if bracket branch is not at the max depth, set node.value to a placeholder and check right and left nodes
        else:
            node.value = self.place_holder_tbd
            self.__traverse_bracket(node.right, level + 1)
            self.__traverse_bracket(node.left, level + 1)

    def draw_bracket(self):
        # see tree.py for this function
        self.tree.save_tree_as_array(self.tree.root)
        # used to draw horizontal lines in bracket
        level = 0
        # traverse trr_arr
        for i in self.tree.tree_arr:
            # update level
            level += 1
            # dynamically set max_line_size to fit up to 16 nodes from tree
            max_line_size = 11 * np.power(2, self.tree.depth - 1)
            # dynamicallt set fill based on max line size
            # fill is used to determine the space each TreeNode.value will have
            fill = int(max_line_size / np.power(2, level - 1))
            # for all passes of the function except the first
            if level != 1:
                # draw horizontal lines of bracket
                print('\n', "|".center(fill) * len(i), sep="")
            # traverse each index of tree_arr 
            for j in i:
                # this checks if the current node is the at the bottom of its respective branch
                if not j.left and not j.right: 
                    # if so the only difference is that it will not use '_' to fill in the space
                    print(j.value.name.center(fill // 2 - 1, ' ').center(fill), end="")
                else:
                    print(j.value.name.center(fill // 2 - 1, '_').center(fill), end="")
        # before going into the next index of tree_arr, use a linebreak
        print('\n')