import itertools
import Queue as queue

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

def wetherellShannon(root, depth=0, slots=[]):
    def depthOf(root):
        if root:
            return max(depthOf(root.left), depthOf(root.right)) + 1
        else:
            return 0

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

layouts = [
        wsByQueue,
        wetherellShannon,
        knuth,
        preorder,
        postorder,
        ]

if __name__ == '__main__':
    import main
