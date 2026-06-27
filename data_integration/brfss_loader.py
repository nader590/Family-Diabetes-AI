import pandas as pd
import numpy as np

df = pd.read_sas("../datasets/raw/brfss/LLCP2023.XPT")

master = pd.DataFrame()

master["age"] = df["_AGE80"]

master["gender"] = df["_SEX"].map({
    1: "Male",
    2: "Female"
})

master["weight_kg"] = df["WTKG3"] / 100

master["bmi"] = df["_BMI5"] / 100

master["diabetic"] = (df["DIABETE4"] == 1).astype(int)

# مؤقتا
master["father_diabetes"] = np.nan
master["mother_diabetes"] = np.nan
master["siblings_diabetes"] = np.nan

master["father_hypertension"] = np.nan
master["mother_hypertension"] = np.nan

master["father_hyperlipidemia"] = np.nan
master["mother_hyperlipidemia"] = np.nan

master["fatty_liver"] = np.nan
master["sleep_apnea"] = np.nan
master["pcos"] = np.nan

master.to_csv(
    "../datasets/brfss_clean.csv",
    index=False
)

print(master.head())
print("BRFSS saved successfully")