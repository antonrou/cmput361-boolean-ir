import argparse
from index_builder import build_index, write_index_to_json, build_term_document_matrix, write_matrix_to_json
from query_engines.boolean import main as boolean_query_main


def main():
    parser = argparse.ArgumentParser(description="Build an index from a corpus.")
    parser.add_argument("--corpus", required=False, help="Path to the corpus directory.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", metavar="INDEX_PATH", help="Build an inverted index and write to the given path.")
    group.add_argument("-t", metavar="INDEX_PATH", help="Build a term-document matrix and write to the given path.")
    group.add_argument("-qb", nargs=2, metavar=("INDEX_PATH", "QUERY"), help="Write a boolean query.")

    args = parser.parse_args()
    if args.i or args.t:
        doc_map, index, postings = build_index(args.corpus)
        if args.i:
            write_index_to_json(args.i, doc_map, index)
        elif args.t:
            matrix = build_term_document_matrix(doc_map, postings)
            write_matrix_to_json(args.t, doc_map, matrix)
    elif args.qb:
        results = boolean_query_main(args.qb[0], args.qb[1])
        for filename in results:            
          print(filename)



if __name__ == "__main__":
    main()
