from TrackCircuitElement.Variable import Variable


class Node:
    """
        节点
    """

    def __init__(self):
        self.edges = list()
        self.variable = Variable()
        self.variable_type = 'U'
        self.zero = False
