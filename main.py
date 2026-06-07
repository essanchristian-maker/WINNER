"""
main.py
=======
FitTracker — AI-Generated Fitness Tracker
==========================================
Entry point that ties all steps together :
1. Load/Generate user profiles
2. Generate personalized daily workout plans
3. Statistical analysis (SciPy)
4. Analyze and visualize data (Pandas + Matplotlib)
"""

import json
import os
from data.file_handler          import load_users, save_users
from data.generator             import generate_users
from services.workout_generator import WorkoutGenerator
from services.data_analysis     import users_to_dataframe, clean_dataframe, exploratory_analysis
from services.stats_service     import (
    anova_calories_by_workout,
    linear_regression_steps,
    paired_ttest_before_after
)
from visualizations.charts      import (
    plot_steps_and_calories,
    plot_workout_frequency
)


def main():
    print("=" * 50)
    print("   FitTracker — AI-Generated Fitness Tracker")
    print("=" * 50)

    # ── Step 1 : Load or generate user profiles ───────────────────────────────
    print("\n[Step 1] Loading user profiles...")
    users = load_users()
    if not users:
        print("  No users found. Generating 50 users...")
        users = generate_users(n_users=50)
        save_users(users)
    print(f"   {len(users)} users loaded.")

    # ── Step 2 : Generate personalized daily workout plans ────────────────────
    print("\n[Step 2] Generating personalized workout plans...")
    recommendations = []
    for user in users:
        plan = WorkoutGenerator(user).generate()
        recommendations.append(plan)

    # Save recommendations
    os.makedirs("data", exist_ok=True)
    with open("data/recommendations.json", "w") as f:
        json.dump(recommendations, f, indent=4)

    print(f"   {len(recommendations)} workout plans generated.")
    print(f"\n  Sample recommendation :")
    print(f"  → {recommendations[0]['message']}")

    # ── Step 3 : Statistical analysis (SciPy) ────────────────────────────────
    print("\n[Step 3] Running statistical analysis...")
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())

    # ANOVA
    anova = anova_calories_by_workout(df_clean)
    print(f"\n  ANOVA — {anova['conclusion']}")
    print(f"  F-statistic : {anova['f_statistic']} | P-value : {anova['p_value']}")

    # Linear Regression — per user
    user_name  = df_clean["name"].value_counts().index[0]
    df_user    = df_clean[df_clean["name"] == user_name].copy()
    regression = linear_regression_steps(df_user)
    print(f"\n  Linear Regression ({user_name}) — {regression['conclusion']}")
    print(f"  Predicted steps next 7 days : {regression['predicted_steps_next_7_days']}")

    # Paired T-test — per user
    ttest = paired_ttest_before_after(df_user)
    print(f"\n  T-test ({user_name}) — {ttest['conclusion']}")
    print(f"  Mean before : {ttest['mean_before']} | Mean after : {ttest['mean_after']}")

    # ── Step 4 : Analyze and visualize data ───────────────────────────────────
    print("\n[Step 4] Analyzing and visualizing data...")

    # Pandas weekly progress
    eda = exploratory_analysis(df_clean.copy())
    print(f"\n  Weekly Steps :")
    print(eda["weekly_steps"].to_string())
    print(f"\n  Weekly Calories :")
    print(eda["weekly_calories"].to_string())

    # Visualizations
    plot_steps_and_calories(df_clean, user_name)
    plot_workout_frequency(df_clean)

    print("\n" + "=" * 50)
    print("   FitTracker analysis complete !")
    print("   Charts saved to visualizations/")
    print("   Recommendations saved to data/recommendations.json")
    print("=" * 50)


if __name__ == "__main__":
    main()