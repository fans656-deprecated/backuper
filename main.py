import random
import string
from operator import gt, lt

from PySide.QtGui import *
from PySide.QtCore import *

class Node(object):

    index = 0

    def __init__(self):
        self.left = None
        self.right = None
        self.index = Node.index
        Node.index += 1

def layout(root):
    def setup(root, depth):
        def push(left, right):
            def contour(root, comp, cur=[]):
                if root:
                    if not cur:
                        cur = [root.x]
                    if comp(root.x, cur[0]):
                        cur[0] = root.x
                    l = contour(root.left, comp, cur)
                    r = contour(root.right, comp, cur)
                    cur[0] = l if comp(l, r) else r
                return cur[0]

            l = contour(left, gt)
            r = contour(right, lt)
            dx = max(l - r + 1, 0)
            print '{} contour: {} {}, dx: {}'.format(root.index, l, r, dx)
            right.x += dx
            right.offset = dx

        if not root:
            return
        root.offset = 0
        if not root.left and not root.right:
            root.x = 0
        else:
            setup(root.left, depth + 1)
            setup(root.right, depth + 1)
            if root.left and root.right:
                push(root.left, root.right)
                root.x = (root.left.x + root.right.x) / 2.0
            elif root.left:
                root.x = root.left.x + 1
            elif root.right:
                root.x = root.right.x - 1
        root.y = depth

    def offset(root, dx):
        if root:
            print 'offset {}: {}'.format(root.index, dx)
            root.x += dx
            offset(root.left, dx + root.offset)
            offset(root.right, dx + root.offset)

    setup(root, 0)
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
        radius = self.width() / 40.0
        p.drawEllipse(pt, radius, radius)
        p.drawText(pt, str(root.index))
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
            root = self.randomTree(root, 5)
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
root.left.right = Node()
root.left.right.right = Node()
root.right = Node()
root.right.left = Node()
root.right.left.left = Node()

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
