"""
test_step3.py
=============
Ce fichier teste et démontre le prétraitement
et l'analyse exploratoire des données de FitTracker.


- Bloc 1 : Importation des librairies
- Bloc 2 : Collecte des données
- Bloc 3 : Prétraitement des données
- Bloc 4 : Analyse descriptive
"""

# ── BLOC 1 : Importation des librairies ───────────────────────────────────────

# Modules internes FitTracker
from data.file_handler      import load_users, save_users       # persistance JSON
from data.generator         import generate_users               # génération données
from services.data_analysis import users_to_dataframe, \
                                   clean_dataframe, \
                                   exploratory_analysis         # analyse Pandas


def main():
    print("=" * 50)
    print("  FitTracker — Prétraitement et Analyse des Données")
    print("=" * 50)

    # ── BLOC 2 : Collecte des données ─────────────────────────────────────────
    # Les données sont chargées depuis le fichier JSON (data/users.json)
    # Si le fichier n'existe pas encore, on génère 500 profils avec NumPy

    print("\n[Bloc 2] Collecte des données...")
    users = load_users()
    if not users:
        print("Aucun utilisateur trouvé. Génération en cours...")
        users = generate_users(n_users=500)
        save_users(users)
    print(f"✅ {len(users)} profils utilisateurs chargés.")

    # Conversion des objets User en DataFrame Pandas
    # Un DataFrame = tableau structuré avec lignes et colonnes
    df = users_to_dataframe(users)

    # ── BLOC 3 : Prétraitement des données ────────────────────────────────────

    print("\n[Bloc 3] Prétraitement des données")
    print("-" * 40)

    # 3.1 Afficher les 5 premières lignes
    # df.head() donne un aperçu rapide de la structure des données
    print("\n--- Affichage des 5 premières lignes (df.head()) ---")
    print(df.head())

    # 3.2 Informations générales sur le dataset
    # df.info() affiche : nombre de lignes, colonnes, types et valeurs manquantes
    print("\n--- Informations générales sur le dataset (df.info()) ---")
    print(df.info())

    # 3.3 Dimensions du dataset
    print(f"\n--- Dimensions du dataset ---")
    print(f"  Lignes   : {df.shape[0]}")
    print(f"  Colonnes : {df.shape[1]}")
    print(f"  Colonnes : {df.columns.tolist()}")

    # 3.4 Variables quantitatives et qualitatives
    # Quantitatives = colonnes numériques (int, float)
    # Qualitatives  = colonnes texte (object)
    quantitative = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    qualitative  = df.select_dtypes(include=['object']).columns.tolist()

    print(f"\n--- Variables quantitatives ---")
    print(f"  {quantitative}")

    print(f"\n--- Variables qualitatives ---")
    print(f"  {qualitative}")

    # 3.5 Valeurs manquantes AVANT nettoyage
    # Identifie quelles colonnes ont des données incomplètes
    print("\n--- Valeurs manquantes AVANT nettoyage ---")
    print(df.isnull().sum())

    # 3.6 Nettoyage des données
    # - fillna(médiane) pour les colonnes numériques
    # - fillna(mode) pour les colonnes texte
    # - Suppression des outliers avec Z-score > 3:
#Le Z-score mesure à combien d'écarts-types une valeur est éloignée de la moyenne.

    print("\n--- Nettoyage en cours... ---")
    df_clean = clean_dataframe(df.copy())

    # 3.7 Valeurs manquantes APRÈS nettoyage
    print("\n--- Valeurs manquantes APRÈS nettoyage ---")
    print(df_clean.isnull().sum())
    print(f"\n  Lignes avant nettoyage : {len(df)}")
    print(f"  Lignes après nettoyage : {len(df_clean)}")
    print(f"  Lignes supprimées      : {len(df) - len(df_clean)}")

    # ── BLOC 4 : Analyse descriptive ──────────────────────────────────────────
    # On calcule les statistiques clés pour comprendre les données

    print("\n[Bloc 4] Analyse descriptive")
    print("-" * 40)

    eda = exploratory_analysis(df_clean.copy())

    # 4.1 Statistiques descriptives
    # count, mean, std, min, 25%, 50%, 75%, max
    print("\n--- Statistiques descriptives (df.describe()) ---")
    print(eda["summary"])

    # 4.2 Distribution des objectifs fitness
    # Combien d'utilisateurs ont chaque objectif ?
    print("\n--- Distribution des objectifs fitness ---")
    print(eda["goals_distribution"])

    # 4.3 Distribution des entraînements
    # Quels sont les entraînements les plus pratiqués ?
    print("\n--- Distribution des entraînements ---")
    print(eda["workouts_distribution"])

    # 4.4 Progression hebdomadaire
    # Total des pas et calories par semaine
    print("\n--- Progression hebdomadaire — Total des pas ---")
    print(eda["weekly_steps"])

    print("\n--- Progression hebdomadaire — Total des calories ---")
    print(eda["weekly_calories"])

    # 4.5 Moyennes par objectif
    # Quel objectif génère le plus de pas ? Le plus de calories ?
    print("\n--- Moyenne des pas par objectif ---")
    print(eda["avg_steps_by_goal"])

    print("\n--- Moyenne des calories par objectif ---")
    print(eda["avg_calories_by_goal"])

    print("\n" + "=" * 50)
    print("  ✅ Prétraitement et analyse terminés !")
    print("=" * 50)


if __name__ == "__main__":
    main()