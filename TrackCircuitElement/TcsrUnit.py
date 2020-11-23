from TrackCircuitElement.Unit import Unit
from TrackCircuitElement.OutsideModule import ZPW2000A_TCSR_QJ_Normal


class TcsrUnit(Unit):
    """
        发送接收单元
    """

    def __init__(self, parent):
        super().__init__(parent)
        # structure
        # self.parent = parent

        # parameters
        # self._bas_name = None
        self.snd_lvl = None
        self.rcv_lvl = None
        self._mode = None
        self.cable_len = None

    @property
    def bas_name(self):
        from TrackCircuitElement.Section import Section

        if isinstance(self.parent, Section):
            if self == self.parent.l_tcsr:
                return '左侧TCSR'
            elif self == self.parent.r_tcsr:
                return '右侧TCSR'
        if self._bas_name is None:
            return ''
        else:
            return self._bas_name

    @property
    def mode(self):
        return self._mode

    @property
    def rlt_pos(self):
        from TrackCircuitElement.Section import Section

        if isinstance(self.parent, Section):
            if self == self.parent.l_tcsr:
                return 0 + self.parent.l_joint.length/2
            elif self == self.parent.r_tcsr:
                return self.parent.length - self.parent.r_joint.length/2
        if self._rlt_pos is None:
            return 0
        else:
            return self._rlt_pos

    # @property
    # def abs_pos(self):
    #     if self.parent is None:
    #         return self.rlt_pos
    #     else:
    #         pos = self.parent.rlt_pos + self.rlt_pos
    #         return pos

    @property
    def connect_joint(self):
        if self == self.parent.l_tcsr:
            return self.parent.l_joint
        elif self == self.parent.r_tcsr:
            return self.parent.r_joint
        else:
            return

    @property
    def md_type(self):
        from TrackCircuitElement.Section import ZPW2000A_STyp
        from TrackCircuitElement.Joint import Electric_2000A_JTyp, Mechanical_JTyp

        sec = self.parent
        jnt = self.connect_joint

        text = "Warning: 区段类型：'%r'；绝缘节类型：'%r'；无法设置TCSR类型"\
               % (sec.sec_type, jnt.j_type)

        if sec.sec_type == ZPW2000A_STyp:
            if jnt.j_type == Electric_2000A_JTyp:
                return ZPW2000A_TCSR_QJ_Normal
            elif jnt.j_type == Mechanical_JTyp:
                # return ZPW2000A_TCSR_ZN_PTSVA_Plus
                return
            else:
                print(text)
                return
        else:
            print(text)
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
