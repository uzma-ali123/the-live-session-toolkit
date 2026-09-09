import os
import random
import string
from io import BytesIO

import qrcode
import requests
import streamlit as st

try:
    BACKEND_URL = st.secrets["BACKEND_URL"]
except Exception:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Live Session Toolkit",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# SaaS UI
# ==================================================

st.markdown(
    """
<style>
#MainMenu, footer {visibility:hidden;}
header {background:transparent !important;}
.stApp {background:#f5f7fb;}
.main .block-container {max-width:1500px; padding:2rem 2.6rem 3rem;}

/* Hide Streamlit's sidebar decoration / empty blocks */
section[data-testid="stSidebar"] {background:#0f172a !important; border-right:1px solid #1e293b;}
section[data-testid="stSidebar"] > div {background:#0f172a !important;}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {background:#0f172a !important; padding:1.2rem 1rem 1.5rem;}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {background:transparent !important;}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {background:transparent !important;}
section[data-testid="stSidebar"] .stMarkdown {background:transparent !important;}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {color:#e5e7eb;}

.brand {font-size:1.18rem;font-weight:800;color:#fff !important;letter-spacing:-.02em;margin:.1rem 0 0;}
.brand-sub {font-size:.73rem;color:#94a3b8 !important;margin:.2rem 0 1.1rem;}
.nav-title {font-size:.66rem;font-weight:800;letter-spacing:.12em;color:#64748b !important;margin:1rem .2rem .45rem;}
.session-mini {background:#172033;border:1px solid #263449;border-radius:12px;padding:.8rem .85rem;margin-top:.75rem;}
.session-mini-label {font-size:.64rem;color:#94a3b8 !important;font-weight:700;letter-spacing:.08em;}
.session-mini-code {font-size:1.15rem;color:#fff !important;font-weight:800;letter-spacing:.14em;margin-top:.2rem;}
.session-mini-name {font-size:.72rem;color:#cbd5e1 !important;margin-top:.2rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}

section[data-testid="stSidebar"] .stButton > button {
    background:transparent !important;border:1px solid transparent !important;color:#cbd5e1 !important;
    text-align:left !important;border-radius:9px !important;min-height:40px !important;padding:.5rem .75rem !important;
    font-weight:600 !important;margin:.08rem 0 !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {background:#172033 !important;border-color:#263449 !important;color:#fff !important;}
section[data-testid="stSidebar"] .stButton > button p {color:inherit !important;}

h1 {font-size:2.25rem !important;color:#0f172a !important;letter-spacing:-.035em;}
h2,h3 {color:#0f172a !important;}
p {color:#64748b;}

/* Topbar */
.topbar {display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:1.5rem;}
.eyebrow {font-size:.72rem;font-weight:800;letter-spacing:.11em;color:#64748b;text-transform:uppercase;}
.page-title {font-size:2.1rem;font-weight:800;color:#0f172a;letter-spacing:-.04em;margin-top:.18rem;}
.page-subtitle {color:#64748b;font-size:.92rem;margin-top:.3rem;}
.live-pill {display:inline-flex;align-items:center;gap:.45rem;background:#ecfdf5;border:1px solid #a7f3d0;color:#047857;border-radius:999px;padding:.4rem .7rem;font-size:.72rem;font-weight:800;}
.live-dot {width:7px;height:7px;border-radius:50%;background:#10b981;display:inline-block;}

.card {background:#fff;border:1px solid #e5e7eb;border-radius:16px;padding:1.25rem;box-shadow:0 5px 18px rgba(15,23,42,.045);}
.card-title {font-size:1rem;font-weight:750;color:#111827;margin-bottom:.3rem;}
.card-text {font-size:.84rem;color:#64748b;line-height:1.55;}
.metric {background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:1.05rem 1.1rem;box-shadow:0 4px 15px rgba(15,23,42,.035);}
.metric-label {font-size:.68rem;font-weight:800;color:#94a3b8;letter-spacing:.08em;}
.metric-value {font-size:1.65rem;font-weight:800;color:#0f172a;margin-top:.18rem;}
.metric-note {font-size:.72rem;color:#64748b;margin-top:.12rem;}
.section-head {display:flex;justify-content:space-between;align-items:end;gap:1rem;margin:1.6rem 0 .75rem;}
.section-title {font-size:1.08rem;font-weight:800;color:#0f172a;}
.section-caption {font-size:.78rem;color:#94a3b8;}
.code-box {background:#0f172a;border-radius:14px;padding:1.15rem 1.25rem;color:#fff;}
.code-label {font-size:.64rem;color:#94a3b8;font-weight:800;letter-spacing:.1em;}
.code-value {font-size:1.8rem;font-weight:850;letter-spacing:.16em;margin-top:.2rem;}
.activity {padding:.8rem 0;border-bottom:1px solid #eef2f7;}
.activity:last-child {border-bottom:0;}
.activity-title {font-size:.86rem;font-weight:700;color:#1e293b;}
.activity-text {font-size:.75rem;color:#94a3b8;margin-top:.15rem;}

.main .stButton > button {border-radius:10px;min-height:42px;font-weight:650;border:1px solid #dbe1e8;background:#fff;color:#0f172a;}
.main .stButton > button:hover {background:#0f172a;color:#fff;border-color:#0f172a;}
.stTextInput input,.stTextArea textarea {border-radius:10px !important;border:1px solid #dbe1e8 !important;background:#fff !important;color:#111827 !important;}
.stTextInput input:focus,.stTextArea textarea:focus {border-color:#64748b !important;box-shadow:0 0 0 1px #64748b !important;}
[data-testid="stDataFrame"] {border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;}

.hero {background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:20px;padding:2.5rem 2.6rem;margin-bottom:1.5rem;box-shadow:0 12px 30px rgba(15,23,42,.12);}
.hero-kicker {color:#94a3b8;font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;}
.hero-title {color:#fff;font-size:2.55rem;font-weight:850;letter-spacing:-.045em;line-height:1.08;margin:.55rem 0 .8rem;}
.hero-text {color:#cbd5e1;font-size:.94rem;max-width:760px;line-height:1.65;}

@media (max-width:900px){.main .block-container{padding:1.2rem}.hero-title{font-size:2rem}.page-title{font-size:1.7rem}}
</style>
""",
    unsafe_allow_html=True,
)

