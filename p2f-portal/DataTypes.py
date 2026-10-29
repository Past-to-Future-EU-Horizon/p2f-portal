from p2f_client.p2f_client import P2F_Client
from p2f_pydantic.harm_data_types import HARM_Data_Type
from portallogs import logger
from assets import disclosure_text
import streamlit as st
from dotenv import load_dotenv
import os
from inspect import stack
from datetime import datetime

logger.debug("PAGE ACCESS: DataTypes.py")

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
st.title("Explore Data Types")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

def get_datatypes(active_datatypes: bool=True):
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        email=P2F_PORTAL_EMAIL_ADDRESS, 
                        token=P2F_PORTAL_TOKEN)
    datatypes = client.harm_data_type.list_data_types(active_datatypes=active_datatypes)
    return datatypes


active_datatypes_toggle = st.toggle("Show only datatypes with data", 
                             value=True, key="active_datatypes_toggle_key")

datatypes = get_datatypes(active_datatypes=st.session_state["active_datatypes_toggle_key"])

# Categorize the datatypes
unique_datatype_measures = {x.measure for x in datatypes}
categorized_datatype_measures = {x: [] for x in unique_datatype_measures}
for datatype in datatypes:
    categorized_datatype_measures[datatype.measure].append(datatype)

measures_columns = {}

for measure_category in unique_datatype_measures:
    st.subheader(measure_category)
    measures_columns[f"{measure_category}_l"], measures_columns[f"{measure_category}_r"] = st.columns(2)
    for datatype in categorized_datatype_measures[measure_category]:
        if categorized_datatype_measures[measure_category].index(datatype) in list(range(0, len(datatypes), 2)):
            current_column = measures_columns[f"{measure_category}_l"]
        else:
            current_column = measures_columns[f"{measure_category}_r"]
        with current_column.container(border=True):
            st.markdown(f"Units: {datatype.unit_of_measurement}  \nMethod: {datatype.method}  \nCalibration: {datatype.calibration}  \ndatatype_id: `{datatype.datatype_id}`")
            st.link_button("Inspect Data Type", 
                           url=f"/datatype-detail?datatype_id={datatype.datatype_id}")