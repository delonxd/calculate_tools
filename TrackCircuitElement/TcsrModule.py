from TrackCircuitElement.BasicModule import BasicModule
from TrackCircuitElement.ElectricModule import ImpedanceModule
from TrackCircuitElement.ElectricModule import XfmrModule
from TrackCircuitElement.ElectricModule import TCircuitModule
from TrackCircuitElement.Edge import VolSrcEdge
from TrackCircuitElement.Edge import WireEdge
from TrackCircuitElement.Port import Port


class TcsrXfmr(BasicModule):
    """
        TCSR变压器
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.m1 = TCircuitModule(self, '1等效内阻')
        self.m2 = XfmrModule(self, '2理想变压器')

        self.add_element(self.m1, self.m2)
        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z1' in kwargs:
            self.m1.load_kw(z1=kwargs['z1'])

        if 'z2' in kwargs:
            self.m1.load_kw(z2=kwargs['z2'])

        if 'z3' in kwargs:
            self.m1.load_kw(z3=kwargs['z3'])

        if 'n' in kwargs:
            self.m2.load_kw(n=kwargs['n'])

    def create_circuit(self):
        self.m1.ports[2].link_node(self.m2.ports[0])
        self.m1.ports[3].link_node(self.m2.ports[1])

    def create_port(self):
        self.config_port(self.m1.ports[0], self.m1.ports[1],
                         self.m2.ports[2], self.m2.ports[3])


class TcsrFLXfmr(TcsrXfmr):
    """
        防雷变压器
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z1' in kwargs:
            self.m1.load_kw(z1=kwargs['z1'], z3=kwargs['z1'])

        if 'z2' in kwargs:
            self.m1.load_kw(z2=kwargs['z2'])

        if 'n' in kwargs:
            self.m2.load_kw(n=kwargs['n'])


class TcsrTADXfmr(BasicModule):
    """
        TAD变压器
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.l1 = ImpedanceModule(self, '1共模电感')
        self.m1 = TcsrXfmr(self, '2变压器')
        self.c1 = ImpedanceModule(self, '3电容')

        self.add_element(self.l1, self.m1, self.c1)
        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z1' in kwargs:
            self.m1.load_kw(z1=kwargs['z1'], z3=kwargs['z1'])

        if 'z2' in kwargs:
            self.m1.load_kw(z2=kwargs['z2'])

        if 'n' in kwargs:
            self.m1.load_kw(n=kwargs['n'])

        if 'n' in kwargs:
            self.l1.load_kw(z=kwargs['z3'])

        if 'zc' in kwargs:
            self.m1.load_kw(z=kwargs['zc'])


    def create_circuit(self):
        self.l1.ports[1].link_node(self.m1.ports[0])
        self.c1.ports[0].link_node(self.m1.ports[2])

    def create_port(self):
        self.config_port(self.l1.ports[0], self.m1.ports[1],
                         self.c1.ports[1], self.m1.ports[3])


class TcsrPower(BasicModule):
    """
        功出电源
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.u1 = VolSrcEdge(self, '1理想电压源')
        self.r1 = ImpedanceModule(self, '2内阻')

        self.add_element(self.u1, self.r1)
        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z1' in kwargs:
            self.r1.load_kw(z=kwargs['z1'])

    def create_circuit(self):
        self.u1.start.link_node(self.r1.ports[0])

    def create_port(self):
        self.config_port(self.r1.ports[1], Port(self.u1, False))


class TcsrReceiver(ImpedanceModule):
    """
        接收器
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.load_kw(**kwargs)


class TcsrBA(ImpedanceModule):
    """
        匹配单元
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.load_kw(**kwargs)

    def config_edge_para(self, freq):
        self.r1.config_parameter(self.z[freq])

    @property
    def main_freq(self):
        return self.parent.freq


class TcsrCA(BasicModule):
    """
        引接线
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.r1 = ImpedanceModule(self, '1电阻')
        self.wr1 = WireEdge(self, '2导线')

        self.add_element(self.r1, self.wr1)
        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z' in kwargs:
            self.r1.load_kw(z=kwargs['z'])

    def create_circuit(self):
        pass

    def create_port(self):
        self.config_port(self.r1.ports[0], Port(self.wr1, True),
                         self.r1.ports[1], Port(self.wr1, False))
