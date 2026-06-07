"""
test_step3.py
=============
Tests Step 3 : Pandas data analysis + cleaning + EDA.
"""

from data.file_handler       import load_users, save_users
from data.generator          import generate_users
from services.data_analysis  import users_to_dataframe, clean_dataframe, exploratory_analysis


def main():
    print("=============================")
    print("  FitTracker — Step 3 Test   ")
    print("=============================")

    # 1. Load users
    users = load_users()
    if not users:
        print("No users found. Generating...")
        users = generate_users(n_users=50)
        save_users(users)

    # 2. Convert to DataFrame
    print("\n--- 2.1 Converting to DataFrame ---")
    df = users_to_dataframe(users)
    print(f"  Shape        : {df.shape}")
    print(f"  Columns      : {df.columns.tolist()}")
    print(f"\n{df.head()}")

    # 3. Missing values before cleaning
    print("\n--- 2.2 Missing values BEFORE cleaning ---")
    print(df.isnull().sum())

    # 4. Clean DataFrame
    df_clean = clean_dataframe(df.copy())

    # 5. Missing values after cleaning
    print("\n--- Missing values AFTER cleaning ---")
    print(df_clean.isnull().sum())
    print(f"\n  Rows before : {len(df)}")
    print(f"  Rows after  : {len(df_clean)}")

    # 6. EDA
    print("\n--- 2.3 Exploratory Data Analysis ---")
    eda = exploratory_analysis(df_clean.copy())

    print("\nSummary Statistics :")
    print(eda["summary"])

    print("\nGoals Distribution :")
    print(eda["goals_distribution"])

    print("\nWorkouts Distribution :")
    print(eda["workouts_distribution"])

    print("\nWeekly Steps :")
    print(eda["weekly_steps"])

    print("\nWeekly Calories :")
    print(eda["weekly_calories"])

    print("\nAvg Steps by Goal :")
    print(eda["avg_steps_by_goal"])

    print("\nAvg Calories by Goal :")
    print(eda["avg_calories_by_goal"])


if __name__ == "__main__":
    main()