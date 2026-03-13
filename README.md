# AI Resume Analyzer 📄🤖

An intelligent web application that analyzes resumes using **Natural Language Processing (NLP)** and provides insights such as **resume score, keyword matching, and automated summaries**.
The application supports **PDF and DOCX resumes**, allows **custom keyword analysis**, and visualizes results with charts.

---

## 🚀 Features

* 📂 Upload resumes in **PDF, DOCX, or DOC** format
* 🧠 **AI-based resume summarization** using the **Sumy LSA summarizer**
* 🔍 **Custom keyword matching** (user-defined keywords)
* 📊 **Resume score calculation** based on keyword matches
* 🥧 **Pie chart visualization** of matched vs missing keywords
* 🗂 **Resume history sidebar** showing previously analyzed resumes
* 💾 **SQLite database storage** for resume results
* 🌐 Clean and responsive **web UI with Bootstrap**

---

## 🖥 Demo

Upload a resume and enter keywords like:

```
python, flask, machine learning, sql, data science
```

The system will:

1. Extract text from the resume
2. Generate a short summary
3. Calculate a resume score
4. Show matched vs missing keywords in a chart
5. Save the result for later viewing

---

## 🏗 Project Structure

```
ai_resume_analyzer
│
├── app.py
├── resumes.db
├── uploads/
│
├── templates/
│   └── index.html
│
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```
git clone https://github.com/juk-bx/ai_resume_analyzer.git
cd ai_resume_analyzer
```

### 2️⃣ Create a Virtual Environment (optional but recommended)

```
python -m venv venv
```

Activate it:

Windows

```
venv\Scripts\activate
```

Linux / macOS

```
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```
pip install flask python-docx nltk PyPDF2 sumy
```

---

### 4️⃣ Download NLTK Data

Run once:

```
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

---

### 5️⃣ Run the Application

```
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## 📊 How the Resume Score Works

The score is calculated based on:

* **Keyword matches** in the resume
* **Length of resume content**
* **Presence of important technical terms**

Example:

| Metric        | Description                        |
| ------------- | ---------------------------------- |
| Keyword Match | +5 points for each matched keyword |
| Resume Length | Bonus based on text size           |
| Maximum Score | 100                                |

---

## 🧠 Summarization Method

The project uses the **LSA summarization algorithm** from the **Sumy NLP library**.

Steps:

1. Extract text from resume
2. Split into sentences
3. Identify key semantic patterns
4. Select the most relevant sentences as a summary

---

## 📈 Visualization

The application generates a **pie chart** using **Chart.js** showing:

* Matched keywords
* Missing keywords

This helps quickly evaluate resume compatibility with specific skill requirements.

---

## 🛠 Technologies Used

Backend:

* Python
* Flask
* SQLite

NLP & Processing:

* NLTK
* Sumy
* PyPDF2
* python-docx

Frontend:

* HTML
* Bootstrap
* Chart.js

---

## 🔮 Future Improvements

Planned features:

* 📑 **Resume keyword highlighting**
* 📊 **ATS compatibility score**
* 🧾 **Resume vs Job Description matching**
* 🧠 **AI-powered resume improvement suggestions**
* 📥 **Downloadable analysis report**
* 📊 Skill graphs and analytics dashboard



---

## 👨‍💻 Author

**Ojas Joshi**

GitHub
https://github.com/juk-bx


