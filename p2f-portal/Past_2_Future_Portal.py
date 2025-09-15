from assets import disclosure_text
import streamlit as st

st.logo("./assets/P2F_text_transparent_MR.png")
st.image("./assets/P2F_text_transparent_MR.png")
st.title("Welcome to the Past 2 Future Data Portal")

st.sidebar.image("./assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)



welcome_markdown = """
This portal is for the Past 2 Future project, 
grouping together source datasets that will go into our project, 
and the datasets that are produced by the project. 
"""

st.markdown(welcome_markdown)