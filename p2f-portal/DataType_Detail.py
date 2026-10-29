from p2f_client.p2f_client import P2F_Client
from p2f_pydantic.harm_data_types import HARM_Data_Type
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

logger.debug("PAGE ACCESS: DataType_Detail.py")

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
st.title("Explore Datatype in Detail")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

def get_datatype(datatype_id): 
    logger.debug(f"{stack()[0][3]}({datatype_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    datatype_data = client.harm_data_type.get_data_type(datatype_id=datatype_id)
    return datatype_data

def get_datatype_statistics(datatype_id):
    logger.debug(f"{stack()[0][3]}({datatype_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    datatype_data = client.harm_numerical.get_numeric_statistics(datatype_id=datatype_id)
    return datatype_data

def get_graphable_data(datatype_id, flatten=True) -> pd.DataFrame | None:
    logger.debug(f"{stack()[0][3]}()")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    statistics = client.harm_numerical.get_numeric_statistics(datatype_id=datatype_id)
    logger.debug(f"Statistics: {statistics}")
    df = None
    if statistics.count_total > 0:
        if statistics.count_float_confidence > 0:
            df = client.harm_numerical.list_harm_numericals(numeric_type="float_confidence", datatype_id=datatype_id, request_as="pandas")["float_confidence"]
        # logger.debug(f"float_confidence dataframe status: {repr(df)}")
        if statistics.count_float > 0:
            request_new_df = client.harm_numerical.list_harm_numericals(numeric_type="float", datatype_id=datatype_id, request_as="pandas")["float"]
            # logger.debug(repr(request_new_df))
            if type(df) == type(None):
                df = request_new_df
            else:
                df = pd.concat([df, request_new_df])
        # logger.debug(f"float dataframe status: {repr(df)}")
        if statistics.count_int_confidence > 0:
            request_new_df = client.harm_numerical.list_harm_numericals(numeric_type="int_confidence", datatype_id=datatype_id, request_as="pandas")["int_confidence"]
            # logger.debug(repr(request_new_df))
            if type(df) == type(None):
                df = request_new_df
            else:
                df = pd.concat([df, request_new_df])
        # logger.debug(f"int_confidence dataframe status: {repr(df)}")
        if statistics.count_int > 0:
            request_new_df = client.harm_numerical.list_harm_numericals(numeric_type="int", datatype_id=datatype_id, request_as="pandas")["int"]
            # logger.debug(repr(request_new_df))
            if type(df) == type(None):
                df = request_new_df
            else:
                df = pd.concat([df, request_new_df])
        # logger.debug(f"int dataframe status: {repr(df)}")
    return df

def get_location_data(datatype_id):
    logger.debug(f"{stack()[0][3]}({datatype_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    locations = client.harm_location.list_harm_locations(datatype_id=datatype_id)
    return locations

def get_related_datasets(datatype_id):
    logger.debug(f"{stack()[0][3]}({datatype_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    datasets = client.datasets.list_remote_datasets()

if "datatype_id" in st.query_params.keys():
    datatype_id = st.query_params["datatype_id"]
    datatype_data = get_datatype(datatype_id=datatype_id)
    datatype_statistics = get_datatype_statistics(datatype_id=datatype_id)
    st.header(datatype_data.measure)
    dataset_metadata_L, dataset_metadata_R = st.columns([2,1])
    dataset_metadata_L.subheader(f"Method: {datatype_data.method}")
    dataset_metadata_L.subheader(f"Calibration: {datatype_data.calibration}")
    dataset_metadata_L.text(f"Units: {datatype_data.unit_of_measurement}")
    dataset_metadata_R.metric("Total Records of this data type",
                              value=datatype_statistics.count_total)
    with dataset_metadata_R.container(border=True):
        st.text("datatype_id")
        st.code(f"{datatype_data.datatype_id}")

    graphable_data = get_graphable_data(datatype_id=datatype_id)

    graph_mode_options = ["Violin Plot", "Box Plot", "Histogram"]
    graph_mode = st.pills("How would you like to preview the graph of the data?",
                            options=graph_mode_options,
                            default=graph_mode_options[0],
                            required=True)

    graph_height = 475
    
    violin = px.violin(
        graphable_data,
        x="value",
        title=f"Data Preview",
        # color="Data Type",
        # color_discrete_sequence=graph_colors,
        height=graph_height,
        # subtitle=selected_measure_method,
        # labels={"value": selected_data_type_obj.unit_of_measurement},
    )
    boxplot = px.box(
        graphable_data,
        x="value",
        title=f"Data Preview",
        # color="Data Type", 
        # color_discrete_sequence=graph_colors,
        height=graph_height,
        # subtitle=selected_measure_method,
        # labels={"value": selected_data_type_obj.unit_of_measurement},
    )
    histogram = px.histogram(
        graphable_data,
        x="value",
        title=f"Data Preview",
        # color="Data Type",
        # color_discrete_sequence=graph_colors,
        height=graph_height,
        # subtitle=selected_measure_method,
        # labels={"value": selected_data_type_obj.unit_of_measurement},
    )

    graph_display = {"Violin Plot": violin, "Box Plot": boxplot, "Histogram": histogram,}
    st.plotly_chart(graph_display[graph_mode], 
                    height=graph_height,)