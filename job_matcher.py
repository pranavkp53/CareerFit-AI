import re


# ==================================================
# 1. RECOGNIZED TECHNICAL AND PROFESSIONAL SKILLS
# ==================================================

SKILLS = [
    "python",
    "sql",
    "mysql",
    "oracle",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "matplotlib",
    "machine learning",
    "deep learning",
    "data analysis",
    "data visualization",
    "statistics",
    "data cleaning",
    "exploratory data analysis",
    "data preprocessing",
    "etl",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "spacy",
    "flask",
    "django",
    "html",
    "css",
    "javascript",
    "java",
    "c",
    "c++",
    "git",
    "github",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "linux",
    "rest api",
    "mongodb",
    "postgresql",
    "communication",
    "problem solving",
    "teamwork",
    "leadership",
    "critical thinking",
    "business intelligence",
    "dashboard development",
    "power query",
    "dax",
    "data modeling",
    "data warehousing",
    "predictive analytics",
    "data mining",
    "big data",
    "spark",
    "hadoop",
    "jupyter notebook",
    "regression analysis",
    "classification",
    "clustering",
    "project management",
]


# ==================================================
# 2. SKILL PRIORITY RULES
# ==================================================

# These are configurable defaults, not a guarantee of
# how important a skill is for every particular job.

HIGH_PRIORITY_SKILLS = {
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "java",
    "machine learning",
    "data analysis",
    "data cleaning",
    "statistics",
    "aws",
    "azure",
}

MEDIUM_PRIORITY_SKILLS = {
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "data visualization",
    "exploratory data analysis",
    "data preprocessing",
    "etl",
    "business intelligence",
    "dashboard development",
    "power query",
    "dax",
    "data modeling",
    "data warehousing",
    "rest api",
    "mongodb",
    "postgresql",
    "mysql",
    "oracle",
    "git",
    "github",
}


# ==================================================
# 3. LEARNING SUGGESTIONS
# ==================================================

LEARNING_SUGGESTIONS = {
    "python": (
        "Learn Python fundamentals, functions, data structures, "
        "file handling, and practical scripting."
    ),
    "sql": (
        "Practice SELECT queries, filtering, joins, aggregate "
        "functions, subqueries, and window functions."
    ),
    "excel": (
        "Practice formulas, lookup functions, PivotTables, "
        "charts, and data-cleaning techniques."
    ),
    "power bi": (
        "Learn Power Query, data modeling, DAX measures, "
        "and interactive dashboard development."
    ),
    "tableau": (
        "Practice connecting datasets, building charts, "
        "creating dashboards, and using calculated fields."
    ),
    "pandas": (
        "Practice DataFrame operations, filtering, grouping, "
        "merging, missing-value handling, and data cleaning."
    ),
    "numpy": (
        "Learn arrays, indexing, vectorized operations, "
        "and numerical calculations."
    ),
    "matplotlib": (
        "Practice line charts, bar charts, histograms, "
        "labels, legends, and data visualization."
    ),
    "machine learning": (
        "Learn supervised and unsupervised learning, "
        "model training, evaluation, and data preparation."
    ),
    "deep learning": (
        "Study neural networks, activation functions, "
        "backpropagation, and model evaluation."
    ),
    "data analysis": (
        "Practice cleaning datasets, exploratory analysis, "
        "identifying trends, and communicating findings."
    ),
    "data visualization": (
        "Learn to select appropriate charts, communicate "
        "trends, and build clear visual summaries."
    ),
    "statistics": (
        "Review descriptive statistics, probability, "
        "distributions, hypothesis testing, and correlation."
    ),
    "data cleaning": (
        "Practice handling missing values, duplicates, "
        "inconsistent formats, and invalid records."
    ),
    "exploratory data analysis": (
        "Practice summary statistics, distributions, "
        "outlier analysis, and relationships between variables."
    ),
    "scikit-learn": (
        "Practice preprocessing data, fitting models, "
        "cross-validation, and evaluating model performance."
    ),
    "tensorflow": (
        "Learn tensor operations, neural networks, "
        "model training, and evaluation."
    ),
    "pytorch": (
        "Practice tensors, automatic differentiation, "
        "neural networks, and model training."
    ),
    "etl": (
        "Learn how to extract data, transform it, "
        "validate it, and load it into a destination."
    ),
    "business intelligence": (
        "Learn reporting, KPI tracking, data modeling, "
        "and communicating business insights."
    ),
    "dashboard development": (
        "Build interactive dashboards with clear KPIs, "
        "filters, charts, and useful summaries."
    ),
    "power query": (
        "Practice importing, transforming, merging, "
        "and cleaning data in Power Query."
    ),
    "dax": (
        "Learn DAX measures, filter context, CALCULATE, "
        "and common aggregation and iterator functions."
    ),
    "java": (
        "Practice Java syntax, object-oriented programming, "
        "collections, exception handling, and problem-solving."
    ),
    "flask": (
        "Learn routes, request handling, templates, "
        "form validation, and API development."
    ),
    "django": (
        "Study Django models, views, templates, forms, "
        "authentication, and database integration."
    ),
    "aws": (
        "Study cloud fundamentals, IAM, storage, computing, "
        "networking, and security basics."
    ),
    "azure": (
        "Learn cloud concepts, identity management, storage, "
        "computing, and monitoring."
    ),
    "git": (
        "Practice commits, branches, merges, conflict resolution, "
        "and collaboration workflows."
    ),
    "github": (
        "Practice repositories, branches, pull requests, "
        "issues, and project documentation."
    ),
    "mongodb": (
        "Learn document databases, CRUD operations, "
        "filtering, indexing, and aggregation pipelines."
    ),
    "postgresql": (
        "Practice SQL queries, joins, constraints, indexing, "
        "and relational database design."
    ),
    "mysql": (
        "Practice relational database design, SQL queries, "
        "joins, aggregation, and constraints."
    ),
    "oracle": (
        "Practice Oracle SQL, joins, subqueries, functions, "
        "and analytical queries."
    ),
    "rest api": (
        "Learn HTTP methods, status codes, JSON, API requests, "
        "authentication, and error handling."
    ),
    "teamwork": (
        "Build collaboration skills through team projects, "
        "clear communication, and shared responsibilities."
    ),
    "communication": (
        "Practice explaining technical work clearly, "
        "writing concise reports, and presenting findings."
    ),
    "problem solving": (
        "Practice breaking problems into smaller steps, "
        "testing solutions, and explaining your reasoning."
    ),
}


