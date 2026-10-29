from assets import disclosure_text
from p2f_client.p2f_client import P2F_Client
from p2f_pydantic.harm_location import HARM_Location
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import folium
from streamlit_folium import st_folium
import os
from math import sqrt
from datetime import datetime
from typing import List

de = load_dotenv()

P2F_API_HOSTNAME = os.getenv("P2F_API_HOSTNAME")
P2F_API_PORT = int(os.getenv("P2F_API_PORT", default="443"))
P2F_API_HTTPS_STRING = os.getenv("P2F_API_HTTPS", default="True")
match P2F_API_HTTPS_STRING:
    case "True": 
        P2F_API_HTTPS = True
    case "False":
        P2F_API_HTTPS = False
P2F_PORTAL_EMAIL_ADDRESS = os.getenv("P2F_PORTAL_EMAIL_ADDRESS")
P2F_PORTAL_TOKEN = os.getenv("P2F_PORTAL_TOKEN")



st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Dataset Locations")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

st.markdown("""Locations of data that is being re-used in the Past to Future project. . """)

def get_locations() -> pd.DataFrame:
    client = P2F_Client(hostname=P2F_API_HOSTNAME,
                        port=P2F_API_PORT,
                        https=P2F_API_HTTPS, 
                        email=P2F_PORTAL_EMAIL_ADDRESS, 
                        token=P2F_PORTAL_TOKEN)
    locations = client.harm_location.list_harm_locations(active_locations=True)
    locations = [x.model_dump(exclude_unset=True) for x in locations]
    # locations = {x.location_name: x for x in locations}
    locations = pd.DataFrame(locations)
    return locations

def dist_calc(src_lat, src_lon, tgt_lat, tgt_lon) -> float:
    dst_lat = (src_lat - tgt_lat) ** 2
    dst_lon = (src_lon - tgt_lon) ** 2
    dist = sqrt(dst_lat + dst_lon)
    return dist

locations_data = get_locations()
# st.dataframe(locations_data)

location_map = folium.Map(location=(0, 0), zoom_start=2, max_zoom=15)

for ix, rec in locations_data.iterrows():
    lmark = folium.Marker(
                location=[rec.latitude, rec.longitude], 
                tooltip=rec.location_code, 
                icon=folium.Icon(color="orange", icon="cog"),
                ).add_to(location_map)

st_data = st_folium(location_map, width=800, returned_objects=["last_object_clicked"])
st.text("Click on a marker the map and the list below will update in ascending order of distance to marker.")

if st_data["last_object_clicked"] is not None:
    locations_data["distance-to-click"] = [dist_calc(y, x, st_data["last_object_clicked"]["lat"], st_data["last_object_clicked"]["lng"]) for y, x in zip(locations_data["latitude"], locations_data["longitude"])]
    ordered_locations = locations_data.sort_values("distance-to-click", ignore_index=True)
    for ix, rec in ordered_locations.iterrows():
        with st.container(border=True):
            st.markdown(f"{rec.location_name} ({rec.location_code})")
            st.link_button("Inspect Location",
                           url=f"/location-detail?location_id={rec.location_id}")
else:
    for ix, rec in locations_data.iterrows():
        with st.container(border=True):
            st.markdown(f"{rec.location_name} ({rec.location_code})")
            st.link_button("Inspect Location",
                           url=f"/location-detail?location_id={rec.location_id}")