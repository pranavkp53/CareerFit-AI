import uuid
import json
from pathlib import Path
from collections import Counter
from services.resume_readiness import calculate_resume_readiness
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from database import get_connection
from services.resume_parser import extract_resume_text
from services.job_matcher import analyze_resume
from services.ats_checker import check_resume
from services.resume_improver import generate_improvement_report
from services.job_recommender import recommend_jobs


app = Flask(__name__)


# ============================================================
# UPLOAD CONFIGURATION
# ============================================================

UPLOAD_FOLDER = Path(app.root_path) / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def parse_analysis_result(value):
    """
    Convert a saved analysis result into a Python dictionary.
    """

    if isinstance(value, dict):
        return value

    if isinstance(value, str):
        try:
            parsed_value = json.loads(value)

            if isinstance(parsed_value, dict):
                return parsed_value

        except (ValueError, TypeError):
            pass

    return {}


def normalize_skill_list(value):
    """
    Normalize skill data into a list of readable strings.
    """

    if not isinstance(value, list):
        return []

    normalized = []

    for item in value:
        if isinstance(item, str):
            skill = item.strip()

        elif isinstance(item, dict):
            skill = (
                item.get("skill")
                or item.get("name")
                or item.get("keyword")
                or ""
            )

            skill = str(skill).strip()

        else:
            continue

        if skill:
            normalized.append(skill)

    return normalized


def extract_missing_skills(analysis_result):
    """
    Extract missing skills from commonly used result keys.
    """

    possible_keys = [
        "missing_skills",
        "skills_missing",
        "missing_keywords",
        "missing",
    ]

    for key in possible_keys:
        if key in analysis_result:
            skills = normalize_skill_list(analysis_result[key])

            if skills:
                return skills

    for parent_key in [
        "skill_analysis",
        "skills_analysis",
        "skills",
    ]:
        nested_data = analysis_result.get(parent_key)

        if isinstance(nested_data, dict):
            for key in possible_keys:
                if key in nested_data:
                    skills = normalize_skill_list(
                        nested_data[key]
                    )

                    if skills:
                        return skills

    return []


def extract_matched_skills(analysis_result):
    """
    Extract matched skills from commonly used result keys.
    """

    possible_keys = [
        "matched_skills",
        "skills_matched",
        "matched_keywords",
        "matched",
    ]

    for key in possible_keys:
        if key in analysis_result:
            skills = normalize_skill_list(
                analysis_result[key]
            )

            if skills:
                return skills

    for parent_key in [
        "skill_analysis",
        "skills_analysis",
        "skills",
    ]:
        nested_data = analysis_result.get(parent_key)

        if isinstance(nested_data, dict):
            for key in possible_keys:
                if key in nested_data:
                    skills = normalize_skill_list(
                        nested_data[key]
                    )

                    if skills:
                        return skills

    return []


def format_datetime(value, date_format="%d %b %Y"):
    """
    Format a datetime value for JSON responses.
    """

    if value is None:
        return None

    if hasattr(value, "strftime"):
        return value.strftime(date_format)

    return str(value)


# ============================================================
# DASHBOARD PAGE
# ============================================================

@app.route("/")
def dashboard():
    return render_template("index.html")


# ============================================================
# RESUME ANALYSIS PAGE
# ============================================================

@app.route("/analyze", methods=["GET"])
def analyze():
    return render_template("analyze.html")


# ============================================================
# RESUME PARSER API
# ============================================================

@app.route("/api/resume/parse", methods=["POST"])
def parse_resume():

    if "resume" not in request.files:
        return jsonify({
            "error": "Please select a resume file."
        }), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({
            "error": "No file selected."
        }), 400

    original_name = secure_filename(file.filename)
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({
            "error": "Only PDF and DOCX files are supported."
        }), 400

    saved_name = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_FOLDER / saved_name

    try:
        file.save(str(file_path))

        resume_text = extract_resume_text(file_path)

        return jsonify({
            "message": "Resume uploaded and parsed successfully.",
            "file_name": original_name,
            "resume_text": resume_text
        }), 200

    except ValueError as error:
        file_path.unlink(missing_ok=True)

        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        file_path.unlink(missing_ok=True)

        app.logger.exception("Resume parsing failed.")

        return jsonify({
            "error": (
                "Unable to process this resume. "
                "Please try another file."
            )
        }), 500


# ============================================================
# FILE SIZE ERROR HANDLER
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({
        "error": "The resume file must be 5 MB or smaller."
    }), 413


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "application": "CareerFit AI"
    })


# ============================================================
# RESUME ANALYSIS API — PHASE 8 GAP ANALYSIS
# ============================================================

