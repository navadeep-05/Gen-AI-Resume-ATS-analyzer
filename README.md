# Gen AI Resume ATS Analyzer

A lightweight **Resume Analyzer** that parses resumes, extracts key information, and evaluates them against job descriptions using AI-powered matching. The tool helps job seekers improve their resumes and assists recruiters in shortlisting candidates efficiently.

---

## 📖 What Does the Tool Do?

- **Extract**: Parses PDF or DOCX resumes to pull out contact details, skills, work experience, and education.
- **Fetch Jobs**: Given a company name or URL, the tool scrapes the official careers page to retrieve current job openings.
- **Score with ATS**: Uses a language‑model‑backed ATS scoring algorithm to compare the extracted resume data with the job description.
- **Feedback Report**: Produces a concise markdown report with strengths, gaps, and concrete suggestions to improve the resume for the specific role.

All steps are modular, so you can run just the extraction, just the scoring, or the full end‑to‑end pipeline.

---

## ✨ Features

- **Multi‑format support** – PDF and DOCX parsing.
- **AI‑driven matching** – configurable LLM backend.
- **Customizable scoring** – weight sections (experience, skills, etc.).
- **Plain‑text & JSON output** – easy integration with CI pipelines.
- **Modular pipeline** – each step (extract, clean, score, report) lives in its own module for extensibility.

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Note**: You need an API key for the LLM provider (OpenAI, Gemini, etc.). Add it to a `.env` file:
>
> ```
> LLM_API_KEY=your_api_key_here
> ```

---

## 📂 Project Structure

```
resume-analyzer/
├─ pipeline/               # Core processing pipeline
│   ├─ extract.py          # Resume extraction logic
│   ├─ score.py            # Scoring & matching
│   └─ report.py           # Report generation
├─ models/                 # Pydantic data models
├─ tests/                  # Unit tests
├─ .env.example            # Example environment file
├─ requirements.txt        # Python dependencies
└─ README.md               # This file
```

---

## 🌐 Usage

https://gen-ai-resume-ats-analyzer.onrender.com/


You can check working with the website to find the ATS of your resume how well it matches the job openings you provide to it.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for your changes.
4. Ensure all tests pass (`pytest`).
5. Open a Pull Request with a clear description.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
