"""Plotly styling helpers, kept visually consistent across pages."""
from lib.theme import INK, MUTED, GRID

FONT = ('-apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", '
        "Roboto, Helvetica, Arial, sans-serif")


def style_fig(fig, height=None, legend_top=True):
    """Apply the house style to a Plotly figure."""
    fig.update_layout(
        font=dict(family=FONT, size=13, color=INK),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        hoverlabel=dict(font_size=12, font_family=FONT),
        colorway=["#2563EB", "#0EA5A4", "#F59E0B", "#EF4444", "#8B5CF6"],
    )
    if height:
        fig.update_layout(height=height)
    if legend_top:
        fig.update_layout(legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, title_text="",
        ))
    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False,
                     linecolor=GRID, tickfont=dict(color=MUTED))
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False,
                     linecolor=GRID, tickfont=dict(color=MUTED))
    return fig


def human(n) -> str:
    """Compact number format: 1234567 -> '1.23M'."""
    try:
        n = float(n)
    except (TypeError, ValueError):
        return "—"
    a = abs(n)
    if a >= 1e9:
        return f"{n/1e9:.2f}B"
    if a >= 1e6:
        return f"{n/1e6:.2f}M"
    if a >= 1e3:
        return f"{n/1e3:.1f}k"
    return f"{n:.0f}"
