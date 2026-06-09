"""
test_step1.py
=============
Tests Step 1 : User profiles simulation and JSON persistence.
"""

import json
from data.generator    import generate_users
from data.file_handler import save_users, load_users


def main():
    print("=============================")
    print("   FitTracker — Step 1 Test  ")
    print("=============================")

    # 1. Simulate 500 users automatically with NumPy
    print("\n--- Generating 20 simulated users (NumPy) ---")
    users = generate_users(n_users=500)
    for u in users:
        print(f"  → {u.name} | Age: {u.age} | Goal: {u.goal} | Logs: {len(u.daily_logs)}")

    # 2. Stats on generated data
    print("\n--- Dataset Overview ---")
    goals_count = {}
    for u in users:
        goals_count[u.goal] = goals_count.get(u.goal, 0) + 1
    print(f"  Goals distribution : {goals_count}")

    workouts_count = {}
    for u in users:
        for log in u.daily_logs:
            if log.workout:
                workouts_count[log.workout] = workouts_count.get(log.workout, 0) + 1
    print(f"  Workouts distribution : {workouts_count}")

    missing_steps = sum(
        1 for u in users
        for log in u.daily_logs
        if log.steps is None
    )
    missing_calories = sum(
        1 for u in users
        for log in u.daily_logs
        if log.calories is None
    )
    missing_age = sum(1 for u in users if u.age is None)
    print(f"  Missing steps    : {missing_steps}")
    print(f"  Missing calories : {missing_calories}")
    print(f"  Missing ages     : {missing_age}")

    # 3. Save to JSON
    save_users(users)

    # 4. Reload from JSON
    loaded_users = load_users()
    print(f"\n Total users loaded : {len(loaded_users)}")

    # 5. Sample user JSON
    print(f"\nSample user JSON :")
    print(json.dumps(loaded_users[0].to_dict(), indent=4))


if __name__ == "__main__":
    main()