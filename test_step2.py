"""
test_step2.py
=============
Tests Step 2 : Daily personalized workout plan generation.
Consigne : "Based on your activity, try a 30-min HIIT session today."
"""

import json
import os
from data.file_handler          import load_users, save_users
from data.generator             import generate_users
from services.workout_generator import WorkoutGenerator


def main():
    print("=============================")
    print("  FitTracker — Step 2 Test   ")
    print("=============================")

    # 1. Load users from JSON
    users = load_users()
    if not users:
        print("No users found. Generating...")
        users = generate_users(n_users=500)
        save_users(users)

    # 2. Generate daily workout plan for each user
    print(f"\n--- Today's workout plans ({len(users)} users) ---\n")
    recommendations = []

    for user in users:
        plan = WorkoutGenerator(user).generate()
        recommendations.append(plan)
        print(f"  {plan['user']} ({plan['goal']})")
        print(f"  → {plan['message']}")
        print()

    # 3. Overview
    print("--- Overview ---")
    levels   = {}
    workouts = {}
    for r in recommendations:
        levels[r["activity_level"]]  = levels.get(r["activity_level"], 0) + 1
        workouts[r["workout"]]       = workouts.get(r["workout"], 0) + 1

    print(f"  Activity levels   : {levels}")
    print(f"  Workouts assigned : {workouts}")

    # 4. Save recommendations to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/recommendations.json", "w") as f:
        json.dump(recommendations, f, indent=4)
    print(f"\n Recommendations saved to data/recommendations.json")


if __name__ == "__main__":
    main()