import hashlib
import colorsys

import matplotlib
matplotlib.use("Agg")  # non-interactive backend (safe for CI)
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go

# ── Deterministic styling based on model name ──────────────────────────

MARKERS = ["o", "s", "^", "v", "D", "p", "*", "h", "X", "P", "d", "<", ">", "8"]
LINESTYLES = ["-", "--", "-.", ":"]
TOP_N = 10  # number of models to annotate directly on lines


def _name_hash(name: str) -> int:
    """Deterministic integer from model name."""
    return int(hashlib.sha256(name.encode()).hexdigest(), 16)


def _color_for_name(name: str) -> str:
    """HSL-based hex color deterministic on name, high saturation/brightness."""
    h = _name_hash(name)
    hue = (h % 360) / 360.0
    sat = 0.55 + (h % 35) / 100.0  # 0.55 – 0.90
    light = 0.35 + (h % 25) / 100.0  # 0.35 – 0.60
    r, g, b = colorsys.hls_to_rgb(hue, light, sat)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def style_for(name: str) -> dict:
    h = _name_hash(name)
    return dict(
        color=_color_for_name(name),
        marker=MARKERS[h % len(MARKERS)],
        linestyle=LINESTYLES[(h >> 8) % len(LINESTYLES)],
    )


# ── Pretty display names (paper-verified) ────────────────────────────

PRETTY_NAMES = {
    "affine-steerers": "Affine Steerers",
    "aliked-lightglue": "ALIKED-LightGlue",
    "aliked-lightglue-subpx": "ALIKED-LightGlue-SubPx",
    "aspanformer": "ASpanFormer",
    "d2net": "D2-Net",
    "dedode": "DeDoDe",
    "dedode-kornia": "DeDoDe-Kornia",
    "dedode-lightglue": "DeDoDe-LightGlue",
    "dedode-subpx": "DeDoDe-SubPx",
    "disk-lightglue": "DISK-LightGlue",
    "doghardnet-lightglue": "DoGHardNet-LightGlue",
    "doghardnet-nn": "DoGHardNet-NN",
    "duster": "DUSt3R",
    "edm": "EDM",
    "eloftr": "Efficient LoFTR",
    "gim-dkm": "GIM-DKM",
    "gim-lightglue": "GIM-LightGlue",
    "liftfeat": "LiftFeat",
    "lisrd": "LISRD",
    "lisrd-aliked": "LISRD-ALIKED",
    "lisrd-sift": "LISRD-SIFT",
    "lisrd-superpoint": "LISRD-SuperPoint",
    "loftr": "LoFTR",
    "master": "MASt3R",
    "matchanything-eloftr": "MatchAnything-Efficient LoFTR",
    "matchanything-roma": "MatchAnything-RoMa",
    "matchformer": "MatchFormer",
    "minima": "MINIMA",
    "minima-loftr": "MINIMA-LoFTR",
    "minima-roma": "MINIMA-RoMa",
    "minima-roma-tiny": "MINIMA-RoMa-Tiny",
    "minima-superpoint-lightglue": "MINIMA-SuperPoint-LightGlue",
    "minima-xoftr": "MINIMA-XoFTR",
    "omniglue": "OmniGlue",
    "orb-nn": "ORB-NN",
    "patch2pix": "Patch2Pix",
    "r2d2": "R2D2",
    "rdd": "RDD",
    "rdd-aliked": "RDD-ALIKED",
    "rdd-lightglue": "RDD-LightGlue",
    "rdd-star": "RDD*",
    "ripe": "RIPE",
    "roma": "RoMa",
    "romav2": "RoMa-v2",
    "se2loftr": "SE2-LoFTR",
    "sift-lightglue": "SIFT-LightGlue",
    "sift-nn": "SIFT-NN",
    "sift-sphereglue": "SIFT-SphereGlue",
    "silk": "SiLK",
    "steerers": "Steerers",
    "superglue": "SuperGlue",
    "superpoint-lightglue": "SuperPoint-LightGlue",
    "superpoint-lightglue-subpx": "SuperPoint-LightGlue-SubPx",
    "superpoint-sphereglue": "SuperPoint-SphereGlue",
    "tiny-roma": "Tiny RoMa",
    "topicfm": "TopicFM",
    "topicfm-plus": "TopicFM+",
    "ufm": "UFM",
    "xfeat": "XFeat",
    "xfeat-lightglue": "XFeat-LightGlue",
    "xfeat-lightglue-subpx": "XFeat-LightGlue-SubPx",
    "xfeat-star": "XFeat*",
    "xfeat-star-steerers-learned": "XFeat*-Steerers-Learned",
    "xfeat-star-steerers-perm": "XFeat*-Steerers-Perm",
    "xfeat-steerers-learned": "XFeat-Steerers-Learned",
    "xfeat-steerers-perm": "XFeat-Steerers-Perm",
    "xfeat-subpx": "XFeat-SubPx",
    "xoftr": "XoFTR",
    "zippypoint": "ZippyPoint",
}


