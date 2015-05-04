from PySide.QtCore import *
from PySide.QtGui import *

from tree import BinaryTree, trees
from layout import layouts

print '''
j - next tree
k - prev tree
l - next layout
p - prev layout
r - random tree
'''

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.treeIndex = 0
        self.layoutIndex = 0
        self.init()

    def paintEvent(self, ev):

        def getMima(root, propName):
            prop = getattr(root, propName)
            try:
                mis, mas = zip(*[getMima(c, propName) for c in root.children if c])
            except ValueError:
                mis, mas = (), ()
            return min((prop,) + mis), max((prop,) + mas)

        def draw(painter, root, parentPt=None):
            x = margin + availWidth * ((root.x - minX) / dx if dx else 0.5)
            y = margin + availHeight * ((root.y - minY) / dy if dy else 0.5)
            pt = QPointF(x, y)
            if parentPt:
                painter.drawLine(parentPt, pt)
            for child in root.children:
                if child:
                    draw(painter, child, pt)
            painter.drawEllipse(pt, radius, radius)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255,255,255)))

        side = min(self.width(), self.height())
        margin = side / 10.0
        availWidth = self.width() - margin * 2
        availHeight = self.height() - margin * 2
        radius = side / 40.0
        minX, maxX = getMima(self.tree, 'x')
        minY, maxY = getMima(self.tree, 'y')
        dx, dy = float(maxX - minX), float(maxY - minY)

        draw(painter, self.tree)

    def keyPressEvent(self, ev):
        ch = ev.text()
        if ch == 'j':
            self.tree = self.nextTree()
        elif ch == 'k':
            self.tree = self.prevTree()
        elif ch == 'h':
            self.layout = self.prevLayout()
        elif ch == 'l':
            self.layout = self.nextLayout()
        elif ch == 'r':
            trees[self.treeIndex] = BinaryTree.random()
            self.tree = self.curTree()
        else:
            super(Widget, self).keyPressEvent(ev)
        self.init()

    def init(self):
        self.tree = self.curTree()
        self.layout = self.curLayout()
        self.layout(self.tree)
        self.update()
        self.setWindowTitle('{} {}/{}'.format(
            self.layout.func_name,
            self.treeIndex + 1,
            len(trees)))

    def nextTree(self):
        self.treeIndex = (self.treeIndex + 1) % len(trees)
        return self.curTree()

    def prevTree(self):
        self.treeIndex = (self.treeIndex - 1 + len(trees)) % len(trees)
        return self.curTree()

    def curTree(self):
        return trees[self.treeIndex].clone()

    def nextLayout(self):
        self.layoutIndex = (self.layoutIndex + 1) % len(layouts)
        return self.curLayout()

    def prevLayout(self):
        self.layoutIndex = (self.layoutIndex - 1 + len(layouts)) % len(layouts)
        return self.curLayout()

    def curLayout(self):
        layout = layouts[self.layoutIndex]
        return layout

app = QApplication([])
w = Widget()
w.resize(480, 480)
w.show()
app.exec_()
