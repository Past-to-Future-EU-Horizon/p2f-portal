from assets import disclosure_text
import streamlit as st
import folium
from streamlit_folium import st_folium

st.logo("./assets/P2F_text_transparent_MR.png")
st.image("./assets/P2F_text_transparent_MR.png")
st.title("Explore Dataset in Detail")

st.sidebar.image("./assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

query_params = st.query_params

if "dataset_id" in query_params:
    dataset_id = query_params["dataset_id"]