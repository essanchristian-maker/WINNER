# FitTracker — AI-Generated Fitness Tracker

A Python-based fitness tracker that generates personalized workout plans
and tracks progress over time using data analysis and visualization.

---

## Project Structure

## Project Structure

```
WINNER/
├── models/
│   └── user.py              # User and DailyLog classes (OOP)
├── data/
│   ├── generator.py         # Synthetic data generation (NumPy)
│   ├── file_handler.py      # JSON save/load
│   ├── users.json           # Generated user profiles
│   └── recommendations.json # Generated workout plans
├── services/
│   ├── workout_generator.py # Personalized workout engine
│   ├── data_analysis.py     # Pandas analysis + cleaning + EDA
│   └── stats_service.py     # SciPy statistical analysis
├── visualizations/
│   ├── charts.py            # Matplotlib visualizations
│   ├── line_plot.png        # Steps and calories over time
│   └── bar_plot.png         # Workout frequency
├── main.py                  # Entry point
└── README.md
```


---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/essanchristian-maker/WINNER.git
cd WINNER
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install numpy pandas scipy matplotlib
```

### 4. Run the project
```bash
python main.py
```

---

## What it does

### Step 1 — User Profiles
- Generates 500 synthetic user profiles using NumPy
- Each profile has : name, age, fitness goal, daily logs
- Data saved and loaded from JSON files

### Step 2 — Personalized Workout Plans
- Generates a daily workout plan for each user
- Based on fitness goal and recent activity level
- Example : *"Based on your activity, try a 30-min HIIT session today."*

### Step 3 — Statistical Analysis (SciPy)
- **ANOVA** : tests if calorie burn differs across workout types
- **Linear Regression** : predicts future steps for a specific user
- **Paired T-test** : compares calories before/after a workout program

### Step 4 — Data Analysis and Visualization
- **Pandas** : weekly progress (steps, calories, workouts)
- **Line plots** : steps and calories burned over time
- **Bar plots** : workout frequency across all users

---

## Technologies Used

| Tool | Usage |
|---|---|
| Python | Core language |
| NumPy | Data generation |
| Pandas | Data analysis |
| SciPy | Statistical testing |
| Matplotlib | Visualizations |
| JSON | Data persistence |
| Git/GitHub | Version control |

---

## Author
Christian Essan — DI Bootcamp/TEAM WINNER