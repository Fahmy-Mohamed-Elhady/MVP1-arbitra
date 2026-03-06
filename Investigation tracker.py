import streamlit as st
from datetime import date, datetime

SAMPLE_MATTERS = [
    {
        "id": "INV-2026-041",
        "title": "Oman PSC Payment Transparency Review",
        "type": "FCPA / EITI Compliance",
        "jurisdiction": "Oman",
        "status": "Active",
        "risk": "high",
        "opened": "12 Jan 2026",
        "lead": "Fahmy Mohamed Elhady",
        "stage": "Document Review",
        "notes": "Third-party agent payments in dispute. UN EITI standard gap identified in annual report filings."
    },
    {
        "id": "INV-2026-029",
        "title": "Nigeria Upstream JV — Agent Due Diligence",
        "type": "UKBA / FCPA Investigation",
        "jurisdiction": "Nigeria",
        "status": "Active",
        "risk": "critical",
        "opened": "3 Dec 2025",
        "lead": "Fahmy Mohamed Elhady",
        "stage": "Witness Interviews",
        "notes": "Undisclosed third-party intermediary identified in upstream procurement chain. SFO watch list cross-referenced."
    },
    {
        "id": "INV-2026-017",
        "title": "Libya Concession — Force Majeure Dispute",
        "type": "Contract Arbitration (ICC)",
        "jurisdiction": "Libya",
        "status": "Active",
        "risk": "critical",
        "opened": "8 Oct 2025",
        "lead": "Fahmy Mohamed Elhady",
        "stage": "Expert Witness Preparation",
        "notes": "Force majeure event declared by NOC. Claimant alleges anticipatory breach. ICC Emergency Arbitrator engaged."
    },
    {
        "id": "INV-2025-098",
        "title": "HKEX IPO — GreenEnergy Ltd Disclosure Review",
        "type": "Securities Compliance (HKEX)",
        "jurisdiction": "Hong Kong",
        "status": "Closed",
        "risk": "low",
        "opened": "2 Aug 2025",
        "lead": "Fahmy Mohamed Elhady",
        "stage": "Completed",
        "notes": "All HKEX Main Board Rule 8 and 14A requirements satisfied. Listing approved Nov 2025."
    },
    {
        "id": "INV-2025-071",
        "title": "Kazakhstan Pipeline — Stabilization Clause Analysis",
        "type": "Investment Treaty / BIT",
        "jurisdiction": "Kazakhstan",
        "status": "Closed",
        "risk": "medium",
        "opened": "15 Jun 2025",
        "lead": "Fahmy Mohamed Elhady",
        "stage": "Completed",
        "notes": "Hybrid stabilization clause successfully renegotiated. Investment treaty protection under Kazakhstan-UK BIT confirmed."
    },
]

STAGES = [
    "Intake & Triage",
    "Document Collection",
    "Document Review",
    "Witness Interviews",
    "Expert Witness Preparation",
    "Arbitral Proceedings",
    "Settlement Negotiations",
    "Completed",
]

RISK_COLORS = {
    "critical": "#ef5350",
    "high":     "#FF9800",
    "medium":   "#FFC107",
    "low":      "#4CAF50",
}


