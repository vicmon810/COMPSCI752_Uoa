import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

# Parse text
doc = nlp(text)

# Extract entities and relationships
entities = set()
relationships = set()

for ent in doc.ents:
    entities.add(ent.text)
    
for token in doc:
    if token.pos_ == "VERB" and token.dep_ == "ROOT":
        subject = [tok.text for tok in token.lefts if tok.dep_ in ('nsubj', 'nsubjpass')][0]
        relationships.add((subject, token.text))

print("Entities:", entities)
print("Relationships:", relationships)
