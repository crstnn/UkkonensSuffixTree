class AlphaDict:
    ALPHA_SIZE = 128  # For 7-bit ASCII, for 8-bit increase to 256
    NUMBER_OF_STRINGS = 0

    def __init__(self):
        self.entries = [None] * (AlphaDict.ALPHA_SIZE + AlphaDict.NUMBER_OF_STRINGS)
        self.size = 0

    def __setitem__(self, key, value):
        if self.entries[AlphaDict.rank(key)] is None:
            self.size += 1
        self.entries[AlphaDict.rank(key)] = value

    def __getitem__(self, key):
        return self.entries[AlphaDict.rank(key)]

    def __delitem__(self, key):
        if self.entries[AlphaDict.rank(key)] is not None:
            self.size -= 1
        self.entries[AlphaDict.rank(key)] = None

    def __contains__(self, key):
        return self[key] is not None

    def __len__(self):
        return self.size

    def __bool__(self):
        return len(self) != 0

    def __iter__(self):
        return filter(lambda x: x is not None, self.entries)

    def pop(self, key):
        ret = self[key]
        del self[key]
        return ret

    def get_entries_greater_than_alpha_size(self):
        return filter(lambda x: x is not None, self.entries[AlphaDict.ALPHA_SIZE:])

    @staticmethod
    def rank(char):
        return char
        # return ord(char)
