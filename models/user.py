"""
models/user.py
==============
Defines the User and DailyLog classes.
"""

class DailyLog:
    def __init__(self, date, steps, calories, workout):
        self.date     = date
        self.steps    = steps
        self.calories = calories
        self.workout  = workout

    def to_dict(self):
        return {
            "date"    : self.date,
            "steps"   : self.steps,
            "calories": self.calories,
            "workout" : self.workout
        }


class User:
    def __init__(self, name, age, goal):
        self.name       = name
        self.age        = age
        self.goal       = goal
        self.daily_logs = []

    def add_log(self, log: DailyLog):
        self.daily_logs.append(log)

    def to_dict(self):
        return {
            "name"      : self.name,
            "age"       : self.age,
            "goal"      : self.goal,
            "daily_logs": [log.to_dict() for log in self.daily_logs]
        }

    @classmethod
    def from_dict(cls, data: dict):
        user = cls(data["name"], data["age"], data["goal"])
        for log in data["daily_logs"]:
            user.add_log(DailyLog(
                log["date"],
                log["steps"],
                log["calories"],
                log["workout"]
            ))
        return user