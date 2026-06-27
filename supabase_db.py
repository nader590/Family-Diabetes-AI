import streamlit as st

st.write("URL:", st.secrets["SUPABASE_URL"])
st.write("KEY LENGTH:", len(st.secrets["SUPABASE_KEY"]))
st.stop()