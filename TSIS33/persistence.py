import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "normal"
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []

    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_leaderboard(scores):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


def add_score(name, score, distance):
    scores = load_leaderboard()

    scores.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]

    save_leaderboard(scores)