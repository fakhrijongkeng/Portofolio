import streamlit as st

# Initialize session state variable
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Projects"):
    st.session_state.page = "Projects"
if st.sidebar.button("Contact"):
    st.session_state.page = "Contact"

# Page rendering logic
if st.session_state.page == "Home":
    st.title("Welcome to my portfolio!")
    st.write("This is the home page.")
elif st.session_state.page == "Projects":
    st.title("My Projects")
    st.write("Here are some of my Python/Data Science projects.")
elif st.session_state.page == "Contact":
    st.title("Contact Me")
    st.write("Email: you@example.com")
