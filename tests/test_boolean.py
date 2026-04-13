import pytest                                                                         
import sys                                                                            
import os                                                                             
                                                                                        
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))                     
                
from query_engines.boolean import load_index, tokenize, normalize, shunting_yard, evaluate        
                                                                                    
INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'indexes',         
'corpus_slides.json')
                                                                                        
                
@pytest.fixture(scope='module')
def index_data():
    doc_map, index = load_index(INDEX_PATH)                                           
    all_docs = set(doc_map.keys())
    return doc_map, index, all_docs                                                   
                
                                                                                    
def run(query, index_data):
    doc_map, index, all_docs = index_data                                             
    postfix = shunting_yard(normalize(tokenize(query)))
    doc_ids = evaluate(postfix, index, all_docs)
    return set(doc_map[d] for d in doc_ids)                                           
                                                                                    
                                                                                    
# Single term                                                                         
def test_single_term_tank(index_data):
    assert run("tank", index_data) == {'d2.txt', 'd4.txt'}
                                                                                    
def test_single_term_bowl(index_data):                                                
    assert run("bowl", index_data) == {'d3.txt'}                                      
                                                                                    
def test_single_term_freshwater(index_data):
    assert run("freshwater", index_data) == {'d1.txt'}
                                                                                    
def test_single_term_homepage(index_data):
    assert run("homepage", index_data) == {'d4.txt'}                                  
                
def test_single_term_aquarium(index_data):                                            
    assert run("aquarium", index_data) == {'d1.txt', 'd2.txt', 'd3.txt', 'd4.txt'}
                                                                                    
# :and:         
def test_and_aquarium_setup(index_data):                                              
    assert run("aquarium :and: setup", index_data) == {'d2.txt'}
                                                                                    
def test_and_tank_setup(index_data):
    assert run("tank :and: setup", index_data) == {'d2.txt'}                          
                                                                                    
def test_and_tank_bowl(index_data):
    assert run("tank :and: bowl", index_data) == set()                                
                
def test_and_fish_freshwater(index_data):                                             
    assert run("fish :and: freshwater", index_data) == {'d1.txt'}
                                                                                    
def test_and_fish_goldfish(index_data):
    assert run("fish :and: goldfish", index_data) == {'d3.txt'}
                                                                                    
# :or:
def test_or_tank_bowl(index_data):                                                    
    assert run("tank :or: bowl", index_data) == {'d2.txt', 'd3.txt', 'd4.txt'}
                                                                                    
def test_or_freshwater_homepage(index_data):
    assert run("freshwater :or: homepage", index_data) == {'d1.txt', 'd4.txt'}        
                                                                                    
def test_or_setup_goldfish(index_data):
    assert run("setup :or: goldfish", index_data) == {'d2.txt', 'd3.txt'}             
                                                                                    
# :not:
def test_not_aquarium(index_data):                                                    
    assert run(":not: aquarium", index_data) == set()
                                                                                    
def test_not_bowl(index_data):
    assert run(":not: bowl", index_data) == {'d1.txt', 'd2.txt', 'd4.txt'}            
                
def test_not_tropical(index_data):                                                    
    assert run(":not: tropical", index_data) == set()
                                                                                    
def test_and_not_bowl(index_data):
    assert run("fish :and: :not: bowl", index_data) == {'d1.txt', 'd2.txt', 'd4.txt'}
                                                                                    
def test_and_not_setup(index_data):
    assert run("tank :and: :not: setup", index_data) == {'d4.txt'}                    
                                                                                    
# Parentheses
def test_not_paren_aquarium_and_freshwater(index_data):                               
    assert run(":not: ( aquarium :and: freshwater )", index_data) == {'d2.txt',       
'd3.txt', 'd4.txt'}                                                                   
                                                                                    
def test_paren_or_then_and(index_data):                                               
    assert run("fish :and: ( freshwater :or: tank )", index_data) == {'d1.txt',
'd2.txt', 'd4.txt'}                                                                   

def test_paren_or_and_not(index_data):                                                
    assert run("( tank :or: bowl ) :and: :not: setup", index_data) == {'d3.txt',
'd4.txt'}                                                                             

def test_paren_and_or(index_data):                                                    
    assert run("aquarium :and: ( setup :or: homepage )", index_data) == {'d2.txt',
'd4.txt'}                                                                             

# Operator precedence (no parentheses)                                                
def test_precedence_or_and(index_data):
    # freshwater :or: (tank :and: bowl) = {d1} :or: {} = {d1}
    assert run("freshwater :or: tank :and: bowl", index_data) == {'d1.txt'}           

def test_precedence_or_and_2(index_data):                                             
    # bowl :or: (goldfish :and: fish) = {d3} :or: {d3} = {d3}
    assert run("bowl :or: goldfish :and: fish", index_data) == {'d3.txt'}