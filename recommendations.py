"""
recommendations.py
====================
Explainable AI recommendation engine.

Replaces the old static if/else "reasons" list with explanations derived
directly from the trained models (SHAP where possible). Does NOT modify
predictor.py, preprocessing.py, or the models themselves — only imports
them read-only to compute explanations on top of existing predictions.

Public interface kept backward compatible with app.py's previous usage:
    engine.build(patient, results) -> dict with at least:
        health_score, overall_risk, reasons, recommendations, tests
    plus new richer keys:
        contributing_factors, protective_factors, family_risk,
        health_score_breakdown, what_if
"""

import copy
import numpy as np

import shap

from utils.preprocessing import processor
from utils.predictor import (
    DIABETES_MODEL,
    HYPERTENSION_MODEL,
    HYPERLIPIDEMIA_MODEL,
)

DISEASE_MODELS = {
    "diabetes": DIABETES_MODEL,
    "hypertension": HYPERTENSION_MODEL,
    "hyperlipidemia": HYPERLIPIDEMIA_MODEL,
}

# ==========================================
# Human-readable feature labels
# ==========================================
FEATURE_LABELS = {
    "bmi": "BMI",
    "exercise_days_per_week": "Physical Activity",
    "daily_sitting_hours": "Sedentary Lifestyle",
    "soft_drinks_per_week": "Sugary Drinks",
    "fast_food_meals_per_week": "Fast Food",
    "smoking_status_Current": "Smoking",
    "diabetes_family_score": "Family History",
    "hypertension_family_score": "Family History",
    "hyperlipidemia_family_score": "Family History",
    "age": "Age",
    "bmi": "BMI",
    "age_bmi": "Age combined with BMI",
    "family_bmi": "Family history combined with BMI",
    "family_age_score": "Family history combined with age",
    "diabetes_family_score": "Family history of diabetes",
    "hypertension_family_score": "Family history of hypertension",
    "hyperlipidemia_family_score": "Family history of high cholesterol",
    "exercise_days_per_week": "Physical activity level",
    "daily_sitting_hours": "Sedentary time",
    "inactivity_score": "Inactivity",
    "soft_drinks_per_week": "Sugary drink intake",
    "fast_food_meals_per_week": "Fast food intake",
    "sugar_score": "Overall sugar intake",
    "lifestyle_score": "Lifestyle pattern",
    "sleep_hours": "Sleep duration",
    "fatty_liver": "Fatty liver",
    "sleep_apnea": "Sleep apnea",
    "smoking_status_Current": "Current smoking",
    "smoking_status_Former": "History of smoking",
    "father_diabetes": "Father's diabetes history",
    "mother_diabetes": "Mother's diabetes history",
    "father_hypertension": "Father's hypertension history",
    "mother_hypertension": "Mother's hypertension history",
    "father_hyperlipidemia": "Father's cholesterol history",
    "mother_hyperlipidemia": "Mother's cholesterol history",
}
ALLOWED_EXPLANATION_FEATURES = {
    "bmi",
    "diabetes_family_score",
    "hypertension_family_score",
    "hyperlipidemia_family_score",
    "exercise_days_per_week",
    "daily_sitting_hours",
    "soft_drinks_per_week",
    "fast_food_meals_per_week",
    "sleep_hours",
    "fatty_liver",
    "sleep_apnea",
    "hypertensive",
    "hyperlipidemia",
    "smoking_status_Current",
    "smoking_status_Former",
    "age",
}

def _label(feature_name: str) -> str:
    if feature_name in FEATURE_LABELS:
        return FEATURE_LABELS[feature_name]
    return feature_name.replace("_", " ").strip().capitalize()


def _unwrap_tree_model(model):
    """Find the underlying tree-based estimator inside common sklearn wrappers."""
    if hasattr(model, "calibrated_classifiers_"):
        try:
            base = model.calibrated_classifiers_[0].estimator
            if hasattr(base, "feature_importances_") or hasattr(base, "estimators_"):
                return _unwrap_tree_model(base)
        except Exception:
            pass

    if hasattr(model, "estimators_"):
        for est in model.estimators_:
            if hasattr(est, "feature_importances_"):
                return est

    if hasattr(model, "feature_importances_"):
        return model

    return None


_EXPLAINER_CACHE = {}


def _get_shap_explainer(disease):
    if disease not in _EXPLAINER_CACHE:
        tree_model = _unwrap_tree_model(DISEASE_MODELS[disease])
        _EXPLAINER_CACHE[disease] = (
            shap.TreeExplainer(tree_model) if tree_model is not None else None
        )
    return _EXPLAINER_CACHE[disease]


