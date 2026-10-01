import os
import uuid
import json
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, jsonify, session
)
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from resume_parser import parse_resume_file
from analyzer import analyze_resume_with_openai
from db import (
    init_db, register_user, authenticate_user,
    save_analysis, get_user_history, get_history_by_id
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ai-career-copilot-black-theme-2026")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

# Initialize database
init_db()

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    return dict(
        user_email=session.get("user_email"),
        user_id=session.get("user_id")
    )

# --- Authentication Routes ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = authenticate_user(email, password)
        if user:
            session["user_id"] = user["id"]
            session["user_email"] = user["email"]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "warning")
            return render_template("signup.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "warning")
            return render_template("signup.html")

        success, msg = register_user(email, password)
        if success:
            user = authenticate_user(email, password)
            if user:
                session["user_id"] = user["id"]
                session["user_email"] = user["email"]
            return redirect(url_for("dashboard"))
        else:
            flash(msg, "danger")

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- Dashboard & Core Analysis Routes ---
@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/analyze", methods=["POST"])
@login_required
def analyze():
    resume_text = ""
    filename = ""

    # 1. Check for uploaded resume file (PDF / DOCX)
    if "resume_file" in request.files:
        file = request.files["resume_file"]
        if file and file.filename != "":
            if not allowed_file(file.filename):
                flash("Unsupported file format! Please upload PDF, DOCX, or TXT.", "danger")
                return redirect(url_for("dashboard"))

            clean_name = secure_filename(file.filename)
            unique_name = f"{uuid.uuid4().hex[:8]}_{clean_name}"
            saved_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
            file.save(saved_path)

            try:
                resume_text = parse_resume_file(saved_path)
                filename = clean_name
            except Exception as e:
                flash(f"Error parsing resume: {str(e)}", "danger")
                return redirect(url_for("dashboard"))
            finally:
                if os.path.exists(saved_path):
                    try:
                        os.remove(saved_path)
                    except Exception:
                        pass

    # 2. Check for pasted resume text
    pasted_text = request.form.get("resume_text", "").strip()
    if not resume_text and pasted_text:
        resume_text = pasted_text
        filename = "Pasted Resume"

    if not resume_text:
        flash("Please upload a resume file or paste your resume text.", "warning")
        return redirect(url_for("dashboard"))

    # 3. Target role input
    target_role = request.form.get("target_role", "").strip()
    if not target_role:
        target_role = "Backend Engineer"

    # 4. Run OpenAI Analysis directly from .env key
    results = analyze_resume_with_openai(
        resume_text=resume_text,
        target_role=target_role
    )
    results["filename"] = filename

    # 6. Save to history
    save_analysis(
        user_id=session["user_id"],
        target_role=results["target_role"],
        filename=filename,
        skills=results["skills"],
        new_skills=results["missing_skills"],
        interview_questions=results["interview_questions"],
        projects=results["roadmap"]  # stores roadmap/projects
    )

    # Render results right below the form on dashboard (matching video)
    return render_template(
        "dashboard.html",
        results=results,
        prev_resume_text=resume_text if len(resume_text) < 1000 else "",
        prev_target_role=target_role
    )

@app.route("/history")
@login_required
def history():
    user_history = get_user_history(session["user_id"])
    return render_template("history.html", history=user_history)

@app.route("/history/<int:history_id>")
@login_required
def history_detail(history_id):
    item = get_history_by_id(history_id, session["user_id"])
    if not item:
        flash("Record not found.", "warning")
        return redirect(url_for("history"))
    
    # Format item for result template
    formatted = {
        "target_role": item["target_role"],
        "filename": item["filename"],
        "skills": item["skills"],
        "missing_skills": item["new_skills"],
        "roadmap": item["projects"],
        "interview_questions": item["interview_questions"]
    }
    return render_template("result.html", results=formatted)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"AI Career Copilot running at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)