"""
pages/dashboard.py
Dashboard - at-a-glance overview with live agent activity,
recent scout results, and position demand chart.
"""

import streamlit as st
import plotly.graph_objects as go
from services.mock_data import MockDataService
from state.session_state import set_page
from state.session_state import get_live_agent_steps
from components.agent_reasoning_panel import html

COLOR = {
    "green": "#00E87D", "amber": "#FF8C00",
    "blue": "#3B8EFF", "purple": "#B87DFF",
    "red": "#FF4545", "muted": "#3D5270",
    "t1": "#E2EDFF", "t2": "#7A92B0", "t3": "#3D5270",
    "s1": "#09101C", "s2": "#0D1525", "b1": "#192437",
}


def _render_kpi_row(kpis: dict) -> None:
    cols = st.columns(4)
    labels = {
        "players_scouted": "Players Scouted",
        "active_shortlists": "Active Shortlists",
        "budget_tracked": "Budget Tracked",
        "agent_tasks": "Agent Tasks",
    }
    for col, (key, data) in zip(cols, kpis.items()):
        c = COLOR[data["color"]]
        with col:
            html(f"""
            <div style="background:#0D1525;border:1px solid #192437;
              border-top:2px solid {c};border-radius:10px;padding:16px;">
              <div style="font-size:10px;color:#3D5270;text-transform:uppercase;
                letter-spacing:.07em;margin-bottom:10px;">{labels[key]}</div>
              <div style="font-family:'Syne',sans-serif;font-size:30px;
                font-weight:800;color:#E2EDFF;line-height:1;">{data['value']}</div>
              <div style="font-size:11px;color:#7A92B0;margin-top:5px;">{data['delta']}</div>
            </div>
            """)


