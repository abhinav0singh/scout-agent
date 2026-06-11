"""
pages/scout.py
Scout page — professional player search interface with
filter panel, player grid, and live agent reasoning panel.
"""

import streamlit as st
from services.backend_adapter import BackendAdapter
from state.session_state import toggle_shortlist, is_shortlisted, set_compare, get_live_agent_steps
from components.agent_reasoning_panel import html

C = {
    "green":  "#00E87D", "amber":  "#FF8C00",
    "blue":   "#3B8EFF", "purple": "#B87DFF",
    "red":    "#FF4545",
    "t1": "#E2EDFF", "t2": "#7A92B0", "t3": "#3D5270",
    "s1": "#09101C", "s2": "#0D1525", "s3": "#12192E",
    "b1": "#192437",  "b2": "#223449",
}


# ── Helpers ───────────────────────────────────────────────────────

def _badge(label: str, color: str, size: str = "sm") -> str:
    fs = "9px" if size == "xs" else "10px"
    return (
        f'<span style="background:{color}18;color:{color};border:1px solid {color}28;'
        f'border-radius:4px;padding:2px 7px;font-size:{fs};font-weight:700;'
        f'letter-spacing:.05em;text-transform:uppercase;">{label}</span>'
    )


def _mini_bar(val: int, color: str) -> str:
    """Compact vertical bar for radar preview."""
    return (
        f'<div style="flex:1;text-align:center;">'
        f'<div style="height:28px;background:#09101C;border-radius:3px;'
        f'margin-bottom:3px;display:flex;align-items:flex-end;overflow:hidden;">'
        f'<div style="width:100%;height:{val}%;background:{color}{"" if val > 85 else "80"};'
        f'border-radius:2px 2px 0 0;"></div></div>'
        f'</div>'
    )


def _score_color(score: int) -> str:
    if score >= 92:
        return C["green"]
    elif score >= 85:
        return C["amber"]
    return C["t2"]


# ── Filter Panel ──────────────────────────────────────────────────

def _render_filter_panel() -> tuple[str, str, int, int, int]:
    """Render filter sidebar. Returns (query, position, max_age, max_value, min_score)."""
    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;margin-bottom:12px;">
      <div style="font-size:11px;font-weight:700;color:#E2EDFF;
        font-family:'Syne',sans-serif;margin-bottom:14px;
        display:flex;align-items:center;gap:6px;">
        ⊟ Filters
      </div>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "Search", placeholder="Name, club, league…",
        key="scout_search_input", label_visibility="collapsed"
    )

    positions = ["All", "ST", "LW", "RW", "CAM", "CM", "DM", "CB", "RB", "LB"]
    pos_filter = st.selectbox("Position", positions, key="scout_pos_select")

    max_age = st.slider("Max Age", 18, 35, 28, key="scout_age_slider")
    max_val = st.slider("Max Value (€M)", 1, 50, 25, key="scout_val_slider")
    min_score = st.slider("Min Match Score", 70, 99, 80, key="scout_score_slider")

    st.markdown("</div>", unsafe_allow_html=True)
    return query, pos_filter, max_age, max_val, min_score


# ── Agent Reasoning Panel ─────────────────────────────────────────

def _render_agent_panel() -> None:
    """Render live agent reasoning panel alongside search results."""
    agent_running = st.session_state.get("agent_running", False)
    current_step  = st.session_state.get("agent_step", 0)
    steps = get_live_agent_steps()

    type_colors = {
        "plan": C["purple"], "tool": C["blue"],
        "memory": C["amber"], "output": C["green"],
    }

    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:14px;height:100%;">
      <div style="font-size:11px;font-weight:700;color:#E2EDFF;
        font-family:'Syne',sans-serif;margin-bottom:12px;
        display:flex;align-items:center;gap:7px;">
        🧠 Agent Reasoning
      </div>
    """, unsafe_allow_html=True)

    if not agent_running and current_step == 0:
        st.markdown("""
        <div style="font-size:11px;color:#3D5270;line-height:1.7;padding:8px 0;">
          Run the agent to see live reasoning traces. The agent will decompose
          your query, search the player database, analyse tactical fit, and
          validate market values — all visible here in real time.
        </div>
        """, unsafe_allow_html=True)
    else:
        visible = steps[:current_step] if agent_running else steps
        for step in visible:
            color = type_colors.get(step["type"], C["t2"])
            is_running = step["status"] == "running"
            st.markdown(f"""
            <div style="display:flex;gap:10px;padding:9px 11px;background:#09101C;
              border-radius:7px;border-left:3px solid {color};margin-bottom:7px;
              animation:slideIn .3s ease;">
              <div style="font-size:10px;color:{color};padding-top:1px;flex-shrink:0;">
                {'↻' if is_running else '✓' if step['status']=='complete' else '○'}
              </div>
              <div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                  font-weight:600;color:{color};margin-bottom:3px;">{step['label']}</div>
                <div style="font-size:10px;color:#3D5270;font-family:'JetBrains Mono',monospace;
                  margin-bottom:4px;opacity:.8;">{step['mono_call']}</div>
                <div style="font-size:10px;color:#7A92B0;">{step['description']}</div>
                {f'<div style="margin-top:5px;font-family:JetBrains Mono,monospace;font-size:9px;color:#00E87D;background:#05080F;padding:5px 7px;border-radius:4px;">→ {step["output"]}</div>' if step.get("output") else ''}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── Player Card ───────────────────────────────────────────────────

