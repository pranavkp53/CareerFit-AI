# 🚀 CareerFit AI — Resume Analyzer & Career Guidance Platform

CareerFit AI is a full-stack web application designed to help job seekers improve their resumes and prepare for career opportunities. It analyzes resumes against job descriptions, evaluates ATS compatibility, identifies missing skills, recommends suitable job roles, and provides personalized resume improvement suggestions.

## ✨ Features

- **📄 Resume Parsing:** Upload PDF and DOCX resumes for text extraction.
- **🎯 Resume–Job Matching:** Analyze how well a resume matches a job description.
- **📊 ATS Score Checker:** Evaluate resumes using ATS-related checks and provide improvement suggestions.
- **🔍 Skill Gap Analysis:** Identify missing skills and prioritize areas for improvement.
- **📝 Resume Improvement Assistant:** Generate suggestions to improve resume content and bullet points.
- **💼 Job Recommendations:** Recommend suitable job roles based on detected skills.
- **✅ Resume Readiness Score:** Evaluate resume readiness using multiple assessment criteria.
- **📈 Interactive Dashboard:** View analysis statistics, recent results, score trends, and frequently missing skills.
- **🕘 Analysis History:** Review previous resume analyses.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic and resume analysis |
| Flask | Web application framework and API endpoints |
| MySQL | Database for storing resumes, jobs, and analysis records |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive layouts |
| JavaScript | Frontend interactions and API communication |
| PDF/DOCX processing libraries | Resume text extraction |

## 📁 Project Structure

```text
CareerFitAI/
│
├── app.py
├── database.py
├── .env
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── analyze.html
│   └── history.html
│
├── static/
│   ├── css/
│   │   ├── dashboard.css
│   │   └── analyze.css
│   │
│   └── js/
│       ├── dashboard.js
│       ├── analyze.js
│       └── history.js
│
├── services/
│   ├── resume_parser.py
│   ├── job_matcher.py
│   ├── ats_checker.py
│   ├── resume_improver.py
│   ├── job_recommender.py
│   └── resume_readiness.py
│
├── uploads/
└── README.md
```

*Note: The structure above reflects the project files discussed during development. Adjust it if your final repository differs.*

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have installed:

- Python
- MySQL Server
- Git
- A code editor such as Visual Studio Code

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd CareerFitAI
```

### 2. Create a Virtual Environment

On macOS or Linux:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

If your repository contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If you have not created this file yet, install the packages required by your application and create a `requirements.txt` file from your working environment.

### 4. Configure MySQL

Start your MySQL server and create the project database:

```sql
CREATE DATABASE careerfit_ai;
```

Configure your database connection settings according to your `database.py` implementation.

### 5. Configure Environment Variables

Create a `.env` file in the project root and add the configuration values expected by your application.

Example:

```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=careerfit_ai
```

**Important:** Replace the example values with your own settings. Ensure your `database.py` reads the same variable names. Never upload real passwords or secret credentials to GitHub.

### 6. Run the Application

With your virtual environment activated, start the Flask application:

```bash
python3 app.py
```

Open the local address shown in your terminal. If your application uses Flask's default development server, it is usually:

```text
http://127.0.0.1:5000
```

## 🔄 How It Works

1. **Upload a Resume:** The user uploads a PDF/DOCX resume or provides resume text.
2. **Enter Job Details:** The user provides the target job title and job description.
3. **Analyze the Resume:** The backend extracts resume information and evaluates the resume against the job requirements.
4. **Review the Results:** The application displays matching scores, ATS-related feedback, and missing skills.
5. **Improve the Resume:** The user receives suggestions for improving resume content.
6. **Explore Job Roles:** The application recommends job roles based on the skills identified in the resume.
7. **Track Progress:** The dashboard and analysis history help users review previous results.

## 🔌 Main API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Display the dashboard |
| `/analyze` | GET | Open the resume analysis page |
| `/history` | GET | Display analysis history |
| `/api/analyze` | POST | Analyze a resume against a job description |
| `/api/resume/parse` | POST | Parse an uploaded resume |
| `/api/dashboard` | GET | Retrieve dashboard analytics |
| `/api/history` | GET | Retrieve previous analyses |
| `/api/improve-resume` | POST | Generate resume improvement suggestions |
| `/api/recommend-jobs` | POST | Generate job recommendations |
| `/api/resume-readiness` | POST | Calculate resume readiness |

## 🎯 Project Objectives

- Help job seekers evaluate resumes against job requirements.
- Identify missing skills and potential improvement areas.
- Provide practical suggestions for improving resume content.
- Recommend job roles aligned with detected skills.
- Make resume analysis and career preparation more accessible through a user-friendly web application.

## 🔒 Security Notes

- Keep database credentials in environment variables.
- Do not commit `.env`, passwords, or other sensitive information.
- Validate uploaded files and user inputs.
- Use appropriate file size limits and upload restrictions.
- For production deployment, configure secure settings and use a production-ready WSGI server.

## 🚀 Future Scope

Potential future enhancements include integrating external job listings, supporting additional resume formats, and improving matching accuracy through more advanced NLP or machine learning techniques.

## 👨‍💻 Author

**Pranav KP**

CareerFit AI — Resume Analysis and Career Guidance Platform.

---

⭐ If you find this project interesting, consider giving the repository a star!
