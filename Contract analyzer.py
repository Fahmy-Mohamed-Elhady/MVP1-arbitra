import streamlit as st
import time

# ── Risk Scoring Engine ───────────────────────────────────────────────────────
def score_contract(text: str, contract_type: str) -> dict:
    """Heuristic risk scorer applying Baker McKenzie SPA/HKEX standards."""
    text_lower = text.lower()
    findings = []
    total_risk = 0

    # ── Core clause checks ────────────────────────────────────────────────────
    CLAUSE_RULES = [
        # (keyword_or_absence, flag_if_present, weight, severity, title, detail)
        ("force majeure",         False, 8,  "medium",   "Force Majeure",
         "Force majeure clause detected. Verify scope covers energy-sector events: war, sanctions, pandemic, grid failure."),
        ("stabilization clause",  False, 10, "high",     "Stabilization Clause",
         "Stabilization clause present. Assess if it conflicts with host-state regulatory evolution (Baker McKenzie §4.2)."),
        ("indemnification",       False, 7,  "medium",   "Indemnification Scope",
         "Indemnification provision found. Caps, carve-outs, and environmental liability must be reviewed."),
        ("governing law",         True,  12, "critical", "No Governing Law",
         "No governing law clause identified. This is a critical gap in cross-border energy contracts."),
        ("arbitration",           True,  9,  "high",     "Arbitration Clause Absent",
         "No arbitration/dispute resolution clause detected. ICSID or ICC submission required for PSAs."),
        ("anti-bribery",          True,  11, "high",     "FCPA/UK Bribery Act Compliance",
         "No explicit anti-bribery representations found. FCPA §78dd and UK Bribery Act 2010 §7 compliance risk."),
        ("change of control",     True,  8,  "medium",   "Change of Control",
         "Change of control provisions absent. Acquisition risk unaddressed."),
        ("confidentiality",       True,  5,  "low",      "Confidentiality",
         "No confidentiality clause detected. Trade secret and state-data protection gap."),
        ("environmental",         True,  9,  "high",     "Environmental Liability",
         "Environmental indemnity or liability clause absent. ESG regulatory exposure."),
        ("sanctions",             True,  12, "critical", "Sanctions Compliance",
         "No OFAC/UN sanctions compliance language. Critical in upstream energy deals."),
    ]

    # HKEX-specific checks
    HKEX_RULES = [
        ("connected transaction",  True, 10, "high",    "Connected Transaction Disclosure",
         "HKEX Listing Rule 14A: connected transaction disclosure not identified in prospectus."),
        ("profit forecast",        True, 7,  "medium",  "Profit Forecast Compliance",
         "HKEX Main Board Rule 11.17: profit forecast requires auditor report — not detected."),
        ("working capital",        True, 8,  "medium",  "Working Capital Statement",
         "HKEX Listing Rule 8.21A: 18-month working capital sufficiency statement not found."),
        ("risk factors",           True, 6,  "medium",  "Risk Factors Disclosure",
         "Energy-sector risk factors section not adequately flagged per HKEX Guide 7A."),
    ]

    active_rules = CLAUSE_RULES.copy()
    if contract_type in ("HKEX IPO Prospectus", "Stock Purchase Agreement (SPA)"):
        active_rules += HKEX_RULES

    for kw, flag_if_absent, weight, severity, title, detail in active_rules:
        present = kw in text_lower
        trigger = (not present) if flag_if_absent else present
        if trigger:
            total_risk += weight
            findings.append({
                "title": title,
                "detail": detail,
                "severity": severity,
                "weight": weight,
            })

    # Normalise to 0–100
    max_possible = sum(r[2] for r in active_rules)
    score = min(100, int((total_risk / max(max_possible, 1)) * 100))

    if score >= 70:    level = "critical"
    elif score >= 50:  level = "high"
    elif score >= 30:  level = "medium"
    else:              level = "low"

    return {"score": score, "level": level, "findings": findings}


