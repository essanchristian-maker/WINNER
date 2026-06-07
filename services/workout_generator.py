"""
services/workout_generator.py
==============================
Generates personalized DAILY workout plans based on:
- Fitness goals
- Past activity trends
Consigne : "Based on your activity, try a 30-min HIIT session today."
"""

WORKOUT_PLANS = {
    "strength": {
        "high":   {"name": "Heavy Lifting",       "duration": 60, "calories": 400},
        "medium": {"name": "Strength Training",   "duration": 45, "calories": 300},
        "low":    {"name": "Bodyweight Training", "duration": 30, "calories": 200},
    },
    "cardio": {
        "high":   {"name": "Running",             "duration": 45, "calories": 450},
        "medium": {"name": "Cycling",             "duration": 40, "calories": 350},
        "low":    {"name": "Jump Rope",           "duration": 20, "calories": 200},
    },
    "weight_loss": {
        "high":   {"name": "HIIT",                "duration": 30, "calories": 400},
        "medium": {"name": "Circuit Training",    "duration": 40, "calories": 350},
        "low":    {"name": "Walking",             "duration": 30, "calories": 150},
    },
    "muscle_gain": {
        "high":   {"name": "Weight Lifting",      "duration": 60, "calories": 420},
        "medium": {"name": "Resistance Bands",    "duration": 45, "calories": 280},
        "low":    {"name": "Bodyweight",          "duration": 30, "calories": 180},
    },
    "flexibility": {
        "high":   {"name": "Advanced Yoga",       "duration": 60, "calories": 250},
        "medium": {"name": "Pilates",             "duration": 45, "calories": 200},
        "low":    {"name": "Stretching",          "duration": 20, "calories": 100},
    },
    "endurance": {
        "high":   {"name": "Long Distance Run",   "duration": 60, "calories": 500},
        "medium": {"name": "Swimming",            "duration": 45, "calories": 380},
        "low":    {"name": "Rowing",              "duration": 30, "calories": 250},
    },
    "stress_relief": {
        "high":   {"name": "Yoga",                "duration": 60, "calories": 200},
        "medium": {"name": "Dancing",             "duration": 40, "calories": 250},
        "low":    {"name": "Stretching",          "duration": 20, "calories": 100},
    },
    "general_fitness": {
        "high":   {"name": "Tabata",              "duration": 30, "calories": 350},
        "medium": {"name": "Circuit Training",    "duration": 40, "calories": 300},
        "low":    {"name": "Walking",             "duration": 30, "calories": 150},
    },
}


def get_activity_level(daily_logs: list) -> str:
    """
    Determine activity level based on last 7 logs.
    Returns 'high', 'medium' or 'low'.
    """
    if not daily_logs:
        return "low"

    recent      = daily_logs[-7:]
    valid_steps = [log.steps for log in recent if log.steps is not None]

    if not valid_steps:
        return "low"

    avg_steps = sum(valid_steps) / len(valid_steps)

    if avg_steps >= 8000:
        return "high"
    elif avg_steps >= 4000:
        return "medium"
    else:
        return "low"


class WorkoutGenerator:
    """
    Generates a personalized daily workout plan
    based on user goal and recent activity level.
    """

    def __init__(self, user):
        self.user           = user
        self.activity_level = get_activity_level(user.daily_logs)

    def generate(self) -> dict:
        """Generate today's workout plan for the user."""

        goal  = self.user.goal
        level = self.activity_level

        if goal not in WORKOUT_PLANS:
            goal = "general_fitness"

        workout = WORKOUT_PLANS[goal][level]

        return {
            "user"           : self.user.name,
            "goal"           : goal,
            "activity_level" : level,
            "workout"        : workout["name"],
            "duration_min"   : workout["duration"],
            "calories_target": workout["calories"],
            "message"        : self._build_message(workout)
        }

    def _build_message(self, workout: dict) -> str:
        """Build a personalized recommendation message."""
        return (
            f"Based on your activity, try a "
            f"{workout['duration']}-min "
            f"{workout['name']} session today."
        )