def _format_value(feature_name, raw_value):
    """Formats a raw feature value for human display, e.g. BMI (35.4)."""
    if feature_name == "bmi":
        return f"{raw_value:.1f}"
    if isinstance(raw_value, (int, float)) and not isinstance(raw_value, bool):
        if float(raw_value).is_integer():
            return str(int(raw_value))
        return f"{raw_value:.1f}"
    return str(raw_value)


def explain_disease(patient: dict, disease: str, top_n: int = 4):
    """
    Returns top contributing and protective factors for one disease,
    using real SHAP values whenever the underlying model supports it.
    Falls back to global feature_importances_ if SHAP is unavailable.
    """
    df = processor.prepare(patient, disease)
    explainer = _get_shap_explainer(disease)

    if explainer is None:
        return {"contributing": [], "protective": [], "mode": "unavailable"}

    shap_values = explainer.shap_values(df)
    values = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]

    row = df.iloc[0]
    contributions = []
    for feat, shap_val, raw_val in zip(df.columns, values, row):

        feat_lower = feat.lower()
        base_feat = feat

        if base_feat not in ALLOWED_EXPLANATION_FEATURES:
            continue

        # Ignore technical / missing-value features
        if (
            "_was_missing" in feat_lower
            or "_unknown" in feat_lower
        ):
            continue

        if abs(shap_val) < 1e-6:
            continue

        if raw_val == 0:
            continue

        contributions.append({
            "feature": feat,
            "label": _label(feat),
            "value": raw_val,
            "value_display": _format_value(feat, raw_val),
            "impact": float(shap_val),
        })

    contributing = sorted(
        [c for c in contributions if c["impact"] > 0],
        key=lambda c: c["impact"], reverse=True
    )[:top_n]

    protective = sorted(
        [c for c in contributions if c["impact"] < 0],
        key=lambda c: c["impact"]
    )[:top_n]

    return {"contributing": contributing, "protective": protective, "mode": "shap"}


# ==========================================
# Family Risk (per disease)
# ==========================================
PARENT_WEIGHT = 2.0
GRANDPARENT_WEIGHT = 1.0


def family_risk(patient: dict, disease: str):
    key_map = {
        "diabetes": ("father_diabetes", "mother_diabetes",
                     "paternal_grandparents_diabetes", "maternal_grandparents_diabetes"),
        "hypertension": ("father_hypertension", "mother_hypertension",
                          "paternal_grandparents_hypertension", "maternal_grandparents_hypertension"),
        "hyperlipidemia": ("father_hyperlipidemia", "mother_hyperlipidemia",
                            "paternal_grandparents_hyperlipidemia", "maternal_grandparents_hyperlipidemia"),
    }
    father_k, mother_k, pg_k, mg_k = key_map[disease]

    father = int(patient.get(father_k, 0) or 0)
    mother = int(patient.get(mother_k, 0) or 0)
    pg = int(patient.get(pg_k, 0) or 0)
    mg = int(patient.get(mg_k, 0) or 0)

    raw = father * PARENT_WEIGHT + mother * PARENT_WEIGHT + pg * GRANDPARENT_WEIGHT + mg * GRANDPARENT_WEIGHT
    max_raw = PARENT_WEIGHT * 2 + GRANDPARENT_WEIGHT * 2
    score = round((raw / max_raw) * 100, 1)

    level = "Low" if score < 25 else ("Moderate" if score < 60 else "High")

    return {
        "score": score,
        "level": level,
        "father": bool(father),
        "mother": bool(mother),
        "paternal_grandparents": bool(pg),
        "maternal_grandparents": bool(mg),
    }


# ==========================================
# Realistic Health Score (replaces 100 - avg(probabilities))
# ==========================================
def _bmi_penalty(bmi):
    if bmi < 18.5:
        return 20
    if bmi < 25:
        return 0
    if bmi < 30:
        return 25
    if bmi < 35:
        return 50
    if bmi < 40:
        return 75
    return 100


def _lifestyle_penalty(patient):
    score, weight_used = 0, 0

    exercise = patient.get("exercise_days_per_week")
    if exercise is not None:
        score += max(0, (3 - exercise)) / 3 * 25
        weight_used += 25

    sitting = patient.get("daily_sitting_hours")
    if sitting is not None:
        score += min(sitting, 14) / 14 * 20
        weight_used += 20

    smoking = patient.get("smoking_status")
    if smoking is not None:
        score += {"Current": 30, "Former": 10, "Never": 0}.get(smoking, 0)
        weight_used += 30

    soft_drinks = patient.get("soft_drinks_per_week")
    if soft_drinks is not None:
        score += min(soft_drinks, 14) / 14 * 15
        weight_used += 15

    fast_food = patient.get("fast_food_meals_per_week")
    if fast_food is not None:
        score += min(fast_food, 10) / 10 * 10
        weight_used += 10

    if weight_used == 0:
        return 0
    return min(100, (score / weight_used) * 100)


