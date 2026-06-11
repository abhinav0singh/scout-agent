"""
pages/shortlists.py
Shortlists — manage saved player shortlists,
export to PDF, share with scouting team.
"""

import streamlit as st
from services.mock_data import MockDataService
from state.session_state import toggle_shortlist
from components.agent_reasoning_panel import html

C = {
    "green": "#00E87D", "amber": "#FF8C00", "blue": "#3B8EFF",
    "t1": "#E2EDFF", "t2": "#7A92B0", "t3": "#3D5270",
    "s1": "#09101C", "s2": "#0D1525", "b1": "#192437",
}


def render_shortlists() -> None:
    """Shortlists page renderer."""
    shortlist = st.session_state.get("shortlist", [])

    # Header actions
    h_col, btn_col = st.columns([4, 1])
    with h_col:
        st.markdown(f"""
        <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px 16px;margin-bottom:14px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#E2EDFF;">
              Active Shortlist
            </div>
            <span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;
              border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;">
              {len(shortlist)} players
            </span>
            <span style="font-size:11px;color:#3D5270;margin-left:auto;">
              Shared with 2 scouts · Last updated 2h ago
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    if not shortlist:
        st.markdown("""
        <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
          padding:48px 24px;text-align:center;">
          <div style="font-size:32px;margin-bottom:12px;">☆</div>
          <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;
            color:#E2EDFF;margin-bottom:8px;">No Players Shortlisted</div>
          <div style="font-size:12px;color:#3D5270;">
            Go to the Scout page and click "+ Shortlist" to add players here.
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Shortlist table
    cols = st.columns([0.4, 1.6, 1.2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8])
    headers = ["#", "Player", "Club · League", "Pos", "Age", "Value", "Score", "xG+xA", "Action"]
    for col, h in zip(cols, headers):
        with col:
            st.markdown(f'<div style="font-size:9px;color:#3D5270;text-transform:uppercase;letter-spacing:.06em;padding:4px 0;">{h}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:2px;background:#192437;margin-bottom:8px;'></div>", unsafe_allow_html=True)

    for i, player in enumerate(shortlist):
        score = player["match_score"]
        sc_color = C["green"] if score >= 92 else C["amber"] if score >= 85 else C["t2"]
        xga = round(player["season_stats"]["xg"] + player["season_stats"]["xa"], 1)

        row_cols = st.columns([0.4, 1.6, 1.2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8])
        data = [
            str(i + 1), player["name"],
            f'{player["club"]} · {player["league"]}',
            player["position"], str(player["age"]),
            player["market_value_display"],
            str(score), str(xga),
        ]
        colors = [C["t3"], C["t1"], C["t2"], C["blue"], C["t3"], C["amber"], sc_color, C["green"]]
        weights = ["400", "700", "400", "700", "400", "700", "800", "700"]

        for col, val, color, weight in zip(row_cols[:-1], data, colors, weights):
            with col:
                font = "'Syne',sans-serif" if weight == "800" else "'DM Sans',sans-serif"
                st.markdown(
                    f'<div style="font-size:12px;font-weight:{weight};color:{color};'
                    f'font-family:{font};padding:8px 0;border-bottom:1px solid #192437;">{val}</div>',
                    unsafe_allow_html=True
                )
        with row_cols[-1]:
            if st.button("✕", key=f"remove_{player['id']}", help="Remove from shortlist"):
                toggle_shortlist(player)
                st.rerun()

    # Agent recommendation
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:14px 16px;border-left:3px solid #B87DFF;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span>🧠</span>
        <span style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#E2EDFF;">
          Agent Shortlist Analysis</span>
      </div>
      <div style="font-size:12px;color:#7A92B0;line-height:1.7;">
        Your shortlist covers the LW position gap (Ferreira) but has no DM depth option.
        Recommend adding Kowalski (Legia Warsaw) to provide pressing cover.
        Combined transfer spend: <strong style="color:#00E87D;">€27M</strong> — within budget.
      </div>
    </div>
    """, unsafe_allow_html=True)