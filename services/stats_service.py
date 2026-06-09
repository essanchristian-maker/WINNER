"""
services/stats_service.py
==========================
Ce fichier implémente les 3 analyses statistiques
demandées par la Question 3 du sujet FitTracker.

Les 3 analyses :
1. ANOVA          → comparer les calories entre types de workouts
2. Régression     → prédire les pas futurs d'un utilisateur
3. T-test apparié → mesurer l'impact avant/après un programme
"""

# ── BLOC 1 : Importation des librairies ───────────────────────────────────────

import numpy as np          # calculs numériques et tableaux
from scipy import stats     # tests statistiques avancés


# ── ANALYSE 1 : ANOVA ─────────────────────────────────────────────────────────
#
# Définition :
# ANOVA (Analysis of Variance) compare les moyennes
# de 3 groupes ou plus pour déterminer si les différences
# sont significatives ou dues au hasard.
#
# Dans notre cas :
# On compare les calories brûlées entre 20 types de workouts.
#
# Hypothèses :
# H0 : Pas de différence significative entre les groupes
# H1 : Au moins un groupe diffère significativement
#
# Interprétation :
# p < 0.05  → différence significative ✅
# p >= 0.05 → différence due au hasard ❌

def anova_calories_by_workout(df) -> dict:
    """
    Teste si les calories brûlées diffèrent significativement
    selon le type d'entraînement avec le test ANOVA.
    """

    # Regroupe les calories par type de workout
    # Chaque groupe = toutes les calories d'un type de workout
    # On garde uniquement les groupes avec au moins 2 valeurs
    groups = [
        group["calories"].dropna().values
        for _, group in df.groupby("workout")
        if len(group) >= 2
    ]

    # Applique le test ANOVA sur tous les groupes
    # f_stat  : mesure l'écart entre les groupes
    # p_value : probabilité que la différence soit due au hasard
    f_stat, p_value = stats.f_oneway(*groups)

    return {
        "test"       : "ANOVA",
        "question"   : "Is there a significant difference in calories burned across workout types?",
        "f_statistic": round(float(f_stat), 4),
        "p_value"    : round(float(p_value), 6),
        "conclusion" : "Significant difference (p < 0.05)" if p_value < 0.05
                       else "No significant difference (p >= 0.05)"
    }


# ── ANALYSE 2 : Régression Linéaire ───────────────────────────────────────────
#
# Définition :
# La régression linéaire modélise la relation entre
# deux variables (X = temps, Y = pas) et trace la droite
# qui passe au plus près de tous les points.
# Elle permet de prédire les valeurs futures.
#
# Dans notre cas :
# On analyse l'historique des pas d'un utilisateur
# et on prédit ses pas pour les 7 prochains jours.
#
# Résultats clés :
# - slope     : tendance (positif = amélioration, négatif = déclin)
# - r_squared : qualité de la prédiction (0 = mauvaise, 1 = parfaite)
# - p_value   : significativité de la tendance

def linear_regression_steps(df) -> dict:
    """
    Prédit les pas futurs d'un utilisateur
    en utilisant la régression linéaire sur ses données passées.
    """

    # Nettoie les données et trie par date
    df_clean = df[["date", "steps"]].dropna()
    df_clean = df_clean.sort_values("date").reset_index(drop=True)

    # X = index des jours (0, 1, 2, 3...)
    # Y = nombre de pas de chaque jour
    x = np.arange(len(df_clean))
    y = df_clean["steps"].values

    # Applique la régression linéaire
    # slope     : pente de la droite (tendance)
    # intercept : point de départ de la droite
    # r_value   : corrélation entre X et Y
    # p_value   : significativité de la tendance
    # std_err   : erreur standard de la pente
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # Prédit les pas pour les 7 prochains jours
    # en prolongeant la droite de régression
    next_days = np.arange(len(df_clean), len(df_clean) + 7)
    predicted = [round(slope * d + intercept) for d in next_days]

    return {
        "test"       : "Linear Regression",
        "question"   : "How many steps will the user burn in the next 7 days?",
        "slope"      : round(slope, 4),
        "intercept"  : round(intercept, 2),
        "r_squared"  : round(r_value ** 2, 4),
        "p_value"    : round(p_value, 6),
        "predicted_steps_next_7_days": predicted,
        "conclusion" : "Increasing trend" if slope > 0 else "Decreasing trend"
    }


# ── ANALYSE 3 : T-test Apparié ────────────────────────────────────────────────
#
# Définition :
# Le T-test apparié compare les moyennes de DEUX groupes
# liés (le même individu avant et après) pour déterminer
# si la différence est statistiquement significative.
# "Apparié" = les deux groupes viennent du même individu.
#
# Dans notre cas :
# On compare les calories d'un utilisateur :
# - AVANT le programme (première moitié des logs)
# - APRÈS le programme (deuxième moitié des logs)
#
# Hypothèses :
# H0 : Pas de changement significatif après le programme
# H1 : Changement significatif après le programme
#
# Interprétation :
# p < 0.05  → changement significatif ✅
# p >= 0.05 → pas de changement significatif ❌

def paired_ttest_before_after(df) -> dict:
    """
    Compare les calories brûlées avant et après
    un programme d'entraînement avec le T-test apparié.
    """

    # Nettoie les données et trie par date
    df_clean = df[["date", "calories"]].dropna()
    df_clean = df_clean.sort_values("date").reset_index(drop=True)

    # Divise les données en deux moitiés égales :
    # - before : première moitié (début du programme)
    # - after  : deuxième moitié (fin du programme)
    mid    = len(df_clean) // 2
    before = df_clean["calories"].iloc[:mid].values
    after  = df_clean["calories"].iloc[mid:mid + len(before)].values

    # Applique le T-test apparié
    # t_stat  : mesure l'écart entre avant et après
    # p_value : probabilité que la différence soit due au hasard
    t_stat, p_value = stats.ttest_rel(before, after)

    return {
        "test"        : "Paired T-test",
        "question"    : "Does the workout program lead to significant changes in calories burned?",
        "mean_before" : round(float(np.mean(before)), 2),
        "mean_after"  : round(float(np.mean(after)), 2),
        "t_statistic" : round(float(t_stat), 4),
        "p_value"     : round(float(p_value), 6),
        "conclusion"  : "Significant change (p < 0.05)" if p_value < 0.05
                        else "No significant change (p >= 0.05)"
    }