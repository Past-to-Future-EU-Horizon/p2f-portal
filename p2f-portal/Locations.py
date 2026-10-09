from assets import disclosure_text
from p2f_client.p2f_client import P2F_Client
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import folium
from streamlit_folium import st_folium
import os
from datetime import datetime
from typing import List

de = load_dotenv()

P2F_API_HOSTNAME = os.getenv("P2F_API_HOSTNAME")
P2F_API_PORT = int(os.getenv("P2F_API_PORT", default="443"))
P2F_API_HTTPS = bool(os.getenv("P2F_API_HTTPS", default="True"))
P2F_PORTAL_EMAIL_ADDRESS = os.getenv("P2F_PORTAL_EMAIL_ADDRESS")
P2F_PORTAL_TOKEN = os.getenv("P2F_PORTAL_TOKEN")



st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Source Datasets")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

st.markdown("""On this page you will find datasets that are being re-used by the Past to Future consortium. """)

def get_locations() -> dict:
    client = P2F_Client(hostname=P2F_API_HOSTNAME, email=P2F_PORTAL_EMAIL_ADDRESS, token=P2F_PORTAL_TOKEN)
    locations = client.harm_location.list_harm_locations()
    locations = {x.location_name:[x.latitude, x.longitude, x.elevation, x.location_code] for x in locations}
    return locations

location_map = folium.Map(location=(0, 0), zoom_start=1, max_zoom=15)

for name, loclist in get_locations().items():
    lmark = folium.Marker(
                location=loclist[:2], 
                tooltip=loclist[-1], 
                icon=folium.Icon(color="orange", icon="cog")
                ).add_to(location_map)

st_folium(location_map, width=800)