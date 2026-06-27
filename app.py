import streamlit as st
from utils.predictor import predictor
from recommendations import engine
from supabase_db import save_user
from report import report_generator

st.set_page_config(
    page_title="AI Preventive Healthcare Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

col1, col2 = st.columns([8, 1])

with col2:
    language = st.selectbox("🌍", ["English", "العربية"])

if language == "العربية":
    st.markdown(
        """
        <style>
            [data-testid="stAppViewContainer"]{
            direction:rtl;
             }
        </style>
        """,
        unsafe_allow_html=True
    )

if language == "English":
    APP_TITLE = "AI Preventive Healthcare Assistant"
    PERSONAL_INFO = "👤 Personal Information"
    LIFESTYLE = "🏃 Lifestyle"
    FAMILY = "🧬 Family History"
    MEDICAL = "❤️ Current Medical History"
    MEASUREMENTS = "🩺 Measurements"
    ANALYZE = "🩺 Analyze My Health"
else:
    APP_TITLE = "🩺 مساعد الرعاية الصحية الذكي"
    PERSONAL_INFO = "👤 المعلومات الشخصية"
    LIFESTYLE = "🏃 نمط الحياة"
    FAMILY = "🧬 التاريخ المرضي للعائلة"
    MEDICAL = "❤️ التاريخ المرضي الحالي"
    MEASUREMENTS = "🩺 القياسات الصحية"
    ANALYZE = "🩺 تحليل الحالة الصحية"

# ======================================================
# Styling
# ======================================================
st.markdown("""
<style>
.main{ padding-top:1rem; }
.block-container{ padding-top:2rem; padding-bottom:2rem; }

div[data-testid="metric-container"]{
    padding:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,.08);
    background:#111827;
    color:#F9FAFB;
    border:1px solid #374151;
}

.stButton>button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
}

.stProgress > div > div > div > div{
    background-color:#10B981;
}

.risk-badge{
    display:inline-block;
    padding:4px 14px;
    border-radius:14px;
    font-weight:600;
    font-size:13px;
    color:white;
}

.factor-card{
    background:#111827;
    border:1px solid #374151;
    border-radius:12px;
    padding:14px 18px;
    margin-bottom:8px;
    color:#F9FAFB;
}

.narrative-box{
    border-left:4px solid #2563EB;
    border-radius:8px;
    padding:16px 20px;
    margin-bottom:14px;
    white-space:pre-line;
    font-size:15px;
    background:#1E293B;
    color:#F8FAFC;
}
</style>
""", unsafe_allow_html=True)

st.title(APP_TITLE)
st.markdown("""
### Predict your future health risks using Artificial Intelligence
Diabetes • Hypertension • Hyperlipidemia
---
""")

RISK_COLORS = {"Low": "#2ecc71", "Moderate": "#f39c12", "High": "#e74c3c"}
HEALTH_LEVEL_COLORS = {
    "Excellent": "#2ecc71", "Good": "#27ae60",
    "Moderate": "#f39c12", "Poor": "#e67e22", "Critical": "#e74c3c"
}


def risk_badge_html(level):
    color = RISK_COLORS.get(level, "#7f8c8d")
    return f'<span class="risk-badge" style="background-color:{color};">{level} Risk</span>'


def reduction_label(reduction_pct):
    if reduction_pct >= 10:
        return "Large"
    if reduction_pct >= 5:
        return "Moderate"
    if reduction_pct > 0:
        return "Small"
    return "Minimal"


# ======================================================
# Form
# ======================================================
with st.form("health_form"):

    st.header(PERSONAL_INFO)
    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full Name")
        age = st.slider("Age", min_value=18, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])

    with col2:
        height_cm = st.number_input("Height (cm)", min_value=100, max_value=230, value=170)
        weight_kg = st.slider("Weight (kg)", min_value=30.0, max_value=250.0, value=75.0)

    bmi = weight_kg / ((height_cm / 100) ** 2)
    st.metric("BMI", round(bmi, 2))

    st.divider()

    st.header(LIFESTYLE)
    col1, col2 = st.columns(2)

    with col1:
        smoking_status = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
        exercise_days_per_week = st.slider("Exercise Days Per Week", 0, 7, 3)
        sleep_hours = st.slider("Sleep Hours", 3, 12, 7)

    with col2:
        daily_sitting_hours = st.slider("Daily Sitting Hours", 0, 16, 8)
        soft_drinks_per_week = st.slider("Soft Drinks Per Week", 0, 20, 3)
        fast_food_meals_per_week = st.slider("Fast Food Meals Per Week", 0, 20, 2)

    st.divider()

    st.header(FAMILY)
    options = ["Unknown", "No", "Yes"]
    st.caption("If you don't know whether a family member had a disease, choose 'Unknown'.")

    st.subheader("👨 Father")
    col1, col2, col3 = st.columns(3)
    with col1:
        father_diabetes = st.selectbox("Diabetes", options, key="father_diabetes")
    with col2:
        father_hypertension = st.selectbox("Hypertension", options, key="father_hypertension")
    with col3:
        father_hyperlipidemia = st.selectbox("Hyperlipidemia", options, key="father_hyperlipidemia")

    st.subheader("👩 Mother")
    col1, col2, col3 = st.columns(3)
    with col1:
        mother_diabetes = st.selectbox("Diabetes", options, key="mother_diabetes")
    with col2:
        mother_hypertension = st.selectbox("Hypertension", options, key="mother_hypertension")
    with col3:
        mother_hyperlipidemia = st.selectbox("Hyperlipidemia", options, key="mother_hyperlipidemia")

    st.subheader("👴👵 Father's Parents")
    col1, col2, col3 = st.columns(3)
    with col1:
        paternal_diabetes = st.selectbox("Diabetes", options, key="paternal_diabetes")
    with col2:
        paternal_hypertension = st.selectbox("Hypertension", options, key="paternal_hypertension")
    with col3:
        paternal_hyperlipidemia = st.selectbox("Hyperlipidemia", options, key="paternal_hyperlipidemia")

    st.subheader("👴👵 Mother's Parents")
    col1, col2, col3 = st.columns(3)
    with col1:
        maternal_diabetes = st.selectbox("Diabetes", options, key="maternal_diabetes")
    with col2:
        maternal_hypertension = st.selectbox("Hypertension", options, key="maternal_hypertension")
    with col3:
        maternal_hyperlipidemia = st.selectbox("Hyperlipidemia", options, key="maternal_hyperlipidemia")

    st.divider()

    st.header(MEDICAL)
    col1, col2 = st.columns(2)
    with col1:
        hypertension = st.selectbox("Hypertension", options, key="hypertension")
        hyperlipidemia = st.selectbox("Hyperlipidemia", options, key="hyperlipidemia")
    with col2:
        fatty_liver = st.selectbox("Fatty Liver", options, key="fatty_liver")
        sleep_apnea = st.selectbox("Sleep Apnea", options, key="sleep_apnea")

    st.divider()

    st.header(MEASUREMENTS)
    st.metric("Current BMI", round(bmi, 2))

    st.divider()

    submit = st.form_submit_button(ANALYZE)


