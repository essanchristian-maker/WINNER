"""
data/file_handler.py
====================
Handles saving and loading user data to/from JSON files.
"""

import json
import os
from models.user import User

DATA_PATH = os.path.join(os.path.dirname(__file__), "users.json")


def save_users(users: list):
    """Save list of User objects to JSON file."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump([u.to_dict() for u in users], f, indent=4)
    print(f"✅ {len(users)} users saved to {DATA_PATH}")


def load_users() -> list:
    """Load list of User objects from JSON file."""
    if not os.path.exists(DATA_PATH):
        print("⚠️ No data file found. Starting fresh.")
        return []
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    print(f"✅ {len(data)} users loaded from {DATA_PATH}")
    return [User.from_dict(u) for u in data]