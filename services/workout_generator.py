"""
services/workout_generator.py
==============================
Ce fichier implémente le moteur de recommandation de FitTracker.
Il génère un plan d'entraînement quotidien personnalisé basé sur :
- L'objectif fitness de l'utilisateur (goal)
- Son niveau d'activité récent (7 derniers jours)

Consigne exacte du sujet :
"Based on your activity, try a 30-min HIIT session today."
"""


# ── Table des plans d'entraînement ────────────────────────────────────────────
# Cette table contient tous les plans possibles organisés par :
# - Objectif fitness (strength, cardio, weight_loss...)
# - Niveau d'activité (high, medium, low)
#
# Structure : WORKOUT_PLANS[goal][level] = {name, duration, calories}
# Cela donne 8 objectifs × 3 niveaux = 24 combinaisons possibles

WORKOUT_PLANS = {
    # Objectif : renforcement musculaire
    "strength": {
        "high":   {"name": "Heavy Lifting",       "duration": 60, "calories": 400},
        "medium": {"name": "Strength Training",   "duration": 45, "calories": 300},
        "low":    {"name": "Bodyweight Training", "duration": 30, "calories": 200},
    },
    # Objectif : cardio
    "cardio": {
        "high":   {"name": "Running",             "duration": 45, "calories": 450},
        "medium": {"name": "Cycling",             "duration": 40, "calories": 350},
        "low":    {"name": "Jump Rope",           "duration": 20, "calories": 200},
    },
    # Objectif : perte de poids
    "weight_loss": {
        "high":   {"name": "HIIT",                "duration": 30, "calories": 400},
        "medium": {"name": "Circuit Training",    "duration": 40, "calories": 350},
        "low":    {"name": "Walking",             "duration": 30, "calories": 150},
    },
    # Objectif : prise de masse musculaire
    "muscle_gain": {
        "high":   {"name": "Weight Lifting",      "duration": 60, "calories": 420},
        "medium": {"name": "Resistance Bands",    "duration": 45, "calories": 280},
        "low":    {"name": "Bodyweight",          "duration": 30, "calories": 180},
    },
    # Objectif : flexibilité
    "flexibility": {
        "high":   {"name": "Advanced Yoga",       "duration": 60, "calories": 250},
        "medium": {"name": "Pilates",             "duration": 45, "calories": 200},
        "low":    {"name": "Stretching",          "duration": 20, "calories": 100},
    },
    # Objectif : endurance
    "endurance": {
        "high":   {"name": "Long Distance Run",   "duration": 60, "calories": 500},
        "medium": {"name": "Swimming",            "duration": 45, "calories": 380},
        "low":    {"name": "Rowing",              "duration": 30, "calories": 250},
    },
    # Objectif : gestion du stress
    "stress_relief": {
        "high":   {"name": "Yoga",                "duration": 60, "calories": 200},
        "medium": {"name": "Dancing",             "duration": 40, "calories": 250},
        "low":    {"name": "Stretching",          "duration": 20, "calories": 100},
    },
    # Objectif : forme générale
    "general_fitness": {
        "high":   {"name": "Tabata",              "duration": 30, "calories": 350},
        "medium": {"name": "Circuit Training",    "duration": 40, "calories": 300},
        "low":    {"name": "Walking",             "duration": 30, "calories": 150},
    },
}


# ── Fonction : déterminer le niveau d'activité ────────────────────────────────

def get_activity_level(daily_logs: list) -> str:
    """
    Détermine le niveau d'activité de l'utilisateur
    en analysant ses 7 derniers journaux quotidiens.
    Retourne 'high', 'medium' ou 'low'.

    Seuils utilisés :
    - high   : moyenne >= 8000 pas/jour (très actif)
    - medium : moyenne >= 4000 pas/jour (modérément actif)
    - low    : moyenne < 4000 pas/jour  (peu actif)
    """

    # Si l'utilisateur n'a aucun log, on le considère inactif
    if not daily_logs:
        return "low"

    # On analyse uniquement les 7 derniers jours
    recent = daily_logs[-7:]

    # On filtre les valeurs None (données manquantes)
    valid_steps = [log.steps for log in recent if log.steps is not None]

    # Si tous les pas sont manquants, on considère l'utilisateur inactif
    if not valid_steps:
        return "low"

    # Calcul de la moyenne des pas sur les 7 derniers jours
    avg_steps = sum(valid_steps) / len(valid_steps)

    # Détermination du niveau selon les seuils
    if avg_steps >= 8000:
        return "high"
    elif avg_steps >= 4000:
        return "medium"
    else:
        return "low"


# ── Classe : WorkoutGenerator ─────────────────────────────────────────────────
# C'est le cœur du moteur de recommandation de FitTracker.
# Il combine l'objectif fitness et le niveau d'activité
# pour sélectionner le plan d'entraînement le plus adapté.

class WorkoutGenerator:
    """
    Génère un plan d'entraînement quotidien personnalisé
    basé sur l'objectif et le niveau d'activité de l'utilisateur.
    """

    def __init__(self, user):
        # Stocke l'utilisateur
        self.user = user

        # Calcule son niveau d'activité dès l'initialisation
        # en analysant ses 7 derniers journaux
        self.activity_level = get_activity_level(user.daily_logs)

    def generate(self) -> dict:
        """
        Génère le plan d'entraînement du jour pour l'utilisateur.
        Retourne un dictionnaire avec tous les détails du plan.
        """

        goal  = self.user.goal
        level = self.activity_level

        # Si l'objectif n'est pas reconnu, on utilise general_fitness
        if goal not in WORKOUT_PLANS:
            goal = "general_fitness"

        # Sélectionne le workout correspondant à l'objectif et au niveau
        workout = WORKOUT_PLANS[goal][level]

        # Retourne le plan complet avec le message de recommandation
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
        """
        Construit le message de recommandation personnalisé.
        Format exact demandé par le sujet :
        "Based on your activity, try a X-min Y session today."
        """
        return (
            f"Based on your activity, try a "
            f"{workout['duration']}-min "
            f"{workout['name']} session today."
        )