from TrackCircuitElement.ElectricModule import ImpedanceModule
from TrackCircuitElement.BasicModule import BasicModule


class ZPW2000A_SVA(ImpedanceModule):
    """
        SVA模块
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.parameter = None

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z' in kwargs:
            self.r1.load_kw(z=kwargs['z'])


class ZPW2000A_CapC(ImpedanceModule):
    """
        补偿电容模块
    """

    def __init__(self, parent, bas_name, **kwargs):
        super().__init__(parent, bas_name)
        self.parameter = None

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        if 'z' in kwargs:
            self.r1.load_kw(z=kwargs['z'])


class ZPW2000A_TCSR_QJ_Normal(BasicModule):
    """
        2000A区间模块
    """

    def __init__(self, parent, bas_name, **kwargs):
        from TrackCircuitElement.TcsrUnit import Snd_Mde, Rcv_Mde

        super().__init__(parent, bas_name)
        # self.parameter = None

        self.power = None
        self.receiver = None
        self.fl_xfmr = None
        self.cable = None
        self.tad_xfmr = None
        self.ba = None
        self.ca = None

        if parent.mode == Snd_Mde:
            self.add_element(self.power)
        elif parent.mode == Rcv_Mde:
            self.add_element(self.receiver)
        self.add_element(self.fl_xfmr)
        self.add_element(self.cable)
        self.add_element(self.tad_xfmr)
        self.add_element(self.ba)
        self.add_element(self.ca)

        self.create_circuit()
        self.create_port()

        self.load_kw(**kwargs)

    def load_kw(self, **kwargs):
        pass
        # if 'z' in kwargs:
        #     self.r1.load_kw(z=kwargs['z'])

    def create_circuit(self):
        length = len(self.modules) - 1
        for index in range(length):
            m1 = self.modules[index]
            m2 = self.modules[index + 1]
            m1.ports[-2].link_node(m2.ports[0])
            m1.ports[-1].link_node(m2.ports[1])

    def create_port(self):
        self.config_port(self.modules[-1].ports[-2], self.modules[-1].ports[-1])
