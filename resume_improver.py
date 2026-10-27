import re
from collections import Counter


# ============================================================
# 1. BULLET POINT IMPROVEMENT RULES
# ============================================================

BULLET_REPLACEMENTS = [
    (r"\bworked on\b", "performed"),
    (r"\bworked with\b", "collaborated with"),
    (r"\blooked at\b", "analyzed"),
    (r"\bhelped to create\b", "contributed to creating"),
    (r"\bhelped create\b", "contributed to creating"),
    (r"\bhelped develop\b", "contributed to developing"),
    (r"\bhelped build\b", "contributed to building"),
    (r"\bhelped analyze\b", "contributed to analyzing"),
    (r"\bhelped with\b", "assisted with"),
    (r"\bresponsible for\b", "managed"),
    (r"\bhandled\b", "managed"),
    (r"\bused\b", "applied"),
    (r"\bmade\b", "developed"),
    (r"\bcreated\b", "developed"),
    (r"\bdid\b", "completed"),
    (r"\bgot\b", "obtained"),
    (r"\bkept\b", "maintained"),
    (r"\bfixed\b", "resolved"),
    (r"\bbuilt\b", "developed"),
    (r"\bshowed\b", "demonstrated"),
    (r"\bfound\b", "identified"),
    (r"\bchecked\b", "validated"),
]


# ============================================================
# 2. COMMON WORDS TO IGNORE
# ============================================================

IGNORED_TERMS = {
    "the", "and", "for", "with", "are", "you", "our",
    "this", "that", "will", "have", "from", "your",
    "job", "role", "work", "years", "required", "ability",
    "skills", "experience", "knowledge", "strong", "good",
    "excellent", "preferred", "responsibilities", "including",
    "using", "within", "team", "candidate", "looking",
    "must", "should", "their", "they", "what", "when",
    "where", "which", "while", "also", "such", "into",
    "about", "across", "based", "provide", "support",
    "clear", "key", "complex", "various", "different",
    "new", "best", "well", "able", "one", "two", "three",
    "all", "any", "each", "both", "other", "more", "most",
    "many", "some", "etc", "teams", "candidates",
    "responsible", "responsibility", "requirements",
    "requirement", "qualifications", "qualification",
    "seeking", "join", "company", "organization",
    "environment", "ensure", "maintain", "strongly",
    "effectively", "efficiently", "reports", "report",
    "analyst", "abilities", "would", "could", "may",
    "might", "can", "per", "via", "has", "had", "been",
    "being", "its", "not", "than", "then", "who",
    "whom", "how", "why", "where", "when", "get",
    "able", "make", "take", "use", "etc",
}


# ============================================================
# 3. KNOWN TECHNICAL AND PROFESSIONAL SKILLS
# ============================================================

KNOWN_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "sql",
    "mysql",
    "oracle",
    "postgresql",
    "mongodb",
    "excel",
    "advanced excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "machine learning",
    "deep learning",
    "data analysis",
    "data analytics",
    "data visualization",
    "data cleaning",
    "data preprocessing",
    "statistics",
    "exploratory data analysis",
    "etl",
    "data warehousing",
    "aws",
    "azure",
    "google cloud",
    "docker",
    "kubernetes",
    "git",
    "github",
    "flask",
    "django",
    "html",
    "css",
    "react",
    "node.js",
    "rest api",
    "api",
    "communication",
    "problem solving",
    "critical thinking",
    "teamwork",
    "leadership",
    "project management",
    "data structures",
    "algorithms",
    "c",
    "c++",
    "c#",
    "linux",
    "networking",
    "cybersecurity",
    "power query",
    "dax",
    "business intelligence",
    "dashboard development",
    "data modeling",
    "tensorflow",
    "scikit-learn",
    "pytorch",
    "natural language processing",
    "computer vision",
    "data storytelling",
    "kpi reporting",
    "financial analysis",
    "business analysis",
    "predictive analytics",
    "regression analysis",
    "classification",
    "clustering",
    "data mining",
    "data engineering",
    "big data",
    "spark",
    "hadoop",
    "jupyter notebook",
    "powerpoint",
    "word",
}


# ============================================================
# 4. TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """Normalize whitespace and safely handle empty input."""

    if not isinstance(text, str):
        return ""

    return re.sub(r"\s+", " ", text).strip()


def contains_term(text, term):
    """Check whether a complete word or phrase exists in text."""

    pattern = (
        r"(?<!\w)"
        + re.escape(term.lower())
        + r"(?!\w)"
    )

    return bool(
        re.search(pattern, text.lower())
    )