# ==================================================
# 4. TEXT NORMALIZATION
# ==================================================

def normalize_text(text):
    """Convert text to lowercase and normalize whitespace."""

    if not isinstance(text, str):
        return ""

    return re.sub(r"\s+", " ", text.lower()).strip()


# ==================================================
# 5. SKILL MATCHING
# ==================================================

def contains_skill(text, skill):
    """Check whether a complete skill term exists in the text."""

    pattern = (
        r"(?<!\w)"
        + re.escape(skill.lower())
        + r"(?!\w)"
    )

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    ) is not None


def find_skills(text):
    """Return recognized skills found in the supplied text."""

    normalized = normalize_text(text)

    if not normalized:
        return []

    found = []

    for skill in SKILLS:
        if contains_skill(normalized, skill):
            found.append(skill)

    return sorted(set(found))


# ==================================================
# 6. PRIORITIZE MISSING SKILLS
# ==================================================

def get_skill_priority(skill):
    """
    Return a configurable default priority for a missing skill.

    Actual priority depends on the specific job description.
    """

    normalized_skill = skill.lower()

    if normalized_skill in HIGH_PRIORITY_SKILLS:
        return "High"

    if normalized_skill in MEDIUM_PRIORITY_SKILLS:
        return "Medium"

    return "Low"


# ==================================================
# 7. LEARNING RECOMMENDATIONS
# ==================================================

def get_learning_suggestion(skill):
    """Return a learning suggestion for a recognized skill."""

    normalized_skill = skill.lower()

    if normalized_skill in LEARNING_SUGGESTIONS:
        return LEARNING_SUGGESTIONS[normalized_skill]

    return (
        f"Study the fundamentals of {skill}, practice with "
        "small exercises, and build a project demonstrating "
        "your understanding."
    )


# ==================================================
# 8. MAIN RESUME ANALYSIS
# ==================================================

def analyze_resume(resume_text, job_description):
    """
    Compare recognized resume skills with job requirements.

    Existing response fields are preserved. Additional fields
    provide priorities and learning suggestions.
    """

    if (
        not isinstance(resume_text, str)
        or not resume_text.strip()
    ):
        raise ValueError("Resume text cannot be empty.")

    if (
        not isinstance(job_description, str)
        or not job_description.strip()
    ):
        raise ValueError("Job description cannot be empty.")

    # Detect recognized skills.
    resume_skills = set(find_skills(resume_text))
    required_skills = set(find_skills(job_description))

    # Compare resume skills against detected requirements.
    matched_skills = sorted(
        resume_skills & required_skills
    )

    missing_skills = sorted(
        required_skills - resume_skills
    )

    # Calculate overlap between recognized skills.
    if required_skills:
        match_score = round(
            len(matched_skills)
            / len(required_skills)
            * 100,
            2,
        )
    else:
        match_score = 0.0

    # Build gap-analysis details.
    skill_gaps = []

    for skill in missing_skills:
        skill_gaps.append({
            "skill": skill,
            "priority": get_skill_priority(skill),
            "learning_suggestion": get_learning_suggestion(skill),
        })

    # Group missing skills by default priority.
    missing_by_priority = {
        "High": [],
        "Medium": [],
        "Low": [],
    }

    for gap in skill_gaps:
        missing_by_priority[gap["priority"]].append(
            gap["skill"]
        )

    # Return existing fields plus the new gap-analysis fields.
    return {
        "match_score": match_score,
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(required_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": len(required_skills),
        "total_matched_skills": len(matched_skills),

        # Phase 8 additions.
        "skill_gaps": skill_gaps,
        "missing_skills_by_priority": missing_by_priority,
        "total_missing_skills": len(missing_skills),
        "gap_analysis_available": bool(required_skills),
    }