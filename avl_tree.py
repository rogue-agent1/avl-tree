#!/usr/bin/env python3
"""AVL tree — self-balancing BST."""
import sys

class Node:
    __slots__ = ('key','left','right','height')
    def __init__(self, key):
        self.key, self.left, self.right, self.height = key, None, None, 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.count = 0
    def _h(self, n): return n.height if n else 0
    def _bal(self, n): return self._h(n.left) - self._h(n.right) if n else 0
    def _update(self, n):
        n.height = 1 + max(self._h(n.left), self._h(n.right))
    def _rotR(self, y):
        x = y.left; y.left = x.right; x.right = y
        self._update(y); self._update(x); return x
    def _rotL(self, x):
        y = x.right; x.right = y.left; y.left = x
        self._update(x); self._update(y); return y
    def _balance(self, n):
        self._update(n)
        b = self._bal(n)
        if b > 1:
            if self._bal(n.left) < 0: n.left = self._rotL(n.left)
            return self._rotR(n)
        if b < -1:
            if self._bal(n.right) > 0: n.right = self._rotR(n.right)
            return self._rotL(n)
        return n
    def insert(self, key):
        self.root = self._insert(self.root, key)
    def _insert(self, n, key):
        if not n: self.count += 1; return Node(key)
        if key < n.key: n.left = self._insert(n.left, key)
        elif key > n.key: n.right = self._insert(n.right, key)
        else: return n
        return self._balance(n)
    def __contains__(self, key):
        n = self.root
        while n:
            if key == n.key: return True
            n = n.left if key < n.key else n.right
        return False
    def __len__(self): return self.count
    def inorder(self):
        r = []
        def io(n):
            if not n: return
            io(n.left); r.append(n.key); io(n.right)
        io(self.root); return r

def test():
    t = AVLTree()
    for x in range(1, 16):
        t.insert(x)
    assert t.inorder() == list(range(1, 16))
    assert len(t) == 15
    assert 10 in t
    assert 20 not in t
    h = t.root.height
    assert h <= 5  # AVL: height <= 1.44*log2(n)
    print("  avl_tree: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("AVL tree")
