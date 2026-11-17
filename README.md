# AI-Powered Resume & Job Matching System

A starter web app that extracts skills from a text-based PDF/TXT resume and a job description, then displays overlapping and missing skills.

## Features
- PDF and TXT resume upload
- Skill extraction using a customizable keyword taxonomy
- Transparent skill-match score
- Matched, missing, and additional skills
- Basic input validation and upload size limit

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Visit `http://127.0.0.1:5000`.

## How the score works
`matched skills / skills detected in the job description × 100`.

This is a simple skill-coverage score, not a validated hiring prediction, resume quality score, or guarantee of job suitability. The taxonomy and keyword approach can miss synonyms and context. Add tests and evaluate against labeled examples before using it for real hiring decisions.

## Privacy
This demo processes the uploaded file in the running app and does not save it to a database. Avoid uploading confidential personal data to a public deployment. Add authentication, secure hosting, retention rules, and stronger security review before production use.

## Limitations
- Scanned/image-only PDFs may require OCR before upload.
- Skill extraction is keyword-based and may not understand context, proficiency, or years of experience.
- The score only covers skills detected from the job description.
