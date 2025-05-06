import streamlit as st

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("Another cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")


st.title("FAKHRI AKMAL")
st.write("This is my personal web app")

st.page_link("Web-app.py", label="Home")
st.page_link("pages/portofolio.py", label="Page 1", icon="1️⃣")
