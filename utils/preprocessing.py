import joblib
import pandas as pd
from pathlib import Path


# =====================================================
# Paths
# =====================================================


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

# =====================================================
# Load Feature Names
# =====================================================

DIABETES_FEATURES = joblib.load(
    MODEL_DIR / "diabetes_feature_names.pkl"
)

HYPERTENSION_FEATURES = joblib.load(
    MODEL_DIR / "hypertensive_feature_names.pkl"
)

HYPERLIPIDEMIA_FEATURES = joblib.load(
    MODEL_DIR / "hyperlipidemia_feature_names.pkl"
)


# =====================================================
# Health Preprocessor
# =====================================================

class HealthPreprocessor:

    def __init__(self):
        pass


 


    # ---------------------------------------------

    def calculate_bmi(
        self,
        height_cm,
        weight_kg
    ):

        bmi = weight_kg / ((height_cm / 100) ** 2)

        return round(bmi,2)


    # ---------------------------------------------

    def calculate_family_scores(
        self,
        patient
    ):

        diabetes_family_score = (

            patient["father_diabetes"] * 4 +

            patient["mother_diabetes"] * 4 +

            patient["paternal_grandparents_diabetes"] +

            patient["maternal_grandparents_diabetes"]

        )

        hypertension_family_score = (

            patient["father_hypertension"] * 4 +

            patient["mother_hypertension"] * 4 +

            patient["paternal_grandparents_hypertension"] +

            patient["maternal_grandparents_hypertension"]

        )

        hyperlipidemia_family_score = (

            patient["father_hyperlipidemia"] * 4 +

            patient["mother_hyperlipidemia"] * 4 +

            patient["paternal_grandparents_hyperlipidemia"] +

            patient["maternal_grandparents_hyperlipidemia"]

        )

        return (

            diabetes_family_score,

            hypertension_family_score,

            hyperlipidemia_family_score

        )
    


    # ---------------------------------------------

    def feature_engineering(
        self,
        patient
    ):

        bmi = self.calculate_bmi(

            patient["height_cm"],
            patient["weight_kg"]

        )

        patient["bmi"] = bmi

        (

            diabetes_family_score,

            hypertension_family_score,

            hyperlipidemia_family_score

        ) = self.calculate_family_scores(patient)

        patient["diabetes_family_score"] = diabetes_family_score

        patient["hypertension_family_score"] = hypertension_family_score

        patient["hyperlipidemia_family_score"] = hyperlipidemia_family_score


        # ==============================
        # SAME FEATURES USED IN TRAINING
        # ==============================

        patient["age_bmi"] = (

            patient["age"] * bmi

        )

        patient["family_bmi"] = (

            diabetes_family_score * bmi

        )

        patient["family_age_score"] = (

            diabetes_family_score * patient["age"]

        )

        patient["inactivity_score"] = (

            patient["daily_sitting_hours"]

            -

            patient["exercise_days_per_week"]

        )

        patient["sugar_score"] = (

            patient["soft_drinks_per_week"]

            +

            patient["fast_food_meals_per_week"]

        )

        patient["lifestyle_score"] = (

            patient["daily_sitting_hours"]

            +

            patient["soft_drinks_per_week"]

            +

            patient["fast_food_meals_per_week"]

        )

        return patient
    


    # ---------------------------------------------

    def prepare(
        self,
        patient,
        disease="diabetes"
    ):

        # -----------------------------
        # Feature Engineering
        # -----------------------------

        patient = patient.copy()
        patient = self.feature_engineering(patient)    
        for key, value in patient.items():

            if value is None:

                patient[key] = "Unknown"

        # -----------------------------
        # DataFrame
        # -----------------------------

        df = pd.DataFrame([patient])

        # -----------------------------
        # One Hot Encoding
        # -----------------------------

        df = pd.get_dummies(df)

        # -----------------------------
        # Choose Feature List
        # -----------------------------

        if disease == "diabetes":

            feature_names = DIABETES_FEATURES

        elif disease == "hypertension":

            feature_names = HYPERTENSION_FEATURES

        else:

            feature_names = HYPERLIPIDEMIA_FEATURES

        # -----------------------------
        # Add Missing Columns
        # -----------------------------

        for col in feature_names:

            if col not in df.columns:

                df[col] = 0

        # -----------------------------
        # Keep Correct Order
        # -----------------------------

        df = df[feature_names]

        return df
    


processor = HealthPreprocessor()