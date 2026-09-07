from p2f_client.p2f_client import P2F_Client
from portallogs import logger
from p2f_pydantic.temp_accounts import Authorization_Check
from p2f_pydantic.harm_data_types import HARM_Data_Type
from assets import disclosure_text
import streamlit as st
import requests
import pandas as pd
from furl import furl
import os
import pathlib
from typing import Optional, List

P2F_API_HOSTNAME = os.getenv("P2F_API_HOSTNAME")
P2F_API_PORT = int(os.getenv("P2F_API_PORT", default="443"))
P2F_API_HTTPS = bool(os.getenv("P2F_API_HTTPS", default="True"))
P2F_PORTAL_EMAIL_ADDRESS = os.getenv("P2F_PORTAL_EMAIL_ADDRESS")
P2F_PORTAL_TOKEN = os.getenv("P2F_PORTAL_TOKEN")

api_https = "https"
if P2F_API_HTTPS == False:
    api_https = "http"
api_port = ""
if api_port != 443:
    api_port = f":{P2F_API_PORT}"

P2F_API_FURL = furl(f"{api_https}://{P2F_API_HOSTNAME}{api_port}")

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png", size="large")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Dataset in Detail")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

st.warning(body="This page is not yet fully functional, please send your thoughts on" \
                "layout and functionality to the developer with the date that you used the page")

def yesno_2_bool(yesno):
    result = False
    if yesno.upper == "YES":
        result = True
    return result

def healthcheck_request():
    healthcheck_url = P2F_API_FURL / "health-check"
    r = requests.get(healthcheck_url)
    return r.ok

def session_state_credential_check():
    r = False
    if "auth_email" in st.session_state and "auth_token" in st.session_state:
        r = True
    return r

def credential_check(email, token):
    st.session_state["auth_email"] = email
    st.session_state["auth_token"] = token
    if healthcheck_request:
        upload_request_url = P2F_API_FURL / "token" / "data-upload-check"
        headers = {"x-p2f-token": token, 
                   "x-p2f-email": email}
        r = requests.post(upload_request_url, 
                          headers=headers)
        if r.ok:
            is_authorized = Authorization_Check(r.json()).authorized
            if is_authorized:
                st.session_state["data_upload_authorization"] = is_authorized

def dataset_exists_check(dataset_id):
    client = P2F_Client(hostname=P2F_API_HOSTNAME,
                        port=P2F_API_PORT,
                        https=P2F_API_HTTPS,
                        email=P2F_PORTAL_EMAIL_ADDRESS,
                        token=P2F_PORTAL_TOKEN)
    try:
        dataset_check = client.datasets.get_remote_dataset(dataset_id=dataset_id)
        return True
    except Exception: # TODO fix this exception handler
        return False

def get_data_types(measure_request: Optional[str] = None) -> List[str] | HARM_Data_Type:
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    api_data_types = client.harm_data_type.list_data_types()
    if measure_request is not None:
        return [x for x in api_data_types if x.measure == measure_request][0]
    else:
        measures = list(set([x.measure for x in api_data_types]))
        if len(measures) > 0:
            return measures
        else:
            return ["No data types found on API"]

if "dataset_id" in st.query_params:
    # check if dataset_id exists on API
    continuity = True
    if not dataset_exists_check(st.query_params["dataset_id"]):
        continuity = False
        st.error(body="The dataset ID used for this page cannot be found",
                 icon="⚠️")
    # check user credentials for uploading data
    if continuity:
        if session_state_credential_check():
            if not credential_check(email=st.session_state["auth_email"],
                                    token=st.session_state["auth_token"]):
                continuity = False
                st.error(body="The provided credentials are unauthorized for data upload. ",
                         icon="⛔")
        else:
            credential_form = st.form(key="add-credentials-upload-data-py")
            auth_col1, auth_col2 = credential_form.columns([2, 1], 
                                           vertical_alignment="center",
                                           )
            auth_email = auth_col1.text_input(label="P2F Authorized Email Address")
            auth_token = auth_col1.text_input(label="Your current P2F Token")
            # auth_col2.space(size="large")
            auth_col2.page_link(label="Don't have a token? Request one here ➡️",
                                page="new_Add_Dataset.py",)
            credential_form.form_submit_button("Submit", 
                                               on_click=credential_check, 
                                               kwargs={"email": auth_email, "token": auth_token}, )

if "data_upload_authorization" in st.session_state:
    if st.session_state["data_upload_authorization"]:
        data_upload_box = st.file_uploader(label="Upload a data file here",
                                           accept_multiple_files=False,
                                           max_upload_size=50_000_000,
                                           type=["xlsx", "csv", "tsv", "xls", "odt"])
        if data_upload_box: 
            match data_upload_box.type:
                # ft used below means file type
                case ft if ft in ["xlsx", "xls", "odt"]:
                    # Excel or Open Document Foundation
                    df = pd.read_excel(data_upload_box.read(), 
                                       sheet_name=None # Important, returns each sheet as a separate DF in a dictionary. 
                                       )
                    sheet_selection = st.pills("Choose a sheet from your Excel: ", 
                                               options=list(df.keys()),
                                               selection_mode="single", 
                                               default=list(df.keys())[0],
                                               required=True)
                case ft if ft in ["csv", "tsv"]:
                    df = pd.read_csv(data_upload_box.read())
            st.dataframe(df)
            for column in df.columns:
                col_type_options = [
                                    "Record ID or index", # used for record hash
                                    "Numerical data", # numerical data that needs a data type
                                    "Record Metadata", # Location, season, timeslice, time/age, 
                                    "Reference Data", # literature or dataset
                                    "Other/Ignore",
                                    ]
                
                col_type = st.pills("What type of column is this?",
                                    options= col_type_options,
                                    key=f"{column}_col_type")
                match col_type:
                    case "Record ID or index":
                        pass
                    case "Numerical data":
                        col_numerical_is_proxy = st.pills("Is this a proxy?",
                                                          options=["Yes", "No"],
                                                          default="Yes", 
                                                          required=True, 
                                                          selection_mode="single")
                        col_numerical_is_proxy_bool = yesno_2_bool(col_numerical_is_proxy)
                        col_numerical_type = st.selectbox("What kind of numerical data is this?")
                    case "Record Metadata":
                        col_metadata_options = [
                                                "Location", 
                                                "Season", 
                                                "Timeslice",
                                                "Age", 
                                                "Age Model", 
                                                "Length along core",
                                                "Elevation",
                                                "Species"
                                                ]
                        col_metadata = st.pills("What kind of metadata is this?",
                                                options=col_metadata_options)
                    case "Reference Data":
                        pass
                    case "Other/Ignore":
                        pass

else:
    st.error(body="No dataset id was found, please access this page by through a dataset detail page.",
             icon="❓")