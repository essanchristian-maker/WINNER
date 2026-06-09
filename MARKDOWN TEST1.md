# FitTracker — Question 1 : Résumé des Résultats

## Profils générés
- **500 utilisateurs** avec prénoms français et noms africains
- **8 objectifs fitness** différents
- **Entre 7 et 30 journaux** quotidiens par utilisateur

---

## Distribution des objectifs
| Objectif | Nombre |
|---|---|
| weight_loss | 77 |
| stress_relief | 67 |
| cardio | 66 |
| endurance | 64 |
| muscle_gain | 63 |
| general_fitness | 63 |
| strength | 50 |
| flexibility | 50 |

---

## Distribution des entraînements
| Entraînement | Nombre |
|---|---|
| Swimming | 467 |
| Circuit Training | 460 |
| Strength Training | 439 |
| Tabata | 436 |
| Boxing | 433 |
| Dancing | 433 |

---

## Valeurs manquantes (intentionnelles ~5%)
| Colonne | Manquants |
|---|---|
| Steps | 439 |
| Calories | 457 |
| Ages | 21 |

> Ces valeurs manquantes simulent des données réelles
> et justifient l'étape de nettoyage (Bloc 3).

---

## Exemple de profil JSON
```json
{
    "name": "Nadege Diarra",
    "age": 22,
    "goal": "stress_relief",
    "daily_logs": [
        {
            "date": "2026-01-01",
            "steps": 8973,
            "calories": 481,
            "workout": "Football"
        }
    ]
}
```

---

## Persistance JSON
- ✅ 500 profils sauvegardés dans `data/users.json`
- ✅ 500 profils rechargés avec succès
- ✅ Format conforme à l'exemple du sujet