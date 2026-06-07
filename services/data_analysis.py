
import pandas as pd
import numpy as np


# ── 2.1 Conversion en DataFrame ───────────────────────────────────────────────

def users_to_dataframe(users: list) -> pd.DataFrame:
    """Convert list of User objects to a flat Pandas DataFrame."""
    rows = []
    for user in users:
        for log in user.daily_logs:
            rows.append({
                "name"    : user.name,
                "age"     : user.age,
                "goal"    : user.goal,
                "date"    : log.date,
                "steps"   : log.steps,
                "calories": log.calories,
                "workout" : log.workout
            })
    return pd.DataFrame(rows)


# ── 2.2 Nettoyage des données ─────────────────────────────────────────────────

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame :
    - Fill missing steps with median
    - Fill missing calories with median
    - Fill missing workout with most frequent value
    - Fill missing age with median
    - Remove outliers in steps (Z-score > 3)
    """

    # Fill missing numerical values with median
    df["steps"]    = df["steps"].fillna(df["steps"].median())
    df["calories"] = df["calories"].fillna(df["calories"].median())
    df["age"]      = df["age"].fillna(df["age"].median())

    # Fill missing workout with mode
    df["workout"]  = df["workout"].fillna(df["workout"].mode()[0])

    # Remove outliers in steps using Z-score
    mean  = df["steps"].mean()
    std   = df["steps"].std()
    df    = df[np.abs((df["steps"] - mean) / std) < 3]

    # Reset index
    df = df.reset_index(drop=True)

    return df


# ── 2.3 EDA — Analyse exploratoire ───────────────────────────────────────────

def exploratory_analysis(df: pd.DataFrame) -> dict:
    """
    Perform exploratory data analysis.
    Returns a dict of key statistics.
    """

    eda = {}

    # Summary statistics
    eda["summary"] = df[["age", "steps", "calories"]].describe().round(2)

    # Goals distribution
    eda["goals_distribution"] = df["goal"].value_counts()

    # Workouts distribution
    eda["workouts_distribution"] = df["workout"].value_counts()

    # Weekly progress — total steps and calories per week
    df["date"]   = pd.to_datetime(df["date"])
    df["week"]   = df["date"].dt.isocalendar().week
    eda["weekly_steps"]    = df.groupby("week")["steps"].sum()
    eda["weekly_calories"] = df.groupby("week")["calories"].sum()

    # Average steps and calories per goal
    eda["avg_steps_by_goal"]    = df.groupby("goal")["steps"].mean().round(2)
    eda["avg_calories_by_goal"] = df.groupby("goal")["calories"].mean().round(2)

    return eda