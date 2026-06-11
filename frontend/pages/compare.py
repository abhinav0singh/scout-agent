"""
pages/compare.py
Player comparison page — radar chart, stat bars, season stats,
pros/cons, and agent comparison summary.
"""

import streamlit as st
import plotly.graph_objects as go
from services.mock_data import MockDataService
from components.agent_reasoning_panel import html

C = {
    "green":  "#00E87D", "amber": "#FF8C00",
    "blue":   "#3B8EFF", "purple": "#B87DFF",
    "red":    "#FF4545",
    "t1": "#E2EDFF", "t2": "#7A92B0", "t3": "#3D5270",
    "s1": "#09101C", "s2": "#0D1525", "s3": "#12192E",
    "b1": "#192437",
}


def _score_color(s: int) -> str:
    return C["green"] if s >= 92 else C["amber"] if s >= 85 else C["t2"]


def _render_player_selector(slot: str, current: dict, all_players: list[dict], other: dict) -> dict:
    """Render a player selector panel. Returns selected player."""
    color = C["green"] if slot == "a" else C["blue"]
    sc = _score_color(current["match_score"])

    # Header
    st.markdown(f"""
    <div style="background:#0D1525;border:2px solid {color}30;border-radius:10px;padding:14px;">
      <div style="display:flex;gap:12px;align-items:center;margin-bottom:12px;">
        <div style="font-size:24px;">{current['flag']}</div>
        <div style="flex:1;">
          <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;
            color:#E2EDFF;">{current['name']}</div>
          <div style="font-size:11px;color:#7A92B0;">{current['club']} · {current['league']}</div>
        </div>
        <div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:{sc};">
          {current['match_score']}
        </div>
      </div>
      <div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:12px;">
        {''.join([f"<span style='background:{C['blue']}18;color:{C['blue']};border:1px solid {C['blue']}28;border-radius:4px;padding:1px 6px;font-size:9px;font-weight:700;'>{x}</span>" for x in [current['position'], f"Age {current['age']}", current['market_value_display']]])}
      </div>
    """, unsafe_allow_html=True)

    # Player switcher buttons
    options = [p for p in all_players if p["id"] != other["id"]]
    cols = st.columns(len(options))
    selected = current
    for i, (col, p) in enumerate(zip(cols, options)):
        with col:
            is_active = p["id"] == current["id"]
            if st.button(
                p["name"].split()[-1],
                key=f"sel_{slot}_{p['id']}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                selected = p
                if slot == "a":
                    st.session_state.compare_player_a = p
                else:
                    st.session_state.compare_player_b = p
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    return selected


def _render_radar_chart(pa: dict, pb: dict) -> None:
    """Render dual-player radar chart with Plotly."""
    attrs  = list(pa["radar"].keys())
    vals_a = list(pa["radar"].values()) + [list(pa["radar"].values())[0]]
    vals_b = list(pb["radar"].values()) + [list(pb["radar"].values())[0]]
    attrs_closed = attrs + [attrs[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=vals_a, theta=attrs_closed,
        fill="toself", name=pa["name"].split()[-1],
        line=dict(color=C["green"], width=2),
        fillcolor="rgba(0,232,125,0.15)",
        marker=dict(size=4, color=C["green"]),
    ))

    fig.add_trace(go.Scatterpolar(
        r=vals_b, theta=attrs_closed,
        fill="toself", name=pb["name"].split()[-1],
        line=dict(color=C["blue"], width=2),
        fillcolor="rgba(59,142,255,0.12)",
        marker=dict(size=4, color=C["blue"]),
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 100],
                tickfont=dict(size=8, color=C["t3"]),
                gridcolor=C["b1"], linecolor=C["b1"],
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=C["t2"], family="DM Sans"),
                linecolor=C["b1"], gridcolor=C["b1"],
            ),
        ),
        legend=dict(
            font=dict(color=C["t2"], size=11, family="DM Sans"),
            bgcolor="rgba(0,0,0,0)",
            x=0.5, y=-0.08, orientation="h", xanchor="center",
        ),
        margin=dict(l=30, r=30, t=20, b=30),
        height=290,
    )

    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:16px;margin-bottom:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
        color:#E2EDFF;margin-bottom:10px;">Attribute Radar</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


