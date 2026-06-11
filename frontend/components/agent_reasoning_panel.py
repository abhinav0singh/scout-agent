"""
components/agent_reasoning_panel.py
Reusable agent reasoning and execution timeline components.
Import and call render_agent_reasoning_panel() on any page
that should show live agent traces.
"""

import streamlit as st
from state.session_state import get_live_agent_steps


C_TYPE = {
    "plan":   {"color": "#B87DFF", "label": "PLANNER"},
    "tool":   {"color": "#3B8EFF", "label": "TOOL"},
    "memory": {"color": "#FF8C00", "label": "MEMORY"},
    "output": {"color": "#00E87D", "label": "OUTPUT"},
}

def html(markup: str) -> None:
    """Render raw HTML safely through Streamlit's HTML renderer."""
    st.html(markup)
    
def render_agent_reasoning_panel(
    compact: bool = False,
    title: str = "🧠 Agent Reasoning",
    show_empty_hint: bool = True,
) -> None:
    """
    Renders the agent reasoning / step panel.

    Args:
        compact:          If True, renders a minimal single-column layout.
        title:            Panel title string.
        show_empty_hint:  Show hint text when no steps visible yet.
    """
    steps = get_live_agent_steps()
    agent_running = st.session_state.get("agent_running", False)
    current_step  = st.session_state.get("agent_step", 0)

    visible = (
        steps[:current_step]
        if agent_running and current_step > 0
        else (steps if not agent_running and current_step >= len(steps) else [])
    )

    # Panel wrapper
    border = "1px solid #192437"
    running_border = "1px solid rgba(0,232,125,0.3)" if agent_running else border

    st.markdown(f"""
    <div style="background:#0D1525;border:{running_border};border-radius:10px;padding:14px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
        <div style="font-family:'Syne',sans-serif;font-size:{'11' if compact else '12'}px;
          font-weight:700;color:#E2EDFF;">{title}</div>
        {'<span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;border-radius:4px;padding:1px 6px;font-size:9px;font-weight:700;animation:pulse 1s ease infinite;">LIVE</span>' if agent_running else ''}
      </div>
    """, unsafe_allow_html=True)

    if not visible:
        if show_empty_hint:
            st.markdown("""
            <div style="font-size:11px;color:#3D5270;line-height:1.7;padding:4px 0;">
              Click "⚡ Run Agent" to watch the multi-agent pipeline execute in real time.
              Each step — planning, tool calls, memory retrieval — appears here as it runs.
            </div>
            """, unsafe_allow_html=True)
    else:
        for step in visible:
            cfg   = C_TYPE.get(step["type"], {"color": "#7A92B0", "label": "STEP"})
            color = cfg["color"]
            badge = cfg["label"]
            is_running = step["status"] == "running"
            is_done    = step["status"] == "complete"

            status_glyph = "↻" if is_running else ("✓" if is_done else "○")
            ms_text = f'{step["duration_ms"]}ms' if step["duration_ms"] > 0 else ""
            running_tag = (
                '<span style="font-size:9px;font-weight:700;color:#FF8C00;'
                'animation:pulse 1s ease infinite;">RUNNING</span>'
                if is_running else ""
            )

            output_html = ""
            if is_done and step.get("output"):
                output_html = (
                    f'<div style="margin-top:5px;padding:5px 8px;background:#05080F;'
                    f'border-radius:4px;font-family:JetBrains Mono,monospace;'
                    f'font-size:9px;color:#00E87D;">→ {step["output"]}</div>'
                )

            padding = "8px 10px" if compact else "10px 12px"
            label_size = "10" if compact else "11"
            desc_size  = "9"  if compact else "10"

            st.markdown(f"""
            <div style="display:flex;gap:9px;padding:{padding};background:#09101C;
              border-radius:7px;border-left:3px solid {color};margin-bottom:7px;
              animation:slideIn .3s ease;">
              <div style="font-size:11px;color:{color};flex-shrink:0;padding-top:1px;
                font-weight:700;">{status_glyph}</div>
              <div style="flex:1;min-width:0;">
                <div style="display:flex;justify-content:space-between;
                  align-items:center;margin-bottom:3px;gap:6px;">
                  <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                    <span style="background:{color}18;color:{color};border:1px solid {color}28;
                      border-radius:3px;padding:1px 5px;font-size:9px;font-weight:700;">{badge}</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:{label_size}px;
                      font-weight:600;color:{color};">{step['label']}</span>
                    {running_tag}
                  </div>
                  <span style="font-size:9px;color:#3D5270;flex-shrink:0;">{ms_text}</span>
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:{desc_size}px;
                  color:#3D5270;margin-bottom:3px;opacity:.8;">{step['mono_call']}</div>
                <div style="font-size:{desc_size}px;color:#7A92B0;line-height:1.5;">
                  {step['description']}</div>
                {output_html}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_execution_timeline(steps: list[dict] | None = None) -> None:
    """
    Render a horizontal execution timeline bar.
    Shows each step as a pill — useful as a page sub-header.
    """
    if steps is None:
        steps = get_live_agent_steps()

    agent_running = st.session_state.get("agent_running", False)
    current_step  = st.session_state.get("agent_step", 0)

    pills_html = ""
    for i, step in enumerate(steps):
        cfg     = C_TYPE.get(step["type"], {"color": "#7A92B0", "label": "?"})
        color   = cfg["color"]
        is_done = (not agent_running or i < current_step) and step["status"] == "complete"
        is_run  = agent_running and i == current_step - 1
        opacity = "1" if (is_done or is_run) else "0.35"

        connector = (
            f'<div style="width:20px;height:1px;background:{""+color+"60" if is_done else "#192437"};'
            f'flex-shrink:0;margin-top:10px;"></div>'
            if i < len(steps) - 1 else ""
        )

        pills_html += f"""
        <div style="display:flex;flex-direction:column;align-items:center;
          gap:4px;opacity:{opacity};transition:opacity .3s;">
          <div style="width:20px;height:20px;border-radius:50%;background:{color}18;
            border:1.5px solid {color};display:flex;align-items:center;
            justify-content:center;font-size:9px;color:{color};font-weight:700;">
            {"✓" if is_done else ("↻" if is_run else str(i+1))}</div>
          <div style="font-size:8px;color:#3D5270;text-align:center;
            max-width:50px;line-height:1.3;">{step['label'].split('(')[0][:8]}</div>
        </div>
        {connector}"""

    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:4px;padding:10px 14px;
      background:#0D1525;border:1px solid #192437;border-radius:8px;
      margin-bottom:14px;overflow-x:auto;">
      {pills_html}
    </div>
    """, unsafe_allow_html=True)


def render_agent_status_badge() -> None:
    """
    Inline agent status chip — embed anywhere in a page header.
    """
    running = st.session_state.get("agent_running", False)
    step    = st.session_state.get("agent_step", 0)
    total   = st.session_state.get("agent_total_steps", 7)

    if running:
        st.markdown(f"""
        <span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D30;
          border-radius:20px;padding:5px 14px;font-size:11px;font-weight:700;
          font-family:'DM Sans',sans-serif;animation:subtlePulse 2s ease infinite;">
          ● Agent Running — Step {step}/{total}
        </span>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <span style="background:#3D527018;color:#3D5270;border:1px solid #3D527028;
          border-radius:20px;padding:5px 14px;font-size:11px;font-weight:700;
          font-family:'DM Sans',sans-serif;">
          ○ Agent Standby
        </span>
        """, unsafe_allow_html=True)
