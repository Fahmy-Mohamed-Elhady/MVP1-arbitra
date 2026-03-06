import streamlit as st
import importlib

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Arbitra AI | Legal-Tech Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Google Fonts + Global CSS ─────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap" rel="stylesheet">
<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: #0E1117 !important;
    color: #E8E0D0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stDeployButton"],
[data-testid="stDecoration"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0E1117; }
::-webkit-scrollbar-thumb { background: #C9A84C55; border-radius: 2px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0C10 0%, #0E1117 60%, #0A0C10 100%) !important;
    border-right: 1px solid #C9A84C22 !important;
    width: 288px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* ── Sidebar logo zone ── */
.sidebar-logo-zone {
    padding: 28px 24px 20px;
    border-bottom: 1px solid #C9A84C18;
    text-align: center;
}
.sidebar-wordmark {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #C9A84C;
    text-transform: uppercase;
}
.sidebar-tagline {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px;
    font-weight: 300;
    letter-spacing: 0.18em;
    color: #C9A84C66;
    text-transform: uppercase;
    margin-top: 3px;
}

/* ── Profile Card ── */
.profile-card {
    margin: 20px 16px;
    padding: 16px;
    background: linear-gradient(135deg, #C9A84C0A 0%, #C9A84C04 100%);
    border: 1px solid #C9A84C28;
    border-radius: 10px;
    position: relative;
    overflow: hidden;
}
.profile-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #C9A84C, transparent);
}
.profile-avatar {
    width: 52px; height: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, #C9A84C 0%, #8B6914 100%);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 18px; font-weight: 800;
    color: #0E1117;
    margin: 0 auto 12px;
    border: 2px solid #C9A84C44;
    box-shadow: 0 0 20px #C9A84C22;
}
.profile-name {
    font-family: 'Syne', sans-serif;
    font-size: 13px; font-weight: 700;
    color: #F0E8D5;
    text-align: center;
    letter-spacing: 0.02em;
}
.profile-title {
    font-size: 10px; font-weight: 300;
    color: #C9A84C99;
    text-align: center;
    margin-top: 4px;
    letter-spacing: 0.06em;
}
.profile-uni {
    font-size: 9px; font-weight: 400;
    color: #C9A84C55;
    text-align: center;
    margin-top: 3px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.cert-badge {
    display: inline-block;
    padding: 2px 8px;
    background: #C9A84C14;
    border: 1px solid #C9A84C33;
    border-radius: 20px;
    font-size: 8.5px;
    font-weight: 500;
    color: #C9A84Caa;
    margin: 3px 2px 0;
    letter-spacing: 0.04em;
}
.cert-row {
    text-align: center;
    margin-top: 8px;
}

/* ── Nav Section Label ── */
.nav-section-label {
    font-size: 9px; font-weight: 600;
    color: #C9A84C55;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    padding: 16px 24px 8px;
}

/* ── Nav Button ── */
.nav-btn {
    display: flex; align-items: center; gap: 12px;
    width: calc(100% - 32px);
    margin: 3px 16px;
    padding: 11px 14px;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
    color: #A09080;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 400;
    letter-spacing: 0.02em;
    position: relative;
    overflow: hidden;
    text-decoration: none;
}
.nav-btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, #C9A84C08, transparent);
    opacity: 0;
    transition: opacity 0.25s;
}
.nav-btn:hover::before { opacity: 1; }
.nav-btn:hover {
    border-color: #C9A84C33;
    color: #E8D5A0;
    background: #C9A84C06;
    backdrop-filter: blur(10px);
    transform: translateX(2px);
    box-shadow: 0 4px 20px #C9A84C0A, inset 0 1px 0 #C9A84C18;
}
.nav-btn.active {
    background: linear-gradient(90deg, #C9A84C14, #C9A84C06);
    border-color: #C9A84C44;
    color: #C9A84C;
    font-weight: 500;
    box-shadow: 0 4px 24px #C9A84C14, inset 0 1px 0 #C9A84C28;
}
.nav-btn.active::after {
    content: '';
    position: absolute;
    left: 0; top: 20%; bottom: 20%;
    width: 2px;
    background: #C9A84C;
    border-radius: 0 2px 2px 0;
    box-shadow: 0 0 8px #C9A84C;
}
.nav-icon { font-size: 15px; flex-shrink: 0; }

/* ── Main Content ── */
[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
}
.page-wrapper {
    padding: 40px 48px;
    min-height: 100vh;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 36px;
    padding-bottom: 24px;
    border-bottom: 1px solid #C9A84C18;
    position: relative;
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 60px; height: 1px;
    background: #C9A84C;
    box-shadow: 0 0 12px #C9A84C88;
}
.page-label {
    font-size: 10px; font-weight: 600;
    color: #C9A84C;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 32px; font-weight: 800;
    color: #F0E8D5;
    letter-spacing: -0.01em;
    line-height: 1.1;
}
.page-subtitle {
    font-size: 14px; font-weight: 300;
    color: #706050;
    margin-top: 8px;
    letter-spacing: 0.02em;
}

/* ── Metric Card ── */
.metric-card {
    background: linear-gradient(135deg, #13161C 0%, #0E1117 100%);
    border: 1px solid #C9A84C18;
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}
.metric-card:hover {
    border-color: #C9A84C33;
    box-shadow: 0 8px 32px #C9A84C0A;
    transform: translateY(-2px);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C9A84C44, transparent);
}
.metric-icon {
    font-size: 22px;
    margin-bottom: 12px;
    display: block;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px; font-weight: 800;
    color: #C9A84C;
    line-height: 1;
}
.metric-label {
    font-size: 11px; font-weight: 400;
    color: #706050;
    margin-top: 6px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.metric-delta {
    font-size: 11px;
    font-weight: 500;
    margin-top: 4px;
}
.metric-delta.up { color: #4CAF50; }
.metric-delta.down { color: #ef5350; }
.metric-delta.neutral { color: #C9A84C; }

/* ── Section Title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px; font-weight: 700;
    color: #E8D5A0;
    letter-spacing: 0.04em;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #C9A84C18, transparent);
}

/* ── Risk Badge ── */
.risk-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.risk-critical { background: #ef535018; border: 1px solid #ef535044; color: #ef5350; }
.risk-high     { background: #FF980018; border: 1px solid #FF980044; color: #FF9800; }
.risk-medium   { background: #FFC10718; border: 1px solid #FFC10744; color: #FFC107; }
.risk-low      { background: #4CAF5018; border: 1px solid #4CAF5044; color: #4CAF50; }

/* ── Glass Panel ── */
.glass-panel {
    background: linear-gradient(135deg, #13161C88 0%, #0E111788 100%);
    border: 1px solid #C9A84C18;
    border-radius: 12px;
    padding: 24px;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}

/* ── Table styles ── */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
.styled-table th {
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    font-weight: 600;
    color: #C9A84C;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 10px 14px;
    border-bottom: 1px solid #C9A84C22;
    text-align: left;
}
.styled-table td {
    padding: 12px 14px;
    border-bottom: 1px solid #C9A84C0A;
    color: #B0A090;
    vertical-align: middle;
}
.styled-table tr:hover td {
    background: #C9A84C05;
    color: #E8D5A0;
}

/* ── Input ── */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
    background: #13161C !important;
    border: 1px solid #C9A84C22 !important;
    color: #E8E0D0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #C9A84C66 !important;
    box-shadow: 0 0 0 3px #C9A84C0A !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #C9A84C, #8B6914) !important;
    color: #0E1117 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
    padding: 10px 24px !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 16px #C9A84C22 !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px #C9A84C44 !important;
}

/* ── Progress Bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #C9A84C, #FFC107) !important;
}

/* ── Divider ── */
hr { border-color: #C9A84C18 !important; }

/* ── Auth screen ── */
.auth-screen {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(ellipse at 50% 0%, #C9A84C0A 0%, transparent 60%), #0E1117;
}
.auth-box {
    width: 400px;
    padding: 48px;
    background: linear-gradient(135deg, #13161C 0%, #0E1117 100%);
    border: 1px solid #C9A84C28;
    border-radius: 16px;
    box-shadow: 0 24px 80px #00000066, 0 0 0 1px #C9A84C0A;
    position: relative;
    overflow: hidden;
}
.auth-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #C9A84C, transparent);
}
.auth-logo {
    text-align: center;
    margin-bottom: 36px;
}
.auth-wordmark {
    font-family: 'Syne', sans-serif;
    font-size: 30px; font-weight: 800;
    color: #C9A84C;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.auth-sub {
    font-size: 11px; font-weight: 300;
    color: #C9A84C66;
    letter-spacing: 0.2em;
    margin-top: 4px;
}

/* ── Heatmap cell ── */
.heatmap-cell {
    padding: 14px 10px;
    border-radius: 8px;
    text-align: center;
    font-size: 11px; font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.04em;
    transition: transform 0.2s;
    cursor: default;
}
.heatmap-cell:hover { transform: scale(1.04); }

/* ── Checklist item ── */
.checklist-item {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 14px 18px;
    border-radius: 10px;
    border: 1px solid #C9A84C12;
    margin-bottom: 8px;
    background: #13161C;
    transition: all 0.2s;
}
.checklist-item:hover {
    border-color: #C9A84C28;
    background: #13161C;
    box-shadow: 0 4px 16px #C9A84C06;
}
.checklist-check {
    width: 20px; height: 20px; flex-shrink: 0;
    border-radius: 4px;
    background: #C9A84C18;
    border: 1px solid #C9A84C44;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px;
    color: #C9A84C;
    margin-top: 2px;
}
.checklist-check.done { background: #4CAF5022; border-color: #4CAF5066; color: #4CAF50; }
.checklist-text { font-size: 13px; color: #B0A090; flex: 1; line-height: 1.5; }
.checklist-source {
    font-size: 10px; color: #C9A84C66;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 3px;
}

/* ── Timeline ── */
.timeline-item {
    display: flex; gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid #C9A84C0A;
    position: relative;
}
.timeline-dot {
    width: 10px; height: 10px; flex-shrink: 0;
    border-radius: 50%;
    background: #C9A84C;
    box-shadow: 0 0 8px #C9A84C88;
    margin-top: 5px;
}
.timeline-dot.open { background: #FF9800; box-shadow: 0 0 8px #FF980088; }
.timeline-dot.closed { background: #4CAF50; box-shadow: 0 0 8px #4CAF5088; }
.timeline-content { flex: 1; }
.timeline-title { font-size: 13px; font-weight: 500; color: #E8D5A0; }
.timeline-meta { font-size: 11px; color: #706050; margin-top: 4px; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #13161C !important;
    border: 1px solid #C9A84C18 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: #C9A84C !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Auth Gate ─────────────────────────────────────────────────────────────────
def auth_gate():
    st.markdown("""
    <div class="auth-screen">
      <div class="auth-box">
        <div class="auth-logo">
          <div class="auth-wordmark">⚖ Arbitra AI</div>
          <div class="auth-sub">Global Energy Legal Intelligence</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; font-family:'Syne',sans-serif;
                    font-size:26px; font-weight:800; color:#C9A84C;
                    letter-spacing:0.1em; text-transform:uppercase;
                    padding-top:40px; margin-bottom:4px;">
          ⚖ Arbitra AI
        </div>
        <div style="text-align:center; font-size:11px; font-weight:300;
                    color:#C9A84C66; letter-spacing:0.2em; margin-bottom:36px;">
          Global Energy Legal Intelligence
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Access ID", placeholder="Enter credentials", key="auth_user")
        password = st.text_input("Passphrase", type="password", placeholder="••••••••••", key="auth_pass")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶  AUTHENTICATE", use_container_width=True):
            if username == "Admin" and password == "arbitra2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("⛔ Invalid credentials. Access denied.")
        st.markdown("""
        <div style="text-align:center; font-size:10px; color:#C9A84C33;
                    margin-top:20px; letter-spacing:0.12em;">
          SECURED BY ARBITRA AI · AES-256 ENCRYPTED
        </div>
        """, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
PAGES = {
    "Dashboard":             ("📊", "pages.dashboard"),
    "Contract Analyzer":     ("📄", "pages.contract_analyzer"),
    "Anti-Corruption":       ("🛡️", "pages.anti_corruption"),
    "Investigation Tracker": ("🔍", "pages.investigation_tracker"),
}

def render_sidebar():
    with st.sidebar:
        # Brand
        st.markdown("""
        <div class="sidebar-logo-zone">
          <div style="font-size:26px; margin-bottom:6px;">⚖</div>
          <div class="sidebar-wordmark">Arbitra AI</div>
          <div class="sidebar-tagline">Energy Legal Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

        # Profile Card
        st.markdown("""
        <div class="profile-card">
          <div class="profile-avatar">FE</div>
          <div class="profile-name">Fahmy Mohamed Elhady</div>
          <div class="profile-title">Lead Legal Investigator & Arbitration Counsel</div>
          <div class="profile-uni">Ain Shams University · Cairo</div>
          <div class="cert-row">
            <span class="cert-badge">UK Energy · White &amp; Case</span>
            <span class="cert-badge">Corp Law · Baker McKenzie</span>
            <span class="cert-badge">Compliance · UPenn &amp; UN</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Nav
        st.markdown('<div class="nav-section-label">Navigation</div>', unsafe_allow_html=True)

        if "page" not in st.session_state:
            st.session_state["page"] = "Dashboard"

        for label, (icon, _) in PAGES.items():
            active_class = "active" if st.session_state["page"] == label else ""
            if st.button(f"{icon}  {label}", key=f"nav_{label}",
                         use_container_width=True):
                st.session_state["page"] = label
                st.rerun()

        # Status Bar
        st.markdown("""
        <div style="position:absolute; bottom:0; left:0; right:0;
                    padding:14px 20px; border-top:1px solid #C9A84C18;">
          <div style="display:flex; align-items:center; gap:8px;">
            <div style="width:7px;height:7px;border-radius:50%;
                        background:#4CAF50;box-shadow:0 0 6px #4CAF50;"></div>
            <span style="font-size:10px;color:#706050;letter-spacing:0.1em;">
              SYSTEMS OPERATIONAL
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Main Router ───────────────────────────────────────────────────────────────
def main():
    if not st.session_state.get("authenticated"):
        auth_gate()
        return

    render_sidebar()

    current_page = st.session_state.get("page", "Dashboard")
    _, module_path = PAGES[current_page]

    try:
        module = importlib.import_module(module_path)
        importlib.reload(module)
        module.render()
    except Exception as e:
        st.error(f"Module load error: {e}")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