# ==================================================
# STATE
# ==================================================

DEFAULT_STATE = {
    "page": "home",
    "host_authenticated": False,
    "host_active": False,
    "session_name": "",
    "host_name": "",
    "session_code": "",
    "participant_id": None,
    "participant_name": "",
    "last_poll_id": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(page):
    st.session_state.page = page
    st.rerun()


def api_error(response, action):
    try:
        detail = response.json().get("detail", response.text)
    except Exception:
        detail = response.text
    st.error(f"{action}: {detail}")


def get_list(data, key):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        value = data.get(key, data.get("data", []))
        return value if isinstance(value, list) else []
    return []


def clear_host():
    st.session_state.host_authenticated = False
    st.session_state.host_active = False
    st.session_state.session_code = ""
    st.session_state.session_name = ""
    st.session_state.host_name = ""
    st.session_state.last_poll_id = None


def clear_participant():
    st.session_state.participant_id = None
    st.session_state.participant_name = ""
    st.session_state.session_code = ""

# ==================================================
# SIDEBAR
# ==================================================

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="brand">Live Session Toolkit</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Interactive live-session platform</div>', unsafe_allow_html=True)

        st.markdown('<div class="nav-title">WORKSPACE</div>', unsafe_allow_html=True)

        if st.button("Dashboard", key="nav_dashboard", use_container_width=True):
            go_to("dashboard" if st.session_state.host_authenticated else "home")

        if st.session_state.host_authenticated:
            nav_items = [
                ("Sessions", "sessions"),
                ("Participants", "participants"),
                ("Polls", "polls"),
                ("Q&A", "qa"),
                ("Announcements", "announcements"),
                ("Reactions", "reactions"),
                ("Analytics", "analytics"),
            ]
            for label, page in nav_items:
                if st.button(label, key=f"nav_{page}", use_container_width=True):
                    go_to(page)
        else:
            if st.button("Host Login", key="nav_host_login", use_container_width=True):
                go_to("host_login")
            if st.button("Join Session", key="nav_join", use_container_width=True):
                go_to("join")

        if st.session_state.host_authenticated:
            st.markdown('<div class="nav-title">SESSION</div>', unsafe_allow_html=True)
            code = st.session_state.get("session_code", "")
            name = st.session_state.get("session_name", "Live Session")
            st.markdown(
                f'<div class="session-mini"><div class="session-mini-label">LIVE SESSION</div>'
                f'<div class="session-mini-code">{code or "------"}</div>'
                f'<div class="session-mini-name">{name}</div></div>',
                unsafe_allow_html=True,
            )

            st.markdown('<div class="nav-title">ACCOUNT</div>', unsafe_allow_html=True)
            if st.button("Log out", key="nav_logout", use_container_width=True):
                clear_host()
                go_to("home")
        else:
            st.markdown('<div class="nav-title">GET STARTED</div>', unsafe_allow_html=True)
            if st.button("Create Session", key="nav_create", use_container_width=True):
                go_to("create")

        st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:.68rem;color:#64748b;text-align:center;">Live Session Toolkit · v1.0</div>', unsafe_allow_html=True)

# ==================================================
# SHARED HOST HEADER
# ==================================================

def host_header(title, subtitle):
    st.markdown(
        f'<div class="topbar"><div><div class="eyebrow">LIVE SESSION TOOLKIT</div>'
        f'<div class="page-title">{title}</div><div class="page-subtitle">{subtitle}</div></div>'
        f'<div class="live-pill"><span class="live-dot"></span>LIVE</div></div>',
        unsafe_allow_html=True,
    )


def host_counts():
    code = st.session_state.get("session_code", "")
    counts = {"participants": 0, "polls": 0, "questions": 0, "reactions": 0}
    try:
        r = requests.get(f"{BACKEND_URL}/sessions/{code}/participants", timeout=8)
        if r.status_code == 200:
            counts["participants"] = len(get_list(r.json(), "participants"))
    except requests.RequestException:
        pass
    try:
        r = requests.get(f"{BACKEND_URL}/polls/{code}", timeout=8)
        if r.status_code == 200:
            counts["polls"] = len(get_list(r.json(), "polls"))
    except requests.RequestException:
        pass
    try:
        r = requests.get(f"{BACKEND_URL}/questions/{code}", timeout=8)
        if r.status_code == 200:
            counts["questions"] = len(get_list(r.json(), "questions"))
    except requests.RequestException:
        pass
    try:
        r = requests.get(f"{BACKEND_URL}/reactions/{code}", timeout=8)
        if r.status_code == 200:
            counts["reactions"] = sum(int(x.get("count", 0)) for x in get_list(r.json(), "reactions"))
    except requests.RequestException:
        pass
    return counts

# ==================================================
# HOME
# ==================================================

def home_page():
    st.markdown(
        '<div class="hero"><div class="hero-kicker">LIVE SESSION TOOLKIT</div>'
        '<div class="hero-title">Run live sessions that feel like a real product.</div>'
        '<div class="hero-text">Create a session, invite your audience, launch polls, collect questions, '
        'send announcements and understand engagement from one clean workspace.</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-head"><div><div class="section-title">Get started</div>'
                '<div class="section-caption">Choose how you want to use the platform.</div></div></div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-title">Host a Session</div>'
                    '<div class="card-text">Create a protected host workspace with a session code, PIN, '
                    'polls, Q&A, announcements, reactions and audience analytics.</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("Create a Session", key="home_create", use_container_width=True):
            go_to("create")
    with c2:
        st.markdown('<div class="card"><div class="card-title">Join a Session</div>'
                    '<div class="card-text">Enter a session code and participate in live polls, questions, '
                    'announcements and reactions.</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("Join a Session", key="home_join", use_container_width=True):
            go_to("join")

    st.markdown('<div class="section-head"><div><div class="section-title">Built for engagement</div>'
                '<div class="section-caption">Everything important is organized in the workspace.</div></div></div>',
                unsafe_allow_html=True)
    cols = st.columns(4)
    features = [
        ("Live Polls", "Create questions and collect audience votes."),
        ("Q&A", "Give participants a direct channel to ask questions."),
        ("Announcements", "Send important messages to everyone instantly."),
        ("Analytics", "See participation and interaction at a glance."),
    ]
    for col, (title, text) in zip(cols, features):
        with col:
            st.markdown(f'<div class="card"><div class="card-title">{title}</div>'
                        f'<div class="card-text">{text}</div></div>', unsafe_allow_html=True)

# ==================================================
# CREATE SESSION
# ==================================================

def create_session_page():
    st.markdown('<div class="eyebrow">HOST WORKSPACE</div><div class="page-title">Create a session</div>'
                '<div class="page-subtitle">Set up your live room and protect host access with a 6-digit PIN.</div>',
                unsafe_allow_html=True)
    st.write("")

    left, right = st.columns([1.45, 1])
    with left:
        session_name = st.text_input("Session Name", placeholder="Cybersecurity Awareness Session")
        host_name = st.text_input("Your Name", placeholder="Enter host name")
        host_pin = st.text_input("Host PIN", placeholder="Create a 6-digit PIN", type="password", max_chars=6)
        st.caption("Keep this PIN safe. You will need it to log back into the host dashboard.")
        if st.button("Create Session", key="create_session_btn", use_container_width=True):
            if not session_name.strip() or not host_name.strip() or not host_pin.strip():
                st.warning("Please enter Session Name, Your Name and Host PIN.")
                return
            if not host_pin.strip().isdigit() or len(host_pin.strip()) != 6:
                st.warning("Host PIN must be exactly 6 digits.")
                return
            try:
                r = requests.post(
                    f"{BACKEND_URL}/sessions",
                    json={
                        "title": session_name.strip(),
                        "host_name": host_name.strip(),
                        "host_email": f'{host_name.strip().lower().replace(" ", "_")}@example.com',
                        "host_pin": host_pin.strip(),
                    },
                    timeout=10,
                )
                if r.status_code == 200:
                    data = r.json()
                    st.session_state.session_name = data["title"]
                    st.session_state.host_name = data["host_name"]
                    st.session_state.session_code = data["session_code"]
                    st.session_state.host_active = True
                    st.session_state.host_authenticated = True
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    api_error(r, "Session creation failed")
            except requests.RequestException as e:
                st.error(f"Backend connection failed: {e}")
    with right:
        st.markdown('<div class="card"><div class="card-title">What you get</div>'
                    '<div class="activity"><div class="activity-title">Protected host access</div>'
                    '<div class="activity-text">Session code + private 6-digit Host PIN.</div></div>'
                    '<div class="activity"><div class="activity-title">Audience interaction</div>'
                    '<div class="activity-text">Polls, Q&A, announcements and reactions.</div></div>'
                    '<div class="activity"><div class="activity-title">Live insights</div>'
                    '<div class="activity-text">Participant and engagement analytics.</div></div></div>', unsafe_allow_html=True)

# ==================================================
# HOST LOGIN
# ==================================================

def host_login_page():
    st.markdown('<div class="eyebrow">SECURE ACCESS</div><div class="page-title">Host Login</div>'
                '<div class="page-subtitle">Use the session code and Host PIN you created for this room.</div>',
                unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1, 1.2])
    with left:
        code = st.text_input("Session Code", placeholder="ABC123", key="login_code")
        pin = st.text_input("Host PIN", placeholder="6-digit PIN", type="password", max_chars=6, key="login_pin")
        if st.button("Login as Host", key="login_btn", use_container_width=True):
            if not code.strip() or not pin.strip():
                st.warning("Please enter both Session Code and Host PIN.")
                return
            if not pin.strip().isdigit() or len(pin.strip()) != 6:
                st.warning("Host PIN must be exactly 6 digits.")
                return
            try:
                r = requests.post(f"{BACKEND_URL}/host/login", json={"session_code": code.strip().upper(), "host_pin": pin.strip()}, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    st.session_state.host_authenticated = True
                    st.session_state.host_active = True
                    st.session_state.session_code = data["session_code"]
                    st.session_state.session_name = data["title"]
                    st.session_state.host_name = data["host_name"]
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    api_error(r, "Host login failed")
            except requests.RequestException as e:
                st.error(f"Backend connection failed: {e}")
    with right:
        st.markdown('<div class="card"><div class="card-title">Host access</div>'
                    '<div class="card-text">Your Host PIN is stored on the backend as a SHA-256 hash. '
                    'Use the same 6-digit PIN you created with the session.</div></div>', unsafe_allow_html=True)

# ==================================================
# DASHBOARD
# ==================================================

def dashboard_page():
    if not st.session_state.get("host_authenticated", False):
        go_to("host_login")
        return
    code = st.session_state.session_code
    name = st.session_state.session_name
    host = st.session_state.host_name
    counts = host_counts()
    host_header("Dashboard", f"Welcome back, {host}. Your live workspace is ready.")

    metrics = [
        ("PARTICIPANTS", counts["participants"], "Audience registered"),
        ("POLLS", counts["polls"], "Interactive polls"),
        ("QUESTIONS", counts["questions"], "Audience questions"),
        ("REACTIONS", counts["reactions"], "Total reactions"),
    ]
    cols = st.columns(4)
    for col, (label, value, note) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="metric"><div class="metric-label">{label}</div>'
                        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
                        unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.3, .7])
    with left:
        st.markdown(f'<div class="card"><div class="card-title">{name}</div>'
                    f'<div class="card-text">Your session is live. Use the workspace navigation to manage each part of the event.</div>'
                    f'<div style="height:.9rem"></div><div class="code-box"><div class="code-label">SESSION CODE</div>'
                    f'<div class="code-value">{code}</div></div></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="card"><div class="card-title">Quick actions</div></div>', unsafe_allow_html=True)
        if st.button("Create Poll", key="dash_poll", use_container_width=True): go_to("polls")
        if st.button("View Participants", key="dash_part", use_container_width=True): go_to("participants")
        if st.button("Open Q&A", key="dash_qa", use_container_width=True): go_to("qa")
        if st.button("Send Announcement", key="dash_ann", use_container_width=True): go_to("announcements")

    st.markdown('<div class="section-head"><div><div class="section-title">Session overview</div>'
                '<div class="section-caption">Your main controls are one click away in the sidebar.</div></div></div>', unsafe_allow_html=True)
    overview = st.columns(3)
    with overview[0]:
        st.markdown('<div class="card"><div class="card-title">Participants</div><div class="card-text">Monitor who has joined and search the audience.</div></div>', unsafe_allow_html=True)
    with overview[1]:
        st.markdown('<div class="card"><div class="card-title">Engagement</div><div class="card-text">Use polls, Q&A and reactions to keep the room active.</div></div>', unsafe_allow_html=True)
    with overview[2]:
        st.markdown('<div class="card"><div class="card-title">Insights</div><div class="card-text">Review interaction totals and reaction breakdowns.</div></div>', unsafe_allow_html=True)

# ==================================================
# SESSIONS / QR
# ==================================================

def sessions_page():
    if not st.session_state.host_authenticated:
        go_to("host_login"); return
    code = st.session_state.session_code
    host_header("Sessions", "Manage the current live room and share access with your audience.")
    left, right = st.columns([1, 1.35])
    with left:
        st.markdown('<div class="card"><div class="card-title">Session access</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="code-box"><div class="code-label">SESSION CODE</div><div class="code-value">{code}</div></div>', unsafe_allow_html=True)
        st.write("")
        st.write(f"**Session:** {st.session_state.session_name}")
        st.write(f"**Host:** {st.session_state.host_name}")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="card"><div class="card-title">Session QR code</div>'
                    '<div class="card-text">Participants can scan this code and then enter the displayed session code on Join Session.</div></div>', unsafe_allow_html=True)
        qr = qrcode.QRCode(version=1, box_size=8, border=4)
        qr.add_data(code); qr.make(fit=True)
        img = qr.make_image()
        buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
        st.image(buf, width=240)
    st.write("")
    if st.button("Log out host", key="sessions_logout"):
        clear_host(); go_to("home")

