import numpy as np
import time
import itertools
import os
import sys
import pickle


# 变量
class Variable:
    def __init__(self):
        self.num = dict()
        self.name = ''
        self.value = None
        self.value_abs = None


class Node:
    def __init__(self):
        self.edges = list()
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
        direction, edge = self.edges[0]
        if direction:
            return edge.name + '_起点'
        else:
            return edge.name + '_终点'

    def link_edge(self, edge, outflow: bool = True):
        if isinstance(edge, Edge):
            self.edges.append((outflow, edge))
            if outflow:
                edge.start = self
            else:
                edge.end = self
        else:
            raise KeyboardInterrupt("类型异常：需要边类型")

    def link_node(self, other):
        if isinstance(other, Node):
            for outflow, edge in other.edges:
                self.edges.append((outflow, edge))
                if outflow:
                    edge.start = self
                else:
                    edge.end = self
        elif isinstance(other, Port):
            self.link_node(other.node)
        else:
            raise KeyboardInterrupt("类型异常：需要节点或端口类型")

    def print_edges(self):
        list1 = []
        for outflow, edge in self.edges:
            if outflow:
                list1.append((edge.name, '起点'))
            else:
                list1.append((edge.name, '终点'))
        print(list1)


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

    def config_name(self):
        if self.parent:
            self.name = self.parent.name + '_' + self.name_base
        else:
            self.name = self.name_base
    # def link_edge(self, node):


class EdgeResistance(Edge):
    def __init__(self, parent, name_base, z):
        super().__init__(parent, name_base)
        self.type = '阻抗'
        self.z = z

    def config_parameter(self, z):
        self.z = z


class EdgeWinding(Edge):
    def __init__(self, parent, name_base):
        super().__init__(parent, name_base)
        self.type = '绕组'
        self.other = None
        self.n = 1
        # self.source = True

    def config_parameter(self, other, n):
        self.other = other
        self.n = n


class EdgePowerU(Edge):
    def __init__(self, parent, name_base, u):
        super().__init__(parent, name_base)
        self.type = '电压源'
        self.u = u

    def config_parameter(self, u):
        self.u = u


class EdgePowerI(Edge):
    def __init__(self, parent, name_base, i):
        super().__init__(parent, name_base)
        self.type = '电流源'
        self.i = i

    def config_parameter(self, i):
        self.i = i


class EdgeWire(Edge):
    def __init__(self, parent, name_base):
        super().__init__(parent, name_base)
        self.type = '导线'

    def config_parameter(self):
        pass


class Port:
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


class Module:
    def __init__(self, parent, name_base):
        self.parent = parent
        self.name_base = name_base
        self.name = ''

        self.ports = list()
        self.modules = list()
        self.edges = list()
        # self.edges_all = list()

    def get_edges(self):
        edges = self.edges.copy()
        for ele in self.modules:
            edges.extend(ele.get_edges())
        return edges

    def get_nodes(self):
        nodes = set()
        for edge in self.edges:
            nodes.add(edge.start)
            nodes.add(edge.end)
        for module in self.modules:
            nodes.update(module.get_nodes())
        return nodes

    def print_edges(self):
        for edge in self.get_edges():
            print(edge.name)

    def print_nodes(self):
        for node in self.get_nodes():
            print(node.name)
            node.print_edges()

    def config_port(self, *ports):
        for port in ports:
            if isinstance(port, Port):
                self.ports.append(port)
            else:
                raise KeyboardInterrupt("类型异常：需要Port类型")

    def add_element(self, *element):
        for ele in element:
            if isinstance(ele, Edge):
                self.edges.append(ele)
                ele.parent = self
            elif isinstance(ele, Module):
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
            self.name = self.parent.name + '_' + self.name_base
        else:
            self.name = self.name_base
        for edge in self.edges:
            edge.config_name()
        for module in self.modules:
            module.config_name()


class ModuleImpedance(Module):
    def __init__(self, parent, name_base, z):
        super().__init__(parent, name_base)
        self.z = z
        self.r1 = EdgeResistance(self, '阻抗', 0)

        self.add_element(self.r1)

        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        pass

    def create_port(self):
        self.config_port(Port(self.r1, True), Port(self.r1, False))

    def config_edge_para(self, freq):
        self.r1.config_parameter(self.z[freq])


