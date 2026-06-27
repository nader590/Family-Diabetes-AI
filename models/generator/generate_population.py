import pandas as pd
import numpy as np
import os

# ==========================
# Number of samples
# ==========================
N = 1000000
# ==========================
# Random Seed
# ==========================
np.random.seed(42)

# ==========================
# Age
# ==========================
age = np.random.randint(18, 81, N)

# ==========================
# Gender
# ==========================
gender = np.random.choice(
    ["Male", "Female"],
    size=N,
    p=[0.5, 0.5]
)

# ==========================
# Height
# ==========================
height_cm = []

for g in gender:
    if g == "Male":
        h = np.random.normal(175, 7)
    else:
        h = np.random.normal(162, 6)

    height_cm.append(round(h, 1))

height_cm = np.array(height_cm)

# ==========================
# BMI
# ==========================
bmi = np.random.normal(
    loc=29,
    scale=5,
    size=N
)

bmi = np.clip(bmi, 18, 45)

# ==========================
# Weight
# ==========================
height_m = height_cm / 100

weight_kg = bmi * (height_m ** 2)
weight_kg = np.round(weight_kg, 1)

# ==========================
# Waist Circumference
# ==========================
waist_circumference = np.round(
    bmi * 2.3 + np.random.normal(20, 6, N),
    1
)
obesity = (bmi >= 30).astype(int)

central_obesity = (
    waist_circumference >= 100
).astype(int)

# ==========================
# Pulse Rate
# ==========================
pulse_rate = np.random.randint(
    55,
    110,
    N
)

# ==========================
# Physical Activity
# ==========================
exercise_days_per_week = np.random.choice(
    [0, 1, 2, 3, 4, 5, 6, 7],
    size=N,
    p=[0.15, 0.15, 0.20, 0.20, 0.15, 0.08, 0.05, 0.02]
)

# ==========================
# Sleep Hours
# ==========================
sleep_hours = np.clip(
    np.round(np.random.normal(7, 1.5, N)),
    3,
    10
)
daily_sitting_hours = np.clip(
    np.round(
        np.random.normal(8, 3, N)
    ),
    2,
    16
)

# ==========================
# Smoking Status
# ==========================
smoking_status = np.random.choice(
    ["Never", "Former", "Current"],
    size=N,
    p=[0.65, 0.15, 0.20]
)

# ==========================
# Fast Food Frequency
# ==========================
fast_food_meals_per_week = np.random.randint(
    0,
    10,
    N
)

# ==========================
# Soft Drinks Frequency
# ==========================
soft_drinks_per_week = np.random.randint(
    0,
    15,
    N
)

# ==========================
# Stress Level
# ==========================
stress_level = np.random.choice(
    ["Low", "Moderate", "High"],
    size=N,
    p=[0.30, 0.50, 0.20]
)

# ==========================
# Salt Intake
# ==========================
salt_intake = np.random.choice(
    ["Low", "Moderate", "High"],
    size=N,
    p=[0.20, 0.60, 0.20]
)

# ==========================
# Grandparents
# ==========================
paternal_grandparents_diabetes = np.random.binomial(1, 0.35, N)
maternal_grandparents_diabetes = np.random.binomial(1, 0.35, N)

paternal_grandparents_hypertension = np.random.binomial(1, 0.45, N)
maternal_grandparents_hypertension = np.random.binomial(1, 0.45, N)

paternal_grandparents_hyperlipidemia = np.random.binomial(1, 0.40, N)
maternal_grandparents_hyperlipidemia = np.random.binomial(1, 0.40, N)

# ==========================
# Parents derived from grandparents
# ==========================
father_diabetes = np.random.binomial(
    1,
    np.where(
        paternal_grandparents_diabetes == 1,
        0.50,
        0.15
    )
)

mother_diabetes = np.random.binomial(
    1,
    np.where(
        maternal_grandparents_diabetes == 1,
        0.50,
        0.15
    )
)

siblings_diabetes = np.random.binomial(
    1,
    np.where(
        (father_diabetes + mother_diabetes) >= 1,
        0.30,
        0.08
    )
)

father_hypertension = np.random.binomial(
    1,
    np.where(
        paternal_grandparents_hypertension == 1,
        0.60,
        0.20
    )
)

mother_hypertension = np.random.binomial(
    1,
    np.where(
        maternal_grandparents_hypertension == 1,
        0.60,
        0.20
    )
)

father_hyperlipidemia = np.random.binomial(
    1,
    np.where(
        paternal_grandparents_hyperlipidemia == 1,
        0.50,
        0.15
    )
)

mother_hyperlipidemia = np.random.binomial(
    1,
    np.where(
        maternal_grandparents_hyperlipidemia == 1,
        0.50,
        0.15
    )
)

