from tkinter import Place
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


    def __build_bracket(self):
        self.tree.build_empty_tree(self.depth)
        n = (2 ** (self.depth - 1))
        self.remainder = n - self.size
        level = 1
        self.__traverse_bracket(self.tree.root, level)

    def __traverse_bracket(self, node, level):
        if (self.remainder > 0) and (level == self.depth - 1):
            self.remainder -= 1
            node.left, node.right = None, None
            node.value = self.entrants.pop()
        elif (level == self.depth):
            node.value = self.entrants.pop()
        else:
            node.value = self.place_holder_tbd
            self.__traverse_bracket(node.right, level + 1)
            self.__traverse_bracket(node.left, level + 1)

    def draw_bracket(self):
        self.tree.save_tree_as_array(self.tree.root)
        level = 0
        for i in self.tree.tree_arr:
            level += 1
            max_line_size = 11 * np.power(2, self.tree.depth - 1)
            fill = int(max_line_size / np.power(2, level - 1))
            if level != 1:
                print('\n', "|".center(fill) * len(i), sep="")
            for j in i:
                if not j.left and not j.right: 
                    print(j.value.name.center(fill // 2 - 1, ' ').center(fill), end="")
                else:
                    print(j.value.name.center(fill // 2 - 1, '_').center(fill), end="")
        print('\n')