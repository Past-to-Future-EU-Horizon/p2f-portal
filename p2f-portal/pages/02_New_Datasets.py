from assets import disclosure_text
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore New Datasets Created by the Project")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

edf = pd.read_excel("./p2f-portal/assets/ExistingDatasets.xlsx")

st.pills("Data Themes", options=["SSTs"])

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
            dataset_column_dict[r][c].text(edf.loc[dfc].Authors)
            dataset_column_dict[r][c].link_button("Open Dataset", url=edf.loc[dfc].DOI)
        dfc += 1
        c += 1
    r += 1
    c = 0
