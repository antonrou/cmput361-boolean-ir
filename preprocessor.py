import re
import nltk
from nltk.tokenize import word_tokenize  # function that splits string of text into individual word tokens, handles punctuation, contractions, etc.
from nltk.stem import WordNetLemmatizer  # lemmatizer that uses WordNet database to reduce words to their base/dictionary form
from nltk.corpus import stopwords        # list of common words to filter out (e.g. "the", "and", "in")
from nltk.corpus import wordnet          # used for mapping POS tags to WordNet format

nltk.download('punkt', quiet=True)                      # pre-trained model used to know where sentence and word boundaries are
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)                    # English lexical database that groups words by meaning and relationships. Used by lemmatizer as a lookup to find base form of a word (necessary for lemmatization to work).
nltk.download('stopwords', quiet=True)                  # list of common English stop words
nltk.download('averaged_perceptron_tagger', quiet=True) # POS tagger model
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words('english'))


def tokenize(text):
    tokens = word_tokenize(text) # split text into individual word tokens, handles punctuation, contractions, etc.
    return [t for t in tokens if re.search(r'[a-zA-Z0-9]', t)] # filter out tokens that don't contain any alphanumeric characters (removes punctuation, etc.)


def get_wordnet_pos(treebank_tag):
    # Maps Penn Treebank POS tags to WordNet POS tags for the lemmatizer
    if treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def normalize(tokens):
    tokens = [t.lower() for t in tokens]
    tokens = [t for t in tokens if t not in _stop_words]
    pos_tags = nltk.pos_tag(tokens)
    tokens = [_lemmatizer.lemmatize(t, get_wordnet_pos(pos)) for t, pos in pos_tags]
    return tokens


def preprocess(text):
    tokens = tokenize(text) # split text into individual word tokens, handles punctuation, contractions, etc.
    tokens = normalize(tokens)
    return tokens
