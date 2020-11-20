from TrackCircuitElement.BasicModule import BasicModule
from TrackCircuitElement.Port import Port
from TrackCircuitElement.Edge import *

import numpy as np

class ImpedanceModule(BasicModule):
    """
        阻抗模块
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self._z = None
        self.r1 = ImpedanceEdge(self, 'Edge')

        self.add_element(self.r1)

        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z' in kwargs:
            self._z = kwargs['z']

    @property
    def z(self):
        return self._z

    def create_circuit(self):
        pass

    def create_port(self):
        self.config_port(Port(self.r1, True), Port(self.r1, False))

    def config_edge_param(self, freq):
        self.r1.config_param(self.z[freq])


class CableModule(BasicModule):
    """
        电缆模块
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self._R = None
        self._L = None
        self._C = None
        self._length = None

        self.r1 = ImpedanceEdge(self, 'R1')
        self.r2 = ImpedanceEdge(self, 'R2')
        self.rp1 = ImpedanceEdge(self, 'Rp1')
        self.rp2 = ImpedanceEdge(self, 'Rp2')
        self.add_element(self.r1, self.r2, self.rp1, self.rp2)

        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'R' in kwargs:
            self._R = kwargs['R']

        if 'L' in kwargs:
            self._L = kwargs['L']

        if 'C' in kwargs:
            self._C = kwargs['C']

        if 'length' in kwargs:
            self._length = kwargs['length']

    @property
    def length(self):
        return self._length

    @property
    def R(self):
        return self._R

    @property
    def L(self):
        return self._L

    @property
    def C(self):
        return self._C

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

        self.r1.config_param(zii/2)
        self.r2.config_param(zii/2)
        self.rp1.config_param(1/yii)
        self.rp2.config_param(1/yii)


class XfmrModule(BasicModule):
    """
        理想变压器模块
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self._n = None
        self.w1 = WindingEdge(self, '1原边')
        self.w2 = WindingEdge(self, '2副边')
        self.add_element(self.w1, self.w2)

        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'n' in kwargs:
            self._n = kwargs['n']

    @property
    def n(self):
        return self._n

    def create_circuit(self):
        pass

    def create_port(self):
        self.config_port(Port(self.w1, True), Port(self.w1, False),
                         Port(self.w2, True), Port(self.w2, False))

    def config_edge_para(self, freq):
        self.w1.config_param(self.w2, self.n)
        self.w2.config_param(self.w1, 1 / self.n)
        # self.w1.source = True
        # self.w2.source = False


class PiCircuitModule(BasicModule):
    """
        Pi型二端口网络
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.r1 = ImpedanceModule(self, 'R1')
        self.r2 = ImpedanceModule(self, 'R2')
        self.r3 = ImpedanceModule(self, 'R3')
        self.add_element(self.r1, self.r2, self.r3)

        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z1' in kwargs:
            self.r1.load_kw(z=kwargs['z1'])

        if 'z2' in kwargs:
            self.r2.load_kw(z=kwargs['z2'])

        if 'z3' in kwargs:
            self.r3.load_kw(z=kwargs['z3'])

    @property
    def z1(self):
        return self.r1.z

    @property
    def z2(self):
        return self.r2.z

    @property
    def z3(self):
        return self.r3.z

    def create_circuit(self):
        self.r1.ports[0].link_node(self.r2.ports[0])
        self.r2.ports[1].link_node(self.r3.ports[0])
        self.r1.ports[1].link_node(self.r3.ports[1])

    def create_port(self):
        self.config_port(self.r1.ports[0], self.r2.ports[1],
                         self.r3.ports[0], self.r3.ports[1])


class TCircuitModule(BasicModule):
    """
        T型二端口网络
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.r1 = ImpedanceModule(self, 'R1')
        self.r2 = ImpedanceModule(self, 'R2')
        self.r3 = ImpedanceModule(self, 'R3')
        self.add_element(self.r1, self.r2, self.r3)

        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z1' in kwargs:
            self.r1.load_kw(z=kwargs['z1'])

        if 'z2' in kwargs:
            self.r2.load_kw(z=kwargs['z2'])

        if 'z3' in kwargs:
            self.r3.load_kw(z=kwargs['z3'])

    @property
    def z1(self):
        return self.r1.z

    @property
    def z2(self):
        return self.r2.z

    @property
    def z3(self):
        return self.r3.z

    def create_circuit(self):
        self.r1.ports[1].link_node(self.r3.ports[0])
        self.r1.ports[1].link_node(self.r2.ports[0])

    def create_port(self):
        self.config_port(self.r1.ports[0], self.r2.ports[1],
                         self.r3.ports[1], self.r2.ports[1])
