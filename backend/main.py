from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(title="The Live Session Toolkit API")


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_database_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

# ==================================================
# DATA MODELS
# ==================================================

class SessionCreate(BaseModel):
    title: str
    host_name: str
    host_email: str


class SessionJoin(BaseModel):
    session_code: str
    participant_name: str

class PollCreate(BaseModel):
    session_code: str
    question: str
    options: list[str]


class PollVote(BaseModel):
    poll_id: int
    option_id: int
    participant_id: int

# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():
    return {
        "message": "Live Session Toolkit Backend is Running!"
    }


# ==================================================
# DATABASE HEALTH
# ==================================================

@app.get("/health")
def health():

    try:

        connection = get_database_connection()

        if connection.is_connected():

            connection.close()

            return {
                "status": "OK",
                "database": "Connected"
            }

    except Exception as e:

        return {
            "status": "ERROR",
            "database": str(e)
        }


# ==================================================
# GENERATE SESSION CODE
# ==================================================

def generate_session_code():

    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )


# ==================================================
# CREATE SESSION
# ==================================================

@app.post("/sessions")
def create_session(session: SessionCreate):

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor()

        # ---------------------------------------------
        # GENERATE UNIQUE SESSION CODE
        # ---------------------------------------------

        while True:

            session_code = generate_session_code()

            cursor.execute(
                """
                SELECT id
                FROM sessions
                WHERE session_code = %s
                """,
                (session_code,)
            )

            existing_session = cursor.fetchone()

            if not existing_session:
                break

        # ---------------------------------------------
        # CREATE SESSION
        # ---------------------------------------------

        cursor.execute(
            """
            INSERT INTO sessions
            (session_code, title, host_name)
            VALUES (%s, %s, %s)
            """,
            (
                session_code,
                session.title,
                session.host_name
            )
        )

        session_id = cursor.lastrowid

        connection.commit()

        return {
            "message": "Session created successfully",
            "session_id": session_id,
            "session_code": session_code,
            "title": session.title,
            "host_name": session.host_name
        }

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# ==================================================
# JOIN SESSION
# ==================================================

@app.post("/sessions/join")
def join_session(data: SessionJoin):

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        session_code = data.session_code.strip().upper()
        participant_name = data.participant_name.strip()

        # ------------------------------------------
        # VALIDATE INPUT
        # ------------------------------------------

        if not session_code or not participant_name:

            raise HTTPException(
                status_code=400,
                detail="Session code and participant name are required."
            )

        # ------------------------------------------
        # FIND SESSION
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                session_code,
                title,
                host_name
            FROM sessions
            WHERE session_code = %s
            """,
            (session_code,)
        )

        session = cursor.fetchone()

        # ------------------------------------------
        # SESSION NOT FOUND
        # ------------------------------------------

        if not session:

            raise HTTPException(
                status_code=404,
                detail="Session not found. Please check the session code."
            )

        # ------------------------------------------
        # CHECK PARTICIPANTS TABLE
        # ------------------------------------------

        cursor.execute(
            """
            INSERT INTO participants
            (session_code, participant_name)
            VALUES (%s, %s)
            """,
            (
                    session_code,
                    participant_name
        )
            )

        participant_id = cursor.lastrowid

        connection.commit()

        # ------------------------------------------
        # SUCCESS RESPONSE
        # ------------------------------------------

        return {
            "message": "Successfully joined the session",
            "participant_id": participant_id,
            "participant_name": participant_name,
            "session_id": session["id"],
            "session_code": session["session_code"],
            "session_title": session["title"]
        }

    except HTTPException:
        raise

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# GET SESSION
# ==================================================

@app.get("/sessions/{session_code}")
def get_session(session_code: str):

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                session_code,
                title,
                host_id
            FROM sessions
            WHERE session_code = %s
            """,
            (session_code.strip().upper(),)
        )

        session = cursor.fetchone()

        if not session:

            raise HTTPException(
                status_code=404,
                detail="Session not found."
            )

        return session

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# GET PARTICIPANTS
# ==================================================

