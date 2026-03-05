"""Generate a shields.io endpoint badge JSON with total all-time HF downloads.

Reads downloads.csv where each value is the all-time download count per model.
Sums the latest row across all models.
"""

import json
import pandas as pd


def format_count(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


df = pd.read_csv("downloads.csv", parse_dates=["date"])
df = df.groupby("date").last().sort_index()

total = int(df.iloc[-1].sum())

badge = {
    "schemaVersion": 1,
    "label": "HF downloads",
    "message": format_count(total),
    "color": "blue",
}

with open("badge.json", "w") as f:
    json.dump(badge, f, indent=2)

print(f"Badge: {total} downloads -> {format_count(total)}")
