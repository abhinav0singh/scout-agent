"""
pages/memory_center.py
Memory Center — visualises the agent's long-term memory store.
Shows club profile, stored preferences, search history,
agent reasoning history, and feedback records.
"""

import streamlit as st
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

COLOR_MAP = {
    "green": C["green"], "amber": C["amber"],
    "blue":  C["blue"],  "purple": C["purple"],
}


def _render_club_profile(club: dict) -> None:
    """Render the club identity card."""
    fields = [
        ("Formation",    club.get("formation",   "4-3-3")),
        ("Press Style",  club.get("press_style", "Gegenpressing")),
        ("Budget",       f"€{club.get('budget', 45)}M summer"),
        ("Avg Buy Age",  str(club.get("avg_buy_age", 23.5))),
        ("Markets",      ", ".join(club.get("markets", ["Primeira Liga"]))),
    ]
    rows_html = "".join([
        f'<div style="display:flex;justify-content:space-between;padding:8px 0;'
        f'border-bottom:1px solid #192437;">'
        f'<span style="font-size:10px;color:#3D5270;">{k}</span>'
        f'<span style="font-size:11px;font-weight:600;color:#E2EDFF;'
        f'font-family:\'DM Sans\',sans-serif;">{v}</span></div>'
        for k, v in fields
    ])
    st.markdown(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px;
        padding-bottom:14px;border-bottom:1px solid #192437;">
        <div style="width:44px;height:44px;background:#00E87D15;border:1px solid #00E87D30;
          border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:22px;">
          ⚽</div>
        <div>
          <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;
            color:#E2EDFF;">{club.get('name', 'FC Southampton')}</div>
          <div style="font-size:11px;color:#7A92B0;margin-top:2px;">
            {club.get('league', 'Premier League')} · St Mary's Stadium</div>
        </div>
      </div>
      {rows_html}
    </div>
    """, unsafe_allow_html=True)


def _render_memory_stats() -> None:
    """Render memory store statistics."""
    stats = [
        ("Stored Preferences", "12", C["blue"]),
        ("Search History",     "34", C["green"]),
        ("Agent Memories",     "48", C["purple"]),
        ("Feedback Records",   "7",  C["amber"]),
    ]
    rows_html = "".join([
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'padding:7px 0;border-bottom:1px solid #192437;">'
        f'<span style="font-size:10px;color:#3D5270;">{label}</span>'
        f'<span style="font-family:\'Syne\',sans-serif;font-size:14px;font-weight:800;'
        f'color:{color};">{val}</span></div>'
        for label, val, color in stats
    ])
    st.markdown(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:14px;margin-top:12px;">
      <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
        color:#E2EDFF;margin-bottom:12px;display:flex;align-items:center;gap:6px;">
        ◈ Vector Store
      </div>
      {rows_html}
      <div style="margin-top:10px;padding:8px 10px;background:#09101C;border-radius:6px;
        border-left:2px solid #00E87D;">
        <div style="font-size:10px;color:#3D5270;margin-bottom:2px;">Embedding Model</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#00E87D;">
          text-embedding-3-small · dim=1536</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def _render_memory_timeline(memories: list[dict]) -> None:
    """Render the main memory card timeline."""
    type_icons = {
        "preference": "⚙️", "budget": "💶",
        "search": "🔍", "feedback": "👍", "market": "🌍",
    }

    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:16px;">
      <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
        color:#E2EDFF;margin-bottom:6px;display:flex;align-items:center;gap:8px;">
        🧠 Agent Memory Store
      </div>
      <div style="font-size:11px;color:#3D5270;margin-bottom:16px;line-height:1.6;">
        Long-term memories retrieved and written during agent execution sessions.
        The vector store is queried at the start of every scouting task to
        personalise results for this club profile.
      </div>
    """, unsafe_allow_html=True)

    for mem in memories:
        color = COLOR_MAP.get(mem["color_key"], C["green"])
        icon  = type_icons.get(mem["type"], "📌")
        badge_label = mem["type"].upper()

        st.markdown(f"""
        <div style="display:flex;gap:12px;padding:14px 16px;background:#09101C;
          border:1px solid #192437;border-radius:10px;margin-bottom:10px;
          border-left:3px solid {color};animation:fadeIn .4s ease;">
          <div style="font-size:20px;flex-shrink:0;padding-top:2px;">{icon}</div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;justify-content:space-between;
              align-items:flex-start;margin-bottom:6px;">
              <span style="font-family:'Syne',sans-serif;font-size:13px;
                font-weight:700;color:#E2EDFF;">{mem['title']}</span>
              <div style="display:flex;gap:6px;align-items:center;flex-shrink:0;">
                <span style="background:{color}18;color:{color};border:1px solid {color}28;
                  border-radius:4px;padding:1px 5px;font-size:9px;font-weight:700;">
                  {badge_label}</span>
                <span style="font-size:10px;color:#3D5270;">{mem['created_ago']}</span>
              </div>
            </div>
            <div style="font-size:12px;color:#7A92B0;line-height:1.65;
              font-family:'DM Sans',sans-serif;">{mem['body']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_reasoning_history() -> None:
    """Render agent reasoning history — Q&A style."""
    entries = [
        {
            "q": "Why was Ferreira ranked #1 in the LW search?",
            "a": (
                "Pace (93) and dribbling (92) create a near-perfect match for the "
                "Salah-type profile required. Primeira Liga form is validated across "
                "two seasons. Club memory confirmed Braga as a priority pipeline. "
                "Fit score 96.2 — highest in the database across 147 candidates."
            ),
            "time": "3 days ago",
            "confidence": 97,
        },
        {
            "q": "Why are players over 27 excluded from recommendations?",
            "a": (
                "Club preference logged during Q1 manager briefing: all targets must "
                "have resale value within 4-year contract window. Board directive: "
                "under-25 preferred, 26-27 acceptable with quality ceiling. Over-27 "
                "only if on free transfer or loan."
            ),
            "time": "1 week ago",
            "confidence": 94,
        },
        {
            "q": "Why is J1 League flagged as an emerging pipeline?",
            "a": (
                "Nakashima profile revealed J1 League has undervalued technically "
                "gifted midfielders. PPDA metrics in J1 top division comparable to "
                "Bundesliga 2. Market values 40-60% below equivalent European "
                "profiles. Memory updated to track 3 additional J1 prospects."
            ),
            "time": "2 weeks ago",
            "confidence": 88,
        },
    ]

    st.markdown("""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:16px;margin-top:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
        color:#E2EDFF;margin-bottom:14px;">Reasoning History</div>
    """, unsafe_allow_html=True)

    for entry in entries:
        conf_color = C["green"] if entry["confidence"] >= 90 else C["amber"]
        st.markdown(f"""
        <div style="padding:13px 15px;background:#09101C;border-radius:9px;
          margin-bottom:10px;border-left:2px solid #B87DFF;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;
            margin-bottom:8px;">
            <div style="font-size:11px;font-weight:600;color:#B87DFF;
              flex:1;line-height:1.5;">Q: {entry['q']}</div>
            <div style="display:flex;gap:6px;align-items:center;margin-left:10px;flex-shrink:0;">
              <span style="font-size:9px;color:{conf_color};font-weight:700;">
                {entry['confidence']}% conf.</span>
              <span style="font-size:9px;color:#3D5270;">{entry['time']}</span>
            </div>
          </div>
          <div style="font-size:11px;color:#7A92B0;line-height:1.7;">A: {entry['a']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_search_history() -> None:
    """Render recent search history table."""
    searches = [
        {"query": "LW · Bundesliga · U25 · ≤€18M",    "results": 3,  "date": "3d ago",  "converted": 1},
        {"query": "ST · Allsvenskan · U26 · ≤€15M",    "results": 7,  "date": "5d ago",  "converted": 1},
        {"query": "CAM · J1 League · U23 · ≤€12M",     "results": 4,  "date": "1w ago",  "converted": 0},
        {"query": "DM · Ekstraklasa · U28 · ≤€10M",    "results": 9,  "date": "2w ago",  "converted": 1},
        {"query": "CB · Serie B · U24 · ≤€8M",          "results": 12, "date": "3w ago",  "converted": 0},
    ]

    rows_html = ""
    for s in searches:
        conv_color = C["green"] if s["converted"] else C["t3"]
        conv_label = "✓ Shortlisted" if s["converted"] else "No action"
        rows_html += f"""
        <div style="display:grid;grid-template-columns:2fr 0.5fr 0.5fr 1fr;
          gap:8px;align-items:center;padding:8px 10px;border-bottom:1px solid #192437;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
            color:#7A92B0;">{s['query']}</div>
          <div style="text-align:center;font-family:'Syne',sans-serif;font-size:13px;
            font-weight:700;color:#E2EDFF;">{s['results']}</div>
          <div style="text-align:center;font-size:10px;color:#3D5270;">{s['date']}</div>
          <div style="font-size:10px;color:{conv_color};">{conv_label}</div>
        </div>"""

    html(f"""
    <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;
      padding:16px;margin-top:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
        color:#E2EDFF;margin-bottom:12px;">Search History</div>
      <div style="display:grid;grid-template-columns:2fr 0.5fr 0.5fr 1fr;
        gap:8px;padding:6px 10px;margin-bottom:4px;">
        {''.join([f"<div style='font-size:9px;color:#3D5270;text-transform:uppercase;letter-spacing:.06em;'>{h}</div>" for h in ['Query','Results','Date','Action']])}
      </div>
      {rows_html}
    </div>
    """)


def render_memory_center() -> None:
    """Main Memory Center page renderer."""
    memories = MockDataService.get_memories()
    club     = st.session_state.get("club_profile", {})

    left_col, main_col = st.columns([1, 2.5])

    with left_col:
        _render_club_profile(club)
        _render_memory_stats()

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Memory retrieval demo
        st.markdown("""
        <div style="background:#0D1525;border:1px solid #192437;border-radius:10px;padding:14px;">
          <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
            color:#E2EDFF;margin-bottom:12px;">Last Retrieval</div>
          <div style="padding:9px 11px;background:#09101C;border-radius:7px;
            border-left:2px solid #FF8C00;margin-bottom:8px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
              font-weight:600;color:#FF8C00;margin-bottom:3px;">vectorstore.similarity_search()</div>
            <div style="font-size:10px;color:#3D5270;line-height:1.5;">
              query: "LW high press budget 20M"<br>
              top_k: 5 · threshold: 0.82<br>
              latency: 43ms
            </div>
          </div>
          <div style="font-size:10px;color:#3D5270;">
            Returned: tactical_system, budget_constraints, pipeline_markets
          </div>
        </div>
        """, unsafe_allow_html=True)

    with main_col:
        tab1, tab2, tab3 = st.tabs(["🧠 Memory Store", "🔍 Search History", "💬 Reasoning"])

        with tab1:
            _render_memory_timeline(memories)

        with tab2:
            _render_search_history()

        with tab3:
            _render_reasoning_history()
