from assets import disclosure_text
import streamlit as st

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Publications from the Project")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)
