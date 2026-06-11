"""
pages/agent_activity.py
Agent Activity — LangSmith-style execution trace dashboard.
Shows full agent pipeline, tool calls, timing, and outputs.
"""

import streamlit as st
from components.agent_reasoning_panel import html
from state.session_state import get_live_agent_steps

C = {
    "green": "#00E87D",  "amber":  "#FF8C00",
    "blue":  "#3B8EFF",  "purple": "#B87DFF",
    "red":   "#FF4545",
    "t1": "#E2EDFF", "t2": "#7A92B0", "t3": "#3D5270",
    "s1": "#09101C", "s2": "#0D1525", "b1": "#192437",
}

TYPE_COLORS = {"plan": C["purple"], "tool": C["blue"], "memory": C["amber"], "output": C["green"]}
TYPE_LABELS = {"plan": "PLANNER",   "tool": "TOOL",    "memory": "MEMORY",   "output": "OUTPUT"}


def _render_run_header() -> None:
    """Render the trace run meta-info bar."""
    agent_running = st.session_state.get("agent_running", False)
    current_step  = st.session_state.get("agent_step", 0)
    steps = get_live_agent_steps()
    completed = [s for s in steps if s["status"] == "complete"]
    total_ms  = sum(s["duration_ms"] for s in completed)
    tool_count = len([s for s in steps if s["type"] == "tool"])

    import time
    run_id = f"scout-{int(time.time()) % 100000}"

    badge = (
        '<span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;'
        'border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;">LIVE</span>'
        if agent_running else ""
    )

    html(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:14px 16px;margin-bottom:14px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
          color:#E2EDFF;display:flex;align-items:center;gap:8px;">
          ◉ Execution Trace {badge}
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#3D5270;">
          Run ID: {run_id}
        </div>
      </div>
      <div style="display:flex;gap:20px;font-size:11px;color:#3D5270;">
        <span>Total time: <strong style="color:#7A92B0;">{total_ms:,}ms</strong></span>
        <span>Steps: <strong style="color:#7A92B0;">{len(completed)}/{len(steps)}</strong></span>
        <span>Agents: <strong style="color:#7A92B0;">5</strong></span>
        <span>Tool calls: <strong style="color:#7A92B0;">{tool_count}</strong></span>
        <span>Memory reads: <strong style="color:#7A92B0;">1</strong></span>
      </div>
    </div>
    """)


def _render_trace_step(step: dict, idx: int, is_last: bool, agent_running: bool, current_step: int) -> None:
    """Render a single trace step with connector line."""
    color       = TYPE_COLORS.get(step["type"], C["t2"])
    badge_label = TYPE_LABELS.get(step["type"], step["type"].upper())
    is_running  = agent_running and idx == current_step - 1 and step["status"] == "running"
    is_done     = step["status"] == "complete"
    is_pending  = step["status"] == "pending" and not is_running

    if is_running:
        status_icon, status_color = "↻", C["amber"]
    elif is_done:
        status_icon, status_color = "✓", C["green"]
    else:
        status_icon, status_color = "○", C["t3"]

    line_color     = f"{color}40" if is_done else C["b1"]
    running_border = f"{color}50" if is_running else C["b1"]

    # ── Pre-compute conditional HTML fragments ────────────────────
    # Keeps the main f-string clean and avoids the markdown parser
    # misinterpreting inline ternary expressions as markup.

    connector_line = (
        f'<div style="width:1px;flex:1;background:{line_color};'
        f'margin:3px 0;min-height:10px;"></div>'
        if not is_last else ""
    )

    anim_style = "animation:borderPulse 1.5s ease infinite;" if is_running else ""

    output_block = ""
    if is_done and step.get("output"):
        output_block = (
            f'<div style="margin-top:8px;padding:7px 10px;background:#05080F;'
            f'border-radius:5px;border:1px solid #192437;'
            f'font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#00E87D;">'
            f'&#8594; {step["output"]}</div>'
        )

    running_badge = (
        '<span style="background:#FF8C0018;color:#FF8C00;border:1px solid #FF8C0028;'
        'border-radius:4px;padding:1px 5px;font-size:9px;font-weight:700;">RUNNING</span>'
        if is_running else ""
    )
    pending_badge = (
        '<span style="background:#3D527018;color:#3D5270;border:1px solid #3D527028;'
        'border-radius:4px;padding:1px 5px;font-size:9px;font-weight:700;">PENDING</span>'
        if is_pending else ""
    )
    done_time = (
        f'<span style="font-size:10px;color:#3D5270;'
        f'font-family:JetBrains Mono,monospace;">{step["duration_ms"]}ms</span>'
        if is_done and step["duration_ms"] > 0 else ""
    )

    # ── Render via st.html() (through the html() wrapper) ────────
    # Bypasses Streamlit's markdown parser entirely — identical to
    # how _render_run_header() and _render_agent_performance_panel()
    # already work correctly.
    html(f"""
    <div style="display:flex;gap:0;margin-bottom:4px;">
      <div style="width:36px;display:flex;flex-direction:column;align-items:center;flex-shrink:0;">
        <div style="width:24px;height:24px;border-radius:50%;background:{color}18;
          border:1.5px solid {color};display:flex;align-items:center;
          justify-content:center;color:{status_color};font-size:11px;font-weight:700;
          flex-shrink:0;font-family:'Syne',sans-serif;">{status_icon}</div>
        {connector_line}
      </div>
      <div style="flex:1;background:#0D1525;border:1px solid {running_border};
        border-radius:9px;padding:12px 14px;margin-left:8px;margin-bottom:6px;{anim_style}">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:7px;">
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <span style="background:{color}18;color:{color};border:1px solid {color}28;
              border-radius:4px;padding:1px 6px;font-size:9px;font-weight:700;">{badge_label}</span>
            <span style="font-size:13px;font-weight:700;color:#E2EDFF;
              font-family:'DM Sans',sans-serif;">{step['label']}</span>
            {running_badge}{pending_badge}
          </div>
          {done_time}
        </div>
        <div style="padding:7px 10px;background:#09101C;border-radius:5px;margin-bottom:7px;
          font-family:'JetBrains Mono',monospace;font-size:10px;color:{color};">
          {step['mono_call']}
        </div>
        <div style="font-size:12px;color:#7A92B0;line-height:1.6;">{step['description']}</div>
        {output_block}
      </div>
    </div>
    """)


def _render_agent_performance_panel(steps: list[dict]) -> None:
    """Render agent timing and performance side panel."""
    agent_perf = [
        {"name": "Planner",  "time": 210,  "color": C["purple"]},
        {"name": "Scout",    "time": 1240, "color": C["blue"]},
        {"name": "Research", "time": 2450, "color": C["amber"]},
        {"name": "Compare",  "time": 890,  "color": C["green"]},
        {"name": "Report",   "time": 0,    "color": C["t3"]},
    ]
    rows_html = ""
    for a in agent_perf:
        c = a["color"]
        val = f"{a['time']}ms" if a["time"] > 0 else "—"
        rows_html += f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
          padding:7px 0;border-bottom:1px solid #192437;">
          <div style="display:flex;align-items:center;gap:7px;">
            <div style="width:6px;height:6px;border-radius:50%;
              background:{'#192437' if a['time']==0 else c};"></div>
            <span style="font-size:11px;color:#7A92B0;">{a['name']}</span>
          </div>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
            color:{c if a['time'] > 0 else C['t3']};">{val}</span>
        </div>"""

    tool_calls = [s for s in steps if s["type"] == "tool"]
    tools_html = ""
    tool_names = ["player_db", "statsbomb", "ai_model", "transfermarkt", "vectorstore"]
    for name in tool_names:
        tools_html += f"""
        <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #192437;">
          <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#3B8EFF;">{name}</span>
          <span style="font-size:10px;color:#3D5270;">1x</span>
        </div>"""

    html(f"""
    <div style="display:flex;flex-direction:column;gap:12px;">
      <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;">
        <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
          color:#E2EDFF;margin-bottom:12px;">Agent Timing</div>
        {rows_html}
      </div>
      <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;">
        <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
          color:#E2EDFF;margin-bottom:12px;">Tool Calls</div>
        {tools_html}
      </div>
      <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;">
        <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
          color:#E2EDFF;margin-bottom:10px;">Memory Operations</div>
        <div style="padding:9px 11px;background:#09101C;border-radius:7px;
          border-left:2px solid #FF8C00;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;
            color:#FF8C00;margin-bottom:4px;">vectorstore.get()</div>
          <div style="font-size:10px;color:#3D5270;line-height:1.5;">
            Retrieved: southampton_preferences,<br>tactical_history, budget_constraints
          </div>
        </div>
        <div style="margin-top:8px;font-size:10px;color:#3D5270;text-align:center;">
          1 read · 0 writes · 0 errors
        </div>
      </div>
    </div>
    """)


def render_agent_activity() -> None:
    """Main Agent Activity page renderer."""
    steps = get_live_agent_steps()
    agent_running = st.session_state.get("agent_running", False)
    current_step = st.session_state.get("agent_step", 0)

    trace = st.session_state.get("agent_trace", [])

    steps = []

    for t in trace:
        steps.append({
            "label": f"{t['agent']}: {t['action']}",
            "type": (
                "plan"
                if t["agent"] == "Planner"
                else "tool"
                if t["agent"] == "Tool"
                else "output"
            ),
            "status": "complete",
            "description": t["detail"],
            "mono_call": t["action"],
            "duration_ms": 150,
            "output": t["detail"],
        })

    trace_col, panel_col = st.columns([2.8, 1])

    with trace_col:
        _render_run_header()

        if len(steps) == 0:
            st.markdown("""
            <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
              padding:48px 24px;text-align:center;">
              <div style="font-size:32px;margin-bottom:12px;">◉</div>
              <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;
                color:#E2EDFF;margin-bottom:8px;">No Active Traces</div>
              <div style="font-size:12px;color:#3D5270;margin-bottom:20px;">
                Click "⚡ Run Agent" to start the scouting pipeline and watch
                every step execute in real time — just like LangSmith.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            visible_steps = steps
            for i, step in enumerate(visible_steps):
                is_last = (i == len(visible_steps) - 1)
                _render_trace_step(step, i, is_last, agent_running, current_step)

    with panel_col:
        _render_agent_performance_panel(steps)
