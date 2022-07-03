class Pointer:
    def __init__(self):
        self.v = -1

    def increment(self):
        self.v += 1

    def get_value(self):
        return self.v

    def set(self, value):
        self.v = value

    def __repr__(self):
        return f'GP({self.v})'
