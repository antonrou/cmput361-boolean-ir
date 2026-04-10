import os
import json
from preprocesser import preprocess


def write_index_to_json(index_path, doc_map, index):
    data = {
        'documents': doc_map,
        'index': index
    }
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def get_document_map(corpus_path):
    # Get all .txt files in the corpus folder, sorted for consistency
    all_files = os.listdir(corpus_path)
    txt_files = [f for f in all_files if f.endswith('.txt')]
    files = sorted(txt_files)

    # Map integer IDs to filenames
    doc_map = {}
    for i, fname in enumerate(files):
        doc_map[i + 1] = fname

    return doc_map


def collect_all_postings(corpus_path, doc_map):
    postings = []
    for doc_id, fname in doc_map.items():
        with open(os.path.join(corpus_path, fname), 'r', encoding='utf-8') as f:
            text = f.read()
        tokens = preprocess(text)
        for position, token in enumerate(tokens, start=1):
            postings.append((token, doc_id, position))
    return postings


def build_inverted_index(postings):
    index = {}
    for term, doc_id, position in postings:
        if term not in index:
            index[term] = {'df': 0, 'postings': {}}
        if doc_id not in index[term]['postings']:
            index[term]['postings'][doc_id] = []
            index[term]['df'] += 1
        index[term]['postings'][doc_id].append(position)
    return index


def build_term_document_matrix(doc_map, postings):
    # Count term frequencies from postings
    tf = {}
    for term, doc_id, position in postings:
        if term not in tf:
            tf[term] = {}
        tf[term][doc_id] = tf[term].get(doc_id, 0) + 1

    # Build matrix with tf values, filling 0 for missing entries
    matrix = {}
    for term in tf:
        matrix[term] = {}
        for doc_id in doc_map:
            matrix[term][doc_id] = tf[term].get(doc_id, 0)
    return matrix


def write_matrix_to_json(index_path, doc_map, matrix):
    data = {
        'documents': doc_map,
        'matrix': matrix
    }
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def sort_postings(postings):
    return sorted(postings, key=lambda x: (x[0], x[1], x[2]))


def build_index(corpus_path):
    doc_map = get_document_map(corpus_path)

    # Step 1: Collect all postings
    postings = collect_all_postings(corpus_path, doc_map)

    # Step 2: Sort by term, then doc_id
    postings = sort_postings(postings)

    # Step 3: Build the index by reading the postings list
    index = build_inverted_index(postings)

    return doc_map, index, postings