# ==================================================
# PARTICIPANTS
# ==================================================

def participants_page():
    if not st.session_state.host_authenticated:
        go_to("host_login"); return
    code = st.session_state.session_code
    host_header("Participants", "Monitor everyone registered in your live session.")
    participants = []
    try:
        r = requests.get(f"{BACKEND_URL}/sessions/{code}/participants", timeout=10)
        if r.status_code == 200:
            participants = get_list(r.json(), "participants")
        else: api_error(r, "Could not load participants")
    except requests.RequestException as e: st.error(f"Connection error: {e}")
    a, b = st.columns(2)
    with a: st.markdown(f'<div class="metric"><div class="metric-label">CONNECTED</div><div class="metric-value">{len(participants)}</div><div class="metric-note">Registered participants</div></div>', unsafe_allow_html=True)
    with b: st.markdown('<div class="metric"><div class="metric-label">STATUS</div><div class="metric-value" style="font-size:1.25rem">Active</div><div class="metric-note">Session is live</div></div>', unsafe_allow_html=True)
    st.write("")
    search = st.text_input("Search Participant", placeholder="Search by name...", key="participant_search_saas")
    if search.strip():
        q = search.strip().lower(); participants = [p for p in participants if q in p.get("participant_name", "").lower()]
    rows = [{"No.": i, "Participant ID": p.get("id", ""), "Participant Name": p.get("participant_name", "Participant"), "Status": "Connected"} for i,p in enumerate(participants, 1)]
    if rows: st.dataframe(rows, use_container_width=True, hide_index=True)
    else: st.info("No participants found.")
    if st.button("Refresh", key="participants_refresh_saas"): st.rerun()

