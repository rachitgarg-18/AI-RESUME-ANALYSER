# AI Career Copilot – AI Resume Analyzer

AI Career Copilot is a full-stack Python and Flask web application that analyzes resumes using AI and provides personalized career guidance based on a user's target job role.

## 🚀 Features

* 📄 Upload and parse resumes in PDF, DOCX, and TXT formats
* 🤖 AI-powered resume analysis using the OpenAI API
* 🎯 Target-role based career analysis
* 🛠️ Extracts existing technical skills from resumes
* 📚 Identifies missing skills required for the target role
* 🗺️ Generates a step-by-step learning roadmap
* 💼 Provides role-specific technical interview questions
* 🔐 User registration and login authentication
* 🗄️ SQLite database for storing users and analysis history
* 📊 View previous resume analyses through the history section
* 🔒 Password hashing for secure authentication
* 🌐 Flask-based web application

## 🛠️ Tech Stack

* Python
* Flask
* OpenAI API
* SQLite
* PyPDF2
* python-docx
* HTML/CSS
* JSON
* python-dotenv

## 🔄 How It Works

1. User creates an account or logs in.
2. User uploads a resume or pastes resume text.
3. The application extracts text from the resume.
4. User selects a target career role.
5. The resume is analyzed using the OpenAI API.
6. The system identifies:

   * Existing Skills
   * Missing Skills
   * Learning Roadmap
   * Interview Questions
7. The analysis is saved to the user's history for future reference.

## 🎯 Project Goal

The goal of AI Career Copilot is to help students and job seekers understand their current skill set, identify gaps for a desired career role, and receive a structured roadmap for improving their technical skills and interview preparation.

## 📌 Future Improvements

* Resume scoring and ATS analysis
* Job description matching
* Job recommendation system
* LinkedIn profile analysis
* Skill-based project recommendations
* Progress tracking
* Deployment on cloud platforms
