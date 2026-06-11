"""
services/mock_data.py
Complete mock data service.
Mirrors the exact JSON schemas the real backend will serve.
Swap MockDataService → APIClient when backend is ready.
"""

from __future__ import annotations
from typing import Any


# ═══════════════════════════════════════════════════════════════════
# PLAYER DATA
# Schema: { id, name, club, nation_flag, position, age, market_value,
#           league, match_score, season_stats, radar, tags,
#           pros, cons, shortlisted, similarity_score }
# ═══════════════════════════════════════════════════════════════════
_PLAYERS: list[dict[str, Any]] = [
    {
        "id": 1,
        "name": "Marcus Lindqvist",
        "club": "Malmö FF",
        "nation": "Sweden",
        "flag": "🇸🇪",
        "position": "ST",
        "age": 23,
        "market_value": 12,
        "market_value_display": "€12M",
        "league": "Allsvenskan",
        "match_score": 94,
        "similarity_score": 91,
        "shortlisted": False,
        "season_stats": {
            "goals": 18, "assists": 7, "appearances": 28,
            "minutes_per_goal": 117, "xg": 15.2, "xa": 5.8,
            "ppda": 8.7, "progressive_passes": 42,
        },
        "radar": {
            "Pace": 87, "Finishing": 84, "Vision": 71,
            "Pressing": 79, "Aerial": 82, "Dribbling": 76,
        },
        "tags": ["High Press", "Clinical", "Aerial Threat"],
        "pros": [
            "Clinical finishing with 18 goals in 28 apps",
            "Elite aerial threat — 72% duel win rate",
            "High-press compatible (PPDA 8.7)",
            "Strong market value with resale upside",
        ],
        "cons": [
            "Limited top-5 league exposure",
            "Distribution below average (4.2 key passes/90)",
            "Relatively small sample size",
        ],
        "agent_reasoning": (
            "Lindqvist profiles as a reliable target striker with an excellent "
            "pressing contribution. His PPDA of 8.7 ranks in the top 12% of "
            "forwards across tracked leagues, making him an ideal 4-3-3 press fit. "
            "Market value is significantly below comparable profiles — strong ROI."
        ),
    },
    {
        "id": 2,
        "name": "Kai Nakashima",
        "club": "Urawa Red Diamonds",
        "nation": "Japan",
        "flag": "🇯🇵",
        "position": "CAM",
        "age": 21,
        "market_value": 8,
        "market_value_display": "€8M",
        "league": "J1 League",
        "match_score": 88,
        "similarity_score": 84,
        "shortlisted": False,
        "season_stats": {
            "goals": 9, "assists": 14, "appearances": 30,
            "minutes_per_goal": 212, "xg": 7.1, "xa": 11.4,
            "ppda": 7.9, "progressive_passes": 98,
        },
        "radar": {
            "Pace": 79, "Finishing": 68, "Vision": 91,
            "Pressing": 86, "Aerial": 62, "Dribbling": 89,
        },
        "tags": ["Creative", "Link Play", "Pressing"],
        "pros": [
            "World-class vision (91 rating, top 3% across database)",
            "Elite progressive passing (98 per season)",
            "High press output — PPDA 7.9",
            "Exceptional budget value at €8M",
        ],
        "cons": [
            "Low aerial threat — 38% duel success",
            "Physical adaptation to Premier League needed",
            "Low finishing (xG outpacing goals by 1.9)",
        ],
        "agent_reasoning": (
            "Nakashima's contract expires June 2025 — represent a rare "
            "opportunity to acquire a genuinely elite creative midfielder "
            "at a fraction of market value. Vision metrics place him in "
            "the top 3% of tracked CAMs. Press metrics compatible with 4-3-3."
        ),
    },
    {
        "id": 3,
        "name": "Bruno Ferreira",
        "club": "SC Braga",
        "nation": "Portugal",
        "flag": "🇵🇹",
        "position": "LW",
        "age": 24,
        "market_value": 15,
        "market_value_display": "€15M",
        "league": "Primeira Liga",
        "match_score": 96,
        "similarity_score": 96,
        "shortlisted": True,
        "season_stats": {
            "goals": 12, "assists": 11, "appearances": 32,
            "minutes_per_goal": 162, "xg": 10.8, "xa": 9.4,
            "ppda": 9.1, "progressive_passes": 61,
        },
        "radar": {
            "Pace": 93, "Finishing": 77, "Vision": 80,
            "Pressing": 74, "Aerial": 66, "Dribbling": 92,
        },
        "tags": ["Elite Pace", "Creative", "Direct"],
        "pros": [
            "Elite pace (93) matches Salah replacement profile exactly",
            "Creative dribbler — 4.2 successful dribbles/90",
            "Excellent cross output (2.8 key passes/90)",
            "Proven Primeira Liga form — tracked pipeline",
        ],
        "cons": [
            "Defensive engagement below average for pressing system",
            "Can over-dribble in tight spaces",
            "PL club competition may drive price up",
        ],
        "agent_reasoning": (
            "Ferreira is the standout recommendation. Pace + dribbling profile "
            "is a near-perfect Salah archetype. Braga are willing sellers at "
            "€15M. Club memory confirms Primeira Liga as a priority pipeline. "
            "Act before the window opens publicly — interest from two PL clubs flagged."
        ),
    },
    {
        "id": 4,
        "name": "Luca Bianchi",
        "club": "Atalanta U23",
        "nation": "Italy",
        "flag": "🇮🇹",
        "position": "CB",
        "age": 22,
        "market_value": 5,
        "market_value_display": "€5M",
        "league": "Serie B",
        "match_score": 82,
        "similarity_score": 78,
        "shortlisted": False,
        "season_stats": {
            "goals": 2, "assists": 1, "appearances": 29,
            "minutes_per_goal": 0, "xg": 1.4, "xa": 0.8,
            "ppda": 8.4, "progressive_passes": 54,
        },
        "radar": {
            "Pace": 78, "Finishing": 44, "Vision": 73,
            "Pressing": 84, "Aerial": 90, "Dribbling": 62,
        },
        "tags": ["Ball-Playing CB", "Aerial", "Commanding"],
        "pros": [
            "Outstanding aerial duels — 81% success rate",
            "Ball-playing CB — 54 progressive passes per season",
            "High ceiling prospect from Atalanta academy",
            "Exceptional value at €5M with resale potential",
        ],
        "cons": [
            "No top-flight experience",
            "Slow in transition — pace (78) a concern",
            "Leadership and positioning still developing",
        ],
        "agent_reasoning": (
            "Bianchi is a depth/backup recommendation with high upside. "
            "Atalanta academy pedigree is a strong signal. Aerial metrics "
            "are elite. At €5M, risk is low. Recommended as squad CB to "
            "address the depth concern flagged in squad analysis."
        ),
    },
    {
        "id": 5,
        "name": "Rafael Costa",
        "club": "Flamengo",
        "nation": "Brazil",
        "flag": "🇧🇷",
        "position": "CAM",
        "age": 25,
        "market_value": 22,
        "market_value_display": "€22M",
        "league": "Série A",
        "match_score": 97,
        "similarity_score": 88,
        "shortlisted": False,
        "season_stats": {
            "goals": 15, "assists": 18, "appearances": 34,
            "minutes_per_goal": 140, "xg": 13.2, "xa": 15.4,
            "ppda": 8.2, "progressive_passes": 112,
        },
        "radar": {
            "Pace": 84, "Finishing": 82, "Vision": 94,
            "Pressing": 77, "Aerial": 71, "Dribbling": 92,
        },
        "tags": ["World Class", "Goal Contributions", "Leadership"],
        "pros": [
            "World-class creativity — vision ranks top 1% globally",
            "33 G+A in 34 appearances — elite output",
            "Leadership presence and experience",
            "Série A's best midfielder two seasons running",
        ],
        "cons": [
            "Highest price point — requires wage budget adjustment",
            "European adaptation risk",
            "Wages significant (est. £140k/week)",
        ],
        "agent_reasoning": (
            "Costa is a transformational signing. Output metrics are exceptional. "
            "The risk is purely financial and adaptation. Requires stretching the "
            "budget to €22M + significant wages. Only recommend if Nakashima "
            "or cheaper alternatives are unavailable. High ceiling, high risk."
        ),
    },
    {
        "id": 6,
        "name": "Arjan Kowalski",
        "club": "Legia Warsaw",
        "nation": "Poland",
        "flag": "🇵🇱",
        "position": "DM",
        "age": 26,
        "market_value": 7,
        "market_value_display": "€7M",
        "league": "Ekstraklasa",
        "match_score": 85,
        "similarity_score": 80,
        "shortlisted": False,
        "season_stats": {
            "goals": 3, "assists": 5, "appearances": 31,
            "minutes_per_goal": 0, "xg": 2.1, "xa": 4.2,
            "ppda": 6.8, "progressive_passes": 67,
        },
        "radar": {
            "Pace": 74, "Finishing": 52, "Vision": 80,
            "Pressing": 92, "Aerial": 79, "Dribbling": 70,
        },
        "tags": ["Ball Winner", "Press Leader", "Composed"],
        "pros": [
            "Elite pressing metrics — PPDA 6.8 (top 5% of DMs)",
            "Ball recovery specialist — 8.4 recoveries/90",
            "Composed under pressure with good range of passing",
            "Under-market value at €7M",
        ],
        "cons": [
            "League quality concerns — Ekstraklasa step up required",
            "Limited attacking upside for modern DM role",
            "Minor injury history (2 muscular issues last season)",
        ],
        "agent_reasoning": (
            "Kowalski profiles as a high-press DM specialist. PPDA of 6.8 is "
            "exceptional and would slot seamlessly into the 4-3-3 system. "
            "League step is the key risk — recommend a loan arrangement first. "
            "Represents the best value option in the DM position group."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════
# AGENT STEPS
# Schema: { id, type, label, mono_call, description,
#           duration_ms, status }
# status: "complete" | "running" | "pending"
# type:   "plan" | "tool" | "memory" | "output"
# ═══════════════════════════════════════════════════════════════════
_AGENT_STEPS: list[dict[str, Any]] = [
    {
        "id": 1,
        "type": "plan",
        "label": "Planner Agent",
        "mono_call": "plan_scouting_task(query, club_context)",
        "description": (
            "Decomposing scouting request into 4 subtasks: "
            "search → stats fetch → tactical analysis → market validation. "
            "Routing to Scout Agent + Research Agent in parallel."
        ),
        "duration_ms": 210,
        "status": "complete",
        "output": '{"subtasks": 4, "agents_assigned": ["scout", "research"]}',
    },
    {
        "id": 2,
        "type": "tool",
        "label": "search_players()",
        "mono_call": 'db.query({pos:"ST,LW,CAM", maxAge:26, maxVal:"25M", minScore:80})',
        "description": (
            "Queried player database across 18 tracked leagues. "
            "Found 147 candidates matching filter criteria."
        ),
        "duration_ms": 1240,
        "status": "complete",
        "output": '{"count": 147, "top_score": 96, "leagues": 18}',
    },
    {
        "id": 3,
        "type": "tool",
        "label": "get_season_stats()",
        "mono_call": "statsbomb.fetch(player_ids=[...147], season=2024, metrics='all')",
        "description": (
            "Fetching xG, xA, PPDA, progressive passes, aerial duel %, "
            "dribbles per 90 for all 147 candidates from StatsBomb API."
        ),
        "duration_ms": 890,
        "status": "complete",
        "output": '{"fetched": 147, "errors": 0, "coverage": "100%"}',
    },
    {
        "id": 4,
        "type": "tool",
        "label": "analyze_tactical_fit()",
        "mono_call": "model.score(system='4-3-3', press_intensity=9.2, width='high')",
        "description": (
            "Running tactical compatibility matrix. Scoring each candidate on "
            "press fit, width contribution, transition speed, and positional discipline."
        ),
        "duration_ms": 1560,
        "status": "complete",
        "output": '{"scored": 20, "top": "ferreira_96.2", "avg_fit": 71.4}',
    },
    {
        "id": 5,
        "type": "tool",
        "label": "check_market_values()",
        "mono_call": "transfermarkt.validate(candidates=20, budget=45_000_000)",
        "description": (
            "Validating transfer fees against €45M budget. "
            "Checking auction risk, contract expiry dates, and competing interest."
        ),
        "duration_ms": 0,
        "status": "running",
        "output": None,
    },
    {
        "id": 6,
        "type": "memory",
        "label": "retrieve_club_memory()",
        "mono_call": "vectorstore.get('southampton_preferences', top_k=10)",
        "description": (
            "Loading FC Southampton tactical profile, previous search history, "
            "manager feedback, and budget constraints from memory store."
        ),
        "duration_ms": 0,
        "status": "pending",
        "output": None,
    },
    {
        "id": 7,
        "type": "output",
        "label": "generate_report()",
        "mono_call": "reporter.compile(ranked_list, reasoning=True, format='structured')",
        "description": (
            "Compiling final shortlist with reasoning chains, "
            "confidence scores, and transfer strategy recommendations."
        ),
        "duration_ms": 0,
        "status": "pending",
        "output": None,
    },
]


# ═══════════════════════════════════════════════════════════════════
# MEMORY ENTRIES
# Schema: { id, type, icon, title, body, color_key, created_ago }
# type: "preference" | "budget" | "search" | "feedback" | "market"
# ═══════════════════════════════════════════════════════════════════
_MEMORIES: list[dict[str, Any]] = [
    {
        "id": 1, "type": "preference", "icon": "⚙️",
        "title": "Tactical System",
        "body": (
            "4-3-3 high press preferred. Target PPDA < 9.5. "
            "Width critical — full-backs must support transitions. "
            "Avoid players who cannot contribute to the press."
        ),
        "color_key": "blue",
        "created_ago": "2 days ago",
    },
    {
        "id": 2, "type": "budget", "icon": "💶",
        "title": "Transfer Budget Constraints",
        "body": (
            "Summer window: €45M total. Individual cap: €20M. "
            "Wages max +£90k/week. Loan fallback acceptable for CB depth. "
            "Board expects 2 signings minimum."
        ),
        "color_key": "amber",
        "created_ago": "1 week ago",
    },
    {
        "id": 3, "type": "search", "icon": "🔍",
        "title": "LW Search — Bundesliga / Eredivisie",
        "body": (
            "Searched: LW, U25, Bundesliga + Eredivisie, max €18M. "
            "3 candidates shortlisted. Ferreira (Braga) preferred over shortlist. "
            "Bundesliga options too expensive (>€25M)."
        ),
        "color_key": "green",
        "created_ago": "3 days ago",
    },
    {
        "id": 4, "type": "feedback", "icon": "👍",
        "title": "Agent Recommendation — Approved",
        "body": (
            "User approved Lindqvist recommendation. "
            "Press metrics (PPDA 8.7) confirmed as key signal for future ST searches. "
            "Aerial ability flagged as secondary filter."
        ),
        "color_key": "purple",
        "created_ago": "1 day ago",
    },
    {
        "id": 5, "type": "market", "icon": "🌍",
        "title": "Pipeline Markets — Updated",
        "body": (
            "Primeira Liga & Allsvenskan tracked as undervalued pipelines. "
            "J1 League emerging — Nakashima flagged. "
            "Serie B (Atalanta loans) flagged as depth source."
        ),
        "color_key": "green",
        "created_ago": "2 weeks ago",
    },
]


# ═══════════════════════════════════════════════════════════════════
# TRANSFER PLAN STEPS (animated planning sequence)
# ═══════════════════════════════════════════════════════════════════
_TRANSFER_PLAN_STEPS: list[dict[str, Any]] = [
    {
        "icon": "🧠", "agent": "Planner Agent",
        "text": (
            "Analysing FC Southampton's 4-3-3 system and Salah-type profile "
            "requirements: pace > 88, dribbling > 82, xG+xA > 0.55/90, "
            "press contribution top quartile."
        ),
    },
    {
        "icon": "🔍", "agent": "Scout Agent",
        "text": (
            "Searching 50,000+ players across 24 tracked leagues. "
            "Applying filters: LW/RW, age 20–27, market value ≤ €25M, "
            "PPDA contribution top 30%, minimum 20 appearances."
        ),
    },
    {
        "icon": "📊", "agent": "Research Agent",
        "text": (
            "Running similarity models vs. Salah's 2021–22 positional heatmap. "
            "Comparing 23 shortlisted candidates on 47 tactical metrics. "
            "Ferreira scores 96.2 — highest in database."
        ),
    },
    {
        "icon": "💰", "agent": "Market Agent",
        "text": (
            "Validating fees: Ferreira (SC Braga) — €15M. Market trending +8% YoY. "
            "Window opens in 22 days. Competition flagged from Crystal Palace and Brentford. "
            "Recommend pre-window approach."
        ),
    },
    {
        "icon": "🗄️", "agent": "Memory Agent",
        "text": (
            "Retrieved: Club prefers Primeira Liga pipeline (confirmed 3 searches). "
            "Ferreira flagged 3 days ago as 'watch closely'. "
            "Press compatibility score aligns with manager preference logged Jan 2025."
        ),
    },
    {
        "icon": "✅", "agent": "Report Agent",
        "text": (
            "Transfer plan compiled. 4 ranked targets identified. "
            "Budget allocation: €35M primary spend (Ferreira + Lindqvist), "
            "€8M value option (Nakashima), €2M reserve. Full report ready."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════
# TRANSFER TARGETS
# ═══════════════════════════════════════════════════════════════════
_TRANSFER_TARGETS: list[dict[str, Any]] = [
    {
        "rank": 1, "name": "Bruno Ferreira", "club": "SC Braga", "position": "LW",
        "market_value": "€15M", "fit_score": 96, "urgency": "HIGH",
        "budget_tier": "PRIMARY", "color_key": "green",
        "reason": (
            "Elite pace (93) + dribbling (92). Near-perfect Salah replacement profile. "
            "In-club pipeline (Primeira Liga). Braga open to sell. Pre-window approach recommended."
        ),
        "risk": "LOW", "competition": 2,
    },
    {
        "rank": 2, "name": "Marcus Lindqvist", "club": "Malmö FF", "position": "ST",
        "market_value": "€12M", "fit_score": 91, "urgency": "MED",
        "budget_tier": "PRIMARY", "color_key": "green",
        "reason": (
            "Clinical finisher. Aerial threat. Under-market value. "
            "Could fill ST void and cover LW in transitional system. Strong ROI."
        ),
        "risk": "LOW", "competition": 0,
    },
    {
        "rank": 3, "name": "Kai Nakashima", "club": "Urawa Red Diamonds", "position": "CAM",
        "market_value": "€8M", "fit_score": 88, "urgency": "HIGH",
        "budget_tier": "VALUE", "color_key": "amber",
        "reason": (
            "Contract expires June 2025. Vision elite (top 3%). Budget upside significant. "
            "Press metrics excellent. Must move before contract expiry triggers wage inflation."
        ),
        "risk": "MED", "competition": 1,
    },
    {
        "rank": 4, "name": "Rafael Costa", "club": "Flamengo", "position": "CAM",
        "market_value": "€22M", "fit_score": 84, "urgency": "LOW",
        "budget_tier": "STRETCH", "color_key": "blue",
        "reason": (
            "World-class talent but requires significant wage budget reallocation. "
            "Série A form unmatched. Transformational if budget can flex. High ceiling, high risk."
        ),
        "risk": "HIGH", "competition": 3,
    },
]


# ═══════════════════════════════════════════════════════════════════
# SQUAD FORMATION DATA
# ═══════════════════════════════════════════════════════════════════
_SQUAD_433: list[dict[str, Any]] = [
    {"row": 0, "col": 4, "position": "GK",  "player": "A. McCarthy",        "filled": True},
    {"row": 1, "col": 1, "position": "LB",  "player": "R. Manning",          "filled": True},
    {"row": 1, "col": 3, "position": "LCB", "player": "J. Harwood-Bellis",   "filled": True},
    {"row": 1, "col": 5, "position": "RCB", "player": "T. Salisu",           "filled": True},
    {"row": 1, "col": 7, "position": "RB",  "player": "K. Walker-Peters",    "filled": True},
    {"row": 2, "col": 2, "position": "LCM", "player": "C. Lallana",          "filled": True},
    {"row": 2, "col": 4, "position": "CM",  "player": "S. Ugochukwu",        "filled": True},
    {"row": 2, "col": 6, "position": "RCM", "player": "W. Smallbone",        "filled": True},
    {"row": 3, "col": 1, "position": "LW",  "player": "VACANCY",             "filled": False},
    {"row": 3, "col": 4, "position": "ST",  "player": "A. Armstrong",        "filled": True},
    {"row": 3, "col": 7, "position": "RW",  "player": "S. Cornet",           "filled": True},
]


# ═══════════════════════════════════════════════════════════════════
# MOCK DATA SERVICE
# ═══════════════════════════════════════════════════════════════════
class MockDataService:
    """
    Provides mock data that mirrors exact backend API responses.
    Replace method bodies with real API calls when backend is ready.
    """

    @staticmethod
    def get_players(
        position: str = "All",
        max_age: int = 30,
        max_value: int = 30,
        min_score: int = 70,
        query: str = "",
    ) -> list[dict[str, Any]]:
        """GET /api/players — filtered player list."""
        players = [p.copy() for p in _PLAYERS]

        if position != "All":
            players = [p for p in players if p["position"] == position]

        players = [
            p for p in players
            if p["age"] <= max_age
            and p["market_value"] <= max_value
            and p["match_score"] >= min_score
        ]

        if query:
            q = query.lower()
            players = [
                p for p in players
                if q in p["name"].lower()
                or q in p["club"].lower()
                or q in p["league"].lower()
                or q in p["position"].lower()
            ]

        return players

    @staticmethod
    def get_player(player_id: int) -> dict[str, Any] | None:
        """GET /api/players/{id}."""
        return next((p.copy() for p in _PLAYERS if p["id"] == player_id), None)

    @staticmethod
    def get_agent_steps() -> list[dict[str, Any]]:
        """GET /api/agent/steps — current execution steps."""
        return [s.copy() for s in _AGENT_STEPS]

    @staticmethod
    def get_memories() -> list[dict[str, Any]]:
        """GET /api/memory — club memory entries."""
        return [m.copy() for m in _MEMORIES]

    @staticmethod
    def get_transfer_plan_steps() -> list[dict[str, Any]]:
        """GET /api/transfer/plan-steps — animated planning sequence."""
        return [s.copy() for s in _TRANSFER_PLAN_STEPS]

    @staticmethod
    def get_transfer_targets() -> list[dict[str, Any]]:
        """GET /api/transfer/targets — ranked transfer recommendations."""
        return [t.copy() for t in _TRANSFER_TARGETS]

    @staticmethod
    def get_squad_slots(formation: str = "4-3-3") -> list[dict[str, Any]]:
        """GET /api/squad/{formation} — formation slot data."""
        if formation == "4-3-3":
            return [s.copy() for s in _SQUAD_433]
        return []

    @staticmethod
    def get_kpi_summary() -> dict[str, Any]:
        """GET /api/dashboard/kpis — dashboard headline metrics."""
        return {
            "players_scouted":   {"value": "1,247", "delta": "↑ 84 this week",        "color": "green"},
            "active_shortlists": {"value": "3",     "delta": "12 players total",       "color": "blue"},
            "budget_tracked":    {"value": "€47M",  "delta": "Summer 2025 window",     "color": "amber"},
            "agent_tasks":       {"value": "12",    "delta": "4 queued · 1 running",   "color": "purple"},
        }

    @staticmethod
    def get_recent_activity() -> list[dict[str, Any]]:
        """GET /api/dashboard/activity — recent agent activity feed."""
        return [
            {"time": "2m ago",  "text": "Shortlisted Bruno Ferreira (SC Braga, LW)",                    "color": "green"},
            {"time": "18m ago", "text": "Agent completed tactical fit analysis — 147 candidates",       "color": "blue"},
            {"time": "1h ago",  "text": "Memory updated: Primeira Liga pipeline priority confirmed",     "color": "amber"},
            {"time": "3h ago",  "text": "Transfer report generated — 4 targets ranked, plan compiled",  "color": "purple"},
            {"time": "1d ago",  "text": "User feedback: Lindqvist rec approved. Press signal confirmed.", "color": "green"},
        ]

    @staticmethod
    def get_position_demand() -> list[dict[str, Any]]:
        """GET /api/dashboard/position-demand — positions needed."""
        return [
            {"position": "LW",  "priority": 9},
            {"position": "ST",  "priority": 7},
            {"position": "CAM", "priority": 6},
            {"position": "DM",  "priority": 4},
            {"position": "CB",  "priority": 3},
            {"position": "RB",  "priority": 2},
        ]

    @staticmethod
    def get_radar_comparison(player_a_id: int, player_b_id: int) -> dict[str, Any]:
        """GET /api/compare/{a}/{b} — radar comparison data."""
        pa = MockDataService.get_player(player_a_id)
        pb = MockDataService.get_player(player_b_id)
        if not pa or not pb:
            return {}
        attrs = list(pa["radar"].keys())
        return {
            "player_a": pa,
            "player_b": pb,
            "radar_data": [
                {"attribute": attr, "a": pa["radar"][attr], "b": pb["radar"][attr]}
                for attr in attrs
            ],
            "similarity_score": round((pa["similarity_score"] + pb["similarity_score"]) / 2),
        }