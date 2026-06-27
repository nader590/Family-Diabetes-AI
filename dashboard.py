import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(

    page_title="Admin Dashboard",

    page_icon="📊",

    layout="wide"

)
st.markdown("""

<style>

div[data-testid="metric-container"]{

    background:#F8FAFC;

    border-radius:15px;

    padding:20px;

    border:1px solid #E5E7EB;

    box-shadow:0px 4px 10px rgba(0,0,0,.08);

}

</style>

""",unsafe_allow_html=True)
st.title("📊 AI Preventive Healthcare Dashboard")

connection = sqlite3.connect("database/healthcare.db")

df = pd.read_sql(

    "SELECT * FROM users",

    connection

)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Users",

        len(df)

    )

with col2:

    st.metric(

        "Average Age",

        round(df["age"].mean(),1)

    )

with col3:

    st.metric(

        "Average BMI",

        round(df["bmi"].mean(),1)

    )

with col4:

    st.metric(

        "Average Health Score",

        round(df["health_score"].mean(),1)

    )

        
    st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 BMI Distribution")

    fig = px.histogram(
        df,
        x="bmi",
        nbins=10
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("👨 Gender Distribution")

    gender_df = df["gender"].value_counts()

    st.bar_chart(gender_df)

st.divider()

risk_df = df[[
    "diabetes_probability",
    "hypertension_probability",
    "hyperlipidemia_probability"
]]

st.subheader("🩺 Average Disease Risk")

st.bar_chart(
    risk_df.mean()
)
st.divider()



st.divider()

st.subheader("👥 Recent Users")

st.dataframe(

    df[[
        "full_name",
        "age",
        "gender",
        "bmi",
        "health_score",
        "diabetes_probability",
        "hypertension_probability",
        "hyperlipidemia_probability"
    ]].tail(20)

)
st.divider()

st.subheader("🚨 Highest Risk Users")

top_risk = df.sort_values(

    by="overall_risk",

    ascending=False

)

st.dataframe(

    top_risk[[

        "full_name",

        "overall_risk",

        "health_score"

    ]].head(10)

)

csv = df.to_csv(index=False)

st.download_button(

    "⬇ Download CSV",

    csv,

    "users.csv",

    "text/csv"

)