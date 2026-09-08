from portallogs import logger
import streamlit as st

st.set_page_config(page_title="Privacy Policy",
                   layout="wide")

logger.info("PAGE ACCESS: Privacy_Policy.py")

st.title("Privacy Policy")

with open("p2f-portal/assets/Privacy_Policy.md", "r") as pp:
    PP = pp.read()

st.markdown(PP)