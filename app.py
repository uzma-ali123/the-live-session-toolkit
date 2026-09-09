import os
import random
import string
from io import BytesIO

import qrcode
import requests
import streamlit as st
import plotly.graph_objects as go

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
#MainMenu, footer {visibility:hidden;}
header {background:transparent !important;}
.stApp {background:linear-gradient(180deg,#f7f9ff 0%,#f3f7fc 100%);font-family:'Inter',Arial,sans-serif;}
.main .block-container {max-width:1480px;padding:1.2rem 2.25rem 3.2rem;}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#061a3d 0%,#082552 52%,#0a1838 100%) !important;border-right:0 !important;}
section[data-testid="stSidebar"] > div, section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {background:transparent !important;}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"],section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"],section[data-testid="stSidebar"] .stMarkdown {background:transparent !important;}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {padding:.95rem .8rem 1.2rem;}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] label {color:#dce7fb;}
.brand-row{display:flex;align-items:center;gap:.65rem;margin:.35rem .45rem .1rem;}
.brand-mark{width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#6d4aff,#25b8ff);display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.25rem;font-weight:800;box-shadow:0 8px 20px rgba(67,56,202,.3);}
.brand{font-size:1.05rem;font-weight:800;color:#fff !important;letter-spacing:-.025em;margin:0;}
.brand-sub{font-size:.67rem;color:#8fa8d2 !important;margin:.05rem .45rem 1.1rem 3.25rem;}
.nav-title{font-size:.59rem;font-weight:800;letter-spacing:.16em;color:#6f8bb9 !important;margin:1rem .45rem .38rem;}
section[data-testid="stSidebar"] .stButton > button{background:transparent !important;border:1px solid transparent !important;color:#bfcde5 !important;text-align:left !important;border-radius:11px !important;min-height:39px !important;padding:.43rem .68rem !important;font-weight:600 !important;margin:.06rem 0 !important;}
section[data-testid="stSidebar"] .stButton > button:hover{background:linear-gradient(90deg,rgba(111,76,255,.34),rgba(43,174,255,.12)) !important;border-color:rgba(129,140,248,.25) !important;color:#fff !important;}
section[data-testid="stSidebar"] .stButton > button p{color:inherit !important;}
.session-mini{background:linear-gradient(145deg,rgba(102,75,255,.2),rgba(27,188,255,.08));border:1px solid rgba(148,163,184,.18);border-radius:15px;padding:.78rem .82rem;margin-top:.65rem;}
.session-mini-label{font-size:.57rem;color:#8ea7cc !important;font-weight:800;letter-spacing:.12em;}
.session-mini-code{font-size:1.1rem;color:#fff !important;font-weight:800;letter-spacing:.14em;margin-top:.16rem;}
.session-mini-name{font-size:.67rem;color:#c6d4eb !important;margin-top:.16rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.version{font-size:.62rem;color:#5f79a5 !important;text-align:center;margin-top:1.2rem;}
h1,h2,h3{color:#15213b !important;}
p{color:#667795;}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:1.15rem;}
.eyebrow{font-size:.64rem;font-weight:800;letter-spacing:.14em;color:#7384a4;text-transform:uppercase;}
.page-title{font-size:1.95rem;font-weight:800;color:#14213d;letter-spacing:-.035em;margin-top:.18rem;}
.page-subtitle{color:#71819e;font-size:.84rem;margin-top:.25rem;}
.live-pill{display:inline-flex;align-items:center;gap:.42rem;background:#e8fff5;border:1px solid #b8efd5;color:#07865c;border-radius:999px;padding:.42rem .75rem;font-size:.67rem;font-weight:800;}
.live-dot{width:7px;height:7px;border-radius:50%;background:#16b979;display:inline-block;box-shadow:0 0 0 4px rgba(22,185,121,.12);}
.hero{position:relative;overflow:hidden;background:linear-gradient(118deg,#061a3c 0%,#123b87 47%,#6530ec 100%);border-radius:24px;padding:2.15rem 2.35rem;margin-bottom:1.35rem;box-shadow:0 18px 42px rgba(30,53,103,.18);min-height:300px;}
.hero:before{content:"";position:absolute;width:410px;height:410px;right:-140px;top:-190px;border-radius:50%;background:rgba(255,255,255,.075);}
.hero:after{content:"";position:absolute;width:250px;height:250px;right:235px;bottom:-180px;border-radius:50%;background:rgba(65,209,255,.1);}
.hero-grid{position:relative;z-index:2;display:grid;grid-template-columns:1.15fr .85fr;gap:1rem;align-items:center;}
.hero-kicker{color:#b7c8e8;font-size:.64rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;}
.hero-title{color:#fff;font-size:2.45rem;font-weight:800;letter-spacing:-.045em;line-height:1.08;margin:.5rem 0 .7rem;max-width:800px;}
.hero-title .accent{color:#8de7ff;}
.hero-text{color:#d5e1f6;font-size:.88rem;max-width:720px;line-height:1.6;}
.hero-badges{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1rem;}
.hero-badge{display:inline-flex;align-items:center;gap:.32rem;color:#f5f8ff;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:.34rem .58rem;font-size:.64rem;font-weight:700;}
.hero-visual{position:relative;height:235px;display:flex;align-items:center;justify-content:center;}
.monitor{width:280px;height:165px;border-radius:15px;background:linear-gradient(145deg,#0b2d69,#162e74);border:1px solid rgba(255,255,255,.22);box-shadow:0 20px 38px rgba(0,0,0,.25);padding:14px;position:relative;}
.monitor-screen{height:100%;border-radius:10px;background:linear-gradient(145deg,#f8fbff,#eef3ff);padding:12px;}
.mini-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
.mini-line{height:8px;width:80px;border-radius:8px;background:#d7def0;}.mini-pill{height:18px;width:48px;border-radius:20px;background:#d9ffec;}
.mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}.mini-card{height:45px;border-radius:8px;background:#fff;border:1px solid #e6eaf4;padding:7px;}.mini-card b{font-size:9px;color:#243452;display:block;}.mini-bar{height:6px;border-radius:6px;background:linear-gradient(90deg,#4f8cff 70%,#e6ebf5 70%);margin-top:7px;}
.float-card{position:absolute;background:#fff;border:1px solid rgba(255,255,255,.65);border-radius:13px;padding:.58rem .72rem;box-shadow:0 12px 28px rgba(0,0,0,.2);font-size:.65rem;font-weight:800;color:#243452;}.float-card.poll{top:8px;right:5px;}.float-card.qa{bottom:5px;left:0;}.float-card.react{bottom:28px;right:-10px;}.float-card span{font-size:1rem;margin-right:.25rem;}
.section-head{display:flex;justify-content:space-between;align-items:end;gap:1rem;margin:1.4rem 0 .7rem;}
.section-title{font-size:1.04rem;font-weight:800;color:#17243f;}.section-caption{font-size:.74rem;color:#91a1bd;margin-top:.12rem;}
.action-card{min-height:118px;border-radius:17px;padding:1rem 1.05rem;border:1px solid #e3e8f4;box-shadow:0 8px 22px rgba(31,52,92,.05);position:relative;overflow:hidden;}
.action-card:after{content:"";position:absolute;width:120px;height:120px;border-radius:50%;right:-45px;bottom:-60px;background:rgba(111,76,255,.08);}
.action-card.host{background:linear-gradient(135deg,#fbf9ff,#f1edff);border-color:#e0d8ff;}.action-card.join{background:linear-gradient(135deg,#f5fffb,#ebfff7);border-color:#ccefe0;}
.action-icon{font-size:1.5rem;margin-bottom:.28rem;}.action-title{font-size:1rem;font-weight:800;color:#17243f;}.action-text{font-size:.76rem;color:#6b7c9d;line-height:1.48;margin:.22rem 0 0;max-width:90%;}
.feature-chip,.card,.metric,.qr-card,.reaction-card{background:#fff;border:1px solid #e3e8f2;border-radius:16px;box-shadow:0 8px 22px rgba(31,52,92,.045);}
.feature-chip{padding:.95rem;min-height:105px;}.feature-icon{font-size:1.15rem;margin-bottom:.22rem;}.card{padding:1rem 1.08rem;}.card-title{font-size:.92rem;font-weight:780;color:#17243f;margin-bottom:.22rem;}.card-text{font-size:.77rem;color:#6c7c9b;line-height:1.5;}
.metric{padding:.92rem 1rem;min-height:108px;}.metric-label{font-size:.59rem;font-weight:800;color:#91a1bd;letter-spacing:.1em;}.metric-value{font-size:1.65rem;font-weight:850;color:#14213d;margin-top:.12rem;}.metric-note{font-size:.66rem;color:#8290aa;margin-top:.05rem;}
.activity{padding:.7rem 0;border-bottom:1px solid #edf1f7;}.activity:last-child{border-bottom:0;}.activity-title{font-size:.78rem;font-weight:720;color:#243452;}.activity-text{font-size:.67rem;color:#91a1bd;margin-top:.1rem;}
.code-box{background:linear-gradient(135deg,#102d68,#6332eb);border-radius:15px;padding:1rem 1.12rem;color:#fff;box-shadow:0 10px 24px rgba(67,56,202,.18);}.code-label{font-size:.58rem;color:#c6d4ff;font-weight:800;letter-spacing:.1em;}.code-value{font-size:1.7rem;font-weight:850;letter-spacing:.16em;margin-top:.15rem;}
.qr-card{text-align:center;background:linear-gradient(145deg,#fff,#f7f9ff);padding:1rem;}.reaction-card{text-align:center;padding:.9rem;}.reaction-emoji{font-size:1.7rem;}.reaction-name{font-size:.65rem;color:#71809d;font-weight:750;margin-top:.22rem;}.reaction-count{font-size:1.35rem;color:#17243f;font-weight:850;margin-top:.05rem;}
.main .stButton > button{border-radius:10px;min-height:41px;font-weight:700;border:1px solid #dbe2ee;background:#fff;color:#18243e;transition:.15s;}.main .stButton > button:hover{background:linear-gradient(135deg,#eef2ff,#eaf8ff);color:#4f46e5;border-color:#c7d2fe;}
.stTextInput input,.stTextArea textarea{border-radius:10px !important;border:1px solid #dbe2ee !important;background:#fff !important;color:#17243f !important;}.stTextInput input:focus,.stTextArea textarea:focus{border-color:#7c83f6 !important;box-shadow:0 0 0 2px rgba(99,102,241,.1) !important;}
[data-testid="stDataFrame"]{border:1px solid #e3e8f2;border-radius:12px;overflow:hidden;}
@media(max-width:900px){.main .block-container{padding:1rem}.hero-grid{grid-template-columns:1fr}.hero-visual{display:none}.hero-title{font-size:1.85rem}.page-title{font-size:1.6rem}}
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

def make_qr(data):
    qr = qrcode.QRCode(version=1, box_size=7, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def home_page():
    st.markdown(
        '<div class="hero"><div class="hero-grid">'
        '<div><div class="hero-kicker">LIVE SESSION TOOLKIT</div>'
        '<div class="hero-title">Create, host and engage — <span class="accent">all in one place.</span></div>'
        '<div class="hero-text">Run interactive live sessions with polls, Q&amp;A, announcements, reactions and engagement insights from one clean workspace.</div>'
        '<div class="hero-badges"><span class="hero-badge">✓ Real-time</span><span class="hero-badge">✓ Interactive</span><span class="hero-badge">✓ Easy to use</span><span class="hero-badge">✓ Secure host access</span></div></div>'
        '<div class="hero-visual"><div class="monitor"><div class="monitor-screen"><div class="mini-top"><div class="mini-line"></div><div class="mini-pill"></div></div><div class="mini-grid"><div class="mini-card"><b>Participants</b><div class="mini-bar"></div></div><div class="mini-card"><b>Live Poll</b><div class="mini-bar" style="background:linear-gradient(90deg,#7c4dff 55%,#e6ebf5 55%);"></div></div><div class="mini-card"><b>Questions</b><div class="mini-bar" style="background:linear-gradient(90deg,#23b7a4 80%,#e6ebf5 80%);"></div></div><div class="mini-card"><b>Reactions</b><div class="mini-bar" style="background:linear-gradient(90deg,#ff9f43 45%,#e6ebf5 45%);"></div></div></div></div></div>'
        '<div class="float-card poll"><span>📊</span>Live Polls</div><div class="float-card qa"><span>💬</span>Q&amp;A</div><div class="float-card react"><span>❤️</span>Reactions</div></div>'
        '</div></div>', unsafe_allow_html=True
    )

    st.markdown('<div class="section-head"><div><div class="section-title">Get started</div><div class="section-caption">Choose how you want to use the platform.</div></div></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown('<div class="action-card host"><div class="action-icon">🎤</div><div class="action-title">Host a Session</div><div class="action-text">Create a protected live workspace with polls, Q&amp;A, announcements, reactions and analytics.</div></div>', unsafe_allow_html=True)
        if st.button("Create a Session  →", key="home_create", use_container_width=True): go_to("create")
    with c2:
        st.markdown('<div class="action-card join"><div class="action-icon">👥</div><div class="action-title">Join a Session</div><div class="action-text">Enter a session code and participate in live polls, questions, announcements and reactions.</div></div>', unsafe_allow_html=True)
        if st.button("Join a Session  →", key="home_join", use_container_width=True): go_to("join")

    st.markdown('<div class="section-head"><div><div class="section-title">Live workspace</div><div class="section-caption">Everything you need for a smooth interactive session.</div></div></div>', unsafe_allow_html=True)
    a,b,c = st.columns([1.15,1.0,.8], gap="medium")
    with a:
        if st.session_state.get("host_authenticated") and st.session_state.get("session_code"):
            counts=host_counts()
            st.markdown(f'<div class="card"><div class="card-title">Total Engagement</div><div class="card-text">Live activity at a glance.</div><div style="height:.65rem"></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;">'
                        f'<div class="feature-chip"><div class="feature-icon">👥</div><b>{counts["participants"]}</b><div class="card-text">Participants</div></div>'
                        f'<div class="feature-chip"><div class="feature-icon">📊</div><b>{counts["polls"]}</b><div class="card-text">Polls</div></div>'
                        f'<div class="feature-chip"><div class="feature-icon">💬</div><b>{counts["questions"]}</b><div class="card-text">Questions</div></div>'
                        f'<div class="feature-chip"><div class="feature-icon">😊</div><b>{counts["reactions"]}</b><div class="card-text">Reactions</div></div></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><div class="card-title">Total Engagement</div><div class="card-text">Your live room brings interaction into one workspace.</div><div style="height:.7rem"></div><div class="activity"><div class="activity-title">📊 Live polls</div><div class="activity-text">Collect instant audience responses.</div></div><div class="activity"><div class="activity-title">💬 Audience Q&amp;A</div><div class="activity-text">Keep questions organized and visible.</div></div><div class="activity"><div class="activity-title">😊 Reactions</div><div class="activity-text">Let the audience respond naturally.</div></div></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><div class="card-title">Recent Activity</div><div class="card-text">Keep every interaction moving.</div><div class="activity"><div class="activity-title">🟣 Poll created</div><div class="activity-text">Audience can vote instantly.</div></div><div class="activity"><div class="activity-title">🔵 Question received</div><div class="activity-text">Questions stay in one place.</div></div><div class="activity"><div class="activity-title">🟢 Announcement sent</div><div class="activity-text">Reach everyone at once.</div></div><div class="activity"><div class="activity-title">🟠 Reaction added</div><div class="activity-text">See the room response.</div></div></div>', unsafe_allow_html=True)
    with c:
        if st.session_state.get("host_authenticated") and st.session_state.get("session_code"):
            code=st.session_state.session_code
            app_url = os.getenv("STREAMLIT_APP_URL", "") or ""
            qr_data = f"{app_url}?join={code}" if app_url else code
            st.markdown('<div class="qr-card"><div class="card-title">Quick Join</div><div class="card-text">Scan this QR code to join.</div></div>', unsafe_allow_html=True)
            st.image(make_qr(qr_data), width=175)
            st.markdown(f'<div style="text-align:center;font-size:.68rem;color:#55708f;font-weight:800;letter-spacing:.12em;">SESSION CODE · {code}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="qr-card"><div style="font-size:2rem;margin-bottom:.25rem">▦</div><div class="card-title">Quick Join QR</div><div class="card-text">Create a session to generate a scannable QR code for your audience.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-head"><div><div class="section-title">Built for engagement</div><div class="section-caption">Simple tools with a professional live-room experience.</div></div></div>', unsafe_allow_html=True)
    cols=st.columns(4, gap="medium")
    features=[("📊","Polls","Launch questions and collect votes instantly."),("💬","Q&A","Keep audience questions organized."),("📢","Announcements","Send important updates to everyone."),("😊","Reactions","Let participants react with expressive emojis.")]
    for col,(icon,title,text) in zip(cols,features):
        with col: st.markdown(f'<div class="feature-chip"><div class="feature-icon">{icon}</div><div class="card-title">{title}</div><div class="card-text">{text}</div></div>',unsafe_allow_html=True)

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
    if not st.session_state.get("host_authenticated", False): go_to("host_login"); return
    code=st.session_state.session_code; name=st.session_state.session_name; host=st.session_state.host_name
    counts=host_counts()
    host_header("Dashboard", f"Welcome back, {host}. Your live workspace is ready.")
    metrics=[("👥","PARTICIPANTS",counts["participants"],"Audience registered"),("📊","POLLS",counts["polls"],"Interactive polls"),("💬","QUESTIONS",counts["questions"],"Audience questions"),("😊","REACTIONS",counts["reactions"],"Total reactions")]
    cols=st.columns(4,gap="medium")
    for col,(icon,label,value,note) in zip(cols,metrics):
        with col: st.markdown(f'<div class="metric"><div style="font-size:1.05rem">{icon}</div><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-head"><div><div class="section-title">Your live session</div><div class="section-caption">Share the code or QR with your audience.</div></div><div class="live-pill"><span class="live-dot"></span>LIVE SESSION</div></div>',unsafe_allow_html=True)
    left,mid,right=st.columns([1.25,.85,.75],gap="medium")
    with left:
        st.markdown(f'<div class="card"><div class="card-title">{name}</div><div class="card-text">Hosted by {host}. Your room is ready for interaction.</div><div style="height:.8rem"></div><div class="code-box"><div class="code-label">SESSION CODE</div><div class="code-value">{code}</div></div></div>',unsafe_allow_html=True)
    with mid:
        st.markdown('<div class="card"><div class="card-title">Recent Activity</div><div class="activity"><div class="activity-title">📊 Poll activity</div><div class="activity-text">Use Polls to engage the room.</div></div><div class="activity"><div class="activity-title">💬 Q&amp;A</div><div class="activity-text">Review incoming questions.</div></div><div class="activity"><div class="activity-title">😊 Reactions</div><div class="activity-text">See audience sentiment.</div></div></div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="qr-card"><div class="card-title">Quick Join</div><div class="card-text">Scan to join this session.</div></div>',unsafe_allow_html=True)
        st.image(make_qr(code),width=165)
        st.markdown(f'<div style="text-align:center;font-size:.68rem;color:#55708f;font-weight:800;letter-spacing:.12em;">{code}</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-head"><div><div class="section-title">Engagement overview</div><div class="section-caption">Current activity across your live session.</div></div></div>',unsafe_allow_html=True)
    fig=go.Figure(go.Bar(x=["Participants","Polls","Questions","Reactions"],y=[counts["participants"],counts["polls"],counts["questions"],counts["reactions"]],text=[counts["participants"],counts["polls"],counts["questions"],counts["reactions"]],textposition="outside",marker=dict(color=["#4f8cff","#7c4dff","#23b7a4","#ff9f43"])))
    fig.update_layout(height=320,margin=dict(l=20,r=20,t=20,b=20),plot_bgcolor="white",paper_bgcolor="white",showlegend=False,xaxis=dict(showgrid=False),yaxis=dict(showgrid=True,gridcolor="#edf1f7",rangemode="tozero"),font=dict(family="Inter",color="#40527a"))
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.markdown('<div class="section-head"><div><div class="section-title">Quick actions</div><div class="section-caption">Jump directly to the tools you need.</div></div></div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4,gap="small")
    for col,label,page in [(a,"📊 Create Poll","polls"),(b,"👥 Participants","participants"),(c,"💬 Open Q&amp;A","qa"),(d,"📢 Announcement","announcements")]:
        with col:
            if st.button(label,key=f"dash_{page}",use_container_width=True): go_to(page)

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
    if not st.session_state.host_authenticated: go_to("host_login"); return
    code=st.session_state.session_code
    host_header("Reactions","See how the audience is responding in real time.")
    items=[]
    try:
        r=requests.get(f"{BACKEND_URL}/reactions/{code}",timeout=10)
        items=get_list(r.json(),"reactions") if r.status_code==200 else []
        if r.status_code!=200: api_error(r,"Could not load reactions")
    except requests.RequestException as e: st.error(f"Connection error: {e}")
    emoji_map={"Like":"👍","Love":"❤️","Clap":"👏","Interesting":"🤔","Laugh":"😂","Fire":"🔥","Amazing":"😍","Excited":"🚀"}
    if not items: st.info("No reactions yet. Ask your audience to react during the session.")
    else:
        cols=st.columns(4,gap="medium")
        for i,item in enumerate(items):
            raw=str(item.get("reaction","Reaction")); name=raw.replace("👍 ","").replace("❤️ ","").replace("👏 ","").replace("😂 ","").replace("🔥 ","").replace("🚀 ","").strip()
            emoji=next((e for k,e in emoji_map.items() if k.lower() in name.lower()),"😊")
            with cols[i%4]: st.markdown(f'<div class="reaction-card"><div class="reaction-emoji">{emoji}</div><div class="reaction-name">{name.upper()}</div><div class="reaction-count">{int(item.get("count",0))}</div></div>',unsafe_allow_html=True)
    if st.button("Refresh Reactions",key="reactions_refresh_saas"): st.rerun()

# ==================================================
# ANALYTICS
# ==================================================

def analytics_page():
    if not st.session_state.host_authenticated: go_to("host_login"); return
    code=st.session_state.session_code
    host_header("Analytics","Visualize participation and engagement at a glance.")
    counts=host_counts()
    cols=st.columns(4,gap="medium")
    for col,(icon,label,key) in zip(cols,[("👥","PARTICIPANTS","participants"),("📊","POLLS","polls"),("💬","QUESTIONS","questions"),("😊","REACTIONS","reactions")]):
        with col: st.markdown(f'<div class="metric"><div style="font-size:1.05rem">{icon}</div><div class="metric-label">{label}</div><div class="metric-value">{counts[key]}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-head"><div><div class="section-title">Engagement overview</div><div class="section-caption">Current activity across your live session.</div></div></div>',unsafe_allow_html=True)
    fig=go.Figure(go.Bar(x=["Participants","Polls","Questions","Reactions"],y=[counts["participants"],counts["polls"],counts["questions"],counts["reactions"]],text=[counts["participants"],counts["polls"],counts["questions"],counts["reactions"]],textposition="outside",marker=dict(color=["#4f8cff","#7c4dff","#23b7a4","#ff9f43"])))
    fig.update_layout(height=340,margin=dict(l=20,r=20,t=20,b=20),plot_bgcolor="white",paper_bgcolor="white",showlegend=False,xaxis=dict(showgrid=False),yaxis=dict(showgrid=True,gridcolor="#edf1f7",rangemode="tozero"),font=dict(family="Arial",color="#40527a"))
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.markdown('<div class="section-head"><div><div class="section-title">Reaction breakdown</div><div class="section-caption">See which responses are getting the most attention.</div></div></div>',unsafe_allow_html=True)
    try:
        r=requests.get(f"{BACKEND_URL}/reactions/{code}",timeout=10); items=get_list(r.json(),"reactions") if r.status_code==200 else []
        if items:
            rows=[]
            emoji_map={"Like":"👍","Love":"❤️","Clap":"👏","Interesting":"🤔","Laugh":"😂","Fire":"🔥","Amazing":"😍","Excited":"🚀"}
            for x in items:
                name=str(x.get("reaction","Reaction")); rows.append({"Reaction":f'{emoji_map.get(name,"😊")} {name}',"Count":int(x.get("count",0))})
            st.dataframe(rows,use_container_width=True,hide_index=True)
        else: st.info("No reaction data yet.")
    except requests.RequestException: pass

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
    reaction_choices=[("👍","Like"),("❤️","Love"),("👏","Clap"),("😂","Laugh"),("🔥","Fire"),("🚀","Excited")]
    for i,(emoji,label) in enumerate(reaction_choices):
        with cols[i%4]:
            if st.button(f"{emoji} {label}",key=f"joined_reaction_{label.lower()}",use_container_width=True):
                try:
                    r=requests.post(f"{BACKEND_URL}/reactions",json={"session_code":code,"participant_id":pid,"reaction":label},timeout=10)
                    if r.status_code==200: st.success(f"{emoji} {label} sent.")
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
