import json
import subprocess
import pytest


def test_index(request):
    corpus = request.config.getoption("--corpus")
    output = request.config.getoption("--output")
    ground_truth = request.config.getoption("--ground-truth")
    index_type = request.config.getoption("--index-type")

    subprocess.run(
        ["python3", "main.py", "--corpus", corpus, "--index", f"-{index_type}", output],
        check=True
    )

    with open(output, "r", encoding="utf-8") as f:
        generated = json.load(f)

    with open(ground_truth, "r", encoding="utf-8") as f:
        expected = json.load(f)

    assert generated == expected

