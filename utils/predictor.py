import joblib
from pathlib import Path

from .preprocessing import processor
# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"


# ==========================================
# Load Models
# ==========================================

DIABETES_MODEL = joblib.load(
    
    MODEL_DIR / "diabetes_ultimate_model.pkl"
)

HYPERTENSION_MODEL = joblib.load(
    MODEL_DIR / "hypertensive_ultimate_model.pkl"
)

HYPERLIPIDEMIA_MODEL = joblib.load(
    MODEL_DIR / "hyperlipidemia_ultimate_model.pkl"
)

class HealthPredictor:

    def __init__(self):

        pass



    def predict(self, patient):

        diabetes_df = processor.prepare(
            patient,
            "diabetes"
        )

        hypertension_df = processor.prepare(
            patient,
            "hypertension"
        )

        hyperlipidemia_df = processor.prepare(
            patient,
            "hyperlipidemia"
        )



        diabetes_probability = DIABETES_MODEL.predict_proba(
            diabetes_df
        )[0][1]

        hypertension_probability = HYPERTENSION_MODEL.predict_proba(
            hypertension_df
        )[0][1]

        hyperlipidemia_probability = HYPERLIPIDEMIA_MODEL.predict_proba(
            hyperlipidemia_df
        )[0][1]


        return {

            "diabetes_probability":
                float(diabetes_probability),

            "hypertension_probability":
                float(hypertension_probability),

            "hyperlipidemia_probability":
                float(hyperlipidemia_probability)

        }


predictor = HealthPredictor()