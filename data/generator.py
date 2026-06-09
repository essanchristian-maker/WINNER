"""
data/generator.py
=================
Ce fichier génère des profils utilisateurs synthétiques
en utilisant uniquement NumPy.
Les données simulées reproduisent des comportements réels :
valeurs manquantes, valeurs aberrantes, journaux irréguliers.
"""
# Ce qui a été généré :
# - 500 profils utilisateurs avec prénoms français et noms africains
# - 8 objectifs fitness différents (strength, cardio, weight_loss...)
# - 20 types d'entraînements (Running, HIIT, Yoga, Football...)
# - Entre 7 et 30 journaux quotidiens par utilisateur
# - Des pas entre 2 000 et 12 000 par jour
# - Des calories entre 150 et 600 par jour
#
# Imperfections introduites intentionnellement :
# - 5% de valeurs manquantes sur steps, calories, workout et age
# - 3% de valeurs aberrantes sur steps (entre 50 000 et 150 000)
#
# Toutes les données sont sauvegardées dans data/users.json



import numpy as np
from datetime import date, timedelta
from models.user import User, DailyLog

# Générateur de nombres aléatoires avec seed fixe
# seed=42 garantit que les mêmes données sont générées
# à chaque exécution — important pour la reproductibilité
rng = np.random.default_rng(seed=42)


# ── Listes de données ──────────────────────────────────────────────────────────

# Les 8 objectifs fitness disponibles dans FitTracker
GOALS = [
    "strength", "cardio", "weight_loss", "muscle_gain",
    "flexibility", "endurance", "stress_relief", "general_fitness"
]

# Les 20 types d'entraînements disponibles
# Organisés par catégorie : Cardio, Force, Flexibilité, HIIT, Sport
WORKOUTS = [
    "Running", "Cycling", "Swimming", "Jump Rope", "Rowing",
    "Weight Lifting", "Strength Training", "Bodyweight", "Resistance Bands",
    "Yoga", "Pilates", "Stretching",
    "HIIT", "Circuit Training", "Tabata",
    "Football", "Basketball", "Tennis", "Boxing", "Dancing"
]

# 20 prénoms français — typiques de la Côte d'Ivoire francophone
FIRST_NAMES = [
    "Jean-Baptiste", "Marie", "Pierre", "Francoise", "Michel",
    "Christiane", "Philippe", "Monique", "Christian", "Isabelle",
    "Jacques", "Sylvie", "Emmanuel", "Christine", "Patrice",
    "Nadege", "Olivier", "Veronique", "Serge", "Celestine"
]

# 20 noms de famille africains — majoritairement ivoiriens
LAST_NAMES = [
    "Kouassi", "Traore", "Diallo", "Kone", "Coulibaly",
    "Ouedraogo", "Bamba", "Toure", "Diarra", "Konate",
    "Yao", "N'Guessan", "Assoumou", "Ake", "Brou",
    "Tape", "Gnagne", "Soro", "Camara", "Doumbia"
]


# ── Fonction : générer un nom français/africain ────────────────────────────────

def african_name() -> str:
    """Génère un nom complet aléatoire français/africain."""
    # Pioche un prénom et un nom dans les listes avec NumPy
    first = str(rng.choice(FIRST_NAMES))
    last  = str(rng.choice(LAST_NAMES))
    return f"{first} {last}"


# ── Fonction : générer les journaux quotidiens ─────────────────────────────────

def generate_logs(n_days: int, start_date: date) -> list:
    """
    Génère n_days journaux quotidiens avec des imperfections réalistes.
    Simule des données réelles : valeurs manquantes et valeurs aberrantes.
    """
    logs = []

    for i in range(n_days):

        # Calcule la date du jour en ajoutant i jours à la date de départ
        day = (start_date + timedelta(days=i)).isoformat()

        # ── Génération des pas ──────────────────────────────────────────────
        # Valeur normale entre 2000 et 12000 pas
        steps = int(rng.integers(2000, 12000))

        # 5% de chance que les pas soient manquants (non renseignés)
        if rng.random() < 0.05:
            steps = None

        # 3% de chance d'avoir une valeur aberrante (outlier)
        # ex: 80 000 pas — clairement irréaliste
        elif rng.random() < 0.03:
            steps = int(rng.integers(50000, 150000))

        # ── Génération des calories ─────────────────────────────────────────
        # Valeur normale entre 150 et 600 calories
        calories = int(rng.integers(150, 600))

        # 5% de chance que les calories soient manquantes
        if rng.random() < 0.05:
            calories = None

        # ── Génération du workout ───────────────────────────────────────────
        # Sélectionne un entraînement aléatoire dans la liste
        workout = str(rng.choice(WORKOUTS))

        # 5% de chance que le workout soit manquant
        if rng.random() < 0.05:
            workout = None

        # Crée le journal du jour et l'ajoute à la liste
        logs.append(DailyLog(day, steps, calories, workout))

    return logs


# ── Fonction : générer les profils utilisateurs ────────────────────────────────

def generate_users(n_users: int = 500) -> list:
    """
    Génère n_users profils utilisateurs synthétiques.
    Chaque profil contient un nom, un âge, un objectif
    et entre 7 et 30 journaux quotidiens.
    """
    users = []

    for _ in range(n_users):

        # Génère un âge entre 18 et 65 ans
        # Correspond à la tranche d'âge majoritaire en Côte d'Ivoire
        age = int(rng.integers(18, 65))

        # 5% de chance que l'âge soit manquant
        if rng.random() < 0.05:
            age = None

        # Crée l'utilisateur avec un nom, un âge et un objectif aléatoires
        user = User(
            name = african_name(),
            age  = age,
            goal = str(rng.choice(GOALS))
        )

        # Nombre de journaux variable entre 7 et 30 jours
        # Simule des utilisateurs plus ou moins actifs
        n_days     = int(rng.integers(7, 31))
        start_date = date(2026, 1, 1)

        # Génère les journaux et les ajoute au profil
        for log in generate_logs(n_days=n_days, start_date=start_date):
            user.add_log(log)

        users.append(user)

    return users