# ============================================================
# 5. CASE-PRESERVING REPLACEMENT
# ============================================================

def replace_preserving_case(match, replacement):
    """Preserve the capitalization style of the matched phrase."""

    matched_text = match.group(0)

    if matched_text.isupper():
        return replacement.upper()

    if matched_text.istitle():
        return replacement.capitalize()

    if matched_text[0].isupper():
        return replacement[0].upper() + replacement[1:]

    return replacement


# ============================================================
# 6. SKILL DETECTION
# ============================================================

def extract_known_skills(text):
    """Find known skills that appear in the supplied text."""

    normalized = normalize_text(text).lower()
    found_skills = []

    for skill in sorted(KNOWN_SKILLS, key=len, reverse=True):
        if contains_term(normalized, skill):
            found_skills.append(skill)

    return sorted(set(found_skills))


# ============================================================
# 7. IMPROVE A RESUME BULLET POINT
# ============================================================

def improve_bullet_point(text):
    """
    Improve weak wording without inventing skills,
    achievements, numbers, or results.
    """

    original = normalize_text(text)

    if not original:
        return {
            "original": "",
            "improved": "",
            "reason": "No text was provided.",
            "changed": False,
        }

    improved = original

    # Apply one appropriate wording replacement.
    for pattern, replacement in BULLET_REPLACEMENTS:
        updated = re.sub(
            pattern,
            lambda match: replace_preserving_case(
                match,
                replacement,
            ),
            improved,
            count=1,
            flags=re.IGNORECASE,
        )

        if updated != improved:
            improved = updated
            break

    if improved != original:
        reason = (
            "Replaced weak wording with a stronger action phrase. "
            "Verify that the revised sentence accurately describes "
            "your actual contribution."
        )

    else:
        reason = (
            "No automatic wording replacement was suitable. "
            "Consider explaining the specific task, tools used, "
            "your contribution, and the outcome. Include measurable "
            "results only when you have genuine evidence."
        )

    return {
        "original": original,
        "improved": improved,
        "reason": reason,
        "changed": improved != original,
    }


# ============================================================
# 8. EXTRACT RESUME BULLET POINTS
# ============================================================

def extract_resume_bullets(text):
    """Extract likely bullet points and resume statements."""

    bullets = []

    for line in text.splitlines():
        cleaned = line.strip()

        if not cleaned:
            continue

        # Remove bullet symbols and numbering.
        cleaned = re.sub(
            r"^\s*(?:[•●▪◦*–-]|\d+[.)])\s*",
            "",
            cleaned,
        ).strip()

        if len(cleaned.split()) < 4:
            continue

        if len(cleaned) > 400:
            continue

        # Skip common section headings.
        if re.fullmatch(
            r"(summary|education|skills|projects|experience|"
            r"certifications|internships|achievements|objective|"
            r"technical skills|professional experience|"
            r"work experience|contact|personal details|"
            r"career objective)",
            cleaned,
            re.IGNORECASE,
        ):
            continue

        bullets.append(cleaned)

    return bullets


# ============================================================
# 9. DETECT WEAK OR VAGUE STATEMENTS
# ============================================================

WEAK_VERB_PATTERN = re.compile(
    r"^(made|did|worked on|helped|used|handled|"
    r"looked at|created|got|kept|fixed|built|"
    r"showed|found|checked|responsible for)\b",
    re.IGNORECASE,
)

VAGUE_PHRASE_PATTERN = re.compile(
    r"\b("
    r"responsible for|"
    r"worked with|"
    r"worked on various|"
    r"helped with various|"
    r"good knowledge of|"
    r"basic knowledge of"
    r")\b",
    re.IGNORECASE,
)


# ============================================================
# 10. JOB-DESCRIPTION KEYWORD ANALYSIS
# ============================================================

