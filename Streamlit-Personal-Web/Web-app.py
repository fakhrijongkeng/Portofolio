import streamlit as st

col1, col2 = st.columns([1, 3])
 
st.title("FAKHRI AKMAL")

with col1:
    st.image("Streamlit-Personal-Web/images/photo-profile.png"
with col2:
    st.write("This is my personal web app")

st.page_link("Web-app.py", label="Home")
st.page_link("pages/portofolio.py", label="Page 1", icon="1️⃣")