class Cable(Module):
    def __init__(self, parent, name_base, length, cab_r, cab_l, cab_c):
        super().__init__(parent, name_base)
        self.R = cab_r
        self.L = cab_l
        self.C = cab_c
        self.length = length

        self.r1 = EdgeResistance(self, 'R1', 0)
        self.r2 = EdgeResistance(self, 'R2', 0)
        self.rp1 = EdgeResistance(self, 'Rp1', 0)
        self.rp2 = EdgeResistance(self, 'Rp2', 0)
        self.add_element(self.r1, self.r2, self.rp1, self.rp2)

        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        self.r1.start.link_node(self.rp1.start)
        self.r2.start.link_node(self.rp1.end)
        self.r1.end.link_node(self.rp2.start)
        self.r2.end.link_node(self.rp2.end)

    def create_port(self):
        self.config_port(Port(self.r1, True), Port(self.r2, True),
                         Port(self.r1, False), Port(self.r2, False))

    def config_edge_para(self, freq):
        length = float(self.length)
        w = 2 * np.pi * freq
        z0 = float(self.R) + 1j * w * float(self.L)
        y0 = 10e-10 + 1j * w * float(self.C)
        # y0 = 1j * w * float(self.C)
        zc = np.sqrt(z0 / y0)
        gama = np.sqrt(z0 * y0)
        zii = zc * np.sinh(gama * length)
        yii = (np.cosh(gama * length) - 1) / zc / np.sinh(gama * length)

        self.r1.config_parameter(zii/2)
        self.r2.config_parameter(zii/2)
        self.rp1.config_parameter(1/yii)
        self.rp2.config_parameter(1/yii)


class Transformer(Module):
    def __init__(self, parent, name_base, n):
        super().__init__(parent, name_base)
        self.n = n
        self.w1 = EdgeWinding(self, '1原边')
        self.w2 = EdgeWinding(self, '2副边')
        self.add_element(self.w1, self.w2)

        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        pass

    def create_port(self):
        self.config_port(Port(self.w1, True), Port(self.w1, False),
                         Port(self.w2, True), Port(self.w2, False))

    def config_edge_para(self, freq):
        self.w1.config_parameter(self.w2, self.n)
        self.w2.config_parameter(self.w1, 1 / self.n)
        # self.w1.source = True
        # self.w2.source = False


class TwoPortCircuitPi(Module):
    def __init__(self, parent, name_base, z1, z2, z3):
        super().__init__(parent, name_base)
        self.r1 = ModuleImpedance(self, 'R1', z1)
        self.r2 = ModuleImpedance(self, 'R2', z2)
        self.r3 = ModuleImpedance(self, 'R3', z3)
        self.add_element(self.r1, self.r2, self.r3)
        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        self.r1.ports[0].link_node(self.r2.ports[0])
        self.r2.ports[1].link_node(self.r3.ports[0])
        self.r1.ports[1].link_node(self.r3.ports[1])

    def create_port(self):
        self.config_port(self.r1.ports[0], self.r2.ports[1],
                         self.r3.ports[0], self.r3.ports[1])


class TwoPortCircuitT(Module):
    def __init__(self, parent, name_base, z1, z2, z3):
        super().__init__(parent, name_base)
        self.r1 = ModuleImpedance(self, 'R1', z1)
        self.r2 = ModuleImpedance(self, 'R2', z2)
        self.r3 = ModuleImpedance(self, 'R3', z3)
        self.add_element(self.r1, self.r2, self.r3)
        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        self.r1.ports[1].link_node(self.r3.ports[0])
        self.r1.ports[1].link_node(self.r2.ports[0])

    def create_port(self):
        self.config_port(self.r1.ports[0], self.r2.ports[1],
                         self.r3.ports[1], self.r2.ports[1])


class TcsrTransformer(Module):
    def __init__(self, parent, name_base, z1, z2, z3, n):
        super().__init__(parent, name_base)
        self.m1 = TwoPortCircuitT(self, '1等效内阻', z1, z2, z3)
        self.m2 = Transformer(self, '2理想变压器', n)

        self.add_element(self.m1, self.m2)
        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        self.m1.ports[2].link_node(self.m2.ports[0])
        self.m1.ports[3].link_node(self.m2.ports[1])

    def create_port(self):
        self.config_port(self.m1.ports[0], self.m1.ports[1],
                         self.m2.ports[2], self.m2.ports[3])


class TcsrFL(TcsrTransformer):
    def __init__(self, parent, name_base, z1, z2, n):
        super().__init__(parent, name_base, z1, z2, z1, n)


