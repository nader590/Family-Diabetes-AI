import streamlit as st
from supabase import create_client

st.write("URL =", st.secrets["SUPABASE_URL"])
st.write("KEY =", st.secrets["SUPABASE_KEY"][:20])

try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
    st.success("Connected")
except Exception as e:
    st.error(str(e))