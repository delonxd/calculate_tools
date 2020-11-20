class Port:
    """
        端口
    """

    def __init__(self, edge, flag: bool):
        self.edge = edge
        self.start_flag = flag

    @property
    def node(self):
        if self.start_flag:
            return self.edge.start
        else:
            return self.edge.end

    def link_node(self, other):
        self.node.link_node(other)