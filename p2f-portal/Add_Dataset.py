from p2f_client.p2f_client import P2F_Client
from p2f_pydantic.datasets import Datasets
import streamlit as st
import requests
from furl import furl
from datetime import datetime
# import json
import pathlib

if "parent_id" in st.query_params.keys():
    temp_client = P2F_Client(hostname="localhost", port=8000, https=False)
    st.session_state["parent_info"] = temp_client.datasets.get_remote_dataset(dataset_id=st.query_params["parent_id"])
    del temp_client
if "dataset_id" in st.query_params.keys():
    if st.query_params["dataset_id"] == "new":
        dmode = "New"
    else: 
        dmode = "Edit"
        temp_client = P2F_Client(hostname="localhost", port=8000, https=False)
        st.session_state["existing_data"] = temp_client.datasets.get_remote_dataset(dataset_id=st.query_params["dataset_id"])

st.set_page_config(page_title=f"{dmode} dataset",
                   page_icon="➕",
                   layout="wide")

st.title("Insert a new Dataset")

parent_folder = pathlib.Path("")
badges_folder = list(parent_folder.rglob("badges"))[0]

def date2datetime(date):
    match len(date):
        case 4:
            return datetime.strptime(date, "%Y")
        case 10:
            return datetime.strptime(date, "%Y-%m-%d")
        
def load_SVG(svg_name):
    svg_path = badges_folder / svg_name
    with open(svg_path, "r") as f:
        return f.read()

def get_url_form_data():
    url_form_url = st.session_state["url_form_url"]
    url_form_furl = furl(url_form_url)
    intermediate_dataset_title = None
    intermediate_dataset_publication_date = None
    if url_form_furl.host == "doi.org":
        request_furl = furl("https://api.datacite.org/dois")
        request_furl = request_furl / url_form_furl.path.segments[-2] / url_form_furl.path.segments[-1]
        intermediate_request = requests.get(request_furl)
        if intermediate_request.ok:
            intermediate_json = intermediate_request.json()
            try:
                intermediate_dataset_title = intermediate_json["data"]["attributes"]["titles"][0]["title"]
            except:
                pass
            try:
                intermediate_dates = {x["dateType"]:date2datetime(x["date"]) for x in intermediate_json["data"]["attributes"]["dates"]}
                # st.write(intermediate_dates)
                intermediate_dataset_publication_date = intermediate_dates["Created"]
            except Exception as e:
                # st.error(e)
                pass
    st.session_state["intermediate_title"] = intermediate_dataset_title
    st.session_state["intermediate_pub_date"] = intermediate_dataset_publication_date

def submit_new_dataset():
    stss = st.session_state
    new_dataset = Datasets(doi=stss["url_form_url"],
                           title=stss["main_form_dataset_title"],
                           publication_date=stss["main_form_publication_date"],
                           is_sub_dataset=False,
                           is_new_p2f=stss["main_form_original_p2f"])
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    client.datasets.upload_dataset(new_dataset)
    
def add_sub_dataset():
    st.session_state["subdataset_list"].append(st.session_state[f"main_form_subdataset_{st.session_state['subdataset_counter']:03}"])
    

with st.form(key="url_form"):
    st.write("🥬 Let us begin")
    st.text_input("What is the dataset URL?", 
                  key="url_form_url")
    st.form_submit_button("Submit", on_click=get_url_form_data)

# st.code(st.session_state)

if st.session_state["FormSubmitter:url_form-Submit"]:
    with st.form(key="secondary_form"):
        st.write("Going further...")
        st.text_input("Dataset title:", 
                      value=st.session_state["intermediate_title"],
                      key="main_form_dataset_title")
        st.date_input("Dataset publication date: ", 
                      value=st.session_state["intermediate_pub_date"],
                      key="main_form_publication_date")
        with st.container():
            st.write("Please select the ages/epochs/time slices contained within the dataset")
            era_col_1, era_col_2, era_col_3, era_col_4 = st.columns(4)
            era_col_1.image(load_SVG("Epoch-Holocene.svg"))
            era_col_1.checkbox("Holocene", key="main_form_holocene")
            era_col_2.image(load_SVG("Epoch-Pleistocene.svg"))
            era_col_2.checkbox("Pleistocene",  key="main_form_pleistocene")
            era_col_3.image(load_SVG("Epoch-Pliocene.svg"))
            era_col_3.checkbox("Pliocene",  key="main_form_pliocene")
            era_col_4.image(load_SVG("Epoch-Miocene.svg"))
            era_col_4.checkbox("Miocene",  key="main_form_miocene")
            era_col_1.image(load_SVG("Epoch-Oligocene.svg"))
            era_col_1.checkbox("Oligocene",  key="main_form_oligocene")
            era_col_2.image(load_SVG("Epoch-Eocene.svg"))
            era_col_2.checkbox("Eocene",  key="main_form_eocene")
            era_col_3.image(load_SVG("Epoch-Paleocene.svg"))
            era_col_3.checkbox("Paleocene",  key="main_form_paleocene")
        # Is this a P2F original dataset? 
        st.pills("Was this dataset created by the P2F project?", 
                options=["Yes", "No"], 
                key="main_form_original_p2f")
        # Does this dataset have sub-datasets?
        subdatasets = st.pills("Is this dataset a sub dataset?",
                key="main_form_subdatasets",
                options=["Yes", "No"])
        st.form_submit_button("Add dataset")

st.write(st.session_state)

