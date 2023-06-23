class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def remove_child(self, node):
        self.children.remove(node)
        node.parent = None

    def walk_forward(self):
        yield self
        for child in self.children:
            yield from child.walk_forward()

    def walk_backward(self):
        yield self
        if self.parent is not None:
            yield from self.parent.walk_backward()


class Tree:
    def __init__(self, root):
        self.root = Node(root)

    def walk_forward(self):
        yield from self.root.walk_forward()

    def walk_backward(self):
        yield from self.root.walk_backward()

    def add_node(self, node):
        self.root.add_child(Node(node))

    def search_cmd_name(self, cmd_name):
        matching_nodes = []

        for node in self.walk_forward():
            if node.data.name == cmd_name:
                matching_nodes.append(node)

        return matching_nodes

    def search_tree(self, cmd_name, provided_args):
        for node in self.walk_forward():
            if node.data.name == cmd_name:
                for arg in provided_args:
                    if arg in node.data.commands:
                        return node
        return None