@app.get("/sessions/{session_code}/participants")
def get_participants(session_code: str):

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # ------------------------------------------
        # FIND SESSION
        # ------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM sessions
            WHERE session_code = %s
            """,
            (session_code.strip().upper(),)
        )

        session = cursor.fetchone()

        if not session:

            raise HTTPException(
                status_code=404,
                detail="Session not found."
            )

        # ------------------------------------------
        # GET PARTICIPANTS
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                participant_name
            FROM participants
            WHERE session_id = %s
            ORDER BY id DESC
            """,
            (session["id"],)
        )

        participants = cursor.fetchall()

        return {
            "session_code": session_code.strip().upper(),
            "total_participants": len(participants),
            "participants": participants
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# ============================================================
# POLL SYSTEM
# ============================================================

@app.post("/polls")
def create_poll(poll: PollCreate):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        session_code = poll.session_code.strip().upper()
        question = poll.question.strip()

        options = [
            option.strip()
            for option in poll.options
            if option.strip()
        ]

        if not session_code or not question:
            raise HTTPException(
                status_code=400,
                detail="Session code and question are required."
            )

        if len(options) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least 2 poll options are required."
            )

        # Check whether session exists
        cursor.execute(
            """
            SELECT id
            FROM sessions
            WHERE session_code = %s
            """,
            (session_code,)
        )

        session = cursor.fetchone()

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Session not found."
            )

        # Create poll
        cursor.execute(
            """
            INSERT INTO polls
            (session_code, question)
            VALUES (%s, %s)
            """,
            (session_code, question)
        )

        poll_id = cursor.lastrowid

        # Create poll options
        for option in options:
            cursor.execute(
                """
                INSERT INTO poll_options
                (poll_id, option_text)
                VALUES (%s, %s)
                """,
                (poll_id, option)
            )

        connection.commit()

        return {
            "message": "Poll created successfully",
            "poll_id": poll_id,
            "session_code": session_code,
            "question": question,
            "options": options
        }

    except HTTPException:
        raise

    except Exception as e:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.get("/polls/{session_code}")
def get_polls(session_code: str):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        session_code = session_code.strip().upper()

        cursor.execute(
            """
            SELECT id, question, created_at
            FROM polls
            WHERE session_code = %s
            ORDER BY id DESC
            """,
            (session_code,)
        )

        polls = cursor.fetchall()

        for poll in polls:
            cursor.execute(
                """
                SELECT id, option_text
                FROM poll_options
                WHERE poll_id = %s
                ORDER BY id
                """,
                (poll["id"],)
            )

            poll["options"] = cursor.fetchall()

        return {
            "session_code": session_code,
            "polls": polls
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

# ============================================================
# VOTE SYSTEM
# ============================================================

@app.post("/polls/vote")
def vote_on_poll(vote: PollVote):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Check poll exists
        cursor.execute(
            """
            SELECT id, session_code
            FROM polls
            WHERE id = %s
            """,
            (vote.poll_id,)
        )

        poll = cursor.fetchone()

        if not poll:
            raise HTTPException(
                status_code=404,
                detail="Poll not found."
            )

        # Check option belongs to this poll
        cursor.execute(
            """
            SELECT id, option_text
            FROM poll_options
            WHERE id = %s AND poll_id = %s
            """,
            (vote.option_id, vote.poll_id)
        )

        option = cursor.fetchone()

        if not option:
            raise HTTPException(
                status_code=404,
                detail="Poll option not found."
            )

        # Check participant exists
        cursor.execute(
            """
            SELECT id
            FROM participants
            WHERE id = %s
            """,
            (vote.participant_id,)
        )

        participant = cursor.fetchone()

        if not participant:
            raise HTTPException(
                status_code=404,
                detail="Participant not found."
            )

        # Check if participant already voted
        cursor.execute(
            """
            SELECT id
            FROM votes
            WHERE poll_id = %s
            AND participant_id = %s
            """,
            (vote.poll_id, vote.participant_id)
        )

        existing_vote = cursor.fetchone()

        if existing_vote:
            raise HTTPException(
                status_code=400,
                detail="You have already voted in this poll."
            )

        # Save vote
        cursor.execute(
            """
            INSERT INTO votes
            (poll_id, option_id, participant_id)
            VALUES (%s, %s, %s)
            """,
            (
                vote.poll_id,
                vote.option_id,
                vote.participant_id
            )
        )

        connection.commit()

        return {
            "message": "Vote submitted successfully",
            "poll_id": vote.poll_id,
            "option_id": vote.option_id,
            "participant_id": vote.participant_id
        }

    except HTTPException:
        raise

    except Exception as e:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
        
# ============================================================
# POLL RESULTS
# ============================================================

@app.get("/polls/{poll_id}/results")
def get_poll_results(poll_id: int):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        # Check poll exists
        cursor.execute(
            """
            SELECT id, session_code, question
            FROM polls
            WHERE id = %s
            """,
            (poll_id,)
        )

        poll = cursor.fetchone()

        if not poll:
            raise HTTPException(
                status_code=404,
                detail="Poll not found."
            )

        # Get options with vote counts
        cursor.execute(
            """
            SELECT
                po.id AS option_id,
                po.option_text,
                COUNT(v.id) AS vote_count
            FROM poll_options po
            LEFT JOIN votes v
                ON po.id = v.option_id
                AND v.poll_id = po.poll_id
            WHERE po.poll_id = %s
            GROUP BY po.id, po.option_text
            ORDER BY po.id
            """,
            (poll_id,)
        )

        results = cursor.fetchall()

        total_votes = sum(
            int(result["vote_count"])
            for result in results
        )

        return {
            "poll_id": poll["id"],
            "session_code": poll["session_code"],
            "question": poll["question"],
            "total_votes": total_votes,
            "results": results
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()