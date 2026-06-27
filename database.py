import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_FOLDER = BASE_DIR / "database"

DB_FOLDER.mkdir(exist_ok=True)


# ==========================================
# Database Path
# ==========================================

DATABASE_PATH = DB_FOLDER / "healthcare.db"
# ==========================================
# Connection
# ==========================================

def get_connection():

    conn = sqlite3.connect(DATABASE_PATH)

    return conn


# ==========================================
# Create Database
# ==========================================

def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT,

        age INTEGER,

        gender TEXT,

        height_cm REAL,

        weight_kg REAL,

        bmi REAL,

        pulse_rate INTEGER,

        sleep_hours REAL,

        exercise_days_per_week INTEGER,

        daily_sitting_hours REAL,

        soft_drinks_per_week INTEGER,

        fast_food_meals_per_week INTEGER,

        smoking_status TEXT,

        father_diabetes INTEGER,
        mother_diabetes INTEGER,

        father_hypertension INTEGER,
        mother_hypertension INTEGER,

        father_hyperlipidemia INTEGER,
        mother_hyperlipidemia INTEGER,

        paternal_grandparents_diabetes INTEGER,
        maternal_grandparents_diabetes INTEGER,

        paternal_grandparents_hypertension INTEGER,
        maternal_grandparents_hypertension INTEGER,

        paternal_grandparents_hyperlipidemia INTEGER,
        maternal_grandparents_hyperlipidemia INTEGER,

        diabetes_family_score INTEGER,
        hypertension_family_score INTEGER,
        hyperlipidemia_family_score INTEGER,

        hypertensive INTEGER,

        hyperlipidemia INTEGER,

        fatty_liver INTEGER,

        sleep_apnea INTEGER,

        diabetes_probability REAL,

        hypertension_probability REAL,

        hyperlipidemia_probability REAL,

        overall_risk REAL,

        health_score REAL,

        selected_model TEXT,

        predicted_label INTEGER,

        model_version TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()


# ==========================================
# Save User
# ==========================================

def save_user(user):

    conn = get_connection()

    df = pd.DataFrame([user])

    df.to_sql(

        "users",

        conn,

        if_exists="append",

        index=False

    )

    conn.close()


# ==========================================
# Read Database
# ==========================================

def load_users():

    conn = get_connection()

    df = pd.read_sql(

        "SELECT * FROM users",

        conn

    )

    conn.close()

    return df


# ==========================================
# Export CSV
# ==========================================

def export_csv():

    df = load_users()

    EXPORT_PATH = DB_FOLDER / "users_export.csv"

    df.to_csv(
        EXPORT_PATH,
        index=False
     )
    print("CSV exported successfully.")


# ==========================================
# First Run
# ==========================================

if __name__ == "__main__":

    create_database()

    print("Database Created Successfully.")