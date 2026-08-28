from apilogs import logger
from p2f_client.p2f_client import P2F_Client
import streamlit as st
from assets import disclosure_text
from typing import List
import os

P2F_API_HOSTNAME = os.getenv("P2F_API_HOSTNAME")
P2F_API_PORT = int(os.getenv("P2F_API_PORT", default="443"))
P2F_API_HTTPS = bool(os.getenv("P2F_API_HTTPS", default="True"))
P2F_PORTAL_EMAIL_ADDRESS = os.getenv("P2F_PORTAL_EMAIL_ADDRESS")
P2F_PORTAL_TOKEN = os.getenv("P2F_PORTAL_TOKEN")

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

st.title("Add a new dataset")

st.text("This page is not yet fully implemented. " \
        "Email and token are required to be able to submit a dataset, " \
        "request one before filling in the form")

def yesno_2_bool(yesno):
    result = False
    if yesno.upper == "YES":
        result = True
    return result

def submit_dataset():
    # login with current user authorization
    client = P2F_Client(hostname=P2F_API_HOSTNAME,
                        port=P2F_API_PORT,
                        https=P2F_API_HTTPS,
                        email=auth_email,
                        token=auth_token)
    continuation = True
    try:
        upload_ds_obj = client.datasets.data_model(doi=ds_url, 
                                                   title=ds_title,
                                                   publication_date=ds_publication_date, 
                                                   is_new_p2f=yesno_2_bool(ds_new_p2f),
                                                   is_sub_dataset=False)
        ds_uploaded = client.datasets.upload_dataset(upload_ds_obj)
    except Exception:
        st.error(body="There was an issue uploading the dataset record to the API",
                 icon="⚠️")
        continuation = False # Continuation for when a process fails and we cannot try to do anything else
    # Time coverage upload - client not implemented yet
    if continuation:
        try: 
            upload_timerange = client.harm_ds_timecoverage.data_model(
                dataset_id=ds_uploaded.dataset_id,
                oldest=ds_time_older,
                youngest=ds_time_young,
                reference_zero=ds_time_zero
            )
            client.harm_ds_timecoverage.upload_dataset_timecoverage(upload_timerange)
        except Exception:
            st.warning(body="The time coverage of the dataset failed to upload",
                       icon="⚠️")
    ## Data types
    # if continuation:
    #     try:
    #         upload_dt_obj = client.harm_data_type
    #     except Exception:
    #         pass
    ## Time Slices
    ## Keywords
    ## Seasonailty
    
new_dataset = st.form(key="new-dataset")

ds_url = new_dataset.text_input(label="URL")
# st.button(label="Get metadata from DOI API")

ds_title = new_dataset.text_input(label="Title")

pubcol, newp2fcol = new_dataset.columns(2)

ds_publication_date = pubcol.date_input(label="Publication Date")

ds_new_p2f = newp2fcol.pills(label="Is this a new dataset by the P2F Consortium?", 
                               options=["Yes", "No"], 
                               default="Yes")



tsc0, tsc1, tsc2 = new_dataset.columns(3)
ds_time_older = tsc0.number_input(label="What is the oldest date in this dataset?", 
                                  step=1, 
                                  value=0)
ds_time_young = tsc1.number_input(label="What is the youngest date in this dataset?", 
                                  step=1, 
                                  value=0)
ds_time_zero = tsc2.pills(label="What is the 0 year?", 
                          options=["1950", "2000", "Other"],
                          default="1950",
                          required=True)
if ds_time_zero is not None:
    if ds_time_zero == "Other":
        ds_time_zero_other = tsc2.number_input(label="Other zero year:",
                                               step=1,
                                               value=2000)

def get_data_types() -> List[str]:
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    api_data_types = client.harm_data_type.list_data_types()
    measures = list(set([x.measure for x in api_data_types]))
    if len(measures) > 0:
        return measures
    else:
        return ["No data types found on API"]

def get_timeslices() -> List[str]:
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    api_timeslices =  client.harm_timeslice.list_timeslices()
    timeslices = list(set([x.timeslice_name for x in api_timeslices]))
    if len(timeslices) > 0:
        return timeslices
    else:
        return ["No timeslices found on API"]

############################### BEGIN NOT YET IMPLEMENTED IN CLIENT

# try: 
#     server_data_types = get_data_types()
# except Exception: 
#     server_data_types = None
#     logger.debug("API Error, no data types found")

# try: 
#     server_timeslices = get_timeslices()
# except Exception:
#     server_timeslices = None
#     logger.debug("API Error, no timeslices found")


# # data_theme_selection = st.pills("Data Themes", options=get_data_types())

# if server_data_types is not None:
#     ds_datatypes = new_dataset.pills(label="What P2F Data Types does this contain?",
#                                     options=server_data_types,
#                                     selection_mode="multi")
# else:
#     new_dataset.text("Data types are currently unavailable")
# if server_timeslices is not None:
#     ds_timeslices = new_dataset.pills(label="Which P2F Timeslices does this cover?", 
#                                     options=server_timeslices,
#                                     selection_mode="multi")
# else:
#     new_dataset.text("Timeslices are currently unavailable")
# ds_keywords = new_dataset.text_input(label="Keywords (comma separated)")

# ds_seasonality = new_dataset.pills(label="Does the dataset have seasonality?", 
#                                    options=["No", "Winter/Summer", "Hot/Cold", "Winter/Spring/Summer/Autumn", "Other"], 
#                                    default="No")

################################ END NOT IMPLEMENTED IN CLIENT YET

auth_col1, auth_col2 = new_dataset.columns([2, 1], 
                                           vertical_alignment="center",
                                           )
auth_email = auth_col1.text_input(label="P2F Authorized Email Address")
auth_token = auth_col1.text_input(label="Your current P2F Token")
# auth_col2.space(size="large")
auth_col2.page_link(label="Don't have a token? Request one here ➡️",
                    page="new_Add_Dataset.py",)

submit = new_dataset.form_submit_button("Add dataset",
                                        on_click=submit_dataset)