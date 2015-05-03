import itertools

def knuth_layout(root, depth=0, slot=itertools.count()):
    if root:
        knuth_layout(root.left, depth + 1, slot)
        root.x = slot.next()
        root.y = depth
        knuth_layout(root.right, depth + 1, slot)

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

layouts = [
        knuth_layout,
        preorder,
        postorder,
        ]
