from TrackCircuitElement.Joint import Joint
from TrackCircuitElement.TcsrUnit import TcsrUnit
from TrackCircuitElement.OutsideUnit import CapC
from TrackCircuitElement.TcsrUnit import Snd_Mde, Rcv_Mde
import numpy as np


class Section:
    """

    """

    def __init__(self, parent, bas_name, **kwargs):
        """structure"""
        self.parent = parent
        self.l_joint = Joint(r_par=self)
        self.r_joint = Joint(l_par=self)
        self.l_tcsr = TcsrUnit(parent=self)
        self.r_tcsr = TcsrUnit(parent=self)

        """parameters"""
        self.bas_name = bas_name
        self.rlt_pos = None
        self.length = None
        self.freq = None
        self.sec_type = None
        # self._c_num = None
        # self._c_value = None

        """generated"""
        self.name = str()
        # self.c_list = list()
        self.units = set()
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

        if 'sec_type' in kwargs:
            sec_type = kwargs['sec_type']
            if sec_type == '2000A':
                self.sec_type = ZPW2000A_STyp(self)
            else:
                print("Warning: '%s'为不支持的区段类型" % sec_type)

        if 'tb_mode' in kwargs:
            tb_mode = kwargs['tb_mode']
            if isinstance(self.sec_type, ZPW2000A_STyp):
                if tb_mode == '双端TB':
                    self.sec_type.tb_mode = Two_TB_Mde(self)
                elif tb_mode == '左端单TB':
                    self.sec_type.tb_mode = L_TB_Mde(self)
                elif tb_mode == '右端单TB':
                    self.sec_type.tb_mode = R_TB_Mde(self)
                elif tb_mode == '无TB':
                    self.sec_type.tb_mode = None_TB_Mde(self)
            else:
                print('Warning: 非2000A区段无TB模式')

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
            else:
                print("Warning: '%s'为不支持的发送接收类型" % sr_mode)

        # if 'mode' in kwargs:
        #     mode = kwargs['mode']

        if 'c_nbr' in kwargs:
            c_nbr = kwargs['c_nbr']
            if isinstance(self.sec_type, ZPW2000A_STyp):
                self.sec_type.set_c(c_nbr=c_nbr)
            else:
                print("Warning: '%s'区段类型无法设置电容数" % self.sec_type)

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

    def set_unit(self):
        unit = None
        self.parent.units.clear()
        self.parent.addunit(unit)

    def set_c(self, c_nbr):
        l_pos = self.parent.l_joint.length / 2
        r_pos = self.parent.length - self.parent.r_joint.length / 2
        hf_c_nbr = c_nbr * 2 + 1
        hf_pos = list(np.linspace(l_pos, r_pos, hf_c_nbr))
        c_pos = [hf_pos[index * 2 + 1] for index in range(c_nbr)]
        for index, pos in enumerate(c_pos):
            name = 'C' + str(index+1)
            c = CapC(self.parent, name)
            c.load_kwargs(rlt_pos=pos)
            self.parent.units.add(c)


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