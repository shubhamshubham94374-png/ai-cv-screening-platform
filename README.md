[README.md](https://github.com/user-attachments/files/30624811/README.md)
# AI-Powered CV Screening Platform

An end-to-end recruitment automation platform that parses resumes and job descriptions, matches candidates to roles using NLP and semantic embeddings, generates weighted match scores, and produces AI-generated hiring insights — built with FastAPI, PostgreSQL, and Google Gemini, and deployed on AWS.

## Live Demo

- **API Docs (Swagger UI):** `http://<ec2-public-ip>:8000/docs`
- **Recruiter Dashboard:** `http://<ec2-public-ip>:8501`

## Overview

Recruitment teams often receive hundreds of resumes per job posting, making manual screening slow and inconsistent. This platform automates the pipeline end to end:

1. Upload a resume (PDF/DOCX) → automatically parsed into structured candidate data
2. Create a job posting → automatically parsed into required/preferred skills, experience, and education requirements
3. Score any candidate against any job → weighted score across 8 components
4. Generate AI-written hiring insights → summary, strengths, weaknesses, interview questions, and a recommendation
5. View everyone ranked, side by side, in an interactive dashboard

## Architecture

```
                    ┌─────────────┐
                    │  Streamlit   │  Recruiter Dashboard
                    │  Dashboard   │
                    └──────┬──────┘
                           │ reads directly
                    ┌──────▼──────┐
                    │  PostgreSQL  │ ◄──────────────┐
                    │  (AWS RDS)   │                │
                    └──────▲──────┘                 │
                           │                          │
                    ┌──────┴──────┐          ┌───────┴──────┐
                    │   FastAPI    │◄────────►│  AWS S3       │
                    │   Backend    │          │  (resume      │
                    │   (EC2)      │          │   storage)    │
                    └──────┬──────┘          └──────────────┘
                           │
                    ┌──────┴──────┐
                    │  Google      │
                    │  Gemini API  │
                    └─────────────┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Uvicorn |
| Database | PostgreSQL (AWS RDS), SQLAlchemy, Alembic |
| File Storage | AWS S3 |
| Resume/JD Parsing | PyMuPDF, python-docx, spaCy, Regex |
| Matching Engine | RapidFuzz (fuzzy matching), scikit-learn (TF-IDF), Sentence Transformers (semantic embeddings) |
| AI Insights | Google Gemini API |
| Dashboard | Streamlit, Plotly, Pandas |
| Deployment | AWS EC2, systemd, IAM roles |
| Version Control | Git, GitHub |

## Core Features

### Resume Parsing
Extracts name, email, phone, LinkedIn, GitHub, portfolio links, and skills from PDF/DOCX resumes using a combination of regex pattern matching and spaCy NLP.

### Job Description Parsing
Extracts minimum experience requirements, degree requirements, and splits skills into "required" vs "preferred" based on section markers in the posting text.

### Matching Engine
Combines four signals to compare a candidate against a job:
- **Exact skill matching** — via a shared, normalized skills table
- **Fuzzy + alias-based matching** — catches spelling variations (e.g., "Postgres" vs "PostgreSQL")
- **TF-IDF similarity** — word-overlap based text comparison
- **Semantic similarity** — meaning-based comparison using sentence embeddings, catching conceptually related content even with no shared vocabulary

### Weighted Scoring
Combines 8 components into a single 0–100 score:

| Component | Weight |
|---|---|
| Required Skills | 35% |
| Preferred Skills | 15% |
| Experience | 20% |
| Competencies (semantic similarity) | 10% |
| Education | 5% |
| Certifications | 5% |
| Projects | 5% |
| Domain Experience (TF-IDF similarity) | 5% |

### AI Recommendation Engine
Sends the candidate's data, the job's requirements, and the computed scores to Google Gemini, which returns a structured recommendation: a summary, strengths, weaknesses, tailored interview questions, and a hire/maybe/no-hire justification grounded in the actual score.

### Recruiter Dashboard
- Candidate ranking table, sortable by total match score
- Skill gap analysis — most commonly missing required skills across applicants
- Match score distribution histogram
- Full AI insight detail view per candidate

## Database Schema

Normalized relational schema (PostgreSQL) with 11 tables:

- `candidates` — core candidate record
- `skills` — master skill reference list (shared between candidates and jobs)
- `candidate_skills` — join table linking candidates to skills
- `education`, `experience`, `certifications`, `projects` — candidate detail tables
- `jobs` — job posting record
- `job_skills` — join table linking jobs to required/preferred skills
- `match_scores` — persisted scoring results per candidate-job pair
- `ai_insights` — persisted Gemini-generated recommendations

Schema migrations are managed with Alembic.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/resumes/upload` | Upload and parse a resume |
| POST | `/jobs/` | Create and parse a job posting |
| GET | `/matching/{candidate_id}/{job_id}` | Get raw matching signals |
| POST | `/matching/{candidate_id}/{job_id}/score` | Calculate and persist the weighted match score |
| POST | `/matching/{candidate_id}/{job_id}/insights` | Generate and persist AI hiring insights |

Full interactive documentation is available at `/docs` once the server is running.

## Local Setup

### Prerequisites
- Python 3.10+
- PostgreSQL
- AWS account (for S3/RDS in production; optional for local-only development)
- Google Gemini API key

### Installation

```bash
git clone https://github.com/shubhamshubham94374-png/ai-cv-screening-platform.git
cd ai-cv-screening-platform
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install fastapi uvicorn[standard] python-multipart sqlalchemy psycopg2-binary python-dotenv pydantic-settings pymupdf python-docx spacy rapidfuzz scikit-learn sentence-transformers google-genai boto3 alembic streamlit plotly pandas
python -m spacy download en_core_web_sm
```

### Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:<password>@<host>:5432/cv_screening_db
GEMINI_API_KEY=<your_gemini_api_key>
STORAGE_BACKEND=local          # or "s3" for production
S3_BUCKET_NAME=<your_bucket_name>
AWS_REGION=us-east-1
UPLOAD_DIR=./storage/resumes
MAX_FILE_SIZE_MB=5
```

### Run Migrations

```bash
alembic upgrade head
```

### Start the API

```bash
uvicorn app.main:app --reload
```

### Start the Dashboard

```bash
cd dashboard
streamlit run app.py
```

## Deployment

The production deployment runs on AWS:

- **EC2** (t3.micro) hosts the FastAPI app and Streamlit dashboard as persistent `systemd` services
- **RDS** (PostgreSQL) serves as the managed database
- **S3** stores uploaded resume files
- **IAM roles** grant EC2 permission to access S3 without hardcoded credentials

Both services are configured to restart automatically on failure or server reboot via `systemd` unit files.

## Project Structure

```
ai-cv-screening-platform/
├── app/
│   ├── api/              # FastAPI route handlers
│   ├── core/              # Configuration
│   ├── db/                # SQLAlchemy models and session
│   ├── schemas/            # Pydantic request/response models
│   └── services/
│       ├── parsing/        # Resume and job description parsing
│       ├── matching/        # Skill matching, similarity, scoring
│       ├── ai_insights/     # Gemini integration
│       └── storage/         # Local/S3 storage abstraction
├── alembic/                # Database migrations
├── dashboard/               # Streamlit recruiter dashboard
├── scripts/                 # Test/utility scripts
└── requirements.txt
```

## Future Improvements

- Bulk resume upload (multiple files in one request)
- Structured extraction of education/experience/projects directly from resume text (currently populated manually/partially)
- User authentication for the API and dashboard
- Frontend rebuild as a dedicated web app rather than Swagger UI + Streamlit
- CI/CD pipeline for automated deployment

## Author

Shubham Malik — Computer Science Engineering student, Chandigarh University

## License

This project is for educational and portfolio purposes.
