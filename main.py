import random
import string

from PySide.QtGui import *
from PySide.QtCore import *

class Node(object):

    def __init__(self):
        self.left = None
        self.right = None

def layout(root, depth=0):
    def depthOf(root):
        if root:
            return max(depthOf(root.left), depthOf(root.right)) + 1
        else:
            return 0

    def setup(root, depth):
        if root:
            setup(root.left, depth + 1)
            setup(root.right, depth + 1)
            root.y = depth
            if root.left is None and root.right is None:
                root.x = slots[depth]
            elif root.left and root.right:
                root.x = (root.left.x + root.right.x) / 2.0
            else:
                root.x = root.left.x if root.left else root.right.x
            dx = max(slots[depth] - root.x, 0)
            root.x += dx
            root.successorOffset = dx
            slots[depth] = root.x + 2

    def offset(root, parentOffset):
        if root:
            root.x += parentOffset
            offset(root.left, parentOffset + root.successorOffset)
            offset(root.right, parentOffset + root.successorOffset)

    slots = [0] * depthOf(root)
    setup(root, depth)
    offset(root, 0)

class Widget(QDialog):

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QBrush(QColor(255,255,255)))

        self.minX = 99999
        self.minY = 99999
        self.maxX = -99999
        self.maxY = -99999
        margin = 50
        self.begX = margin
        self.begY = margin
        self.availWidth = self.width() - 2 * margin
        self.availHeight = self.height() - 2 * margin

        self.getmima(root)
        self.adjust(root)
        self.draw(p, root)

    def draw(self, p, root):
        if root is None:
            return
        pt = QPointF(root.x, root.y)
        # draw lines
        if root.left:
            p.drawLine(pt, QPointF(root.left.x, root.left.y))
        if root.right:
            p.drawLine(pt, QPointF(root.right.x, root.right.y))
        # draw nodes
        radius = self.width() / 80.0
        radius = 2
        p.drawEllipse(pt, radius, radius)
        self.draw(p, root.left)
        self.draw(p, root.right)

    def adjust(self, root):
        if root is None:
            return
        dx = self.maxX - self.minX
        dy = self.maxY - self.minY
        if dx:
            root.x = self.begX + self.availWidth * (root.x - self.minX) / float(dx)
        else:
            root.x = self.begX + self.availWidth / 2.0
        if dy:
            root.y = self.begY + self.availHeight * (root.y - self.minY) / float(dy)
        else:
            root.y = self.begY + self.availHeight / 2.0
        self.adjust(root.left)
        self.adjust(root.right)

    def getmima(self, root):
        if root is None:
            return
        if root.x < self.minX:
            self.minX = root.x
        if root.x > self.maxX:
            self.maxX = root.x
        if root.y < self.minY:
            self.minY = root.y
        if root.y > self.maxY:
            self.maxY = root.y
        self.getmima(root.left)
        self.getmima(root.right)

    def keyPressEvent(self, ev):
        global root
        ch = ev.text()
        if ev.key() == Qt.Key_Escape:
            super(Widget, self).keyPressEvent(ev)
            return
        elif ch == 'j':
            if root.left and root.right:
                root.left, root.right = root.right, root.left
                layout(root)
                self.update()
        elif ch and ch in string.printable:
            root = self.randomTree(root, 10)
            layout(root)
            self.update()

    def randomTree(self, root, depth):
        if depth:
            root = Node()
            if random.randint(0, 5):
                root.left = self.randomTree(root.left, depth - 1)
            if random.randint(0, 5):
                root.right = self.randomTree(root.right, depth - 1)
            return root

#root = Node()
#root.left = Node()
#root.right = Node()
#root.right.left = Node()
#root.right.left.left = Node()
#root.right.left.left.left = Node()

root = Node()

root.left = Node()
root.left.left = Node()
root.left.left.left = Node()
root.left.left.right = Node()

root.right = Node()
root.right.left = Node()
root.right.right = Node()
root.right.right.left = Node()
root.right.right.right = Node()

def show(root, depth=0):
    if root:
        print '  ' * depth + '{}, {}'.format(root.x, root.y)
        show(root.left, depth + 1)
        show(root.right, depth + 1)

layout(root)
#show(root)
print '''
j - swap left and right sub-tree of root
esc - quit
others - random tree
'''

app = QApplication([])
w = Widget()
w.resize(480, 480)
#w.showMaximized()
w.show()
app.exec_()
