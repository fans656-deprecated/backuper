from PySide.QtCore import *
from PySide.QtGui import *

from tree import BinaryTree
from layout import layout

print '''
j - random tree
'''

def randomTree():
    global tree
    tree = BinaryTree.random(5)
    #tree = BinaryTree(1)
    #tree.left = BinaryTree(2)
    #tree.left.left = BinaryTree(4)
    #tree.right = BinaryTree(3)
    layout(tree)
    #tree.show(showFunc=lambda t: '{} {}'.format(t.x, t.y) if t else '-')

tree = None
randomTree()

class Widget(QDialog):

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
        minX, maxX = getMima(tree, 'x')
        minY, maxY = getMima(tree, 'y')
        dx, dy = float(maxX - minX), float(maxY - minY)

        draw(painter, tree)

    def keyPressEvent(self, ev):
        ch = ev.text()
        if ch == 'j':
            randomTree()
            self.update()
            return
        super(Widget, self).keyPressEvent(ev)

app = QApplication([])
w = Widget()
w.resize(480, 480)
w.show()
app.exec_()
