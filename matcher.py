import re
from io import BytesIO
import PyPDF2

# Starter skill taxonomy. Extend this list for the job families you support.
SKILL_TAXONOMY = {
    "python": ["python"],
    "sql": ["sql", "structured query language"],
    "machine learning": ["machine learning", "scikit-learn", "sklearn"],
    "data analysis": ["data analysis", "data analytics", "data analyst"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "excel": ["excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "statistics": ["statistics", "statistical analysis"],
    "flask": ["flask"],
    "django": ["django"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript", "js"],
    "java": ["java"],
    "c++": ["c++"],
    "git": ["git", "github"],
    "linux": ["linux"],
    "nlp": ["natural language processing", "nlp"],
    "deep learning": ["deep learning", "neural network", "neural networks"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "docker": ["docker"],
    "rest api": ["rest api", "restful api"],
    "communication": ["communication", "communication skills"],
    "project management": ["project management"],
    "data visualization": ["data visualization", "data visualisation"],
    "etl": ["etl", "extract transform load"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
}

def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def extract_skills(text):
    """Keyword-based skill extraction; transparent and easy to customize."""
    normalized = normalize(text)
    found = []
    for canonical, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            # Boundaries avoid matching short skills inside unrelated words.
            pattern = r"(?<![a-z0-9+#])" + re.escape(alias.lower()) + r"(?![a-z0-9+#])"
            if re.search(pattern, normalized):
                found.append(canonical)
                break
    return sorted(set(found))

def parse_skills(text):
    return extract_skills(text)

def extract_text_from_pdf(file_storage):
    reader = PyPDF2.PdfReader(BytesIO(file_storage.read()))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def match_resume_to_job(resume_text, job_description):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    extra = sorted(resume_skills - job_skills)

    # Score only against skills detected in the job description.
    # If none are detected, a score is not meaningful.
    score = round(len(matched) / len(job_skills) * 100) if job_skills else None

    return {
        "score": score,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": matched,
        "missing_skills": missing,
        "additional_skills": extra,
        "job_skill_count": len(job_skills),
    }
