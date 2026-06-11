"""
pages/squad_builder.py
Squad Builder — visual formation grid with position slots,
budget tracker, squad chemistry, and agent weakness analysis.
"""

import streamlit as st
import plotly.graph_objects as go
from services.mock_data import MockDataService
from components.agent_reasoning_panel import html

C = {
    "green":  "#00E87D", "amber":  "#FF8C00",
    "blue":   "#3B8EFF", "purple": "#B87DFF",
    "red":    "#FF4545",
    "t1": "#E2EDFF", "t2": "#7A92B0", "t3": "#3D5270",
    "s1": "#09101C", "s2": "#0D1525", "s3": "#12192E",
    "b1": "#192437",
}


def _render_formation_grid(slots: list[dict], formation: str) -> None:
    """Render the pitch formation with position circles."""
    vacancies = [s for s in slots if not s["filled"]]
    vacancy_count = len(vacancies)

    st.markdown(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
        <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#E2EDFF;">
          Formation: {formation} High Press
        </div>
        {'<span style="background:#FF8C0018;color:#FF8C00;border:1px solid #FF8C0028;border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;">' + str(vacancy_count) + ' Vacanc' + ('y' if vacancy_count==1 else 'ies') + '</span>' if vacancy_count > 0 else '<span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;">Squad Full</span>'}
      </div>
      <div style="font-size:11px;color:#3D5270;margin-bottom:18px;">
        {'LW slot vacant — Transfer Strategy recommends Bruno Ferreira (96% fit)' if vacancy_count > 0 else 'All positions filled.'}
      </div>
    """, unsafe_allow_html=True)

    # Group by row
    rows = sorted(set(s["row"] for s in slots), reverse=True)
    row_labels = {3: "ATT", 2: "MID", 1: "DEF", 0: "GK"}

    # Build pitch HTML
    pitch_html = """
    <div style="background:linear-gradient(180deg,#0A3020 0%,#071D12 100%);
      border-radius:12px;padding:28px 20px;position:relative;
      border:1px solid #0F4028;min-height:320px;">
    """

    # Pitch markings (CSS lines)
    pitch_html += """
    <div style="position:absolute;inset:15px 30px;border:1px solid rgba(255,255,255,0.05);border-radius:8px;"></div>
    <div style="position:absolute;top:50%;left:30px;right:30px;height:1px;background:rgba(255,255,255,0.05);"></div>
    <div style="position:absolute;top:25%;left:25%;right:25%;bottom:25%;border:1px solid rgba(255,255,255,0.04);border-radius:4px;"></div>
    """

    for row_idx in rows:
        row_slots = [s for s in slots if s["row"] == row_idx]
        n = len(row_slots)
        pitch_html += '<div style="display:flex;justify-content:center;gap:0;margin-bottom:28px;position:relative;z-index:1;">'

        for slot in row_slots:
            if slot["filled"]:
                circle_bg   = "rgba(0,232,125,0.12)"
                circle_bdr  = "rgba(0,232,125,0.4)"
                pos_color   = C["green"]
                name_color  = C["t2"]
                name        = slot["player"].split()[-1] if " " in slot["player"] else slot["player"]
                glow        = ""
            else:
                circle_bg   = "rgba(255,140,0,0.12)"
                circle_bdr  = C["amber"]
                pos_color   = C["amber"]
                name_color  = C["amber"]
                name        = "VACANT"
                glow        = "animation:glow-amber 2s ease infinite;"

            pitch_html += f"""
            <div style="display:flex;flex-direction:column;align-items:center;gap:5px;flex:1;max-width:90px;">
              <div style="width:52px;height:52px;border-radius:50%;background:{circle_bg};
                border:2px solid {circle_bdr};display:flex;align-items:center;
                justify-content:center;{glow}">
                <span style="font-size:10px;font-weight:700;color:{pos_color};
                  text-align:center;font-family:'DM Sans',sans-serif;">{slot['position']}</span>
              </div>
              <div style="font-size:9px;color:{name_color};font-family:'DM Sans',sans-serif;
                text-align:center;max-width:70px;line-height:1.3;font-weight:{'700' if not slot['filled'] else '400'};">
                {name}
              </div>
            </div>"""

        pitch_html += "</div>"

    pitch_html += "</div>"
    st.markdown(pitch_html + "</div>", unsafe_allow_html=True)


def _render_budget_panel() -> None:
    """Render squad budget tracker with bar chart."""
    budget_items = [
        {"label": "Squad Cost",      "value": 68,  "total": 113, "display": "€68M",  "color": C["green"]},
        {"label": "Summer Budget",   "value": 45,  "total": 113, "display": "€45M",  "color": C["amber"]},
        {"label": "Weekly Wages",    "value": 840, "total": 1200,"display": "£840k/wk","color": C["blue"]},
        {"label": "Wage Budget Left","value": 360, "total": 1200,"display": "£360k/wk","color": C["t3"]},
    ]

    bars_html = ""
    for item in budget_items:
        pct = min(round(item["value"] / item["total"] * 100), 100)
        bars_html += f"""
        <div style="margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span style="font-size:11px;color:#7A92B0;">{item['label']}</span>
            <span style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
              color:{item['color']};">{item['display']}</span>
          </div>
          <div style="height:5px;background:#192437;border-radius:3px;overflow:hidden;">
            <div style="width:{pct}%;height:100%;background:{item['color']};
              border-radius:3px;transition:width .8s ease;"></div>
          </div>
        </div>"""

    html(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;margin-bottom:12px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
        color:#E2EDFF;margin-bottom:14px;">Budget Tracker</div>
      {bars_html}
    </div>
    """)


