import streamlit as st
import random

def render():
    st.markdown("""
    <div class="page-wrapper">
      <div class="page-header">
        <div class="page-label">Overview · Real-Time Intelligence</div>
        <div class="page-title">Compliance Risk Dashboard</div>
        <div class="page-subtitle">Global Energy Sector · Threat Matrix Updated 06 Mar 2026</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Metrics ──────────────────────────────────────────────────────────
    st.markdown('<div style="padding: 0 48px;">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("📁", "47", "Active Matters", "↑ 3 this week", "up"),
        ("⚠️", "12", "High-Risk Alerts", "↓ 2 resolved", "down"),
        ("📋", "89%", "Compliance Score", "Sector Average: 72%", "neutral"),
        ("🌍", "23", "Jurisdictions", "6 under review", "neutral"),
    ]
    for col, (icon, val, label, delta, dclass) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <span class="metric-icon">{icon}</span>
              <div class="metric-value">{val}</div>
              <div class="metric-label">{label}</div>
              <div class="metric-delta {dclass}">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Heatmap + Active Alerts ───────────────────────────────────────────────
    col_heat, col_alerts = st.columns([3, 2], gap="large")

    with col_heat:
        st.markdown('<div style="padding: 0 0 0 48px;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⬛ Jurisdiction Risk Heatmap</div>', unsafe_allow_html=True)

        heatmap_data = [
            ("North Sea (UK)",    "Sanctions",      85, "critical"),
            ("Gulf Region (UAE)", "Anti-Bribery",   62, "high"),
            ("West Africa",       "Corruption",     91, "critical"),
            ("Central Asia",      "State Control",  74, "high"),
            ("North America",     "ESG Compliance", 38, "medium"),
            ("Latin America",     "Arbitration",    55, "high"),
            ("SE Asia",           "Licensing",      29, "low"),
            ("EU Bloc",           "GDPR/Antitrust", 44, "medium"),
        ]

        risk_colors = {
            "critical": ("background:#ef535022;border:1px solid #ef535044;color:#ef5350", "CRITICAL"),
            "high":     ("background:#FF980022;border:1px solid #FF980044;color:#FF9800", "HIGH"),
            "medium":   ("background:#FFC10722;border:1px solid #FFC10744;color:#FFC107", "MEDIUM"),
            "low":      ("background:#4CAF5022;border:1px solid #4CAF5044;color:#4CAF50", "LOW"),
        }

        for region, category, score, level in heatmap_data:
            style, label = risk_colors[level]
            col_a, col_b, col_c, col_d = st.columns([3, 2, 2, 1])
            with col_a:
                st.markdown(f'<span style="font-size:13px;color:#E8D5A0;font-weight:500;">{region}</span>', unsafe_allow_html=True)
            with col_b:
                st.markdown(f'<span style="font-size:11px;color:#706050;">{category}</span>', unsafe_allow_html=True)
            with col_c:
                st.progress(score / 100)
            with col_d:
                st.markdown(f'<span class="risk-badge risk-{level}" style="font-size:9px;padding:2px 7px;">{label}</span>', unsafe_allow_html=True)
            st.markdown('<hr style="margin:6px 0;">', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_alerts:
        st.markdown('<div style="padding: 0 48px 0 0;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔔 Active Alerts</div>', unsafe_allow_html=True)
        alerts = [
            ("🔴", "CRITICAL", "SPA clause 14.3 — Force Majeure exposure in Libya concession contract exceeds threshold."),
            ("🟠", "HIGH", "FCPA risk flag: undisclosed third-party agent in Nigeria upstream deal."),
            ("🟡", "MEDIUM", "HKEX IPO disclosure: energy asset valuation methodology inconsistency detected."),
            ("🟠", "HIGH", "UN EITI standard deviation: payment transparency gap in Oman PSA."),
            ("🟢", "LOW", "Arbitration clause review completed — UNCITRAL rules confirmed in LNG offtake."),
        ]
        for emoji, level, text in alerts:
            level_map = {"CRITICAL": "critical", "HIGH": "high", "MEDIUM": "medium", "LOW": "low"}
            lclass = level_map[level]
            st.markdown(f"""
            <div style="padding:12px 14px;background:#13161C;border:1px solid #C9A84C12;
                        border-radius:10px;margin-bottom:8px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <span>{emoji}</span>
                <span class="risk-badge risk-{lclass}" style="font-size:9px;padding:2px 7px;">{level}</span>
              </div>
              <div style="font-size:12px;color:#A09080;line-height:1.5;">{text}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recent Activity ───────────────────────────────────────────────────────
    st.markdown('<div style="padding: 0 48px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Recent Platform Activity</div>', unsafe_allow_html=True)

    activity = [
        ("Contract Analyzer", "SPA — North Sea Block 21 (BP/Shell JV)", "Risk Score: 74 / High", "2h ago", "high"),
        ("Anti-Corruption",   "FCPA Checklist — Nigeria Upstream",        "8/12 items flagged",    "5h ago", "medium"),
        ("Investigation",     "Matter #INV-2026-041 — Oman PSC Review",   "Status: Active",        "1d ago", "neutral"),
        ("Contract Analyzer", "HKEX IPO Prospectus — GreenEnergy Ltd",    "Risk Score: 42 / Low",  "2d ago", "low"),
    ]

    st.markdown("""
    <table class="styled-table">
      <thead>
        <tr>
          <th>Module</th><th>Matter</th><th>Finding</th><th>Time</th><th>Level</th>
        </tr>
      </thead>
      <tbody>
    """, unsafe_allow_html=True)

    for module, matter, finding, time, level in activity:
        st.markdown(f"""
        <tr>
          <td style="color:#C9A84C99;font-size:11px;letter-spacing:0.06em;">{module}</td>
          <td>{matter}</td>
          <td style="color:#9090A0;">{finding}</td>
          <td style="color:#504840;font-size:11px;">{time}</td>
          <td><span class="risk-badge risk-{level}" style="font-size:9px;padding:2px 8px;">{level.upper()}</span></td>
        </tr>
        """, unsafe_allow_html=True)

    st.markdown("</tbody></table>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
