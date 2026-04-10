import argparse
from index_builder import build_index, write_index_to_json, build_term_document_matrix, write_matrix_to_json


def main():
    parser = argparse.ArgumentParser(description="Build an index from a corpus.")
    parser.add_argument("--corpus", required=True, help="Path to the corpus directory.")
    parser.add_argument("--index", action="store_true", help="Build an index.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", metavar="INDEX_PATH", help="Build an inverted index and write to the given path.")
    group.add_argument("-t", metavar="INDEX_PATH", help="Build a term-document matrix and write to the given path.")

    args = parser.parse_args()

    doc_map, index, postings = build_index(args.corpus)

    if args.i:
        write_index_to_json(args.i, doc_map, index)
    elif args.t:
        matrix = build_term_document_matrix(doc_map, postings)
        write_matrix_to_json(args.t, doc_map, matrix)


if __name__ == "__main__":
    main()
