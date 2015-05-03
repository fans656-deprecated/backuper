def layout(root, depth=0, slots=None):

    def depthOf(root):
        if root:
            if len(root.children):
                return max(depthOf(c) for c in root.children) + 1
            return 1
        else:
            return 0

    if slots is None:
        slots = [0] * depthOf(root)
    root.y = depth
    root.x = slots[depth]
    slots[depth] += 1
    for c in root.children:
        if c:
            layout(c, depth + 1, slots)
