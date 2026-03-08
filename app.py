from flask import Flask, render_template, request
import os
from docx import Document
import nltk
from nltk.corpus import stopwords
from collections import Counter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

stop_words = set(stopwords.words('english'))

# -----------------------------
# Resume Text Extraction
# -----------------------------
def extract_docx_text(path):
    doc = Document(path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return " ".join(text)

# -----------------------------
# Resume Summary (Concise Notes)
# -----------------------------
def generate_summary(text, limit=80):
    words = [w.lower() for w in text.split() if w.lower() not in stop_words]
    common_words = [word for word, freq in Counter(words).most_common(limit)]
    return " ".join(common_words)

# -----------------------------
# Resume Scoring Logic
# -----------------------------
def score_resume(text):
    keywords = [
        "python", "java", "sql", "machine learning",
        "deep learning", "data science", "project",
        "experience", "internship", "flask", "django",
        "react", "html", "css", "javascript"
    ]

    score = 0
    text = text.lower()

    for kw in keywords:
        if kw in text:
            score += 5

    length_bonus = min(len(text.split()) // 100, 20)
    score += length_bonus

    return min(score, 100)

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    score = None
    filename = ""

    if request.method == "POST":
        file = request.files["resume"]

        if file.filename.endswith(".docx"):
            filename = file.filename
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)

            text = extract_docx_text(path)
            summary = generate_summary(text)
            score = score_resume(text)

    return render_template(
        "index.html",
        summary=summary,
        score=score,
        filename=filename
    )

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