def extract_missing_keywords(resume_text, job_description, limit=10):
    """
    Identify relevant words and known skills in the job description
    that were not detected in the resume.

    These are suggestions for review, not proof that the applicant
    lacks a particular skill.
    """

    resume_text = normalize_text(resume_text).lower()
    job_description = normalize_text(job_description).lower()

    if not job_description:
        return []

    missing_keywords = []

    # First identify missing known technical/professional skills.
    resume_skills = set(extract_known_skills(resume_text))
    job_skills = set(extract_known_skills(job_description))

    for skill in sorted(job_skills - resume_skills):
        missing_keywords.append({
            "keyword": skill,
            "type": "skill",
            "reason": (
                "This skill appears in the job description but "
                "was not detected in the resume."
            ),
        })

    # Remove words already represented by known skill phrases.
    skill_words = set()

    for skill in KNOWN_SKILLS:
        skill_words.update(
            re.findall(
                r"[a-zA-Z][a-zA-Z+#.]*",
                skill.lower(),
            )
        )

    job_words = re.findall(
        r"\b[a-zA-Z][a-zA-Z+#.]{2,}\b",
        job_description,
    )

    word_counts = Counter(
        word
        for word in job_words
        if word not in IGNORED_TERMS
        and word not in skill_words
        and len(word) >= 4
    )

    existing_keywords = {
        item["keyword"]
        for item in missing_keywords
    }

    # Add relevant individual keywords that are absent.
    for word, _ in word_counts.most_common():
        if word in existing_keywords:
            continue

        if contains_term(resume_text, word):
            continue

        missing_keywords.append({
            "keyword": word,
            "type": "keyword",
            "reason": (
                "This term appears in the job description but "
                "was not detected in the resume."
            ),
        })

        existing_keywords.add(word)

        if len(missing_keywords) >= limit:
            break

    return missing_keywords[:limit]


# ============================================================
# 11. GENERATE JOB-SPECIFIC RECOMMENDATIONS
# ============================================================

def generate_job_recommendations(
    resume_text,
    job_description,
):
    """Generate recommendations based on resume/job comparison."""

    recommendations = []

    resume_skills = set(
        extract_known_skills(resume_text)
    )

    job_skills = set(
        extract_known_skills(job_description)
    )

    matched_skills = sorted(
        resume_skills & job_skills
    )

    missing_skills = sorted(
        job_skills - resume_skills
    )

    if matched_skills:
        recommendations.append({
            "priority": "Low",
            "title": "Highlight your matching skills",
            "description": (
                "Your resume already contains these job-related "
                "skills: "
                + ", ".join(matched_skills[:10])
                + "."
            ),
            "action": (
                "Demonstrate these skills through relevant projects, "
                "internships, coursework, or experience."
            ),
        })

    if missing_skills:
        recommendations.append({
            "priority": "High",
            "title": "Review missing job-related skills",
            "description": (
                "These skills appear in the job description but "
                "were not detected in your resume: "
                + ", ".join(missing_skills[:10])
                + "."
            ),
            "action": (
                "Check whether you genuinely have these skills. "
                "If you do, consider describing where you applied "
                "them. Otherwise, consider learning them."
            ),
        })

    return recommendations


# ============================================================
# 12. GENERATE THE IMPROVEMENT REPORT
# ============================================================

