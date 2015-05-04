import itertools
import Queue as queue
from collections import defaultdict
from operator import gt, lt

def knuth(root, depth=0, slot=itertools.count()):
    if root:
        knuth(root.left, depth + 1, slot)
        root.x = slot.next()
        root.y = depth
        knuth(root.right, depth + 1, slot)

def preorder(root, depth=0, slot=itertools.count()):
    if root:
        preorder(root.left, depth + 1, slot)
        preorder(root.right, depth + 1, slot)
        root.x = slot.next()
        root.y = depth

def postorder(root, depth=0, slot=itertools.count()):
    if root:
        root.x = slot.next()
        root.y = depth
        postorder(root.left, depth + 1, slot)
        postorder(root.right, depth + 1, slot)

def depthOf(root):
    if root:
        return max(depthOf(root.left), depthOf(root.right)) + 1
    else:
        return 0

def wetherellShannon(root, depth=0, slots=[]):
    if root:
        if not slots:
            slots = [itertools.count() for _ in range(depthOf(root))]
        root.y = depth
        root.x = slots[depth].next()
        wetherellShannon(root.left, depth + 1, slots)
        wetherellShannon(root.right, depth + 1, slots)

def wsByQueue(root):
    q = queue.Queue()
    q.put(root)
    for depth in itertools.count():
        if q.empty():
            break
        nodes = []
        while not q.empty():
            nodes.append(q.get())
        for i, node in enumerate(nodes):
            node.x = i
            node.y = depth
            for child in node.children:
                if child:
                    q.put(child)

def wsCentered(root, depth=0):
    def setup(root, depth=0, slots=None):
        if slots is None: slots = defaultdict(lambda: 0)
        if root:
            root.y = depth
            setup(root.left, depth + 1, slots)
            setup(root.right, depth + 1, slots)
            if root.left and root.right:
                root.x = (root.left.x + root.right.x) / 2.0
            elif root.left:
                root.x = root.left.x
            elif root.right:
                root.x = root.right.x
            else:
                root.x = slots[depth]
            dx = max(slots[depth] - root.x, 0)
            root.x += dx
            root.offset = dx
            slots[depth] = root.x + 1

    def offset(root, dx=0):
        if root:
            root.x += dx
            offset(root.left, dx + root.offset)
            offset(root.right, dx + root.offset)

    setup(root)
    offset(root)

def contourLayout(root, depth=0):
    def setup(root, depth, comp=gt):
        def better(a, b):
            return a if comp(a, b) else b

        if root:
            root.y = depth
            root.offset = 0
            llc, lrc = setup(root.left, depth + 1, gt)
            rlc, rrc = setup(root.right, depth + 1, lt)
            if root.left and root.right:
                dx = max(l - r for l, r in zip(lrc, rlc)) + 1
                root.right.x += dx
                root.right.offset += dx
                root.x = (root.left.x + root.right.x) / 2.0
            elif root.left:
                root.x = root.left.x + 1
            elif root.right:
                root.x = root.right.x - 1
            else:
                root.x = 0
            lc, rc = [root.x] + llc, [root.x] + rrc
            print root.data, lc, rc
            return lc, rc
        else:
            return [], []

    def offset(root, dx):
        if root:
            root.x += dx
            offset(root.left, dx + root.offset)
            offset(root.right, dx + root.offset)

    setup(root, depth)
    offset(root, 0)

layouts = [
        #wsByQueue,
        contourLayout,
        wetherellShannon,
        wsCentered,
        knuth,
        preorder,
        postorder,
        ]

if __name__ == '__main__':
    import main