def pretty_name(raw: str) -> str:
    """Return display name for a model, falling back to title-cased segments."""
    if raw in PRETTY_NAMES:
        return PRETTY_NAMES[raw]
    return "-".join(seg.title() for seg in raw.split("-"))


# ── Load and prepare data ──────────────────────────────────────────────

df = pd.read_csv("downloads.csv", parse_dates=["date"])
df = df.groupby("date").last().sort_index()
start_date = df.index[0].strftime("%b %d, %Y")
df = df.subtract(df.iloc[0])

# Rank models by final cumulative downloads (for annotation)
final = df.iloc[-1].sort_values(ascending=False)
top_models = set(final.index[:TOP_N])

# ── Matplotlib static plot ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(16, 9))

for col in df.columns:
    s = style_for(col)
    ax.plot(
        df.index, df[col],
        color=s["color"],
        marker=s["marker"],
        linestyle=s["linestyle"],
        markersize=3,
        linewidth=1.4,
        label=pretty_name(col),
    )

# Annotate top N at the end of their lines
for col in top_models:
    last_date = df.index[-1]
    last_val = df[col].iloc[-1]
    ax.annotate(
        pretty_name(col),
        xy=(last_date, last_val),
        xytext=(8, 0),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
        color=style_for(col)["color"],
        va="center",
    )

ax.set_xlabel("Date", fontsize=16)
ax.set_ylabel("Cumulative Downloads", fontsize=16)
ax.set_title(f"Cumulative Downloads per Model (since {start_date})", fontsize=18)
ax.tick_params(axis="both", labelsize=13)
ax.grid(True, linestyle="--", alpha=0.4)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=35)

ax.legend(
    bbox_to_anchor=(1.15, 0), loc="lower left",
    fontsize=9.5, ncol=2, framealpha=0.9, columnspacing=1.0,
    borderaxespad=0,
)
plt.tight_layout()
plt.savefig("downloads_per_day.png", dpi=150, bbox_inches="tight")
print("Saved downloads_per_day.png")

# ── Plotly interactive plot ────────────────────────────────────────────

PLOTLY_DASH = {"-": "solid", "--": "dash", "-.": "dashdot", ":": "dot"}
PLOTLY_MARKER = {
    "o": "circle", "s": "square", "^": "triangle-up", "v": "triangle-down",
    "D": "diamond", "p": "pentagon", "*": "star", "h": "hexagon",
    "X": "x", "P": "cross", "d": "diamond-tall", "<": "triangle-left",
    ">": "triangle-right", "8": "octagon",
}

pfig = go.Figure()
for col in final.index:  # ordered by most downloads
    s = style_for(col)
    pfig.add_trace(go.Scatter(
        x=df.index, y=df[col],
        name=pretty_name(col),
        mode="lines+markers",
        line=dict(color=s["color"], dash=PLOTLY_DASH.get(s["linestyle"], "solid"), width=2),
        marker=dict(symbol=PLOTLY_MARKER.get(s["marker"], "circle"), size=5),
        hovertemplate=f"<b>{pretty_name(col)}</b><br>%{{x|%b %d}}<br>Downloads: %{{y}}<extra></extra>",
    ))

pfig.update_layout(
    title=f"Cumulative Downloads per Model (since {start_date})",
    xaxis_title="Date",
    yaxis_title="Cumulative Downloads",
    hovermode="closest",
    hoverdistance=20,
    template="plotly_white",
    legend=dict(font=dict(size=10)),
)
pfig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
pfig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
HOVER_JS = """
document.body.style.margin = '0';
var gd = document.getElementsByClassName('plotly-graph-div')[0];
var numTraces = gd.data.length;
var allIdx = [];
for (var i = 0; i < numTraces; i++) allIdx.push(i);

gd.on('plotly_hover', function(data) {
    var idx = data.points[0].curveNumber;
    var others = allIdx.filter(function(i) { return i !== idx; });
    Plotly.restyle(gd, {'line.width': 1, 'opacity': 0.15}, others);
    Plotly.restyle(gd, {'line.width': 5, 'opacity': 1}, [idx]);
});

gd.on('plotly_unhover', function() {
    Plotly.restyle(gd, {'line.width': 2, 'opacity': 1}, allIdx);
});
"""
pfig.write_html("downloads_per_day.html", post_script=HOVER_JS,
                config={"displayModeBar": False},
                default_width='100%', default_height='100vh')
print("Saved downloads_per_day.html")
