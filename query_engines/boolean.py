import json
import preprocessor

def load_index(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        inverted_index = json.load(f)
        doc_map = inverted_index['documents']
        index = inverted_index['index']
    return (doc_map, index)

    
def tokenize(query):
    query = query.replace('(', ' ( ').replace(')', ' ) ')
    query_without_whitespace = query.split()
    tokens = []
    for term in query_without_whitespace:
        if term.startswith(':') and term.endswith(':'):                
            tokens.append(('OPERATOR', term))
        elif term == '(' or term == ')':                                                   
            tokens.append(('PAREN', term))
        else:                                                                              
            tokens.append(('TERM', term))
    return tokens

def normalize(tokenized_query):                
    normalized = []                            
    for token_type, value in tokenized_query:  
        if token_type == 'TERM':               
            normalized.append((token_type, preprocessor.preprocess(value)[0]))                
        else:
            normalized.append((token_type, value))                                      
    return normalized

def op_helper(operator_stack, value, 
  precedence, right_associative):                                 
      if not operator_stack or operator_stack[-1][0] != 'OPERATOR':                                                     
          return False
      top_prec = precedence[operator_stack[-1][1]]                
      cur_prec = precedence[value]
      return top_prec > cur_prec or (top_prec == cur_prec and
  value not in right_associative)

def evaluate(postfix, index, all_docs):                         
      stack = []  
      for token_type, value in postfix:
          if token_type == 'TERM':
                stack.append(set(index[value]['postings'].keys()) if value in index else set())              
          elif value == ':and:':
            if len(stack) < 2:                                              
                raise ValueError("Invalid query")
            else:                                   
                a = stack.pop()
                b = stack.pop()
                stack.append(a & b)                         
          elif value == ':or:':
            if len(stack) < 2:                                              
                raise ValueError("Invalid query")
            else:                                    
                a = stack.pop()
                b = stack.pop()
                stack.append(a | b)                             
          elif value == ':not:':
                if len(stack) < 1:
                    raise ValueError("Invalid query")
                else:
                    a = stack.pop()
                    not_a = all_docs - a
                    stack.append(not_a)
      return stack[0]

"""
Credit Claude for this algorithm implementation
"""
def shunting_yard(normalized_query):
    output_queue = []
    operator_stack = []
    precedence = {':not:': 3, ':and:': 2, ':or:': 1}
    right_associative = {':not:'}
    for token_type, value in normalized_query:
        if token_type == 'TERM': # Case 1
            output_queue.append((token_type, value))
        elif token_type == 'OPERATOR': # Case 2
            while op_helper(operator_stack, value, 
  precedence, right_associative):
                output_queue.append(operator_stack.pop())
            operator_stack.append((token_type, value))
        elif token_type == 'PAREN': # Case 3
            if value == '(':
                operator_stack.append((token_type, value))
            elif value == ')':
                while operator_stack[-1][1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
    while operator_stack:
        output_queue.append(operator_stack.pop())
    return output_queue

def main(index_path, query):
    doc_map, index = load_index(index_path)
    tokenized_query = tokenize(query)
    normalized_query = normalize(tokenized_query)
    output_queue = shunting_yard(normalized_query)
    doc_set = evaluate(output_queue, index, set(doc_map.keys()))
    return [doc_map[doc_id] for doc_id in doc_set]



