def knuth_layout(root, depth=0, slot=[0]):
    if root:
        knuth_layout(root.left, depth + 1, slot)
        root.x = slot[0]
        root.y = depth
        slot[0] += 1
        knuth_layout(root.right, depth + 1, slot)

def preorder(root, depth=0, slot=[0]):
    if root:
        preorder(root.left, depth + 1, slot)
        preorder(root.right, depth + 1, slot)
        root.x = slot[0]
        root.y = depth
        slot[0] += 1

def postorder(root, depth=0, slot=[0]):
    if root:
        root.x = slot[0]
        root.y = depth
        slot[0] += 1
        postorder(root.left, depth + 1, slot)
        postorder(root.right, depth + 1, slot)

layouts = [
        knuth_layout,
        preorder,
        postorder,
        ]
