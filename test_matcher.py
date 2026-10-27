
from services.job_matcher import analyze_resume

resume = """
Data Analyst with experience in Python, SQL, Excel and Power BI.
Used Pandas for data cleaning and data visualization.
"""

job_description = """
We need a Data Analyst with Python, SQL, Power BI,
Tableau, statistics and machine learning skills.
"""

result = analyze_resume(resume, job_description)

print("Match score:", result["match_score"], "%")
print("Resume skills:", result["resume_skills"])
print("Matched skills:", result["matched_skills"])
print("Missing skills:", result["missing_skills"])
