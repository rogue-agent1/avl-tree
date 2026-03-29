#!/usr/bin/env python3
"""AVL tree (self-balancing BST). Zero dependencies."""

class AVLNode:
    def __init__(self, key, value=None):
        self.key, self.value = key, value
        self.left = self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def _height(self, n): return n.height if n else 0
    def _balance(self, n): return self._height(n.left) - self._height(n.right) if n else 0
    def _update(self, n):
        n.height = 1 + max(self._height(n.left), self._height(n.right))

    def _rotate_right(self, y):
        x = y.left; t = x.right
        x.right = y; y.left = t
        self._update(y); self._update(x)
        return x

    def _rotate_left(self, x):
        y = x.right; t = y.left
        y.left = x; x.right = t
        self._update(x); self._update(y)
        return y

    def _rebalance(self, node):
        self._update(node)
        b = self._balance(node)
        if b > 1:
            if self._balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if b < -1:
            if self._balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, key, value=None):
        def _ins(node):
            if not node:
                self.size += 1
                return AVLNode(key, value)
            if key < node.key: node.left = _ins(node.left)
            elif key > node.key: node.right = _ins(node.right)
            else: node.value = value; return node
            return self._rebalance(node)
        self.root = _ins(self.root)

    def search(self, key):
        node = self.root
        while node:
            if key < node.key: node = node.left
            elif key > node.key: node = node.right
            else: return node.value
        return None

    def delete(self, key):
        def _min(n):
            while n.left: n = n.left
            return n
        def _del(node, key):
            if not node: return node
            if key < node.key: node.left = _del(node.left, key)
            elif key > node.key: node.right = _del(node.right, key)
            else:
                self.size -= 1
                if not node.left: return node.right
                if not node.right: return node.left
                succ = _min(node.right)
                node.key, node.value = succ.key, succ.value
                self.size += 1
                node.right = _del(node.right, succ.key)
                return self._rebalance(node)
            return self._rebalance(node)
        self.root = _del(self.root, key)

    def inorder(self):
        result = []
        def _walk(n):
            if not n: return
            _walk(n.left); result.append((n.key, n.value)); _walk(n.right)
        _walk(self.root)
        return result

    def __len__(self): return self.size
    def __contains__(self, key): return self.search(key) is not None

if __name__ == "__main__":
    t = AVLTree()
    for i in range(10): t.insert(i, i*10)
    print(f"AVL tree height: {t.root.height}, size: {len(t)}")
