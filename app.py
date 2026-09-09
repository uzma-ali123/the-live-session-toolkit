import streamlit as st
import random
import string
import requests
import uuid
import os
try:
    BACKEND_URL = st.secrets["BACKEND_URL"]
except Exception:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Live Session Toolkit",
    layout="wide",
    initial_sidebar_state="locked"
)
# ---------- PROFESSIONAL UI ----------
st.markdown("""
<style>

    /* Global */
    .stApp {
        background-color: #f7f8fa;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    /* Main headings */
    h1 {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
        color: #111827;
    }

    h2 {
        font-weight: 650 !important;
        color: #111827;
    }

    h3 {
        font-weight: 600 !important;
        color: #1f2937;
    }

    /* Paragraph */
    p {
        color: #4b5563;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #d1d5db;
        background-color: #ffffff;
        color: #111827;
        font-weight: 600;
        padding: 0.65rem 1rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #111827;
        background-color: #111827;
        color: #ffffff;
    }

    /* Primary button */
    .primary-button {
        background-color: #111827;
        color: #ffffff;
        padding: 0.75rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
    }

    /* Inputs */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        background-color: #ffffff;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #111827;
        box-shadow: 0 0 0 1px #111827;
    }

    /* Cards */
    .app-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .app-card:hover {
        border-color: #d1d5db;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    }

    .card-title {
        font-size: 1.15rem;
        font-weight: 650;
        color: #111827;
        margin-bottom: 0.5rem;
    }

    .card-text {
        font-size: 0.95rem;
        color: #6b7280;
        line-height: 1.6;
    }

    /* Hero */
    .hero {
        background: #111827;
        border-radius: 16px;
        padding: 3rem;
        margin-bottom: 2rem;
    }

    .hero-title {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 750;
        line-height: 1.1;
        margin-bottom: 1rem;
    }

    .hero-text {
        color: #d1d5db;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 720px;
    }

    /* Status */
    .status-live {
        display: inline-block;
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        border-radius: 999px;
        padding: 0.35rem 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Metrics */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.25rem;
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: #111827;
        font-size: 1.8rem;
        font-weight: 700;
    }

    /* Divider */
    hr {
        border-color: #e5e7eb !important;
    }
/* Sidebar buttons */
section[data-testid="stSidebar"] button {
    background-color: #1f2937 !important;
    color: #ffffff !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] button p {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] button:hover {
    background-color: #374151 !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #ffffff;
}
/* Fix blank white area in sidebar */
section[data-testid="stSidebar"] .stMarkdown {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    min-height: 0 !important;
    height: auto !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "host_active" not in st.session_state:
    st.session_state.host_active = False

# ---------- PROFESSIONAL SIDEBAR ----------

def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div style="
                padding-bottom: 1.2rem;
                border-bottom: 1px solid #374151;
                margin-bottom: 1.5rem;
            ">
                <div style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: #ffffff;
                ">
                    Live Session Toolkit
                </div>

                <div style="
                    font-size: 0.78rem;
                    color: #9ca3af;
                    margin-top: 0.35rem;
                ">
                    Interactive session platform
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                color: #9ca3af;
                font-size: 0.72rem;
                font-weight: 600;
                letter-spacing: 0.08em;
                margin-bottom: 0.5rem;
            ">
                NAVIGATION
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

        if st.session_state.get("host_active", False):

            if st.button("Host Dashboard", use_container_width=True):
                st.session_state.page = "host_dashboard"
                st.rerun()

        if st.button("Join Session", use_container_width=True):
            st.session_state.page = "join"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                color: #9ca3af;
                font-size: 0.72rem;
                font-weight: 600;
                letter-spacing: 0.08em;
                margin-bottom: 0.5rem;
            ">
                SESSION
            </div>
            """,
            unsafe_allow_html=True
        )

        session_code = st.session_state.get("session_code")

        if session_code:

            st.markdown(
                f"""
                <div style="
                    background: #1f2937;
                    border: 1px solid #374151;
                    border-radius: 8px;
                    padding: 0.8rem;
                    margin-bottom: 0.75rem;
                ">
                    <div style="
                        color: #9ca3af;
                        font-size: 0.72rem;
                    ">
                        SESSION CODE
                    </div>

                    <div style="
                        color: #ffffff;
                        font-size: 1.15rem;
                        font-weight: 700;
                        letter-spacing: 0.08em;
                        margin-top: 0.25rem;
                    ">
                        {session_code}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div style="
                    color: #9ca3af;
                    font-size: 0.82rem;
                    line-height: 1.5;
                ">
                    No active session
                </div>
                """,
                unsafe_allow_html=True
            )
# ---------- CREATE SESSION CODE ----------
def generate_session_code():
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )


# ==================================================
# HOME PAGE
# ==================================================

