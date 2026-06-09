"""
main.py
=======
FitTracker — AI-Generated Fitness Tracker
Interactive menu with rich UI
"""

import json
import os
from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.prompt  import Prompt
from rich         import box

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


# ── Header ─────────────────────────────────────────────────────────────────────

def display_header():
    console.print(Panel.fit(
        "[bold green]FitTracker — AI-Generated Fitness Tracker[/bold green]\n"
        "[dim]Personalized workouts · Data analysis · Progress tracking[/dim]",
        border_style="green"
    ))


# ── Menu ───────────────────────────────────────────────────────────────────────

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


# ── Select user ────────────────────────────────────────────────────────────────

def select_user(users):
    table = Table(
        title="Select a User",
        box=box.SIMPLE,
        border_style="yellow"
    )
    table.add_column("No.", style="bold yellow", width=4)
    table.add_column("Name",  style="white")
    table.add_column("Age",   style="cyan")
    table.add_column("Goal",  style="green")
    table.add_column("Logs",  style="magenta")

    for i, u in enumerate(users[:10]):
        table.add_row(
            str(i+1),
            u.name,
            str(u.age) if u.age else "N/A",
            u.goal,
            str(len(u.daily_logs))
        )

    console.print(table)
    choice = int(Prompt.ask("[yellow]Enter number[/yellow]")) - 1
    return users[choice]


# ── Option 1 — View all users ──────────────────────────────────────────────────

def view_all_users(users):
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


# ── Option 2 — Add a new user ──────────────────────────────────────────────────

def add_new_user(users):
    console.print(Panel(
        "[bold cyan]Create a new user profile[/bold cyan]",
        border_style="cyan"
    ))

    name = Prompt.ask("[white]Full name[/white]")
    age  = int(Prompt.ask("[white]Age[/white]"))

    # Display available goals
    goals_table = Table(box=box.SIMPLE, show_header=False)
    goals_table.add_column("No.", style="bold yellow", width=4)
    goals_table.add_column("Goal", style="green")
    for i, g in enumerate(GOALS):
        goals_table.add_row(str(i+1), g)
    console.print(goals_table)

    goal_choice = int(Prompt.ask("[white]Choose a goal (number)[/white]")) - 1
    goal        = GOALS[goal_choice]

    # Create user
    new_user = User(name=name, age=age, goal=goal)
    users.append(new_user)
    save_users(users)

    console.print(Panel(
        f"[green]✅ New user created successfully ![/green]\n\n"
        f"[cyan]Name :[/cyan] {name}\n"
        f"[cyan]Age  :[/cyan] {age}\n"
        f"[cyan]Goal :[/cyan] {goal}",
        title="[bold green]New User[/bold green]",
        border_style="green"
    ))

    return users


# ── Option 3 — Get workout plan ────────────────────────────────────────────────

def get_workout_plan(users):
    user = select_user(users)
    plan = WorkoutGenerator(user).generate()

    console.print(Panel(
        f"[bold white]{plan['message']}[/bold white]\n\n"
        f"[cyan]Workout  :[/cyan] {plan['workout']}\n"
        f"[cyan]Duration :[/cyan] {plan['duration_min']} min\n"
        f"[cyan]Calories :[/cyan] {plan['calories_target']} kcal\n"
        f"[cyan]Level    :[/cyan] {plan['activity_level']}",
        title=f"[bold green]Today's Plan — {plan['user']}[/bold green]",
        border_style="green"
    ))


# ── Option 4 — Add daily log ───────────────────────────────────────────────────

def add_daily_log(users):
    user = select_user(users)
    console.print(f"\n[bold cyan]Adding log for {user.name}[/bold cyan]")

    date = Prompt.ask("[white]Date (YYYY-MM-DD)[/white]")
    steps    = int(Prompt.ask("[white]Steps[/white]"))
    calories = int(Prompt.ask("[white]Calories burned[/white]"))

    # Display available workouts
    workout_table = Table(box=box.SIMPLE, show_header=False)
    workout_table.add_column("No.", style="bold yellow", width=4)
    workout_table.add_column("Workout", style="green")
    for i, w in enumerate(WORKOUTS):
        workout_table.add_row(str(i+1), w)
    console.print(workout_table)

    workout_choice = int(Prompt.ask("[white]Choose a workout (number)[/white]")) - 1
    workout        = WORKOUTS[workout_choice]

    user.add_log(DailyLog(date, steps, calories, workout))
    save_users(users)

    console.print(Panel(
        f"[green]✅ Log added for {user.name} on {date}[/green]\n\n"
        f"[cyan]Steps   :[/cyan] {steps}\n"
        f"[cyan]Calories:[/cyan] {calories} kcal\n"
        f"[cyan]Workout :[/cyan] {workout}",
        border_style="green"
    ))


# ── Option 5 — Weekly progress ─────────────────────────────────────────────────

def view_weekly_progress(users):
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())
    eda      = exploratory_analysis(df_clean.copy())

    # Weekly steps and calories
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

    # Avg steps by goal
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


# ── Option 6 — Statistical analysis ───────────────────────────────────────────

def run_statistical_analysis(users):
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())

    # ANOVA
    anova = anova_calories_by_workout(df_clean)
    console.print(Panel(
        f"[white]{anova['question']}[/white]\n\n"
        f"[cyan]F-statistic :[/cyan] {anova['f_statistic']}\n"
        f"[cyan]P-value     :[/cyan] {anova['p_value']}\n"
        f"[bold green]→ {anova['conclusion']}[/bold green]",
        title="[bold cyan]ANOVA[/bold cyan]",
        border_style="cyan"
    ))

    # Select user
    user    = select_user(users)
    df_user = df_clean[df_clean["name"] == user.name].copy()

    if len(df_user) < 4:
        console.print("[red]⚠️ Not enough logs. Select another user.[/red]")
        return

    # Linear Regression
    regression = linear_regression_steps(df_user)
    console.print(Panel(
        f"[white]{regression['question']}[/white]\n\n"
        f"[cyan]Slope     :[/cyan] {regression['slope']}\n"
        f"[cyan]R-squared :[/cyan] {regression['r_squared']}\n"
        f"[cyan]Predicted :[/cyan] {regression['predicted_steps_next_7_days']}\n"
        f"[bold green]→ {regression['conclusion']}[/bold green]",
        title=f"[bold cyan]Linear Regression — {user.name}[/bold cyan]",
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
        title=f"[bold cyan]Paired T-test — {user.name}[/bold cyan]",
        border_style="cyan"
    ))


# ── Option 7 — Visualizations ─────────────────────────────────────────────────

def view_visualizations(users):
    df       = users_to_dataframe(users)
    df_clean = clean_dataframe(df.copy())
    user     = select_user(users)

    df_user  = df_clean[df_clean["name"] == user.name]
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


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    display_header()

    # Load or generate users
    console.print("\n[dim]Loading user profiles...[/dim]")
    users = load_users()
    if not users:
        console.print("[yellow]No users found. Generating 500 users...[/yellow]")
        users = generate_users(n_users=500)
        save_users(users)
    console.print(f"[green]✅ {len(users)} users loaded.[/green]")

    # Interactive menu
    while True:
        display_menu()
        choice = Prompt.ask("[bold cyan]Choose an option[/bold cyan]",
                            choices=["1","2","3","4","5","6","7","8"])

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