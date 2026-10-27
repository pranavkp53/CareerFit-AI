
# services/job_recommender.py

import re


# Job roles and their required skills
JOB_ROLES = {
    "Data Analyst": {
        "skills": [
            "python",
            "sql",
            "excel",
            "power bi",
            "tableau",
            "statistics",
            "data visualization"
        ],
        "learning": [
            "Advanced SQL",
            "Statistics",
            "Data visualization",
            "Dashboard development"
        ]
    },

    "Python Developer": {
        "skills": [
            "python",
            "flask",
            "django",
            "rest api",
            "git",
            "sql"
        ],
        "learning": [
            "Flask or Django",
            "REST APIs",
            "Git and GitHub",
            "Backend development"
        ]
    },

    "Junior Data Scientist": {
        "skills": [
            "python",
            "sql",
            "statistics",
            "machine learning",
            "pandas",
            "numpy",
            "data visualization"
        ],
        "learning": [
            "Machine learning",
            "Statistics",
            "Pandas and NumPy",
            "Model evaluation"
        ]
    },

    "Business Intelligence Analyst": {
        "skills": [
            "sql",
            "power bi",
            "tableau",
            "excel",
            "data visualization",
            "dax"
        ],
        "learning": [
            "Advanced Power BI",
            "DAX",
            "Data modeling",
            "Advanced SQL"
        ]
    },

    "Machine Learning Engineer": {
        "skills": [
            "python",
            "machine learning",
            "scikit-learn",
            "pandas",
            "numpy",
            "tensorflow",
            "deep learning"
        ],
        "learning": [
            "Machine learning algorithms",
            "Model deployment",
            "Deep learning",
            "Model evaluation"
        ]
    }
}


def extract_skills(resume_text):
    """
    Identify recognized skills mentioned in the resume.
    """

    text = resume_text.lower()
    detected_skills = set()

    for role_details in JOB_ROLES.values():
        for skill in role_details["skills"]:
            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text):
                detected_skills.add(skill)

    return detected_skills


def recommend_jobs(resume_text):
    """
    Recommend job roles based on skills found in the resume.
    """

    if not resume_text or not resume_text.strip():
        return {
            "detected_skills": [],
            "recommendations": []
        }

    detected_skills = extract_skills(resume_text)
    recommendations = []

    for role, details in JOB_ROLES.items():

        required_skills = set(details["skills"])

        matched_skills = detected_skills.intersection(
            required_skills
        )

        missing_skills = required_skills - detected_skills

        match_score = round(
            (len(matched_skills) / len(required_skills)) * 100
        )

        # Recommend roles with at least one matching skill
        if matched_skills:

            recommendations.append({
                "job_role": role,
                "match_score": match_score,
                "matched_skills": sorted(matched_skills),
                "missing_skills": sorted(missing_skills),
                "learning_suggestions": details["learning"]
            })

    # Show the strongest matches first
    recommendations.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return {
        "detected_skills": sorted(detected_skills),
        "recommendations": recommendations
    }