# ==================================================
# POLLS
# ==================================================

def polls_page():
    if not st.session_state.host_authenticated:
        go_to("host_login"); return
    code = st.session_state.session_code
    host_header("Polls", "Create live questions and review audience responses.")
    st.markdown('<div class="section-head"><div><div class="section-title">Create a poll</div><div class="section-caption">Use at least two answer options.</div></div></div>', unsafe_allow_html=True)
    question = st.text_input("Poll Question", placeholder="Which cybersecurity topic matters most?", key="saas_poll_question")
    c1,c2 = st.columns(2)
    with c1:
        o1=st.text_input("Option 1", key="saas_o1"); o2=st.text_input("Option 2", key="saas_o2")
    with c2:
        o3=st.text_input("Option 3", key="saas_o3"); o4=st.text_input("Option 4", key="saas_o4")
    if st.button("Create Poll", key="saas_create_poll", use_container_width=True):
        opts=[x.strip() for x in [o1,o2,o3,o4] if x.strip()]
        if not question.strip(): st.warning("Please enter a poll question.")
        elif len(opts)<2: st.warning("Please enter at least 2 options.")
        else:
            try:
                r=requests.post(f"{BACKEND_URL}/polls",json={"session_code":code,"question":question.strip(),"options":opts},timeout=10)
                if r.status_code==200:
                    st.session_state.last_poll_id=r.json().get("poll_id"); st.success("Poll created successfully.")
                else: api_error(r,"Poll creation failed")
            except requests.RequestException as e: st.error(f"Connection error: {e}")
    st.markdown('<div class="section-head"><div><div class="section-title">Existing polls</div><div class="section-caption">Refresh to see current poll data.</div></div></div>', unsafe_allow_html=True)
    try:
        r=requests.get(f"{BACKEND_URL}/polls/{code}",timeout=10)
        polls=get_list(r.json(),"polls") if r.status_code==200 else []
        if r.status_code!=200: api_error(r,"Could not load polls")
        if not polls: st.info("No polls created yet.")
        for poll in polls:
            st.markdown(f'<div class="card"><div class="card-title">{poll.get("question", "Poll")}</div><div class="card-text">{len(poll.get("options", []))} options · Poll ID {poll.get("id", "")}</div></div>',unsafe_allow_html=True)
            st.write("")
    except requests.RequestException as e: st.error(f"Connection error: {e}")

