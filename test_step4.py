"""
test_step4.py
=============
Ce fichier teste la Question 3 du sujet FitTracker :
Application des analyses statistiques avec SciPy.

Les 3 analyses effectuées :
- ANOVA         : comparer les calories entre types de workouts
- Régression    : prédire les pas futurs d'un utilisateur
- T-test apparié : mesurer l'impact avant/après un programme
"""

# ── BLOC 1 : Importation des librairies ───────────────────────────────────────

from data.file_handler        import load_users, save_users      # persistance JSON
from data.generator           import generate_users              # génération données
from services.data_analysis   import users_to_dataframe, \
                                     clean_dataframe             # prétraitement
from services.stats_service   import (
    anova_calories_by_workout,   # test ANOVA
    linear_regression_steps,     # régression linéaire
    paired_ttest_before_after    # T-test apparié
)


def main():
    print("=" * 50)
    print("  FitTracker — Question 3 : Analyses SciPy")
    print("=" * 50)

    # ── BLOC 2 : Collecte et préparation des données ──────────────────────────
    # Chargement des profils et conversion en DataFrame Pandas
    # Le DataFrame est nettoyé avant les analyses statistiques
    # (valeurs manquantes et outliers supprimés)

    print("\n[Bloc 2] Chargement et préparation des données...")
    users = load_users()
    if not users:
        print("Aucun utilisateur trouvé. Génération en cours...")
        users = generate_users(n_users=500)
        save_users(users)

    # Conversion en DataFrame et nettoyage
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())
    print(f"✅ {len(df_clean)} journaux prêts pour l'analyse.")

    # ── ANALYSE 1 : ANOVA ─────────────────────────────────────────────────────
    #
    # Définition :
    # ANOVA (Analysis of Variance) est un test statistique
    # qui compare les moyennes de 3 groupes ou plus
    # pour déterminer si les différences sont significatives
    # ou simplement dues au hasard.
    #
    # Dans notre cas :
    # On compare les calories brûlées entre 20 types de workouts
    # (Yoga, Running, HIIT, Swimming, Football...)
    #
    # Résultat clé :
    # - F-statistic : mesure l'écart entre les groupes
    #   (plus F est grand, plus les groupes sont différents)
    # - P-value : probabilité que la différence soit due au hasard
    #   p < 0.05 → différence significative ✅
    #   p >= 0.05 → différence due au hasard ❌

    print("\n--- ANALYSE 1 : ANOVA ---")
    print("Question : Les calories brûlées diffèrent-elles")
    print("           selon le type d'entraînement ?")
    print("-" * 40)

    anova = anova_calories_by_workout(df_clean)
    print(f"  Question    : {anova['question']}")
    print(f"  F-statistic : {anova['f_statistic']}")
    print(f"  P-value     : {anova['p_value']}")
    print(f"  Conclusion  : {anova['conclusion']}")

    # ── Sélection d'un utilisateur spécifique ─────────────────────────────────
    # On sélectionne l'utilisateur avec le plus de logs
    # pour avoir suffisamment de données pour les analyses suivantes

    user_name = df_clean["name"].value_counts().index[0]
    df_user   = df_clean[df_clean["name"] == user_name].copy()
    print(f"\n--- Utilisateur analysé : {user_name} ({len(df_user)} logs) ---")

    # ── ANALYSE 2 : Régression Linéaire ───────────────────────────────────────
    #
    # Définition :
    # La régression linéaire est une technique statistique
    # qui modélise la relation entre deux variables :
    # - Variable X : le temps (jours)
    # - Variable Y : les pas effectués
    # Elle trace la droite qui passe au plus près de tous les points
    # et l'utilise pour prédire les valeurs futures.
    #
    # Dans notre cas :
    # On analyse l'historique des pas d'un utilisateur
    # et on prédit combien de pas il fera les 7 prochains jours.
    #
    # Résultats clés :
    # - Slope (pente) : tendance des pas dans le temps
    #   slope > 0 → tendance à la hausse (amélioration)
    #   slope < 0 → tendance à la baisse (déclin)
    # - R-squared : qualité de la prédiction (0 à 1)
    #   R² proche de 1 → prédiction très fiable
    #   R² proche de 0 → prédiction peu fiable
    # - P-value : significativité de la tendance

    print("\n--- ANALYSE 2 : Régression Linéaire ---")
    print("Question : Combien de pas cet utilisateur")
    print("           fera-t-il la semaine prochaine ?")
    print("-" * 40)

    regression = linear_regression_steps(df_user)
    print(f"  Question    : {regression['question']}")
    print(f"  Slope       : {regression['slope']}")
    print(f"  R-squared   : {regression['r_squared']}")
    print(f"  P-value     : {regression['p_value']}")
    print(f"  Prédiction 7 jours : {regression['predicted_steps_next_7_days']}")
    print(f"  Conclusion  : {regression['conclusion']}")

    # ── ANALYSE 3 : T-test Apparié ────────────────────────────────────────────
    #
    # Définition :
    # Le T-test apparié (Paired T-test) compare les moyennes
    # de DEUX groupes liés pour déterminer si la différence
    # entre eux est statistiquement significative.
    # "Apparié" signifie que les deux groupes viennent
    # du MÊME individu (avant et après).
    #
    # Dans notre cas :
    # On compare les calories brûlées par le même utilisateur :
    # - AVANT le programme (première moitié des logs)
    # - APRÈS le programme (deuxième moitié des logs)
    #
    # Résultats clés :
    # - Mean before : moyenne des calories avant le programme
    # - Mean after  : moyenne des calories après le programme
    # - T-statistic : mesure l'écart entre avant et après
    # - P-value : significativité du changement
    #   p < 0.05 → changement significatif ✅
    #   p >= 0.05 → pas de changement significatif ❌

    print("\n--- ANALYSE 3 : T-test Apparié ---")
    print("Question : Le programme d'entraînement a-t-il")
    print("           produit un changement significatif ?")
    print("-" * 40)

    ttest = paired_ttest_before_after(df_user)
    print(f"  Question      : {ttest['question']}")
    print(f"  Moyenne avant : {ttest['mean_before']} kcal")
    print(f"  Moyenne après : {ttest['mean_after']} kcal")
    print(f"  T-statistic   : {ttest['t_statistic']}")
    print(f"  P-value       : {ttest['p_value']}")
    print(f"  Conclusion    : {ttest['conclusion']}")

    print("\n" + "=" * 50)
    print("  ✅ Analyses statistiques terminées !")
    print("=" * 50)


if __name__ == "__main__":
    main()