def _render_activity_feed(activity: list[dict]) -> None:
    color_map = {"green": "#00E87D", "blue": "#3B8EFF", "amber": "#FF8C00", "purple": "#B87DFF"}
    items_html = ""
    for item in activity:
        c = color_map.get(item["color"], "#3B8EFF")
        items_html += f"""
        <div style="display:flex;gap:10px;padding:8px 10px;background:#09101C;
          border-radius:7px;border-left:2px solid {c};margin-bottom:6px;">
          <span style="font-size:9px;color:#3D5270;white-space:nowrap;
            padding-top:1px;min-width:48px;">{item['time']}</span>
          <span style="font-size:11px;color:#7A92B0;line-height:1.5;">{item['text']}</span>
        </div>"""
    html(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
        <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#E2EDFF;">
          Agent Activity
        </div>
        <span style="font-size:11px;color:#00E87D;text-decoration:none;">Full Traces ↗</span>
      </div>
      {items_html}
    </div>
    """)

    if st.button("→ Agent Activity", key="dash_to_agent", use_container_width=True):
        set_page("agent")


def _render_recent_scouts(players: list[dict]) -> None:
    rows_html = ""
    for p in players[:5]:
        score = p["match_score"]
        score_color = COLOR["green"] if score >= 92 else COLOR["amber"] if score >= 85 else COLOR["t2"]
        rows_html += f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
          padding:9px 8px;border-radius:7px;margin-bottom:2px;transition:all .15s;">
          <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:18px;">{p['flag']}</span>
            <div>
              <div style="font-size:12px;font-weight:600;color:#E2EDFF;
                font-family:'DM Sans',sans-serif;">{p['name']}</div>
              <div style="font-size:10px;color:#3D5270;">{p['position']} · {p['club']}</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:10px;">
            <span style="background:#FF8C0018;color:#FF8C00;border:1px solid #FF8C0028;
              border-radius:4px;padding:2px 6px;font-size:10px;font-weight:700;">
              {p['market_value_display']}</span>
            <span style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;
              color:{score_color};">{score}</span>
          </div>
        </div>"""

    html(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
        color:#E2EDFF;margin-bottom:14px;">Recent Scout Results</div>
      {rows_html}
    </div>
    """)

    if st.button("→ Full Scout", key="dash_to_scout", use_container_width=True):
        set_page("scout")


def _render_position_demand(demand: list[dict]) -> None:
    positions = [d["position"] for d in demand]
    priorities = [d["priority"] for d in demand]
    colors = [COLOR["green"] if p >= 6 else COLOR["blue"] if p >= 4 else COLOR["muted"] for p in priorities]

    fig = go.Figure(go.Bar(
        x=priorities, y=positions,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[str(v) for v in priorities],
        textposition="outside",
        textfont=dict(color=COLOR["t2"], size=10),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=24, t=0, b=0),
        height=200,
        xaxis=dict(visible=False, range=[0, 12]),
        yaxis=dict(
            tickfont=dict(color=COLOR["t2"], size=11, family="DM Sans"),
            gridcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
    )

    html("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
        color:#E2EDFF;margin-bottom:10px;">Position Priority</div>
    """)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    html("</div>")


def _render_transfer_alerts() -> None:
    alerts = [
        {"text": "Nakashima contract expires Jun 2025 — window is closing fast", "color": "amber"},
        {"text": "Ferreira — PL club interest flagged — pre-window approach critical", "color": "red"},
    ]
    alerts_html = ""
    for a in alerts:
        c = COLOR[a["color"]]
        alerts_html += f"""
        <div style="display:flex;gap:7px;padding:8px 10px;background:#09101C;
          border-radius:7px;border-left:2px solid {c};margin-bottom:7px;">
          <span style="color:{c};font-size:12px;flex-shrink:0;">⚠</span>
          <span style="font-size:10px;color:#7A92B0;">{a['text']}</span>
        </div>"""
    html(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;margin-top:12px;">
      <div style="font-size:10px;color:#3D5270;text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px;">
        Transfer Alerts
      </div>
      {alerts_html}
    </div>
    """)


def _render_agent_execution_panel() -> None:
    steps = get_live_agent_steps()
    agent_running = st.session_state.get("agent_running", False)
    current_step = st.session_state.get("agent_step", 0)

    type_colors = {"plan": "#B87DFF", "tool": "#3B8EFF", "memory": "#FF8C00", "output": "#00E87D"}
    type_labels = {"plan": "PLANNER", "tool": "TOOL", "memory": "MEMORY", "output": "OUTPUT"}

    steps_html = ""
    for i, step in enumerate(steps):
        is_visible = not agent_running or i < current_step
        if not is_visible:
            continue

        color = type_colors.get(step["type"], "#7A92B0")
        badge_label = type_labels.get(step["type"], step["type"].upper())
        is_running = agent_running and i == current_step - 1 and step["status"] == "running"
        is_done = step["status"] == "complete"
        status_icon = "✓" if is_done else ("…" if is_running else "○")
        mono_output = ""
        if is_done and step.get("output"):
            mono_output = f"""
            <div style="margin-top:6px;padding:6px 8px;background:#05080F;border-radius:4px;
              border:1px solid #192437;font-family:'JetBrains Mono',monospace;
              font-size:10px;color:#00E87D;">→ {step['output']}</div>"""

        steps_html += f"""
        <div style="display:flex;gap:10px;padding:10px 12px;background:#09101C;border-radius:8px;
          border-left:3px solid {color};margin-bottom:7px;">
          <div style="padding-top:1px;font-size:12px;color:{color};flex-shrink:0;">{status_icon}</div>
          <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
              <div style="display:flex;align-items:center;gap:7px;">
                <span style="background:{color}18;color:{color};border:1px solid {color}28;
                  border-radius:4px;padding:1px 5px;font-size:9px;font-weight:700;">{badge_label}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
                  font-weight:600;color:{color};">{step['label']}</span>
              </div>
              {f"<span style='font-size:9px;color:#3D5270;'>{step['duration_ms']}ms</span>" if step['duration_ms'] > 0 else ""}
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
              color:#3D5270;margin-bottom:4px;opacity:.8;">{step['mono_call']}</div>
            <div style="font-size:11px;color:#7A92B0;">{step['description']}</div>
            {mono_output}
          </div>
        </div>"""

    html(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
        <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#E2EDFF;">
          Live Agent Execution
        </div>
        {'<span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;">RUNNING</span>' if agent_running else ''}
      </div>
      <div style="font-size:11px;color:#3D5270;margin-bottom:14px;">
        Click "⚡ Run Agent" in the top bar to watch the scouting pipeline execute
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        {steps_html if steps_html else '<div style="color:#3D5270;font-size:12px;padding:16px;text-align:center;">No steps visible yet — run the agent</div>'}
      </div>
    </div>
    """)


def render_dashboard() -> None:
    kpis = MockDataService.get_kpi_summary()
    activity = MockDataService.get_recent_activity()
    players = MockDataService.get_players()
    demand = MockDataService.get_position_demand()

    _render_kpi_row(kpis)
    html("<div style='height:6px'></div>")

    col_scouts, col_activity, col_right = st.columns([2, 2, 1.4])
    with col_scouts:
        _render_recent_scouts(players)
    with col_activity:
        _render_activity_feed(activity)
    with col_right:
        _render_position_demand(demand)
        _render_transfer_alerts()

    html("<div style='height:6px'></div>")
    _render_agent_execution_panel()
