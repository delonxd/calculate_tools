from TrackCircuitElement.Joint import Joint
from TrackCircuitElement.TCSR import TCSR
from TrackCircuitElement.OutsideUnit import CapC
from TrackCircuitElement.OutsideUnit import TB
from TrackCircuitElement.TCSR import Snd_Mde, Rcv_Mde
import numpy as np


class Section:
    """
        区段
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
        self._rlt_pos = None
        self.length = None
        self.freq = None
        self.sec_type = None
        self.tb_mode = None
        self._c_nbr = None
        # self._c_num = None
        # self._c_value = None

        # generated
        self.name = str()
        # self.c_list = list()
        self.units = set()
        # self.turnout = Turnout()

        self.load_kwargs(**kwargs)

    @property
    def rlt_pos(self):
        if self.l_joint.l_par:
            sec = self.l_joint.l_par
            return sec.rlt_pos + sec.length
        elif self._rlt_pos is None:
            return 0
        else:
            return self._rlt_pos

    @property
    def abs_pos(self):
        return

    @property
    def mode(self):
        if self.l_tcsr.mode == Snd_Mde and self.r_tcsr.mode == Rcv_Mde:
            return L_Snd_Mde
        elif self.r_tcsr.mode == Snd_Mde and self.l_tcsr.mode == Rcv_Mde:
            return R_Snd_Mde
        else:
            print("Warning: '%s'区段发送接收方向异常" % self.sec_type)
            return None

    def load_kwargs(self, **kwargs):

        if 'sec_type' in kwargs:
            sec_type = kwargs['sec_type']
            if sec_type == '2000A':
                self.sec_type = ZPW2000A_STyp
            else:
                print("Warning: '%s'为不支持的区段类型" % sec_type)

        if 'tb_mode' in kwargs:
            tb_mode = kwargs['tb_mode']
            if self.sec_type == ZPW2000A_STyp:
                if tb_mode == '双端TB':
                    self.tb_mode = Two_TB_Mde
                elif tb_mode == '左端单TB':
                    self.tb_mode = L_TB_Mde
                elif tb_mode == '右端单TB':
                    self.tb_mode = R_TB_Mde
                elif tb_mode == '无TB':
                    self.tb_mode = None_TB_Mde
            else:
                print('Warning: 非2000A区段无TB模式')

        if 'bas_name' in kwargs:
            self.bas_name = kwargs['bas_name']

        if 'rlt_pos' in kwargs:
            self._rlt_pos = kwargs['rlt_pos']

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
                self.l_tcsr._mode = Snd_Mde
                self.r_tcsr._mode = Rcv_Mde
            elif sr_mode == '右发':
                self.l_tcsr._mode = Rcv_Mde
                self.r_tcsr._mode = Snd_Mde
            else:
                print("Warning: '%s'为不支持的发送接收类型" % sr_mode)

        # if 'mode' in kwargs:
        #     mode = kwargs['mode']

        if 'c_nbr' in kwargs:
            c_nbr = kwargs['c_nbr']
            self._c_nbr = kwargs['c_nbr']

    def get_element(self):
        return

    @property
    def c_tb_list(self):
        c_tb_list = list()
        for ele in self.units:
            if isinstance(ele, CapC):
                c_tb_list.append((ele.rlt_pos, ele))
        c_tb_list.sort()
        return c_tb_list

    def init_unit(self):
        if self.sec_type == ZPW2000A_STyp:
            self.sec_type.init_c(section=self, c_nbr=self._c_nbr)
            self.sec_type.init_tb(section=self)
            self.l_joint.init_unit()
            self.r_joint.init_unit()
        else:
            pass


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


class Section_Type:
    """
        区段类型
    """

    def __init__(self, parent):
        self.parent = parent


class ZPW2000A_STyp(Section_Type):
    """
        2000A电气绝缘节
    """
    def __init__(self, parent: Section):
        super().__init__(parent)
        self.tb_mode = None

    @classmethod
    def init_c(cls, section: Section, c_nbr: int):
        section.units.clear()
        l_pos = section.l_joint.length / 2
        r_pos = section.length - section.r_joint.length / 2
        hf_c_nbr = c_nbr * 2 + 1
        hf_pos = list(np.linspace(l_pos, r_pos, hf_c_nbr))
        c_pos = [hf_pos[index * 2 + 1] for index in range(c_nbr)]
        for index, pos in enumerate(c_pos):
            name = 'C' + str(index+1)
            c = CapC(section, name)
            c.load_kwargs(rlt_pos=pos)
            section.units.add(c)

    @classmethod
    def init_tb(cls, section: Section):
        tb_mode = section.tb_mode
        r_pos = section.length
        c_tb_list = section.c_tb_list
        c_nbr = len(c_tb_list)

        if tb_mode == Two_TB_Mde:
            if c_nbr < 2:
                cls.print_warning(tb_mode, c_nbr)
            else:
                section.units.discard(c_tb_list[0][1])
                section.units.discard(c_tb_list[-1][1])
                cls.add_tb(sec=section, name='左TB', pos=18)
                cls.add_tb(sec=section, name='右TB', pos=r_pos-18)

        elif tb_mode == L_TB_Mde:
            if c_nbr < 1:
                cls.print_warning(tb_mode, c_nbr)
            else:
                section.units.discard(c_tb_list[0][1])
                cls.add_tb(sec=section, name='左TB', pos=18)

        elif tb_mode == R_TB_Mde:
            if c_nbr < 1:
                cls.print_warning(tb_mode, c_nbr)
            else:
                section.units.discard(c_tb_list[-1][1])
                cls.add_tb(sec=section, name='右TB', pos=r_pos-18)

        elif tb_mode == None_TB_Mde:
            pass

    @classmethod
    def add_tb(cls, sec: Section, name, pos):
        tb = TB(sec, name)
        tb.load_kwargs(rlt_pos=pos)
        sec.units.add(tb)

    @classmethod
    def print_warning(cls, tb_mode, cap_nbr):
        text = """Warning:
            TB模式与电容数量冲突；
            TB模式：'%s'；电容数量：'%s'；
        """ % tb_mode, cap_nbr
        print(text)


class TB_Mde_Flg:
    """
        TB模式标志位
    """

    def __init__(self, parent: Section):
        self.parent = parent


class L_TB_Mde(TB_Mde_Flg):
    """
        左TB
    """


class R_TB_Mde(TB_Mde_Flg):
    """
        右TB
    """


class None_TB_Mde(TB_Mde_Flg):
    """
        无TB
    """


class Two_TB_Mde(TB_Mde_Flg):
    """
        双端TB
    """