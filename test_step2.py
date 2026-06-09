"""
test_step2.py
=============
Ce fichier teste la Question 2 du sujet FitTracker :
Génération de plans d'entraînement quotidiens personnalisés.
Consigne exacte du sujet :
"Based on your activity, try a 30-min HIIT session today."
"""

# ── BLOC 1 : Importation des librairies ───────────────────────────────────────

import json                                        # sauvegarde en JSON
import os                                          # gestion des dossiers
from data.file_handler          import load_users, save_users   # persistance
from data.generator             import generate_users           # génération
from services.workout_generator import WorkoutGenerator         # recommandation


def main():
    print("=" * 50)
    print("  FitTracker — Question 2 : Plans d'Entraînement")
    print("=" * 50)

    # ── BLOC 2 : Collecte des données ─────────────────────────────────────────
    # Chargement des profils depuis data/users.json
    # Si le fichier n'existe pas, on génère 500 profils avec NumPy

    print("\n[Bloc 2] Chargement des profils utilisateurs...")
    users = load_users()
    if not users:
        print("Aucun utilisateur trouvé. Génération en cours...")
        users = generate_users(n_users=500)
        save_users(users)
    print(f"✅ {len(users)} profils chargés.")

    # ── Génération des plans d'entraînement ───────────────────────────────────
    # Pour chaque utilisateur, WorkoutGenerator analyse :
    # 1. Son objectif fitness (goal)
    # 2. Son niveau d'activité des 7 derniers jours (high/medium/low)
    # Et génère une recommandation personnalisée

    print(f"\n[Question 2] Génération des plans ({len(users)} utilisateurs)\n")
    recommendations = []

    for user in users:
        # Crée un générateur pour cet utilisateur
        # et génère son plan du jour
        plan = WorkoutGenerator(user).generate()
        recommendations.append(plan)

        # Affiche le nom, l'objectif et la recommandation
        print(f"  {plan['user']} ({plan['goal']})")
        print(f"  → {plan['message']}")
        print()

    # ── Vue d'ensemble des recommandations ───────────────────────────────────
    # Compte combien d'utilisateurs ont chaque niveau d'activité
    # et quels workouts ont été assignés

    print("--- Vue d'ensemble ---")

    # Distribution des niveaux d'activité
    levels = {}
    for r in recommendations:
        levels[r["activity_level"]] = levels.get(r["activity_level"], 0) + 1

    # Distribution des workouts assignés
    workouts = {}
    for r in recommendations:
        workouts[r["workout"]] = workouts.get(r["workout"], 0) + 1

    print(f"\n  Niveaux d'activité  : {levels}")
    print(f"  Workouts assignés   : {workouts}")

    # ── Sauvegarde des recommandations en JSON ────────────────────────────────
    # Toutes les recommandations sont sauvegardées dans
    # data/recommendations.json pour être réutilisées
    os.makedirs("data", exist_ok=True)
    with open("data/recommendations.json", "w") as f:
        json.dump(recommendations, f, indent=4)

    print(f"\n✅ Recommandations sauvegardées dans data/recommendations.json")


if __name__ == "__main__":
    main()