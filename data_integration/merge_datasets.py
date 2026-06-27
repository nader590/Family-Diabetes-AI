import pandas as pd

# ==========================
# Load datasets
# ==========================
egypt = pd.read_csv("../datasets/egypt_health_dataset_v5.csv")
nhanes = pd.read_csv("../datasets/nhanes_clean.csv")
brfss = pd.read_csv("../datasets/brfss_clean.csv")

# ==========================
# Add source column
# ==========================
egypt["source"] = "egypt"
nhanes["source"] = "nhanes"
brfss["source"] = "brfss"

# ==========================
# Unify columns
# ==========================
all_columns = sorted(
    list(
        set(egypt.columns)
        | set(nhanes.columns)
        | set(brfss.columns)
    )
)

egypt = egypt.reindex(columns=all_columns)
nhanes = nhanes.reindex(columns=all_columns)
brfss = brfss.reindex(columns=all_columns)

# ==========================
# Merge datasets
# ==========================
final_df = pd.concat(
    [egypt, nhanes, brfss],
    ignore_index=True
)

# ==========================
# Remove duplicate rows
# ==========================
final_df = final_df.drop_duplicates()
print("\nColumns:")
print(final_df.columns.tolist())

print("\nMissing Percentage:")
print((final_df.isnull().mean() * 100).sort_values(ascending=False).head(20))

# ==========================
# Information
# ==========================
print("\nShape:")
print(final_df.shape)

print("\nSource Counts:")
print(final_df["source"].value_counts())

print("\nMissing Values:")
print(final_df.isnull().sum())

print("\nPreview:")
print(final_df.head())

# ==========================
# Save dataset
# ==========================
final_df.to_csv(
    "../datasets/egypt_health_dataset_v6.csv",
    index=False
)

print("\nDataset V6 saved successfully.")