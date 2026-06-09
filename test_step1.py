"""
test_step1.py
=============
Ce fichier teste la Question 1 du sujet FitTracker :
- Création des profils utilisateurs avec NumPy
- Persistance des données en JSON
- Vérification des données générées
"""

# ── BLOC 1 : Importation des librairies ───────────────────────────────────────

import json                            # formatage et affichage du JSON
from data.generator    import generate_users  # génération des profils NumPy
from data.file_handler import save_users, load_users  # persistance JSON


def main():
    print("=" * 50)
    print("   FitTracker — Question 1 : Profils Utilisateurs")
    print("=" * 50)

    # ── BLOC 2 : Collecte des données ─────────────────────────────────────────
    # Génération synthétique de 500 profils utilisateurs avec NumPy
    # Chaque profil contient : nom, âge, objectif, journaux quotidiens
    # seed=42 garantit les mêmes données à chaque exécution

    print("\n[Bloc 2] Génération des profils utilisateurs...")
    users = generate_users(n_users=500)

    # Affichage de chaque profil généré
    for u in users:
        print(f"  → {u.name} | Age: {u.age} | Goal: {u.goal} | Logs: {len(u.daily_logs)}")

    # ── BLOC 3 : Aperçu du dataset généré ────────────────────────────────────
    print("\n[Bloc 3] Aperçu du dataset généré")
    print("-" * 40)

    # Distribution des objectifs fitness
    # Compte combien d'utilisateurs ont chaque objectif
    goals_count = {}
    for u in users:
        goals_count[u.goal] = goals_count.get(u.goal, 0) + 1
    print(f"\n  Distribution des objectifs : {goals_count}")

    # Distribution des entraînements
    # Compte combien de fois chaque workout apparaît dans les logs
    workouts_count = {}
    for u in users:
        for log in u.daily_logs:
            if log.workout:
                workouts_count[log.workout] = workouts_count.get(log.workout, 0) + 1
    print(f"\n  Distribution des entraînements : {workouts_count}")

    # Valeurs manquantes intentionnellement introduites (5%)
    # Simulent des données réelles incomplètes
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

    print(f"\n  Valeurs manquantes :")
    print(f"  - Steps    : {missing_steps}")
    print(f"  - Calories : {missing_calories}")
    print(f"  - Ages     : {missing_age}")

    # ── Sauvegarde en JSON ────────────────────────────────────────────────────
    # Tous les profils sont sauvegardés dans data/users.json
    # pour être rechargés à chaque démarrage de l'application
    print("\n[Sauvegarde] Écriture dans data/users.json...")
    save_users(users)

    # ── Rechargement depuis JSON ──────────────────────────────────────────────
    # Vérifie que la sauvegarde et le chargement fonctionnent correctement
    print("\n[Rechargement] Lecture depuis data/users.json...")
    loaded_users = load_users()
    print(f"✅ Total utilisateurs rechargés : {len(loaded_users)}")

    # ── Exemple de profil au format JSON ─────────────────────────────────────
    # Affiche le premier utilisateur dans le format JSON exact
    # demandé par le sujet :
    # {"name": "Alice", "age": 30, "goal": "strength", "daily_logs": [...]}
    print(f"\n[Exemple] Premier profil au format JSON :")
    print(json.dumps(loaded_users[0].to_dict(), indent=4))


if __name__ == "__main__":
    main()