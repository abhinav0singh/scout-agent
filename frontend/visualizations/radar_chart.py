"""
visualizations/radar_chart.py
All chart functions for the Scout Agent Pro platform.
Every chart returns a Plotly Figure — call st.plotly_chart(fig, ...) to render.
"""

from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px


# ── Shared theme ──────────────────────────────────────────────────
_BG   = "rgba(0,0,0,0)"
_GRID = "#192437"
_T2   = "#7A92B0"
_T3   = "#3D5270"
_S1   = "#09101C"

_FONT = dict(family="DM Sans, sans-serif", color=_T2)

GREEN  = "#00E87D"
AMBER  = "#FF8C00"
BLUE   = "#3B8EFF"
PURPLE = "#B87DFF"
RED    = "#FF4545"


def _base_layout(**overrides) -> dict:
    layout = dict(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=_FONT,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
    )
    layout.update(overrides)
    return layout


# ── Radar Chart ───────────────────────────────────────────────────

def radar_single(player: dict, height: int = 260) -> go.Figure:
    """Single-player radar chart."""
    attrs  = list(player["radar"].keys())
    vals   = list(player["radar"].values())
    closed = attrs + [attrs[0]]
    v_closed = vals + [vals[0]]

    fig = go.Figure(go.Scatterpolar(
        r=v_closed, theta=closed,
        fill="toself",
        line=dict(color=GREEN, width=2),
        fillcolor="rgba(0,232,125,0.15)",
        marker=dict(size=4, color=GREEN),
        name=player["name"],
    ))
    fig.update_layout(**_base_layout(height=height), polar=dict(
        bgcolor=_BG,
        radialaxis=dict(visible=True, range=[0, 100],
            tickfont=dict(size=8, color=_T3),
            gridcolor=_GRID, linecolor=_GRID),
        angularaxis=dict(
            tickfont=dict(size=10, color=_T2, family="DM Sans"),
            linecolor=_GRID, gridcolor=_GRID),
    ))
    return fig


def radar_comparison(player_a: dict, player_b: dict, height: int = 300) -> go.Figure:
    """Dual-player radar comparison chart."""
    attrs     = list(player_a["radar"].keys())
    vals_a    = list(player_a["radar"].values())
    vals_b    = list(player_b["radar"].values())
    closed    = attrs + [attrs[0]]
    v_a_close = vals_a + [vals_a[0]]
    v_b_close = vals_b + [vals_b[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=v_a_close, theta=closed,
        fill="toself", name=player_a["name"].split()[-1],
        line=dict(color=GREEN, width=2),
        fillcolor="rgba(0,232,125,0.15)",
        marker=dict(size=4, color=GREEN),
    ))
    fig.add_trace(go.Scatterpolar(
        r=v_b_close, theta=closed,
        fill="toself", name=player_b["name"].split()[-1],
        line=dict(color=BLUE, width=2),
        fillcolor="rgba(59,142,255,0.12)",
        marker=dict(size=4, color=BLUE),
    ))

    fig.update_layout(
        **_base_layout(height=height, showlegend=True),
        legend=dict(
            font=dict(color=_T2, size=11, family="DM Sans"),
            bgcolor=_BG, orientation="h",
            x=0.5, y=-0.12, xanchor="center",
        ),
        polar=dict(
            bgcolor=_BG,
            radialaxis=dict(visible=True, range=[0, 100],
                tickfont=dict(size=8, color=_T3),
                gridcolor=_GRID, linecolor=_GRID),
            angularaxis=dict(
                tickfont=dict(size=11, color=_T2, family="DM Sans"),
                linecolor=_GRID, gridcolor=_GRID),
        ),
    )
    return fig


# ── Bar Charts ────────────────────────────────────────────────────

def horizontal_bar(
    labels: list[str],
    values: list[float],
    colors: list[str] | None = None,
    height: int = 200,
    title: str = "",
) -> go.Figure:
    """Horizontal bar chart — used for position demand, budget allocation, etc."""
    bar_colors = colors or [GREEN] * len(values)

    fig = go.Figure(go.Bar(
        x=values, y=labels,
        orientation="h",
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[str(v) for v in values],
        textposition="outside",
        textfont=dict(color=_T2, size=10),
    ))
    fig.update_layout(
        **_base_layout(height=height),
        title=dict(text=title, font=dict(color=_T2, size=12)) if title else {},
        xaxis=dict(visible=False),
        yaxis=dict(
            tickfont=dict(color=_T2, size=11, family="DM Sans"),
            gridcolor=_BG,
        ),
        bargap=0.3,
    )
    return fig


def vertical_bar(
    labels: list[str],
    values: list[float],
    colors: list[str] | None = None,
    height: int = 220,
    title: str = "",
) -> go.Figure:
    """Vertical bar chart."""
    bar_colors = colors or [GREEN] * len(values)

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[str(v) for v in values],
        textposition="outside",
        textfont=dict(color=_T2, size=10),
    ))
    fig.update_layout(
        **_base_layout(height=height),
        title=dict(text=title, font=dict(color=_T2, size=12)) if title else {},
        xaxis=dict(tickfont=dict(color=_T2, size=11, family="DM Sans"), gridcolor=_BG),
        yaxis=dict(tickfont=dict(color=_T3, size=9), gridcolor=_GRID, linecolor=_GRID),
        bargap=0.35,
    )
    return fig


# ── Gauge / Indicator ─────────────────────────────────────────────

