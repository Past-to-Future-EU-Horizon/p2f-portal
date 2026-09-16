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
from io import BytesIO
from typing import Optional, List
from random import choice as rchoice

logger.info("PAGE ACCESS: upload_data.py")

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

def session_state_credentials_exist():
    r = False
    if "auth_email" in st.session_state and "auth_token" in st.session_state:
        r = True
    return r

def credential_check(email, token):
    logger.debug(f"Function credential_check() received email={email}, {'*'*len(token)}")
    logger.debug(f"Just received credential form input, session state: \n{st.session_state}")
    if "auth_email" not in st.session_state and email is not None:
        logger.debug("credential_check() auth email not in session state and email var was not none")
        st.session_state["auth_email"] = email
    if "auth_token" not in st.session_state and token is not None:
        logger.debug("credential_check() auth token not in session state and token var was not none")
        st.session_state["auth_token"] = token
    if healthcheck_request:
        upload_request_url = P2F_API_FURL / "token" / "data-upload-check"
        headers = {"x-p2f-token": token, 
                   "x-p2f-email": email}
        r = requests.post(upload_request_url, 
                          headers=headers)
        if r.ok:
            authorization_result = Authorization_Check(**r.json())
            is_authorized = authorization_result.authorized
            logger.debug(f"User {email} authorization result: {authorization_result.model_dump_json()}")
            st.session_state["data_upload_authorization"] = authorization_result
            logger.debug(f"Credential check request have run, session state: \n{st.session_state}")
            return is_authorized

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
    dataset_id = st.query_params["dataset_id"]
    logger.debug(f"Request made for upload_data page with dataset_id set as {dataset_id}")
    continuity = True
    if not dataset_exists_check(dataset_id=dataset_id):
        logger.error(f"The upload_page for dataset_id {dataset_id} could not be found on the API")
        continuity = False
        st.error(body="The dataset ID used for this page cannot be found",
                 icon="⚠️")
    # check user credentials for uploading data
    if continuity:
        logger.debug(f"dataset_id requirements met, session state: \n{st.session_state}")
        if session_state_credentials_exist():
            logger.debug(f"Credentials for {st.session_state['auth_email']} were found in the session state, running authorization")
            if not credential_check(email=st.session_state["auth_email"],
                                    token=st.session_state["auth_token"]):
                continuity = False
                logger.error(f"The user {st.session_state['auth_email']} attempted to use a token but is marked as unauthorized for uploading data. ")
                logger.debug(f"The session state at the time of the above credential failure: \n{st.session_state}")
                st.error(body="The provided credentials are unauthorized for data upload. ",
                         icon="⛔")
        else:
            credential_form = st.form(key="add-credentials-upload-data-py")
            auth_col1, auth_col2 = credential_form.columns([2, 1], 
                                           vertical_alignment="center",
                                           )
            auth_email = auth_col1.text_input(label="P2F Authorized Email Address", key="auth_email")
            auth_token = auth_col1.text_input(label="Your current P2F Token", key="auth_token")
            # auth_col2.space(size="large")
            auth_col2.page_link(label="Don't have a token? Request one here ➡️",
                                page="new_Add_Dataset.py",)
            credential_form.form_submit_button("Submit", 
                                               on_click=credential_check, 
                                               kwargs={"email": auth_email, "token": auth_token}, )
else:
    logger.debug("The page upload_data was accessed without a dataset_id query parameter. ")
    st.error(body="No dataset id was found, please access this page by through a dataset detail page.",
             icon="❓")

