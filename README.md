# CMPUT 361 Assignment 1: Preprocessing and Indexing

This repository implements a preprocessing and indexing pipeline that reads a corpus of plain-text UTF-8 documents and builds either an inverted index or a term-document incidence matrix.

## Repository Layout

- `main.py`: Entry point for running the pipeline.
- `preprocesser.py`: Tokenization and normalization logic.
- `index_builder.py`: Index construction logic.
- `data/`: Input corpora and generated index files.
- `tests/`: Tests and ground truth files.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Build an inverted index:

```bash
python3 main.py --corpus ./data/corpus1 --index -i ./data/corpus1.json
```

Build a term-document incidence matrix:

```bash
python3 main.py --corpus ./data/corpus1 --index -t ./data/corpus1_matrix.json
```

- `--corpus` — path to the folder containing `.txt` files to index
- `--index -i` — build an inverted index and write to the given path
- `--index -t` — build a term-document matrix and write to the given path

## Testing

Ground truth files were verified by hand using the example corpus from the course slides, as well as a custom corpus (`corpus_mine`) created and verified manually.

Run a test comparing generated output against a ground truth file:

```bash
pytest tests/test_compare.py \
  --corpus <corpus_path> \
  --output <output_path> \
  --ground-truth <ground_truth_path> \
  --index-type i|t
```

Example — test inverted index for corpus_slides:

```bash
pytest tests/test_compare.py \
  --corpus ./data/corpus_slides \
  --output ./data/corpus_slides.json \
  --ground-truth ./tests/inverted_index/ground_truth/corpus_slides.json \
  --index-type i
```

Example — test term-document matrix for corpus_slides:

```bash
pytest tests/test_compare.py \
  --corpus ./data/corpus_slides \
  --output ./data/corpus_slides_matrix.json \
  --ground-truth ./tests/term-document_matrix/ground_truth/corpus_slides_matrix.json \
  --index-type t
```

## Future Steps

- **Stemming**: Experiment with stemming as an alternative to lemmatization and compare the effect on index size and retrieval quality.
- **Date normalization**: Normalize different representations of the same date to a single token (e.g. `01/01/2026`, `January 1, 2026`, and `Jan 1 2026` should all map to the same term).
- **Compound word handling**: Improve tokenization of hyphenated words (e.g. `word-level`) and multi-word expressions (e.g. `Nova Scotia`) so they are treated as single tokens.
