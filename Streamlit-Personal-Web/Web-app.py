import streamlit as st

col1, col2 = st.columns([1, 3])
 
st.title("FAKHRI AKMAL")

with col1:
    st.image("https://raw.githubusercontent.com/fakhrijongkeng/Portofolio/main/Streamlit-Personal-Web/images/WhatsApp%20Image%202024-10-07%20at%2019.27.27_6ab775b0.jpg")
    
with col2:
    st.write("This is my personal web app")

st.page_link("Web-app.py", label="Home")
st.page_link("pages/portofolio.py", label="Page 1", icon="1️⃣")
