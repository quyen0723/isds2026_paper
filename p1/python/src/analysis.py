"""Descriptive + inferential analysis for p1.

``summarize`` returns a dict usable by ``visualization.make_figures``. Inference
uses statsmodels' RM-ANOVA as the primary test; pingouin is optional for the
Mauchly / Greenhouse-Geisser check.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

try:
    import pingouin as pg  # optional
except Exception:  # pragma: no cover
    pg = None

from statsmodels.stats.anova import AnovaRM


def summarize(df: pd.DataFrame) -> dict[str, Any]:
    grouped = df.groupby(["prompt_level", "platform"], observed=True)["composite_aioq_r"]
    means = grouped.mean().unstack("platform")
    sds = grouped.std(ddof=1).unstack("platform")
    ns = grouped.size().unstack("platform")

    # Primary RM-ANOVA on participant-level aggregates.
    wide = (
        df.groupby(["participant_id", "prompt_level", "platform"], observed=True)["composite_aioq_r"]
        .mean()
        .reset_index()
    )
    rm = AnovaRM(
        data=wide,
        depvar="composite_aioq_r",
        subject="participant_id",
        within=["prompt_level", "platform"],
    ).fit()

    mauchly = None
    if pg is not None:
        try:
            mauchly = pg.sphericity(
                data=wide,
                dv="composite_aioq_r",
                subject="participant_id",
                within=["prompt_level"],
            )._asdict()
        except Exception:
            mauchly = None

    return {
        "means": means,
        "sds": sds,
        "ns": ns,
        "rm_anova": rm.anova_table.reset_index().to_dict(orient="records"),
        "mauchly": mauchly,
        "bonferroni_alpha_prime": 0.05 / 5,
        "tool_citations": {
            "rm_anova": "statsmodels.stats.anova.AnovaRM",
            "mauchly": "pingouin.sphericity" if pg is not None else "skipped (pingouin not installed)",
        },
    }
