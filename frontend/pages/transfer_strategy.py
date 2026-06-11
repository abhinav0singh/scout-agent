"""
pages/transfer_strategy.py
Transfer Strategy — the WOW feature.
Animated multi-agent planning pipeline with ranked transfer targets,
budget allocation, and alternative scenarios.
"""

import time
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

URGENCY_COLOR = {"HIGH": "#FF4545", "MED": "#FF8C00", "LOW": "#00E87D"}
BUDGET_COLOR  = {"PRIMARY": "#00E87D", "VALUE": "#FF8C00", "STRETCH": "#3B8EFF"}
RISK_COLOR    = {"LOW": "#00E87D", "MED": "#FF8C00", "HIGH": "#FF4545"}


# ── Input Panel ───────────────────────────────────────────────────

def _render_input_panel() -> dict:
    """Render the left input form. Returns form values."""
    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
        color:#E2EDFF;margin-bottom:16px;display:flex;align-items:center;gap:8px;">
        ◎ Transfer Parameters
      </div>
    """, unsafe_allow_html=True)

    club = st.text_input("Club", value=st.session_state.get("transfer_club", "FC Southampton"),
                         key="ts_club")
    budget = st.text_input("Budget (€M)", value=st.session_state.get("transfer_budget", "45"),
                           key="ts_budget")
    positions = st.text_input("Positions Needed",
                              value=st.session_state.get("transfer_positions", "LW, ST"),
                              key="ts_positions")
    style = st.selectbox(
        "Tactical Style",
        ["4-3-3 High Press", "4-2-3-1 Possession", "3-4-3 Wing Play", "4-4-2 Counter"],
        key="ts_style"
    )
    urgency = st.selectbox("Urgency", ["High", "Medium", "Low"], key="ts_urgency")

    st.markdown("</div>", unsafe_allow_html=True)

    # Persist to session
    st.session_state.transfer_club      = club
    st.session_state.transfer_budget    = budget
    st.session_state.transfer_positions = positions

    return dict(club=club, budget=budget, positions=positions, style=style, urgency=urgency)


def _render_generate_button() -> bool:
    """Render the generate button. Returns True if clicked."""
    running = st.session_state.get("transfer_running", False)
    label   = "⏳ Generating Plan…" if running else "⚡  Generate Transfer Plan"
    clicked = st.button(label, key="ts_generate", type="primary",
                        use_container_width=True, disabled=running)
    return clicked


# ── Budget Donut ──────────────────────────────────────────────────

def _render_budget_donut() -> None:
    labels  = ["Ferreira (LW)", "Lindqvist (ST)", "Nakashima (CAM)", "Reserve"]
    values  = [15, 12, 8, 10]
    colors  = [C["green"], C["green"], C["amber"], C["b1"]]

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors, line=dict(color=C["s1"], width=2)),
        hole=0.65,
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>€%{value}M<extra></extra>",
    ))
    fig.add_annotation(
        text="€45M", x=0.5, y=0.55, showarrow=False,
        font=dict(size=18, color=C["t1"], family="Syne"),
    )
    fig.add_annotation(
        text="Budget", x=0.5, y=0.42, showarrow=False,
        font=dict(size=10, color=C["t3"], family="DM Sans"),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=180,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Legend
    alloc = [
        ("Ferreira",   "€15M", "PRIMARY"),
        ("Lindqvist",  "€12M", "PRIMARY"),
        ("Nakashima",  "€8M",  "VALUE"),
        ("Reserve",    "€10M", "STRETCH"),
    ]
    for name, val, tier in alloc:
        c = BUDGET_COLOR.get(tier, C["t3"])
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:5px 0;
          border-bottom:1px solid #192437;">
          <div style="display:flex;align-items:center;gap:7px;">
            <div style="width:8px;height:8px;border-radius:50%;background:{c};flex-shrink:0;"></div>
            <span style="font-size:11px;color:#7A92B0;">{name}</span>
          </div>
          <span style="font-size:11px;font-weight:700;color:{c};font-family:'Syne',sans-serif;">{val}</span>
        </div>
        """, unsafe_allow_html=True)


# ── Planning Trace ────────────────────────────────────────────────

