import streamlit as st

st.set_page_config(page_title="Privacy Policy",
                   layout="wide")

st.title("Privacy Policy")

with open("p2f-portal/assets/Privacy_Policy.md", "r") as pp:
    PP = pp.read()

st.markdown(PP)