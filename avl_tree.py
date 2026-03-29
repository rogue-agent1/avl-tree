#!/usr/bin/env python3
"""avl_tree - Self-balancing AVL tree with rotations."""
import sys

class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def _height(self, n):
        return n.height if n else 0

    def _balance(self, n):
        return self._height(n.left) - self._height(n.right) if n else 0

    def _update(self, n):
        n.height = 1 + max(self._height(n.left), self._height(n.right))

    def _rot_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self._update(y)
        self._update(x)
        return x

    def _rot_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self._update(x)
        self._update(y)
        return y

    def _rebalance(self, n):
        self._update(n)
        b = self._balance(n)
        if b > 1:
            if self._balance(n.left) < 0:
                n.left = self._rot_left(n.left)
            return self._rot_right(n)
        if b < -1:
            if self._balance(n.right) > 0:
                n.right = self._rot_right(n.right)
            return self._rot_left(n)
        return n

    def _insert(self, node, key):
        if not node:
            self.size += 1
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return self._rebalance(node)

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _min_node(self, n):
        while n.left:
            n = n.left
        return n

    def _delete(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            self.size -= 1
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            succ = self._min_node(node.right)
            node.key = succ.key
            self.size += 1
            node.right = self._delete(node.right, succ.key)
        return self._rebalance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def search(self, key):
        n = self.root
        while n:
            if key == n.key: return True
            n = n.left if key < n.key else n.right
        return False

    def inorder(self):
        result = []
        def traverse(n):
            if n:
                traverse(n.left)
                result.append(n.key)
                traverse(n.right)
        traverse(self.root)
        return result

def test():
    t = AVLTree()
    for v in [10, 20, 30, 40, 50, 25]:
        t.insert(v)
    assert t.inorder() == [10, 20, 25, 30, 40, 50]
    assert t.size == 6
    assert abs(t._balance(t.root)) <= 1
    assert t.search(30)
    assert not t.search(99)
    t.delete(30)
    assert not t.search(30)
    assert t.inorder() == [10, 20, 25, 40, 50]
    assert t.size == 5
    t2 = AVLTree()
    for i in range(100):
        t2.insert(i)
    assert t2.size == 100
    assert t2._height(t2.root) <= 8
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("avl_tree: AVL tree. Use --test")
