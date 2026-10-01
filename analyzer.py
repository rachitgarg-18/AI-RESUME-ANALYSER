import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

def analyze_resume_with_openai(resume_text: str, target_role: str, user_api_key: str = None) -> dict:
    """
    Analyze resume using OpenAI API exactly as shown in the video:
    Outputs:
    - Skills (extracted from resume)
    - Missing Skills (skills required for target role)
    - Roadmap (step-by-step learning guide)
    - Interview Questions (role-specific questions)
    """
    api_key = user_api_key or os.getenv("OPENAI_API_KEY")

    if not api_key or not api_key.strip():
        # Fallback if API key is missing
        return generate_local_fallback(resume_text, target_role, "Please provide an OpenAI API key in the .env file or input box.")

    try:
        client = OpenAI(api_key=api_key.strip())
        prompt = f"""
You are an expert AI Career Copilot and tech hiring recruiter.
Analyze the candidate's resume for their desired target role: "{target_role}".

Candidate Resume Text:
\"\"\"
{resume_text[:6000]}
\"\"\"

Please generate a precise analysis in valid JSON format with the following exact 4 keys:
1. "skills": Array of strings representing the candidate's existing technical skills, tools, and proficiencies extracted from their resume.
2. "missing_skills": Array of strings representing the key missing skills, frameworks, and tools they need to learn to become a {target_role}.
3. "roadmap": Array of detailed step-by-step actionable bullet points outlining how to learn those missing skills and master the role.
4. "interview_questions": Array of realistic technical interview questions they will be asked for a {target_role} position.

Respond ONLY with valid JSON.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI Career Copilot. Respond strictly in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        return {
            "success": True,
            "target_role": target_role,
            "skills": data.get("skills", []),
            "missing_skills": data.get("missing_skills", []),
            "roadmap": data.get("roadmap", []),
            "interview_questions": data.get("interview_questions", [])
        }

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return generate_local_fallback(resume_text, target_role, f"OpenAI API Error: {str(e)}")


def generate_local_fallback(resume_text: str, target_role: str, error_msg: str = "") -> dict:
    """Smart structured fallback if OpenAI key is not configured or fails."""
    # Heuristic extraction
    import re
    known_skills = [
        "SQL", "Creating and modifying views in SQL Server", "ETL processes", "Data modeling",
        "Performance tuning of SQL scripts", "Data transformation and treatment", "DAX for calculations",
        "Power Query", "Python (Pandas, NumPy)", "JSON processing", "Data ingestion", "Data quality testing workflows",
        "Python", "Flask", "Django", "FastAPI", "React", "JavaScript", "TypeScript", "HTML/CSS", "Docker", "Kubernetes", "AWS", "Git", "REST APIs", "Redis", "PostgreSQL", "MongoDB"
    ]
    
    lower = resume_text.lower()
    found_skills = [s for s in known_skills if s.lower() in lower or any(word in lower for word in s.lower().split())]
    if not found_skills:
        found_skills = ["Python", "SQL", "Data Analysis", "Git", "Problem Solving"]

    role_lower = target_role.lower()
    if "backend" in role_lower or "java" in role_lower:
        missing_skills = [
            "Java programming language",
            "Java frameworks (e.g., Spring, Hibernate)",
            "Java development tools (e.g., Maven, Gradle)",
            "Java IDEs (e.g., IntelliJ IDEA, Eclipse)",
            "Understanding of Java backend development concepts (e.g., REST APIs, multithreading)",
            "Unit testing frameworks for Java (e.g., JUnit, Mockito)",
            "Build and deployment pipelines for Java applications",
            "Version control with Git in Java projects"
        ]
        roadmap = [
            "Learn core Java programming concepts: syntax, OOP principles, exception handling, collections, streams.",
            "Study and practice Java backend frameworks like Spring Boot and Hibernate.",
            "Get familiar with Java build tools such as Maven or Gradle.",
            "Practice using Java IDEs like IntelliJ IDEA or Eclipse for development.",
            "Understand RESTful API development and how to implement it in Java.",
            "Learn multithreading and concurrency in Java.",
            "Explore unit testing in Java using JUnit and Mockito.",
            "Build sample Java backend projects to apply learned skills."
        ]
        interview_questions = [
            "Explain the difference between HashMap and ConcurrentHashMap in Java.",
            "How does dependency injection work in Spring Boot?",
            "What is the lifecycle of a Spring Bean?",
            "How do you handle multithreading and race conditions in Java backend services?",
            "Explain how Hibernate manages ORM mappings and the N+1 select problem."
        ]
    elif "python" in role_lower:
        missing_skills = [
            "Python web frameworks (Django, Flask)",
            "REST API development and consumption",
            "Version control systems (Git)",
            "Containerization and orchestration (Docker, Kubernetes)",
            "Cloud services for Python applications (AWS Lambda, Azure Functions)",
            "CI/CD pipelines for Python projects",
            "Python packaging and dependency management (pip, virtualenv, poetry)",
            "Understanding of software development lifecycle and agile methodologies"
        ]
        roadmap = [
            "Learn advanced Python programming concepts including OOP, decorators, and generators.",
            "Gain proficiency in Python web frameworks such as Django or Flask to build backend applications.",
            "Study and practice writing unit and integration tests using pytest or unittest.",
            "Understand REST API principles and practice building and consuming APIs with Python.",
            "Learn Git for version control and collaboration.",
            "Explore containerization with Docker and orchestration basics with Kubernetes.",
            "Familiarize yourself with deploying Python applications on cloud platforms like AWS, Azure, or GCP.",
            "Understand and implement CI/CD pipelines for Python projects to automate testing and deployment."
        ]
        interview_questions = [
            "Explain the differences between Python lists and tuples. When would you use each?",
            "How do you manage dependencies and virtual environments in Python projects?",
            "Describe how you would design and implement a RESTful API using Flask or Django.",
            "What are decorators in Python and how have you used them?",
            "Explain how you would write unit tests for a Python function. What testing frameworks have you used?"
        ]
    else:
        missing_skills = [
            f"Core frameworks and architectures required for {target_role}",
            "RESTful API design and database modeling",
            "Containerization using Docker",
            "Unit testing and automated CI/CD pipelines",
            "Cloud infrastructure deployment (AWS / GCP)"
        ]
        roadmap = [
            f"Master fundamental programming and architectural patterns for {target_role}.",
            "Build hands-on projects integrating modern databases and backend APIs.",
            "Learn automated testing, containerization, and cloud deployment best practices.",
            "Prepare for technical system design and behavioral interviews."
        ]
        interview_questions = [
            f"What are the most critical architectural considerations when building systems for {target_role}?",
            "How do you ensure high performance, security, and scalability in production?",
            "Describe a challenging technical problem you solved and how you approached debugging it."
        ]

    return {
        "success": True,
        "target_role": target_role,
        "skills": found_skills,
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "interview_questions": interview_questions,
        "notice": error_msg
    }
