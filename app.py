import os
import sys
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from resume_matcher.scripts.utils import read_single_pdf, get_score
from resume_matcher.scripts.parser import ParseDocumentToJson
from resume_matcher.dataextractor.TextCleaner import TextCleaner

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def analyze_resume_vs_jd(resume_text: str, jd_text: str) -> dict:
    """Core analysis function — returns all results as a dict."""
    # Parse both documents
    resume_parsed = ParseDocumentToJson(resume_text, "resume").get_JSON()
    jd_parsed = ParseDocumentToJson(jd_text, "job_description").get_JSON()

    resume_keywords = resume_parsed.get("extracted_keywords", [])
    jd_keywords = jd_parsed.get("extracted_keywords", [])

    resume_string = " ".join(resume_keywords)
    jd_string = " ".join(jd_keywords)

    # Get similarity score
    score = get_score(resume_string, jd_string)

    # Find matching and missing keywords
    resume_kw_set = set(k.lower() for k in resume_keywords)
    jd_kw_set = set(k.lower() for k in jd_keywords)
    matched_keywords = list(resume_kw_set & jd_kw_set)[:20]
    missing_keywords = list(jd_kw_set - resume_kw_set)[:20]

    # Keyterms from JD
    jd_keyterms = [kt[0] for kt in jd_parsed.get("keyterms", [])][:10]

    return {
        "score": score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "jd_keyterms": jd_keyterms,
        "resume_entities": resume_parsed.get("entities", [])[:10],
        "resume_name": resume_parsed.get("name", []),
        "total_resume_keywords": len(resume_keywords),
        "total_jd_keywords": len(jd_keywords),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        resume_text = ""
        jd_text = ""

        # Handle resume — file or text
        if "resume_file" in request.files and request.files["resume_file"].filename:
            f = request.files["resume_file"]
            path = os.path.join(UPLOAD_FOLDER, secure_filename(f.filename))
            f.save(path)
            resume_text = read_single_pdf(path)
            os.remove(path)
        elif request.form.get("resume_text"):
            resume_text = request.form.get("resume_text", "")

        # Handle JD — file or text
        if "jd_file" in request.files and request.files["jd_file"].filename:
            f = request.files["jd_file"]
            path = os.path.join(UPLOAD_FOLDER, secure_filename(f.filename))
            f.save(path)
            jd_text = read_single_pdf(path)
            os.remove(path)
        elif request.form.get("jd_text"):
            jd_text = request.form.get("jd_text", "")

        if not resume_text.strip() or not jd_text.strip():
            return jsonify({"error": "Please provide both resume and job description."}), 400

        results = analyze_resume_vs_jd(resume_text, jd_text)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
