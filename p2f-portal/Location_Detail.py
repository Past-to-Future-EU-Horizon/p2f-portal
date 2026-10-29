from p2f_client.p2f_client import P2F_Client
from portallogs import logger
from shared import graph_colors
from assets import disclosure_text
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
import json
import pathlib
import os
from inspect import stack
from datetime import datetime

logger.debug("PAGE ACCESS: Location_Detail.py")

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

logger.debug(f"API Path from variables (True=https, False=http): {P2F_API_HTTPS}://{P2F_API_HOSTNAME}:{P2F_API_PORT}/")

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png", size="large")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Location in Detail")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

def get_location(location_id):
    logger.debug(f"{stack()[0][3]}({location_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    location_data = client.harm_location.get_harm_location(location_id=location_id)
    return location_data

def get_related_datasets(location_id, parents_only: bool=True):
    ## parents only is to get only the parent datasets
    logger.debug(f"{stack()[0][3]}({location_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    datasets = client.datasets.list_remote_datasets(location_id=location_id)
    if parents_only:
        parents = []
        for dataset in {x.doi for x in datasets}: # using a set to get only unique DOI values
            parents.append(client.datasets.list_remote_datasets(doi=dataset, is_sub_dataset=False)[0])
        return parents
    else:
        return datasets

def get_related_datatypes(location_id):
    logger.debug(f"{stack()[0][3]}({location_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    datatypes = client.harm_data_type.list_data_types(location_id=location_id)
    return datatypes

if "location_id" in st.query_params.keys():
    location_id = st.query_params["location_id"]
    location_data = get_location(location_id=location_id)
    st.header(location_data.location_name)
    st.markdown(f"Code: {location_data.location_code}  \nlocation_id: `{location_data.location_code}`")


    st.subheader("Related Datasets")
    related_datasets = get_related_datasets(location_id=location_id, parents_only=True)
    for dataset in related_datasets:
        with st.container(border=True):
            st.subheader(dataset.title)
            st.link_button("Go to dataset", 
                           url=f"/dataset-detail?dataset_id={dataset.dataset_id}")

    st.subheader("Related Data Types")
    related_datatypes = get_related_datatypes(location_id=location_id)
    for datatype in related_datatypes:
        with st.container(border=True):
            st.markdown(f"{datatype.measure} ({datatype.unit_of_measurement})  \nMethod: {datatype.method}  \nCalibration: {datatype.calibration}")
            st.link_button("Go to data type",
                           url=f"/datatype-detail?datatype_id={datatype.datatype_id}")