from TrackCircuitElement.Variable import Variable
from TrackCircuitElement.Node import Node


class Edge:
    """
        边
    """

    def __init__(self, parent, base_name):
        self.parent = parent

        self.start = Node()
        self.end = Node()
        # self.start.edges.append((True, self))
        # self.end.edges.append((False, self))
        self.start.edges.add(self)
        self.end.edges.add(self)

        self.base_name = base_name
        self.name = ''

        self.variable = Variable()
        self.variable_type = 'I'

    @property
    def current(self):
        return self.variable.value

    @property
    def voltage(self):
        voltage = self.start.voltage - self.end.voltage
        return voltage

    def config_name(self):
        if self.parent:
            self.name = self.parent.name + '_' + self.base_name
        else:
            self.name = self.base_name
    # def link_edge(self, node):


class ImpedanceEdge(Edge):
    def __init__(self, parent, base_name):
        super().__init__(parent, base_name)
        self._z = None

    @property
    def z(self):
        return self._z

    def config_param(self, param):
        self._z = param


class WindingEdge(Edge):
    def __init__(self, parent, base_name):
        super().__init__(parent, base_name)
        self._other = None
        self._n = None
        # self.source = True

    @property
    def other(self):
        return self._other

    @property
    def n(self):
        return self._n

    def config_param(self, other, n):
        self._other = other
        self._n = n


class VolSrcEdge(Edge):
    def __init__(self, parent, base_name):
        super().__init__(parent, base_name)
        # self.type = '电压源'
        self._vol = None

    @property
    def vol(self):
        return self._vol

    def config_param(self, vol):
        self._vol = vol


class CurSrcEdge(Edge):
    def __init__(self, parent, base_name):
        super().__init__(parent, base_name)
        self.type = '电流源'
        self._cur = None

    @property
    def cur(self):
        return self._cur

    def config_param(self, cur):
        self._cur = cur


class WireEdge(Edge):
    def __init__(self, parent, base_name):
        super().__init__(parent, base_name)
        self.type = '导线'

    def config_param(self):
        pass