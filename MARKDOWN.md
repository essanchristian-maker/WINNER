# FitTracker — De la Donnée à la Performance

> *"Et si vos données pouvaient vous dire exactement quel entraînement faire aujourd'hui ?"*

---

## Étape 1 — Construire les Fondations
### *"Qui sont nos utilisateurs et que veulent-ils ?"*

**Le défi :**
Créer des profils utilisateurs réalistes avec des objectifs fitness
et des journaux d'activité quotidiens.
Tout stocker dans un format structuré et réutilisable.

**Notre solution :**
Nous avons conçu deux classes Python — `User` et `DailyLog` —
en suivant les principes de la Programmation Orientée Objet.
500 profils synthétiques ont été générés avec NumPy,
avec des prénoms français et des noms africains,
8 objectifs fitness différents,
et entre 7 et 30 journaux quotidiens par utilisateur.
Pour simuler des données réelles, nous avons intentionnellement
introduit 5% de valeurs manquantes et 3% de valeurs aberrantes.
Chaque profil est sauvegardé et rechargé depuis un fichier JSON —
aucune donnée n'est jamais perdue entre les sessions.

**Le résultat :**
> 500 utilisateurs. 8 objectifs. 8 926 journaux quotidiens. Tout persisté en JSON.

---

## Étape 2 — L'Intelligence Derrière la Recommandation
### *"Basé sur ce que vous avez fait, voici ce que vous devriez faire aujourd'hui."*

**Le défi :**
Générer un plan d'entraînement quotidien personnalisé pour chaque utilisateur,
basé sur son objectif fitness et son niveau d'activité récent.

**Notre solution :**
Nous avons construit une classe `WorkoutGenerator` qui analyse
les 7 derniers jours d'activité de chaque utilisateur.
En calculant la moyenne des pas quotidiens,
elle détermine le niveau d'activité — élevé, moyen ou faible.
Combiné à l'objectif de l'utilisateur,
elle sélectionne l'entraînement le plus adapté parmi
24 combinaisons possibles (8 objectifs × 3 niveaux d'activité).

Le résultat est simple, clair et actionnable :
> *"Based on your activity, try a 30-min HIIT session today."*

**Le résultat :**
> 500 recommandations personnalisées. Générées instantanément. Sauvegardées en JSON.

---

## Étape 3 — La Puissance des Statistiques
### *"Que nous disent vraiment les chiffres ?"*

**Le défi :**
Appliquer des tests statistiques avancés pour extraire
des insights significatifs depuis les données fitness.

**Notre solution :**

**ANOVA** a répondu à la question :
*"Le type d'entraînement influence-t-il significativement les calories brûlées ?"*
Résultat : p = 0.76 — pas de différence significative.
C'est l'intensité qui compte, pas le type d'exercice.

**Régression Linéaire** a répondu à la question :
*"Combien de pas cet utilisateur fera-t-il la semaine prochaine ?"*
Résultat : Pierre Kouassi est prédit à 6 929 pas par jour —
une tendance légèrement décroissante.

**T-test Apparié** a répondu à la question :
*"Le programme de cet utilisateur a-t-il fait une vraie différence ?"*
Résultat : p = 0.56 — pas encore de changement significatif.
Plus de données sont nécessaires pour confirmer l'impact.

**Le résultat :**
> Trois tests statistiques. Trois insights. Une vision claire de la performance.

---

## Étape 4 — Rendre les Données Visibles
### *"Un chiffre ne veut rien dire. Une tendance raconte une histoire."*

**Le défi :**
Analyser la progression hebdomadaire et créer des visualisations
qui rendent les données compréhensibles en un coup d'œil.

**Notre solution :**
Avec Pandas, nous avons calculé le total des pas,
des calories brûlées et des entraînements réalisés par semaine.
Les données ont révélé un schéma clair :
l'activité atteint un pic en semaine 2 et décline progressivement —
un reflet réaliste du comportement des utilisateurs dans le temps.

Deux graphiques Matplotlib donnent vie aux données :
- Un line plot montrant l'évolution des pas
  et des calories brûlées dans le temps pour un utilisateur spécifique.
- Un bar chart révélant les entraînements les plus pratiqués
  parmi les 500 utilisateurs — la natation domine avec 881 séances.

**Le résultat :**
> Deux graphiques. Cinq semaines de données. Une histoire de progression.

---

## La Vue d'Ensemble

| Étape | Question | Outil | Résultat |
|---|---|---|---|
| 1 | Qui sont nos utilisateurs ? | POO + NumPy + JSON | 500 profils générés |
| 2 | Que doivent-ils faire aujourd'hui ? | WorkoutGenerator | 500 plans personnalisés |
| 3 | Que disent les chiffres ? | SciPy | 3 insights statistiques |
| 4 | À quoi ressemble la progression ? | Pandas + Matplotlib | 2 graphiques + tendances hebdo |

---

## Une Commande. L'Expérience Complète.

```bash
python main.py
```

> *FitTracker — parce que chaque pas compte.*