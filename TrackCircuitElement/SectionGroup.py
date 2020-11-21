from TrackCircuitElement.Section import Section


class SectionGroup:
    """
        区段组
    """

    def __init__(self, parent, **kwargs):
        """structure"""
        self.parent = parent

        """parameters"""
        self.bas_name = None
        self.rlt_pos = None
        self.sec_list = list()
        self.turnout_list = list()

        """generated"""
        self.name = str()
        self.units = set()

        # if 'm_nbr' in kwargs:
        #     self.sec_list.clear()
        #     self.add_sections(kwargs['m_nbr'])

        self.load_kwargs(**kwargs)

    @property
    def abs_pos(self):
        return

    def add_sections(self, number):
        for i in range(number):
            bas_name = '区段' + str(i + 1)
            self.add_section(bas_name)

    def add_section(self, bas_name):
        self.sec_list.append(Section(parent=self, bas_name=bas_name))

    def load_kwargs(self, **kwargs):
        if 'm_nbr' in kwargs:
            self.sec_list.clear()
            self.add_sections(kwargs['m_nbr'])

        if 'sec_type' in kwargs:
            sec_type = kwargs['sec_type']
            for index, section in enumerate(self.sec_list):
                section.load_kwargs(sec_type=sec_type)

        if 'bas_name' in kwargs:
            self.bas_name = kwargs['bas_name']

        if 'rlt_pos' in kwargs:
            self.rlt_pos = kwargs['rlt_pos']

        if 'm_freqs' in kwargs:
            m_freqs = kwargs['m_freqs']
            for index, section in enumerate(self.sec_list):
                section.load_kwargs(freq=m_freqs[index])

        if 'm_lens' in kwargs:
            m_lens = kwargs['m_lens']
            for index, section in enumerate(self.sec_list):
                section.load_kwargs(length=m_lens[index])

        if 'j_lens' in kwargs:
            j_lens = kwargs['j_lens']
            for index, section in enumerate(self.sec_list):
                lens = [j_lens[index], j_lens[index + 1]]
                section.load_kwargs(j_lens=lens)

        if 'snd_lvl' in kwargs:
            snd_lvl = kwargs['snd_lvl']
            for section in self.sec_list:
                section.load_kwargs(snd_lvl=snd_lvl)

        if 'cable_len' in kwargs:
            cable_len = kwargs['cable_len']
            for section in self.sec_list:
                section.load_kwargs(cable_len=cable_len)

        if 'sr_mode' in kwargs:
            sr_mode = kwargs['sr_mode']
            for section in self.sec_list:
                section.load_kwargs(sr_mode=sr_mode)

        if 'c_nbrs' in kwargs:
            c_nbrs = kwargs['c_nbrs']
            for index, section in enumerate(self.sec_list):
                section.load_kwargs(c_nbr=c_nbrs[index])


        if 'section_mde' in kwargs:
            sec_params = kwargs['sec_params']
            for section in self.sec_list:
                pass


if __name__ == '__main__':
    sg1 = SectionGroup(
        parent=None,
        bas_name='地面',
        rlt_pos=30,
        m_nbr=1,
        m_freqs=[1750],
        m_lens=[650],
        j_lens=[20, 50],
        sec_type='2000A',
        c_nbrs=[7],
        sr_mode='左发',
        snd_lvl=1,
        cable_len=10,
        # parameter=parameter,
    )

    pass
