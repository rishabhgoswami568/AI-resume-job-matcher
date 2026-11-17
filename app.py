from flask import Flask, render_template, request
from pathlib import Path
from werkzeug.utils import secure_filename
import re
import PyPDF2

from matcher import extract_text_from_pdf, match_resume_to_job, parse_skills

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf", "txt"}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    resume_text = ""
    job_description = ""
    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        upload = request.files.get("resume")
        if not upload or not upload.filename:
            error = "Please upload a PDF or TXT resume."
        elif not job_description:
            error = "Please paste a job description."
        elif not allowed_file(upload.filename):
            error = "Unsupported file type. Upload a PDF or TXT file."
        else:
            filename = secure_filename(upload.filename)
            suffix = Path(filename).suffix.lower()
            try:
                if suffix == ".pdf":
                    resume_text = extract_text_from_pdf(upload)
                else:
                    resume_text = upload.read().decode("utf-8", errors="ignore")
                if not resume_text.strip():
                    error = "No readable text was found. For scanned PDFs, run OCR first or upload a text-based PDF."
                else:
                    result = match_resume_to_job(resume_text, job_description)
            except (PyPDF2.errors.PdfReadError, ValueError, OSError) as exc:
                error = f"Could not read the resume: {exc}"
    return render_template("index.html", result=result, error=error, job_description=job_description)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True)
