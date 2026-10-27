import re


# ========================================
# 1. STANDARD RESUME SECTION KEYWORDS
# ========================================

SECTION_KEYWORDS = {
    "Education": [
        "education",
        "academic background",
        "qualification",
    ],
    "Skills": [
        "skills",
        "technical skills",
        "core competencies",
    ],
    "Projects": [
        "projects",
        "academic projects",
        "personal projects",
    ],
    "Experience": [
        "experience",
        "work experience",
        "internship",
        "professional experience",
    ],
}


# ========================================
# 2. ACTION VERBS
# ========================================

ACTION_VERBS = [
    "developed",
    "implemented",
    "created",
    "analyzed",
    "designed",
    "built",
    "improved",
    "managed",
    "automated",
    "tested",
    "optimized",
    "achieved",
]


# ========================================
# 3. RECOGNIZED TECHNICAL AND PROFESSIONAL SKILLS
# ========================================

COMMON_SKILLS = [
    "python",
    "java",
    "sql",
    "mysql",
    "oracle",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "machine learning",
    "data analysis",
    "data cleaning",
    "communication",
    "problem solving",
    "etl",
    "postgresql",
    "git",
    "github",
    "html",
    "css",
    "javascript",
    "flask",
    "statistics",
    "data visualization",
    "data analytics",
    "data science",
    "deep learning",
    "artificial intelligence",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "matplotlib",
    "seaborn",
    "power query",
    "dax",
    "pivot tables",
    "vlookup",
    "xlookup",
    "data modeling",
    "dashboard development",
    "database management",
    "database design",
    "exploratory data analysis",
    "natural language processing",
    "aws",
    "azure",
    "google cloud",
    "docker",
    "kubernetes",
    "linux",
    "gitlab",
    "rest api",
    "fastapi",
    "django",
    "html5",
    "css3",
    "c",
    "c++",
    "c#",
    "r programming",
    "sas",
    "spark",
    "hadoop",
    "mongodb",
    "redis",
    "postgres",
    "agile",
    "scrum",
    "data structures",
    "algorithms",
    "oop",
    "object oriented programming",
    "software testing",
    "unit testing",
    "cybersecurity",
    "networking",
    "cloud computing",
]


# ========================================
# 4. WORDS THAT MUST NOT BE TREATED AS SKILLS
# ========================================

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "if",
    "in", "on", "at", "to", "for", "from", "of",
    "with", "by", "as", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "should",
    "can", "could", "may", "might", "must",
    "this", "that", "these", "those", "it", "its",
    "you", "your", "we", "our", "they", "their",
    "who", "what", "when", "where", "why", "how",
    "here", "there", "complete", "copy", "paste",
    "pasteable", "description", "tailored", "immediate",
    "please", "kindly", "also", "more", "most",
    "some", "any", "all", "each", "every", "other",
    "such", "very", "much", "many", "well",
    "good", "great", "strong", "excellent",
    "required", "preferred", "desired", "relevant",
    "responsible", "responsibilities", "requirements",
    "requirement", "candidate", "candidates",
    "applicant", "applicants", "position", "role",
    "job", "jobs", "company", "team", "work",
    "working", "ability", "abilities", "knowledge",
    "understanding", "experience", "skills",
    "skill", "qualification", "qualifications",
    "including", "include", "includes", "using",
    "use", "used", "support", "supporting",
    "ensure", "ensuring", "provide", "providing",
    "help", "helping", "looking", "seeking",
    "apply", "applying", "application",
    "improve", "improving", "enhance", "enhancing",
    "develop", "developing", "maintain", "maintaining",
    "manage", "managing", "perform", "performing",
    "various", "multiple", "related", "based",
    "within", "across", "through", "about",
    "new", "different", "appropriate", "immediate",
    "analyst", "description", "tailored",
}


# ========================================
# 5. MATCH SKILLS AS COMPLETE TERMS
# ========================================

