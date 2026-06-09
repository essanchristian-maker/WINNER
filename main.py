"""
main.py
=======
FitTracker — AI-Generated Fitness Tracker
==========================================
Point d'entrée principal de l'application.
Menu interactif avec interface Rich.
"""

# ── BLOC 1 : Importation des librairies ───────────────────────────────────────

import json
import os
from datetime import datetime

# Interface terminal enrichie
from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.prompt  import Prompt
from rich         import box

# Modules internes FitTracker
from data.file_handler          import load_users, save_users
from data.generator             import generate_users, GOALS, WORKOUTS
from models.user                import User, DailyLog
from services.workout_generator import WorkoutGenerator
from services.data_analysis     import users_to_dataframe, clean_dataframe, exploratory_analysis
from services.stats_service     import (
    anova_calories_by_workout,
    linear_regression_steps,
    paired_ttest_before_after
)
from visualizations.charts      import (
    plot_steps_and_calories,
    plot_workout_frequency
)

console = Console()


# ── Header ────────────────────────────────────────────────────────────────────

def display_header():
    console.print(Panel.fit(
        "[bold green]FitTracker — AI-Generated Fitness Tracker[/bold green]\n"
        "[dim]Personalized workouts · Data analysis · Progress tracking[/dim]",
        border_style="green"
    ))


# ── Menu ──────────────────────────────────────────────────────────────────────

def display_menu():
    table = Table(box=box.ROUNDED, border_style="cyan", show_header=False)
    table.add_column("Option", style="bold cyan", width=4)
    table.add_column("Description", style="white")

    table.add_row("1", "👥 View all users")
    table.add_row("2", "➕ Add a new user")
    table.add_row("3", "🏋️  Get today's workout plan")
    table.add_row("4", "📝 Add a daily log")
    table.add_row("5", "📈 View weekly progress")
    table.add_row("6", "📊 Statistical analysis (SciPy)")
    table.add_row("7", "📉 View visualizations")
    table.add_row("8", "👋 Quit")

    console.print("\n")
    console.print(table)


# ── Sélection d'un utilisateur par recherche ──────────────────────────────────

def select_user(users):
    """Recherche un utilisateur par nom et le sélectionne."""

    while True:
        search = Prompt.ask("[yellow]Search user by name[/yellow]")

        if not search.strip():
            console.print("[red]⚠️ Please enter a name.[/red]")
            continue

        # Filtre par nom
        filtered = [u for u in users if search.lower() in u.name.lower()]

        if not filtered:
            console.print(f"[red]No user found with name '{search}'. Try again.[/red]")
            continue

        # Affiche les résultats
        table = Table(
            title=f"Results for '{search}'",
            box=box.SIMPLE,
            border_style="yellow"
        )
        table.add_column("No.", style="bold yellow", width=4)
        table.add_column("Name",  style="white")
        table.add_column("Age",   style="cyan")
        table.add_column("Goal",  style="green")
        table.add_column("Logs",  style="magenta")

        for i, u in enumerate(filtered):
            table.add_row(
                str(i+1),
                u.name,
                str(u.age) if u.age else "N/A",
                u.goal,
                str(len(u.daily_logs))
            )

        console.print(table)

        # Sélection dans les résultats
        try:
            choice = int(Prompt.ask("[yellow]Enter number[/yellow]")) - 1
            if 0 <= choice < len(filtered):
                return filtered[choice]
            console.print("[red]⚠️ Invalid number.[/red]")
        except ValueError:
            console.print("[red]⚠️ Please enter a valid number.[/red]")


# ── Option 1 : Voir tous les utilisateurs ─────────────────────────────────────

def view_all_users(users):
    """Affiche tous les profils utilisateurs."""
    table = Table(
        title=f"[bold green]All Users ({len(users)})[/bold green]",
        box=box.ROUNDED,
        border_style="green"
    )
    table.add_column("Name",  style="white")
    table.add_column("Age",   style="cyan",    justify="center")
    table.add_column("Goal",  style="green")
    table.add_column("Logs",  style="magenta", justify="center")

    for u in users:
        table.add_row(
            u.name,
            str(u.age) if u.age else "N/A",
            u.goal,
            str(len(u.daily_logs))
        )

    console.print(table)


# ── Option 2 : Ajouter un nouvel utilisateur ──────────────────────────────────

