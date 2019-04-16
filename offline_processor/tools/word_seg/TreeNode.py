class TreeNode:
    def __init__(self, value=None):
        self.after = dict()
        self.value = value

    def add_node(self, value):
        if value not in self.after.keys():
            treeNode = TreeNode(value=value)
            self.after[value] = treeNode

    def get_node(self, value):
        return self.after.get(value, None)