def _conditions_penalty(patient):
    flags = [
        int(bool(patient.get("fatty_liver", 0))),
        int(bool(patient.get("sleep_apnea", 0))),
        int(bool(patient.get("hypertensive", 0))),
        int(bool(patient.get("hyperlipidemia", 0))),
    ]
    return min(100, (sum(flags) / len(flags)) * 100 * 1.5)


def compute_health_score(patient: dict, results: dict, family_risks: dict):
    avg_model_risk_pct = np.mean([
        results["diabetes_probability"],
        results["hypertension_probability"],
        results["hyperlipidemia_probability"],
    ]) * 100

    bmi_pen = _bmi_penalty(patient.get("bmi", 25))
    family_pen = np.mean([fr["score"] for fr in family_risks.values()])
    lifestyle_pen = _lifestyle_penalty(patient)
    conditions_pen = _conditions_penalty(patient)

    weights = {"model": 40, "bmi": 20, "family": 15, "lifestyle": 15, "conditions": 10}

    total_penalty = (
        avg_model_risk_pct * weights["model"]
        + bmi_pen * weights["bmi"]
        + family_pen * weights["family"]
        + lifestyle_pen * weights["lifestyle"]
        + conditions_pen * weights["conditions"]
    ) / 100

    score = max(0, round(100 - total_penalty))

    if score >= 85:
        level = "Excellent"
    elif score >= 70:
        level = "Good"
    elif score >= 50:
        level = "Moderate"
    elif score >= 30:
        level = "Poor"
    else:
        level = "Critical"

    return {
        "score": score,
        "level": level,
        "breakdown": {
            "model_risk": round(avg_model_risk_pct, 1),
            "bmi": round(bmi_pen, 1),
            "family_history": round(family_pen, 1),
            "lifestyle": round(lifestyle_pen, 1),
            "existing_conditions": round(conditions_pen, 1),
        }
    }


# ==========================================
# What-If Simulation (re-runs the real models)
# ==========================================
def _predict_all(patient):
    diab_df = processor.prepare(patient, "diabetes")
    hyp_df = processor.prepare(patient, "hypertension")
    lip_df = processor.prepare(patient, "hyperlipidemia")
    return {
        "diabetes_probability": float(DIABETES_MODEL.predict_proba(diab_df)[0][1]),
        "hypertension_probability": float(HYPERTENSION_MODEL.predict_proba(hyp_df)[0][1]),
        "hyperlipidemia_probability": float(HYPERLIPIDEMIA_MODEL.predict_proba(lip_df)[0][1]),
    }


def _scenario_weight_loss(patient):
    p = copy.deepcopy(patient)
    target_bmi = max(24.0, patient["bmi"] * 0.93)  # ~7% body weight loss
    height_m = patient["height_cm"] / 100
    p["bmi"] = round(target_bmi, 1)
    p["weight_kg"] = round(target_bmi * (height_m ** 2), 1)
    return p, "Lose 5-7% of body weight"


def _scenario_more_exercise(patient):
    p = copy.deepcopy(patient)
    p["exercise_days_per_week"] = min(7, patient["exercise_days_per_week"] + 3)
    return p, "Exercise 3 more days per week"


def _scenario_quit_smoking(patient):
    p = copy.deepcopy(patient)
    p["smoking_status"] = "Former"
    return p, "Quit smoking"


def _scenario_reduce_sugar(patient):
    p = copy.deepcopy(patient)
    p["soft_drinks_per_week"] = max(0, patient["soft_drinks_per_week"] - 5)
    p["fast_food_meals_per_week"] = max(0, patient["fast_food_meals_per_week"] - 2)
    return p, "Cut sugary drinks and fast food"


SCENARIOS = [
    _scenario_weight_loss,
    _scenario_more_exercise,
    _scenario_quit_smoking,
    _scenario_reduce_sugar,
]


def run_what_if(patient: dict, results: dict):
    """
    Runs each predefined scenario through the REAL trained models and
    returns the one with the largest risk reduction for the patient's
    highest-risk disease, plus the full comparison table.
    """
    diseases = ["diabetes", "hypertension", "hyperlipidemia"]
    primary_disease = max(diseases, key=lambda d: results[f"{d}_probability"])

    scenario_results = []
    for scenario_fn in SCENARIOS:
        modified_patient, label = scenario_fn(patient)

        # Only run scenarios that don't no-op (e.g. already non-smoker)
        if scenario_fn is _scenario_quit_smoking and patient.get("smoking_status") != "Current":
            continue

        new_results = _predict_all(modified_patient)

        before_pct = results[f"{primary_disease}_probability"] * 100
        after_pct = new_results[f"{primary_disease}_probability"] * 100
        reduction = round(before_pct - after_pct, 1)

        scenario_results.append({
            "label": label,
            "primary_disease": primary_disease,
            "before_pct": round(before_pct, 1),
            "after_pct": round(after_pct, 1),
            "reduction_pct": reduction,
            "full_after": {k: round(v * 100, 1) for k, v in new_results.items()},
        })

    scenario_results = sorted(scenario_results, key=lambda r: r["reduction_pct"], reverse=True)

    best = scenario_results[0] if scenario_results else None
    return {"primary_disease": primary_disease, "best_action": best, "all_scenarios": scenario_results}


