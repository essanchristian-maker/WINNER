"""
data/generator.py
=================
Generates synthetic user profiles using NumPy only.
"""

import numpy as np
from datetime import date, timedelta
from models.user import User, DailyLog

rng = np.random.default_rng(seed=42)

GOALS = ["strength","cardio","weight_loss","muscle_gain","flexibility","endurance","stress_relief","general_fitness"]

WORKOUTS = ["Running","Cycling","Swimming","Jump Rope","Rowing","Weight Lifting","Strength Training","Bodyweight","Resistance Bands",
    "Yoga","Pilates","Stretching","HIIT","Circuit Training","Tabata","Football","Basketball","Tennis","Boxing",
    "Dancing"]

FIRST_NAMES = [
    "Jean-Baptiste", "Marie", "Pierre", "Francoise", "Michel",
    "Christiane", "Philippe", "Monique", "Christian", "Isabelle",
    "Jacques", "Sylvie", "Emmanuel", "Christine", "Patrice",
    "Nadege", "Olivier", "Veronique", "Serge", "Celestine"
]

LAST_NAMES = [
    "Kouassi", "Traore", "Diallo", "Kone", "Coulibaly",
    "Ouedraogo", "Bamba", "Toure", "Diarra", "Konate",
    "Yao", "N'Guessan", "Assoumou", "Ake", "Brou",
    "Tape", "Gnagne", "Soro", "Camara", "Doumbia"
]


def african_name() -> str:
    """Generate a random French/African full name."""
    first = str(rng.choice(FIRST_NAMES))
    last  = str(rng.choice(LAST_NAMES))
    return f"{first} {last}"


def generate_logs(n_days: int, start_date: date) -> list:
    #"""Generate n_days of random daily logs with realistic imperfections."""
    logs = []
    for i in range(n_days):

        day = (start_date + timedelta(days=i)).isoformat()

        # Steps with missing values (5%) and outliers (3%)
        steps = int(rng.integers(2000, 12000))
        if rng.random() < 0.05:
            steps = None
        elif rng.random() < 0.03:
            steps = int(rng.integers(50000, 150000))

        # Calories with missing values (5%)
        calories = int(rng.integers(150, 600))
        if rng.random() < 0.05:
            calories = None

        # Workout with missing values (5%)
        workout = str(rng.choice(WORKOUTS))
        if rng.random() < 0.05:
            workout = None

        logs.append(DailyLog(day, steps, calories, workout))
    return logs


def generate_users(n_users: int = 10) -> list:
    """Generate n_users synthetic user profiles."""
    users = []
    for _ in range(n_users):

        # Age with missing values (5%)
        age = int(rng.integers(18, 65)) #age majoritaire CI
        if rng.random() < 0.05:
            age = None

        user = User(
            name = african_name(),
            age  = age,
            goal = str(rng.choice(GOALS))
        )
        n_days     = int(rng.integers(7, 31))
        start_date = date(2026, 1, 1)
        for log in generate_logs(n_days=n_days, start_date=start_date):
            user.add_log(log)
        users.append(user)
    return users