if "data_upload_authorization" in st.session_state:
    logger.debug(f"Authorization passed, letting user upload data now, session state: \n{st.session_state}")
    if st.session_state["data_upload_authorization"]:
        data_upload_box = st.file_uploader(label="Upload a data file here",
                                           accept_multiple_files=False,
                                           max_upload_size=50,
                                           type=["xlsx", "csv", "tsv", "xls", "ods", "txt"])
        if data_upload_box: 
            file_bytes = BytesIO(data_upload_box.read())
            logger.debug(f"The user {st.session_state['auth_email']} uploaded a {data_upload_box.type}. ")
            match data_upload_box.type:
                # ft used below means file type
                case ft if ft in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.oasis.opendocument.spreadsheet"]:
                    logger.debug("Following EXCEL family route")
                    # Excel or Open Document Foundation
                    df = pd.read_excel(file_bytes, 
                                       sheet_name=None, # Important, returns each sheet as a separate DF in a dictionary. 
                                       )
                    sheet_selection = st.pills("Choose a sheet from your Excel: ", 
                                               options=list(df.keys()),
                                               selection_mode="single", 
                                               default=list(df.keys())[0],
                                               required=True,
                                               key=f"sheet_selection")
                    if sheet_selection:
                        df = df[sheet_selection]
                case ft if ft in ["text/csv", "text/txt", "text/tsv"]:
                    logger.debug("Following CSV family route")
                    df = pd.read_csv(file_bytes)
            st.dataframe(df)
            for column in df.columns:
                with st.container(border=True,
                                  key=f"container_{column}"):
                    col_type_options = [
                                        "Record ID or index", # used for record hash
                                        "Numerical data", # numerical data that needs a data type
                                        "Record Metadata", # Location, season, timeslice, time/age, 
                                        "Reference Data", # literature or dataset
                                        "Other/Ignore",
                                        ]
                    
                    col_type = st.pills(f"What type of column is {column}?",
                                        options= col_type_options,
                                        key=f"{column}_col_type")
                    placeholder_options = ["Option 1", "Option 2"]
                    match col_type:
                        case "Record ID or index":
                            pass
                        case "Numerical data":
                            col_numerical_is_main = st.pills("Is this a central value or a companion confidence interval value?",
                                                            options=["Central Value", "Confidence or Error value", "Interval of Confidence or Error"], 
                                                            help="Central value is the headline number (24°C), confidence or error value is the value at a confidence interval (21°C), interval of confidence or error is for example 5% or 95%",
                                                            selection_mode="single",
                                                            key=f"numerical_ismain_{column}")
                            if col_numerical_is_main:
                                match col_numerical_is_main:
                                    case "Central Value":
                                        col_numerical_is_proxy = st.pills("Is this a proxy?",
                                                                            options=["Yes", "No"],
                                                                            default="Yes", 
                                                                            required=True, 
                                                                            selection_mode="single",
                                                                            key=f"numerical_isproxy_{column}")
                                        if col_numerical_is_proxy:
                                            col_numerical_is_proxy_bool = yesno_2_bool(col_numerical_is_proxy)
                                            col_numerical_type_measure = st.selectbox("What does this numerical data measure?", 
                                                                                    options=placeholder_options,
                                                                                    key=f"numerical_measure_{column}")
                                            if col_numerical_type_measure:
                                                col_numerical_type_method = st.selectbox("How was this unit measured?", 
                                                                                        options=placeholder_options,
                                                                                        key=f"numerical_method_{column}")
                                                if col_numerical_type_method:
                                                    col_numerical_type_calibration = st.selectbox("How was this measure calibrated?",
                                                                                                options=placeholder_options,
                                                                                                key=f"numerical_calibration_{column}")
                                    case "Confidence or Error Value":
                                        col_numerical_confval_upperorlower = st.pills("Is this an upper or lower confidencevalue?",
                                                                                        options=["Upper", "Lower"],
                                                                                        key=f"numerical_confval_uol_{column}")
                                        col_numerical_confval_companionto = st.selectbox("What column is the central value?",
                                                                                            options=df.columns,
                                                                                            key=f"numerical_confval_companion_{column}")
                                    case "Interval of Confidence or Error":
                                        col_numerical_confint_upperorlower = st.pills("Is this an upper or lower confidence interval?",
                                                                                        options=["Upper", "Lower"],
                                                                                        key=f"numerical_confint_uol_{column}")
                                        col_numerical_confint_companionto = st.selectbox("What column is the confidence value?",
                                                                                        options=df.columns,
                                                                                        key=f"numerical_confint_companion_{column}")
                        case "Record Metadata":
                            col_metadata_options = [
                                                    "Location", 
                                                    "Season", 
                                                    "Age", 
                                                    "Age Model", 
                                                    "Length along core",
                                                    "Species"
                                                    ]
                            col_metadata = st.pills("What kind of metadata is this?",
                                                    options=col_metadata_options, 
                                                    key=f"metadata_type_{column}")
                            if col_metadata:
                                match col_metadata:
                                    case "Location":
                                        col_metadata_location_options = ["Latitude", "Longitude", "Elevation", "Location Age", "WKB", "WKT", "Other"]
                                        col_metadata_location = st.pills(label="What location information is this?",
                                                                        options=col_metadata_location_options, 
                                                                        selection_mode="single",
                                                                        key=f"location_type_{column}")
                                    case "Season":
                                        st.write("Please review the unique seasons found in this column")
                                        season_markdown_list = """"""
                                        for season in list(df[column].unique()):
                                            season_markdown_list += f"* {season}\n"
                                        st.markdown(season_markdown_list)
                                    case "Age":
                                        col_metadata_age_unit_options = ["Years before present",
                                                                        "Thousands of years before present",
                                                                        "Millions of years before present"]
                                        col_metadata_age_unit = st.pills(label="What are the units of this column?",
                                                                        options=col_metadata_age_unit_options,
                                                                        selection_mode="single",
                                                                        key=f"age_unit_{column}")
                                        col_metadata_age_zero = st.pills(label="What is the zero calendar year for this column?",
                                                                        options=["1950", "2000", "Other"],
                                                                        key=f"age_zero_{column}")
                                        if col_metadata_age_zero:
                                            if col_metadata_age_zero == "Other":
                                                zero_year = st.number_input("What is the other zero year?", 
                                                                value=2000,
                                                                step=10,
                                                                key=f"age_otherzero_{column}")
                                            else: 
                                                zero_year = int(col_metadata_age_zero)                                            
                                    case "Age Model":
                                        st.write("Please review the unique Age Models found in this column: ")
                                        age_model_markdown_list = ""
                                        for age_model in list(df[column].unique()):
                                            age_model_markdown_list += f"* {age_model}"
                                        st.markdown(age_model_markdown_list)
                                    case "Length along core":
                                        col_metadata_corelength_options = ["millimeters", "centimeters", "meters"]
                                        col_metadata_corelength_unit = st.pills(label="What are the units for the length along the core?",
                                                                                options=col_metadata_corelength_options,
                                                                                selection_mode="single",
                                                                                key=f"corelength_unit_{column}")
                                    case "Species":
                                        species_emoji = ['😻', '🐵', '🐶', '🐺', '🦁', '🐯', 
                                                        '🦒', '🦊', '🦝', '🐮', '🐷', '🐗', 
                                                        '🐭', '🐹', '🐰', '🐻', '🐨', '🐼', 
                                                        '🐸', '🦓', '🐴', '🫎', '🫏', '🦄', 
                                                        '🐔', '🐲', '🐒', '🦍', '🦧', '🐩', 
                                                        '🐕', '🐈', '🐈', '🐅', '🐎', '🦌', 
                                                        '🦬', '🦏', '🦛', '🐂', '🐃', '🐄', 
                                                        '🐖', '🐏', '🐑', '🐐', '🐪', '🐫', 
                                                        '🦙', '🦘', '🦥', '🦨', '🦡', '🐘', 
                                                        '🦣', '🐁', '🐀', '🦔', '🐇', '🐿', 
                                                        '🦫', '🦎', '🐊', '🐢', '🐍', '🐉', 
                                                        '🦕', '🦖', '🦦', '🦈', '🐬', '🦭', 
                                                        '🐳', '🐋', '🐟', '🐠', '🐡', '🦐', 
                                                        '🦑', '🐙', '🦞', '🦀', '🪼', '🦆', 
                                                        '🐓', '🦃', '🦅', '🕊', '🦢', '🦜', 
                                                        '🐦', '🪿', '🦩', '🦚', '🦉', '🦤', 
                                                        '🐥', '🐤', '🐣', '🦇', '🦋', '🐌', 
                                                        '🐛', '🦟', '🪰', '🪱', '🦗', '🐜', 
                                                        '🪳', '🐝', '🪲', '🐞', '🦂', '🕷', 
                                                        '🦠']
                                        st.warning(icon=rchoice(species_emoji),
                                                body="We're still working on implementing the species functionality for the P2F Portal.")
                        case "Reference Data":
                            st.warning(icon="📚",
                                    body="Thank you for indicating the references, this feature is currently not implemented.")
                        case "Other/Ignore":
                            st.warning(icon="⚠️",
                                    body="This feature is not currently implemented, please let the developer know what kind of data you need to add")

