# 变量
class Variable:
    def __init__(self):
        self.num = dict()
        self.name = ''
        self.value = None
        self.value_abs = None


# 节点类型

class Node:
    def __init__(self):
        self.edges = list()
        self.variable = Variable()
        self.variable_type = 'U'
        self.zero = False

class Edge:
    def __init__(self, parent, name_base):
        self.parent = parent
        self.name_base = name_base
        self.name = ''

        self.start = Node()
        self.end = Node()
        self.start.edges.append((True, self))
        self.end.edges.append((False, self))
        self.variable = Variable()
        self.variable_type = 'I'

    @property
    def current(self):
        return self.variable.value

    @property
    def voltage(self):
        voltage = self.start.voltage - self.end.voltage
        return voltage


class ElePack:
    """
    Object serving as a base class for all element package.
    """


    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.element = dict()
        self.ele_list = list()
        self.ele_set = set()
        # self.flag_outside = False
        self._posi_rlt = None
        self.posi_abs = None
        # self.flag_ele_list = False
        # self.flag_ele_unit = False
        # self.called_set = set()

