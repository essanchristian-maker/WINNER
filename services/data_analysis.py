"""
services/data_analysis.py
==========================
Ce fichier gère le prétraitement et l'analyse exploratoire
des données de FitTracker.
- Prétraitement des données
- Analyse descriptive
"""

import pandas as pd
import numpy as np


# ── BLOC 3 : Prétraitement des données ────────────────────────────────────────


# ── 3.1 Conversion en DataFrame ───────────────────────────────────────────────
# On transforme la liste d'objets User en tableau Pandas (DataFrame)
# Un DataFrame c'est comme un tableau Excel en Python —
# chaque ligne = un journal quotidien d'un utilisateur

def users_to_dataframe(users: list) -> pd.DataFrame:
    """
    Convertit la liste des objets User en DataFrame Pandas plat.
    Chaque ligne représente UN journal quotidien d'UN utilisateur.
    """
    rows = []

    # Pour chaque utilisateur, on parcourt tous ses journaux quotidiens
    for user in users:
        for log in user.daily_logs:
            # On crée une ligne avec les infos de l'utilisateur et les données de son journal du jour
            rows.append({
                "name"    : user.name,     # Nom de l'utilisateur
                "age"     : user.age,      # Âge (peut être None)
                "goal"    : user.goal,     # Objectif fitness
                "date"    : log.date,      # Date du journal
                "steps"   : log.steps,     # Nombre de pas (peut être None)
                "calories": log.calories,  # Calories brûlées (peut être None)
                "workout" : log.workout    # Type d'entraînement (peut être None)
            })

    # Crée et retourne le DataFrame depuis la liste de lignes
    return pd.DataFrame(rows)


# ── 3.2 Nettoyage des données ─────────────────────────────────────────────────
# Les données réelles contiennent toujours des imperfections.
# On applique 3 stratégies selon le type de colonne :
# - Valeurs numériques manquantes  → remplacer par la médiane
# - Valeurs texte manquantes       → remplacer par la valeur la plus fréquente
# - Valeurs aberrantes (outliers)  → supprimer avec le Z-score

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie le DataFrame :
    - Remplace les valeurs manquantes de steps par la médiane
    - Remplace les valeurs manquantes de calories par la médiane
    - Remplace les valeurs manquantes de workout par le mode
    - Remplace les valeurs manquantes d'age par la médiane
    - Supprime les outliers de steps avec le Z-score > 3
    """

    # Remplace les valeurs manquantes numériques par la médiane
    # La médiane est plus robuste que la moyenne face aux valeurs extrêmes
    df["steps"]    = df["steps"].fillna(df["steps"].median())
    df["calories"] = df["calories"].fillna(df["calories"].median())
    df["age"]      = df["age"].fillna(df["age"].median())

    # Remplace les workouts manquants par la valeur la plus fréquente (mode)
    # Ex : si "Swimming" est le workout le plus fréquent, il remplace les None
    df["workout"]  = df["workout"].fillna(df["workout"].mode()[0])

    # Supprime les outliers dans steps avec le Z-score
    # Le Z-score mesure à combien d'écarts-types une valeur
    # est éloignée de la moyenne
    # Z-score > 3 = valeur aberrante (ex: 80 000 pas en une journée)
    mean  = df["steps"].mean()
    std   = df["steps"].std()
    df    = df[np.abs((df["steps"] - mean) / std) < 3]

    # Réinitialise l'index après suppression des lignes aberrantes
    df = df.reset_index(drop=True)

    return df


# ── BLOC 4 : Analyse descriptive ──────────────────────────────────────────────
# On calcule les statistiques clés pour comprendre les données :
# - Statistiques descriptives (moyenne, médiane, écart-type...)
# - Distribution des objectifs et des entraînements
# - Progression hebdomadaire (pas, calories)
# - Moyennes par objectif fitness

def exploratory_analysis(df: pd.DataFrame) -> dict:
    """
    Effectue l'analyse exploratoire des données (EDA).
    Retourne un dictionnaire contenant toutes les statistiques clés.
    """

    # Dictionnaire qui va stocker tous les résultats
    eda = {}

    # ── Statistiques descriptives ──────────────────────────────────────────
    # describe() calcule : count, mean, std, min, 25%, 50%, 75%, max
    eda["summary"] = df[["age", "steps", "calories"]].describe().round(2)

    # ── Distribution des objectifs ─────────────────────────────────────────
    # Compte combien d'utilisateurs ont chaque objectif fitness
    eda["goals_distribution"] = df["goal"].value_counts()

    # ── Distribution des entraînements ────────────────────────────────────
    # Compte combien de fois chaque type d'entraînement apparaît
    eda["workouts_distribution"] = df["workout"].value_counts()

    # ── Progression hebdomadaire ───────────────────────────────────────────
    # Convertit la colonne date en format datetime pour extraire la semaine
    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.isocalendar().week

    # Total des pas par semaine (somme de tous les utilisateurs)
    eda["weekly_steps"]    = df.groupby("week")["steps"].sum()

    # Total des calories par semaine
    eda["weekly_calories"] = df.groupby("week")["calories"].sum()

    # ── Moyennes par objectif ──────────────────────────────────────────────
    # Moyenne des pas selon l'objectif fitness
    eda["avg_steps_by_goal"]    = df.groupby("goal")["steps"].mean().round(2)

    # Moyenne des calories selon l'objectif fitness
    eda["avg_calories_by_goal"] = df.groupby("goal")["calories"].mean().round(2)

    return eda