def add_new_user(users):
    """Crée un nouveau profil utilisateur avec validation."""
    console.print(Panel(
        "[bold cyan]Create a new user profile[/bold cyan]",
        border_style="cyan"
    ))

    # Validation nom
    while True:
        name = Prompt.ask("[white]Full name[/white]")
        if name.strip():
            break
        console.print("[red]⚠️ Name cannot be empty.[/red]")

    # Validation âge
    while True:
        try:
            age = int(Prompt.ask("[white]Age[/white]"))
            if 10 <= age <= 100:
                break
            console.print("[red]⚠️ Age must be between 10 and 100.[/red]")
        except ValueError:
            console.print("[red]⚠️ Please enter a valid number.[/red]")

    # Sélection de l'objectif
    goals_table = Table(box=box.SIMPLE, show_header=False)
    goals_table.add_column("No.", style="bold yellow", width=4)
    goals_table.add_column("Goal", style="green")
    for i, g in enumerate(GOALS):
        goals_table.add_row(str(i+1), g)
    console.print(goals_table)

    while True:
        try:
            goal_choice = int(Prompt.ask("[white]Choose a goal (number)[/white]")) - 1
            if 0 <= goal_choice < len(GOALS):
                goal = GOALS[goal_choice]
                break
            console.print(f"[red]⚠️ Choose between 1 and {len(GOALS)}.[/red]")
        except ValueError:
            console.print("[red]⚠️ Please enter a valid number.[/red]")

    # Création et sauvegarde
    new_user = User(name=name, age=age, goal=goal)
    users.append(new_user)
    save_users(users)

    console.print(Panel(
        f"[green]✅ New user created successfully![/green]\n\n"
        f"[cyan]Name :[/cyan] {name}\n"
        f"[cyan]Age  :[/cyan] {age}\n"
        f"[cyan]Goal :[/cyan] {goal}",
        title="[bold green]New User[/bold green]",
        border_style="green"
    ))

    return users


# ── Option 3 : Plan d'entraînement du jour ────────────────────────────────────

def get_workout_plan(users):
    """Génère le plan d'entraînement personnalisé du jour."""
    user = select_user(users)
    plan = WorkoutGenerator(user).generate()

    console.print(Panel(
        f"[bold white]{plan['message']}[/bold white]\n\n"
        f"[cyan]Workout       :[/cyan] {plan['workout']}\n"
        f"[cyan]Duration      :[/cyan] {plan['duration_min']} min\n"
        f"[cyan]Calories      :[/cyan] {plan['calories_target']} kcal\n"
        f"[cyan]Activity Level:[/cyan] {plan['activity_level']}",
        title=f"[bold green]Today's Plan — {plan['user']}[/bold green]",
        border_style="green"
    ))


# ── Option 4 : Ajouter un journal quotidien ───────────────────────────────────

def add_daily_log(users):
    """Ajoute un journal quotidien avec validation complète."""
    user = select_user(users)
    console.print(f"\n[bold cyan]Adding log for {user.name}[/bold cyan]")

    # Validation date
    while True:
        date = Prompt.ask("[white]Date (YYYY-MM-DD)[/white]")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            console.print("[red]⚠️ Format invalide. Utilisez YYYY-MM-DD (ex: 2026-05-14)[/red]")

    # Validation steps
    while True:
        try:
            steps = int(Prompt.ask("[white]Steps[/white]"))
            if steps > 0:
                break
            console.print("[red]⚠️ Steps must be positive.[/red]")
        except ValueError:
            console.print("[red]⚠️ Please enter a valid number.[/red]")

    # Validation calories
    while True:
        try:
            calories = int(Prompt.ask("[white]Calories burned[/white]"))
            if calories > 0:
                break
            console.print("[red]⚠️ Calories must be positive.[/red]")
        except ValueError:
            console.print("[red]⚠️ Please enter a valid number.[/red]")

    # Sélection workout
    workout_table = Table(box=box.SIMPLE, show_header=False)
    workout_table.add_column("No.", style="bold yellow", width=4)
    workout_table.add_column("Workout", style="green")
    for i, w in enumerate(WORKOUTS):
        workout_table.add_row(str(i+1), w)
    console.print(workout_table)

    while True:
        try:
            workout_choice = int(Prompt.ask("[white]Choose a workout (number)[/white]")) - 1
            if 0 <= workout_choice < len(WORKOUTS):
                workout = WORKOUTS[workout_choice]
                break
            console.print(f"[red]⚠️ Choose between 1 and {len(WORKOUTS)}.[/red]")
        except ValueError:
            console.print("[red]⚠️ Please enter a valid number.[/red]")

    # Sauvegarde
    user.add_log(DailyLog(date, steps, calories, workout))
    save_users(users)

    console.print(Panel(
        f"[green]✅ Log added for {user.name} on {date}[/green]\n\n"
        f"[cyan]Steps   :[/cyan] {steps}\n"
        f"[cyan]Calories:[/cyan] {calories} kcal\n"
        f"[cyan]Workout :[/cyan] {workout}",
        border_style="green"
    ))


# ── Option 5 : Progression hebdomadaire ───────────────────────────────────────

