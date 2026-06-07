

import numpy as np
from scipy import stats


# ── 1. ANOVA — Calories par type de workout ───────────────────────────────────

def anova_calories_by_workout(df) -> dict:
    """
    Test if calorie burn differs significantly
    between workout types using ANOVA.
    H0 : No significant difference between groups.
    H1 : At least one group differs significantly.
    """

    # Group calories by workout type
    groups = [
        group["calories"].dropna().values
        for _, group in df.groupby("workout")
        if len(group) >= 2
    ]

    f_stat, p_value = stats.f_oneway(*groups)

    return {
        "test"       : "ANOVA",
        "question"   : "Is there a significant difference in calories burned across workout types?",
        "f_statistic": round(float(f_stat), 4),
        "p_value"    : round(float(p_value), 6),
        "conclusion" : "Significant difference (p < 0.05)" if p_value < 0.05
                       else "No significant difference (p >= 0.05)"
    }


# ── 2. Régression linéaire — Prédire les steps futurs ─────────────────────────

def linear_regression_steps(df) -> dict:
    """
    Predict future steps using linear regression
    based on past daily steps data.
    """

    # Use day index as X and steps as Y
    df_clean = df[["date", "steps"]].dropna()
    df_clean = df_clean.sort_values("date").reset_index(drop=True)

    x = np.arange(len(df_clean))
    y = df_clean["steps"].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # Predict next 7 days
    next_days     = np.arange(len(df_clean), len(df_clean) + 7)
    predicted     = [round(slope * d + intercept) for d in next_days]

    return {
        "test"       : "Linear Regression",
        "question"   : "How many steps will the user burn in the next 7 days?",
        "slope"      : round(slope, 4),
        "intercept"  : round(intercept, 2),
        "r_squared"  : round(r_value ** 2, 4),
        "p_value"    : round(p_value, 6),
        "predicted_steps_next_7_days": predicted,
        "conclusion" : "Increasing trend" if slope > 0 else "Decreasing trend"
    }


# ── 3. T-test apparié — Avant/Après programme ─────────────────────────────────

def paired_ttest_before_after(df) -> dict:
    """
    Compare calories burned before and after
    a workout program using paired t-test.
    H0 : No significant change after the program.
    H1 : Significant change after the program.
    """

    df_clean = df[["date", "calories"]].dropna()
    df_clean = df_clean.sort_values("date").reset_index(drop=True)

    # Split into two equal halves — before and after
    mid     = len(df_clean) // 2
    before  = df_clean["calories"].iloc[:mid].values
    after   = df_clean["calories"].iloc[mid:mid + len(before)].values

    t_stat, p_value = stats.ttest_rel(before, after)

    return {
        "test"        : "Paired T-test",
        "question"    : "Does the workout program lead to significant changes in calories burned?",
        "mean_before" : round(float(np.mean(before)), 2),
        "mean_after"  : round(float(np.mean(after)), 2),
        "t_statistic" : round(float(t_stat), 4),
        "p_value"     : round(float(p_value), 6),
        "conclusion"  : "Significant change (p < 0.05)" if p_value < 0.05
                        else "No significant change (p >= 0.05)"
    }