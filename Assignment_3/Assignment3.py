import re
import string
import nltk
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from collections import defaultdict

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

text = "I received my PhD in Information Systems from Massey University in 2005. Then I was lecturing in Information Systems at Massey University, Palmerston North, until 2007. From 2008 until 2011, I was Associate Professor at the School of Information Management at the Victoria University of Wellington. In 2012, I joined the Department of Computer Science at the University of Auckland. I was awarded a Doctor of Science degree from the University of Auckland in 2015.I received the Chris Wallace Award for outstanding research contributions to Australia and New Zealand in 2013, awarded by the Computing Research and Education Association of Australasia (CORE). This is the most prestigious award for mid-career computer scientists in Australasia. The prize is available to academics for post-PhD research undertaken in a university or research institution in Australia or New Zealand. The research must include a notable breakthrough or contribution of particular significance. At most one award is made each year. Currently, I am an editorial board member of the journals Information Systems, Data and Knowledge Engineering, and Proceedings of the VLDB Endowment. I am reviewing extensively for other journals and conferences including ACM SIGMOD, ACM Transactions on Database System, IEEE ICDE, IEEE Transactions on Knowledge and Data Engineering, VLDB and the VLDB Journal."

text = text.lower()

special_terms = ["PhD", "CORE", "VLDB", "ACM","SIGMOD", "ACM", "IEEE", "ICDE"]

for term in special_terms:
    pattern = re.compile(r'\b' + re.escape(term.lower()) + r'\b')
    text = pattern.sub(term, text)

sentences = sent_tokenize(text)
entities = set()
relationships = defaultdict(list)

for sentence in sentences:
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    prev_entity = None
    for word, tag in tagged_words:
        if tag.startswith('NN'):
            entities.add(word)
            if prev_entity:
                relationships[prev_entity].append(word)
        elif tag.startswith('VB'):
            if prev_entity:
                relationships[prev_entity].append(word)
        prev_entity = word if tag.startswith('NN') else None

# Print entities and relationships
print("Entities:", entities)
print("\nRelationships:")
for entity, rels in relationships.items():
    print(entity, ":", rels)

# Constructing the knowledge graph
print("---------")
knowledge_graph = defaultdict(list)

for entity, rels in relationships.items():
    for rel in rels:
        knowledge_graph[entity].append(rel)

# Print the knowledge graph
print("\nKnowledge Graph:")
for entity, rels in knowledge_graph.items():
    print(entity, ":", rels)

## Question 2
print("Quesiton 2 ------------------")

nlp = spacy.load("en_core_web_sm")

doc = nlp(text)

entities = set()
relationships = set()

for ent in doc.ents:
    entities.add(ent.text)

for token in doc: 
    if token.pos_ == "VERB" and token.dep_ == "ROOT":
        subject = [tok.text for tok in token.lefts if tok.dep_ in('nsubj', 'nsubjpass') ][0]
        relationships.add((subject, token.text))

print("Entities: ", entities)
print("Relationships", relationships)

# Refine relationships
print("Questin 3 ------------------------")

refined_relationships = set()

for subject, verb in relationships:
    if "editorial board member" in subject:
        subject = "contributes to"
    refined_relationships.add((subject, verb))

print("Refined Relationships:", refined_relationships)
