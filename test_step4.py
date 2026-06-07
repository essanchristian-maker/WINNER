"""
test_step4.py
=============
Tests Step 4 : SciPy statistical analysis per user.
- ANOVA : calories by workout type
- Linear Regression : predict future steps for a specific user
- Paired T-test : before/after program for a specific user
"""

from data.file_handler        import load_users, save_users
from data.generator           import generate_users
from services.data_analysis   import users_to_dataframe, clean_dataframe
from services.stats_service   import (
    anova_calories_by_workout,
    linear_regression_steps,
    paired_ttest_before_after
)


def main():
    print("=============================")
    print("  FitTracker — Step 4 Test   ")
    print("  SciPy Statistical Analysis ")
    print("=============================")

    # 1. Load and prepare data
    users = load_users()
    if not users:
        print("No users found. Generating...")
        users = generate_users(n_users=50)
        save_users(users)

    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())

    # 2. ANOVA — on all data (workout types comparison)
    print("\n--- ANOVA : Calories by Workout Type (all users) ---")
    anova = anova_calories_by_workout(df_clean)
    print(f"  Question    : {anova['question']}")
    print(f"  F-statistic : {anova['f_statistic']}")
    print(f"  P-value     : {anova['p_value']}")
    print(f"  Conclusion  : {anova['conclusion']}")

    # 3. Select user with most logs for individual analysis
    user_name = df_clean["name"].value_counts().index[0]
    df_user   = df_clean[df_clean["name"] == user_name].copy()
    print(f"\n--- Analyzing user : {user_name} ({len(df_user)} logs) ---")

    # 4. Linear Regression — per user
    print("\n--- Linear Regression : Predict Future Steps ---")
    regression = linear_regression_steps(df_user)
    print(f"  Question    : {regression['question']}")
    print(f"  Slope       : {regression['slope']}")
    print(f"  R-squared   : {regression['r_squared']}")
    print(f"  P-value     : {regression['p_value']}")
    print(f"  Predicted steps next 7 days : {regression['predicted_steps_next_7_days']}")
    print(f"  Conclusion  : {regression['conclusion']}")

    # 5. Paired T-test — per user
    print("\n--- Paired T-test : Before/After Program ---")
    ttest = paired_ttest_before_after(df_user)
    print(f"  Question    : {ttest['question']}")
    print(f"  Mean before : {ttest['mean_before']}")
    print(f"  Mean after  : {ttest['mean_after']}")
    print(f"  T-statistic : {ttest['t_statistic']}")
    print(f"  P-value     : {ttest['p_value']}")
    print(f"  Conclusion  : {ttest['conclusion']}")


if __name__ == "__main__":
    main()