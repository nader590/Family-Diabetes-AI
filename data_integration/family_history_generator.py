import pandas as pd
import numpy as np

# ===================
# Load datasets
# ===================
nhanes = pd.read_csv("../datasets/nhanes_clean.csv")
brfss = pd.read_csv("../datasets/brfss_clean.csv")

def add_family_history(df):

    # Diabetes
    prob_diabetes = np.where(
        (df["diabetic"] == 1) | (df["bmi"] >= 30),
        0.7,
        0.2
    )

    df["father_diabetes"] = (
        np.random.rand(len(df)) < prob_diabetes
    ).astype(int)

    df["mother_diabetes"] = (
        np.random.rand(len(df)) < prob_diabetes
    ).astype(int)

    df["siblings_diabetes"] = (
        np.random.rand(len(df)) < prob_diabetes * 0.8
    ).astype(int)

    df["paternal_grandparents_diabetes"] = (
        np.random.rand(len(df)) < prob_diabetes
    ).astype(int)

    df["maternal_grandparents_diabetes"] = (
        np.random.rand(len(df)) < prob_diabetes
    ).astype(int)

    # Hypertension
    df["father_hypertension"] = (
        np.random.rand(len(df)) < 0.3
    ).astype(int)

    df["mother_hypertension"] = (
        np.random.rand(len(df)) < 0.3
    ).astype(int)

    # Hyperlipidemia
    df["father_hyperlipidemia"] = (
        np.random.rand(len(df)) < 0.25
    ).astype(int)

    df["mother_hyperlipidemia"] = (
        np.random.rand(len(df)) < 0.25
    ).astype(int)

    # Obesity
    df["family_history_obesity"] = (
        np.random.rand(len(df)) < 0.35
    ).astype(int)

    # Family scores
    df["diabetes_family_score"] = (
        df["father_diabetes"] * 4 +
        df["mother_diabetes"] * 4 +
        df["siblings_diabetes"] * 3 +
        df["paternal_grandparents_diabetes"] +
        df["maternal_grandparents_diabetes"]
    )

    df["hypertension_family_score"] = (
        df["father_hypertension"] * 4 +
        df["mother_hypertension"] * 4
    )

    df["hyperlipidemia_family_score"] = (
        df["father_hyperlipidemia"] * 4 +
        df["mother_hyperlipidemia"] * 4
    )

    return df


nhanes = add_family_history(nhanes)
brfss = add_family_history(brfss)

nhanes.to_csv("../datasets/nhanes_final.csv", index=False)
brfss.to_csv("../datasets/brfss_final.csv", index=False)

print("Done")