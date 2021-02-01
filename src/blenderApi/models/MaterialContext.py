class MaterialContext:
    def __init__(self, material):
        self.material = material
        self.node_tree = material.node_tree
        self.nodes = material.node_tree.nodes
        self.node_links = self.node_tree.links
