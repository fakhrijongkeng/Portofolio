import streamlit as st

tab1, tab2, tab3 = st.tabs(["Home", "Projects", "Contact"])

with tab1:
    st.header("Home")
    st.write("Welcome to my portfolio!")

with tab2:
    st.header("Projects")
    st.write("These are my projects.")

with tab3:
    st.header("Contact")
    st.write("Email: you@example.com")