def similarity_gauge(score: int, height: int = 180) -> go.Figure:
    """Circular gauge for similarity / fit score."""
    color = GREEN if score >= 85 else AMBER if score >= 70 else RED

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge=dict(
            axis=dict(range=[0, 100], tickfont=dict(color=_T3, size=9)),
            bar=dict(color=color),
            bgcolor=_S1,
            bordercolor=_GRID,
            steps=[
                dict(range=[0, 50],  color="rgba(61,82,112,0.2)"),
                dict(range=[50, 75], color="rgba(255,140,0,0.08)"),
                dict(range=[75, 100],color="rgba(0,232,125,0.08)"),
            ],
        ),
        number=dict(suffix="%", font=dict(size=30, color="#E2EDFF", family="Syne")),
    ))
    fig.update_layout(**_base_layout(height=height), margin=dict(l=20, r=20, t=20, b=0))
    return fig


def transfer_fit_bar(
    targets: list[dict],
    height: int = 220,
) -> go.Figure:
    """Horizontal bar showing transfer fit scores for ranked targets."""
    names  = [f"#{t['rank']} {t['name']}" for t in targets]
    scores = [t["fit_score"] for t in targets]
    colors_map = {"green": GREEN, "amber": AMBER, "blue": BLUE}
    bar_colors = [colors_map.get(t.get("color_key", "green"), GREEN) for t in targets]

    fig = go.Figure(go.Bar(
        x=scores, y=names,
        orientation="h",
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f"{s}% fit" for s in scores],
        textposition="outside",
        textfont=dict(color=_T2, size=10),
    ))
    fig.update_layout(
        **_base_layout(height=height),
        xaxis=dict(range=[0, 110], visible=False),
        yaxis=dict(tickfont=dict(color=_T2, size=11, family="DM Sans"), gridcolor=_BG),
        bargap=0.35,
    )
    return fig


# ── Budget Donut ──────────────────────────────────────────────────

def budget_donut(
    labels: list[str],
    values: list[float],
    colors: list[str] | None = None,
    total_label: str = "",
    height: int = 200,
) -> go.Figure:
    """Budget allocation donut chart."""
    pie_colors = colors or [GREEN, GREEN, AMBER, "#192437"]

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=pie_colors, line=dict(color=_S1, width=2)),
        hole=0.65,
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>€%{value}M<extra></extra>",
    ))
    if total_label:
        parts = total_label.split("\n")
        fig.add_annotation(
            text=parts[0], x=0.5, y=0.55, showarrow=False,
            font=dict(size=18, color="#E2EDFF", family="Syne"),
        )
        if len(parts) > 1:
            fig.add_annotation(
                text=parts[1], x=0.5, y=0.42, showarrow=False,
                font=dict(size=10, color=_T3, family="DM Sans"),
            )
    fig.update_layout(
        **_base_layout(height=height, showlegend=False),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


# ── Squad Chemistry Radar ─────────────────────────────────────────

def squad_chemistry_radar(
    current_vals: list[float],
    target_vals: list[float],
    categories: list[str],
    height: int = 240,
) -> go.Figure:
    """Squad chemistry comparison radar — current vs. post-transfer."""
    closed_cats = categories + [categories[0]]
    v_curr = current_vals + [current_vals[0]]
    v_targ = target_vals  + [target_vals[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=v_curr, theta=closed_cats,
        fill="toself", name="Current",
        line=dict(color=BLUE, width=2),
        fillcolor="rgba(59,142,255,0.12)",
    ))
    fig.add_trace(go.Scatterpolar(
        r=v_targ, theta=closed_cats,
        fill="toself", name="After Transfers",
        line=dict(color=GREEN, width=2, dash="dot"),
        fillcolor="rgba(0,232,125,0.08)",
    ))
    fig.update_layout(
        **_base_layout(height=height, showlegend=True),
        legend=dict(
            font=dict(color=_T2, size=10, family="DM Sans"),
            bgcolor=_BG, orientation="h",
            x=0.5, y=-0.12, xanchor="center",
        ),
        polar=dict(
            bgcolor=_BG,
            radialaxis=dict(visible=True, range=[0, 100],
                tickfont=dict(size=8, color=_T3),
                gridcolor=_GRID, linecolor=_GRID),
            angularaxis=dict(
                tickfont=dict(size=10, color=_T2, family="DM Sans"),
                linecolor=_GRID, gridcolor=_GRID),
        ),
    )
    return fig


# ── Agent Timeline ────────────────────────────────────────────────

def agent_execution_gantt(steps: list[dict], height: int = 200) -> go.Figure:
    """
    Horizontal Gantt-style chart showing agent step durations.
    steps: list of dicts with keys label, duration_ms, type
    """
    type_color = {"plan": PURPLE, "tool": BLUE, "memory": AMBER, "output": GREEN}
    labels  = [s["label"] for s in steps if s.get("duration_ms", 0) > 0]
    durations = [s["duration_ms"] for s in steps if s.get("duration_ms", 0) > 0]
    colors_list = [type_color.get(s["type"], _T2) for s in steps if s.get("duration_ms", 0) > 0]

    fig = go.Figure(go.Bar(
        x=durations, y=labels,
        orientation="h",
        marker=dict(color=colors_list, line=dict(width=0)),
        text=[f"{d}ms" for d in durations],
        textposition="outside",
        textfont=dict(color=_T2, size=10),
    ))
    fig.update_layout(
        **_base_layout(height=height),
        xaxis=dict(
            title=dict(text="Duration (ms)", font=dict(color=_T3, size=10)),
            tickfont=dict(color=_T3, size=9),
            gridcolor=_GRID, linecolor=_GRID,
        ),
        yaxis=dict(
            tickfont=dict(color=_T2, size=10, family="DM Sans"),
            gridcolor=_BG,
        ),
        bargap=0.35,
    )
    return fig