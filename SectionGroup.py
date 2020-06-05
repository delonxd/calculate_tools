import numpy as np
import time
import itertools
import os
import sys
import pickle


class OutsideConcept:
    def __init__(self, parent, rlt_pst):
        self.parent = parent
        self.rlt_pst = rlt_pst


class GroupInfo:
    def __init__(self, rlt_pst, para,
                 s_num, freqs, s_lens, j_lens, s_types,
                 c_nums, sr_mods, send_lvs):
        self.rlt_pst = rlt_pst
        self.para = para
        self.s_num = s_num
        self.freqs = freqs
        self.s_lens = s_lens
        self.j_lens = j_lens
        self.s_types = s_types
        self.c_nums = c_nums
        self.sr_mods = sr_mods
        self.send_lvs = send_lvs
        self.j_types = ['电气' if value > 0 else '机械' for value in j_lens]


class SectionGroup:
    def __init__(self, group_info):
        self.rlt_pst = group_info.rlt_pst
        self.para = group_info.para
        self.element = dict()
        self.config_section(self.get_sec_info(group_info))

    @staticmethod
    def get_sec_info(g_info):
        sec_info = list()
        rlt_pst = 0
        for num in range(g_info.s_num):
            name = '区段' + str(num+1)
            info = SectionInfo(
                name_base=name,
                rlt_pst=rlt_pst,
                freq=g_info.freqs[num],
                s_type=g_info.s_types[num],
                s_len=g_info.s_lens[num],
                j_len=[g_info.j_lens[num], g_info.j_lens[num+1]],
                c_num=g_info.c_nums[num],
                j_type=[g_info.j_types[num], g_info.j_types[num+1]],
                sr_mod=g_info.sr_mods[num],
                send_lv=g_info.send_lvs[num],
            )
            sec_info.append(info)
            rlt_pst += info.s_length
        return sec_info

    def config_section(self, sec_info):
        for info in sec_info:
            self.element[info.name_base] = Section(self, info)


class SectionInfo:
    def __init__(self, name_base, rlt_pst,
                 freq, s_type, s_len, j_len, c_num,
                 j_type, sr_mod, send_lv):
        self.name_base = name_base
        self.rlt_pst = rlt_pst
        self.freq = freq
        self.s_type = s_type
        self.s_length = s_len
        self.j_length = j_len
        self.c_num = c_num
        self.j_type = j_type
        self.sr_mod = sr_mod
        self.send_lv = send_lv
        self.j_cls = list()
        self.config_j_cls()

    def config_j_cls(self):
        self.j_cls = list()
        s_type = self.s_type
        for value in self.j_type:
            if not value == '电气' and not value == '机械':
                raise KeyboardInterrupt("绝缘节类型异常：必须为'电气'或'机械'")

            elif s_type == '2000A':
                if value == '电气':
                    self.j_cls.append('Joint_2000A_Electric')
                elif value == '机械':
                    self.j_cls.append('Joint_Mechanical')

            elif s_type == '2000A_YPMC':
                if value == '电气':
                    raise KeyboardInterrupt('2000A移频脉冲不支持电气绝缘节')
                elif value == '机械':
                    self.j_cls.append('Joint_Mechanical')

            elif s_type == '2000A_Belarus':
                if value == '电气':
                    self.j_cls.append('Joint_2000A_Electric_Belarus')
                elif value == '机械':
                    raise KeyboardInterrupt('2000A白俄暂不支持机械绝缘节')

            elif s_type == '2000A_BPLN':
                if value == '电气':
                    raise KeyboardInterrupt('2000A_BPLN不支持电气绝缘节')
                elif value == '机械':
                    self.j_cls.append('Joint_Mechanical')

            elif s_type == '2000A_25Hz_Coding':
                if value == '电气':
                    raise KeyboardInterrupt('2000A_25Hz_Coding不支持电气绝缘节')
                elif value == '机械':
                    self.j_cls.append('Joint_Mechanical')


class Section:
    def __init__(self, parent, info):
        self.parent = parent
        self.name_base = info.name_base
        self.rlt_pst = info.rlt_pst
        self.turnout = list()
        self.straight = StraightTrack(self, info)
        self.freq = info.freq
        self.type = info.s_type


class SectionZPW2000A_YPMC(Section):
    def __init__(self, parent, info):
        super().__init__(parent, info)


class SectionZPW2000A_Belarus(Section):
    def __init__(self, parent, info):
        super().__init__(parent, info)


class SectionZPW2000A_BPLN(Section):
    def __init__(self, parent, info):
        super().__init__(parent, info)


class SectionZPW2000A_25Hz_Coding(Section):
    def __init__(self, parent, info):
        super().__init__(parent, info)


class StraightTrack:
    def __init__(self, parent, info):
        self.parent = parent
        self.rlt_pst = 0
        self.s_length = info.s_length
        self.element = dict()
        self.l_joint = None
        self.r_joint = None
        self.config_joint(info)
        self.config_c(info.c_num)

    def config_joint(self, info):
        cls = info.j_cls
        print(cls)
        self.l_joint = Joint(self, info, '左')
        self.r_joint = Joint(self, info, '右')

    @property
    def type(self):
        return self.parent.type

    @property
    def left_tcsr(self):
        return self.l_joint.r_tcsr

    @property
    def right_tcsr(self):
        return self.r_joint.l_tcsr

    def config_c(self, c_num):
        left = self.l_joint.r_pst
        right = self.s_length + self.r_joint.l_pst
        num = c_num * 2 + 1
        hlf_pst = list(np.linspace(left, right, num))
        c_pst = [hlf_pst[num * 2 + 1] for num in range(c_num)]

        for num in range(len(c_pst)):
            c_name = 'C' + str(num + 1)
            # ele = CapC(parent_ins=self,
            #            name_base=c_name,
            #            posi=c_pst[num],
            #            z=self.parameter['Ccmp_z'])
            # self.add_child(c_name, ele)


class Joint:
    def __init__(self, parent, info, flag):
        self.parent = parent
        self.l_track = None
        self.r_track = None
        self.l_tcsr = None
        self.r_tcsr = None
        self.element = dict()

        if flag == '左':
            self.l_pst = -info.j_length[0]/2
            self.r_pst = info.j_length[0]/2
            self.r_track = parent
        if flag == '右':
            self.l_pst = -info.j_length[1]/2
            self.r_pst = info.j_length[1]/2
            self.l_track = parent

    def config_tcsr(self):
        pass

    def config_joint(self):
        pass


class JointMechanical(Joint):
    def __init__(self, parent, info, flag):
        super().__init__(parent, info, flag)


class JointElectric2000A(Joint):
    def __init__(self, parent, info, flag):
        super().__init__(parent, info, flag)
        self.config_sva()

    def config_sva(self):
        pass


if __name__ == '__main__':
    # 初始化变量
    path = os.getcwd() + '/BasicParameter.pkl'

    # with open('src/parameter_pkl/BasicParameter.pkl', 'rb') as pk_f:
    with open(path, 'rb') as pk_f:
        parameter = pickle.load(pk_f)

    inf1 = GroupInfo(rlt_pst=0, para=parameter,
                     s_num=3,
                     freqs=[1700, 2300, 1700],
                     s_lens=[600] * 3,
                     j_lens=[29] * 4,
                     # m_typs=['2000A_BPLN']*3,
                     s_types=['2000A'] * 3,
                     c_nums=[5, 6, 7],
                     sr_mods=['左发'] * 3,
                     send_lvs=[5] * 3)
    sg = SectionGroup(inf1)

    pass
