from __future__ import annotations

from UkkonensSuffixTree.pointer_int import Pointer
from UkkonensSuffixTree.active_information import ActiveInformation
from UkkonensSuffixTree.vertex import Vertex


class SuffixTree:
    """
    Ukkonen's linear-time implicit suffix tree construction
    Accepts single strings, with the terminal character being `$` (do not use this character in input)
    """

    def __init__(self) -> None:
        self.txt_total: list = []
        self.end: Pointer | None = None
        self.ROOT: Vertex = Vertex.create_root()

    def add_to_suffix_tree(self, txt: str) -> None:
        self._do_ukkonen(txt)

    def _do_ukkonen(self, txt: str) -> None:
        self.txt_total = list(map(ord, [*txt])) + [ord("$")]  # adding terminal character
        self.end = Pointer()
        active_info = ActiveInformation(self.ROOT)
        pending_vertex = None
        last_j = -1

        txt_start_idx = len(self.txt_total) - len(txt) - 1
        for phase in range(txt_start_idx, len(self.txt_total)):
            self.end.increment()  # leaf extension
            j = last_j + 1
            while j <= phase:
                active_info = self._traverse(active_info)
                rule, active_info, pending_vertex = self._do_extension(active_info, pending_vertex, j, phase)
                if rule == 3: break  # stop prematurely
                if rule == 2: last_j += 1
                j = last_j + 1
                active_info = SuffixTree._maybe_move_to_next_extension(active_info, rule)

    def _traverse(self, active_info: ActiveInformation) -> ActiveInformation:
        # Skip-count down to the extension point

        while active_info.has_remainder():
            temp_vertex = active_info.vertex.get_child(self.txt_total[active_info.start_index])
            if temp_vertex is None or temp_vertex.length() > active_info.remainder():
                break
            active_info.vertex = temp_vertex
            active_info.increase_start_index(temp_vertex.length())

        return active_info

    def _do_extension(self, active_info: ActiveInformation, pending_vertex: Vertex, extension: int, end_idx: int) \
            -> tuple[int, ActiveInformation, None | Vertex]:

        # rule 2 - no edge split: mismatch character at start of edge
        if active_info.has_no_remainder() and not active_info.vertex.is_child_present(self.txt_total[end_idx]):
            self._add_leaf_to_internal_vertex(active_info.vertex, extension, end_idx)
            SuffixTree._maybe_add_suffix_link(pending_vertex, active_info.vertex)
            return 2, active_info, None

        # rule 2 - edge split: mismatch character between edge
        if active_info.has_remainder() and not self._do_implicit_comparison(active_info, end_idx):
            new_pending_vertex = self \
                ._do_internal_vertex_split(active_info.vertex,
                                           active_info.vertex.get_child(self.txt_total[active_info.start_index]),
                                           extension,
                                           self._get_edge_comparison_point(active_info),
                                           self._get_edge_comparison_point(active_info) - 1,
                                           end_idx)
            SuffixTree._maybe_add_suffix_link(pending_vertex, new_pending_vertex)
            return 2, active_info, new_pending_vertex

        # rule 3 - matching character on existing edge
        if (active_info.has_no_remainder() and active_info.vertex.is_child_present(self.txt_total[end_idx])) or \
                (active_info.has_remainder() and self._do_implicit_comparison(active_info, end_idx)):
            SuffixTree._maybe_add_suffix_link(pending_vertex, active_info.vertex)
            active_info.increment_end_index()
            return 3, active_info, None

    def _get_edge_comparison_point(self, active_info: ActiveInformation) -> int:
        return active_info.vertex.get_child(
            self.txt_total[active_info.start_index]).parent_edge_start_index + active_info.remainder()

    def _do_implicit_comparison(self, active_info: ActiveInformation, end_idx) -> bool:
        return self.txt_total[end_idx] == self.txt_total[self._get_edge_comparison_point(active_info)]

    @staticmethod
    def _maybe_add_suffix_link(pending_vertex: Vertex, new_vertex: Vertex) -> None:
        if pending_vertex is not None:
            pending_vertex.suffix_link = new_vertex

    @staticmethod
    def _maybe_move_to_next_extension(active_info: ActiveInformation, previous_rule: int) -> ActiveInformation:
        # Move to next extension after rule 2 i.e. traversing suffix links
        if previous_rule == 2:
            if active_info.vertex.is_root and active_info.has_remainder():
                active_info.increment_start_index()
            elif active_info.vertex.is_root and active_info.has_no_remainder():
                active_info.increment_both_indices()
            active_info.vertex = active_info.vertex.suffix_link
        return active_info

    def _do_internal_vertex_split(self, active_vertex: Vertex, child_vertex: Vertex, extension: int,
                                  mismatch_edge_idx: int, before_mismatch_char_edge_idx: int,
                                  current_txt_mismatch_idx: int) -> Vertex:
        # rule 2 normal scenario
        active_vertex.remove_child(self.txt_total[child_vertex.parent_edge_start_index])
        new_vert = Vertex(child_vertex.string_number,
                          child_vertex.parent_edge_start_index, before_mismatch_char_edge_idx)
        active_vertex.add_child(new_vert, self.txt_total[child_vertex.parent_edge_start_index])

        new_vert.add_child(child_vertex, self.txt_total[mismatch_edge_idx])
        child_vertex.parent_edge_start_index = mismatch_edge_idx

        new_vert.add_child(Vertex.create_leaf(self.end, extension), self.txt_total[current_txt_mismatch_idx])

        return new_vert

    def _add_leaf_to_internal_vertex(self, active_vertex: Vertex, extension: int, end_index: int) -> Vertex:
        # rule 2 alternative scenario
        active_vertex.add_child(Vertex.create_leaf(self.end, extension), self.txt_total[end_index])
        return active_vertex

    def _search_for_final_matching_vertex(self, search_string: str) -> Vertex | None:
        current_vertex = self.ROOT
        search_string_idx = 0
        search_string_lst = list(map(ord, [*search_string]))
        while search_string_idx < len(search_string_lst):
            current_vertex = current_vertex.get_child(search_string_lst[search_string_idx])
            if current_vertex is None:
                return None
            txt_idx = current_vertex.parent_edge_start_index
            while txt_idx <= current_vertex.parent_edge_end_index and search_string_idx < len(search_string_lst):
                if self.txt_total[txt_idx] != search_string_lst[search_string_idx]:
                    return None
                txt_idx += 1
                search_string_idx += 1
        return current_vertex

    def search_for_suffix_match(self, search_string: str):
        vertex = self._search_for_final_matching_vertex(search_string + "$")
        return None if vertex is None else vertex.parent_edge_start_index

    def search_for_match(self, search_string) -> list[int]:
        """Search for exact substring matches (not suffix matches)"""
        vertex = self._search_for_final_matching_vertex(search_string)
        visited = []
        if vertex is None: return visited

        def dfs(v):
            visited.append(v)
            if v.children is not None:
                for child in v.children:
                    dfs(child)

        dfs(vertex)
        search_string_occurrence_indices = list(map(lambda leaf: leaf.suffix_start_index,
                                                    filter(lambda v: v.is_leaf(), visited)))
        return search_string_occurrence_indices


if __name__ == "__main__":
    s1 = SuffixTree()
    s1.add_to_suffix_tree("abacabad")
    print(s1.search_for_match("aba"))