def _render_squad_chemistry() -> None:
    """Render squad chemistry radar."""
    categories = ["Pace", "Press Fit", "Technical", "Aerial", "Experience", "Depth"]
    values_now  = [82, 78, 85, 74, 68, 60]
    values_full = [88, 92, 87, 78, 70, 75]
    closed = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_now + [values_now[0]], theta=closed,
        fill="toself", name="Current",
        line=dict(color=C["blue"], width=2),
        fillcolor="rgba(59,142,255,0.12)",
    ))
    fig.add_trace(go.Scatterpolar(
        r=values_full + [values_full[0]], theta=closed,
        fill="toself", name="After Targets",
        line=dict(color=C["green"], width=2, dash="dot"),
        fillcolor="rgba(0,232,125,0.08)",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100],
                tickfont=dict(size=8, color=C["t3"]),
                gridcolor=C["b1"], linecolor=C["b1"]),
            angularaxis=dict(
                tickfont=dict(size=9, color=C["t2"], family="DM Sans"),
                linecolor=C["b1"], gridcolor=C["b1"]),
        ),
        legend=dict(font=dict(color=C["t2"], size=10, family="DM Sans"),
            bgcolor="rgba(0,0,0,0)", orientation="h",
            x=0.5, y=-0.1, xanchor="center"),
        margin=dict(l=20, r=20, t=10, b=30),
        height=230,
    )

    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:14px;margin-bottom:12px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
        color:#E2EDFF;margin-bottom:6px;">Squad Chemistry</div>
      <div style="font-size:10px;color:#3D5270;margin-bottom:8px;">
        Current squad vs. after transfer targets
      </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


