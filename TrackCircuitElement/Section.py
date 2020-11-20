from TrackCircuitElement.Joint import Joint
from TrackCircuitElement.TCSR import TCSR
# from TrackCircuitElement.OutsideElement import CapC
from TrackCircuitElement.TCSR import Snd_Mde, Rcv_Mde

class Section:
    """

    """

    def __init__(self, parent, bas_name, **kwargs):
        # structure
        self.parent = parent
        self.l_joint = Joint(r_par=self)
        self.r_joint = Joint(l_par=self)
        self.l_tcsr = TCSR(parent=self)
        self.r_tcsr = TCSR(parent=self)

        # parameters
        self.bas_name = bas_name
        self.rlt_pos = None
        self.length = None
        self.freq = None

        # generated
        self.name = str()
        self.c_list = list()
        self.element = set()
        # self.turnout = Turnout()

        self.load_kwargs(**kwargs)

    @property
    def abs_pos(self):
        return

    @property
    def mode(self):
        if isinstance(self.l_tcsr.mode, Snd_Mde) and isinstance(self.r_tcsr.mode, Rcv_Mde):
            return L_Snd_Mde(self)
        elif isinstance(self.r_tcsr.mode, Snd_Mde) and isinstance(self.l_tcsr.mode, Rcv_Mde):
            return R_Snd_Mde(self)
        else:
            return None

    def load_kwargs(self, **kwargs):

        if 'bas_name' in kwargs:
            self.bas_name = kwargs['bas_name']

        if 'rlt_pos' in kwargs:
            self.rlt_pos = kwargs['rlt_pos']

        if 'freq' in kwargs:
            self.freq = kwargs['freq']

        if 'length' in kwargs:
            self.length = kwargs['length']

        if 'snd_lvl' in kwargs:
            snd_lvl = kwargs['snd_lvl']
            self.l_tcsr.load_kwargs(snd_lvl=snd_lvl)
            self.r_tcsr.load_kwargs(snd_lvl=snd_lvl)

        if 'cable_len' in kwargs:
            cable_len = kwargs['cable_len']
            self.l_tcsr.load_kwargs(cable_len=cable_len)
            self.r_tcsr.load_kwargs(cable_len=cable_len)

        if 'j_lens' in kwargs:
            j_lens = kwargs['j_lens']
            self.l_joint.load_kwargs(length=j_lens[0])
            self.r_joint.load_kwargs(length=j_lens[1])

        if 'sr_mode' in kwargs:
            sr_mode = kwargs['sr_mode']
            if sr_mode == '左发':
                self.l_tcsr._mode = Snd_Mde(self.l_tcsr)
                self.r_tcsr._mode = Rcv_Mde(self.r_tcsr)
            elif sr_mode == '右发':
                self.l_tcsr._mode = Rcv_Mde(self.l_tcsr)
                self.r_tcsr._mode = Snd_Mde(self.r_tcsr)

        if 'mode' in kwargs:
            mode = kwargs['mode']

        if 'c_nbr' in kwargs:
            self.c_list.clear()
            # self.add_sections(kwargs['m_nbr'])

    def get_element(self):
        return

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