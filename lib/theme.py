"""Shared colours and visual constants — kept consistent with the paper."""

# Two-dimensional station types (paper palette)
TYPE_COLORS = {
    "HH": "#F59092",   # high service · high access
    "HL": "#F2B77C",   # high service · low access
    "LH": "#3FA6A0",   # low service  · high access (deepened teal)
    "LL": "#90BFF9",   # low service  · low access
}
TYPE_EDGE = {
    "HH": "#D86E70",
    "HL": "#D9954E",
    "LH": "#2C7E79",
    "LL": "#5E97E0",
}
TYPE_ORDER = ["HH", "HL", "LH", "LL"]

# As 0-255 RGB triples for pydeck
TYPE_RGB = {
    "HH": [245, 144, 146],
    "HL": [242, 183, 124],
    "LH": [63, 166, 160],
    "LL": [144, 191, 249],
}

# City tiers
TIER_ORDER = ["Tier-1", "New Tier-1", "Tier-2", "Tier-3"]
TIER_COLORS = {
    "Tier-1": "#2563EB",
    "New Tier-1": "#0EA5A4",
    "Tier-2": "#F59E0B",
    "Tier-3": "#94A3B8",
}

# App accents
PRIMARY = "#2563EB"
INK = "#1E293B"
MUTED = "#64748B"
GRID = "#E2E8F0"

# Sequential ramp for continuous metrics (light → deep blue)
SEQ_BLUE = ["#EFF6FF", "#BFDBFE", "#60A5FA", "#2563EB", "#1E3A8A"]
