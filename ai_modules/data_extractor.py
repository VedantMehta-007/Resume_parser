
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_data(text):
    # Clean text: Remove extra spaces and noise
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Use spaCy to detect the name
    doc = nlp(text)
    name = None
    
    # Rule 1: Extract the first PERSON entity
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
    
    # Rule 2: Fallback to the first line (common in resumes)
    if not name:
        first_line = text.split('\n')[0].strip()
        name = first_line if len(first_line.split()) <= 3 else None  # Assume name is short
    
    # Rule 3: Use regex for uppercase/lowercase patterns (e.g., "John Doe")
    if not name:
        match = re.search(r'^([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)', text)
        if match:
            name = match.group(1)
    
    # Create DataFrame
    data = {
        "Name": [name],
        # ... other fields (email, skills, etc.)
    }
    return pd.DataFrame(data)

def extract_data(text):
    print("========= RAW TEXT =========")
    print(text)  # Check if the name appears here
    print("============================")
    # ... rest of your code