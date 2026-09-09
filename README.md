The Live Session Toolkit

A professional real-time platform for hosting and managing interactive live sessions.

Overview

The Live Session Toolkit lets a host create a protected live session and engage participants through polls, Q&A, announcements, emoji reactions, participant tracking, QR-based joining, and engagement analytics.

Key Features

Live session creation with unique session code

Secure host access with a 6-digit Host PIN

Participant management

Live polls and voting

Duplicate vote protection

Audience Q&A

Announcements

Emoji reactions: 👍 ❤️ 😂 👏 🔥 🚀

QR code for quick session joining

Engagement analytics and bar charts

Reaction breakdown

Technology Stack

Layer

Technology

Frontend

Streamlit / Python

Backend

FastAPI / Python

Database

MySQL

Validation

Pydantic

Charts

Plotly

QR Code

Python QRCode

Configuration

python-dotenv

Version Control

Git / GitHub

Deployment

Railway + Streamlit Community Cloud

System Architecture

Users (Host + Participants)
          |
          v
Streamlit Frontend
          |
       HTTP/API
          |
          v
FastAPI Backend
          |
         SQL
          |
          v
     MySQL Database

Main Flow

Create Session
      |
      v
Session Code + Host PIN + QR
      |
      v
Participants Join
      |
      +--> Polls --> Vote --> Results
      +--> Q&A --> Questions
      +--> Announcements
      +--> Reactions --> Engagement
      |
      v
Analytics Dashboard

Security Features

Protected host workspace

6-digit Host PIN authentication

Host PIN stored as a SHA-256 hash

Environment variables for database credentials

.env excluded from Git

Duplicate vote protection

Backend input validation

Database-backed sessions

Project Structure

the-live-session-toolkit/
├── app.py
├── requirements.txt
├── .gitignore
├── .env
├── backend/
│   └── main.py
├── database/
├── frontend/
├── utils/
└── venv/

Local Setup

Clone

git clone https://github.com/uzma-ali123/the-live-session-toolkit.git
cd the-live-session-toolkit

Install dependencies

venv\Scripts\python.exe -m pip install -r requirements.txt

Configure .env

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD
MYSQL_DATABASE=live_session_toolkit

Never commit the real .env file.

Start Backend

venv\Scripts\python.exe -m uvicorn backend.main:app --reload

API docs:

http://127.0.0.1:8000/docs

Start Frontend

venv\Scripts\python.exe -m streamlit run app.py

Important API Endpoints

GET  /health
POST /sessions
POST /sessions/join
POST /host/login

GET  /sessions/{session_code}/participants

POST /polls
GET  /polls/{session_code}
GET  /polls/{poll_id}/results
POST /polls/vote

POST /questions
GET  /questions/{session_code}

POST /announcements
GET  /announcements/{session_code}

POST /reactions
GET  /reactions/{session_code}

Deployment

Railway Backend

Start command:

uvicorn backend.main:app --host 0.0.0.0 --port $PORT

Configure the MySQL production variables in Railway.

Streamlit Frontend

Configure the backend URL in Streamlit Secrets:

BACKEND_URL = "YOUR_RAILWAY_BACKEND_URL"

Demo Flow

Create a session.

Set a 6-digit Host PIN.

Display the session code and QR.

Join from a participant device.

Create a poll and vote.

Submit a Q&A question.

Send an announcement.

Send emoji reactions.

Open Analytics.

Show the engagement bar chart and reaction breakdown.

Future Enhancements

WebSocket real-time updates

Full user accounts and RBAC

Session history

CSV/PDF analytics export

Advanced moderation

AI-powered question summarization

Attendance reports

Security audit logging

Project Status

MVP completed and functional.

Author

Uzma Ali
BS Cyber Security
Dawood University of Engineering and Technology (DUET)

License

Academic/internship project