def view_weekly_progress(users):
    """Affiche la progression hebdomadaire avec Pandas."""
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())
    eda      = exploratory_analysis(df_clean.copy())

    table = Table(
        title="[bold cyan]Weekly Progress[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan"
    )
    table.add_column("Week",     style="bold cyan")
    table.add_column("Steps",    style="green",   justify="right")
    table.add_column("Calories", style="magenta", justify="right")

    weeks    = eda["weekly_steps"].index.tolist()
    steps    = eda["weekly_steps"].values.tolist()
    calories = eda["weekly_calories"].reindex(weeks, fill_value=0).values.tolist()

    for w, s, c in zip(weeks, steps, calories):
        table.add_row(f"Week {w}", f"{int(s):,}", f"{int(c):,}")

    console.print(table)

    table2 = Table(
        title="[bold green]Avg Steps by Goal[/bold green]",
        box=box.SIMPLE,
        border_style="green"
    )
    table2.add_column("Goal",      style="white")
    table2.add_column("Avg Steps", style="green", justify="right")

    for goal, avg in eda["avg_steps_by_goal"].items():
        table2.add_row(goal, f"{avg:,.2f}")

    console.print(table2)


# ── Option 6 : Analyses statistiques SciPy ───────────────────────────────────

def run_statistical_analysis(users):
    """Lance ANOVA + Régression + T-test."""
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())

    # ANOVA
    anova = anova_calories_by_workout(df_clean)
    console.print(Panel(
        f"[white]{anova['question']}[/white]\n\n"
        f"[cyan]F-statistic :[/cyan] {anova['f_statistic']}\n"
        f"[cyan]P-value     :[/cyan] {anova['p_value']}\n"
        f"[bold green]→ {anova['conclusion']}[/bold green]",
        title="[bold cyan]ANOVA — Calories par type de workout[/bold cyan]",
        border_style="cyan"
    ))

    # Sélection utilisateur
    user    = select_user(users)
    df_user = df_clean[df_clean["name"] == user.name].copy()

    if len(df_user) < 4:
        console.print("[red]⚠️ Not enough logs. Select another user.[/red]")
        return

    # Régression linéaire
    regression = linear_regression_steps(df_user)
    console.print(Panel(
        f"[white]{regression['question']}[/white]\n\n"
        f"[cyan]Slope     :[/cyan] {regression['slope']}\n"
        f"[cyan]R-squared :[/cyan] {regression['r_squared']}\n"
        f"[cyan]Predicted :[/cyan] {regression['predicted_steps_next_7_days']}\n"
        f"[bold green]→ {regression['conclusion']}[/bold green]",
        title=f"[bold cyan]Régression Linéaire — {user.name}[/bold cyan]",
        border_style="cyan"
    ))

    # T-test
    ttest = paired_ttest_before_after(df_user)
    console.print(Panel(
        f"[white]{ttest['question']}[/white]\n\n"
        f"[cyan]Mean before :[/cyan] {ttest['mean_before']} kcal\n"
        f"[cyan]Mean after  :[/cyan] {ttest['mean_after']} kcal\n"
        f"[cyan]T-statistic :[/cyan] {ttest['t_statistic']}\n"
        f"[bold green]→ {ttest['conclusion']}[/bold green]",
        title=f"[bold cyan]T-test Apparié — {user.name}[/bold cyan]",
        border_style="cyan"
    ))


# ── Option 7 : Visualisations ─────────────────────────────────────────────────

def view_visualizations(users):
    """Génère les graphiques Matplotlib."""
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())
    user     = select_user(users)

    df_user = df_clean[df_clean["name"] == user.name]
    if len(df_user) < 2:
        console.print("[red]⚠️ Not enough logs.[/red]")
        return

    plot_steps_and_calories(df_clean, user.name)
    plot_workout_frequency(df_clean)

    console.print(Panel(
        "[green]✅ Charts saved to visualizations/[/green]\n"
        "→ line_plot.png\n"
        "→ bar_plot.png",
        border_style="green"
    ))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    display_header()

    # Chargement des données
    console.print("\n[dim]Loading user profiles...[/dim]")
    users = load_users()
    if not users:
        console.print("[yellow]No users found. Generating 500 users...[/yellow]")
        users = generate_users(n_users=500)
        save_users(users)
    console.print(f"[green]✅ {len(users)} users loaded.[/green]")

    # Boucle principale
    while True:
        display_menu()
        choice = Prompt.ask(
            "[bold cyan]Choose an option[/bold cyan]",
            choices=["1","2","3","4","5","6","7","8"]
        )

        if choice == "1":
            view_all_users(users)
        elif choice == "2":
            users = add_new_user(users)
        elif choice == "3":
            get_workout_plan(users)
        elif choice == "4":
            add_daily_log(users)
        elif choice == "5":
            view_weekly_progress(users)
        elif choice == "6":
            run_statistical_analysis(users)
        elif choice == "7":
            view_visualizations(users)
        elif choice == "8":
            console.print(Panel(
                "[bold green]👋 Goodbye — Keep moving![/bold green]",
                border_style="green"
            ))
            break


if __name__ == "__main__":
    main()