def contains_term(text, term):
    """
    Match a complete word or phrase instead of a substring.

    Examples:
    - 'sql' matches 'SQL'
    - 'java' does not match 'JavaScript'
    - 'power bi' matches 'Power BI'
    """

    text = text.lower()
    term = term.lower()

    pattern = (
        r"(?<![a-zA-Z0-9+#])"
        + re.escape(term)
        + r"(?![a-zA-Z0-9+#])"
    )

    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def extract_recognized_skills(text):
    """
    Extract only skills included in COMMON_SKILLS.

    Ordinary words are not treated as missing skills.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    found_skills = []

    for skill in COMMON_SKILLS:
        if contains_term(text, skill):
            found_skills.append(skill)

    return found_skills


def get_missing_job_skills(resume_text, job_description):
    """
    Compare recognized job-description skills against the resume.

    Returns only known skills that occur in the job description
    but are not detected in the resume.
    """

    required_skills = extract_recognized_skills(job_description)
    resume_skills = extract_recognized_skills(resume_text)

    resume_skills_set = set(resume_skills)

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skills_set
    ]

    return missing_skills


# ========================================
# 6. ADD A RECOMMENDATION
# ========================================

def add_recommendation(
    recommendations,
    priority,
    title,
    description,
    action,
):
    """
    Add a recommendation without duplicating it.
    """

    # Prevent duplicate recommendations with the same title.
    for existing in recommendations:
        if existing["title"] == title:
            return

    recommendations.append({
        "priority": priority,
        "title": title,
        "description": description,
        "action": action,
    })


# ========================================
# 7. MAIN ATS CHECKER
# ========================================

def check_resume(resume_text, job_description=""):
    """
    Perform rule-based ATS checks.

    The existing ATS scoring system remains out of 100.
    Job-specific recommendations use recognized skills only.
    """

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    if not isinstance(job_description, str):
        job_description = ""

    text = resume_text.strip()
    lower_text = text.lower()
    lower_job_description = job_description.lower()

    checks = []
    suggestions = []
    recommendations = []
    score = 0

    # ========================================
    # CHECK 1: EMAIL ADDRESS — 15 POINTS
    # ========================================

    has_email = bool(
        re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text,
        )
    )

    checks.append({
        "name": "Email address",
        "passed": has_email,
        "points": 15,
        "earned_points": 15 if has_email else 0,
    })

    if has_email:
        score += 15
    else:
        message = (
            "Add a professional email address to your contact information."
        )

        suggestions.append(message)

        add_recommendation(
            recommendations,
            "High",
            "Add an email address",
            "Your resume does not appear to contain an email address.",
            "Add a professional email address near the top of your resume.",
        )

    # ========================================
    # CHECK 2: PHONE NUMBER — 10 POINTS
    # ========================================

    has_phone = bool(
        re.search(
            r"(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)",
            text,
        )
    )

    checks.append({
        "name": "Phone number",
        "passed": has_phone,
        "points": 10,
        "earned_points": 10 if has_phone else 0,
    })

    if has_phone:
        score += 10
    else:
        message = (
            "Add a contact phone number if appropriate for your applications."
        )

        suggestions.append(message)

        add_recommendation(
            recommendations,
            "Medium",
            "Add contact information",
            "No phone number was detected in the resume text.",
            "Add a reachable phone number if appropriate for the job.",
        )

    # ========================================
    # CHECK 3: STANDARD RESUME SECTIONS — 40 POINTS
    # ========================================

    sections_found = []

    for section, keywords in SECTION_KEYWORDS.items():
        found = any(
            contains_term(lower_text, keyword)
            for keyword in keywords
        )

        checks.append({
            "name": section + " section",
            "passed": found,
            "points": 10,
            "earned_points": 10 if found else 0,
        })

        if found:
            sections_found.append(section)
            score += 10

        else:
            message = (
                f"Consider adding a clearly labelled {section} section "
                "if relevant to your background."
            )

            suggestions.append(message)

            add_recommendation(
                recommendations,
                "High" if section in ("Skills", "Education") else "Medium",
                f"Review your {section.lower()} section",
                f"No clearly recognized {section.lower()} section was found.",
                f"Add a clearly labelled {section} section if relevant "
                "to your background.",
            )

    # ========================================
    # CHECK 4: RESUME LENGTH — 15 POINTS
    # ========================================

    word_count = len(re.findall(r"\b[\w+#.-]+\b", text))
    reasonable_length = 150 <= word_count <= 1200

    checks.append({
        "name": "Resume text length",
        "passed": reasonable_length,
        "points": 15,
        "earned_points": 15 if reasonable_length else 0,
    })

    if reasonable_length:
        score += 15

    elif word_count < 150:
        message = (
            "Your resume text is quite short. Add relevant projects, "
            "skills, education, and achievements where applicable."
        )

        suggestions.append(message)

        add_recommendation(
            recommendations,
            "High",
            "Add relevant resume content",
            f"Only {word_count} words were detected in your resume.",
            "Review the extracted text and add relevant projects, skills, "
            "education, experience, and achievements where applicable.",
        )

    else:
        message = (
            "Consider removing repetitive or less relevant content "
            "to make your resume more concise."
        )

        suggestions.append(message)

        add_recommendation(
            recommendations,
            "Medium",
            "Make your resume more concise",
            f"{word_count} words were detected in your resume.",
            "Remove repetition and prioritize information relevant to "
            "the job you are applying for.",
        )

    # ========================================
    # CHECK 5: ACTION VERBS — 20 POINTS
    # ========================================

    action_verbs_found = [
        verb
        for verb in ACTION_VERBS
        if contains_term(lower_text, verb)
    ]

    has_action_verbs = len(action_verbs_found) >= 2

    checks.append({
        "name": "Action-oriented language",
        "passed": has_action_verbs,
        "points": 20,
        "earned_points": 20 if has_action_verbs else 0,
    })

    if has_action_verbs:
        score += 20

    else:
        message = (
            "Use specific action verbs to describe your work, "
            "such as developed, implemented, analyzed, or automated."
        )

        suggestions.append(message)

        add_recommendation(
            recommendations,
            "Medium",
            "Use stronger action verbs",
            "Fewer than two recognized action verbs were found.",
            "Describe what you actually did using specific verbs such as "
            "developed, analyzed, implemented, designed, or tested.",
        )

    # ========================================
    # CHECK 6: JOB-SPECIFIC SKILL RECOMMENDATIONS
    # ========================================

    if lower_job_description.strip():

        missing_skills = get_missing_job_skills(
            text,
            lower_job_description,
        )

        if missing_skills:
            skills_text = ", ".join(missing_skills)

            suggestions.append(
                "Review these recognized job-related skills that were "
                "not detected in your resume: "
                + skills_text
                + "."
            )

            add_recommendation(
                recommendations,
                "High",
                "Review skills required by the job",
                "The following recognized skills appear in the job "
                "description but were not detected in your resume: "
                + skills_text
                + ".",
                "Check each skill against your actual knowledge and "
                "experience. Include relevant skills only if you genuinely "
                "have them, and demonstrate them through projects or work "
                "experience where possible.",
            )

    # ========================================
    # CHECK 7: RESUME TEXT EXTRACTION
    # ========================================

    if len(text.splitlines()) < 5:
        message = (
            "Check that your resume text was extracted correctly. "
            "A scanned or image-based PDF may need OCR."
        )

        suggestions.append(message)

        add_recommendation(
            recommendations,
            "High",
            "Check resume text extraction",
            "Very few lines of text were extracted from the resume.",
            "Check the parsed resume text. If the PDF contains scanned "
            "pages or images, OCR may be needed.",
        )

    # ========================================
    # CHECK 8: SORT RECOMMENDATIONS BY PRIORITY
    # ========================================

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
    }

    recommendations.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    # ========================================
    # FINAL RESULT
    # ========================================

    return {
        "ats_score": min(score, 100),
        "word_count": word_count,
        "sections_found": sections_found,
        "action_verbs_found": action_verbs_found,
        "checks": checks,
        "suggestions": suggestions,
        "recommendations": recommendations,
    }