def home_page():

    # HERO SECTION
    st.markdown("""
    <div class="hero">
        <div class="hero-title">
            Live sessions, built for real engagement.
        </div>
        <div class="hero-text">
            Create interactive sessions, connect with your audience,
            collect responses and manage everything from one place.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ACTION SECTION
    st.markdown("## Get started")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="app-card">
            <div class="card-title">Host a Session</div>
            <div class="card-text">
                Create a live session and manage polls, audience
                interaction, questions and session activity.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button(
            "Create a Session",
            use_container_width=True
        ):
            st.session_state.page = "create"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="app-card">
            <div class="card-title">Join a Session</div>
            <div class="card-text">
                Enter a session code and participate in live polls,
                questions and audience activities.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button(
            "Join a Session",
            use_container_width=True
        ):
            st.session_state.page = "join"
            st.rerun()

    st.write("")
    st.write("")

    # FEATURES
    st.markdown("## Everything you need for an interactive session")

    feature1, feature2, feature3, feature4 = st.columns(4)

    with feature1:
        st.markdown("""
        <div class="app-card">
            <div class="card-title">Live Polls</div>
            <div class="card-text">
                Ask questions and collect audience responses
                during your session.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with feature2:
        st.markdown("""
        <div class="app-card">
            <div class="card-title">Q&A</div>
            <div class="card-text">
                Give participants a dedicated space to ask
                questions and share ideas.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with feature3:
        st.markdown("""
        <div class="app-card">
            <div class="card-title">Reactions</div>
            <div class="card-text">
                Keep your audience involved with instant
                session reactions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with feature4:
        st.markdown("""
        <div class="app-card">
            <div class="card-title">Analytics</div>
            <div class="card-text">
                Review participation and session responses
                with clear insights.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # FOOTER
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #6b7280;
        font-size: 0.85rem;
    ">
        Live Session Toolkit
        <br>
        Interactive sessions made simple.
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# CREATE SESSION PAGE
# ==================================================

def create_session_page():

    st.title("🎙️ Create a Live Session")

    st.write("Fill in the details below to create your session.")

    st.divider()

    session_name = st.text_input(
        "Session Name",
        placeholder="Example: Cybersecurity Awareness Session"
    )

    host_name = st.text_input(
        "Your Name",
        placeholder="Enter host name"
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🚀 Create Session",
            use_container_width=True
        ):
            if session_name and host_name:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/sessions",
                        json={
                            "title": session_name,
                            "host_name": host_name,
                            "host_email": f"{host_name.strip().lower().replace(' ', '_')}@example.com"                        }
                    )

                    if response.status_code == 200:
                        data = response.json()

                        st.session_state.session_name = data["title"]
                        st.session_state.host_name = data["host_name"]
                        st.session_state.session_code = data["session_code"]
                        st.session_state.host_active = True

                        st.session_state.page = "session_created"

                        st.rerun()

                    else:
                        st.error(
                            f"Session creation failed: {response.text}"
                        )

                except Exception as e:
                    st.error(
                        f"Backend connection failed: {e}"
                    )

            else:
                st.warning(
                    "Please enter both Session Name and Host Name."
                )

    with col2:

        if st.button(
            "← Back to Home",
            use_container_width=True
        ):

            st.session_state.page = "home"

            st.rerun()


# ==================================================
# SESSION CREATED PAGE
# ==================================================

def session_created_page():

    st.title("🎉 Session Created Successfully!")

    st.success("Your live session is ready.")

    st.divider()

    st.subheader(
        f"🎙️ {st.session_state.session_name}"
    )

    st.write(
        f"**Host:** {st.session_state.host_name}"
    )

    st.write("")

    st.markdown("### 🔑 Your Session Code")

    st.code(
        st.session_state.session_code,
        language=None
    )

    st.info(
        "Share this Session Code with your audience so they can join."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶️ Start Live Session",
            use_container_width=True
        ):
            st.session_state.page = "host_dashboard"
            st.rerun()

    with col2:

        if st.button(
            "🏠 Back to Home",
            use_container_width=True
        ):
            st.session_state.page = "home"
            st.rerun()

def host_dashboard_page():

    st.title("🎤 Host Dashboard")

    session_code = st.session_state.get("session_code", "")

    st.success(f"Live Session: {session_code}")

    st.divider()

    # =========================================================
    # CREATE POLL
    # =========================================================

    st.header("📊 Create a Poll")

    question = st.text_input(
        "Poll Question",
        placeholder="Example: Which cybersecurity topic is most important?"
    )

    option1 = st.text_input("Option 1")
    option2 = st.text_input("Option 2")
    option3 = st.text_input("Option 3")
    option4 = st.text_input("Option 4")

    if st.button("🚀 Create Poll", use_container_width=True):

        options = [
            option1,
            option2,
            option3,
            option4
        ]

        options = [
            option.strip()
            for option in options
            if option.strip()
        ]

        if not question.strip():
            st.error("Please enter a poll question.")

        elif len(options) < 2:
            st.error("Please enter at least 2 options.")

        else:

            try:

                response = requests.post(
                    f"{BACKEND_URL}/polls",
                    json={
                        "session_code": session_code,
                        "question": question.strip(),
                        "options": options
                    },
                    timeout=10
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        f"Poll created successfully! Poll ID: {data['poll_id']}"
                    )

                    st.session_state.last_poll_id = data["poll_id"]

                else:

                    st.error(
                        f"Poll creation failed: {response.text}"
                    )

            except Exception as e:

                st.error(f"Connection error: {e}")

    st.divider()

    # =========================================================
    # POLL RESULTS
    # =========================================================

    st.header("📈 Poll Results")

    poll_id = st.session_state.get("last_poll_id")

    if poll_id:

        if st.button("🔄 Refresh Results"):

            try:

                response = requests.get(
                    f"{BACKEND_URL}/polls/{poll_id}/results",
                    timeout=10
                )

                if response.status_code == 200:

                    data = response.json()

                    st.subheader(data["question"])

                    st.write(
                        f"**Total Votes: {data['total_votes']}**"
                    )

                    for result in data["results"]:

                        st.write(
                            f"**{result['option_text']}** — "
                            f"{result['vote_count']} vote(s)"
                        )

                else:

                    st.error(
                        f"Could not load results: {response.text}"
                    )

            except Exception as e:

                st.error(f"Connection error: {e}")

    else:

        st.info("Create a poll first to see its results.")

    st.divider()

    if st.button("🏠 Back Home"):

        st.session_state.page = "home"

        st.rerun()
# ==================================================
# TEMPORARY JOIN PAGE
# ==================================================

def join_page():

    st.title("👥 Join a Live Session")

    st.write("Enter the session code provided by your host.")

    session_code = st.text_input(
        "Session Code",
        placeholder="e.g. GM3TFA"
    )

    participant_name = st.text_input(
        "Your Name",
        placeholder="Enter your name"
    )

    if st.button(
        "🚀 Join Session",
        use_container_width=True
    ):

        if not session_code or not participant_name:

            st.warning(
                "Please enter both Session Code and Your Name."
            )

        else:

            try:

                response = requests.post(
                    f"{BACKEND_URL}/sessions/join",
                    json={
                        "session_code": session_code.strip().upper(),
                        "participant_name": participant_name.strip()
                    }
                )

                if response.status_code == 200:
                    st.session_state.participant_id = response.json()["participant_id"]
                    st.session_state.session_code = session_code.strip().upper()
                    st.session_state.participant_name = participant_name.strip()
                    st.session_state.host_active = False

                    st.session_state.page = "joined"

                    st.success(
                        "Successfully joined the session!"
                    )

                    st.rerun()

                else:

                    st.error(
                        f"Unable to join session: {response.text}"
                    )

            except Exception as e:

                st.error(
                    f"Backend connection failed: {e}"
                )

    st.write("")

    if st.button(
        "← Back to Home",
        use_container_width=True
    ):

        st.session_state.page = "home"
        st.rerun()

def joined_session_page():

    st.title("👋 Live Session")

    session_code = st.session_state.get("session_code", "")
    participant_name = st.session_state.get(
        "participant_name",
        "Participant"
    )
    participant_id = st.session_state.get("participant_id")

    st.success(
        f"Welcome, {participant_name}!"
    )

    st.write(
        f"Session Code: **{session_code}**"
    )

    st.divider()

    # =========================================================
    # LOAD POLLS
    # =========================================================

    st.header("📊 Live Polls")

    try:

        response = requests.get(
            f"{BACKEND_URL}/polls/{session_code}",
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            polls = data.get("polls", [])

            if not polls:

                st.info("No polls available yet.")

            else:

                for poll in polls:

                    st.subheader(poll["question"])

                    options = poll.get("options", [])

                    option_labels = [
                        option["option_text"]
                        for option in options
                    ]

                    selected = st.radio(
                        "Choose your answer:",
                        option_labels,
                        key=f"poll_{poll['id']}"
                    )

                    if st.button(
                        "🗳️ Submit Vote",
                        key=f"vote_{poll['id']}"
                    ):

                        selected_option = next(
                            option
                            for option in options
                            if option["option_text"] == selected
                        )

                        try:

                            vote_response = requests.post(
                                f"{BACKEND_URL}/polls/vote",
                                json={
                                    "poll_id": poll["id"],
                                    "option_id": selected_option["id"],
                                    "participant_id": participant_id
                                },
                                timeout=10
                            )

                            if vote_response.status_code == 200:

                                st.success(
                                    "✅ Your vote has been submitted!"
                                )

                            else:

                                st.error(
                                    vote_response.text
                                )

                        except Exception as e:

                            st.error(
                                f"Connection error: {e}"
                            )

                    st.divider()

        else:

            st.error(
                f"Could not load polls: {response.text}"
            )

    except Exception as e:

        st.error(
            f"Connection error: {e}"
        )

    # =========================================================
    # LEAVE SESSION
    # =========================================================

    if st.button("🚪 Leave Session"):

        st.session_state.page = "home"

        st.rerun()

render_sidebar()

# ==================================================
# PAGE ROUTING
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "create":
    create_session_page()

elif st.session_state.page == "session_created":
    session_created_page()

elif st.session_state.page == "join":
    join_page()

elif st.session_state.page == "joined":
    joined_session_page()

elif st.session_state.page == "host_dashboard":
    host_dashboard_page()