# ==================================================
# Q&A
# ==================================================

def qa_page():
    if not st.session_state.host_authenticated:
        go_to("host_login"); return
    code=st.session_state.session_code
    host_header("Q&A", "Review questions submitted by your audience.")
    try:
        r=requests.get(f"{BACKEND_URL}/questions/{code}",timeout=10)
        questions=get_list(r.json(),"questions") if r.status_code==200 else []
        if r.status_code!=200: api_error(r,"Could not load questions")
        if not questions: st.info("No questions have been submitted yet.")
        for q in questions:
            text=q.get("question",q.get("question_text","")); participant=q.get("participant_name","Participant")
            st.markdown(f'<div class="card"><div class="card-title">{text}</div><div class="card-text">Asked by {participant}</div></div>',unsafe_allow_html=True); st.write("")
    except requests.RequestException as e: st.error(f"Connection error: {e}")
    if st.button("Refresh Questions",key="qa_refresh_saas"): st.rerun()

# ==================================================
# ANNOUNCEMENTS
# ==================================================

def announcements_page():
    if not st.session_state.host_authenticated:
        go_to("host_login"); return
    code=st.session_state.session_code
    host_header("Announcements", "Send important messages to everyone in the live room.")
    message=st.text_area("Announcement Message",placeholder="Type an announcement...",height=120,key="saas_announcement")
    if st.button("Send Announcement",key="saas_send_announcement",use_container_width=True):
        if not message.strip(): st.warning("Please enter an announcement first.")
        else:
            try:
                r=requests.post(f"{BACKEND_URL}/announcements",json={"session_code":code,"message":message.strip()},timeout=10)
                if r.status_code==200: st.success("Announcement sent successfully.")
                else: api_error(r,"Announcement sending failed")
            except requests.RequestException as e: st.error(f"Connection error: {e}")
    st.markdown('<div class="section-head"><div><div class="section-title">Recent announcements</div></div></div>',unsafe_allow_html=True)
    try:
        r=requests.get(f"{BACKEND_URL}/announcements/{code}",timeout=10)
        items=get_list(r.json(),"announcements") if r.status_code==200 else []
        if not items: st.info("No announcements yet.")
        for item in items:
            st.markdown(f'<div class="card"><div class="card-title">{item.get("message","")}</div><div class="card-text">Live announcement</div></div>',unsafe_allow_html=True); st.write("")
    except requests.RequestException as e: st.error(f"Connection error: {e}")

