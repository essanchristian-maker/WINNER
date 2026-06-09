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

from data.file_handler      import load_users, save_users       # persistance JSON
from data.generator         import generate_users               # génération données
from services.data_analysis import users_to_dataframe, \
                                   clean_dataframe              # prétraitement
from visualizations.charts  import (
    plot_steps_and_calories,   # line plot : pas et calories
    plot_workout_frequency     # bar plot  : fréquence workouts
)


def main():
    print("=" * 50)
    print("  FitTracker — Question 4 : Visualisations")
    print("=" * 50)

    # ── BLOC 2 : Collecte et préparation des données ──────────────────────────
    # Chargement des profils et conversion en DataFrame Pandas nettoyé

    print("\n[Bloc 2] Chargement et préparation des données...")
    users = load_users()
    if not users:
        print("Aucun utilisateur trouvé. Génération en cours...")
        users = generate_users(n_users=500)
        save_users(users)

    # Conversion en DataFrame et nettoyage
    # (valeurs manquantes et outliers supprimés)
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())
    print(f"✅ {len(df_clean)} journaux prêts pour la visualisation.")

    # ── Sélection de l'utilisateur ────────────────────────────────────────────
    # On sélectionne l'utilisateur avec le plus de logs
    # pour avoir des graphiques plus riches et représentatifs

    user_name = df_clean["name"].value_counts().index[0]
    n_logs    = len(df_clean[df_clean["name"] == user_name])
    print(f"\n  Utilisateur sélectionné : {user_name} ({n_logs} logs)")

    # ── VISUALISATION 1 : Line Plot ───────────────────────────────────────────
    #
    # Définition :
    # Un line plot (graphique linéaire) relie les points de données
    # par une ligne continue pour montrer l'évolution dans le temps.
    # Il est idéal pour visualiser des tendances et des progressions.
    #
    # Dans notre cas :
    # - Graphique 1 : évolution des pas quotidiens dans le temps
    # - Graphique 2 : évolution des calories brûlées dans le temps
    #
    # Ce qu'on peut observer :
    # - Les pics d'activité (jours très actifs)
    # - Les creux (jours peu actifs)
    # - La tendance générale (amélioration ou déclin)

    print("\n--- VISUALISATION 1 : Line Plot ---")
    print("Évolution des pas et calories dans le temps")
    print(f"Utilisateur : {user_name}")
    print("-" * 40)
    plot_steps_and_calories(df_clean, user_name)

    # ── VISUALISATION 2 : Bar Plot ────────────────────────────────────────────
    #
    # Définition :
    # Un bar plot (graphique en barres) représente des catégories
    # avec des barres dont la hauteur correspond à leur valeur.
    # Il est idéal pour comparer des catégories entre elles.
    #
    # Dans notre cas :
    # On compte combien de fois chaque type d'entraînement
    # apparaît dans les logs de TOUS les utilisateurs.
    #
    # Ce qu'on peut observer :
    # - Les entraînements les plus populaires
    # - La distribution entre cardio, force, flexibilité...
    # - Les entraînements peu pratiqués

    print("\n--- VISUALISATION 2 : Bar Plot ---")
    print("Fréquence de chaque type d'entraînement")
    print("(tous les utilisateurs confondus)")
    print("-" * 40)
    plot_workout_frequency(df_clean)

    print("\n" + "=" * 50)
    print("  ✅ Visualisations sauvegardées !")
    print("  → visualizations/line_plot.png")
    print("  → visualizations/bar_plot.png")
    print("=" * 50)


if __name__ == "__main__":
    main()