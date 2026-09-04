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