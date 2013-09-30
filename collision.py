import sfml as sf

def collides(rect1, rect2):
    left = max(rect1.left, rect2.left)
    top = max(rect1.top, rect2.top)
    right = min(rect1.right, rect2.right)
    bottom = min(rect1.bottom, rect2.bottom)

    if left < right and top < bottom:
        return True
    else:
        return False