@app.route("/api/analyze", methods=["POST"])
def run_analysis():
    data = request.get_json(silent=True)

    # Validate incoming JSON.
    if not isinstance(data, dict):
        return jsonify({
            "error": "Please provide valid JSON input."
        }), 400

    resume_text = data.get("resume_text", "")
    job_title = data.get("job_title", "")
    company_name = data.get("company_name", "")
    job_description = data.get("job_description", "")
    resume_file_name = data.get("resume_file_name", "")

    # Validate input types.
    if not all(
        isinstance(value, str)
        for value in [
            resume_text,
            job_title,
            company_name,
            job_description,
            resume_file_name,
        ]
    ):
        return jsonify({
            "error": "All supplied fields must be strings."
        }), 400

    # Clean input.
    resume_text = resume_text.strip()
    job_title = job_title.strip()
    company_name = company_name.strip()
    job_description = job_description.strip()
    resume_file_name = resume_file_name.strip()

    # Validate required fields.
    if not resume_text or not job_title or not job_description:
        return jsonify({
            "error": (
                "Resume, job title, and job description "
                "are required."
            )
        }), 400

    # Prevent excessively large inputs.
    if len(resume_text) > 100000:
        return jsonify({
            "error": "Resume text is too long."
        }), 400

    if len(job_description) > 30000:
        return jsonify({
            "error": "Job description is too long."
        }), 400

    connection = None

    try:
        # ----------------------------------------------------
        # 1. Resume and job matching
        # ----------------------------------------------------

        result = analyze_resume(
            resume_text,
            job_description
        )

        # ----------------------------------------------------
        # 2. Ensure Phase 8 gap-analysis fields are available
        # ----------------------------------------------------

        result.setdefault("skill_gaps", [])
        result.setdefault(
            "missing_skills_by_priority",
            {
                "High": [],
                "Medium": [],
                "Low": [],
            }
        )
        result.setdefault("total_missing_skills", len(
            result.get("missing_skills", [])
        ))
        result.setdefault(
            "gap_analysis_available",
            True
        )

        # Preserve existing matching fields.
        result.setdefault("resume_skills", [])
        result.setdefault("required_skills", [])
        result.setdefault("matched_skills", [])
        result.setdefault("missing_skills", [])
        result.setdefault("total_required_skills", 0)
        result.setdefault("total_matched_skills", 0)

        # ----------------------------------------------------
        # 3. ATS analysis
        # ----------------------------------------------------

        ats_result = check_resume(
            resume_text,
            job_description
        )

        result["ats_analysis"] = ats_result
        result["ats_score"] = ats_result["ats_score"]

        # Add job information.
        result["job_title"] = job_title
        result["company_name"] = company_name

        # ----------------------------------------------------
        # 4. Save analysis to MySQL
        # ----------------------------------------------------

        connection = get_connection()

        with connection.cursor() as cursor:

            # Find the existing demo user.
            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE email = %s
                """,
                ("demo@careerfit.local",)
            )

            demo_user = cursor.fetchone()

            # Create a demo user if one does not exist.
            if demo_user:
                user_id = demo_user["user_id"]

            else:
                cursor.execute(
                    """
                    INSERT INTO users
                        (full_name, email, password_hash)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        "Demo User",
                        "demo@careerfit.local",
                        generate_password_hash(uuid.uuid4().hex)
                    )
                )

                user_id = cursor.lastrowid

            # Save the resume.
            cursor.execute(
                """
                INSERT INTO resumes
                    (user_id, file_name, file_path, extracted_text)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_id,
                    resume_file_name or "pasted_resume.txt",
                    None,
                    resume_text
                )
            )

            resume_id = cursor.lastrowid

            # Save the job description.
            cursor.execute(
                """
                INSERT INTO jobs
                    (user_id, job_title, company_name, job_description)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_id,
                    job_title,
                    company_name or None,
                    job_description
                )
            )

            job_id = cursor.lastrowid

            # Save the full analysis, including Phase 8 gap data.
            cursor.execute(
                """
                INSERT INTO job_analyses
                    (user_id, resume_id, job_id,
                     match_score, analysis_result)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    resume_id,
                    job_id,
                    result["match_score"],
                    json.dumps(result)
                )
            )

            analysis_id = cursor.lastrowid

        connection.commit()

        # ----------------------------------------------------
        # 5. Return analysis results to the frontend
        # ----------------------------------------------------

        result["analysis_id"] = analysis_id
        result["message"] = (
            "Analysis completed and saved successfully."
        )

        return jsonify(result), 200

    except ValueError as error:
        if connection:
            connection.rollback()

        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        if connection:
            connection.rollback()

        app.logger.exception(
            "Failed to analyze or save resume."
        )

        return jsonify({
            "error": (
                "Analysis could not be saved. "
                "Check the Flask terminal."
            )
        }), 500

    finally:
        if connection:
            connection.close()


# ============================================================
# ANALYSIS HISTORY PAGE
# ============================================================

@app.route("/history")
def analysis_history():

    return render_template("history.html")


# ============================================================
# ANALYSIS HISTORY API
# ============================================================

@app.route("/api/history", methods=["GET"])
def get_analysis_history():

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    a.analysis_id,
                    a.match_score,
                    a.created_at,
                    j.job_title,
                    j.company_name
                FROM job_analyses a
                JOIN jobs j
                    ON j.job_id = a.job_id
                ORDER BY
                    a.created_at DESC,
                    a.analysis_id DESC
                LIMIT 50
                """
            )

            analyses = cursor.fetchall()

        for analysis in analyses:

            analysis["created_at"] = format_datetime(
                analysis.get("created_at"),
                "%d %b %Y, %I:%M %p"
            )

            if analysis.get("match_score") is not None:
                analysis["match_score"] = float(
                    analysis["match_score"]
                )

        return jsonify({
            "analyses": analyses
        }), 200

    except Exception:

        app.logger.exception(
            "Unable to retrieve analysis history."
        )

        return jsonify({
            "error": "Unable to load analysis history."
        }), 500

    finally:

        if connection:
            connection.close()


