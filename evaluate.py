import json
import argparse
from query_engines.boolean import load_index, tokenize, normalize, shunting_yard, evaluate


def load_relevance_judgments(rel_path, query_ids):
    relevant = {qid: set() for qid in query_ids}
    with open(rel_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            qid = parts[0].strip()
            doc_id = parts[1].strip()
            if qid in relevant:
                relevant[qid].add(doc_id)
    return relevant


def run_query(query, index, all_docs):
    tokenized = tokenize(query)
    normalized = normalize(tokenized)
    postfix = shunting_yard(normalized)
    if not postfix:
        return set()
    return evaluate(postfix, index, all_docs)


def confusion_matrix(retrieved, relevant, all_docs):
    tp = len(retrieved & relevant)
    fp = len(retrieved - relevant)
    fn = len(relevant - retrieved)
    tn = len(all_docs - retrieved - relevant)
    return tp, fp, fn, tn


def precision(tp, fp):
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0


def recall(tp, fn):
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0


def f1(p, r):
    return 2 * p * r / (p + r) if (p + r) > 0 else 0.0


def load_queries(queries_path):
    with open(queries_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main(index_path, queries_path, rel_path):
    doc_map, index = load_index(index_path)
    all_docs = set(doc_map.keys())

    queries = load_queries(queries_path)
    relevant = load_relevance_judgments(rel_path, set(queries.keys()))

    total_tp = total_fp = total_fn = total_tn = 0
    total_p = total_r = total_f = 0

    print(f"{'Query':<8} {'TP':>6} {'FP':>6} {'FN':>6} {'TN':>6} {'P':>8} {'R':>8} {'F1':>8}")
    print("-" * 66)

    for qid, query in queries.items():
        retrieved = run_query(query, index, all_docs)
        rel = relevant.get(qid, set())

        tp, fp, fn, tn = confusion_matrix(retrieved, rel, all_docs)
        p = precision(tp, fp)
        r = recall(tp, fn)
        f = f1(p, r)

        total_tp += tp
        total_fp += fp
        total_fn += fn
        total_tn += tn
        total_p += p
        total_r += r
        total_f += f

        print(f"q{qid:<7} {tp:>6} {fp:>6} {fn:>6} {tn:>6} {p:>8.3f} {r:>8.3f} {f:>8.3f}")

    n = len(queries)
    print("-" * 66)

    # Macro-average: average of per-query metrics
    macro_p = total_p / n
    macro_r = total_r / n
    macro_f = total_f / n
    print(f"\nMacro-Average:")
    print(f"  Precision : {macro_p:.3f}")
    print(f"  Recall    : {macro_r:.3f}")
    print(f"  F1        : {macro_f:.3f}")

    # Micro-average: computed from summed TP, FP, FN across all queries
    micro_p = precision(total_tp, total_fp)
    micro_r = recall(total_tp, total_fn)
    micro_f = f1(micro_p, micro_r)
    print(f"\nMicro-Average:")
    print(f"  Precision : {micro_p:.3f}")
    print(f"  Recall    : {micro_r:.3f}")
    print(f"  F1        : {micro_f:.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate boolean query engine on a benchmark.")
    parser.add_argument("index_path", help="Path to the inverted index JSON.")
    parser.add_argument("queries_path", help="Path to the boolean queries JSON file.")
    parser.add_argument("rel_path", help="Path to the relevance judgments file (CISI.REL).")
    args = parser.parse_args()
    main(args.index_path, args.queries_path, args.rel_path)
