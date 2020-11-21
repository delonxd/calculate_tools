class TCSR:
    """
        发送接收单元
    """

    def __init__(self, parent):

        self._bas_name = parent

        # parameters
        self._bas_name = None
        self.snd_lvl = None
        self.rcv_lvl = None
        self._mode = None
        self.cable_len = None
        self.module = None

        # generated
        self.name = str()
        # self.sub_object = set()

    @property
    def bas_name(self):
        from TrackCircuitElement.Section import Section
        from TrackCircuitElement.Joint import Joint

        if self._bas_name:
            return self._bas_name
        elif isinstance(self.parent, Section):
            if self == self.parent.l_tcsr:
                return '左侧TCSR'
            elif self == self.parent.r_tcsr:
                return '右侧TCSR'
            else:
                return
        return

    @property
    def mode(self):
        return self._mode

    @property
    def rlt_pos(self):
        from TrackCircuitElement.Section import Section
        from TrackCircuitElement.Joint import Joint

        if isinstance(self.parent, Section):
            if self == self.parent.l_tcsr:
                return 0 + self.parent.l_joint.length/2
            elif self == self.parent.r_tcsr:
                return self.parent.length - self.parent.r_joint.length/2
            else:
                return
        return

    @property
    def abs_pos(self):
        return

    def load_kwargs(self, **kwargs):

        if 'bas_name' in kwargs:
            self._bas_name = kwargs['bas_name']

        if 'snd_lvl' in kwargs:
            self.snd_lvl = kwargs['snd_lvl']

        if 'rcv_lvl' in kwargs:
            self.rcv_lvl = kwargs['rcv_lvl']

        if 'mode' in kwargs:
            self._mode = kwargs['mode']

        if 'cable_len' in kwargs:
            self.cable_len = kwargs['cable_len']


class TCSR_Mde_Flg:
    """

    """

    def __init__(self, parent):
        self.parent = parent


class Snd_Mde(TCSR_Mde_Flg):
    """

    """


class Rcv_Mde(TCSR_Mde_Flg):
    """

    """


class TCSR_Type_Flg:
    """

    """

    def __init__(self, parent):
        self.parent = parent


class ZPW2000A_TCSR_QJ(TCSR_Type_Flg):
    """

    """

class ZPW2000A_TCSR_QJ(TCSR_Type_Flg):
    """

    """