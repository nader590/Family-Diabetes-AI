import pandas as pd
import numpy as np

# ==========================
# Load NHANES Files
# ==========================
demo = pd.read_sas("../datasets/raw/nhanes/DEMO_J.xpt")
bmx = pd.read_sas("../datasets/raw/nhanes/BMX_J.xpt")
diq = pd.read_sas("../datasets/raw/nhanes/DIQ_J.xpt")
smq = pd.read_sas("../datasets/raw/nhanes/SMQ_J.xpt")
bpq = pd.read_sas("../datasets/raw/nhanes/BPQ_J.xpt")
paq = pd.read_sas("../datasets/raw/nhanes/PAQ_J.xpt")
slq = pd.read_sas("../datasets/raw/nhanes/SLQ_J.xpt")

# ==========================
# Merge Files
# ==========================
df = demo.merge(bmx, on="SEQN", how="left")
df = df.merge(diq, on="SEQN", how="left")
df = df.merge(smq, on="SEQN", how="left")
df = df.merge(bpq, on="SEQN", how="left")
df = df.merge(paq, on="SEQN", how="left")
df = df.merge(slq, on="SEQN", how="left")

# ==========================
# Rename Important Columns
# ==========================
df = df.rename(columns={
    "RIDAGEYR": "age",
    "RIAGENDR": "gender",
    "BMXBMI": "bmi",
    "BMXWT": "weight_kg",
    "DIQ010": "diabetic"
})

# ==========================
# Create Master DataFrame
# ==========================
master = pd.DataFrame()

master["age"] = df["age"]

master["gender"] = df["gender"].map({
    1: "Male",
    2: "Female"
})

master["weight_kg"] = df["weight_kg"]

master["bmi"] = df["bmi"]

master["diabetic"] = (df["diabetic"] == 1).astype(int)

# ==========================
# Family History
# ==========================
master["father_diabetes"] = np.nan
master["mother_diabetes"] = np.nan
master["siblings_diabetes"] = np.nan

master["father_hypertension"] = np.nan
master["mother_hypertension"] = np.nan

master["father_hyperlipidemia"] = np.nan
master["mother_hyperlipidemia"] = np.nan

master["paternal_grandparents_diabetes"] = np.nan
master["maternal_grandparents_diabetes"] = np.nan

# ==========================
# Other Features
# ==========================
master["fatty_liver"] = np.nan
master["sleep_apnea"] = np.nan
master["pcos"] = np.nan

# ==========================
# Save
# ==========================
print(master.head())

master.to_csv(
    "../datasets/nhanes_clean.csv",
    index=False
)

print("\nNHANES dataset saved successfully.")