def _render_stat_comparison(pa: dict, pb: dict) -> None:
    """Render head-to-head stat comparison bars."""
    attrs = list(pa["radar"].keys())
    bars_html = ""

    for attr in attrs:
        a = pa["radar"][attr]
        b = pb["radar"][attr]
        winner = "a" if a > b else "b" if b > a else "tie"

        bar_a = f'<div style="flex:1;height:5px;background:#192437;border-radius:3px 0 0 3px;overflow:hidden;display:flex;justify-content:flex-end;"><div style="width:{a}%;height:100%;background:#00E87D;opacity:.8;"></div></div>'
        bar_b = f'<div style="flex:1;height:5px;background:#192437;border-radius:0 3px 3px 0;overflow:hidden;"><div style="width:{b}%;height:100%;background:#3B8EFF;opacity:.8;"></div></div>'

        bars_html += f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:9px;">
          <div style="width:26px;text-align:right;font-family:'Syne',sans-serif;
            font-size:13px;font-weight:700;color:{'#00E87D' if winner=='a' else '#7A92B0'};">
            {a}</div>
          <div style="flex:1;display:flex;gap:2px;">{bar_a}{bar_b}</div>
          <div style="width:26px;font-family:'Syne',sans-serif;font-size:13px;
            font-weight:700;color:{'#3B8EFF' if winner=='b' else '#7A92B0'};">{b}</div>
          <div style="width:60px;font-size:10px;color:#3D5270;
            text-transform:uppercase;letter-spacing:.04em;">{attr}</div>
        </div>"""

    # Season stats comparison
    season_keys = [("goals","Goals"),("assists","Assists"),("appearances","Apps"),("xg","xG")]
    season_html = '<div style="display:grid;grid-template-columns:1fr auto 1fr;gap:8px;margin-top:12px;padding-top:12px;border-top:1px solid #192437;">'
    for key, label in season_keys:
        va = pa["season_stats"][key]
        vb = pb["season_stats"][key]
        season_html += f"""
        <div style="text-align:right;font-family:'Syne',sans-serif;font-size:14px;
          font-weight:700;color:#00E87D;">{va}</div>
        <div style="text-align:center;font-size:10px;color:#3D5270;">{label}</div>
        <div style="text-align:left;font-family:'Syne',sans-serif;font-size:14px;
          font-weight:700;color:#3B8EFF;">{vb}</div>"""
    season_html += "</div>"

    html(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:16px;margin-bottom:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
        color:#E2EDFF;margin-bottom:14px;">Head-to-Head Stats</div>
      {bars_html}
      {season_html}
    </div>
    """)


def _render_similarity_score(pa: dict, pb: dict) -> None:
    """Render similarity gauge."""
    score = round((pa["similarity_score"] + pb["similarity_score"]) / 2)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge=dict(
            axis=dict(range=[0, 100], tickfont=dict(color=C["t3"], size=9)),
            bar=dict(color=C["green"]),
            bgcolor=C["s1"],
            bordercolor=C["b1"],
            steps=[
                dict(range=[0, 50],  color=C["s2"]),
                dict(range=[50, 75], color="rgba(255,140,0,0.1)"),
                dict(range=[75, 100],color="rgba(0,232,125,0.1)"),
            ],
        ),
        number=dict(suffix="%", font=dict(size=28, color=C["t1"], family="Syne")),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=160,
        margin=dict(l=20, r=20, t=20, b=0),
    )

    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;margin-bottom:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
        color:#E2EDFF;margin-bottom:6px;">Similarity Score</div>
      <div style="font-size:10px;color:#3D5270;margin-bottom:8px;">AI-computed profile similarity</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


def _render_pros_cons(pa: dict, pb: dict) -> None:
    """Render side-by-side pros/cons."""
    def pros_list(items: list, color: str) -> str:
        return "".join([
            f"<div style='display:flex;gap:6px;margin-bottom:5px;'>"
            f"<span style='color:{color};font-size:11px;flex-shrink:0;margin-top:1px;'>✓</span>"
            f"<span style='font-size:11px;color:#7A92B0;line-height:1.5;'>{item}</span></div>"
            for item in items
        ])

    def cons_list(items: list) -> str:
        return "".join([
            f"<div style='display:flex;gap:6px;margin-bottom:5px;'>"
            f"<span style='color:#FF4545;font-size:11px;flex-shrink:0;margin-top:1px;'>✗</span>"
            f"<span style='font-size:11px;color:#7A92B0;line-height:1.5;'>{item}</span></div>"
            for item in items
        ])

    st.markdown(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:16px;border-left:3px solid #B87DFF;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
        <span style="font-size:14px;">🧠</span>
        <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#E2EDFF;">
          Agent Comparison Analysis
        </div>
        <span style="background:#B87DFF18;color:#B87DFF;border:1px solid #B87DFF28;
          border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;">AI GENERATED</span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">
        <div>
          <div style="font-size:10px;color:#00E87D;font-weight:700;text-transform:uppercase;
            letter-spacing:.06em;margin-bottom:8px;">{pa['name'].split()[0]} · Strengths</div>
          {pros_list(pa['pros'][:3], C['green'])}
          <div style="margin-top:10px;">
            <div style="font-size:10px;color:#FF4545;font-weight:700;text-transform:uppercase;
              letter-spacing:.06em;margin-bottom:6px;">Concerns</div>
            {cons_list(pa['cons'][:2])}
          </div>
        </div>
        <div style="padding:14px 16px;background:#09101C;border-radius:9px;text-align:center;">
          <div style="font-size:10px;color:#3D5270;text-transform:uppercase;
            letter-spacing:.06em;margin-bottom:10px;">Agent Verdict</div>
          <div style="font-size:11px;color:#7A92B0;line-height:1.7;">
            <strong style="color:#00E87D;">{pa['name'].split()[0]}</strong> edges on physical
            and finishing metrics. <strong style="color:#3B8EFF;">{pb['name'].split()[0]}</strong>
            leads on creativity and vision. Both recommended for shortlist — choice
            depends on final tactical brief.
          </div>
        </div>
        <div>
          <div style="font-size:10px;color:#3B8EFF;font-weight:700;text-transform:uppercase;
            letter-spacing:.06em;margin-bottom:8px;">{pb['name'].split()[0]} · Strengths</div>
          {pros_list(pb['pros'][:3], C['blue'])}
          <div style="margin-top:10px;">
            <div style="font-size:10px;color:#FF4545;font-weight:700;text-transform:uppercase;
              letter-spacing:.06em;margin-bottom:6px;">Concerns</div>
            {cons_list(pb['cons'][:2])}
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_compare() -> None:
    """Main Compare page renderer."""
    all_players = MockDataService.get_players()

    pa = st.session_state.get("compare_player_a") or all_players[2]
    pb = st.session_state.get("compare_player_b") or all_players[0]

    # ── Player Selectors ──────────────────────────────────────
    sel_a_col, vs_col, sel_b_col = st.columns([3, 1, 3])

    with sel_a_col:
        _render_player_selector("a", pa, all_players, pb)

    with vs_col:
        score = round((pa["similarity_score"] + pb["similarity_score"]) / 2)
        st.markdown(f"""
        <div style="text-align:center;padding-top:20px;">
          <div style="font-size:11px;color:#3D5270;margin-bottom:4px;">SIMILARITY</div>
          <div style="font-family:'Syne',sans-serif;font-size:34px;font-weight:800;
            color:#00E87D;line-height:1;">{score}%</div>
          <div style="font-size:10px;color:#3D5270;margin-top:2px;">AI Score</div>
        </div>
        """, unsafe_allow_html=True)

    with sel_b_col:
        _render_player_selector("b", pb, all_players, pa)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Charts Row ────────────────────────────────────────────
    radar_col, stats_col, sim_col = st.columns([2, 2, 1])

    with radar_col:
        _render_radar_chart(pa, pb)

    with stats_col:
        _render_stat_comparison(pa, pb)

    with sim_col:
        _render_similarity_score(pa, pb)

    # ── AI Insight ────────────────────────────────────────────
    _render_pros_cons(pa, pb)
