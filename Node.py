class Node:

    def __init__(self, parent, score, max_min):
        self.score = score
        self.parent = parent
        self.max_min = max_min
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_child_state(self):
        return not self.max_min

    def print_children(self):
        pass

    def printTree(self, indentation_number):  # function to print the minimax tree
        if self.max_min:
            string = "MAX"
        else:
            string = "MIN"
        print(indentation_number * '\t', string, " Score: ", self.score, "\tdepth:", indentation_number)
        for child in self.children:
            child.printTree(indentation_number + 1)


def get_tree_len(root):
    if not root:
        return 0
    count = 1
    children = root.get_children()
    for child in children:
        count += get_tree_len(child)
    return count
