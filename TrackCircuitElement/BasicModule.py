from TrackCircuitElement.Port import Port
from TrackCircuitElement.Edge import Edge


class BasicModule:
    """
        基础模块
    """

    def __init__(self, parent, bas_name, **kw):
        # structure
        self.parent = parent

        # parameters
        self.bas_name = bas_name
        self.param = None

        # generated
        self.name = str()
        self.ports = list()
        self.modules = list()
        self.edges = list()
        # self.edges_all = list()

    def load_kw(self, **kwargs):
        """

        """
        pass

    def get_edges(self):
        edges = self.edges.copy()
        for ele in self.modules:
            edges.extend(ele.get_edges())
        return edges

    def get_nodes(self):
        nodes = set()
        # for edge in self.edges:
        #     nodes.add(edge.start)
        #     nodes.add(edge.end)
        # for module in self.modules:
        #     nodes.update(module.get_nodes())
        for edge in self.get_edges():
            nodes.add(edge.start)
            nodes.add(edge.end)
        return nodes

    def print_edges(self):
        name_list = list()
        for edge in self.get_edges():
            name_list.append(edge.name)
        name_list.sort()
        print(name_list)

    def print_nodes(self):
        name_list = list()
        for node in self.get_nodes():
            name_list.append(node.name)
            print(node.name)
            node.print_edges()

    def config_port(self, *ports):
        for port in ports:
            if isinstance(port, Port):
                self.ports.append(port)
            else:
                raise KeyboardInterrupt("类型异常：需要Port类型")

    # def config_port(self, *nodes):
    #     for node in nodes:
    #         if isinstance(node, Node):
    #             self.ports.append(node)
    #         else:
    #             raise KeyboardInterrupt("类型异常：需要Node类型")

    def add_element(self, *element):
        for ele in element:
            if isinstance(ele, Edge):
                self.edges.append(ele)
                ele.parent = self
            elif isinstance(ele, BasicModule):
                self.modules.append(ele)
                ele.parent = self
            else:
                raise KeyboardInterrupt("类型异常：需要Edge或Module类型")

    def config_edge_para(self, freq):
        pass

    def config_parameter(self, freq):
        for md in self.modules:
            md.config_parameter(freq)
        self.config_edge_para(freq)

    def create_circuit(self):
        pass

    def create_port(self):
        pass

    def config_name(self):
        if self.parent:
            self.name = self.parent.name + '_' + self.bas_name
        else:
            self.name = self.bas_name
        for edge in self.edges:
            edge.config_name()
        for module in self.modules:
            module.config_name()
