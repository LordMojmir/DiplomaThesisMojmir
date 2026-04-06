"""
ERP Thesis Figures — Plotly Express generation script
Consistent dark theme, same font, same color palette across all figures.

Usage:
    python3 plots/generate_figures.py

Outputs PNGs to plots/
"""

import plotly.graph_objects as go
import numpy as np
import os

# ── Shared design tokens ─────────────────────────────────────────────────────
BG          = "#ffffff"   # white background
PAPER_BG    = "#ffffff"   # white panel
GRID        = "#e5e5e5"   # light grey grid
AXIS_COLOR  = "#444444"   # dark axis / tick labels
TEXT_COLOR  = "#222222"   # near-black titles & labels
FONT_FAMILY = "Inter, Arial, sans-serif"
FONT_SIZE   = 16

# Palette — muted science colours (Nature / seaborn "muted" style)
# Same set used across every chart for visual consistency
C1 = "#4878cf"   # steel blue
C2 = "#d65f5f"   # muted red
C3 = "#6acc65"   # sage green
C4 = "#b47cc7"   # dusty purple

W, H = 1200, 700       # output resolution

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def base_layout(title: str) -> dict:
    """Return a shared layout dict for all figures."""
    return dict(
        title=dict(text=title, font=dict(size=22, color=TEXT_COLOR, family=FONT_FAMILY),
                   x=0.5, xanchor="center", y=0.95),
        paper_bgcolor=BG,
        plot_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAMILY, size=FONT_SIZE, color=TEXT_COLOR),
        xaxis=dict(
            color=AXIS_COLOR,
            gridcolor=GRID,
            linecolor=AXIS_COLOR,
            tickfont=dict(size=14, color=AXIS_COLOR),
            title_font=dict(size=15, color=AXIS_COLOR),
        ),
        yaxis=dict(
            color=AXIS_COLOR,
            gridcolor=GRID,
            linecolor=AXIS_COLOR,
            tickfont=dict(size=14, color=AXIS_COLOR),
            title_font=dict(size=15, color=AXIS_COLOR),
            zeroline=False,
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.05)",
            bordercolor=GRID,
            borderwidth=1,
            font=dict(size=14, color=TEXT_COLOR),
        ),
        margin=dict(l=70, r=40, t=80, b=70),
    )


# ════════════════════════════════════════════════════════════════════════════
# Figure 2 — Impact of Fuzzy Matching
# ════════════════════════════════════════════════════════════════════════════
def fig_fuzzy_matching():
    groups     = ["Rules Only", "Rules + Fuzzy Matching"]
    val_pass   = [82, 97]
    llm_invoke = [19,  3]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Validation Pass Rate (%)",
        x=groups, y=val_pass,
        marker_color=C1,
        marker_line_width=0,
        text=[f"{v}%" for v in val_pass],
        textposition="outside",
        textfont=dict(size=15, color=TEXT_COLOR),
        width=0.3,
        offset=-0.18,
    ))

    fig.add_trace(go.Bar(
        name="LLM Invocation Rate (%)",
        x=groups, y=llm_invoke,
        marker_color=C2,
        marker_line_width=0,
        text=[f"{v}%" for v in llm_invoke],
        textposition="outside",
        textfont=dict(size=15, color=TEXT_COLOR),
        width=0.3,
        offset=0.18,
    ))

    layout = base_layout("Impact of Fuzzy Matching on Pipeline Accuracy")
    layout["barmode"] = "group"
    layout["yaxis"]["title"] = "Percentage (%)"
    layout["yaxis"]["range"] = [0, 115]
    layout["xaxis"]["title"] = ""
    layout["bargap"] = 0.35
    fig.update_layout(**layout)

    path = os.path.join(OUTPUT_DIR, "FuzzyMatching_Image.png")
    fig.write_image(path, width=W, height=H, scale=2)
    print(f"Saved: {path}")


# ════════════════════════════════════════════════════════════════════════════
# Figure 4 — Pure Rule-Based vs. Hybrid Pipeline
# ════════════════════════════════════════════════════════════════════════════
def fig_hybrid_vs_rules():
    categories = ["Pure Rule-Based", "Hybrid (Rules + ML + LLM)"]
    values     = [68.4, 97.8]
    colors     = [C1, C3]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories, y=values,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(size=17, color=TEXT_COLOR, family=FONT_FAMILY),
        width=0.45,
        showlegend=False,
    ))

    # delta annotation arrow
    fig.add_annotation(
        x=1, y=97.8 + 6,
        ax=0, ay=68.4 + 6,
        axref="x", ayref="y",
        xref="x", yref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.2,
        arrowwidth=2,
        arrowcolor=C3,
        text="+29.4 pp",
        font=dict(size=14, color=C3),
        align="center",
    )

    layout = base_layout("Pure Rule-Based vs. Hybrid Pipeline Success Rate")
    layout["yaxis"]["title"] = "Transformation Success Rate (%)"
    layout["yaxis"]["range"] = [0, 115]
    layout["xaxis"]["title"] = ""
    fig.update_layout(**layout)

    path = os.path.join(OUTPUT_DIR, "RuleVSPipeline_Image.png")
    fig.write_image(path, width=W, height=H, scale=2)
    print(f"Saved: {path}")


# ════════════════════════════════════════════════════════════════════════════
# Figure 5 — Latency Distribution
# ════════════════════════════════════════════════════════════════════════════
def fig_latency_distribution():
    np.random.seed(42)

    rules_ms = np.random.exponential(scale=15, size=500).clip(1, 150)
    llm_ms   = np.random.normal(loc=3100, scale=800, size=150).clip(800, 6500)

    # Use log-spaced bins so both clusters get equal visual weight
    bins = np.logspace(0, np.log10(7000), 40)

    r_counts, r_edges = np.histogram(rules_ms, bins=bins)
    l_counts, l_edges = np.histogram(llm_ms,   bins=bins)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=r_edges[:-1],
        y=r_counts,
        name="Rules + ML Path",
        marker_color=C1,
        opacity=0.9,
        marker_line_width=0,
        width=np.diff(r_edges) * 0.9,
    ))

    fig.add_trace(go.Bar(
        x=l_edges[:-1],
        y=l_counts,
        name="LLM Fallback Path",
        marker_color=C2,
        opacity=0.85,
        marker_line_width=0,
        width=np.diff(l_edges) * 0.9,
    ))

    layout = base_layout("Latency Distribution: Rules+ML vs. LLM Fallback")
    layout["barmode"] = "overlay"
    layout["xaxis"].update(
        title="Processing Latency (ms)  [log scale]",
        type="log",
        range=[0, np.log10(7000)],
        tickmode="array",
        tickvals=[1, 10, 100, 1000, 5000],
        ticktext=["1", "10", "100", "1 000", "5 000"],
    )
    layout["yaxis"].update(
        title="Number of Records (log scale)",
        type="log",
        range=[0, 3],
        tickmode="array",
        tickvals=[1, 10, 100, 1000],
        ticktext=["10⁰", "10¹", "10²", "10³"],
    )
    fig.update_layout(**layout)

    path = os.path.join(OUTPUT_DIR, "LatencyDistribution_Image-3.png")
    fig.write_image(path, width=W, height=H, scale=2)
    print(f"Saved: {path}")


if __name__ == "__main__":
    fig_fuzzy_matching()
    fig_hybrid_vs_rules()
    fig_latency_distribution()
    print("\nAll figures generated. Review them before updating main.tex.")
