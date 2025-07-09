import spacy
import re
from datetime import datetime

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.skill_db = {
            'technical': ['Python', 'Machine Learning', 'SQL', 'Flask', 'Pandas','Java','DSA','FrontEnd','PHP','AngularJs',],
            'soft': ['Communication', 'Teamwork', 'Leadership']
        }

    def extract_data(self, text):
        clean_text = re.sub(r'\s+', ' ', text)
        doc = self.nlp(clean_text)
        
        return {
            'name': self._get_name(doc),
            'education': self._find_education(clean_text),
            'experience': self._find_experience(clean_text),
            'skills': self._find_skills(clean_text)
        }

    def _get_name(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Not Found"
    
    def _find_education(self, text):
        edu_keywords = r'\b(B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|PhD|Bachelor|Master)\b'
        return ", ".join(set(re.findall(edu_keywords, text, re.I)))

    def _find_experience(self, text):
        exp_match = re.search(r'(\d+)\+?\s*(years?|yrs?)\b', text, re.I)
        return exp_match.group(0) if exp_match else "Unknown"

    def _find_skills(self, text):
        found = []
        for category in self.skill_db:
            found += [skill for skill in self.skill_db[category] 
                      if re.search(rf'\b{skill}\b', text, re.I)]
        return ", ".join(found) if found else "None Found"
    
