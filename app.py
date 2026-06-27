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
col1, col2 = st.columns([8,1])

with col2:

    language = st.selectbox(
        "🌍",
        ["English", "العربية"]
    )


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
# Page Configuration
# ======================================================

# ======================================================
# Title
# ======================================================

st.markdown("""

<style>

.main{

    padding-top:1rem;

}

.block-container{

    padding-top:2rem;

    padding-bottom:2rem;

}

div[data-testid="metric-container"]{

    border-radius:15px;

    padding:20px;

    border:1px solid #E5E7EB;

    background:#F8FAFC;

    box-shadow:0px 4px 15px rgba(0,0,0,.08);

}

.stButton>button{
    h1{
        color:#2563EB;
    }

    h2{
        color:#0F172A;
    }

    h3{
        color:#334155;
    }

    .stMetric{
        background:white;
    }

    width:100%;

    height:55px;

    border-radius:12px;

    font-size:18px;

    font-weight:bold;

}
.stProgress > div > div > div > div{

    background-color:#10B981;

}

</style>

""",unsafe_allow_html=True)
st.title(APP_TITLE)

st.markdown("""

### Predict your future health risks using Artificial Intelligence

Diabetes • Hypertension • Hyperlipidemia

---

""")


# ======================================================
# Start Form
# ======================================================

with st.form("health_form"):

    # ======================================================
    # Personal Information
    # ======================================================
    st.header(PERSONAL_INFO)

    col1, col2 = st.columns(2)

    with col1:

        full_name = st.text_input(
            "Full Name"
        )

        age = st.slider(
            "Age",
            min_value=18,
            max_value=120,
            value=30
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

    with col2:

        height_cm = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=230,
            value=170
        )

        weight_kg = st.slider(
            "Weight (kg)",
            min_value=30.0,
            max_value=250.0,
            value=75.0
        )

    bmi = weight_kg / ((height_cm / 100) ** 2)

    st.metric(
        "BMI",
        round(bmi, 2)
    )

    st.divider()

    # ======================================================
    # Lifestyle
    # ======================================================

    st.header(LIFESTYLE)

    col1, col2 = st.columns(2)

    with col1:

        smoking_status = st.selectbox(
            "Smoking Status",
            [
                "Never",
                "Former",
                "Current"
            ]
        )

        exercise_days_per_week = st.slider(
            "Exercise Days Per Week",
            0,
            7,
            3
        )

        sleep_hours = st.slider(
            "Sleep Hours",
            3,
            12,
            7
        )

    with col2:

        daily_sitting_hours = st.slider(
            "Daily Sitting Hours",
            0,
            16,
            8
        )

        soft_drinks_per_week = st.slider(
            "Soft Drinks Per Week",
            0,
            20,
            3
        )

        fast_food_meals_per_week = st.slider(
            "Fast Food Meals Per Week",
            0,
            20,
            2
        )

    st.divider()



    # ==========================================
    # Family History
    # ==========================================

    st.header(FAMILY)
    options = [
            "Unknown",
            "No",
            "Yes"
    ]

    st.caption(
            "If you don't know whether a family member had a disease, choose 'Unknown'."
    )

    # =====================================================
    # Father
    # =====================================================

    st.subheader("👨 Father")

    col1, col2, col3 = st.columns(3)

    with col1:
        father_diabetes = st.selectbox(
            "Diabetes",
            options,
            key="father_diabetes"
        )

    with col2:
        father_hypertension = st.selectbox(
            "Hypertension",
            options,
            key="father_hypertension"
        )

    with col3:
        father_hyperlipidemia = st.selectbox(
            "Hyperlipidemia",
            options,
            key="father_hyperlipidemia"
        )

    # =====================================================
    # Mother
    # =====================================================

    st.subheader("👩 Mother")

    col1, col2, col3 = st.columns(3)

    with col1:
        mother_diabetes = st.selectbox(
            "Diabetes",
            options,
            key="mother_diabetes"
        )

    with col2:
        mother_hypertension = st.selectbox(
            "Hypertension",
            options,
            key="mother_hypertension"
        )

    with col3:
        mother_hyperlipidemia = st.selectbox(
            "Hyperlipidemia",
            options,
            key="mother_hyperlipidemia"
        )

    # =====================================================
    # Father's Parents
    # =====================================================

    st.subheader("👴👵 Father's Parents")

    col1, col2, col3 = st.columns(3)

    with col1:
        paternal_diabetes = st.selectbox(
            "Diabetes",
            options,
            key="paternal_diabetes"
        )

    with col2:
        paternal_hypertension = st.selectbox(
            "Hypertension",
            options,
            key="paternal_hypertension"
        )

    with col3:
        paternal_hyperlipidemia = st.selectbox(
            "Hyperlipidemia",
            options,
            key="paternal_hyperlipidemia"
        )

    # =====================================================
    # Mother's Parents
    # =====================================================

    st.subheader("👴👵 Mother's Parents")

    col1, col2, col3 = st.columns(3)

    with col1:
        maternal_diabetes = st.selectbox(
            "Diabetes",
            options,
            key="maternal_diabetes"
        )

    with col2:
        maternal_hypertension = st.selectbox(
            "Hypertension",
            options,
            key="maternal_hypertension"
        )

    with col3:
        maternal_hyperlipidemia = st.selectbox(
            "Hyperlipidemia",
            options,
            key="maternal_hyperlipidemia"
        )

    st.divider()

    # ==========================================
    # Current Medical History
    # ==========================================

    st.header(MEDICAL)

    col1, col2 = st.columns(2)

    with col1:

        hypertension = st.selectbox(
            "Hypertension",
            options,
            key="hypertension"
        )

        hyperlipidemia = st.selectbox(
            "Hyperlipidemia",
            options,
            key="hyperlipidemia"
        )

    with col2:

        fatty_liver = st.selectbox(
            "Fatty Liver",
            options,
            key="fatty_liver"
        )

        sleep_apnea = st.selectbox(
            "Sleep Apnea",
            options,
            key="sleep_apnea"
        )

    st.divider()

    # ==========================================
    # Measurements
    # ==========================================

    st.header(MEASUREMENTS)

    st.metric(
        "Current BMI",
        round(bmi,2)
    )

  

    with col2:

        st.metric(
            "Current BMI",
            round(bmi, 2)
        )

    st.divider()

    # ==========================================
    # Submit Button
    # ==========================================

    submit = st.form_submit_button(
       ANALYZE
    )


