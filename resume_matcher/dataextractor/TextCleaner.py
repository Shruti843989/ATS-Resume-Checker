import re
import spacy

nlp = spacy.load("en_core_web_md")

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\(?\d{3}\)?[-.\\s]?\d{3}[-.\\s]?\d{4}",
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
}


class TextCleaner:
    @staticmethod
    def remove_emails_links(text):
        for pattern in REGEX_PATTERNS:
            text = re.sub(REGEX_PATTERNS[pattern], "", text)
        return text

    @staticmethod
    def clean_text(text):
        text = TextCleaner.remove_emails_links(text)
        doc = nlp(text)
        for token in doc:
            if token.pos_ == "PUNCT":
                text = text.replace(token.text, "")
        return str(text)

    @staticmethod
    def remove_stopwords(text):
        doc = nlp(text)
        for token in doc:
            if token.is_stop:
                text = text.replace(token.text, "")
        return text


class CountFrequency:
    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)

    def count_frequency(self):
        pos_freq = {}
        for token in self.doc:
            if token.pos_ in pos_freq:
                pos_freq[token.pos_] += 1
            else:
                pos_freq[token.pos_] = 1
        return pos_freq
