import random

class Tree(object):

    def __init__(self, data='*'):
        self.data = data
        self.children = []

    def __iter__(self):
        return self.children.__iter__()

    def show(self, depth=0, showFunc=str):
        print '  ' * depth + showFunc(self)
        for child in self.children:
            child.show(depth + 1, showFunc)

class BinaryTree(Tree):

    def __init__(self, data='*'):
        super(BinaryTree, self).__init__(data)
        self.children = [None, None]

    @property
    def left(self):
        return self.children[0] if len(self.children) else None

    @left.setter
    def left(self, tree):
        self.children[0] = tree

    @property
    def right(self):
        return self.children[1] if len(self.children) >= 2 else None

    @right.setter
    def right(self, tree):
        self.children[1] = tree

    def show(self, depth=0, showFunc=str):
        print '  ' * depth + showFunc(self)
        if self.left and self.right:
            self.left.show(depth + 1, showFunc)
            self.right.show(depth + 1, showFunc)
        elif self.left:
            self.left.show(depth + 1, showFunc)
            BinaryTree().show(depth + 1, lambda _: '-')
        elif self.right:
            BinaryTree().show(depth + 1, lambda _: '-')
            self.right.show(depth + 1, showFunc)

    @staticmethod
    def random(depth=5, probability=2):
        def randomByDepth(depth):
            root = BinaryTree()
            if depth > 1:
                root.left = randomByDepth(depth - 1)
                root.right = randomUntilDepth(depth - 1)
                if random.randint(0, probability - 1):
                    root.left, root.right = root.right, root.left
            return root

        def randomUntilDepth(depth):
            root = None
            if depth and random.randint(0, probability - 1):
                root = BinaryTree()
                if random.randint(0, probability - 1):
                    root.left = randomUntilDepth(depth - 1)
                if random.randint(0, probability - 1):
                    root.right = randomUntilDepth(depth - 1)
            return root

        return randomByDepth(depth)