# ======================================================
# Prediction Pipeline
# ======================================================
# ==========================================
# Helpers
# ==========================================



if submit:
    st.success("✅ Analysis Completed Successfully")

    st.divider()


    # ----------------------------------------
    # Helper Function
    # ----------------------------------------

    def yn(value):
        if value == "Yes":
            return 1
        return 0



    # ----------------------------------------
    # Feature Dictionary
    # ----------------------------------------
    if not full_name.strip():

        st.error("Please enter your full name.")

        st.stop()
    patient = {
        
        "full_name": full_name,

        "age": age,
        "gender": gender,

        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": round(bmi,2),

       # "pulse_rate": pulse_rate,

        "sleep_hours": sleep_hours,

        "exercise_days_per_week":
            exercise_days_per_week,

        "daily_sitting_hours":
            daily_sitting_hours,

        "soft_drinks_per_week":
            soft_drinks_per_week,

        "fast_food_meals_per_week":
            fast_food_meals_per_week,

        "smoking_status":
            smoking_status,

        "father_diabetes":
            yn(father_diabetes),

        "mother_diabetes":
            yn(mother_diabetes),

        "father_hypertension":
            yn(father_hypertension),

        "mother_hypertension":
            yn(mother_hypertension),

        "father_hyperlipidemia":
            yn(father_hyperlipidemia),

        "mother_hyperlipidemia":
            yn(mother_hyperlipidemia),

        "paternal_grandparents_diabetes":
            yn(paternal_diabetes),

        "maternal_grandparents_diabetes":
            yn(maternal_diabetes),

        "paternal_grandparents_hypertension":
            yn(paternal_hypertension),

        "maternal_grandparents_hypertension":
            yn(maternal_hypertension),

        "paternal_grandparents_hyperlipidemia":
            yn(paternal_hyperlipidemia),

        "maternal_grandparents_hyperlipidemia":
            yn(maternal_hyperlipidemia),



        "fatty_liver":
            yn(fatty_liver),

        "sleep_apnea":
            yn(sleep_apnea),

        "hyperlipidemia":
            yn(hyperlipidemia),

        "hypertensive":
            yn(hypertension)

    }
    results = predictor.predict(patient)
    recommendations = engine.build(

        patient,

        results

    )
    
    st.subheader("❤️ Health Score")

    st.progress(
        recommendations["health_score"] / 100
    )

    st.metric(
        "Health Score",
        f'{recommendations["health_score"]}/100'
    )
        
    
    
    st.divider()

    

    patient["diabetes_probability"] = results["diabetes_probability"]

    patient["hypertension_probability"] = results["hypertension_probability"]

    patient["hyperlipidemia_probability"] = results["hyperlipidemia_probability"]

    patient["overall_risk"] = max(

    patient["diabetes_probability"],

    patient["hypertension_probability"],

    patient["hyperlipidemia_probability"]

    )

    patient["selected_model"] = "Ultimate Ensemble"

    patient["model_version"] = "v1.0"

    patient["predicted_label"] = int(
        patient["overall_risk"] >= 0.50
    )

    patient["health_score"] = recommendations["health_score"]

    st.subheader("Prediction Results")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🩸 Diabetes",
            f"{results['diabetes_probability']*100:.1f}%"
        )

        st.progress(
            results["diabetes_probability"]
        )


    with col2:

        st.metric(
            "❤️ Hypertension",
            f"{results['hypertension_probability']*100:.1f}%"
        )

        st.progress(
            results["hypertension_probability"]
        )


    with col3:

        st.metric(
            "🫀 Hyperlipidemia",
            f"{results['hyperlipidemia_probability']*100:.1f}%"
        )

        st.progress(
            results["hyperlipidemia_probability"]
        )

    st.divider()

    st.subheader("📊 Overall Assessment")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Overall Health Score",
            f"{recommendations['health_score']}/100"
        )

    with col2:

        risk = recommendations["overall_risk"]

        if risk == "Low":
            st.success("🟢 Low Risk")

        elif risk == "Moderate":
            st.warning("🟡 Moderate Risk")

        else:
            st.error("🔴 High Risk")

    save_user(patient)

    st.divider()

    st.divider()

    st.subheader("⚠ Risk Factors")

    if recommendations["reasons"]:

        for reason in recommendations["reasons"]:

            st.warning(reason)

    else:

        st.success("No major risk factors detected.")

    st.divider()

    st.subheader("🍎 Recommendations")

    for rec in recommendations["recommendations"]:

        st.success(rec)

    st.divider()

    st.subheader("🧪 Suggested Medical Tests")

    for test in recommendations["tests"]:

        st.info(test)

    pdf = report_generator.generate(
        patient,
        results,
        recommendations
    )

    with open(pdf, "rb") as file:

        st.download_button(

            "📄 Download Health Report",

            data=file,

            file_name="Health_Report.pdf",

            mime="application/pdf"

        )