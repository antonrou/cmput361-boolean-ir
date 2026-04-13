# CMPUT 361: Preprocessing, Indexing, and Boolean Query Engine
## Assignments 1 & 2

This repository implements a full information retrieval pipeline across two assignments:

1. **Assignment 1** — A preprocessing and indexing pipeline that reads a corpus of plain-text UTF-8 documents and builds either an inverted index or a term-document incidence matrix.
2. **Assignment 2** — A Boolean query engine that evaluates boolean expressions against the inverted index, and an evaluation framework that measures precision, recall, and F1 against the CISI benchmark dataset.

## Repository Layout

- `main.py` — Entry point for building indexes and running boolean queries.
- `preprocessor.py` — Tokenization and normalization logic (lemmatization, stopword removal).
- `index_builder.py` — Index construction logic (inverted index and term-document matrix).
- `query_engines/boolean.py` — Boolean query engine (tokenizer, normalizer, Shunting Yard algorithm, evaluator).
- `data/cisi/cisi_boolean_queries.json` — The 35 CISI boolean queries manually translated into the engine's `:and:/:or:/:not:` infix syntax.
- `evaluate.py` — Evaluation script that runs all CISI boolean queries and reports precision, recall, and F1.
- `data/` — Input corpora, generated index files, and CISI benchmark files.
- `tests/` — Tests and ground truth files.

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Building an Index

Build an inverted index:

```bash
python3 main.py --corpus ./data/corpus_slides -i ./data/indexes/corpus_slides.json
```

Build a term-document incidence matrix:

```bash
python3 main.py --corpus ./data/corpus_slides -t ./data/indexes/corpus_slides_matrix.json
```

- `--corpus` — path to the folder containing `.txt` files to index
- `-i` — build an inverted index and write to the given path
- `-t` — build a term-document matrix and write to the given path

### Running a Boolean Query

Queries use the operators `:and:`, `:or:`, and `:not:`, with parentheses for grouping:

```bash
python3 main.py -qb ./data/indexes/corpus_slides.json "aquarium :and: setup"
python3 main.py -qb ./data/indexes/corpus_slides.json "tank :or: fish"
python3 main.py -qb ./data/indexes/corpus_slides.json "fish :and: :not: bowl"
python3 main.py -qb ./data/indexes/corpus_slides.json "aquarium :and: ( setup :or: :not: bowl )"
```

Results are printed to STDOUT as filenames, one per line.

## Evaluation

### Evaluating the Index Generation

Ground truth files were verified by hand using the example corpus from the course slides, as well as a custom corpus (`corpus_mine`) created and verified manually.

Run a test comparing generated output against a ground truth file:

```bash
pytest tests/test_compare.py \
  --corpus <corpus_path> \
  --output <output_path> \
  --ground-truth <ground_truth_path>
```

Example — test inverted index for corpus_slides:

```bash
pytest tests/test_compare.py \
  --corpus ./data/corpus_slides \
  --output ./data/indexes/corpus_slides.json \
  --ground-truth ./tests/inverted_index/ground_truth/corpus_slides.json
```

Example — test term-document matrix for corpus_slides:

```bash
pytest tests/test_compare.py \
  --corpus ./data/corpus_slides \
  --output ./data/indexes/corpus_slides_matrix.json \
  --ground-truth ./tests/term-document_matrix/ground_truth/corpus_slides_matrix.json
```


### Evaluating the Boolean Query Engine

The evaluation uses the [CISI benchmark dataset](https://ir.dcs.gla.ac.uk/resources/test_collections/cisi/), which includes:

- `cisi_boolean_queries.json` — 35 boolean queries manually translated into the engine's infix syntax
- `CISI.REL` — relevance judgments (ground truth)

First, build the CISI inverted index:

```bash
python3 main.py --corpus ./data/corpus_cisi -i ./data/indexes/corpus_cisi.json
```

Then run the evaluation:

```bash
python3 evaluate.py ./data/indexes/corpus_cisi.json ./data/cisi/CISI.BLN ./data/cisi/CISI.REL
```

This outputs per-query TP, FP, FN, TN, precision, recall, and F1, followed by macro-average and micro-average summary statistics.

#### How It Works

1. Each converted query is run through the boolean query engine against the CISI inverted index.
3. The returned set of document IDs is compared against the relevant documents in `CISI.REL`.
4. Precision, recall, and F1 are computed per query, then aggregated as macro and micro averages.


## Future Steps

- **Linked list implementation** — The inverted index is currently implemented using Python dictionaries stored as JSON. A more efficient implementation would represent posting lists as sorted linked lists, enabling the merge-based intersection and union algorithms described in the course slides.
- **Skip pointers** — Once posting lists are implemented as linked lists, skip pointers can be added to speed up the merge algorithm for `:and:` queries. Skip pointers allow jumping ahead in a posting list when the current doc ID is behind the other list's pointer, reducing the number of comparisons needed.
- **Stemming** — Experiment with stemming (e.g. Porter Stemmer) as an alternative to lemmatization and compare the effect on index size and retrieval quality against the CISI benchmark.
- **Date normalization** — Normalize different representations of the same date to a single token (e.g. `01/01/2026`, `January 1, 2026`, and `Jan 1 2026` should all map to the same term).
- **Compound word handling** — Improve tokenization of hyphenated words (e.g. `word-level`) and multi-word expressions (e.g. `Nova Scotia`) so they are treated as single tokens.
