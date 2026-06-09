"""
models/user.py
==============
Ce fichier définit la structure des données de FitTracker.
Il contient deux classes principales :
- DailyLog : représente un journal d'activité d'une journée
- User     : représente un profil utilisateur complet
"""


# ── Classe DailyLog ────────────────────────────────────────────────────────────
# Un DailyLog représente ce qu'un utilisateur a fait pendant UNE journée :
# combien de pas il a fait, combien de calories il a brûlées,
# et quel entraînement il a réalisé.

class DailyLog:
    def __init__(self, date, steps, calories, workout):
        self.date     = date   # La date du journal (format : YYYY-MM-DD, ex: 2026-01-15)
        self.steps    = steps   # Nombre de pas effectués ce jour-là (peut être None si non renseigné)
        self.calories = calories   # Calories brûlées ce jour-là (peut être None si non renseigné)
        self.workout  = workout   # Type d'entraînement réalisé (ex: Running, HIIT, Yoga...)

    def to_dict(self):
        # Convertit le journal en dictionnaire Python
        # pour pouvoir le sauvegarder dans un fichier JSON
        return {
            "date"    : self.date,
            "steps"   : self.steps,
            "calories": self.calories,
            "workout" : self.workout
        }


# ── Classe User ────────────────────────────────────────────────────────────────
# Un User représente un profil utilisateur complet.
# Il contient ses informations personnelles et tous ses journaux quotidiens.

class User:
    def __init__(self, name, age, goal):
        # Nom complet de l'utilisateur (ex: Marie Kouassi)
        self.name = name  # Nom complet de l'utilisateur (ex: Marie Kouassi)
        self.age  = age   # Âge de l'utilisateur (peut être None si non renseigné)
        self.goal = goal   # Objectif fitness de l'utilisateur  # (ex: strength, cardio, weight_loss, muscle_gain...)
        self.daily_logs = []   # Liste de tous les journaux quotidiens de l'utilisateur
                                # Au départ elle est vide — les journaux sont ajoutés avec add_log()



    def add_log(self, log: DailyLog):
        # Ajoute un nouveau journal quotidien à la liste de l'utilisateur
        # Exemple : user.add_log(DailyLog("2026-01-15", 8000, 400, "Running"))
        self.daily_logs.append(log)

    def to_dict(self):
        return {
            "name"      : self.name,
            "age"       : self.age,
            "goal"      : self.goal,
            "daily_logs": [log.to_dict() for log in self.daily_logs]
        }
    # Convertit le profil utilisateur complet en dictionnaire Python
        # pour pouvoir le sauvegarder dans un fichier JSON
        # Chaque journal quotidien est aussi converti en dictionnaire

    @classmethod
    def from_dict(cls, data: dict):
        # Recrée un objet User depuis un dictionnaire chargé depuis le JSON
        # C'est l'opération inverse de to_dict()
        # Utilisé au démarrage pour recharger les profils sauvegardés

        # Crée l'utilisateur avec ses informations de base
        user = cls(data["name"], data["age"], data["goal"])

        # Recrée chaque journal quotidien et l'ajoute à l'utilisateur
        for log in data["daily_logs"]:
            user.add_log(DailyLog(
                log["date"],
                log["steps"],
                log["calories"],
                log["workout"]
            ))
        return user