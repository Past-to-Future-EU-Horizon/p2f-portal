from assets import disclosure_text
import streamlit as st

st.logo("./assets/P2F_text_transparent_MR.png")
st.image("./assets/P2F_text_transparent_MR.png")
st.title("Explore Source Datasets")

st.sidebar.image("./assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)