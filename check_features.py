import joblib

print("=" * 50)
print("DIABETES FEATURES")
print("=" * 50)

features = joblib.load("models/diabetes_feature_names.pkl")

for f in sorted(features):
    print(f)

print("\n" + "=" * 50)
print("HYPERTENSION FEATURES")
print("=" * 50)

features = joblib.load("models/hypertensive_feature_names.pkl")

for f in sorted(features):
    print(f)

print("\n" + "=" * 50)
print("HYPERLIPIDEMIA FEATURES")
print("=" * 50)

features = joblib.load("models/hyperlipidemia_feature_names.pkl")

for f in sorted(features):
    print(f)