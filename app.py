from flask import Flask, render_template, request
import os
import sqlite3
import re
from collections import Counter

from docx import Document
import PyPDF2

import nltk
from nltk.corpus import stopwords

# Download required datasets
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
# SUMY for summarization
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

stop_words = set(stopwords.words('english'))

DB = "resumes.db"


# -----------------------------
# DATABASE
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS resumes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            score INTEGER,
            summary TEXT
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# DOCX TEXT EXTRACTION
# -----------------------------
def extract_docx_text(path):

    doc = Document(path)
    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return " ".join(text)


# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_pdf_text(path):

    text = ""

    with open(path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text


# -----------------------------
# SUMY SUMMARY
# -----------------------------
def generate_summary(text, sentences=3):

    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    summarizer = LsaSummarizer()

    summary = summarizer(parser.document, sentences)

    return " ".join(str(sentence) for sentence in summary)


# -----------------------------
# RESUME SCORING
# -----------------------------
def score_resume(text, keywords):

    text = text.lower()

    matched = []

    score = 0

    for kw in keywords:

        if kw in text:

            score += 5
            matched.append(kw)

    length_bonus = min(len(text.split()) // 100, 20)

    score += length_bonus

    score = min(score, 100)

    return score, matched


# -----------------------------
# MAIN ROUTE
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    summary = ""
    score = None
    filename = ""
    matched = []
    missing = 0

    if request.method == "POST":

        file = request.files["resume"]

        keyword_input = request.form.get("keywords")

        keywords = [k.strip().lower() for k in keyword_input.split(",")]

        filename = file.filename

        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(path)

        # Detect file type
        if filename.endswith(".docx") or filename.endswith(".doc"):

            text = extract_docx_text(path)

        elif filename.endswith(".pdf"):

            text = extract_pdf_text(path)

        else:

            text = ""

        # Generate summary using SUMY
        summary = generate_summary(text)

        # Score resume
        score, matched = score_resume(text, keywords)

        missing = len(keywords) - len(matched)

        # Save to database
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute(
            "INSERT INTO resumes(filename,score,summary) VALUES(?,?,?)",
            (filename, score, summary),
        )

        conn.commit()
        conn.close()

    # Fetch history
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT filename,score FROM resumes ORDER BY id DESC")

    history = c.fetchall()

    conn.close()

    return render_template(
        "index.html",
        summary=summary,
        score=score,
        filename=filename,
        history=history,
        matched=len(matched),
        missing=missing,
    )


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":

    os.makedirs("uploads", exist_ok=True)

    init_db()

    app.run(debug=True)