def _render_player_card(player: dict, col_key: str) -> None:
    """Render a single player card with actions."""
    score = player["match_score"]
    sc = _score_color(score)
    shortlisted = is_shortlisted(player["id"])

    # Radar mini bars
    radar_html = '<div style="display:flex;gap:4px;margin-bottom:10px;">'
    for attr, val in player["radar"].items():
        bar_color = C["green"] if val >= 85 else C["blue"] if val >= 75 else C["t3"]
        radar_html += _mini_bar(val, bar_color)
    radar_html += "</div>"

    # Attribute labels
    attr_labels = '<div style="display:flex;gap:4px;margin-bottom:12px;">'
    for attr in player["radar"].keys():
        attr_labels += f'<div style="flex:1;text-align:center;font-size:7px;color:#3D5270;text-transform:uppercase;">{attr[:3]}</div>'
    attr_labels += "</div>"

    tags_html = " ".join([
        f'<span style="background:{C["blue"]}18;color:{C["blue"]};border:1px solid {C["blue"]}28;'
        f'border-radius:4px;padding:1px 5px;font-size:9px;font-weight:700;">{t}</span>'
        for t in player["tags"]
    ])

    shortlist_btn_key = f"sl_{player['id']}_{col_key}"
    compare_btn_key   = f"cmp_{player['id']}_{col_key}"

    card_bg = C["s3"] if shortlisted else C["s2"]
    card_border = C["green"] if shortlisted else C["b1"]

    st.markdown(f"""
    <div style="background:{card_bg};border:1px solid {card_border};border-radius:10px;
      padding:14px;transition:all .18s;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
        <div style="display:flex;gap:10px;align-items:center;">
          <div style="width:36px;height:36px;border-radius:8px;background:{sc}15;
            border:1px solid {sc}30;display:flex;align-items:center;
            justify-content:center;font-size:18px;">{player['flag']}</div>
          <div>
            <div style="font-size:13px;font-weight:700;color:#E2EDFF;
              font-family:'Syne',sans-serif;">{player['name']}</div>
            <div style="font-size:10px;color:#7A92B0;margin-top:2px;">
              {player['club']} · {player['league']}</div>
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:'Syne',sans-serif;font-size:22px;
            font-weight:800;color:{sc};line-height:1;">{score}</div>
          <div style="font-size:9px;color:#3D5270;text-transform:uppercase;
            letter-spacing:.06em;">MATCH</div>
        </div>
      </div>
      <div style="display:flex;gap:5px;margin-bottom:12px;flex-wrap:wrap;">
        {_badge(player['position'], C['blue'], 'xs')}
        {_badge('Age ' + str(player['age']), C['t3'], 'xs')}
        {_badge(player['market_value_display'], C['amber'], 'xs')}
        {'<span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;border-radius:4px;padding:1px 5px;font-size:9px;font-weight:700;">✓ LISTED</span>' if shortlisted else ''}
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;
        padding:10px 0;border-top:1px solid #192437;border-bottom:1px solid #192437;margin-bottom:12px;">
        {''.join([f'<div style="text-align:center;"><div style="font-family:Syne,sans-serif;font-size:16px;font-weight:700;color:#E2EDFF;">{v}</div><div style="font-size:9px;color:#3D5270;text-transform:uppercase;">{k}</div></div>' for k, v in [('Goals', player['season_stats']['goals']), ('Assists', player['season_stats']['assists']), ('Apps', player['season_stats']['appearances']), ('xG+xA', round(player['season_stats']['xg'] + player['season_stats']['xa'], 1))]])}
      </div>
      {radar_html}
      {attr_labels}
      <div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:12px;">{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)

    sl_label = "✓ Shortlisted" if shortlisted else "+ Shortlist"

    if st.button(
        sl_label,
        key=shortlist_btn_key,
        use_container_width=True
    ):
        toggle_shortlist(player)
        st.rerun()

    if st.button(
        "⇌ Compare",
        key=compare_btn_key,
        use_container_width=True
    ):
        set_compare(player, "a")
        st.session_state.active_page = "compare"
        st.rerun()

    if st.button(
        "👁 View",
        key=f"view_{player['id']}_{col_key}",
        use_container_width=True
    ):
        st.session_state.scout_selected_player = player


# ── Selected Player Detail ────────────────────────────────────────

def _render_player_detail(player: dict) -> None:
    """Render expanded player detail panel."""
    score = player["match_score"]
    sc = _score_color(score)

    st.markdown(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="display:flex;gap:12px;align-items:center;margin-bottom:16px;
        padding-bottom:14px;border-bottom:1px solid #192437;">
        <div style="font-size:28px;">{player['flag']}</div>
        <div style="flex:1;">
          <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;
            color:#E2EDFF;">{player['name']}</div>
          <div style="font-size:11px;color:#7A92B0;">{player['club']} · {player['league']}</div>
        </div>
        <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:{sc};">{score}</div>
      </div>
      <div style="font-size:10px;color:#3D5270;text-transform:uppercase;
        letter-spacing:.07em;margin-bottom:8px;">Agent Reasoning</div>
      <div style="font-size:11px;color:#7A92B0;line-height:1.7;padding:10px 12px;
        background:#09101C;border-radius:7px;border-left:3px solid {C['purple']};margin-bottom:14px;">
        {player['agent_reasoning']}
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
        <div>
          <div style="font-size:10px;color:#00E87D;font-weight:700;text-transform:uppercase;
            letter-spacing:.06em;margin-bottom:8px;">Strengths</div>
          {''.join([f"<div style='display:flex;gap:6px;margin-bottom:5px;'><span style='color:#00E87D;font-size:11px;flex-shrink:0;'>✓</span><span style='font-size:11px;color:#7A92B0;'>{p}</span></div>" for p in player['pros']])}
        </div>
        <div>
          <div style="font-size:10px;color:#FF4545;font-weight:700;text-transform:uppercase;
            letter-spacing:.06em;margin-bottom:8px;">Concerns</div>
          {''.join([f"<div style='display:flex;gap:6px;margin-bottom:5px;'><span style='color:#FF4545;font-size:11px;flex-shrink:0;'>✗</span><span style='font-size:11px;color:#7A92B0;'>{c}</span></div>" for c in player['cons']])}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✕ Close", key="close_detail"):
        st.session_state.scout_selected_player = None
        st.rerun()


# ── Main Render ───────────────────────────────────────────────────

def render_scout() -> None:
    """Main Scout page renderer."""

    # ── Layout: filters | grid | agent reasoning ──────────────
    left, main, right = st.columns([1, 3.2, 1.4])

    with left:
        query, pos_filter, max_age, max_val, min_score = _render_filter_panel()

        # Agent reasoning in left panel
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        _render_agent_panel()

    with main:
        # ── Search bar ─────────────────────────────────────
        search_col, count_col = st.columns([5, 1])
        with search_col:
            live_query = st.text_input(
                "Search players",
                value=query,
                placeholder="Search by name, club, league, position…",
                key="scout_main_search",
                label_visibility="collapsed",
            )
        # Merge both search inputs
        final_query = live_query or query

        # ── Fetch & filter ─────────────────────────────────
        players = BackendAdapter.search_players(
            position=pos_filter,
            max_age=max_age,
            max_value=max_val,
            min_score=min_score,
            query=final_query,
        )

        with count_col:
            st.markdown(f"""
            <div style="background:#0D1525;border:1px solid #192437;border-radius:8px;
              padding:8px 12px;text-align:center;margin-top:2px;">
              <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;
                color:#00E87D;">{len(players)}</div>
              <div style="font-size:9px;color:#3D5270;text-transform:uppercase;">Results</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── Player grid (2 columns) ─────────────────────────
        if not players:
            st.markdown("""
            <div style="text-align:center;padding:48px 16px;color:#3D5270;font-size:14px;">
              No players match your current filters. Try relaxing the criteria.
            </div>
            """, unsafe_allow_html=True)
        else:
            for i in range(0, len(players), 2):
                card_cols = st.columns(2)
                for j, col in enumerate(card_cols):
                    if i + j < len(players):
                        with col:
                            _render_player_card(players[i + j], f"r{i}c{j}")
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    with right:
        # ── Selected Player Detail ──────────────────────────
        selected = st.session_state.get("scout_selected_player")
        if selected:
            _render_player_detail(selected)
        else:
            # ── Shortlist summary ───────────────────────────
            shortlist = st.session_state.get("shortlist", [])
            st.markdown(f"""
            <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;">
              <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                color:#E2EDFF;margin-bottom:12px;display:flex;justify-content:space-between;">
                <span>Shortlist</span>
                <span style="background:#00E87D18;color:#00E87D;border:1px solid #00E87D28;
                  border-radius:4px;padding:1px 6px;font-size:10px;font-weight:700;">
                  {len(shortlist)}</span>
              </div>
            """, unsafe_allow_html=True)

            if not shortlist:
                st.markdown("""
                <div style="font-size:11px;color:#3D5270;text-align:center;padding:16px 0;">
                  No players shortlisted yet
                </div>
                """, unsafe_allow_html=True)
            else:
                for p in shortlist:
                    sc = _score_color(p["match_score"])
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:8px 0;
                      border-bottom:1px solid #192437;">
                      <span style="font-size:14px;">{p['flag']}</span>
                      <div style="flex:1;">
                        <div style="font-size:11px;font-weight:600;color:#E2EDFF;">{p['name']}</div>
                        <div style="font-size:9px;color:#3D5270;">{p['position']} · {p['market_value_display']}</div>
                      </div>
                      <span style="font-family:'Syne',sans-serif;font-size:13px;
                        font-weight:800;color:{sc};">{p['match_score']}</span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
