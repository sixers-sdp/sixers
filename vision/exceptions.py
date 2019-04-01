

class IncorrectNode(Exception):
    def __init__(self, node_seen):
        self.node_seen = node_seen

