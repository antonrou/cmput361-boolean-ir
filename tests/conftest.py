def pytest_addoption(parser):
    parser.addoption("--corpus", action="store", help="Path to the corpus directory.")
    parser.addoption("--output", action="store", help="Path to write the index output file.")
    parser.addoption("--ground-truth", action="store", help="Path to the ground truth JSON file.")
