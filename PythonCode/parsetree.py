import nltk
from nltk.draw.tree import draw_trees

# Download required NLTK data
nltk.download('punkt', quiet=True)

def create_constituency_tree(sentence):
    tokens = nltk.word_tokenize(sentence)
    print(f"Tokens: {tokens}")
    
    grammar = nltk.CFG.fromstring("""
        S -> NP VP
        NP -> Det N | Det N PP | N | PRP | Det ADJ N | NP CC NP
        VP -> V | V NP | V NP PP | V NP NP
        PP -> P NP
        Det -> 'The' | 'the' | 'a' | 'an'
        N -> 'government' | 'interest' | 'rates' | 'internet' | 'voice' | 'man' | 'dog' | 'telescope' | 'everyone'
        V -> 'raised' | 'gives' | 'saw'
        P -> 'with'
        PRP -> 'everyone'
        ADJ -> 'interest'
        CC -> 'and'
    """)
    parser = nltk.ChartParser(grammar)
    return list(parser.parse(tokens))

# Sentences to parse
sentences = [
    "The government raised interest rates",
    "The internet gives everyone a voice",
    "The man saw the dog with the telescope"
]

# Create parse trees
all_trees = []
for sentence in sentences:
    trees = create_constituency_tree(sentence)
    unique_trees = list({str(tree): tree for tree in trees}.values())
    
    all_trees.extend(unique_trees)
    
    # Visualize unique trees for this sentence
    if unique_trees:
        draw_trees(*unique_trees)


