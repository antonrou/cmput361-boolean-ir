import json
import subprocess
import pytest


def test_index(request):
    corpus = request.config.getoption("--corpus")
    output = request.config.getoption("--output")
    ground_truth = request.config.getoption("--ground-truth")

    with open(ground_truth, "r", encoding="utf-8") as f:
        expected = json.load(f)

    index_type = "t" if "matrix" in expected else "i"

    subprocess.run(
        ["python3", "main.py", "--corpus", corpus, f"-{index_type}", output],
        check=True
    )

    with open(output, "r", encoding="utf-8") as f:
        generated = json.load(f)

    assert generated == expected