def _reduction_category(reduction_pct):
    if reduction_pct >= 10:
        return "Large"
    if reduction_pct >= 5:
        return "Moderate"
    if reduction_pct > 0:
        return "Small"
    return "Minimal"


# ==========================================
# Narrative builder (the "Your diabetes risk is mainly driven by..." text)
# ==========================================
def build_narrative(disease: str, explanation: dict, what_if_best):
    pretty = disease.replace("_", " ").capitalize()
    lines = []

    contributing = explanation.get("contributing", [])
    if contributing:
        factor_strs = [f"{c['label']} ({c['value_display']})" for c in contributing[:3]]
        lines.append(f"Your {pretty.lower()} risk is mainly driven by:")
        for f in factor_strs:
            lines.append(f"- {f}")
    else:
        lines.append(f"No single dominant driver was found for {pretty.lower()} risk.")

    if what_if_best and what_if_best["primary_disease"] == disease:
        best = what_if_best["best_action"]
        if best:
            lines.append("")
            lines.append(f"Recommended first action: {best['label']}.")
            lines.append(f"Expected risk reduction: {_reduction_category(best['reduction_pct'])} "
                          f"(~{best['reduction_pct']} percentage points).")

    return "\n".join(lines)


# ==========================================
# Backward-compatible test suggestions (kept, lightly extended)
# ==========================================
def suggested_tests(results):
    tests = []
    if results["diabetes_probability"] >= 0.40:
        tests.extend(["HbA1c", "Fasting Blood Glucose"])
    if results["hypertension_probability"] >= 0.40:
        tests.append("Blood Pressure Measurement (ideally ambulatory monitoring)")
    if results["hyperlipidemia_probability"] >= 0.40:
        tests.append("Lipid Profile")
    if not tests:
        tests.append("Annual routine medical check-up")
    return tests


def risk_level(probability):
    if probability < 0.30:
        return "Low"
    elif probability < 0.60:
        return "Moderate"
    return "High"


# ==========================================
# Main Engine
# ==========================================
class RecommendationEngine:

    def build(self, patient: dict, results: dict) -> dict:
        diseases = ["diabetes", "hypertension", "hyperlipidemia"]

        explanations = {d: explain_disease(patient, d) for d in diseases}
        family_risks = {d: family_risk(patient, d) for d in diseases}
        health_score = compute_health_score(patient, results, family_risks)
        what_if = run_what_if(patient, results)

        narratives = {
            d: build_narrative(d, explanations[d], what_if) for d in diseases
        }
        print("\n=== NARRATIVES ===")
        print(narratives)
        print("==================\n")

        # Backward-compatible flat "reasons" list (now model-driven, not static)
        reasons = []
        for d in diseases:
            for factor in explanations[d]["contributing"][:2]:
                reasons.append(f"{factor['label']} ({factor['value_display']}) → increases {d} risk")

        # Backward-compatible flat recommendations list
        flat_recommendations = []
        if what_if["best_action"]:
            flat_recommendations.append(
                f"{what_if['best_action']['label']} — "
                f"estimated {_reduction_category(what_if['best_action']['reduction_pct'])} "
                f"reduction in {what_if['primary_disease']} risk."
            )
        for scenario in what_if["all_scenarios"][1:3]:
            flat_recommendations.append(
                f"{scenario['label']} — estimated "
                f"{_reduction_category(scenario['reduction_pct'])} reduction."
            )
        if not flat_recommendations:
            flat_recommendations.append("Maintain your current healthy habits.")

        overall_risk = risk_level(max(
            results["diabetes_probability"],
            results["hypertension_probability"],
            results["hyperlipidemia_probability"],
        ))

        return {
            # ---- backward-compatible keys (app.py's old code keeps working) ----
            "health_score": health_score["score"],
            "overall_risk": overall_risk,
            "reasons": reasons,
            "recommendations": flat_recommendations,
            "tests": suggested_tests(results),

            # ---- new, richer keys for the upgraded dashboard ----
            "health_score_full": health_score,
            "explanations": explanations,
            "family_risk": family_risks,
            "what_if": what_if,
            "narratives": narratives,
        }


engine = RecommendationEngine()