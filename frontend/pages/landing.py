"""pages/landing.py
Landing page for ScoutAgent Pro.

A premium, dark-themed Streamlit landing page that explains the scouting workflow
with interactive tabs, metrics, expanders, and action-oriented CTAs.
"""

from __future__ import annotations

import json
from typing import Optional

import streamlit as st

# -----------------------------------------------------------------------------
# Optional animation support
# -----------------------------------------------------------------------------
# Add your own Lottie JSON URL here, or replace it with a local JSON asset path.
# Example:
#   LOTTIE_URL = "https://assets10.lottiefiles.com/packages/lf20_xxx.json"
# If you keep it empty, the page falls back to a subtle CSS animation card.
LOTTIE_URL: Optional[str] = None

try:
    from streamlit_lottie import st_lottie  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    st_lottie = None  # type: ignore

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
try:
    st.set_page_config(
        page_title="ScoutAgent Pro",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    # In some multipage setups, page config may already be set by the app entrypoint.
    pass

# -----------------------------------------------------------------------------
# Theme / CSS
# -----------------------------------------------------------------------------
_FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Syne:wght@500;600;700;800"
    "&family=DM+Sans:wght@400;500;600;700"
    "&family=JetBrains+Mono:wght@400;500;600"
    "&display=swap"
)