# ======================================================
# Prediction Pipeline
# ======================================================
if submit:

    def yn(value):
        return 1 if value == "Yes" else 0

    if not full_name.strip():
        st.error("Please enter your full name.")
        st.stop()

    st.success("✅ Analysis Completed Successfully")
    st.divider()

    patient = {
        "full_name": full_name,
        "age": age,
        "gender": gender,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": round(bmi, 2),
        "sleep_hours": sleep_hours,
        "exercise_days_per_week": exercise_days_per_week,
        "daily_sitting_hours": daily_sitting_hours,
        "soft_drinks_per_week": soft_drinks_per_week,
        "fast_food_meals_per_week": fast_food_meals_per_week,
        "smoking_status": smoking_status,
        "father_diabetes": yn(father_diabetes),
        "mother_diabetes": yn(mother_diabetes),
        "father_hypertension": yn(father_hypertension),
        "mother_hypertension": yn(mother_hypertension),
        "father_hyperlipidemia": yn(father_hyperlipidemia),
        "mother_hyperlipidemia": yn(mother_hyperlipidemia),
        "paternal_grandparents_diabetes": yn(paternal_diabetes),
        "maternal_grandparents_diabetes": yn(maternal_diabetes),
        "paternal_grandparents_hypertension": yn(paternal_hypertension),
        "maternal_grandparents_hypertension": yn(maternal_hypertension),
        "paternal_grandparents_hyperlipidemia": yn(paternal_hyperlipidemia),
        "maternal_grandparents_hyperlipidemia": yn(maternal_hyperlipidemia),
        "fatty_liver": yn(fatty_liver),
        "sleep_apnea": yn(sleep_apnea),
        "hyperlipidemia": yn(hyperlipidemia),
        "hypertensive": yn(hypertension),
    }

    # ---- Unchanged prediction call ----
    results = predictor.predict(patient)

    # ---- New explainable recommendation engine ----
    recommendations = engine.build(patient, results)

    # ==================================================
    # Overall Health Score (with breakdown)
    # ==================================================
    st.subheader("❤️ Overall Health Score")

    score_full = recommendations["health_score_full"]
    score = score_full["score"]
    level = score_full["level"]
    color = HEALTH_LEVEL_COLORS.get(level, "#7f8c8d")

    sc1, sc2 = st.columns([1, 3])
    with sc1:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <div style="font-size:46px; font-weight:700; color:{color};">{score}</div>
                <div style="font-size:16px; color:{color}; font-weight:600;">{level}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sc2:
        st.progress(score / 100)
        with st.expander("See what's driving your Health Score"):
            b = score_full["breakdown"]
            st.write(f"- Model-predicted disease risk: **{b['model_risk']}%** impact")
            st.write(f"- BMI: **{b['bmi']}%** impact")
            st.write(f"- Family history: **{b['family_history']}%** impact")
            st.write(f"- Lifestyle: **{b['lifestyle']}%** impact")
            st.write(f"- Existing conditions: **{b['existing_conditions']}%** impact")

    st.divider()

    # ==================================================
    # Prediction Results
    # ==================================================
    patient["diabetes_probability"] = results["diabetes_probability"]
    patient["hypertension_probability"] = results["hypertension_probability"]
    patient["hyperlipidemia_probability"] = results["hyperlipidemia_probability"]
    patient["overall_risk"] = max(
        patient["diabetes_probability"],
        patient["hypertension_probability"],
        patient["hyperlipidemia_probability"],
    )
    patient["selected_model"] = "Ultimate Ensemble"
    patient["model_version"] = "v1.0"
    patient["predicted_label"] = int(patient["overall_risk"] >= 0.50)
    patient["health_score"] = score

    st.subheader("📋 Prediction Results")
    col1, col2, col3 = st.columns(3)

    disease_meta = [
        ("diabetes", "🩸 Diabetes", col1),
        ("hypertension", "❤️ Hypertension", col2),
        ("hyperlipidemia", "🫀 Hyperlipidemia", col3),
    ]

    for disease_key, disease_label, col in disease_meta:
        prob = results[f"{disease_key}_probability"]
        with col:
            st.metric(disease_label, f"{prob*100:.1f}%")
            st.progress(prob)
            risk_lvl = "Low" if prob < 0.30 else ("Moderate" if prob < 0.60 else "High")
            st.markdown(risk_badge_html(risk_lvl), unsafe_allow_html=True)

    st.divider()

    # ==================================================
    # Why? — Model-driven narrative explanations
    # ==================================================
    st.subheader("🧠 Why these numbers? (AI Explanation)")

    for disease_key, disease_label, _ in disease_meta:
        narrative = recommendations["narratives"].get(disease_key, "")
        with st.expander(f"{disease_label} — explanation"):
            explanation = recommendations["explanations"][disease_key]
            st.markdown(f'<div class="narrative-box">{narrative}</div>', unsafe_allow_html=True)

            if explanation["contributing"]:
                if explanation["protective"]:
                    st.markdown("**Protective factors:**")
                    for p in explanation["protective"]:
                        st.write(f"- {p['label']} ({p['value_display']})")

    st.divider()

    # ==================================================
    # Top Risk Factors (across all diseases)
    # ==================================================
    st.subheader("⚠️ Top Risk Factors Overall")

    all_factors = []
    for disease_key, _, _ in disease_meta:
        for f in recommendations["explanations"][disease_key]["contributing"]:
            all_factors.append({"disease": disease_key, **f})

    all_factors = sorted(all_factors, key=lambda f: f["impact"], reverse=True)[:6]

    if all_factors:
        for f in all_factors:
            st.markdown(
                f'<div class="factor-card">'
                f'<b>{f["label"]}</b> ({f["value_display"]}) — '
                f'increases <b>{f["disease"]}</b> risk'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.success("No dominant risk factors detected.")

    st.divider()

    # ==================================================
    # Family Disease Impact
    # ==================================================
    st.subheader("🧬 Family Disease Impact")

    fcol1, fcol2, fcol3 = st.columns(3)
    for (disease_key, disease_label, _), fcol in zip(disease_meta, [fcol1, fcol2, fcol3]):
        fr = recommendations["family_risk"][disease_key]
        with fcol:
            st.markdown(f"**{disease_label}**")
            st.markdown(risk_badge_html(fr["level"]), unsafe_allow_html=True)
            st.caption(f"Family Risk Score: {fr['score']}%")
            contributors = [
                k.replace("_", " ").title()
                for k in ("father", "mother", "paternal_grandparents", "maternal_grandparents")
                if fr.get(k)
            ]
            if contributors:
                st.caption("Reported history: " + ", ".join(contributors))
            else:
                st.caption("No reported family history")

    st.divider()

    # ==================================================
    # What-If Simulation
    # ==================================================
    st.subheader("🔁 What-If Simulation")
    st.caption("These results come from re-running the actual trained models with modified inputs.")

    what_if = recommendations["what_if"]

    if what_if["all_scenarios"]:
        for scenario in what_if["all_scenarios"]:
            wc1, wc2, wc3 = st.columns([2, 1, 1])
            with wc1:
                st.write(f"**{scenario['label']}**")
            with wc2:
                st.metric(
                    f"{scenario['primary_disease'].title()} risk",
                    f"{scenario['after_pct']}%",
                    delta=f"-{scenario['reduction_pct']}%"
                )
            with wc3:
                st.write(f"Reduction: **{reduction_label(scenario['reduction_pct'])}**")
        st.markdown("---")
    else:
        st.info("No applicable simulation scenarios for this profile.")

    st.divider()

    # ==================================================
    # Recommendations & Tests
    # ==================================================
    st.subheader("🍎 Recommendations")
    for rec in recommendations["recommendations"]:
        st.success(rec)

    st.divider()

    st.subheader("🧪 Suggested Medical Tests")
    for test in recommendations["tests"]:
        st.info(test)

    st.divider()

    # ==================================================
    # Overall Assessment + Save + Report
    # ==================================================
    st.subheader("📊 Overall Assessment")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Overall Health Score", f"{score}/100")

    with col2:
        risk = recommendations["overall_risk"]
        if risk == "Low":
            st.success("🟢 Low Risk")
        elif risk == "Moderate":
            st.warning("🟡 Moderate Risk")
        else:
            st.error("🔴 High Risk")

        try:
            save_user(patient)
            st.success("Saved to Supabase")
        except Exception as e:
            st.error(str(e))

    st.divider()

    pdf = report_generator.generate(patient, results, recommendations)

    with open(pdf, "rb") as file:
        st.download_button(
            "📄 Download Health Report",
            data=file,
            file_name="Health_Report.pdf",
            mime="application/pdf"
        )