def render():
    st.markdown("""
    <div class="page-wrapper">
      <div class="page-header">
        <div class="page-label">Matter Management · Internal Investigations</div>
        <div class="page-title">Investigation Tracker</div>
        <div class="page-subtitle">Corporate Investigations · Arbitration Proceedings · Regulatory Inquiries</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 48px;">', unsafe_allow_html=True)

    # ── Stats row ─────────────────────────────────────────────────────────────
    active   = [m for m in SAMPLE_MATTERS if m["status"] == "Active"]
    closed   = [m for m in SAMPLE_MATTERS if m["status"] == "Closed"]
    critical = [m for m in SAMPLE_MATTERS if m["risk"] == "critical"]

    c1, c2, c3, c4 = st.columns(4)
    for col, (icon, val, label, delta, dc) in zip([c1, c2, c3, c4], [
        ("🔍", str(len(SAMPLE_MATTERS)), "Total Matters", "2 opened this month", "neutral"),
        ("🔴", str(len(active)),          "Active",        f"{len(critical)} critical", "down"),
        ("✅", str(len(closed)),           "Closed",        "YTD 2025–26", "up"),
        ("⚡", str(len(critical)),          "Critical Risk", "Requires immediate action", "down"),
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <span class="metric-icon">{icon}</span>
              <div class="metric-value">{val}</div>
              <div class="metric-label">{label}</div>
              <div class="metric-delta {dc}">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filter Bar ────────────────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_status = st.selectbox("Filter by Status", ["All", "Active", "Closed"])
    with col_f2:
        filter_risk = st.selectbox("Filter by Risk", ["All", "critical", "high", "medium", "low"])
    with col_f3:
        filter_jur = st.selectbox("Filter by Jurisdiction",
                                  ["All"] + sorted(set(m["jurisdiction"] for m in SAMPLE_MATTERS)))

    matters = SAMPLE_MATTERS
    if filter_status != "All":
        matters = [m for m in matters if m["status"] == filter_status]
    if filter_risk != "All":
        matters = [m for m in matters if m["risk"] == filter_risk]
    if filter_jur != "All":
        matters = [m for m in matters if m["jurisdiction"] == filter_jur]

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📁 Matter Register ({len(matters)} result{"s" if len(matters)!=1 else ""})</div>', unsafe_allow_html=True)

    # ── Matter Cards ──────────────────────────────────────────────────────────
    for m in matters:
        risk_col = RISK_COLORS[m["risk"]]
        status_col = "#4CAF50" if m["status"] == "Closed" else "#FF9800"
        stage_idx  = STAGES.index(m["stage"]) if m["stage"] in STAGES else 0
        stage_pct  = int(((stage_idx + 1) / len(STAGES)) * 100)

        with st.expander(f"  {m['id']}  ·  {m['title']}", expanded=(m["status"] == "Active")):
            col_a, col_b, col_c = st.columns([2, 2, 1])

            with col_a:
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                  <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.15em;
                               text-transform:uppercase;margin-bottom:4px;">Matter Type</div>
                  <div style="font-size:13px;color:#E8D5A0;">{m['type']}</div>
                </div>
                <div style="margin-bottom:12px;">
                  <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.15em;
                               text-transform:uppercase;margin-bottom:4px;">Jurisdiction</div>
                  <div style="font-size:13px;color:#E8D5A0;">🌍 {m['jurisdiction']}</div>
                </div>
                <div>
                  <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.15em;
                               text-transform:uppercase;margin-bottom:4px;">Lead Investigator</div>
                  <div style="font-size:13px;color:#C9A84C;">{m['lead']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                  <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.15em;
                               text-transform:uppercase;margin-bottom:4px;">Opened</div>
                  <div style="font-size:13px;color:#E8D5A0;">📅 {m['opened']}</div>
                </div>
                <div style="margin-bottom:12px;">
                  <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.15em;
                               text-transform:uppercase;margin-bottom:4px;">Current Stage</div>
                  <div style="font-size:13px;color:#E8D5A0;">⚙ {m['stage']}</div>
                </div>
                <div>
                  <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.15em;
                               text-transform:uppercase;margin-bottom:8px;">
                    PROGRESS — {stage_pct}%
                  </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(stage_pct / 100)

            with col_c:
                st.markdown(f"""
                <div style="text-align:center;padding:16px 0;">
                  <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.12em;
                               text-transform:uppercase;margin-bottom:8px;">STATUS</div>
                  <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;
                               color:{status_col};padding:8px 12px;
                               background:{status_col}18;border:1px solid {status_col}44;
                               border-radius:8px;margin-bottom:12px;">
                    {m['status'].upper()}
                  </div>
                  <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.12em;
                               text-transform:uppercase;margin-bottom:8px;">RISK LEVEL</div>
                  <span class="risk-badge risk-{m['risk']}">{m['risk'].upper()}</span>
                </div>
                """, unsafe_allow_html=True)

            # Notes
            st.markdown(f"""
            <div style="margin-top:14px;padding:14px 16px;background:#0E1117;
                        border:1px solid #C9A84C0A;border-radius:8px;
                        border-left:2px solid {risk_col}44;">
              <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.1em;
                           text-transform:uppercase;margin-bottom:6px;">CASE NOTES</div>
              <div style="font-size:12px;color:#9090A0;line-height:1.6;">{m['notes']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Stage timeline
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:10px;color:#C9A84C66;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px;">INVESTIGATION PIPELINE</div>', unsafe_allow_html=True)
            cols_stages = st.columns(len(STAGES))
            for si, (sc, stage_name) in enumerate(zip(cols_stages, STAGES)):
                if si <= stage_idx:
                    dot_style = f"background:#C9A84C;box-shadow:0 0 8px #C9A84C66;"
                    text_style = "color:#C9A84C;font-weight:600;"
                else:
                    dot_style = "background:#2A2820;border:1px solid #C9A84C22;"
                    text_style = "color:#404040;"
                with sc:
                    st.markdown(f"""
                    <div style="text-align:center;">
                      <div style="width:10px;height:10px;border-radius:50%;
                                  {dot_style}margin:0 auto 5px;"></div>
                      <div style="font-size:8.5px;{text_style}line-height:1.3;">
                        {stage_name}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── New Matter Form ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">➕ Open New Matter</div>', unsafe_allow_html=True)

    with st.expander("New Investigation / Matter"):
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            new_title = st.text_input("Matter Title", key="new_title")
            new_type  = st.selectbox("Matter Type", [
                "FCPA / Anti-Corruption Investigation",
                "UKBA / SFO Referral",
                "ICC / ICSID Arbitration",
                "HKEX Securities Compliance",
                "Contract Dispute",
                "Internal Compliance Review",
            ], key="new_type")
        with col_n2:
            new_jur   = st.text_input("Jurisdiction", key="new_jur")
            new_risk  = st.selectbox("Initial Risk Assessment",
                                     ["critical", "high", "medium", "low"], key="new_risk")

        new_notes = st.text_area("Initial Notes", height=100, key="new_notes")

        if st.button("📁  OPEN MATTER", use_container_width=True):
            if new_title:
                st.success(f"✅ Matter opened: **{new_title}** | Risk: {new_risk.upper()} | Jurisdiction: {new_jur or 'TBD'}")
            else:
                st.warning("Please provide a matter title.")

    st.markdown("</div>", unsafe_allow_html=True)
