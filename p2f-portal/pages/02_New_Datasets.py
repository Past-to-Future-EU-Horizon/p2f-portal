from p2f_client.p2f_client import P2F_Client
from assets import disclosure_text
import streamlit as st
import pandas as pd
import pathlib

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore New Datasets Created by the Project")


parent_folder = pathlib.Path("")
add_dataset_path = list(parent_folder.rglob("Add_Dataset.py"))[0]
st.link_button(label="Add Dataset", url=f"http://localhost:8082/Add_Dataset?dataset_id=new")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

def get_datasets():
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    datasets = client.datasets.list_remote_datasets(is_new_p2f=True)
    # datasets = [x.model_dump_json(exclude_unset=True) for x in datasets]
    dataset_df = pd.DataFrame(columns=["Title", "UUID", "P2F_Original", "Subdataset"])
    c = 0
    for dataset in datasets:
        # st.write(dataset)
        dataset_df.loc[c] = (dataset.title, dataset.dataset_identifier, dataset.is_new_p2f, dataset.is_sub_dataset)
        c += 1
    return dataset_df

st.pills("Data Themes", options=["SSTs"])

edf = get_datasets()

COLUMNS = 2

dataset_column_dict = {}
dfc = 0
r = 0
c = 0 
for row in range(len(edf)%COLUMNS+1):
    dataset_column_dict[r] = st.columns(COLUMNS)
    for col in range(COLUMNS):
        if dfc in edf.index:
            dataset_column_dict[r][c].subheader(edf.loc[dfc].Title)
            # dataset_column_dict[r][c].text(edf.loc[dfc].Authors)
            dataset_column_dict[r][c].link_button("Open Dataset", url=f"http://localhost:8082/Dataset_Detail?dataset_id={edf.loc[dfc].UUID}")
        dfc += 1
        c += 1
    r += 1
    c = 0