# ==================================================
# REACTIONS
# ==================================================

def reactions_page():
    if not st.session_state.host_authenticated:
        go_to("host_login"); return
    code=st.session_state.session_code
    host_header("Reactions", "See how the audience is responding in real time.")
    try:
        r=requests.get(f"{BACKEND_URL}/reactions/{code}",timeout=10)
        items=get_list(r.json(),"reactions") if r.status_code==200 else []
        if not items: st.info("No reactions yet.")
        cols=st.columns(4)
        for i,item in enumerate(items):
            with cols[i%4]:
                st.markdown(f'<div class="metric"><div class="metric-label">{str(item.get("reaction","REACTION")).upper()}</div><div class="metric-value">{int(item.get("count",0))}</div></div>',unsafe_allow_html=True)
    except requests.RequestException as e: st.error(f"Connection error: {e}")
    if st.button("Refresh Reactions",key="reactions_refresh_saas"): st.rerun()

# ==================================================
# ANALYTICS
# ==================================================

def analytics_page():
    if not st.session_state.host_authenticated:
        go_to("host_login"); return
    code=st.session_state.session_code
    host_header("Analytics", "A simple live view of participation and engagement.")
    counts=host_counts()
    cols=st.columns(4)
    for col,(label,key) in zip(cols,[("PARTICIPANTS","participants"),("POLLS","polls"),("QUESTIONS","questions"),("REACTIONS","reactions")]):
        with col: st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{counts[key]}</div></div>',unsafe_allow_html=True)
    st.write("")
    total=counts["questions"]+counts["reactions"]+counts["polls"]
    st.markdown(f'<div class="card"><div class="card-title">Engagement summary</div>'
                f'<div class="card-text">Total tracked interactions: <strong>{total}</strong></div>'
                f'<div class="activity"><div class="activity-title">Questions</div><div class="activity-text">{counts["questions"]} submitted</div></div>'
                f'<div class="activity"><div class="activity-title">Reactions</div><div class="activity-text">{counts["reactions"]} received</div></div>'
                f'<div class="activity"><div class="activity-title">Polls</div><div class="activity-text">{counts["polls"]} created</div></div></div>',unsafe_allow_html=True)
    try:
        r=requests.get(f"{BACKEND_URL}/reactions/{code}",timeout=10)
        items=get_list(r.json(),"reactions") if r.status_code==200 else []
        if items:
            st.markdown('<div class="section-head"><div><div class="section-title">Reaction breakdown</div></div></div>',unsafe_allow_html=True)
            st.dataframe([{"Reaction":x.get("reaction",""),"Count":int(x.get("count",0))} for x in items],use_container_width=True,hide_index=True)
    except requests.RequestException:
        pass