def generate_improvement_report(
    resume_text,
    job_description="",
):
    """
    Generate a rule-based resume improvement report.

    Preserves the existing return keys:
        recommendations
        bullet_improvements

    Adds:
        missing_keywords
        matched_skills
        missing_skills
        summary
    """

    text = (
        resume_text
        if isinstance(resume_text, str)
        else ""
    ).strip()

    job_description = (
        job_description
        if isinstance(job_description, str)
        else ""
    ).strip()

    recommendations = []
    bullet_improvements = []

    if not text:
        return {
            "recommendations": [],
            "bullet_improvements": [],
            "missing_keywords": [],
            "matched_skills": [],
            "missing_skills": [],
            "summary": {
                "recommendation_count": 0,
                "bullet_improvement_count": 0,
                "missing_keyword_count": 0,
            },
        }

    resume_lower = text.lower()

    # --------------------------------------------------------
    # CHECK 1: PROFESSIONAL SUMMARY
    # --------------------------------------------------------

    summary_pattern = (
        r"\b(summary|professional summary|career objective|"
        r"professional profile|profile|objective)\b"
    )

    if not re.search(summary_pattern, text, re.IGNORECASE):
        recommendations.append({
            "priority": "Medium",
            "title": "Add a professional summary",
            "description": (
                "A professional summary or career objective "
                "was not clearly detected."
            ),
            "action": (
                "Add 2–3 lines highlighting your relevant skills, "
                "projects, experience, and career goals."
            ),
        })

    # --------------------------------------------------------
    # CHECK 2: MEASURABLE ACHIEVEMENTS
    # --------------------------------------------------------

    quantified_pattern = (
        r"\b\d+(?:\.\d+)?\s*%"
        r"|\b\d+(?:,\d{3})*(?:\.\d+)?\s*\+?\s*"
        r"(?:users|records|customers|reports|projects|"
        r"employees|clients|hours|days|months|years|"
        r"datasets|rows|tables|dashboards|queries)\b"
    )

    if not re.search(
        quantified_pattern,
        text,
        re.IGNORECASE,
    ):
        recommendations.append({
            "priority": "Low",
            "title": "Add measurable results where possible",
            "description": (
                "No obvious numerical achievements were detected."
            ),
            "action": (
                "Where genuine evidence is available, include metrics "
                "such as records analyzed, dashboards created, or "
                "processing time reduced. Never invent numbers."
            ),
        })

    # --------------------------------------------------------
    # CHECK 3: EDUCATION
    # --------------------------------------------------------

    education_pattern = (
        r"\b(education|academic background|qualifications|"
        r"educational qualification)\b"
    )

    if not re.search(
        education_pattern,
        text,
        re.IGNORECASE,
    ):
        recommendations.append({
            "priority": "Low",
            "title": "Review your education section",
            "description": (
                "An education section was not clearly detected."
            ),
            "action": (
                "If relevant, include your degree, institution, "
                "and graduation year."
            ),
        })

    # --------------------------------------------------------
    # CHECK 4: PROJECTS
    # --------------------------------------------------------

    projects_pattern = (
        r"\b(projects|academic projects|personal projects|"
        r"project experience)\b"
    )

    if not re.search(
        projects_pattern,
        text,
        re.IGNORECASE,
    ):
        recommendations.append({
            "priority": "Medium",
            "title": "Highlight relevant projects",
            "description": (
                "A projects section was not clearly detected."
            ),
            "action": (
                "Consider adding relevant projects and describing "
                "your contribution, tools, and outcomes accurately."
            ),
        })

    # --------------------------------------------------------
    # CHECK 5: BULLET POINT IMPROVEMENTS
    # --------------------------------------------------------

    resume_bullets = extract_resume_bullets(text)

    for bullet in resume_bullets:
        weak_verb = bool(
            WEAK_VERB_PATTERN.search(bullet)
        )

        vague_phrase = bool(
            VAGUE_PHRASE_PATTERN.search(bullet)
        )

        if not weak_verb and not vague_phrase:
            continue

        result = improve_bullet_point(bullet)

        # Do not label an unchanged sentence as an improved version.
        if result["improved"] == result["original"]:
            if vague_phrase:
                result["reason"] = (
                    "This statement may be too vague. Describe "
                    "the specific task, tools, and contribution "
                    "that accurately reflect your work."
                )
                result["changed"] = False
                bullet_improvements.append(result)

        else:
            bullet_improvements.append(result)

        if len(bullet_improvements) >= 10:
            break

    # --------------------------------------------------------
    # CHECK 6: JOB-SPECIFIC SKILL ANALYSIS
    # --------------------------------------------------------

    resume_skills = set(
        extract_known_skills(text)
    )

    matched_skills = []
    missing_skills = []
    missing_keywords = []

    if job_description:
        job_skills = set(
            extract_known_skills(job_description)
        )

        matched_skills = sorted(
            resume_skills & job_skills
        )

        missing_skills = sorted(
            job_skills - resume_skills
        )

        recommendations.extend(
            generate_job_recommendations(
                text,
                job_description,
            )
        )

        # ----------------------------------------------------
        # CHECK 7: ADDITIONAL JOB-DESCRIPTION KEYWORDS
        # ----------------------------------------------------

        missing_keywords = extract_missing_keywords(
            text,
            job_description,
            limit=10,
        )

        if missing_keywords:
            keyword_names = [
                item["keyword"]
                for item in missing_keywords
            ]

            recommendations.append({
                "priority": "Medium",
                "title": "Review missing job-description keywords",
                "description": (
                    "These terms were not detected in your resume: "
                    + ", ".join(keyword_names)
                    + "."
                ),
                "action": (
                    "Review each term and include it only when it "
                    "accurately describes your skills or experience. "
                    "Do not add keywords just to increase a score."
                ),
            })

    # --------------------------------------------------------
    # CHECK 8: RETURN THE REPORT
    # --------------------------------------------------------

    return {
        "recommendations": recommendations,
        "bullet_improvements": bullet_improvements,
        "missing_keywords": missing_keywords,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "summary": {
            "recommendation_count": len(recommendations),
            "bullet_improvement_count": len(
                bullet_improvements
            ),
            "missing_keyword_count": len(
                missing_keywords
            ),
        },
    }
