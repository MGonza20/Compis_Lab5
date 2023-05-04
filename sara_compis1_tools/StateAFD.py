
class StateAFD:

    def __init__(self, name, transitions, start=False, accepting=False, value=None):
        self.name = name
        self.transitions = transitions
        self.accepting = accepting
        self.start = start
        self.value = value