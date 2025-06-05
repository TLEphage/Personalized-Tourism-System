class Node:
    __slots__ = ('id', 'value', 'left', 'right', 'parent')
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _rotate_left(self, x):
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
            y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
            y.right = x
        x.parent = y

    def splay(self, node):
        while node.parent:
            parent = node.parent
            grand = parent.parent
            if not grand:
                if node == parent.left:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
            else:
                if parent == grand.left:
                    if node == parent.left:
                        self._rotate_right(grand)
                        self._rotate_right(parent)
                    else:
                        self._rotate_left(parent)
                        self._rotate_right(grand)
                else:
                    if node == parent.right:
                        self._rotate_left(grand)
                        self._rotate_left(parent)
                    else:
                        self._rotate_right(parent)
                        self._rotate_left(grand)
        self.root = node

    def insert(self, id, value):
        if not self.root:
            self.root = Node(id, value)
            return
        node = self.root
        while node:
            if value == node.value:
                node.id = id
                self.splay(node)
                return
            elif value < node.value:
                if not node.left:
                    new_node = Node(id, value)
                    node.left = new_node
                    new_node.parent = node
                    self.splay(new_node)
                    return
                node = node.left
            else:
                if not node.right:
                    new_node = Node(id, value)
                    node.right = new_node
                    new_node.parent = node
                    self.splay(new_node)
                    return
                node = node.right

    def find(self, value):
        node = self.root
        last_node = None
        while node:
            last_node = node
            if value == node.value:
                self.splay(node)
                return node.id
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        if last_node:
            self.splay(last_node)
        return None

    def delete(self, value):
        if not self.root:
            return
        self.find(value)
        if self.root.value != value:
            return
        left_tree = self.root.left
        right_tree = self.root.right
        if left_tree:
            left_tree.parent = None
        if right_tree:
            right_tree.parent = None
        if not left_tree:
            self.root = right_tree
        else:
            max_node = left_tree
            while max_node.right:
                max_node = max_node.right
            self.splay(max_node)
            max_node.right = right_tree
            if right_tree:
                right_tree.parent = max_node
            self.root = max_node

    def in_order_traversal(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node:
            self.in_order_traversal(node.left, result)
            result.append((node.id, node.value))
            self.in_order_traversal(node.right, result)
        return result

# 示例用法
if __name__ == "__main__":
    splay_tree = SplayTree()
    splay_tree.insert(1, 100)
    splay_tree.insert(2, 50)
    splay_tree.insert(3, 200)
    splay_tree.insert(4, 150)
    
    print("In-order traversal:", splay_tree.in_order_traversal())
    print("Find value 50:", splay_tree.find(50))
    print("Root after find(50):", (splay_tree.root.id, splay_tree.root.value))
    
    splay_tree.delete(50)
    print("After delete(50):", splay_tree.in_order_traversal())
    print("Root after delete:", (splay_tree.root.id, splay_tree.root.value))