class TcsrTAD(Module):
    def __init__(self, parent, name_base, z1, z2, z3, zc, n):
        super().__init__(parent, name_base)
        self.l1 = ModuleImpedance(self, '1共模电感', z3)
        self.m1 = TcsrTransformer(self, '2变压器', z1, z2, z1, n)
        self.c1 = ModuleImpedance(self, '3电容', zc)

        self.add_element(self.l1, self.m1, self.c1)
        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        self.l1.ports[1].link_node(self.m1.ports[0])
        self.c1.ports[0].link_node(self.m1.ports[2])

    def create_port(self):
        self.config_port(self.l1.ports[0], self.m1.ports[1],
                         self.c1.ports[1], self.m1.ports[3])


class TcsrPower(Module):
    def __init__(self, parent, name_base, z1):
        super().__init__(parent, name_base)
        self.u1 = EdgePowerU(self, '1理想电压源', 0)
        self.r1 = ModuleImpedance(self, '2内阻', z1)

        self.add_element(self.u1, self.r1)
        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        self.u1.start.link_node(self.r1.ports[0])

    def create_port(self):
        self.config_port(self.r1.ports[1], Port(self.u1, False))


class TcsrReceiver(ModuleImpedance):
    def __init__(self, parent, name_base, z1):
        super().__init__(parent, name_base, z1)


class TcsrBA(ModuleImpedance):
    def __init__(self, parent, name_base, z1):
        super().__init__(parent, name_base, z1)

    def config_edge_para(self, freq):
        self.r1.config_parameter(self.z[freq])

    @property
    def main_freq(self):
        return self.parent.freq


class TcsrCA(Module):
    def __init__(self, parent, name_base, z1):
        super().__init__(parent, name_base)
        self.r1 = ModuleImpedance(self, '1电阻', z1)
        self.wr1 = EdgeWire(self, '2导线')

        self.add_element(self.r1, self.wr1)
        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        pass

    def create_port(self):
        self.config_port(self.r1.ports[0], Port(self.wr1, True),
                         self.r1.ports[1], Port(self.wr1, False))


class TCSRBasic(Module):
    def __init__(self, parent, name_base, para):
        super().__init__(parent, name_base)
        self.para = para
        cable_length = 10
        self.add_element(
            TcsrReceiver(
                self, '1接收器',
                para['Z_rcv'],
            ),
            TcsrFL(
                self, '2防雷变压器',
                para['FL_z1_发送端'],
                para['FL_z2_发送端'],
                para['FL_n_发送端'],
            ),
            Cable(
                self, '3电缆',
                cable_length,
                para['Cable_R'],
                para['Cable_L'],
                para['Cable_C'],
            ),
            TcsrTAD(
                self, '4TAD',
                para['TAD_z1_发送端_区间'],
                para['TAD_z2_发送端_区间'],
                para['TAD_z3_发送端_区间'],
                para['TAD_n_发送端_区间'],
                para['TAD_c_发送端_区间'],
            ),
            TcsrBA(
                self, '5PT',
                para['PT'],
            ),
            TcsrCA(
                self, '6CA',
                para['CA_z_区间'],
            ))

        self.create_circuit()
        self.create_port()

    def create_circuit(self):
        length = len(self.modules) - 1
        for index in range(length):
            m1 = self.modules[index]
            m2 = self.modules[index + 1]
            m1.ports[-2].link_node(m2.ports[0])
            m1.ports[-1].link_node(m2.ports[1])

    def create_port(self):
        self.config_port(self.modules[0].ports[0], self.modules[0].ports[1],
                         self.modules[-1].ports[-2], self.modules[-1].ports[-1])


if __name__ == '__main__':
    # 初始化变量
    path = os.getcwd() + '/BasicParameter.pkl'

    # with open('src/parameter_pkl/BasicParameter.pkl', 'rb') as pk_f:
    with open(path, 'rb') as pk_f:
        parameter = pickle.load(pk_f)

    # a = Cable(12)
    # b = Cable(15)
    # c = Edge()
    # a.ports[2].link_node(b.ports[0])
    # a.ports[3].link_node(b.ports[1])
    # m1 = Module()
    #
    # m1.add_element(a, b)
    # m1.config_port(a.ports[0])
    # m1.config_port(a.ports[1])
    # m1.config_port(b.ports[2])
    # m1.config_port(b.ports[3])
    #
    # m2 = Module()
    # m2.add_element(m1, c)
    # c.start.link_node(m1.ports[2])
    # c.end.link_node(m1.ports[3])
    # m2.config_port(m1.ports[0])
    # m2.config_port(m1.ports[1])

    md1 = TCSRBasic(None, 'tcsr_test', parameter)
    md1.config_name()

    pass