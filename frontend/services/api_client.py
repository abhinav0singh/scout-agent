"""
services/api_client.py
Real API client — mirrors the MockDataService interface exactly.
Swap MockDataService → APIClient throughout the codebase by
changing one import line per page when the backend is ready.

Usage:
    # Current (mock):
    from services.mock_data import MockDataService as DataService

    # Production:
    from services.api_client import APIClient as DataService
"""

from __future__ import annotations
import requests
import streamlit as st
from typing import Any


class APIClient:
    """
    HTTP client for the Scout Agent backend.
    All methods mirror MockDataService signatures exactly.
    """

    # ── Config ────────────────────────────────────────────────
    _BASE_URL: str = "http://localhost:8000"
    _TIMEOUT:  int = 10

    @classmethod
    def _base(cls) -> str:
        return st.session_state.get("settings_api_url", cls._BASE_URL)

    @classmethod
    def _get(cls, path: str, params: dict | None = None) -> Any:
        try:
            r = requests.get(
                f"{cls._base()}{path}",
                params=params,
                timeout=cls._TIMEOUT,
            )
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            st.error(f"API Error: {e}")
            return None

    @classmethod
    def _post(cls, path: str, body: dict) -> Any:
        try:
            r = requests.post(
                f"{cls._base()}{path}",
                json=body,
                timeout=cls._TIMEOUT,
            )
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            st.error(f"API Error: {e}")
            return None

    # ── Players ───────────────────────────────────────────────

    @classmethod
    def get_players(
        cls,
        position:  str = "All",
        max_age:   int = 30,
        max_value: int = 30,
        min_score: int = 70,
        query:     str = "",
    ) -> list[dict[str, Any]]:
        """GET /api/players"""
        params = {
            "position":  position,
            "max_age":   max_age,
            "max_value": max_value,
            "min_score": min_score,
            "q":         query,
        }
        return cls._get("/api/players", params) or []

    @classmethod
    def get_player(cls, player_id: int) -> dict[str, Any] | None:
        """GET /api/players/{id}"""
        return cls._get(f"/api/players/{player_id}")

    # ── Agent ─────────────────────────────────────────────────

    @classmethod
    def get_agent_steps(cls) -> list[dict[str, Any]]:
        """GET /api/agent/steps"""
        return cls._get("/api/agent/steps") or []

    @classmethod
    def start_agent(cls, query: dict) -> dict[str, Any]:
        """POST /api/agent/run — trigger agent pipeline."""
        return cls._post("/api/agent/run", query) or {}

    # ── Memory ────────────────────────────────────────────────

    @classmethod
    def get_memories(cls) -> list[dict[str, Any]]:
        """GET /api/memory"""
        return cls._get("/api/memory") or []

    @classmethod
    def add_memory(cls, entry: dict) -> dict[str, Any]:
        """POST /api/memory — store new memory entry."""
        return cls._post("/api/memory", entry) or {}

    # ── Transfer ──────────────────────────────────────────────

    @classmethod
    def get_transfer_plan_steps(cls) -> list[dict[str, Any]]:
        """GET /api/transfer/plan-steps"""
        return cls._get("/api/transfer/plan-steps") or []

    @classmethod
    def get_transfer_targets(cls) -> list[dict[str, Any]]:
        """GET /api/transfer/targets"""
        return cls._get("/api/transfer/targets") or []

    @classmethod
    def generate_transfer_plan(cls, params: dict) -> dict[str, Any]:
        """POST /api/transfer/generate"""
        return cls._post("/api/transfer/generate", params) or {}

    # ── Squad ─────────────────────────────────────────────────

    @classmethod
    def get_squad_slots(cls, formation: str = "4-3-3") -> list[dict[str, Any]]:
        """GET /api/squad/{formation}"""
        return cls._get(f"/api/squad/{formation.replace('-', '')}") or []

    # ── Dashboard ─────────────────────────────────────────────

    @classmethod
    def get_kpi_summary(cls) -> dict[str, Any]:
        """GET /api/dashboard/kpis"""
        return cls._get("/api/dashboard/kpis") or {}

    @classmethod
    def get_recent_activity(cls) -> list[dict[str, Any]]:
        """GET /api/dashboard/activity"""
        return cls._get("/api/dashboard/activity") or []

    @classmethod
    def get_position_demand(cls) -> list[dict[str, Any]]:
        """GET /api/dashboard/position-demand"""
        return cls._get("/api/dashboard/position-demand") or []

    # ── Compare ───────────────────────────────────────────────

    @classmethod
    def get_radar_comparison(
        cls, player_a_id: int, player_b_id: int
    ) -> dict[str, Any]:
        """GET /api/compare/{a}/{b}"""
        return cls._get(f"/api/compare/{player_a_id}/{player_b_id}") or {}


# ── Backend API Contract Reference ───────────────────────────────
#
# All endpoints return JSON. Standard error envelope:
#   { "error": "message", "code": 4xx|5xx }
#
# ── GET /api/players ──────────────────────────────────────────────
# Query params: position, max_age, max_value, min_score, q
# Response: [ {player_schema} ]
#
# ── GET /api/players/{id} ────────────────────────────────────────
# Response: {player_schema} | 404
#
# ── GET /api/agent/steps ────────────────────────────────────────
# Response: [ {step_schema} ]
#
# ── POST /api/agent/run ─────────────────────────────────────────
# Body:  { club, budget, positions, style, query }
# Response: { run_id, status, steps: [...] }
#
# ── GET /api/memory ─────────────────────────────────────────────
# Response: [ {memory_schema} ]
#
# ── POST /api/memory ────────────────────────────────────────────
# Body:   { type, title, body, club_id }
# Response: { id, created_at }
#
# ── GET /api/transfer/targets ───────────────────────────────────
# Response: [ {target_schema} ]
#
# ── POST /api/transfer/generate ─────────────────────────────────
# Body:   { club, budget, positions, style, urgency }
# Response: { plan_id, steps: [...], targets: [...], budget_split: {} }
#
# ── GET /api/dashboard/kpis ─────────────────────────────────────
# Response: { players_scouted, active_shortlists, budget_tracked, agent_tasks }
#
# ── GET /api/compare/{a}/{b} ────────────────────────────────────
# Response: { player_a, player_b, radar_data, similarity_score }
#
# ── Player Schema ────────────────────────────────────────────────
# { id, name, club, nation, flag, position, age, market_value,
#   market_value_display, league, match_score, similarity_score,
#   shortlisted, season_stats: { goals, assists, appearances,
#   minutes_per_goal, xg, xa, ppda, progressive_passes },
#   radar: { Pace, Finishing, Vision, Pressing, Aerial, Dribbling },
#   tags: [], pros: [], cons: [], agent_reasoning: "" }