# ==================================================
# JOIN + PARTICIPANT
# ==================================================

def join_page():
    st.markdown('<div class="eyebrow">AUDIENCE ACCESS</div><div class="page-title">Join a live session</div>'
                '<div class="page-subtitle">Enter the session code provided by your host.</div>',unsafe_allow_html=True)
    st.write("")
    code=st.text_input("Session Code",placeholder="ABC123",key="join_code_saas")
    participant=st.text_input("Your Name",placeholder="Enter your name",key="join_name_saas")
    if st.button("Join Session",key="join_session_saas",use_container_width=True):
        if not code.strip() or not participant.strip(): st.warning("Please enter both Session Code and Your Name."); return
        normalized=code.strip().upper(); pname=participant.strip()
        try:
            r=requests.post(f"{BACKEND_URL}/sessions/join",json={"session_code":normalized,"participant_name":pname},timeout=10)
            if r.status_code==200:
                data=r.json(); st.session_state.participant_id=data["participant_id"]; st.session_state.session_code=normalized; st.session_state.participant_name=pname; st.session_state.host_active=False; st.session_state.host_authenticated=False; st.session_state.page="joined"; st.rerun()
            else: api_error(r,"Unable to join session")
        except requests.RequestException as e: st.error(f"Backend connection failed: {e}")


