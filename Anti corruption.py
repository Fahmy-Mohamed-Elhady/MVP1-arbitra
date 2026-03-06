import streamlit as st

CHECKLIST = {
    "UN Global Compact / UNCAC Framework": [
        ("Beneficial ownership verified through approved registry (FATF Rec. 24)", True),
        ("Anti-bribery policy formally adopted and published per UNCAC Art. 9", True),
        ("Third-party agents screened against UN Consolidated Sanctions List", True),
        ("Facilitation payments policy: zero-tolerance clause documented", False),
        ("Whistleblower protection mechanism established and operational", False),
        ("Annual compliance training records maintained (all relevant staff)", True),
        ("Gift & hospitality register maintained with ≤ USD 50 threshold", True),
    ],
    "FCPA (U.S. Dept of Justice — Resource Guide)": [
        ("Foreign government official contact log maintained", False),
        ("No unjustified payments to officials via third parties (FCPA §78dd-2)", True),
        ("Books and records accurately reflect all transactions (FCPA §78m)", True),
        ("Adequate procedures documented per DOJ FCPA Pilot Program", False),
        ("Pre-acquisition FCPA due diligence on all M&A targets completed", True),
        ("Anti-corruption representations in all JV/partnership agreements", False),
    ],
    "UK Bribery Act 2010 (SFO Guidance)": [
        ("Section 7 'adequate procedures' defence framework established", True),
        ("Risk assessment conducted for all high-risk jurisdictions", True),
        ("Associated persons (agents, JV partners) contractually bound by UKBA", False),
        ("Top-level commitment anti-bribery statement issued by Board", True),
        ("Enhanced due diligence performed for PEP-linked counterparties", False),
        ("Monitoring and review cycle established (minimum annual)", True),
    ],
    "University of Pennsylvania Compliance Framework": [
        ("Compliance risk matrix updated within last 12 months", True),
        ("Internal audit scope includes anti-corruption testing", True),
        ("Segregation of duties enforced in financial approvals", True),
        ("Compliance officer holds independent reporting line to Board", False),
        ("Speak-up culture metrics tracked and disclosed", False),
        ("External compliance counsel engaged for high-risk markets", True),
    ],
}


