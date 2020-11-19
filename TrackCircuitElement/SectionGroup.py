from TrackCircuitElement.Section import *

class SectionGroup:
    """

    """

    def __init__(self, parent, **kw):
        # structure
        self.parent = parent

        # parameters
        self.bas_name = None
        self.rlt_pos = None
        self.sec_list = list()
        self.turnout_list = list()

        # generated
        self.name = str()
        self.element = set()

        if 'm_nbr' in kw:
            self.sec_list.clear()
            self.add_sections()

    @property
    def abs_pos(self):
        return

    def add_sections(self, number):
        for _ in range(number):
            self.add_section()

    def add_section(self):
        self.sec_list.append(Section())

    def load_params(self, **kw):
        if 'm_nbr' in kw:
            self.sec_list.clear()
            self.add_sections()

        if 'bas_name' in kw:
            self.bas_name = kw['bas_name']

        if 'rlt_pos' in kw:
            self.rlt_pos = kw['rlt_pos']

        if 'm_freqs' in kw:
            m_freqs = kw['m_freqs']
            for index, section in enumerate(self.sec_list):
                section.load_params(freq=m_freqs[index])

        if 'm_lens' in kw:
            m_lens = kw['m_lens']
            for index, section in enumerate(self.sec_list):
                section.load_params(length=m_lens[index])

        if 'j_lens' in kw:
            j_lens = kw['j_lens']
            for index, section in enumerate(self.sec_list):
                lens = [j_lens[index], j_lens[index+1]]
                section.load_params(j_lens=lens[index])

        if 'snd_lvl' in kw:
            snd_lvl = kw['snd_lvl']
            for section in self.sec_list:
                section.load_params(snd_lvl=snd_lvl)

        if 'section_mde' in kw:
            sec_params = kw['sec_params']
            for section in self.sec_list:
                pass

