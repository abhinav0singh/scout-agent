"""
state/session_state.py
Centralised session state schema and initialisation.
All keys live here — import this before any page renders.
"""

import streamlit as st
from typing import Any
import time
from services.mock_data import MockDataService


# ── Default Values ────────────────────────────────────────────────
DEFAULTS: dict[str, Any] = {
    # Navigation
    "active_page": "home",

    # Agent execution state
    "agent_running":       False,
    "agent_step":          0,
    "agent_total_steps":   7,
    "agent_steps_visible": [],   # list of step indices revealed so far
    "agent_log":           [],   # list of log string messages
    "agent_next_update_at": 0.0,
    "agent_step_interval_sec": 0.8,

    # Scout page
    "scout_query":           "",
    "scout_pos_filter":      "All",
    "scout_max_age":         30,
    "scout_max_value":       30,
    "scout_min_score":       75,
    "scout_results":         [],
    "scout_selected_player": None,

    # Shortlist  (list of player dicts)
    "shortlist": [],

    # Compare page
    "compare_player_a": None,
    "compare_player_b": None,

    # Transfer Strategy
    "transfer_club":       "FC Southampton",
    "transfer_budget":     "45",
    "transfer_positions":  "LW, ST",
    "transfer_style":      "4-3-3 High Press",
    "transfer_urgency":    "High",
    "transfer_plan_steps": [],    # list of revealed step indices
    "transfer_targets":    [],    # final ranked list
    "transfer_running":    False,
    "transfer_complete":   False,

    # Squad Builder
    "squad_formation": "4-3-3",
    "squad_slots":     {},        # {position: player_name}
    "squad_budget_spent": 68,     # €M

    # Memory Center
    "memory_entries":   [],       # loaded from mock / backend
    "reasoning_history": [],

    # Club profile
    "club_profile": {
        "name":       "FC Southampton",
        "league":     "Premier League",
        "formation":  "4-3-3",
        "budget":     45,
        "press_style": "Gegenpressing",
        "avg_buy_age": 23.5,
        "markets":    ["Primeira Liga", "Allsvenskan", "J1 League"],
    },

    # Settings
    "settings_api_url":    "http://localhost:8000",
    "settings_use_mock":   True,
    "settings_theme":      "dark",
    "settings_show_traces": True,
}


def init_session_state() -> None:
    """
    Idempotently initialise every session state key.
    Call once at the top of app.py before any rendering.
    """
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default

    # Populate compare defaults from mock data on first load
    if st.session_state.compare_player_a is None:
        try:
            players = MockDataService.get_players()
            if len(players) >= 2:
                st.session_state.compare_player_a = players[2]  # Bruno Ferreira
                st.session_state.compare_player_b = players[0]  # Marcus Lindqvist
        except Exception:
            pass

    # Seed shortlist with one player
    if not st.session_state.shortlist:
        try:
            players = MockDataService.get_players()
            shortlisted = [p for p in players if p.get("shortlisted", False)]
            st.session_state.shortlist = shortlisted
        except Exception:
            pass


# ── Helpers ───────────────────────────────────────────────────────

def set_page(page_id: str) -> None:
    """Navigate to a page and trigger rerun."""
    st.session_state.active_page = page_id
    st.rerun()


def toggle_shortlist(player: dict) -> None:
    """Add or remove a player from the shortlist."""
    existing_ids = [p["id"] for p in st.session_state.shortlist]
    if player["id"] in existing_ids:
        st.session_state.shortlist = [
            p for p in st.session_state.shortlist if p["id"] != player["id"]
        ]
        player["shortlisted"] = False
    else:
        player["shortlisted"] = True
        st.session_state.shortlist.append(player)


def is_shortlisted(player_id: int) -> bool:
    return any(p["id"] == player_id for p in st.session_state.shortlist)


def set_compare(player: dict, slot: str = "a") -> None:
    """Set player A or B for the compare page."""
    if slot == "a":
        st.session_state.compare_player_a = player
    else:
        st.session_state.compare_player_b = player


def start_agent() -> None:
    """Reset and start agent execution."""
    total_steps = len(MockDataService.get_agent_steps())
    st.session_state.agent_running = True
    st.session_state.agent_step = 0
    st.session_state.agent_total_steps = total_steps
    st.session_state.agent_steps_visible = []
    st.session_state.agent_log = []
    st.session_state.agent_next_update_at = time.time() + st.session_state.agent_step_interval_sec


def advance_agent_step() -> None:
    """Move agent to the next step."""
    st.session_state.agent_step += 1
    if st.session_state.agent_step >= st.session_state.agent_total_steps:
        st.session_state.agent_running = False
        st.session_state.agent_step = st.session_state.agent_total_steps
        st.session_state.agent_next_update_at = 0.0
    else:
        st.session_state.agent_next_update_at = time.time() + st.session_state.agent_step_interval_sec


def tick_agent_progress() -> None:
    """Advance the agent run when its next scheduled tick is due."""
    if not st.session_state.get("agent_running", False):
        return

    if time.time() < st.session_state.get("agent_next_update_at", 0.0):
        return

    advance_agent_step()


def get_live_agent_steps():
    """
    Return real planner trace if available,
    otherwise fall back to mock steps.
    """

    result = st.session_state.get("last_agent_result")

    if result and result.get("trace"):

        steps = []

        for i, t in enumerate(result["trace"]):

            agent = t.get("agent", "")
            action = t.get("action", "")
            detail = t.get("detail", "")

            if agent == "Planner":
                step_type = "plan"
            elif agent == "Tool":
                step_type = "tool"
            else:
                step_type = "output"

            steps.append({
                "type": step_type,
                "label": f"{agent}: {action}",
                "description": detail,
                "mono_call": action,
                "status": "complete",
                "duration_ms": 100 + (i * 50),
                "output": detail[:100]
            })

        return steps

    # fallback to original mock behaviour

    steps = MockDataService.get_agent_steps()

    current_step = st.session_state.get("agent_step", 0)
    total_steps = len(steps)
    agent_running = st.session_state.get("agent_running", False)

    live_steps = []

    for idx, step in enumerate(steps):
        live_step = step.copy()

        if agent_running:
            if idx < current_step - 1:
                live_step["status"] = "complete"
            elif idx == current_step - 1:
                live_step["status"] = "running"
            else:
                live_step["status"] = "pending"
        elif current_step >= total_steps:
            live_step["status"] = "complete"
        else:
            live_step["status"] = "pending"

        live_steps.append(live_step)

    return live_steps


def get_agent_progress_pct() -> float:
    if st.session_state.agent_total_steps == 0:
        return 0.0
    return st.session_state.agent_step / st.session_state.agent_total_steps