def _render_planning_trace(visible_steps: list[int], all_steps: list[dict]) -> None:
    """Render agent planning steps, only those in visible_steps."""
    st.markdown(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
        <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#E2EDFF;
          display:flex;align-items:center;gap:8px;">
          🧠 Agent Planning Trace
        </div>
        {'<span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;">COMPLETE</span>' if len(visible_steps) == len(all_steps) else '<span style="background:#FF8C0018;color:#FF8C00;border:1px solid #FF8C0028;border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;animation:pulse 1s ease infinite;">RUNNING</span>' if visible_steps else ''}
      </div>
    """, unsafe_allow_html=True)

    if not visible_steps:
        st.markdown("""
        <div style="padding:32px 16px;text-align:center;color:#3D5270;font-size:13px;">
          Fill in the parameters and click Generate to watch the agents
          plan your transfer strategy in real time.
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx in visible_steps:
            if idx >= len(all_steps):
                break
            step = all_steps[idx]
            icon = step["icon"]
            agent = step["agent"]
            text  = step["text"]
            is_last = idx == visible_steps[-1]

            st.markdown(f"""
            <div style="display:flex;gap:12px;padding:12px 14px;background:#09101C;
              border-radius:8px;border-left:3px solid #B87DFF;margin-bottom:8px;
              animation:slideIn .35s ease;">
              <div style="font-size:20px;flex-shrink:0;padding-top:2px;">{icon}</div>
              <div>
                <div style="font-size:11px;font-weight:700;color:#B87DFF;
                  font-family:'DM Sans',sans-serif;margin-bottom:5px;">{agent}</div>
                <div style="font-size:12px;color:#7A92B0;line-height:1.65;
                  font-family:'DM Sans',sans-serif;">{text}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── Transfer Targets ──────────────────────────────────────────────

def _render_transfer_targets(targets: list[dict]) -> None:
    """Render ranked transfer target cards."""
    st.markdown(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;margin-top:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
        color:#E2EDFF;margin-bottom:14px;display:flex;align-items:center;gap:8px;">
        📈 Ranked Transfer Targets
        <span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;
          border-radius:4px;padding:2px 7px;font-size:10px;font-weight:700;">
          {len(targets)} targets
        </span>
      </div>
    """, unsafe_allow_html=True)

    for t in targets:
        fit   = t["fit_score"]
        color = C[t["color_key"]]
        urgency_c = URGENCY_COLOR.get(t["urgency"], C["t2"])
        budget_c  = BUDGET_COLOR.get(t["budget_tier"], C["t2"])
        risk_c    = RISK_COLOR.get(t["risk"], C["t2"])

        comp_stars = "⭐" * t.get("competition", 0)
        fit_bar = (
            f'<div style="flex:1;height:5px;background:#192437;border-radius:3px;overflow:hidden;">'
            f'<div style="width:{fit}%;height:100%;background:{color};border-radius:3px;"></div></div>'
        )

        st.markdown(f"""
        <div style="display:flex;gap:14px;padding:14px 16px;background:#09101C;
          border:1px solid #192437;border-radius:10px;margin-bottom:10px;
          border-left:3px solid {color};transition:all .15s;">
          <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
            color:#223449;flex-shrink:0;width:24px;text-align:center;padding-top:4px;">
            #{t['rank']}
          </div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;justify-content:space-between;
              align-items:flex-start;margin-bottom:6px;">
              <div>
                <div style="font-family:'Syne',sans-serif;font-size:15px;
                  font-weight:700;color:#E2EDFF;">{t['name']}</div>
                <div style="font-size:11px;color:#7A92B0;margin-top:2px;">
                  {t['club']} · {t['position']}</div>
              </div>
              <div style="display:flex;gap:5px;align-items:center;flex-shrink:0;flex-wrap:wrap;justify-content:flex-end;">
                <span style="background:{urgency_c}18;color:{urgency_c};
                  border:1px solid {urgency_c}28;border-radius:4px;padding:2px 6px;
                  font-size:9px;font-weight:700;">{t['urgency']}</span>
                <span style="background:{budget_c}18;color:{budget_c};
                  border:1px solid {budget_c}28;border-radius:4px;padding:2px 6px;
                  font-size:9px;font-weight:700;">{t['budget_tier']}</span>
                <span style="background:#FF8C0018;color:#FF8C00;border:1px solid #FF8C0028;
                  border-radius:4px;padding:2px 7px;font-size:11px;font-weight:700;">
                  {t['market_value']}</span>
              </div>
            </div>
            <div style="font-size:11px;color:#7A92B0;line-height:1.6;
              margin-bottom:10px;">{t['reason']}</div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
              {fit_bar}
              <span style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;
                color:{color};flex-shrink:0;">{fit}%</span>
            </div>
            <div style="display:flex;gap:12px;">
              <span style="font-size:10px;color:#3D5270;">Risk:
                <strong style="color:{risk_c};">{t['risk']}</strong></span>
              <span style="font-size:10px;color:#3D5270;">Competition: {comp_stars if comp_stars else '—'}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── Main Render ───────────────────────────────────────────────────

def render_transfer_strategy() -> None:
    """Main Transfer Strategy page renderer."""

    plan_steps  = MockDataService.get_transfer_plan_steps()
    targets     = MockDataService.get_transfer_targets()

    left, right = st.columns([1, 2.4])

    with left:
        form_vals = _render_input_panel()
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        generate_clicked = _render_generate_button()

        # Budget allocation card (show when complete)
        if st.session_state.get("transfer_complete", False):
            st.markdown("""
            <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
              padding:14px;margin-top:14px;">
              <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                color:#E2EDFF;margin-bottom:12px;">Budget Allocation</div>
            """, unsafe_allow_html=True)
            _render_budget_donut()
            st.markdown("</div>", unsafe_allow_html=True)

    with right:
        visible = st.session_state.get("transfer_plan_steps", [])
        complete = st.session_state.get("transfer_complete", False)

        # ── Animate steps on generate click ───────────────
        if generate_clicked:
            st.session_state.transfer_plan_steps = []
            st.session_state.transfer_complete   = False
            st.session_state.transfer_running    = True
            st.session_state.transfer_targets    = []

            # Show steps one by one with delay
            placeholder = st.empty()
            for idx in range(len(plan_steps)):
                st.session_state.transfer_plan_steps = list(range(idx + 1))
                with placeholder.container():
                    _render_planning_trace(st.session_state.transfer_plan_steps, plan_steps)
                time.sleep(0.75)

            st.session_state.transfer_complete = True
            st.session_state.transfer_running  = False
            st.session_state.transfer_targets  = targets
            st.rerun()

        # ── Render current state ───────────────────────────
        _render_planning_trace(visible, plan_steps)

        if complete:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            final_targets = st.session_state.get("transfer_targets", targets)
            _render_transfer_targets(final_targets)

            # Alternative scenarios
            st.markdown("""
            <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
              padding:16px;margin-top:14px;">
              <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                color:#E2EDFF;margin-bottom:12px;">Alternative Scenarios</div>
            """, unsafe_allow_html=True)

            scenarios = [
                {
                    "title": "Loan + Buy Option",
                    "desc": "Loan Nakashima (free) + Ferreira (€15M) — saves €8M for wages",
                    "saving": "€8M saved",
                    "color": C["green"],
                },
                {
                    "title": "Budget Stretch",
                    "desc": "Replace Nakashima with Rafael Costa (€22M). Transformational but risky.",
                    "saving": "+€14M spend",
                    "color": C["amber"],
                },
                {
                    "title": "Youth Pipeline",
                    "desc": "Lindqvist + Bianchi only. Preserve budget for January window.",
                    "saving": "€17M saved",
                    "color": C["blue"],
                },
            ]

            for s in scenarios:
                c = s["color"]
                st.markdown(f"""
                <div style="display:flex;gap:10px;padding:10px 12px;background:#09101C;
                  border-radius:8px;border-left:2px solid {c};margin-bottom:8px;">
                  <div style="flex:1;">
                    <div style="font-size:11px;font-weight:700;color:{c};margin-bottom:4px;">{s['title']}</div>
                    <div style="font-size:11px;color:#7A92B0;">{s['desc']}</div>
                  </div>
                  <div style="font-size:10px;font-weight:700;color:{c};
                    white-space:nowrap;padding-top:2px;">{s['saving']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)