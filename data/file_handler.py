"""
data/file_handler.py
====================
Ce fichier gère la sauvegarde et le chargement
des profils utilisateurs depuis un fichier JSON.
C'est la couche de persistance de FitTracker —
sans ce fichier, toutes les données seraient perdues
à chaque fermeture du programme.
"""

import json
import os
from models.user import User

# Chemin vers le fichier JSON de sauvegarde
# os.path.dirname(__file__) récupère le dossier où se trouve ce fichier
# os.path.join construit le chemin complet vers users.json
DATA_PATH = os.path.join(os.path.dirname(__file__), "users.json")


# ── Fonction : sauvegarder les utilisateurs ────────────────────────────────────

def save_users(users: list):
    """
    Sauvegarde la liste des objets User dans le fichier JSON.
    Chaque objet User est converti en dictionnaire avant la sauvegarde.
    """

    # Crée le dossier data/ s'il n'existe pas encore
    os.makedirs("data", exist_ok=True)

    # Ouvre le fichier en mode écriture
    # "w" écrase le contenu existant à chaque sauvegarde
    with open(DATA_PATH, "w") as f:
        # Convertit chaque User en dictionnaire avec to_dict()
        # json.dump écrit la liste complète dans le fichier
        # indent=4 rend le JSON lisible et bien indenté
        json.dump([u.to_dict() for u in users], f, indent=4)

    print(f"✅ {len(users)} users saved to {DATA_PATH}")


# ── Fonction : charger les utilisateurs ───────────────────────────────────────

def load_users() -> list:
    """
    Charge la liste des profils utilisateurs depuis le fichier JSON.
    Recrée les objets User à partir des dictionnaires sauvegardés.
    Retourne une liste vide si le fichier n'existe pas encore.
    """

    # Vérifie si le fichier JSON existe avant de le lire
    # Au premier lancement, le fichier n'existe pas encore
    if not os.path.exists(DATA_PATH):
        print("⚠️ No data file found. Starting fresh.")
        return []

    # Ouvre le fichier en mode lecture
    with open(DATA_PATH, "r") as f:
        # Charge le contenu JSON sous forme de liste de dictionnaires
        data = json.load(f)

    print(f"✅ {len(data)} users loaded from {DATA_PATH}")

    # Recrée chaque objet User depuis son dictionnaire
    # User.from_dict() est l'opération inverse de to_dict()
    return [User.from_dict(u) for u in data]