import sys
from pathlib import Path

BACKEND_ROOT = (
    Path(__file__).resolve().parents[2]
    / "backend"
)

if str(BACKEND_ROOT) not in sys.path:
    sys.path.append(str(BACKEND_ROOT))

from agents.planner import run_planner
from tools.player_search import search_players


class BackendAdapter:

    @staticmethod
    def search_players(
        position="All",
        max_age=30,
        max_value=100,
        min_score=0,
        query=""
    ):
        from db.queries import search_players

        try:
            pos = None if position == "All" else position

            results = search_players(
                position=pos,
                max_age=max_age,
                min_rating=min_score
            )
            mapped = []

            for p in results:

                p.pop("stats_embedding", None)

                mapped.append({
                    **p,

                    "id": str(p.get("_id", p.get("name"))),

                    "match_score": p.get("overall_rating", 0),

                    "similarity_score": p.get("overall_rating", 0),

                    "club": p.get("club_name", "Unknown"),

                    "nation": p.get("nationality", "Unknown"),

                    "market_value": p.get("value_eur", 0),

                    "market_value_display":
                        f"€{round(p.get('value_eur',0)/1_000_000,1)}M",

                    "league": p.get("league_name", ""),

                    "shortlisted": False,
                    "tags": [
                        p.get("position", "Unknown"),
                        p.get("preferred_foot", "Unknown"),
                        f"Age {p.get('age', 0)}"
                    ],
                    "flag": "🏳️",
                    "season_stats": {
                        "goals": max(0, round(p.get("shooting", 0) / 8)),
                        "assists": max(0, round(p.get("passing", 0) / 10)),
                        "appearances": 38,
                        "xg": round(p.get("shooting", 0) / 10, 1),
                        "xa": round(p.get("passing", 0) / 12, 1),
                    },
                    "radar": {
                        "Pace": p.get("pace", 0),
                        "Finishing": p.get("shooting", 0),
                        "Vision": p.get("passing", 0),
                        "Pressing": p.get("defending", 0),
                        "Aerial": p.get("physic", 0),
                        "Dribbling": p.get("dribbling", 0),
                    },
                    "pros": [
                        f"Pace {p.get('pace', 0)}",
                        f"Shooting {p.get('shooting', 0)}",
                        f"Dribbling {p.get('dribbling', 0)}",
                    ],

                    "cons": [
                        f"Defending {p.get('defending', 0)}",
                        f"Weak Foot {p.get('weak_foot', 0)}★",
                        f"Age {p.get('age', 0)}",
                    ],
                })
                
            print("FOUND PLAYERS:", len(mapped))

            return mapped
            
        except Exception as e:
            print("ERROR:", e)
            return []

    @staticmethod
    def ask_agent(query, session_id="demo"):
        return run_planner(
            query,
            session_id
        )