# company_extractor.py
import spacy
import sys
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_company(text):
    doc = nlp(text)
    companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    return companies[0] if companies else "Unknown"

if __name__ == "__main__":
    # Node se text input aayega
    text = sys.argv[1]
    company = extract_company(text)
    print(json.dumps({"company": company}))
