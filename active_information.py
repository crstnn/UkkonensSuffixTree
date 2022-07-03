from UkkonensSuffixTree.vertex import Vertex


class ActiveInformation:
    def __init__(self, active_vertex: Vertex):
        self.vertex: Vertex = active_vertex
        self.start_index: int = 0
        self.end_index: int = 0

    def increment_start_index(self):
        self.start_index += 1

    def increase_start_index(self, amount):
        self.start_index += amount

    def increment_end_index(self):
        self.end_index += 1

    def increment_both_indices(self):
        self.increment_start_index()
        self.increment_end_index()

    def remainder(self):
        return self.end_index - self.start_index

    def has_no_remainder(self):
        return self.start_index == self.end_index

    def has_remainder(self):
        return self.start_index != self.end_index