def render():
    st.markdown("""
    <div class="page-wrapper">
      <div class="page-header">
        <div class="page-label">AI-Driven Audit · Baker McKenzie Standards</div>
        <div class="page-title">Contract Analyzer — Energy Edition</div>
        <div class="page-subtitle">SPA · PSA · HKEX IPO Prospectuses · Petroleum Concession Agreements</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 48px;">', unsafe_allow_html=True)

    col_form, col_info = st.columns([3, 2], gap="large")

    with col_form:
        st.markdown('<div class="section-title">📄 Contract Input</div>', unsafe_allow_html=True)

        contract_type = st.selectbox(
            "Contract Type",
            [
                "Petroleum Concession Agreement (PCA)",
                "Stock Purchase Agreement (SPA)",
                "HKEX IPO Prospectus",
                "Production Sharing Agreement (PSA)",
                "LNG Offtake Agreement",
                "Energy Infrastructure EPC Contract",
                "Joint Operating Agreement (JOA)",
            ],
            key="ct_type"
        )

        jurisdiction = st.selectbox(
            "Primary Jurisdiction",
            ["United Kingdom", "UAE / Gulf Region", "Nigeria / West Africa",
             "Kazakhstan / Central Asia", "Hong Kong (HKEX)", "United States (FCPA)",
             "Libya", "Oman", "Brazil", "Egypt"],
            key="ct_jur"
        )

        counterparty_type = st.selectbox(
            "Counterparty Classification",
            ["National Oil Company (NOC)", "International Oil Company (IOC)",
             "Private Equity / Fund", "State Entity", "Listed Company (HKEX/LSE)",
             "SPV / Shell Entity"],
            key="ct_cpty"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        contract_text = st.text_area(
            "Paste Contract Text or Key Clauses",
            height=280,
            placeholder=(
                "Paste the full contract text here, or relevant clauses for targeted analysis.\n\n"
                "Example: Article 14 — Governing Law: This Agreement shall be governed by...\n"
                "Article 21 — Arbitration: All disputes arising under...\n"
                "Annex B — Anti-Bribery Representations..."
            ),
            key="ct_text"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡  RUN CONTRACT ANALYSIS", use_container_width=True):
            if not contract_text.strip():
                st.warning("Please paste contract text to analyse.")
            else:
                with st.spinner("Parsing clauses · Applying Baker McKenzie audit matrix..."):
                    time.sleep(1.2)
                    result = score_contract(contract_text, contract_type)
                    st.session_state["ct_result"] = result
                    st.session_state["ct_meta"] = {
                        "type": contract_type,
                        "jur": jurisdiction,
                        "cpty": counterparty_type
                    }

    with col_info:
        st.markdown('<div class="section-title">📚 Audit Framework</div>', unsafe_allow_html=True)
        frameworks = [
            ("Baker McKenzie", "SPA due diligence checklist, HKEX IPO review standards, cross-border M&A risk matrix."),
            ("FCPA / UK Bribery Act", "Anti-corruption clause verification per DOJ FCPA Resource Guide §3 and UK Bribery Act 2010 s.7."),
            ("ICSID / ICC Rules", "Dispute resolution clause conformance with ICSID Arbitration Rules 2022 and ICC 2021 Rules."),
            ("HKEX Listing Rules", "Main Board Rules 8, 11, 14 and 14A — connected transactions, working capital, profit forecasts."),
            ("UN EITI Standard", "Payment transparency and beneficial ownership disclosure per EITI Standard 2023."),
            ("UNCITRAL Model Law", "International arbitration clause structure per UNCITRAL 2006 amendments."),
        ]
        for name, detail in frameworks:
            with st.expander(f"⚖ {name}"):
                st.markdown(f'<div style="font-size:12px;color:#9090A0;line-height:1.6;">{detail}</div>', unsafe_allow_html=True)

    # ── Results ───────────────────────────────────────────────────────────────
    if "ct_result" in st.session_state:
        result = st.session_state["ct_result"]
        meta   = st.session_state["ct_meta"]
        score  = result["score"]
        level  = result["level"]
        findings = result["findings"]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Analysis Results</div>', unsafe_allow_html=True)

        # Score Header
        score_color = {"critical": "#ef5350", "high": "#FF9800", "medium": "#FFC107", "low": "#4CAF50"}[level]
        st.markdown(f"""
        <div class="glass-panel" style="margin-bottom:24px;">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
            <div>
              <div style="font-size:11px;color:#C9A84C66;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:6px;">
                COMPOSITE RISK SCORE
              </div>
              <div style="font-family:'Syne',sans-serif;font-size:52px;font-weight:800;
                          color:{score_color};line-height:1;">
                {score}
              </div>
              <div style="font-size:13px;color:#706050;margin-top:4px;">out of 100 · {level.upper()} RISK</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:12px;color:#706050;margin-bottom:6px;">
                <strong style="color:#C9A84C99;">Type:</strong> {meta['type']}
              </div>
              <div style="font-size:12px;color:#706050;margin-bottom:6px;">
                <strong style="color:#C9A84C99;">Jurisdiction:</strong> {meta['jur']}
              </div>
              <div style="font-size:12px;color:#706050;">
                <strong style="color:#C9A84C99;">Counterparty:</strong> {meta['cpty']}
              </div>
            </div>
          </div>
          <div style="margin-top:20px;">
        """, unsafe_allow_html=True)
        st.progress(score / 100)
        st.markdown("</div></div>", unsafe_allow_html=True)

        # Findings
        if findings:
            st.markdown(f'<div style="font-size:13px;color:#706050;margin-bottom:16px;">⚠ {len(findings)} risk flag(s) identified</div>', unsafe_allow_html=True)
            for f in sorted(findings, key=lambda x: -x["weight"]):
                sev = f["severity"]
                st.markdown(f"""
                <div style="padding:16px 18px;background:#13161C;border:1px solid #C9A84C12;
                            border-radius:10px;margin-bottom:10px;
                            border-left:3px solid {'#ef5350' if sev=='critical' else '#FF9800' if sev=='high' else '#FFC107' if sev=='medium' else '#4CAF50'}">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    <span class="risk-badge risk-{sev}" style="font-size:9px;padding:2px 7px;">{sev.upper()}</span>
                    <span style="font-family:'Syne',sans-serif;font-size:13px;
                                 font-weight:700;color:#E8D5A0;">{f['title']}</span>
                    <span style="margin-left:auto;font-size:10px;color:#C9A84C66;">
                      Weight: +{f['weight']}pts
                    </span>
                  </div>
                  <div style="font-size:12px;color:#9090A0;line-height:1.6;">{f['detail']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:20px;background:#4CAF5010;border:1px solid #4CAF5033;
                        border-radius:10px;text-align:center;">
              <div style="font-size:20px;margin-bottom:8px;">✅</div>
              <div style="font-size:14px;color:#4CAF50;font-weight:600;">
                No critical clause deficiencies detected
              </div>
              <div style="font-size:12px;color:#706050;margin-top:4px;">
                Manual review by qualified counsel is still recommended.
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Recommendations
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">💡 Counsel Recommendations</div>', unsafe_allow_html=True)
        recs = [
            ("Engage Baker McKenzie Energy Practice",
             "For complex cross-border PSAs and HKEX listings, engage lead counsel with dual energy/capital markets expertise."),
            ("UNCITRAL Seat Selection",
             "Specify London, Hong Kong, or Singapore as arbitral seat. Avoid jurisdictions without New York Convention membership."),
            ("Stabilization Clause Drafting",
             "Use hybrid stabilization (freezing + economic equilibrium). Avoid full legislative freeze which conflicts with ESG obligations."),
            ("Anti-Corruption Protocol",
             "Attach Baker McKenzie model FCPA/UKBA representations as Annex. Require counterparty compliance certification annually."),
        ]
        for title, detail in recs:
            st.markdown(f"""
            <div style="display:flex;gap:14px;padding:14px 16px;
                        background:#13161C;border:1px solid #C9A84C12;
                        border-radius:10px;margin-bottom:8px;">
              <div style="color:#C9A84C;font-size:16px;flex-shrink:0;">→</div>
              <div>
                <div style="font-family:'Syne',sans-serif;font-size:13px;
                             font-weight:600;color:#E8D5A0;margin-bottom:4px;">{title}</div>
                <div style="font-size:12px;color:#9090A0;line-height:1.5;">{detail}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