_CSS = f"""
<style>
@import url("{_FONTS}");

:root {{
  --bg: #07080c;
  --bg-2: #0b1020;
  --panel: rgba(15, 20, 34, 0.88);
  --panel-strong: rgba(17, 24, 41, 0.96);
  --panel-soft: rgba(255, 255, 255, 0.03);
  --border: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(110, 145, 255, 0.25);
  --text: #edf2ff;
  --muted: #9badcf;
  --faint: #6f7f9e;
  --accent: #1ef29a;
  --accent-2: #5ca8ff;
  --accent-3: #ffb84d;
  --danger: #ff5c7a;
  --shadow: 0 24px 80px rgba(0, 0, 0, 0.45);
  --radius: 22px;
}}

html, body, [data-testid="stAppViewContainer"] {{
  background:
    radial-gradient(circle at 10% 10%, rgba(92, 168, 255, 0.10), transparent 22%),
    radial-gradient(circle at 90% 0%, rgba(30, 242, 154, 0.08), transparent 16%),
    linear-gradient(180deg, #04050a 0%, #07080c 42%, #05070b 100%) !important;
  color: var(--text) !important;
  font-family: "DM Sans", sans-serif !important;
}}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer {{
  display: none !important;
}}

[data-testid="stMain"] {{
  background: transparent !important;
  padding-top: 0 !important;
}}

[data-testid="block-container"] {{
  padding: 0 !important;
  max-width: 100% !important;
}}

.landing-shell {{
  position: relative;
  padding: 30px 32px 52px;
  overflow: hidden;
}}

.landing-shell::before {{
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(120deg, rgba(255,255,255,0.03) 0%, transparent 18%, transparent 82%, rgba(255,255,255,0.02) 100%),
    radial-gradient(circle at 20% 20%, rgba(30, 242, 154, 0.09), transparent 20%),
    radial-gradient(circle at 85% 15%, rgba(92, 168, 255, 0.08), transparent 18%);
  opacity: 0.9;
  z-index: 0;
}}

.section {{
  position: relative;
  z-index: 1;
  max-width: 1280px;
  margin: 0 auto;
}}

.hero-wrap {{
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 18px;
  align-items: stretch;
  padding-top: 12px;
}}

.hero-copy, .hero-panel, .glass-card, .workflow-card, .expander-card, .cta-card {{
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.018));
  box-shadow: var(--shadow);
  backdrop-filter: blur(14px);
}}

.hero-copy {{
  padding: 28px 28px 24px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)),
    linear-gradient(135deg, rgba(18,24,41,0.96), rgba(10,14,25,0.92));
}}

.eyebrow {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid rgba(30, 242, 154, 0.2);
  background: rgba(30, 242, 154, 0.06);
  color: #aef7cf;
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  margin-bottom: 16px;
}}

.pulse-dot {{
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--accent);
  box-shadow: 0 0 0 0 rgba(30, 242, 154, 0.65);
  animation: pulse 2.2s infinite;
}}

.hero-copy h1 {{
  margin: 0;
  font-family: "Syne", sans-serif;
  font-size: clamp(42px, 5.5vw, 82px);
  line-height: 0.95;
  letter-spacing: -0.045em;
  color: var(--text);
  max-width: 11ch;
}}

.hero-copy .lede {{
  margin: 18px 0 0;
  max-width: 760px;
  font-size: clamp(17px, 1.6vw, 22px);
  line-height: 1.65;
  color: var(--muted);
}}

.chips {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}}

.chip {{
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.03);
  color: var(--text);
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}

.hero-stat-row {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 24px;
}}

.hero-stat {{
  padding: 14px 14px 13px;
  border-radius: 18px;
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.06);
}}

.hero-stat .label {{
  font-size: 10px;
  font-family: "JetBrains Mono", monospace;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--faint);
}}

.hero-stat .value {{
  margin-top: 8px;
  font-size: 28px;
  line-height: 1;
  font-family: "Syne", sans-serif;
  color: var(--text);
}}

.hero-stat .hint {{
  margin-top: 6px;
  font-size: 13px;
  color: var(--muted);
}}

.mini-alert {{
  margin-top: 18px;
  padding: 14px 16px;
  border-left: 3px solid var(--accent-3);
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(255,184,77,0.10), rgba(255,255,255,0.02));
}}

.mini-alert strong {{
  display: block;
  margin-bottom: 4px;
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #ffdca6;
}}

.mini-alert span {{
  color: var(--muted);
  line-height: 1.55;
}}

.hero-panel {{
  padding: 18px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)),
    radial-gradient(circle at 50% 0%, rgba(92, 168, 255, 0.12), transparent 35%),
    rgba(12, 16, 28, 0.94);
  overflow: hidden;
}}

.panel-title {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}}

.panel-title h3 {{
  margin: 0;
  font-family: "Syne", sans-serif;
  font-size: 18px;
  color: var(--text);
}}

.panel-title .tag {{
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(30, 242, 154, 0.09);
  border: 1px solid rgba(30, 242, 154, 0.18);
  color: #aef7cf;
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

.hero-panel .subtle {{
  color: var(--muted);
  line-height: 1.55;
  margin-bottom: 16px;
}}

.analysis-frame {{
  min-height: 220px;
  border-radius: 18px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)),
    radial-gradient(circle at 50% 50%, rgba(30,242,154,0.13), transparent 42%);
  border: 1px solid rgba(255,255,255,0.06);
  padding: 12px;
  position: relative;
  overflow: hidden;
}}

.scan-lines {{
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, transparent 0%, rgba(255,255,255,0.05) 50%, transparent 100%);
  opacity: 0.16;
  background-size: 100% 18px;
  animation: scan 5s linear infinite;
  pointer-events: none;
}}

.dashboard-metrics {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
}}

.metric-card {{
  padding: 14px 14px 13px;
  border-radius: 18px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
}}

.metric-card .label {{
  color: var(--faint);
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}}

.metric-card .value {{
  margin-top: 8px;
  font-family: "Syne", sans-serif;
  font-size: 24px;
  color: var(--text);
}}

.metric-card .delta {{
  margin-top: 4px;
  color: var(--accent);
  font-size: 13px;
}}

.section-label {{
  margin: 30px 0 14px;
  color: #cdd9ff;
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
}}

.grid-3 {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}}

.glass-card {{
  padding: 18px 18px 16px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)),
    rgba(13, 18, 30, 0.94);
  min-width: 0;
}}

.glass-card h3 {{
  margin: 0 0 10px;
  font-family: "Syne", sans-serif;
  font-size: 18px;
  color: var(--text);
}}

.glass-card p {{
  margin: 0;
  color: var(--muted);
  line-height: 1.65;
}}

.workflow-card {{
  padding: 18px;
  background: linear-gradient(180deg, rgba(14, 18, 30, 0.98), rgba(10, 14, 24, 0.96));
}}

.stepper {{
  display: flex;
  gap: 10px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}}

.step-pill {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  color: var(--text);
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}

.step-pill .num {{
  display: inline-grid;
  place-items: center;
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: rgba(92, 168, 255, 0.15);
  color: #bbd4ff;
  font-size: 10px;
}}

.tabs-note {{
  margin-top: 8px;
  color: var(--muted);
  line-height: 1.55;
}}

.expander-card {{
  padding: 4px;
  background: rgba(255,255,255,0.02);
  border-radius: 18px;
}}

.cta-card {{
  padding: 20px;
  background:
    linear-gradient(135deg, rgba(20, 27, 44, 0.96), rgba(8, 10, 18, 0.98));
}}

.cta-card h2 {{
  margin: 0 0 8px;
  font-family: "Syne", sans-serif;
  font-size: clamp(24px, 2.8vw, 36px);
  color: var(--text);
}}

.cta-card p {{
  margin: 0 0 18px;
  color: var(--muted);
  line-height: 1.6;
  max-width: 820px;
}}

.cta-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}}

.cta-mini {{
  padding: 16px;
  border-radius: 18px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
}}

.cta-mini strong {{
  display: block;
  margin-bottom: 8px;
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #d5e4ff;
}}

.cta-mini span {{
  color: var(--muted);
  line-height: 1.55;
}}

.button-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 18px;
}}

@keyframes pulse {{
  0%, 100% {{ box-shadow: 0 0 0 0 rgba(30, 242, 154, 0.55); transform: scale(1); }}
  50% {{ box-shadow: 0 0 0 10px rgba(30, 242, 154, 0.0); transform: scale(1.02); }}
}}

@keyframes scan {{
  from {{ transform: translateY(-100%); }}
  to {{ transform: translateY(100%); }}
}}

@media (max-width: 1100px) {{
  .hero-wrap,
  .grid-3,
  .cta-grid {{
    grid-template-columns: 1fr;
  }}
}}

@media (max-width: 720px) {{
  .landing-shell {{
    padding: 18px 16px 34px;
  }}

  .hero-copy {{
    padding: 20px 18px 18px;
  }}

  .hero-copy h1 {{
    max-width: 100%;
  }}

  .hero-stat-row {{
    grid-template-columns: 1fr;
  }}
}}
</style>
"""

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def _navigate(page_key: str) -> None:
    """Route through the existing multipage/session-state pattern."""
    st.session_state.active_page = page_key
    st.rerun()