# ==========================
# Family Scores
# ==========================
diabetes_family_score = (
    father_diabetes * 2
    + mother_diabetes * 2
    + siblings_diabetes * 2
    + paternal_grandparents_diabetes
    + maternal_grandparents_diabetes
)

hypertension_family_score = (
    father_hypertension
    + mother_hypertension
    + paternal_grandparents_hypertension
    + maternal_grandparents_hypertension
)

hyperlipidemia_family_score = (
    father_hyperlipidemia
    + mother_hyperlipidemia
    + paternal_grandparents_hyperlipidemia
    + maternal_grandparents_hyperlipidemia
)

# ==========================
# Associated Diseases
# ==========================
abdominal_obesity = np.random.choice(
    ["No", "Mild", "Moderate", "Severe"],
    size=N,
    p=[0.30, 0.30, 0.25, 0.15]
)
fatty_liver = np.random.binomial(1, 0.18, N)

sleep_apnea = np.random.binomial(1, 0.12, N)
family_history_obesity = np.random.binomial(
    1,
    0.35,
    N
)

pcos = (
    (gender == "Female")
    &
    (age < 50)
    &
    (
        np.random.rand(N) < 0.10
    )
).astype(int)

# ==========================
# Diabetes Risk Score
# ==========================
diabetes_risk = (
    (age > 45) * 2
    + (bmi > 30) * 2
    + (exercise_days_per_week <= 1) * 2
    + (daily_sitting_hours >= 10) * 1
    + (soft_drinks_per_week >= 7) * 1
    + (fast_food_meals_per_week >= 4) * 1
    + (smoking_status == "Current") * 1
    + (sleep_hours < 6) * 1
    + diabetes_family_score * 1
    + fatty_liver * 2
    + pcos * 2
    + (abdominal_obesity == "Moderate") * 1
    + (abdominal_obesity == "Severe") * 2
    + family_history_obesity * 1
)

# ==========================
# Hypertension Risk Score
# ==========================
hypertension_risk = (
    (age > 50) * 2
    + (pulse_rate > 90) * 1
    + (stress_level == "High") * 1
    + (salt_intake == "High") * 2
    + (smoking_status == "Current") * 1
    + hypertension_family_score * 1.5
    + sleep_apnea * 2
    + (abdominal_obesity == "Moderate") * 1
    + (abdominal_obesity == "Severe") * 2
)

# ==========================
# Hyperlipidemia Risk Score
# ==========================
hyperlipidemia_risk = (
    (age > 45) * 1
    + (bmi > 30) * 2
    + (fast_food_meals_per_week >= 5) * 1
    + (soft_drinks_per_week >= 10) * 1
    + (exercise_days_per_week <= 1) * 1
    + (daily_sitting_hours >= 10) * 1
    + (soft_drinks_per_week >= 7) * 1
    + (fast_food_meals_per_week >= 4) * 1
    + (smoking_status == "Current") * 1
    + hyperlipidemia_family_score * 1
    + fatty_liver * 2
)

# =====================================================
# Labels — SIGMOID MAPPING (KEY FIX)
# =====================================================
# OLD APPROACH (linear clip) added too much irreducible noise:
#   diabetic = np.random.binomial(1, np.clip(diabetes_risk / 30, 0.01, 0.95))
# This made probability rise too slowly and too linearly, so people with
# very different risk levels still had very similar outcome probabilities,
# capping any model's achievable AUC around ~0.65 regardless of algorithm.
#
# NEW APPROACH: logistic (sigmoid) mapping centered on a realistic midpoint,
# giving a much sharper separation between low-risk and high-risk people,
# while still keeping genuine randomness (no risk score guarantees outcome).

def risk_to_prob(risk, midpoint, steepness, low=0.02, high=0.93):
    prob = 1 / (1 + np.exp(-(risk - midpoint) / steepness))
    return np.clip(prob, low, high)


# Hyperlipidemia first
hyperlipidemia_prob = risk_to_prob(
    hyperlipidemia_risk,
    midpoint=8,
    steepness=2.2
)
hyperlipidemia = np.random.binomial(1, hyperlipidemia_prob)

# Hypertension affected by Hyperlipidemia
hypertension_risk = hypertension_risk + hyperlipidemia * 2

hypertension_prob = risk_to_prob(
    hypertension_risk,
    midpoint=9,
    steepness=2.2
)
hypertensive = np.random.binomial(1, hypertension_prob)

diabetes_prob = risk_to_prob(
    diabetes_risk,
    midpoint=9,
    steepness=2.2
)
diabetic = np.random.binomial(1, diabetes_prob)

# ==========================
# Derived Features
# ==========================
metabolic_syndrome = (
    (obesity == 1)
    &
    (
        diabetic + hypertensive + hyperlipidemia >= 2
    )
).astype(int)

age_group = pd.cut(
    age,
    bins=[18, 30, 45, 60, 80],
    labels=["18-30", "31-45", "46-60", "60+"]
)