def render():
    st.markdown("""
    <div class="page-wrapper">
      <div class="page-header">
        <div class="page-label">UN · UPenn · DOJ · SFO Frameworks</div>
        <div class="page-title">Anti-Corruption Compliance Checklist</div>
        <div class="page-subtitle">
          Based on UNCAC, FCPA Resource Guide, UK Bribery Act 2010 &
          University of Pennsylvania Compliance Architecture
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 48px;">', unsafe_allow_html=True)

    # ── Header Controls ────────────────────────────────────────────────────────
    col_sel, col_info = st.columns([2, 1], gap="large")
    with col_sel:
        entity_name = st.text_input("Entity / Matter Name", placeholder="e.g. GreenEnergy Ltd — Nigeria Upstream JV")
        jurisdiction = st.selectbox("Jurisdiction", [
            "Nigeria", "Libya", "Kazakhstan", "UAE", "Iraq",
            "Angola", "Mozambique", "Brazil", "Egypt", "Global / Multi-jurisdictional"
        ])
    with col_info:
        risk_profile = st.selectbox("Corruption Risk Profile", [
            "🔴 Very High", "🟠 High", "🟡 Medium", "🟢 Low"
        ])
        industry = st.selectbox("Industry Segment", [
            "Upstream E&P", "Midstream / Pipeline", "LNG / FLNG",
            "Refining & Downstream", "Renewables / Energy Transition",
            "Energy Finance / M&A"
        ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── State init ────────────────────────────────────────────────────────────
    if "ac_state" not in st.session_state:
        st.session_state["ac_state"] = {}

    total_items  = sum(len(v) for v in CHECKLIST.values())
    checked_items = sum(1 for v in st.session_state["ac_state"].values() if v)
    score_pct = int((checked_items / total_items) * 100) if total_items else 0

    # ── Summary Bar ───────────────────────────────────────────────────────────
    if score_pct >= 80:   bar_col, bar_label = "#4CAF50", "COMPLIANT"
    elif score_pct >= 55: bar_col, bar_label = "#FFC107", "PARTIAL COMPLIANCE"
    else:                 bar_col, bar_label = "#ef5350", "NON-COMPLIANT"

    st.markdown(f"""
    <div class="glass-panel" style="margin-bottom:28px;">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
        <div>
          <div style="font-size:10px;color:#C9A84C66;letter-spacing:0.15em;
                      text-transform:uppercase;margin-bottom:6px;">COMPLIANCE COMPLETION</div>
          <div style="font-family:'Syne',sans-serif;font-size:42px;font-weight:800;
                      color:{bar_col};line-height:1;">{score_pct}%</div>
          <div style="font-size:12px;color:#706050;margin-top:4px;">
            {checked_items} of {total_items} controls verified · <strong style="color:{bar_col};">{bar_label}</strong>
          </div>
        </div>
        <div style="text-align:right;font-size:12px;color:#706050;">
          <div><strong style="color:#C9A84C99;">Entity:</strong> {entity_name or '—'}</div>
          <div><strong style="color:#C9A84C99;">Jurisdiction:</strong> {jurisdiction}</div>
          <div><strong style="color:#C9A84C99;">Risk:</strong> {risk_profile}</div>
        </div>
      </div>
      <div style="margin-top:16px;">
    """, unsafe_allow_html=True)
    st.progress(score_pct / 100)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Checklist Sections ─────────────────────────────────────────────────────
    for section_name, items in CHECKLIST.items():
        st.markdown(f'<div class="section-title">📋 {section_name}</div>', unsafe_allow_html=True)

        section_checked = 0
        for i, (item_text, default) in enumerate(items):
            key = f"ac_{section_name}_{i}"
            if key not in st.session_state["ac_state"]:
                st.session_state["ac_state"][key] = default

            checked = st.session_state["ac_state"][key]
            check_icon = "✓" if checked else "·"
            check_class = "done" if checked else ""
            section_checked += 1 if checked else 0

            col_cb, col_text = st.columns([0.06, 0.94])
            with col_cb:
                new_val = st.checkbox("", value=checked, key=f"cb_{key}",
                                      label_visibility="collapsed")
                st.session_state["ac_state"][key] = new_val
            with col_text:
                status_color = "#4CAF50" if new_val else "#706050"
                st.markdown(f"""
                <div style="padding:10px 14px;border-radius:8px;
                            background:{'#4CAF5008' if new_val else '#13161C'};
                            border:1px solid {'#4CAF5022' if new_val else '#C9A84C0A'};
                            margin-bottom:6px;">
                  <div style="font-size:13px;color:{'#B8D4B0' if new_val else '#9090A0'};
                               text-decoration:{'line-through' if new_val else 'none'};
                               opacity:{'0.65' if new_val else '1'};line-height:1.5;">
                    {item_text}
                  </div>
                </div>
                """, unsafe_allow_html=True)

        completed_pct = int((section_checked / len(items)) * 100)
        st.markdown(f"""
        <div style="font-size:10px;color:#504840;letter-spacing:0.08em;
                    margin-bottom:20px;text-align:right;">
          SECTION COMPLETION: {completed_pct}% ({section_checked}/{len(items)})
        </div>
        """, unsafe_allow_html=True)

    # ── Export Notice ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥  GENERATE COMPLIANCE REPORT", use_container_width=True):
        st.success(
            f"✅ Compliance snapshot prepared for **{entity_name or 'entity'}** | "
            f"Score: {score_pct}% | Status: {bar_label}. "
            "In production, a PDF report with digital signature would be generated here."
        )

    st.markdown("</div>", unsafe_allow_html=True)
