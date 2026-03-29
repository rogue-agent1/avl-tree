#!/usr/bin/env python3
"""AVL tree with self-balancing rotations."""
import sys

class Node:
    def __init__(self, key, val=None):
        self.key, self.val, self.left, self.right, self.height = key, val, None, None, 1

def height(n): return n.height if n else 0
def balance(n): return height(n.left) - height(n.right) if n else 0
def update_height(n): n.height = 1 + max(height(n.left), height(n.right))

def rotate_right(y):
    x = y.left; t = x.right; x.right = y; y.left = t
    update_height(y); update_height(x); return x

def rotate_left(x):
    y = x.right; t = y.left; y.left = x; x.right = t
    update_height(x); update_height(y); return y

def insert(root, key, val=None):
    if not root: return Node(key, val)
    if key < root.key: root.left = insert(root.left, key, val)
    elif key > root.key: root.right = insert(root.right, key, val)
    else: root.val = val; return root
    update_height(root); b = balance(root)
    if b > 1 and key < root.left.key: return rotate_right(root)
    if b < -1 and key > root.right.key: return rotate_left(root)
    if b > 1 and key > root.left.key: root.left = rotate_left(root.left); return rotate_right(root)
    if b < -1 and key < root.right.key: root.right = rotate_right(root.right); return rotate_left(root)
    return root

def search(root, key):
    if not root: return None
    if key == root.key: return root.val
    return search(root.left, key) if key < root.key else search(root.right, key)

def inorder(root):
    if not root: return []
    return inorder(root.left) + [(root.key, root.val)] + inorder(root.right)

def is_balanced(root):
    if not root: return True
    return abs(balance(root)) <= 1 and is_balanced(root.left) and is_balanced(root.right)

def main():
    if len(sys.argv) < 2: print("Usage: avl_tree.py <demo|test>"); return
    if sys.argv[1] == "test":
        root = None
        for i in range(100): root = insert(root, i, f"v{i}")
        assert is_balanced(root)
        assert height(root) <= 8  # log2(100) ~ 7
        assert search(root, 50) == "v50"
        assert search(root, 999) is None
        items = inorder(root)
        assert len(items) == 100
        assert items == sorted(items, key=lambda x: x[0])
        # Update
        root = insert(root, 50, "updated")
        assert search(root, 50) == "updated"
        assert is_balanced(root)
        print("All tests passed!")
    else:
        root = None
        for i in [5,3,7,1,4,6,8]: root = insert(root, i)
        print(f"Balanced: {is_balanced(root)}, Height: {height(root)}")

if __name__ == "__main__": main()