# ==========================
# Symptoms
# ==========================
frequent_urination = np.random.binomial(
    1,
    np.where(
        (diabetic == 1) & (diabetes_risk >= 8),
        0.80,
        np.where(diabetic == 1, 0.55, 0.05)
    )
)

excessive_thirst = np.random.binomial(
    1,
    np.where(
        (diabetic == 1) & (diabetes_risk >= 8),
        0.80,
        np.where(diabetic == 1, 0.55, 0.05)
    )
)

fatigue = np.random.binomial(
    1,
    np.where(
        (diabetic == 1) & (diabetes_risk >= 8),
        0.80,
        np.where(diabetic == 1, 0.55, 0.05)
    )
)

blurred_vision = np.random.binomial(
    1,
    np.where(
        (diabetic == 1) & (diabetes_risk >= 8),
        0.80,
        np.where(diabetic == 1, 0.55, 0.05)
    )
)

slow_wound_healing = np.random.binomial(
    1,
    np.where(
        (diabetic == 1) & (diabetes_risk >= 8),
        0.80,
        np.where(diabetic == 1, 0.55, 0.05)
    )
)

headache = np.random.binomial(
    1,
    np.where(
        (hypertensive == 1) & (hypertension_risk >= 8),
        0.75,
        np.where(hypertensive == 1, 0.40, 0.10)
    )
)

dizziness = np.random.binomial(
    1,
    np.where(
        (hypertensive == 1) & (hypertension_risk >= 8),
        0.60,
        np.where(hypertensive == 1, 0.30, 0.05)
    )
)

# ==========================
# Create DataFrame
# ==========================
df = pd.DataFrame({
    "diabetes_risk": diabetes_risk,
    "hypertension_risk": hypertension_risk,
    "hyperlipidemia_risk": hyperlipidemia_risk,

    "diabetic": diabetic,
    "hypertensive": hypertensive,
    "hyperlipidemia": hyperlipidemia,

    "frequent_urination": frequent_urination,
    "excessive_thirst": excessive_thirst,
    "fatigue": fatigue,
    "blurred_vision": blurred_vision,
    "slow_wound_healing": slow_wound_healing,

    "headache": headache,
    "dizziness": dizziness,

    "age": age,
    "gender": gender,

    "height_cm": height_cm,
    "weight_kg": weight_kg,
    "bmi": np.round(bmi, 2),

    "pulse_rate": pulse_rate,

    "sleep_hours": sleep_hours,
    "diabetes_family_score": diabetes_family_score,
    "hypertension_family_score": hypertension_family_score,
    "hyperlipidemia_family_score": hyperlipidemia_family_score,
    "exercise_days_per_week": exercise_days_per_week,
    "daily_sitting_hours": daily_sitting_hours,
    "soft_drinks_per_week": soft_drinks_per_week,
    "fast_food_meals_per_week": fast_food_meals_per_week,
    "siblings_diabetes": siblings_diabetes,
    "metabolic_syndrome": metabolic_syndrome,
    "age_group": age_group,

    "smoking_status": smoking_status,

    "stress_level": stress_level,
    "salt_intake": salt_intake,

    "father_diabetes": father_diabetes,
    "mother_diabetes": mother_diabetes,

    "father_hypertension": father_hypertension,
    "mother_hypertension": mother_hypertension,

    "father_hyperlipidemia": father_hyperlipidemia,
    "mother_hyperlipidemia": mother_hyperlipidemia,

    "paternal_grandparents_diabetes": paternal_grandparents_diabetes,
    "maternal_grandparents_diabetes": maternal_grandparents_diabetes,

    "paternal_grandparents_hypertension": paternal_grandparents_hypertension,
    "maternal_grandparents_hypertension": maternal_grandparents_hypertension,

    "paternal_grandparents_hyperlipidemia": paternal_grandparents_hyperlipidemia,
    "maternal_grandparents_hyperlipidemia": maternal_grandparents_hyperlipidemia,

    "fatty_liver": fatty_liver,
    "sleep_apnea": sleep_apnea,
    "abdominal_obesity": abdominal_obesity,
    "family_history_obesity": family_history_obesity,
    "pcos": pcos

})

# ==========================
# Preview
# ==========================
print(df.head())

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nDescription:")
print(df.describe())

# ==========================
# Save Dataset
# ==========================
os.makedirs("../../datasets", exist_ok=True)
print("\nDisease prevalence")

print(
    df[
        [
            "diabetic",
            "hypertensive",
            "hyperlipidemia"
        ]
    ].mean()
)

df.to_csv(
    "../../datasets/egypt_health_dataset_v5.csv",
    index=False
)

print("\nDataset saved successfully as egypt_health_dataset_v5.csv")

print(df[[
    "diabetes_risk",
    "hypertension_risk",
    "hyperlipidemia_risk"
]].describe())