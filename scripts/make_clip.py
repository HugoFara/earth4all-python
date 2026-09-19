"""Render a short square clip contrasting the two Earth4All scenarios.

Both runs are the same model: up to 2022 they are identical to the last digit,
and the Giant Leap only changes a handful of parameters from there on. So the
shared stretch is drawn as a single neutral line, and the two colours only
appear at the point where the runs actually part.

    python scripts/make_clip.py                    # earth4all-scenarios.mp4, needs ffmpeg
    python scripts/make_clip.py clip.mp4           # another name
    python scripts/make_clip.py stills             # five PNG frames instead of a video

The clip is not committed; render it again when the model or the palette moves.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
sys.path.insert(0, str(Path(__file__).parent.parent))  # run without installing

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation

from earth4all import run_gl_solution, run_tltl_solution

# --- palette (validated for the dark surface) --------------------------------
SURFACE = "#1a1a19"
INK = "#ffffff"
INK_2 = "#c3c2b7"
INK_3 = "#7e7d76"
SHARED = "#8f8e86"
TLTL = "#d95926"  # Too Little Too Late
GL = "#3987e5"  # Giant Leap

FPS = 30
INTRO = 54  # 1.8 s title card
FAST = 120  # 1980 -> 2022, the years the two runs share
SLOW = 360  # 2022 -> 2100, where they part
OUTRO = 150  # 5 s hold on the end values
TOTAL = INTRO + FAST + SLOW + OUTRO

SPLIT = 2022.0
START, STOP = 1980.0, 2100.0
GUTTER = 2136.0  # room to the right of the plot for the end-value labels

PANELS = [
    ("pop.POP", "Population", "million people", "{:,.0f}"),
    ("wel.AWBI", "Average wellbeing", "index", "{:.2f}"),
    ("dem.INEQ", "Inequality", "index", "{:.2f}"),
    ("cli.OW", "Global warming", "°C over pre-industrial", "{:.2f}"),
]


def year_at(frame):
    """The year drawn at `frame`, slower after 2022 so the split can be read."""
    if frame < INTRO:
        return START
    step = frame - INTRO
    if step < FAST:
        return START + (SPLIT - START) * step / FAST
    step -= FAST
    return SPLIT + (STOP - SPLIT) * min(step / SLOW, 1.0)


def main(out):
    tltl, gl = run_tltl_solution(), run_gl_solution()
    times = tltl.t
    before, after = times <= SPLIT, times >= SPLIT

    fig = plt.figure(figsize=(10.8, 10.8), dpi=100, facecolor=SURFACE)
    fig.subplots_adjust(left=0.085, right=0.965, top=0.815, bottom=0.105,
                        hspace=0.40, wspace=0.30)

    fig.text(0.5, 0.975, "Two futures, one model", ha="center", va="top",
             color=INK, fontsize=32, fontweight="bold")
    fig.text(0.5, 0.936, "The Earth4All model, run in Python",
             ha="center", va="top", color=INK_2, fontsize=17)

    # The legend is a pair of direct labels, so identity never rests on colour.
    fig.text(0.085, 0.892, "●  Too Little Too Late", ha="left", va="top",
             color=TLTL, fontsize=16, fontweight="bold")
    fig.text(0.965, 0.892, "Giant Leap  ●", ha="right", va="top",
             color=GL, fontsize=16, fontweight="bold")
    counter = fig.text(0.5, 0.892, "1980", ha="center", va="top", color=INK,
                       fontsize=21, fontweight="bold", family="monospace")

    panels = []
    for index, (key, title, unit, fmt) in enumerate(PANELS):
        axes = fig.add_subplot(2, 2, index + 1)
        axes.set_facecolor(SURFACE)
        both = np.concatenate([tltl[key], gl[key]])
        low, high = both.min(), both.max()
        pad = 0.09 * (high - low)
        axes.set_ylim(low - pad, high + pad)
        axes.set_xlim(START, GUTTER)
        axes.set_title(title, color=INK, fontsize=19, fontweight="bold",
                       loc="left", pad=26)
        axes.text(0.0, 1.015, unit, transform=axes.transAxes, color=INK_3,
                  fontsize=12, va="bottom")
        axes.grid(color="#373734", linewidth=0.7)
        axes.set_axisbelow(True)
        for side in ("top", "right"):
            axes.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            axes.spines[side].set_color("#4a4a46")
        axes.tick_params(colors=INK_3, labelsize=11)
        axes.set_xticks([1980, 2020, 2060, 2100])

        marker = axes.axvline(SPLIT, color=INK_3, linewidth=1.0,
                              linestyle=(0, (4, 4)), alpha=0.0)
        shared, = axes.plot([], [], color=SHARED, linewidth=2.6,
                            solid_capstyle="round")
        drawn = {}
        for name, colour in (("tltl", TLTL), ("gl", GL)):
            line, = axes.plot([], [], color=colour, linewidth=2.8,
                              solid_capstyle="round")
            dot, = axes.plot([], [], "o", color=colour, markersize=9,
                             markeredgecolor=SURFACE, markeredgewidth=2)
            label = axes.text(STOP + 4, 0, "", ha="left", va="center",
                              color=colour, fontsize=16, fontweight="bold",
                              alpha=0.0)
            drawn[name] = (line, dot, label)
        panels.append((key, fmt, axes, marker, shared, drawn))

    caption = fig.text(0.5, 0.030, "", ha="center", va="bottom", color=INK_2,
                       fontsize=15)

    # The title card covers the whole figure and lifts away after the intro.
    # Its ticks and spines go, but not `set_axis_off` — that would stop the
    # background patch being drawn, and the patch is the whole point.
    cover = fig.add_axes([0, 0, 1, 1], zorder=10)
    cover.set_facecolor(SURFACE)
    cover.set_xticks([])
    cover.set_yticks([])
    for spine in cover.spines.values():
        spine.set_visible(False)
    cover_text = [
        cover.text(0.5, 0.60, "What if we changed course?", ha="center",
                   color=INK, fontsize=38, fontweight="bold"),
        cover.text(0.5, 0.505, "Earth4All, ported to Python", ha="center",
                   color=INK_2, fontsize=23),
        cover.text(0.5, 0.425, "12 sectors  ·  638 variables  ·  two futures",
                   ha="center", color=INK_3, fontsize=18),
    ]

    def update(frame):
        if frame < INTRO:
            return
        fade = min((frame - INTRO) / 12.0, 1.0)
        cover.patch.set_alpha(1.0 - fade)
        for text in cover_text:
            text.set_alpha(1.0 - fade)
        cover.set_visible(fade < 1.0)

        year = year_at(frame)
        counter.set_text(f"{year:.0f}")
        head = times <= year

        for key, fmt, _, marker, shared, drawn in panels:
            window = before & head
            shared.set_data(times[window], tltl[key][window])

            for name, solution in (("tltl", tltl), ("gl", gl)):
                line, dot, _ = drawn[name]
                window = after & head
                values = solution[key][window]
                line.set_data(times[window], values)
                if len(values):
                    dot.set_data([times[window][-1]], [values[-1]])
            if year >= SPLIT:
                marker.set_alpha(min((year - SPLIT) / 3.0, 0.5))

        if year >= STOP:
            reveal = min((frame - (INTRO + FAST + SLOW)) / 15.0, 1.0)
            for key, fmt, _, _, _, drawn in panels:
                for name, solution in (("tltl", tltl), ("gl", gl)):
                    _, _, label = drawn[name]
                    label.set_text(fmt.format(solution[key][-1]))
                    label.set_y(solution[key][-1])
                    label.set_alpha(reveal)
            caption.set_text("Five turnarounds, started in 2022  ·  "
                             "github.com/HugoFara/earth4all-python")
            caption.set_alpha(reveal)

    if out == "stills":
        for frame in (0, INTRO + 6, INTRO + FAST, INTRO + FAST + SLOW // 2, TOTAL - 1):
            update(frame)
            fig.savefig(f"still-{frame:04d}.png", facecolor=SURFACE)
        return

    animation = FuncAnimation(fig, update, frames=TOTAL, interval=1000 / FPS)
    writer = FFMpegWriter(fps=FPS, bitrate=6000,
                          extra_args=["-pix_fmt", "yuv420p", "-profile:v", "high"])
    animation.save(out, writer=writer, savefig_kwargs={"facecolor": SURFACE})
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "earth4all-scenarios.mp4")
