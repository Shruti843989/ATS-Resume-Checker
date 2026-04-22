# ResumeRank — ATS Resume Checker

A modern, web-based ATS (Applicant Tracking System) resume checker built with Flask, spaCy, and FastEmbed.

## Features
- Upload resume & job description as PDF or paste as text
- Instant ATS match score (0–100%)
- Matched & missing keywords
- Key themes from JD
- Named entity extraction
- Beautiful dark-mode UI (no Streamlit!)

## Tech Stack
| Component | Library |
|---|---|
| Web Framework | Flask |
| PDF Parsing | pypdf |
| NLP | spaCy (`en_core_web_md`) |
| Keyword Extraction | textacy (SGRank, TextRank, YAKE, sCAKE) |
| Vector Similarity | FastEmbed + Qdrant (in-memory) |

## Setup

```bash
# 1. Create virtual environment
python -m venv env

# On Windows
env\Scripts\activate

# On Mac/Linux
source env/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

## Project Structure
```
ResumeRank/
├── app.py                          # Flask app (main entry point)
├── requirements.txt
├── templates/
│   └── index.html                  # Full UI (HTML/CSS/JS)
├── resume_matcher/
│   ├── dataextractor/
│   │   ├── DataExtractor.py        # NLP entity/keyword extraction
│   │   ├── KeyTermExtractor.py     # textacy keyterm algorithms
│   │   └── TextCleaner.py         # Text preprocessing
│   └── scripts/
│       ├── parser.py               # Document → JSON pipeline
│       └── utils.py               # PDF reader + scoring engine
└── uploads/                        # Temporary upload folder (auto-created)
```

## How It Works
1. PDF text is extracted using `pypdf`
2. Text is cleaned with spaCy (punctuation, stopwords, emails removed)
3. Keywords (nouns/proper nouns) are extracted
4. FastEmbed converts keywords to vectors using `BAAI/bge-base-en` model
5. Qdrant computes cosine similarity between resume and JD vectors
6. Results are shown with matched/missing keywords and improvement tips
