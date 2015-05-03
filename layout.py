def layout(root, depth=0, slot=[0]):
    if root:
        layout(root.left, depth + 1, slot)
        root.x = slot[0]
        root.y = depth
        slot[0] += 1
        layout(root.right, depth + 1, slot)