# ============================================================
# DASHBOARD ANALYTICS API — PHASE 6
# ============================================================

@app.route("/api/dashboard", methods=["GET"])
def dashboard_data():

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            # 1. Overall summary
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_analyses,
                    AVG(match_score) AS average_score,
                    MAX(created_at) AS latest_analysis
                FROM job_analyses
            """)

            summary = cursor.fetchone() or {}

            # 2. Recent analyses
            cursor.execute("""
                SELECT
                    a.analysis_id,
                    a.match_score,
                    a.analysis_result,
                    a.created_at,
                    j.job_title,
                    j.company_name
                FROM job_analyses a
                JOIN jobs j ON j.job_id = a.job_id
                ORDER BY a.created_at DESC, a.analysis_id DESC
                LIMIT 10
            """)

            recent_analyses = cursor.fetchall()

            # 3. Most frequently analyzed job roles
            cursor.execute("""
                SELECT
                    j.job_title,
                    COUNT(*) AS analysis_count,
                    AVG(a.match_score) AS average_match_score
                FROM job_analyses a
                JOIN jobs j ON j.job_id = a.job_id
                GROUP BY j.job_title
                ORDER BY analysis_count DESC, average_match_score DESC
                LIMIT 5
            """)

            top_job_roles = cursor.fetchall()

            # 4. Match score trend
            cursor.execute("""
                SELECT
                    a.analysis_id,
                    a.match_score,
                    a.created_at,
                    j.job_title
                FROM job_analyses a
                JOIN jobs j ON j.job_id = a.job_id
                ORDER BY a.created_at DESC, a.analysis_id DESC
                LIMIT 10
            """)

            score_trend = cursor.fetchall()

        # Convert recent analyses to JSON-compatible values.
        for item in recent_analyses:

            if item.get("created_at"):
                item["created_at"] = item["created_at"].strftime(
                    "%d %b %Y, %I:%M %p"
                )

            item["analysis_result"] = parse_analysis_result(
                item.get("analysis_result")
            )

            if item.get("match_score") is not None:
                item["match_score"] = float(item["match_score"])

        # Convert role analytics.
        for role in top_job_roles:

            if role.get("average_match_score") is not None:
                role["average_match_score"] = round(
                    float(role["average_match_score"]), 2
                )

            role["analysis_count"] = int(
                role["analysis_count"] or 0
            )

        # Convert graph data.
        for item in score_trend:

            if item.get("created_at"):
                item["created_at"] = item["created_at"].strftime(
                    "%d %b %Y"
                )

            if item.get("match_score") is not None:
                item["match_score"] = float(item["match_score"])

        # 5. Count frequently missing skills.
        missing_skill_counts = {}

        for item in recent_analyses:

            result = item.get("analysis_result", {})

            missing_skills = extract_missing_skills(result)

            for skill in missing_skills:

                key = skill.casefold()

                if key not in missing_skill_counts:
                    missing_skill_counts[key] = {
                        "skill": skill,
                        "count": 0
                    }

                missing_skill_counts[key]["count"] += 1

        frequently_missing_skills = sorted(
            missing_skill_counts.values(),
            key=lambda item: item["count"],
            reverse=True
        )[:10]

        # Format overall summary.
        summary["total_analyses"] = int(
            summary.get("total_analyses") or 0
        )

        if summary.get("average_score") is not None:
            summary["average_score"] = round(
                float(summary["average_score"]), 2
            )

        if summary.get("latest_analysis"):
            summary["latest_analysis"] = (
                summary["latest_analysis"].strftime(
                    "%d %b %Y, %I:%M %p"
                )
            )

        # Return all dashboard datasets.
        return jsonify({
            "summary": summary,
            "recent_analyses": recent_analyses,
            "score_trend": list(reversed(score_trend)),
            "top_job_roles": top_job_roles,
            "frequently_missing_skills": frequently_missing_skills
        }), 200

    except Exception:

        app.logger.exception(
            "Unable to load dashboard analytics."
        )

        return jsonify({
            "error": "Unable to load dashboard analytics."
        }), 500

    finally:

        if connection:
            connection.close()


# ============================================================
# RESUME IMPROVEMENT API — PHASE 7
# ============================================================

@app.route("/api/improve-resume", methods=["POST"])
def improve_resume():

    data = request.get_json(silent=True)

    # Validate the request body.
    if not isinstance(data, dict):
        return jsonify({
            "error": "Please provide valid JSON input."
        }), 400

    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")
    job_title = data.get("job_title", "")

    # Validate input types.
    if not isinstance(resume_text, str):
        return jsonify({
            "error": "Resume text must be a string."
        }), 400

    if not isinstance(job_description, str):
        return jsonify({
            "error": "Job description must be a string."
        }), 400

    if not isinstance(job_title, str):
        return jsonify({
            "error": "Job title must be a string."
        }), 400

    # Clean the input.
    resume_text = resume_text.strip()
    job_description = job_description.strip()
    job_title = job_title.strip()

    # Validate required input.
    if not resume_text:
        return jsonify({
            "error": "Resume text is required."
        }), 400

    # Prevent excessively large text inputs.
    if len(resume_text) > 100000:
        return jsonify({
            "error": (
                "Resume text is too long. "
                "Please use a shorter resume."
            )
        }), 400

    if len(job_description) > 30000:
        return jsonify({
            "error": "Job description is too long."
        }), 400

    try:
        # Generate the resume improvement report.
        improvement_result = generate_improvement_report(
            resume_text,
            job_description
        )

        recommendations = improvement_result.get(
            "recommendations", []
        )

        bullet_improvements = improvement_result.get(
            "bullet_improvements", []
        )

        # Return the report and useful metadata.
        return jsonify({
            "success": True,
            "job_title": job_title,
            "recommendations": recommendations,
            "bullet_improvements": bullet_improvements,
            "recommendation_count": len(recommendations),
            "bullet_improvement_count": len(bullet_improvements)
        }), 200

    except Exception:

        app.logger.exception(
            "Failed to generate resume improvements."
        )

        return jsonify({
            "error": "Could not generate resume improvements."
        }), 500


# ============================================================
# JOB RECOMMENDATIONS API — PHASE 5
# ============================================================

@app.route("/api/recommend-jobs", methods=["POST"])
def recommend_jobs_api():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please provide valid JSON input."
        }), 400

    resume_text = data.get("resume_text", "")

    if not isinstance(resume_text, str) or not resume_text.strip():
        return jsonify({
            "error": "Please provide resume text."
        }), 400

    try:
        result = recommend_jobs(resume_text)

        return jsonify(result), 200

    except Exception:

        app.logger.exception(
            "Failed to generate job recommendations."
        )

        return jsonify({
            "error": "Unable to generate job recommendations."
        }), 500


# ============================================================
# RUN APPLICATION
# ============================================================
# ==========================================
# PHASE 10: RESUME READINESS API
# ==========================================

@app.route("/api/resume-readiness", methods=["POST"])
def resume_readiness():
    data = request.get_json(silent=True) or {}

    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")

    if not isinstance(resume_text, str) or not resume_text.strip():
        return jsonify({
            "success": False,
            "error": "Resume text is required."
        }), 400

    if not isinstance(job_description, str):
        job_description = ""

    try:
        result = calculate_resume_readiness(
            resume_text=resume_text,
            job_description=job_description
        )

        return jsonify({
            "success": True,
            **result
        }), 200

    except Exception:
        app.logger.exception(
            "Failed to calculate resume readiness."
        )

        return jsonify({
            "success": False,
            "error": "Could not calculate resume readiness."
        }), 500
    
if __name__ == "__main__":
    app.run(debug=True)


