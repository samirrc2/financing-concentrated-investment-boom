#!/usr/bin/env python3
"""Figure 1, built from the frozen source files only.

(a) capital expenditure as a share of operating cash flow, five largest investors;
(b) Herfindahl index of capital expenditure within the 500, with and without those five;
(c) cumulative internal cash coverage of the increment through each year, five against the rest.

Panels (a) and (b) reproduce the published figure; the percent labels in (a) previously carried
LaTeX escapes and rendered literally.
"""
import sys, os; sys.path.insert(0, "code")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from engine import *

RED, GREY, GRID, INK = "#a11d33", "#494949", "#dddddd", "#222222"
plt.rcParams.update({"font.size": 10.5, "axes.edgecolor": INK, "axes.labelcolor": INK,
                     "text.color": INK, "xtick.color": INK, "ytick.color": INK,
                     "axes.linewidth": 0.9, "figure.dpi": 200, "savefig.dpi": 200})

F = f500()
AI5 = {1652044, 1018724, 1341439, 1326801, 789019}


def style(ax):
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def panel_margin(ax):
    yrs = list(range(2017, 2026))
    v = [agg("capex", AI5, y) / agg("ocf", AI5, y) * 100 for y in yrs]
    ax.plot(yrs, v, "-o", color=RED, lw=1.9, ms=4.5, mfc="white", mec=RED, mew=1.4, zorder=3)
    for y in (2017, 2021, 2025):
        k = yrs.index(y)
        off, ha = ((7, -2), "left") if y == 2017 else ((0, 9), "center")
        ax.annotate(f"{v[k]:.0f}%", xy=(y, v[k]), xytext=off, textcoords="offset points",
                    ha=ha, fontsize=9, color=RED)
    ax.set_ylim(0, 85); ax.set_xlim(2016.5, 2025.5)
    ax.set_xticks([2017, 2019, 2021, 2023, 2025])
    ax.set_ylabel("Capital expenditure /\noperating cash flow (%)")
    ax.set_title("(a) Internal financing margin", fontsize=10.5, pad=8)
    style(ax)


def panel_hhi(ax):
    yrs = list(range(2013, 2026))
    h, hx = [], []
    for y in yrs:
        d = {c: S[y]["capex"].get(c, 0) for c in F if S[y]["capex"].get(c, 0) > 0}
        t = sum(d.values()); h.append(sum((x / t) ** 2 for x in d.values()) * 10000)
        e = {c: x for c, x in d.items() if c not in AI5}
        te = sum(e.values()); hx.append(sum((x / te) ** 2 for x in e.values()) * 10000)
    ax.plot(yrs, h, "-o", color=RED, lw=1.9, ms=4.2, mfc="white", mec=RED, mew=1.4,
            label="All 500 firms", zorder=3)
    ax.plot(yrs, hx, "--s", color=GREY, lw=1.4, ms=3.8, mfc="white", mec=GREY, mew=1.2,
            label="Excluding the five", zorder=2)
    ax.set_xticks([2013, 2016, 2019, 2022, 2025])
    ax.set_ylabel("Herfindahl index of\ncapital expenditure")
    ax.set_title("(b) Concentration of investment", fontsize=10.5, pad=8)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    style(ax)


def analysis_sample():
    """The 263 firms of Table 1, ranked by their full-window 2022-2025 increment."""
    yrs = range(2022, 2026)
    rows = []
    for c in F:
        if not (S[2021]["capex"].get(c, 0) > 0 and S[2025]["capex"].get(c, 0) > 0):
            continue
        b = agg("capex", {c}, 2021)
        dx = sum(agg("capex", {c}, t) - b for t in yrs)
        if dx > 0:
            rows.append((c, dx))
    rows.sort(key=lambda r: -r[1])
    return [c for c, _ in rows]


def coverage_through(year, members):
    """Coverage of the increment cumulated through `year`, on FIXED membership.

    Membership is set once from the full-window ranking, not re-selected each year. Filtering to
    a positive increment year by year would drop Amazon from 2022-2024 and put it back in 2025,
    so the path would partly reflect who is in the group rather than how coverage evolved.
    """
    yrs = range(2022, year + 1)
    dx = do = 0.0
    for c in members:
        bx = agg("capex", {c}, 2021); bo = agg("ocf", {c}, 2021)
        dx += sum(agg("capex", {c}, t) - bx for t in yrs)
        do += sum(agg("ocf", {c}, t) - bo for t in yrs)
    return do / dx * 100


def panel_annual(ax):
    yrs = list(range(2022, 2026))
    sample = analysis_sample()
    fixed_five, fixed_rest = sample[:5], sample[5:]
    five = [coverage_through(y, fixed_five) for y in yrs]
    rest = [coverage_through(y, fixed_rest) for y in yrs]
    ax.axhline(0, color=INK, lw=0.8, zorder=1)
    ax.plot(yrs, five, "-o", color=RED, lw=1.9, ms=4.5, mfc="white", mec=RED, mew=1.4,
            label="Five largest investors", zorder=3)
    ax.plot(yrs, rest, "--s", color=GREY, lw=1.4, ms=3.8, mfc="white", mec=GREY, mew=1.2,
            label="All other firms", zorder=2)
    ax.annotate(f"{five[-1]:.0f}%", xy=(2025, five[-1]), xytext=(-6, -14),
                textcoords="offset points", ha="right", fontsize=9, color=RED)
    ax.annotate(f"{five[0]:.0f}%", xy=(2022, five[0]), xytext=(6, -4),
                textcoords="offset points", ha="left", fontsize=9, color=RED)
    ax.set_xticks(yrs); ax.set_ylim(-110, 215)
    ax.set_ylabel("Coverage of the increment\nto date (%)")
    ax.set_title("(c) Cumulative coverage, 2022–2025", fontsize=10.5, pad=8)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    style(ax)


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(1, 3, figsize=(11.0, 2.95))
    panel_margin(ax[0]); panel_hhi(ax[1]); panel_annual(ax[2])
    fig.tight_layout(pad=0.7, w_pad=2.4)
    for ext in ("pdf", "png"):
        fig.savefig(f"figures/Figure_1.{ext}", bbox_inches="tight")
    print("wrote figures/Figure_1.pdf and .png")
