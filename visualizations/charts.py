"""
visualizations/charts.py
=========================
Point 4 du sujet — Visualisations :
- Line plots : steps et calories over time
- Bar plots : workout frequency
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


# ── Line plots ─────────────────────────────────────────────────────────────────

def plot_steps_and_calories(df: pd.DataFrame, user_name: str):
    """
    Line plots for steps and calories burned over time
    for a specific user.
    """

    df_user         = df[df["name"] == user_name].copy()
    df_user["date"] = pd.to_datetime(df_user["date"])
    df_user         = df_user.sort_values("date")

    # Use index instead of dates for x-axis
    x     = range(len(df_user))
    dates = df_user["date"].dt.strftime("%Y-%m-%d").tolist()

    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    # Steps over time
    axes[0].plot(
        x,
        df_user["steps"].values,
        marker    = "o",
        color     = "steelblue",
        linewidth = 1.5,
        markersize= 4
    )
    axes[0].set_title(f"Steps Over Time — {user_name}")
    axes[0].set_ylabel("Steps")
    axes[0].set_xticks(list(x)[::5])
    axes[0].set_xticklabels(dates[::5], rotation=45, ha="right")
    axes[0].grid(True)

    # Calories over time
    axes[1].plot(
        x,
        df_user["calories"].values,
        marker    = "o",
        color     = "orange",
        linewidth = 1.5,
        markersize= 4
    )
    axes[1].set_title(f"Calories Burned Over Time — {user_name}")
    axes[1].set_ylabel("Calories")
    axes[1].set_xticks(list(x)[::5])
    axes[1].set_xticklabels(dates[::5], rotation=45, ha="right")
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig("visualizations/line_plot.png")
    plt.close()
    print(" Line plot saved to visualizations/line_plot.png")


# ── Bar plots ──────────────────────────────────────────────────────────────────

def plot_workout_frequency(df: pd.DataFrame):
    """
    Bar plot showing the frequency of each workout type
    across all users.
    """

    workout_counts = df["workout"].value_counts()

    plt.figure(figsize=(14, 6))
    plt.bar(
        workout_counts.index,
        workout_counts.values,
        color     = "green",
        edgecolor = "black"
    )
    plt.title("Workout Frequency (All Users)")
    plt.xlabel("Workout Type")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("visualizations/bar_plot.png")
    plt.close()
    print(" Bar plot saved to visualizations/bar_plot.png")