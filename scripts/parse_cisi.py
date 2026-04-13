"""
Parse CISI.ALL into individual .txt files (one per document).

Each document's text is the concatenation of its .T (title) and .W (abstract)
sections, which are the content fields relevant to indexing.

Usage:
    python3 scripts/parse_cisi.py
"""

import os
import re


CISI_ALL = os.path.join("data", "cisi", "CISI.ALL")
OUT_DIR = os.path.join("data", "corpus_cisi")


def parse_cisi(cisi_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    with open(cisi_path, encoding="utf-8") as f:
        content = f.read()

    # Split into (id, body) pairs on .I markers
    parts = re.split(r"\.I\s+(\d+)\n", content)[1:]  # skip leading empty string
    pairs = [(parts[i], parts[i + 1]) for i in range(0, len(parts), 2)]

    for doc_id_str, body in pairs:
        doc_id = int(doc_id_str.strip())

        title = ""
        abstract = ""

        t_match = re.search(r"\.T\s*\n(.*?)(?=\n\.[A-Z])", body, re.DOTALL)
        if t_match:
            title = t_match.group(1).strip()

        w_match = re.search(r"\.W\s*\n(.*?)(?=\n\.[A-Z]|\Z)", body, re.DOTALL)
        if w_match:
            abstract = w_match.group(1).strip()

        text = "\n".join(filter(None, [title, abstract]))

        fname = f"d{doc_id:04d}.txt"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as out:
            out.write(text)

    print(f"Wrote {len(pairs)} documents to {out_dir}/")


if __name__ == "__main__":
    parse_cisi(CISI_ALL, OUT_DIR)
