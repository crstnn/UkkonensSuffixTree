from __future__ import annotations

from UkkonensSuffixTree.alpha_dictionary import AlphaDict
from UkkonensSuffixTree.pointer_int import Pointer


class Vertex:

    def __init__(self, string_number, start_idx, end_idx):
        self.is_root: bool = False
        self.children: AlphaDict | None = None

        self.parent_edge_start_index: int = start_idx
        self._parent_edge_end_index: Pointer | int = end_idx
        self.string_number: int = string_number

        self.suffix_link: Vertex | None = None

        # only exists on leaf nodes
        self.suffix_start_index: int | None = None

    @property
    def parent_edge_end_index(self):
        if self.is_root: Exception("Do not ask for parent edge of root")
        return self._parent_edge_end_index.get_value() if self.is_leaf() else self._parent_edge_end_index

    def get_child(self, child_first_char) -> Vertex | None:
        if self.children is None or child_first_char not in self.children: return None
        return self.children[child_first_char]

    def add_child(self, child: Vertex, child_first_char: int) -> None:
        if self.children is None:
            self.children = AlphaDict()
        self.children[child_first_char] = child

    def remove_child(self, child_first_char: int) -> None:
        return self.children.pop(child_first_char)

    def is_child_present(self, child_first_char: int) -> bool:
        if self.children is None:
            return False
        return child_first_char in self.children

    def is_leaf(self) -> bool:
        return self.children is None

    def length(self) -> int:
        if self.is_root: return 0
        return self.parent_edge_end_index - self.parent_edge_start_index + 1

    def __repr__(self):
        return f'start_idx {self.parent_edge_start_index} end_idx {self.parent_edge_end_index}'

    @staticmethod
    def create_root() -> Vertex:
        root = Vertex(None, None, None)
        root.is_root = True
        root.suffix_link = root
        return root

    @staticmethod
    def create_leaf(idx: Pointer, suffix_start_index=None, string_number=None) -> Vertex:
        leaf = Vertex(string_number, idx.get_value(), idx)
        leaf.suffix_start_index = suffix_start_index
        leaf.string_number = string_number
        return leaf