def joined_page():
    code=st.session_state.session_code; pname=st.session_state.participant_name; pid=st.session_state.participant_id
    st.markdown('<div class="eyebrow">AUDIENCE</div><div class="page-title">Live session</div>'
                f'<div class="page-subtitle">Welcome, {pname}. Session code: {code}</div>',unsafe_allow_html=True)
    st.divider()
    st.subheader("Live Polls")
    try:
        r=requests.get(f"{BACKEND_URL}/polls/{code}",timeout=10)
        polls=get_list(r.json(),"polls") if r.status_code==200 else []
        if not polls: st.info("No polls available yet.")
        for poll in polls:
            st.markdown(f'**{poll.get("question","")}**')
            opts=poll.get("options",[])
            labels=[o.get("option_text","") for o in opts]
            if labels:
                selected=st.radio("Choose your answer",labels,key=f"join_poll_{poll.get('id')}")
                if st.button("Submit Vote",key=f"join_vote_{poll.get('id')}"):
                    option=next(o for o in opts if o.get("option_text")==selected)
                    try:
                        vr=requests.post(f"{BACKEND_URL}/polls/vote",json={"poll_id":poll.get("id"),"option_id":option.get("id"),"participant_id":pid},timeout=10)
                        if vr.status_code==200: st.success("Your vote has been submitted.")
                        else: api_error(vr,"Vote submission failed")
                    except requests.RequestException as e: st.error(f"Connection error: {e}")
            st.divider()
    except requests.RequestException as e: st.error(f"Connection error: {e}")

    st.subheader("Ask a Question")
    q=st.text_area("Your Question",placeholder="Type your question...",key="joined_question_saas")
    if st.button("Submit Question",key="joined_submit_q",use_container_width=True):
        if not q.strip(): st.warning("Please enter a question first.")
        else:
            try:
                r=requests.post(f"{BACKEND_URL}/questions",json={"session_code":code,"participant_id":pid,"question_text":q.strip()},timeout=10)
                if r.status_code==200: st.success("Your question has been submitted.")
                else: api_error(r,"Question submission failed")
            except requests.RequestException as e: st.error(f"Connection error: {e}")

    st.subheader("Live Announcements")
    try:
        r=requests.get(f"{BACKEND_URL}/announcements/{code}",timeout=10)
        items=get_list(r.json(),"announcements") if r.status_code==200 else []
        if not items: st.info("No announcements yet.")
        for item in items: st.markdown(f'<div class="card"><div class="card-title">{item.get("message","")}</div><div class="card-text">Live announcement</div></div>',unsafe_allow_html=True)
    except requests.RequestException: pass

    st.subheader("Live Reactions")
    cols=st.columns(4)
    for label,col in [("Like",cols[0]),("Love",cols[1]),("Clap",cols[2]),("Interesting",cols[3])]:
        with col:
            if st.button(label,key=f"joined_reaction_{label.lower()}",use_container_width=True):
                try:
                    r=requests.post(f"{BACKEND_URL}/reactions",json={"session_code":code,"participant_id":pid,"reaction":label},timeout=10)
                    if r.status_code==200: st.success(f"{label} sent.")
                    else: api_error(r,"Reaction submission failed")
                except requests.RequestException as e: st.error(f"Connection error: {e}")
    st.write("")
    if st.button("Leave Session",key="joined_leave",use_container_width=True):
        clear_participant(); st.session_state.host_authenticated=False; st.session_state.host_active=False; go_to("home")

# ==================================================
# ROUTING
# ==================================================

render_sidebar()

page=st.session_state.page
if page=="home": home_page()
elif page=="create": create_session_page()
elif page=="host_login": host_login_page()
elif page=="dashboard": dashboard_page()
elif page=="sessions": sessions_page()
elif page=="participants": participants_page()
elif page=="polls": polls_page()
elif page=="qa": qa_page()
elif page=="announcements": announcements_page()
elif page=="reactions": reactions_page()
elif page=="analytics": analytics_page()
elif page=="join": join_page()
elif page=="joined": joined_page()
else: st.session_state.page="home"; st.rerun()
