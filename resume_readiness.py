import re

from services.ats_checker import (
    contains_term,
    extract_recognized_skills,
)


# ==========================================
# 1. RESUME SECTION KEYWORDS
# ==========================================

SECTION_KEYWORDS = {
    "Professional Summary": [
        "professional summary",
        "summary",
        "profile",
        "career objective",
        "objective",
        "about me",
    ],
    "Education": [
        "education",
        "academic background",
        "qualification",
        "educational background",
    ],
    "Projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience",
    ],
    "Experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships",
    ],
    "Skills": [
        "skills",
        "technical skills",
        "core competencies",
        "technical expertise",
    ],
}


# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def find_resume_sections(resume_text):
    """
    Detect common resume sections.

    Returns a dictionary indicating whether each section
    appears to be present in the resume.
    """

    sections_found = {}

    for section, keywords in SECTION_KEYWORDS.items():

        found = any(
            contains_term(resume_text, keyword)
            for keyword in keywords
        )

        sections_found[section] = found

    return sections_found


def calculate_keyword_coverage(resume_text, job_description):
    """
    Calculate job-related skill coverage.

    Only skills recognized by the existing ATS checker
    are included in this calculation.
    """

    if not job_description.strip():
        return {
            "score": None,
            "matched_skills": [],
            "missing_skills": [],
            "total_required_skills": 0,
            "message": (
                "Add a job description to calculate "
                "job-specific keyword coverage."
            ),
        }

    required_skills = extract_recognized_skills(
        job_description
    )

    resume_skills = extract_recognized_skills(
        resume_text
    )

    resume_skill_set = set(resume_skills)

    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_skill_set
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skill_set
    ]

    if not required_skills:
        coverage_score = None

        message = (
            "No recognized technical or professional skills "
            "were detected in the job description."
        )

    else:
        coverage_score = round(
            len(matched_skills)
            / len(required_skills)
            * 100,
            2,
        )

        message = (
            "Keyword coverage is based on recognized skills "
            "present in the job description."
        )

    return {
        "score": coverage_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": len(required_skills),
        "message": message,
    }


# ==========================================
# 3. CONTENT QUALITY SCORE
# ==========================================

def calculate_content_quality(
    resume_text,
    sections_found,
):
    """
    Calculate content quality out of 100.

    Checks:
    - Professional summary: 20 points
    - Education: 20 points
    - Projects: 20 points
    - Experience: 20 points
    - Skills: 20 points
    """

    checks = []
    score = 0

    for section, present in sections_found.items():

        points = 20
        earned_points = points if present else 0

        checks.append({
            "name": section,
            "passed": present,
            "points": points,
            "earned_points": earned_points,
        })

        score += earned_points

    word_count = len(
        re.findall(r"\b[\w+#.-]+\b", resume_text)
    )

    feedback = []

    if word_count < 150:
        feedback.append(
            "Your resume appears short. Review whether you "
            "have included enough relevant information."
        )

    elif word_count > 1200:
        feedback.append(
            "Your resume is lengthy. Consider removing "
            "repetition and less relevant details."
        )

    if not sections_found["Professional Summary"]:
        feedback.append(
            "Consider adding a short professional summary "
            "or career objective."
        )

    if not sections_found["Education"]:
        feedback.append(
            "Add a clearly labelled Education section "
            "if applicable."
        )

    if not sections_found["Projects"]:
        feedback.append(
            "Include relevant projects and explain your "
            "contributions where applicable."
        )

    if not sections_found["Experience"]:
        feedback.append(
            "Include relevant work experience or internships "
            "if you have them."
        )

    if not sections_found["Skills"]:
        feedback.append(
            "Add a clearly labelled Skills section."
        )

    return {
        "score": score,
        "checks": checks,
        "word_count": word_count,
        "feedback": feedback,
    }


# ==========================================
# 4. JOB RELEVANCE SCORE
# ==========================================

def calculate_job_relevance(
    resume_text,
    job_description,
):
    """
    Estimate how relevant the resume is to the job.

    Recognized skills are compared between the resume
    and the job description.

    If no job description is provided, the score is
    unavailable rather than being treated as zero.
    """

    if not job_description.strip():
        return {
            "score": None,
            "matched_skills": [],
            "missing_skills": [],
            "message": (
                "Provide a job description to calculate "
                "job relevance."
            ),
        }

    required_skills = extract_recognized_skills(
        job_description
    )

    resume_skills = extract_recognized_skills(
        resume_text
    )

    resume_skill_set = set(resume_skills)

    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_skill_set
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skill_set
    ]

    if not required_skills:
        return {
            "score": None,
            "matched_skills": [],
            "missing_skills": [],
            "message": (
                "No recognized skills were detected in the "
                "job description, so job relevance cannot "
                "be calculated reliably."
            ),
        }

    score = round(
        len(matched_skills)
        / len(required_skills)
        * 100,
        2,
    )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "message": (
            "This score estimates skill alignment. It does "
            "not measure every job requirement."
        ),
    }


