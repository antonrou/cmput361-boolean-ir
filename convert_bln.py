import re
import json


def tokenize_bln(expr):
    token_pattern = re.compile(r"#and|#or|#not|'[^']*'|\(|\)|,")
    return token_pattern.findall(expr)


class BLNParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse_expr(self):
        tok = self.peek()
        if tok == '#and':
            return self.parse_op(':and:')
        elif tok == '#or':
            return self.parse_op(':or:')
        elif tok == '#not':
            return self.parse_not()
        elif tok and tok.startswith("'"):
            self.consume()
            return tok.strip("'")
        else:
            raise ValueError(f"Unexpected token: {tok}")

    def parse_op(self, op):
        self.consume()  # consume #and or #or
        self.consume()  # consume (
        args = self.parse_arg_list()
        self.consume()  # consume )
        if len(args) == 1:
            return args[0]
        return '( ' + f' {op} '.join(args) + ' )'

    def parse_not(self):
        self.consume()  # consume #not
        self.consume()  # consume (
        arg = self.parse_expr()
        self.consume()  # consume )
        return f':not: {arg}'

    def parse_arg_list(self):
        args = [self.parse_expr()]
        while self.peek() == ',':
            self.consume()  # consume ,
            args.append(self.parse_expr())
        return args


def extract_queries(bln_path):
    with open(bln_path, 'r', encoding='utf-8') as f:
        content = f.read()

    query_pattern = re.compile(r'#q(\d+)\s*=\s*(.*?);', re.DOTALL)
    queries = {}
    for match in query_pattern.finditer(content):
        qid = match.group(1)
        expr = match.group(2).strip()
        tokens = tokenize_bln(expr)
        parser = BLNParser(tokens)
        queries[qid] = parser.parse_expr()
    return queries


if __name__ == "__main__":
    queries = extract_queries('data/cisi/CISI.BLN')
    for qid, query in queries.items():
        print(f"q{qid}: {query}")
    with open('data/cisi/cisi_boolean_queries_auto.json', 'w', encoding='utf-8') as f:
        json.dump(queries, f, indent=2)
    print("\nSaved to data/cisi/cisi_boolean_queries_auto.json")
