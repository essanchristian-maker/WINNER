"""
test_step5.py
=============
Tests Step 5 : Matplotlib visualizations.
Point 4 du sujet :
- Line plots : steps and calories over time
- Bar plots : workout frequency
"""

from data.file_handler      import load_users, save_users
from data.generator         import generate_users
from services.data_analysis import users_to_dataframe, clean_dataframe
from visualizations.charts  import (
    plot_steps_and_calories,
    plot_workout_frequency
)


def main():
    print("=============================")
    print("  FitTracker — Step 5 Test   ")
    print("     Visualizations          ")
    print("=============================")

    # 1. Load and prepare data
    users = load_users()
    if not users:
        print("No users found. Generating...")
        users = generate_users(n_users=50)
        save_users(users)

    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())

    # 2. Select user with most logs
    user_name = df_clean["name"].value_counts().index[0]
    print(f"\nSelected user : {user_name} ({len(df_clean[df_clean['name'] == user_name])} logs)")

    # 3. Line plots — steps and calories over time
    print("\n--- Line plots : Steps and Calories Over Time ---")
    plot_steps_and_calories(df_clean, user_name)

    # 4. Bar plot — workout frequency
    print("\n--- Bar plot : Workout Frequency ---")
    plot_workout_frequency(df_clean)

    print("\n All visualizations saved to visualizations/")


if __name__ == "__main__":
    main()