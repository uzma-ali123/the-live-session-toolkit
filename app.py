import streamlit as st
import random
import string
import requests
import uuid
import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="The Live Session Toolkit",
    page_icon="🎤",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------- CREATE SESSION CODE ----------
def generate_session_code():
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )


# ==================================================
# HOME PAGE
# ==================================================

def home_page():

    st.title("🎤 The Live Session Toolkit")

    st.markdown("### Make every live session interactive.")

    st.write(
        "Create live sessions, engage your audience, run polls, "
        "collect feedback and generate session insights — all in one place."
    )

    st.divider()

    st.subheader("What would you like to do?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🎙️ Host a Session")

        st.write(
            "Create and manage your live session. "
            "Run polls, Q&A, reactions and view audience responses."
        )

        if st.button(
            "Create a Session",
            use_container_width=True
        ):
            st.session_state.page = "create"
            st.rerun()

    with col2:
        st.markdown("## 👥 Join a Session")

        st.write(
            "Join an existing live session using a session code "
            "or QR code."
        )

        if st.button(
            "Join a Session",
            use_container_width=True
        ):
            st.session_state.page = "join"
            st.rerun()

    st.divider()

    st.subheader("✨ Key Features")

    feature1, feature2, feature3, feature4 = st.columns(4)

    with feature1:
        st.markdown("### 📊 Live Polls")
        st.write("Ask questions and see responses in real time.")

    with feature2:
        st.markdown("### ❓ Q&A")
        st.write("Let your audience ask questions during the session.")

    with feature3:
        st.markdown("### ❤️ Reactions")
        st.write("Keep the audience engaged with quick reactions.")

    with feature4:
        st.markdown("### 📈 Analytics")
        st.write("Review session responses and generate insights.")

    st.divider()

    st.caption(
        "The Live Session Toolkit • Interactive sessions made simple"
    )


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
                        f"{BACKEND_URL}/sessions"
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

# ==================================================
# HOST DASHBOARD
# ==================================================

def host_dashboard_page():

    st.title("🎙️ Host Dashboard")

    st.success(
        f"Live Session: {st.session_state.session_name}"
    )

    st.write(
        f"Session Code: **{st.session_state.session_code}**"
    )

    st.divider()

    st.subheader("🎛️ Session Controls")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Polls")
        st.write("Create questions and collect audience votes.")

        if st.button("Open Polls", use_container_width=True):
            st.info("Poll module will be connected next.")

    with col2:
        st.markdown("### ❓ Q&A")
        st.write("Receive and manage audience questions.")

        if st.button("Open Q&A", use_container_width=True):
            st.info("Q&A module will be connected next.")

    with col3:
        st.markdown("### ❤️ Reactions")
        st.write("See audience reactions during the session.")

        if st.button("View Reactions", use_container_width=True):
            st.info("Reaction module will be connected next.")

    st.divider()

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("### 📢 Announcements")
        st.write("Send important messages to your audience.")

        if st.button("Announcement", use_container_width=True):
            st.info("Announcement module will be connected next.")

    with col5:
        st.markdown("### 👥 Participants")
        st.write("Monitor people currently joining the session.")

        if st.button("Participants", use_container_width=True):
            st.info("Participant management will be connected next.")

    with col6:
        st.markdown("### 📈 Analytics")
        st.write("View responses and session insights.")

        if st.button("View Analytics", use_container_width=True):
            st.info("Analytics will be connected later.")

    st.divider()

    st.subheader("🔴 Session Status")

    st.success("Session is ready to run.")

    if st.button(
        "⛔ End Session",
        use_container_width=True
    ):
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
                    f"{BACKEND_URL}/sessions"
                    json={
                        "session_code": session_code.strip().upper(),
                        "participant_name": participant_name.strip()
                    }
                )

                if response.status_code == 200:

                    st.session_state.session_code = session_code.strip().upper()
                    st.session_state.participant_name = participant_name.strip()

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

    # ==================================================
# JOINED SESSION PAGE
# ==================================================

def joined_session_page():

    st.title("🎉 You Joined the Live Session!")

    st.success(
        f"Session Code: {st.session_state.session_code}"
    )

    st.write(
        f"Welcome, **{st.session_state.participant_name}**!"
    )

    st.divider()

    st.subheader("🎛️ Live Session")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Polls")
        st.write("Participate in live polls.")

        if st.button("View Polls", use_container_width=True):
            st.info("Live polls will be connected next.")

    with col2:
        st.markdown("### ❓ Q&A")
        st.write("Ask questions during the session.")

        if st.button("Ask a Question", use_container_width=True):
            st.info("Q&A will be connected next.")

    with col3:
        st.markdown("### ❤️ Reactions")
        st.write("Send reactions to the host.")

        if st.button("Send Reaction", use_container_width=True):
            st.info("Reactions will be connected next.")

    st.divider()

    st.info(
        "You are successfully connected to the live session."
    )

    if st.button(
        "← Leave Session",
        use_container_width=True
    ):

        st.session_state.page = "home"
        st.rerun()

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
                    f"{BACKEND_URL}/sessions"
                    json={
                        "session_code": session_code.strip().upper(),
                        "participant_name": participant_name.strip()
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.session_code = session_code.strip().upper()
                    st.session_state.participant_name = participant_name.strip()
                    st.session_state.page = "joined"

                    st.success("Successfully joined the session!")

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
        # ==================================================
# PAGE ROUTING
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "create":
    create_session_page()

elif st.session_state.page == "join":
    join_page()

elif st.session_state.page == "host_dashboard":
    host_dashboard_page()

elif st.session_state.page == "joined":
    joined_session_page()