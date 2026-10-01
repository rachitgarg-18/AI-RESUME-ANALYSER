AI Career Copilot — AI Resume Analyzer

AI Career Copilot is a full-stack AI-powered career guidance application built with Python and Flask. It analyzes a user's resume against a selected target role and provides personalized insights into existing skills, missing skills, learning roadmap, and technical interview preparation.

The application supports multiple resume formats, user authentication, AI-powered analysis using the OpenAI API, and persistent analysis history through SQLite.

🚀 Features
📄 Resume Upload & Parsing
Supports PDF, DOCX, and TXT files.
Extracts resume text automatically.
🤖 AI-Powered Resume Analysis
Uses the OpenAI API to analyze resume content.
Evaluates the resume according to the user's target role.
🛠️ Skill Analysis
Identifies existing technical skills.
Highlights important missing skills required for the target role.
🗺️ Personalized Learning Roadmap
Generates actionable, step-by-step learning recommendations.
💼 Interview Preparation
Generates role-specific technical interview questions.
🔐 User Authentication
User registration and login.
Passwords are stored using secure password hashing.
🗃️ Analysis History
Stores previous analyses for each user.
Users can access their previous results.
🌐 Web-Based Interface
Flask-powered backend.
Dashboard-based workflow for resume analysis.
🛠️ Tech Stack
Technology	Purpose
Python	Core application logic
Flask	Web framework and backend
OpenAI API	AI-powered resume analysis
SQLite	User and analysis data storage
PyPDF2	PDF text extraction
python-docx	DOCX text extraction
HTML/CSS	Web interface
JSON	Structured AI responses
python-dotenv	Environment variable management

The project uses Flask routes for authentication, dashboard access, resume analysis, and analysis history.

🔄 Application Workflow
User Registration / Login
          ↓
      Dashboard
          ↓
Upload Resume / Paste Resume Text
          ↓
     Resume Parsing
          ↓
 Select Target Career Role
          ↓
     AI Resume Analysis
          ↓
 ┌─────────────────────────┐
 │ Existing Skills         │
 │ Missing Skills          │
 │ Learning Roadmap        │
 │ Interview Questions     │
 └─────────────────────────┘
          ↓
    Save Analysis History

The analyzer returns structured results containing skills, missing_skills, roadmap, and interview_questions.

📂 Project Structure
AI-Career-Copilot/
│
├── app.py
├── analyzer.py
├── resume_parser.py
├── db.py
├── requirements.txt
├── README.md
├── .env
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── history.html
│   └── result.html
│
└── uploads/
📄 Resume Parsing

The application extracts text from:

PDF using PyPDF2
DOCX using python-docx
TXT using Python's file handling

It can also detect information such as candidate name, email, phone number, LinkedIn, GitHub, portfolio links, and common resume sections.

🗄️ Database

SQLite is used to manage:

User accounts
Password hashes
Target roles
Uploaded resume information
Extracted skills
Missing skills
Interview questions
Learning roadmap
Analysis history

The database uses separate users and history tables with a relationship between them.

⚙️ Installation
1. Clone the repository
git clone https://github.com/rachitgarg-18/AI-Career-Copilot.git
cd AI-Career-Copilot
2. Create a virtual environment
python -m venv venv
3. Activate the environment

Windows:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Configure environment variables

Create a .env file:

OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
6. Run the application
python app.py

Open:

http://127.0.0.1:5000
🔒 Security
API keys should be stored in environment variables.
Never commit your .env file to GitHub.
Never upload real API keys, passwords, or private database files.
Passwords are stored using password hashing rather than plain text.

Add this to .gitignore before pushing the project:

.env
venv/
__pycache__/
*.pyc
*.db
uploads/
