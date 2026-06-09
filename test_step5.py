"""
test_step5.py
=============
Ce fichier teste la Question 4 du sujet FitTracker :
Analyse et visualisation des données avec Matplotlib.

Les 2 visualisations créées :
- Line plot : évolution des pas et calories dans le temps
- Bar plot  : fréquence des types d'entraînements
"""

# ── BLOC 1 : Importation des librairies ───────────────────────────────────────

from data.file_handler      import load_users, save_users
from data.generator         import generate_users
from services.data_analysis import users_to_dataframe, clean_dataframe
from visualizations.charts  import (
    plot_steps_and_calories,
    plot_workout_frequency
)


def main():
    print("=" * 50)
    print("  FitTracker — Question 4 : Visualisations")
    print("=" * 50)

    # ── BLOC 2 : Collecte et préparation des données ──────────────────────────
    print("\n[Bloc 2] Chargement et préparation des données...")
    users = load_users()
    if not users:
        print("Aucun utilisateur trouvé. Génération en cours...")
        users = generate_users(n_users=500)
        save_users(users)

    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())
    print(f"✅ {len(df_clean)} journaux prêts pour la visualisation.")

    # Sélection de l'utilisateur avec le plus de logs
    user_name = df_clean["name"].value_counts().index[0]
    n_logs    = len(df_clean[df_clean["name"] == user_name])
    print(f"\n  Utilisateur sélectionné : {user_name} ({n_logs} logs)")

    # ── VISUALISATION 1 : Line Plot ───────────────────────────────────────────
    # Montre l'évolution des pas et calories dans le temps
    # Inclut : valeur max, min et ligne de moyenne
    print("\n--- VISUALISATION 1 : Line Plot ---")
    plot_steps_and_calories(df_clean, user_name)

    # ── VISUALISATION 2 : Bar Plot ────────────────────────────────────────────
    # Montre la fréquence de chaque entraînement
    # Inclut : valeurs sur les barres et ligne de moyenne
    print("\n--- VISUALISATION 2 : Bar Plot ---")
    plot_workout_frequency(df_clean)

    print("\n" + "=" * 50)
    print("  ✅ Visualisations sauvegardées !")
    print("  → visualizations/line_plot.png")
    print("  → visualizations/bar_plot.png")
    print("=" * 50)


if __name__ == "__main__":
    main()