from assets import disclosure_text
from p2f_client.p2f_client import P2F_Client
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Source Datasets")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)


def get_datasets():
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    datasets = client.datasets.list_remote_datasets(
        is_new_p2f=False, is_sub_dataset=False
    )
    # datasets = [x.model_dump_json(exclude_unset=True) for x in datasets]
    dataset_df = pd.DataFrame(columns=["Title", "UUID", "P2F_Original", "Subdataset"])
    c = 0
    for dataset in datasets:
        st.write(dataset)
        dataset_df.loc[c] = (
            dataset.title,
            dataset.dataset_identifier,
            dataset.is_new_p2f,
            dataset.is_sub_dataset,
        )
        c += 1
    return dataset_df


st.pills("Data Themes", options=["SSTs"])

edf = get_datasets()

COLUMNS = 2

dataset_column_dict = {}
dfc = 0
r = 0
c = 0
for row in range(len(edf) % COLUMNS + 1):
    dataset_column_dict[r] = st.columns(COLUMNS)
    for col in range(COLUMNS):
        if dfc in edf.index:
            dataset_column_dict[r][c].subheader(edf.loc[dfc].Title)
            # dataset_column_dict[r][c].text(edf.loc[dfc].Authors)
            dataset_column_dict[r][c].link_button(
                "Open Dataset",
                url=f"http://localhost:8082/Dataset_Detail?dataset_id={edf.loc[dfc].UUID}",
            )
        dfc += 1
        c += 1
    r += 1
    c = 0
