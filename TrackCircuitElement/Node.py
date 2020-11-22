from TrackCircuitElement.Variable import Variable


class Node:
    """
        节点
    """

    def __init__(self):
        # self.edges = list()
        self.edges = set()
        self.parent = None
        self.variable = Variable()
        self.variable_type = 'U'
        self.zero = False

    @property
    def voltage(self):
        return self.variable.value

    @property
    def voltage_abs(self):
        return self.variable.value_abs

    @property
    def name(self):
        for edge in self.edges:
            if self == edge.start:
                return edge.name + '_起点'
            else:
                return edge.name + '_终点'

    # @property
    # def name(self):
    #     direction, edge = self.edges[0]
    #     if direction:
    #         return edge.name + '_起点'
    #     else:
    #         return edge.name + '_终点'

    # def link_edge(self, edge, outflow: bool = True):
    #     if isinstance(edge, Edge):
    #         self.edges.append((outflow, edge))
    #         if outflow:
    #             edge.start = self
    #         else:
    #             edge.end = self
    #     else:
    #         raise KeyboardInterrupt("类型异常：需要边类型")

    def link_edge(self, edge, outflow: bool = True):
        from TrackCircuitElement.Edge import Edge

        if isinstance(edge, Edge):
            self.edges.add(edge)
            if outflow:
                edge.start = self
            else:
                edge.end = self
        else:
            raise KeyboardInterrupt("类型异常：需要边类型")

    def link_node(self, other):
        from TrackCircuitElement.Port import Port

        if isinstance(other, Node):
            for edge in other.edges:
                self.edges.add(edge)
                if edge.start == other:
                    edge.start = self
                else:
                    edge.end = self
        elif isinstance(other, Port):
            self.link_node(other.node)
        else:
            raise KeyboardInterrupt("类型异常：需要节点类型")

    # def link_node(self, other):
    #     if isinstance(other, Node):
    #         for outflow, edge in other.edges:
    #             self.edges.append((outflow, edge))
    #             if outflow:
    #                 edge.start = self
    #             else:
    #                 edge.end = self
    #     elif isinstance(other, Port):
    #         self.link_node(other.node)
    #     else:
    #         raise KeyboardInterrupt("类型异常：需要节点或端口类型")

    #
    # def print_edges(self):
    #     list1 = []
    #     for outflow, edge in self.edges:
    #         if outflow:
    #             list1.append((edge.name, '起点'))
    #         else:
    #             list1.append((edge.name, '终点'))
    #     print(list1)