def _page_link_or_button(label: str, page_key: str, icon: str, kind: str = "primary") -> None:
    """
    Prefer st.page_link when available; fall back to a button that updates session state.
    Update the path below if your multipage file names differ.
    """
    page_path_map = {
        "dashboard": "pages/dashboard.py",
        "scout": "pages/scout.py",
        "compare": "pages/compare.py",
        "transfer_strategy": "pages/transfer_strategy.py",
    }

    page_path = page_path_map.get(page_key)

    if hasattr(st, "page_link") and page_path:
        # NOTE: If your Streamlit version uses a different page_link signature,
        # adjust this call to match your installed release.
        st.page_link(page_path, label=label, icon=icon)
    else:
        if st.button(label, key=f"cta_{page_key}", type=kind, use_container_width=True):
            _navigate(page_key)


def _metric_card(label: str, value: str, delta: str) -> str:
    return f"""
    <div class="metric-card">
      <div class="label">{label}</div>
      <div class="value">{value}</div>
      <div class="delta">{delta}</div>
    </div>
    """


def _hero_animation() -> None:
    """Render a subtle animation panel.

    Replace LOTTIE_URL with your chosen asset source. Good options:
    - a lightweight AI / data scanning animation
    - a radar sweep
    - a football analytics / dashboard motion graphic
    """
    if st_lottie and LOTTIE_URL:
        try:
            # Optional dependency: streamlit-lottie
            st_lottie(json.loads(st.session_state.get("_lottie_payload", "{}")), height=300, key="landing_lottie")
        except Exception:
            st.markdown(
                """
                <div class="analysis-frame">
                  <div class="scan-lines"></div>
                  <div style="position:relative; z-index:1; padding:12px;">
                    <div class="eyebrow" style="margin-bottom:12px;"><span class="pulse-dot"></span> live analysis</div>
                    <h3 style="margin:0 0 8px; font-family: Syne, sans-serif;">Signal extraction in motion</h3>
                    <p style="margin:0; color: var(--muted); line-height:1.55;">
                      Add a Lottie JSON URL to <code>LOTTIE_URL</code> for a richer animated hero.
                    </p>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        return

    # CSS-only fallback animation.
    st.markdown(
        """
        <div class="analysis-frame">
          <div class="scan-lines"></div>
          <div style="position:relative; z-index:1; padding:12px; height:100%; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <div class="eyebrow" style="margin-bottom:12px;"><span class="pulse-dot"></span> live intelligence</div>
              <h3 style="margin:0 0 8px; font-family: Syne, sans-serif;">Scout engine listening</h3>
              <p style="margin:0; color: var(--muted); line-height:1.55;">
                The landing page mirrors the live workspace: a guided route from search to shortlist to action.
              </p>
            </div>
            <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px; margin-top:14px;">
              <div class="hero-stat">
                <div class="label">Search scope</div>
                <div class="value">147</div>
                <div class="hint">players in queue</div>
              </div>
              <div class="hero-stat">
                <div class="label">AI confidence</div>
                <div class="value">96%</div>
                <div class="hint">tactical fit score</div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _workflow_tab_scout() -> None:
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.info("Scout answers one question fast: who fits the brief?")
        st.metric("Candidates filtered", "147", "+34 this week")
        st.metric("Best match score", "96", "Bruno Ferreira")
        st.markdown(
            """
            <div class="expander-card">
              <div style="padding:16px 16px 8px;">
                <div class="section-label" style="margin-top:0;">Live scouting controls</div>
                <div style="display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:10px;">
                  <div class="hero-stat">
                    <div class="label">Role</div>
                    <div class="value">LW</div>
                    <div class="hint">wide threat</div>
                  </div>
                  <div class="hero-stat">
                    <div class="label">Budget</div>
                    <div class="value">€45M</div>
                    <div class="hint">summer window</div>
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("#### What the user experiences")
        st.progress(0.86)
        st.caption("Filters tighten from broad market view to a tactical shortlist.")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Press fit", "A")
            st.metric("Market value", "€15M")
        with c2:
            st.metric("Dribbling", "Elite")
            st.metric("Age", "24")
        st.code(
            "Scout → search_players(query, filters) → rank by tactical fit → shortlist",
            language="text",
        )


def _workflow_tab_compare() -> None:
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.info("Compare turns two or more targets into a decision.")
        st.metric("Similarity score", "94%", "AI computed")
        st.metric("Decision confidence", "High", "recommended shortlist")
        st.markdown(
            """
            <div class="expander-card">
              <div style="padding:16px;">
                <div class="section-label" style="margin-top:0;">Side-by-side reasoning</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                  <div class="glass-card" style="padding:14px;">
                    <h3 style="margin-top:0; font-size:16px;">Strengths</h3>
                    <p>Explains pace, pressing, aerial dominance, and creation in a compact verdict.</p>
                  </div>
                  <div class="glass-card" style="padding:14px;">
                    <h3 style="margin-top:0; font-size:16px;">Trade-offs</h3>
                    <p>Highlights what the scout should watch next: fee, availability, age curve, and role overlap.</p>
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("#### What the user experiences")
        st.progress(0.94)
        st.caption("The interface compares profiles, then compresses the analysis into a verdict.")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Pace", "93", "+6 vs target")
            st.metric("Dribbling", "92", "+4 vs target")
        with c2:
            st.metric("Aerial", "66", "-8 vs target")
            st.metric("Pressing", "74", "+5 vs target")
        st.code(
            "Compare → attribute radar → head-to-head stats → AI verdict",
            language="text",
        )


def _workflow_tab_act() -> None:
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.info("Act turns analysis into an operational next step.")
        st.metric("Shortlist size", "3", "ready for review")
        st.metric("Budget remaining", "€32M", "after primary target")
        st.markdown(
            """
            <div class="expander-card">
              <div style="padding:16px;">
                <div class="section-label" style="margin-top:0;">Action loop</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                  <div class="hero-stat">
                    <div class="label">Primary action</div>
                    <div class="value">Save</div>
                    <div class="hint">shortlist candidate</div>
                  </div>
                  <div class="hero-stat">
                    <div class="label">Secondary action</div>
                    <div class="value">Route</div>
                    <div class="hint">dashboard / memory</div>
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("#### What the user experiences")
        st.progress(0.78)
        st.caption("The platform keeps the next click obvious: review, save, or move to squad planning.")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Shortlisted", "1")
            st.metric("Queued tasks", "4")
        with c2:
            st.metric("Alerts", "2")
            st.metric("Win-now fit", "Strong")
        st.code(
            "Act → shortlist → push to squad builder → monitor memory",
            language="text",
        )


def _workflow_tab_memory() -> None:
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.info("Memory keeps the workspace coherent across sessions.")
        st.metric("Stored preferences", "12", "tactical + market")
        st.metric("Search history", "34", "recent queries")
        st.markdown(
            """
            <div class="expander-card">
              <div style="padding:16px;">
                <div class="section-label" style="margin-top:0;">Why this matters</div>
                <p style="margin:0; color: var(--muted); line-height:1.65;">
                  The landing page should tell a visitor that the app remembers club context, tactical style,
                  and previous shortlist decisions so every next result is more relevant.
                </p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("#### What the user experiences")
        st.progress(0.64)
        st.caption("Searches and verdicts feed the memory layer so the system improves over time.")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Memory reads", "1")
            st.metric("Vector store", "text-embedding-3-small")
        with c2:
            st.metric("Reasoning trace", "Live")
            st.metric("Feedback loops", "7")
        st.code(
            "Memory → retrieve club context → refine search → explain reasoning",
            language="text",
        )


def _render_feature_row() -> None:
    st.markdown('<div class="section-label">Platform strengths</div>', unsafe_allow_html=True)
    cols = st.columns(3, gap="medium")

    items = [
        (
            "Fast discovery",
            "Filters by role, league, age, budget, contract window, and output profile without dumping a wall of text on the user.",
        ),
        (
            "Analytical comparison",
            "Converts raw scouting into side-by-side insight, then compresses the answer into a crisp verdict.",
        ),
        (
            "Actionable memory",
            "Remembers club preferences and market assumptions so each new scouting pass becomes more precise.",
        ),
    ]

    for col, (title, body) in zip(cols, items):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="min-height: 170px;">
                  <h3>{title}</h3>
                  <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_secondary_features() -> None:
    st.markdown('<div class="section-label">Secondary features</div>', unsafe_allow_html=True)

    with st.expander("Why the interface feels more like a workspace than a website", expanded=False):
        st.write(
            "The landing page uses cards, metrics, and tabs to mirror the real product flow, so visitors "
            "understand the app before they ever click a scouting page."
        )

    with st.expander("Recommended design extras you can add later", expanded=False):
        st.write(
            "Add a Lottie animation, a real radar chart preview, or a small embedded screenshot carousel "
            "to reinforce the premium analytical tone."
        )

    with st.expander("Suggested asset locations", expanded=False):
        st.code(
            "assets/lottie/scouting_scan.json\nassets/images/hero_glow.png\nassets/images/mini_radar.png",
            language="text",
        )


def _render_cta_band() -> None:
    st.markdown(
        """
        <div class="cta-card">
          <h2>Two clear paths. No guesswork.</h2>
          <p>
            Open Dashboard for the squad-wide operating view. Open Scout to start with player discovery.
            Open Compare when you already have targets and need a direct decision.
          </p>
          <div class="cta-grid">
            <div class="cta-mini">
              <strong>Dashboard</strong>
              <span>See the live scouting backlog, shortlist state, budget, and agent activity in one place.</span>
            </div>
            <div class="cta-mini">
              <strong>Scout / Compare</strong>
              <span>Move directly into player search or side-by-side comparison once the brief is clear.</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    btn_left, btn_mid, btn_right = st.columns([1, 1, 1.6], gap="medium")

    with btn_left:
        if st.button("Open Dashboard", key="landing_open_dashboard", use_container_width=True, type="primary"):
            _navigate("dashboard")

    with btn_mid:
        if st.button("Start Scouting", key="landing_start_scouting", use_container_width=True):
            _navigate("scout")

    with btn_right:
        # Leave the page path here in case you want a direct link behavior instead of session-state routing.
        _page_link_or_button("Go to Compare", "compare", "🔁", kind="secondary")


# -----------------------------------------------------------------------------
# Render
# -----------------------------------------------------------------------------
def render_home() -> None:
    """Render the landing page."""
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown('<div class="landing-shell"><div class="section">', unsafe_allow_html=True)

    # Hero
    st.markdown(
        """
        <div class="hero-wrap">
          <div class="hero-copy">
            <div class="eyebrow"><span class="pulse-dot"></span> live intelligence workspace</div>
            <h1>Scout faster. Decide with context.</h1>
            <p class="lede">
              ScoutAgent Pro turns football recruitment into a guided analytical workflow:
              discover fit, compare options, and act on a shortlist with memory-backed context.
            </p>

            <div class="chips">
              <span class="chip">Player scouting</span>
              <span class="chip">Comparisons</span>
              <span class="chip">Shortlists</span>
              <span class="chip">Memory-backed context</span>
            </div>

            <div class="mini-alert">
              <strong>Best first move</strong>
              <span>
                Know the role? Go straight to Scout. Already have a target list? Use Compare.
                Need squad-wide context? Open Dashboard first.
              </span>
            </div>

            <div class="hero-stat-row">
              <div class="hero-stat">
                <div class="label">Players scouted</div>
                <div class="value">1,247</div>
                <div class="hint">+84 this week</div>
              </div>
              <div class="hero-stat">
                <div class="label">Active shortlists</div>
                <div class="value">3</div>
                <div class="hint">12 players total</div>
              </div>
              <div class="hero-stat">
                <div class="label">Budget tracked</div>
                <div class="value">€45M</div>
                <div class="hint">summer window</div>
              </div>
            </div>
          </div>

          <div class="hero-panel">
          <div class="panel-title">
            <h3>AI analysis preview</h3>
            <div class="tag">signal live</div>
          </div>

          <div class="subtle">
            A subtle motion layer makes the landing page feel alive immediately.
            Replace the placeholder with your preferred animation asset when ready.
          </div>

          <div class="animation-placeholder">
            <div class="pulse-ring"></div>
            <div class="pulse-ring delay"></div>
            <div class="pulse-core"></div>
          </div>

        </div>
      </div>
      """,
      unsafe_allow_html=True,
      )
    

   
    # Platform strengths
    _render_feature_row()

    # Workflow tabs
    st.markdown('<div class="section-label">How it works</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="workflow-card">
          <div class="stepper">
            <span class="step-pill"><span class="num">1</span> Scout</span>
            <span class="step-pill"><span class="num">2</span> Compare</span>
            <span class="step-pill"><span class="num">3</span> Act</span>
            <span class="step-pill"><span class="num">4</span> Memory</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    scout_tab, compare_tab, act_tab, memory_tab = st.tabs(["Scout", "Compare", "Act", "Memory"])

    with scout_tab:
        _workflow_tab_scout()

    with compare_tab:
        _workflow_tab_compare()

    with act_tab:
        _workflow_tab_act()

    with memory_tab:
        _workflow_tab_memory()

    # Secondary features
    _render_secondary_features()

    # CTA band
    st.markdown('<div class="section-label">Next step</div>', unsafe_allow_html=True)
    _render_cta_band()

    st.markdown("</div></div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Entry point for Streamlit page
# -----------------------------------------------------------------------------
render_home()
