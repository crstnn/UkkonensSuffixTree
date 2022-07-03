import sys

from generalised_suffix_tree import GeneralisedSuffixTree


def main() -> None:
    """
    Command line version of Ukkonen's
    """
    file_name: str = sys.argv[1]
    inp_lst = []

    with open(file_name) as file:
        while line := file.readline():
            inp_lst.append(line.rstrip("\n").split(" "))

    number_of_text_files = int(inp_lst.pop(0)[0])
    number_of_pattern_files = int(inp_lst.pop(number_of_text_files)[0])

    text_files = inp_lst[:number_of_text_files]
    pattern_files = inp_lst[number_of_text_files:]

    all_text_lst = [None] * number_of_text_files
    all_pattern_lst = [None] * number_of_pattern_files

    def read_by_line(files, lst):
        for line in files:
            with open(line[1]) as f:
                lst[int(line[0])-1] = f.read()

    read_by_line(text_files, all_text_lst)
    read_by_line(pattern_files, all_pattern_lst)


    all_text_lst = list(map(lambda x: x.lower(), all_text_lst))
    all_pattern_lst = list(map(lambda x: x.lower(), all_pattern_lst))

    gst = GeneralisedSuffixTree(number_of_text_files)

    for n, txt in enumerate(all_text_lst):
        gst.add_to_suffix_tree(txt, n)

    gst_triplets = []
    for n, pat in enumerate(all_pattern_lst):
        for pair in gst.search_for_match(pat):
            gst_triplets.append((n, *pair))

    gst_triplets_one_indexed = list(map(lambda t: tuple(map(lambda x: x+1, t)), gst_triplets))

    with open("output_gst.txt", "w") as output_file:
        output_file.writelines("{}\n".format(' '.join(map(str, el))) for el in gst_triplets_one_indexed)


if __name__ == "__main__":
    main()
