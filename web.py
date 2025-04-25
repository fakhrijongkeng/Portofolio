import streamlit as st

# Set up the navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Projects", "Contact"])

# Show the selected page
if page == "Home":
    st.title("Welcome to my portfolio!")
    st.write("This is the home page.")
elif page == "Projects":
    st.title("My Projects")
    st.write("Here are some of my Python/Data Science projects.")
elif page == "Contact":
    st.title("Contact Me")
    st.write("Email: you@example.com")
