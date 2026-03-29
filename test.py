from avl_tree import AVLTree
t = AVLTree()
# Insert in sorted order (worst case for BST, AVL should balance)
for i in range(100):
    t.insert(i, i*10)
assert len(t) == 100
assert t.root.height <= 8  # log2(100) ~ 7, AVL allows up to ~1.44*log2
assert t.search(50) == 500
assert 99 in t
assert 100 not in t
t.delete(50)
assert 50 not in t
assert len(t) == 99
items = t.inorder()
assert items == sorted(items)
print("avl_tree tests passed")
