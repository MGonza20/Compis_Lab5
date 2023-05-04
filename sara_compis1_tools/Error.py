
class Error:
    def __init__(self, line, error, position=None):
        self.line = line
        self.error = error
        self.position = position