import re
import spacy
from resume_matcher.dataextractor.TextCleaner import TextCleaner

nlp = spacy.load("en_core_web_md")

RESUME_SECTIONS = [
    "Contact Information", "Objective", "Summary", "Education", "Experience",
    "Skills", "Projects", "Certifications", "Licenses", "Awards", "Honors",
    "Publications", "References", "Technical Skills", "Computer Skills",
    "Programming Languages", "Software Skills", "Soft Skills", "Language Skills",
    "Professional Skills", "Transferable Skills", "Work Experience",
    "Professional Experience", "Employment History", "Internship Experience",
    "Volunteer Experience", "Leadership Experience", "Research Experience",
    "Teaching Experience",
]


class DataExtractor:
    def __init__(self, raw_text: str):
        self.text = raw_text
        self.clean_text = TextCleaner.clean_text(self.text)
        self.doc = nlp(self.clean_text)

    def extract_links(self):
        link_pattern = r"\b(?:https?://|www\.)\S+\b"
        return re.findall(link_pattern, self.text)

    def extract_names(self):
        return [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]

    def extract_emails(self):
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        return re.findall(email_pattern, self.text)

    def extract_phone_numbers(self):
        phone_number_pattern = r"^(\+\d{1,3})?[-.\\s]?\(?\d{3}\)?[-.\\s]?\d{3}[-.\\s]?\d{4}$"
        return re.findall(phone_number_pattern, self.text)

    def extract_experience(self):
        experience_section = []
        in_experience_section = False
        for token in self.doc:
            if token.text in RESUME_SECTIONS:
                if token.text in ("Experience", "EXPERIENCE", "experience"):
                    in_experience_section = True
                else:
                    in_experience_section = False
            if in_experience_section:
                experience_section.append(token.text)
        return " ".join(experience_section)

    def extract_position_year(self):
        pattern = r"(\b\w+\b\s+\b\w+\b),\s+(\d{4})\s*-\s*(\d{4}|\bpresent\b)"
        return re.findall(pattern, self.text)

    def extract_particular_words(self):
        pos_tags = ["NOUN", "PROPN"]
        return [token.text for token in self.doc if token.pos_ in pos_tags]

    def extract_entities(self):
        entity_labels = ["GPE", "ORG"]
        entities = [token.text for token in self.doc.ents if token.label_ in entity_labels]
        return list(set(entities))