# ==========================================
# 5. GENERATE ACTIONABLE FEEDBACK
# ==========================================

def generate_readiness_feedback(
    sections_found,
    keyword_coverage,
    job_relevance,
    content_quality,
):
    """
    Generate feedback based on detected gaps.
    """

    feedback = []

    for section, present in sections_found.items():

        if not present:
            feedback.append({
                "category": "Content Quality",
                "priority": (
                    "High"
                    if section in ("Education", "Skills")
                    else "Medium"
                ),
                "title": f"Review your {section} section",
                "action": (
                    f"Add a clearly labelled {section} section "
                    "if it is relevant to your background."
                ),
            })

    if keyword_coverage["score"] is not None:

        if keyword_coverage["missing_skills"]:

            missing = ", ".join(
                keyword_coverage["missing_skills"][:8]
            )

            feedback.append({
                "category": "Keyword Coverage",
                "priority": "High",
                "title": "Review missing job-related skills",
                "action": (
                    f"Check these skills against your actual "
                    f"knowledge and experience: {missing}. "
                    "Include only skills you genuinely possess."
                ),
            })

    if job_relevance["score"] is not None:

        if job_relevance["score"] < 50:
            feedback.append({
                "category": "Job Relevance",
                "priority": "High",
                "title": "Improve alignment with the target role",
                "action": (
                    "Review the job description and identify "
                    "relevant skills, projects, and experience "
                    "that you can accurately demonstrate."
                ),
            })

        elif job_relevance["score"] < 80:
            feedback.append({
                "category": "Job Relevance",
                "priority": "Medium",
                "title": "Strengthen job-specific alignment",
                "action": (
                    "Review the missing recognized skills and "
                    "highlight relevant experience where accurate."
                ),
            })

    if content_quality["word_count"] < 150:
        feedback.append({
            "category": "Content Quality",
            "priority": "High",
            "title": "Review resume completeness",
            "action": (
                "Check whether relevant education, skills, "
                "projects, experience, and achievements are "
                "included in the resume."
            ),
        })

    if not feedback:
        feedback.append({
            "category": "General",
            "priority": "Low",
            "title": "Continue tailoring your resume",
            "action": (
                "Review your resume against the target job "
                "and ensure all listed skills and achievements "
                "are accurate."
            ),
        })

    return feedback


# ==========================================
# 6. MAIN READINESS SCORE FUNCTION
# ==========================================

def calculate_resume_readiness(
    resume_text,
    job_description="",
):
    """
    Calculate a separate Resume Readiness Score out of 100.

    Scoring:
    - Content Quality: 40%
    - Job Relevance: 35%
    - Keyword Coverage: 25%

    When a job description is not provided, the score is
    based on content quality alone. The response clearly
    indicates that job-specific checks are unavailable.

    This is a rule-based estimate, not an ATS guarantee.
    """

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text is required.")

    if not isinstance(job_description, str):
        job_description = ""

    resume_text = resume_text.strip()
    job_description = job_description.strip()

    sections_found = find_resume_sections(resume_text)

    content_quality = calculate_content_quality(
        resume_text,
        sections_found,
    )

    job_relevance = calculate_job_relevance(
        resume_text,
        job_description,
    )

    keyword_coverage = calculate_keyword_coverage(
        resume_text,
        job_description,
    )

    feedback = generate_readiness_feedback(
        sections_found,
        keyword_coverage,
        job_relevance,
        content_quality,
    )

    # Calculate the final score using only available components.
    components = [
        {
            "name": "Content Quality",
            "score": content_quality["score"],
            "weight": 40,
        }
    ]

    if job_relevance["score"] is not None:
        components.append({
            "name": "Job Relevance",
            "score": job_relevance["score"],
            "weight": 35,
        })

    if keyword_coverage["score"] is not None:
        components.append({
            "name": "Keyword Coverage",
            "score": keyword_coverage["score"],
            "weight": 25,
        })

    # Normalize the available weights so the score stays out of 100.
    total_weight = sum(
        component["weight"]
        for component in components
    )

    readiness_score = round(
        sum(
            component["score"] * component["weight"]
            for component in components
        )
        / total_weight,
        2,
    )

    if job_description:
        score_basis = "Resume and Job Description"
    else:
        score_basis = "resume_content_only"

    return {
        "readiness_score": readiness_score,
        "score_basis": score_basis,
        "components": components,
        "content_quality": content_quality,
        "job_relevance": job_relevance,
        "keyword_coverage": keyword_coverage,
        "sections_found": sections_found,
        "feedback": feedback,
        "disclaimer": (
            "This is a rule-based estimate of resume readiness. "
            "It does not guarantee ATS acceptance, interview "
            "selection, or job suitability."
        ),
    }