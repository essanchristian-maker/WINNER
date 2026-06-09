"""
visualizations/charts.py
=========================
Point 4 du sujet — Visualisations :
- Line plots : steps et calories over time
- Bar plots : workout frequency
Les graphiques incluent des annotations pour faciliter la lecture.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


# ── Line plots ─────────────────────────────────────────────────────────────────

def plot_steps_and_calories(df: pd.DataFrame, user_name: str):
    """
    Line plots pour les pas et calories d'un utilisateur.
    Inclut des annotations : max, min et moyenne.
    """

    df_user         = df[df["name"] == user_name].copy()
    df_user["date"] = pd.to_datetime(df_user["date"])
    df_user         = df_user.sort_values("date")

    x     = range(len(df_user))
    dates = df_user["date"].dt.strftime("%Y-%m-%d").tolist()

    steps    = df_user["steps"].values
    calories = df_user["calories"].values

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle(f"Progression de {user_name}", fontsize=14, fontweight="bold")

    # ── Graphique 1 : Steps ───────────────────────────────────────────────────
    axes[0].plot(x, steps, marker="o", color="steelblue",
                 linewidth=1.5, markersize=4, label="Pas quotidiens")

    # Ligne moyenne
    avg_steps = steps.mean()
    axes[0].axhline(y=avg_steps, color="red", linestyle="--",
                    linewidth=1, label=f"Moyenne : {avg_steps:.0f} pas")

    # Annotation max
    max_idx = steps.argmax()
    axes[0].annotate(
        f"Max : {steps[max_idx]:.0f}",
        xy=(max_idx, steps[max_idx]),
        xytext=(max_idx + 1, steps[max_idx] + 300),
        fontsize=8, color="green",
        arrowprops=dict(arrowstyle="->", color="green")
    )

    # Annotation min
    min_idx = steps.argmin()
    axes[0].annotate(
        f"Min : {steps[min_idx]:.0f}",
        xy=(min_idx, steps[min_idx]),
        xytext=(min_idx + 1, steps[min_idx] - 500),
        fontsize=8, color="red",
        arrowprops=dict(arrowstyle="->", color="red")
    )

    axes[0].set_title("Évolution des Pas Quotidiens")
    axes[0].set_ylabel("Nombre de pas")
    axes[0].set_xticks(list(x)[::5])
    axes[0].set_xticklabels(dates[::5], rotation=45, ha="right")
    axes[0].legend(loc="upper right")
    axes[0].grid(True, alpha=0.3)

    # ── Graphique 2 : Calories ────────────────────────────────────────────────
    axes[1].plot(x, calories, marker="o", color="orange",
                 linewidth=1.5, markersize=4, label="Calories brûlées")

    # Ligne moyenne
    avg_calories = calories.mean()
    axes[1].axhline(y=avg_calories, color="red", linestyle="--",
                    linewidth=1, label=f"Moyenne : {avg_calories:.0f} kcal")

    # Annotation max
    max_idx_c = calories.argmax()
    axes[1].annotate(
        f"Max : {calories[max_idx_c]:.0f} kcal",
        xy=(max_idx_c, calories[max_idx_c]),
        xytext=(max_idx_c + 1, calories[max_idx_c] + 20),
        fontsize=8, color="green",
        arrowprops=dict(arrowstyle="->", color="green")
    )

    # Annotation min
    min_idx_c = calories.argmin()
    axes[1].annotate(
        f"Min : {calories[min_idx_c]:.0f} kcal",
        xy=(min_idx_c, calories[min_idx_c]),
        xytext=(min_idx_c + 1, calories[min_idx_c] - 30),
        fontsize=8, color="red",
        arrowprops=dict(arrowstyle="->", color="red")
    )

    axes[1].set_title("Évolution des Calories Brûlées")
    axes[1].set_ylabel("Calories (kcal)")
    axes[1].set_xticks(list(x)[::5])
    axes[1].set_xticklabels(dates[::5], rotation=45, ha="right")
    axes[1].legend(loc="upper right")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("visualizations/line_plot.png", dpi=150)
    plt.close()
    print("✅ Line plot saved to visualizations/line_plot.png")


# ── Bar plots ──────────────────────────────────────────────────────────────────

def plot_workout_frequency(df: pd.DataFrame):
    """
    Bar plot de la fréquence des entraînements.
    Inclut les valeurs sur chaque barre et
    une ligne de moyenne pour faciliter la lecture.
    """

    workout_counts = df["workout"].value_counts()
    avg            = workout_counts.mean()

    # Couleurs selon niveau (au-dessus ou en-dessous de la moyenne)
    colors = ["green" if v >= avg else "steelblue"
              for v in workout_counts.values]

    fig, ax = plt.subplots(figsize=(14, 7))

    bars = ax.bar(
        workout_counts.index,
        workout_counts.values,
        color=colors,
        edgecolor="black",
        alpha=0.8
    )

    # Valeur sur chaque barre
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 5,
            f"{int(height)}",
            ha="center", va="bottom",
            fontsize=8, fontweight="bold"
        )

    # Ligne de moyenne
    ax.axhline(y=avg, color="red", linestyle="--",
               linewidth=1.5, label=f"Moyenne : {avg:.0f} séances")

    # Annotation workout le plus populaire
    max_workout = workout_counts.index[0]
    max_val     = workout_counts.values[0]
    ax.annotate(
        f"⭐ Plus populaire\n{max_workout}",
        xy=(0, max_val),
        xytext=(2, max_val - 50),
        fontsize=9, color="green", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="green")
    )

    ax.set_title("Fréquence des Entraînements — Tous les Utilisateurs",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Type d'entraînement")
    ax.set_ylabel("Nombre de séances")
    ax.set_xticklabels(workout_counts.index, rotation=45, ha="right")

    # Légende des couleurs
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="green", label="Au-dessus de la moyenne"),
        Patch(facecolor="steelblue", label="En-dessous de la moyenne"),
        plt.Line2D([0], [0], color="red", linestyle="--",
                   label=f"Moyenne : {avg:.0f}")
    ]
    ax.legend(handles=legend_elements, loc="upper right")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("visualizations/bar_plot.png", dpi=150)
    plt.close()
    print("✅ Bar plot saved to visualizations/bar_plot.png")