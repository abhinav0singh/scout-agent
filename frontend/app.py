"""
ScoutAgent Pro — Main Application Entry Point
Professional multi-agent football scouting platform.
"""

import streamlit as st
from pathlib import Path
import sys
import time
from services.backend_adapter import BackendAdapter
# ── Global HTML safety patch ──────────────────────────────────────
# Ensures every st.markdown() call containing HTML tags always has
# unsafe_allow_html=True — fixes raw-string rendering across all pages
# without requiring changes to individual page files.
_orig_md = st.markdown
def _md(body, *args, **kwargs):
    if isinstance(body, str) and "<" in body:
        kwargs.setdefault("unsafe_allow_html", True)
    return _orig_md(body, *args, **kwargs)
st.markdown = _md
# ─────────────────────────────────────────────────────────────────

# ── Path Setup ────────────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from state.session_state import init_session_state, start_agent, tick_agent_progress

# ── Page Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="ScoutAgent Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": "ScoutAgent Pro v1.0"}
)


def load_css() -> None:
    """Inject the dark analytics CSS theme."""
    css_path = ROOT / "styles" / "styles.css"
    if css_path.exists():
        st.html(css_path)
    else:
        st.warning("⚠️ styles/styles.css not found. Run with full project structure.")


def render_sidebar() -> str:
    """Render the sidebar navigation and return the active page key."""
    with st.sidebar:
        # ── Brand ──────────────────────────────────────────────
        st.markdown("""
        <div class="brand-block">
            <div class="brand-icon">🛡️</div>
            <div>
                <div class="brand-name">SCOUT AGENT</div>
                <div class="brand-sub">Pro Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='sidebar-hr'>", unsafe_allow_html=True)

        # ── Agent Status Strip ──────────────────────────────────
        agent_active = st.session_state.get("agent_running", False)
        status_class = "agent-active" if agent_active else "agent-idle"
        status_label = "● AGENT ACTIVE" if agent_active else "○ STANDBY"
        step = st.session_state.get("agent_step", 0)
        total = st.session_state.get("agent_total_steps", 7)
        st.markdown(f"""
        <div class="agent-status-strip {status_class}">
            <span>{status_label}</span>
            {"<span class='step-counter'>" + str(step) + "/" + str(total) + "</span>" if agent_active else ""}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── Navigation ──────────────────────────────────────────
        nav_items = [
            ("home",       "⌂",  "Home"),
            ("dashboard",  "⊞",  "Dashboard"),
            ("scout",      "⌕",  "Scout"),
            ("compare",    "⇌",  "Compare"),
            ("transfer",   "◎",  "Transfer Strategy"),
            ("squad",      "⋮",  "Squad Builder"),
            ("shortlists", "☆",  "Shortlists"),
            ("memory",     "◈",  "Memory Center"),
            ("agent",      "◉",  "Agent Activity"),
            ("settings",   "⚙",  "Settings"),
        ]

        current = st.session_state.get("active_page", "home")

        for page_id, icon, label in nav_items:
            active_class = "nav-active" if current == page_id else ""
            shortlist_badge = ""
            if page_id == "scout":
                sl_count = len(st.session_state.get("shortlist", []))
                if sl_count > 0:
                    shortlist_badge = f"<span class='nav-badge'>{sl_count}</span>"
            if page_id == "agent" and agent_active:
                shortlist_badge = "<span class='nav-live-dot'></span>"

            clicked = st.button(
                f"{icon}  {label}",
                key=f"nav_{page_id}",
                use_container_width=True,
            )
            if clicked:
                st.session_state.active_page = page_id
                st.rerun()

        st.markdown("<hr class='sidebar-hr'>", unsafe_allow_html=True)

        # ── Club Profile ────────────────────────────────────────
        club = st.session_state.get("club_profile", {})
        st.markdown(f"""
        <div class="club-profile">
            <div class="club-avatar">S</div>
            <div>
                <div class="club-name">{club.get('name', 'FC Southampton')}</div>
                <div class="club-league">{club.get('league', 'Premier League')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.get("active_page", "dashboard")


def render_topbar(page_id: str) -> None:
    """Render the persistent top action bar."""
    titles = {
        "dashboard": "Dashboard",
        "scout": "Player Scout",
        "compare": "Player Comparison",
        "transfer": "Transfer Strategy",
        "squad": "Squad Builder",
        "shortlists": "Shortlists",
        "memory": "Memory Center",
        "agent": "Agent Activity",
        "settings": "Settings",
    }
    title = titles.get(page_id, page_id.title())
    agent_running = st.session_state.get("agent_running", False)
    step = st.session_state.get("agent_step", 0)
    total = st.session_state.get("agent_total_steps", 7)

    col_title, col_query, col_status, col_btn, col_agents = st.columns([3, 4, 2, 1.5, 2])

    with col_title:
        st.markdown(f"<h2 class='page-title'>{title}</h2>", unsafe_allow_html=True)

    with col_query:
        st.text_input(
            "Ask agent",
            key="agent_query",
            placeholder="Find a young Brazilian striker under €20M",
            label_visibility="collapsed",
        )

    with col_status:
        if agent_running:
            st.markdown(f"""
            <div class='topbar-agent-pill running'>
                <span class='pulse-dot'></span>
                Agent Running — Step {step}/{total}
            </div>
            """, unsafe_allow_html=True)

    with col_btn:
        if st.button("⚡ Run Agent", key="run_agent_topbar", type="primary", use_container_width=True):
            query = st.session_state.get("agent_query", "").strip()

            if not query:
                st.session_state.last_agent_result = {
                    "response": "Type a question first.",
                    "trace": [],
                    "tool_calls": [],
                    "agent_outputs": {"gathered_data": []},
                    "players": [],
                }
                st.rerun()

            result = BackendAdapter.ask_agent(query, "demo_user")
            st.session_state.last_agent_result = result
            st.session_state.agent_trace = result.get("trace", [])
            st.rerun()

    with col_agents:
        active_agents = ["Planner", "Scout"] if agent_running else []
        dots_html = " ".join([
            f"<span class='agent-dot {'dot-active' if a in active_agents else 'dot-idle'}'>{a[0]}</span>"
            for a in ["Planner", "Scout", "Research", "Compare", "Report"]
        ])
        st.markdown(f"<div class='agent-dots-row'>{dots_html}</div>", unsafe_allow_html=True)

    st.markdown("<div class='topbar-divider'></div>", unsafe_allow_html=True)


def route_page(page_id: str) -> None:
    """Route to the appropriate page module."""
    if page_id == "home":
        from pages.landing import render_home
        render_home()

    elif page_id == "dashboard":
        from pages.dashboard import render_dashboard
        render_dashboard()

    elif page_id == "scout":
        from pages.scout import render_scout
        render_scout()

    elif page_id == "compare":
        from pages.compare import render_compare
        render_compare()

    elif page_id == "transfer":
        from pages.transfer_strategy import render_transfer_strategy
        render_transfer_strategy()

    elif page_id == "squad":
        from pages.squad_builder import render_squad_builder
        render_squad_builder()

    elif page_id == "shortlists":
        from pages.shortlists import render_shortlists
        render_shortlists()

    elif page_id == "memory":
        from pages.memory_center import render_memory_center
        render_memory_center()

    elif page_id == "agent":
        from pages.agent_activity import render_agent_activity
        render_agent_activity()

    elif page_id == "settings":
        from pages.settings import render_settings
        render_settings()

    else:
        st.error(f"Unknown page: {page_id}")


def main() -> None:
    """Application entry point."""
    # ── Initialize ─────────────────────────────────────────────
    init_session_state()
    tick_agent_progress()
    load_css()

    # ── Layout ─────────────────────────────────────────────────
    active_page = render_sidebar()
    render_topbar(active_page)
    route_page(active_page)

    if st.session_state.get("agent_running", False):
        time.sleep(0.2)
        st.rerun()


if __name__ == "__main__":
    main()
