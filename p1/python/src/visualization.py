"""Figure generation for p1. Writes PNGs to ``output_dir``."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def make_figures(summary: dict[str, Any], output_dir: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    means = summary["means"]
    sds = summary["sds"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = range(len(means.index))
    width = 0.38
    for idx, platform in enumerate(means.columns):
        ax.bar(
            [xi + (idx - 0.5) * width for xi in x],
            means[platform].values,
            width=width,
            yerr=sds[platform].values,
            capsize=3,
            label=str(platform),
        )
    ax.set_xticks(list(x))
    ax.set_xticklabels([str(lvl) for lvl in means.index])
    ax.set_ylabel("Composite AIOQ-R (5-25)")
    ax.set_xlabel("Prompt quality level")
    ax.set_ylim(5, 25)
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(out / "aioq_r_by_level_platform.png", dpi=160)
    plt.close(fig)