def _render_agent_analysis() -> None:
    """Render agent squad weakness analysis."""
    analyses = [
        {
            "title":  "LW Vacancy — Critical",
            "detail": "Bruno Ferreira (96% fit) strongly recommended. Pace + press profile matches 4-3-3 system requirements exactly.",
            "color":  C["red"],
            "action": "Act Now",
        },
        {
            "title":  "CB Depth — Warning",
            "detail": "Single first-choice CB pairing. Bianchi (Atalanta U23) recommended as low-cost depth solution at €5M.",
            "color":  C["amber"],
            "action": "Monitor",
        },
        {
            "title":  "Midfield Balance — Good",
            "detail": "Press + vision balance across CM3 is elite. Ugochukwu (DM) press metrics in top 8% of PL midfielders.",
            "color":  C["green"],
            "action": "No Action",
        },
        {
            "title":  "Wage Budget — Healthy",
            "detail": "£360k/week remaining. Sufficient to accommodate Ferreira (est. £65k) and Lindqvist (est. £45k).",
            "color":  C["blue"],
            "action": "OK",
        },
    ]

    items_html = "".join([
        f'<div style="padding:11px 13px;background:#09101C;border-radius:8px;'
        f'border-left:2px solid {a["color"]};margin-bottom:8px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">'
        f'<span style="font-size:11px;font-weight:700;color:{a["color"]};">{a["title"]}</span>'
        f'<span style="background:{a["color"]}18;color:{a["color"]};border:1px solid {a["color"]}28;'
        f'border-radius:4px;padding:1px 6px;font-size:9px;font-weight:700;">{a["action"]}</span>'
        f'</div>'
        f'<div style="font-size:11px;color:#7A92B0;line-height:1.5;">{a["detail"]}</div>'
        f'</div>'
        for a in analyses
    ])

    st.markdown(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
        color:#E2EDFF;margin-bottom:12px;display:flex;align-items:center;gap:7px;">
        🧠 Agent Analysis
      </div>
      {items_html}
    </div>
    """, unsafe_allow_html=True)


def render_squad_builder() -> None:
    """Main Squad Builder page renderer."""
    formation = st.session_state.get("squad_formation", "4-3-3")
    slots = MockDataService.get_squad_slots(formation)

    # Formation switcher
    form_col, _ = st.columns([2, 3])
    with form_col:
        new_formation = st.selectbox(
            "Formation",
            ["4-3-3", "4-2-3-1", "3-4-3", "4-4-2"],
            key="squad_formation_select",
            label_visibility="collapsed",
        )
        if new_formation != formation:
            st.session_state.squad_formation = new_formation
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Layout
    pitch_col, panel_col = st.columns([2.2, 1])

    with pitch_col:
        _render_formation_grid(slots, formation)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Roster table
        st.markdown("""
        <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
          <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
            color:#E2EDFF;margin-bottom:12px;">Starting XI</div>
          <div style="display:grid;grid-template-columns:0.5fr 1fr 2fr 1fr 1fr;
            gap:8px;padding:5px 8px;margin-bottom:6px;">
        """, unsafe_allow_html=True)

        headers = ["Pos", "Player", "Nationality", "Age", "Value"]
        header_html = "".join([
            f'<div style="font-size:9px;color:#3D5270;text-transform:uppercase;letter-spacing:.06em;">{h}</div>'
            for h in headers
        ])

        roster_rows = [
            ("GK",  "A. McCarthy",       "🏴󠁧󠁢󠁥󠁮󠁧󠁿", 33, "£1.5M"),
            ("RB",  "K. Walker-Peters",  "🏴󠁧󠁢󠁥󠁮󠁧󠁿", 27, "£7M"),
            ("CB",  "J. Harwood-Bellis", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", 22, "£15M"),
            ("CB",  "T. Salisu",         "🇬🇭", 24, "£10M"),
            ("LB",  "R. Manning",        "🇮🇪", 28, "£3.5M"),
            ("CM",  "S. Ugochukwu",      "🇫🇷", 20, "£22M"),
            ("CM",  "C. Lallana",        "🏴󠁧󠁢󠁥󠁮󠁧󠁿", 36, "—"),
            ("CM",  "W. Smallbone",      "🇮🇪", 24, "£6M"),
            ("LW",  "VACANT",            "—",  "—",   "—"),
            ("ST",  "A. Armstrong",      "🏴󠁧󠁢󠁥󠁮󠁧󠁿", 27, "£12M"),
            ("RW",  "S. Cornet",         "🇨🇮", 28, "£4M"),
        ]

        rows_html = header_html + "</div>"
        for pos, player, nat, age, val in roster_rows:
            is_vacant = player == "VACANT"
            row_color = C["amber"] if is_vacant else C["t2"]
            rows_html += f"""
            <div style="display:grid;grid-template-columns:0.5fr 1fr 2fr 1fr 1fr;
              gap:8px;padding:7px 8px;border-bottom:1px solid #192437;transition:all .15s;">
              <span style="font-size:10px;font-weight:700;color:{C['blue']};
                font-family:'DM Sans',sans-serif;">{pos}</span>
              <span style="font-size:11px;font-weight:{'700' if is_vacant else '400'};
                color:{row_color};">{player}</span>
              <span style="font-size:14px;">{nat}</span>
              <span style="font-size:11px;color:#3D5270;">{age}</span>
              <span style="font-size:11px;color:{C['amber']};">{val}</span>
            </div>"""

        st.markdown(f"""
        <div style="background:#09101C;border-radius:7px;overflow:hidden;">
          <div style="display:grid;grid-template-columns:0.5fr 1fr 2fr 1fr 1fr;
            gap:8px;padding:7px 10px;border-bottom:1px solid #192437;">
            {header_html}
          </div>
          {rows_html}
        </div>
        </div>
        """, unsafe_allow_html=True)

    with panel_col:
        _render_budget_panel()
        _render_squad_chemistry()
        _render_agent_analysis()
