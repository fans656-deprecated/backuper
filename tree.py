import random
import re

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

    def clone(self):
        root = self
        root.children = [c.clone() if c else c for c in self.children]
        return root

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
    def random(depth=5, probability=5):
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

    @staticmethod
    def make(s):
        def getNode(key):
            if key not in nodes:
                nodes[key] = BinaryTree(key)
            return nodes[key]

        nodes = {}
        for i, rel in enumerate(s.split()):
            parent, direction, child = re.match(r'(\d+)([<>])(\d+)', rel).groups()
            parent = getNode(parent)
            child = getNode(child)
            if direction == '<':
                parent.left = child
            else:
                parent.right = child
            if i == 0:
                root = parent
        return root

trees = [
        #BinaryTree.random(),
        BinaryTree.make('1<2 1>3 2<4 2>5 3<6 3>7'),
        BinaryTree.make('1<2 1>3'),
        BinaryTree.make('1<2'),
        BinaryTree.make('1<2 1>3 2<4 2>5 5<6 6<7 5>8 8<9 8>10 3>11 11<12 12<13 12>14'), # wrong?
        BinaryTree.make('1<2 1>3 3<4 3>5 4<6 6>7 5<8 5>9 9<10 10<11 11>12 9>13 13<14 14>15 13>16 16<17'), # Tidier.. fig 5
        BinaryTree.make('1<2 1>3 3<4 4<5 5<6'), # figure 2
        BinaryTree.make('1<2 1>3 2>4 4>5 5>6'), # figure 2 mirror
        BinaryTree.make('1<2 2>3 1>4 4<5'),
        BinaryTree.make('1<2 1>3 2>4 4<5 4>6 3<7 3>8 8<9 8>10'), # figure 4
        BinaryTree.make('1<2 1>3 3>4'),
        BinaryTree.make('1<2 1>3 3<4 3>5'),
        BinaryTree.make('1<2 1>3 3<4'),
        ]

if __name__ == '__main__':
    import main
