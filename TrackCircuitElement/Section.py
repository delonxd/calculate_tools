from TrackCircuitElement.Joint import *
from TrackCircuitElement.TCSR import *

class Section:
    """

    """

    def __init__(self):
        # structure
        self.parent = None
        self.l_joint = Joint(r_par=self)
        self.r_joint = Joint(l_par=self)
        self.l_tcsr = TCSR(parent=self)
        self.r_tcsr = TCSR(parent=self)

        # parameters
        self.bas_name = None
        self.rlt_pos = None
        self.length = None
        self.freq = None

        # generated
        self.name = str()
        self.element = set()
        # self.turnout = Turnout()

    @property
    def abs_pos(self):
        return

    def load_params(self, **kw):
        if 'bas_name' in kw:
            self.bas_name = kw['bas_name']

        if 'rlt_pos' in kw:
            self.rlt_pos = kw['rlt_pos']

        if 'freq' in kw:
            self.freq = kw['freq']

        if 'length' in kw:
            self.length = kw['length']

        if 'snd_lvl' in kw:
            snd_lvl = kw['snd_lvl']
            self.l_tcsr.load_params(snd_lvl=snd_lvl)
            self.r_tcsr.load_params(snd_lvl=snd_lvl)

        if 'cable_len' in kw:
            cable_len = kw['cable_len']
            self.l_tcsr.load_params(cable_len=cable_len)
            self.r_tcsr.load_params(cable_len=cable_len)

        if 'cable_len' in kw:
            cable_len = kw['cable_len']
            self.l_tcsr.load_params(cable_len=cable_len)
            self.r_tcsr.load_params(cable_len=cable_len)

        if 'mode' in kw:
            mode = kw['mode']


class Section_Mde_Flg:
    """

    """

    def __init__(self, parent):
        self.parent = parent

class L_Snd_Mde(Section_Mde_Flg):
    """

    """


class R_Snd_Mde(Section_Mde_Flg):
    """

    """