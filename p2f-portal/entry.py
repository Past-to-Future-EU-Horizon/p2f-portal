import streamlit as st

HomePage = st.Page("Past_2_Future_Portal.py", title="Past 2 Future Portal", url_path=None)
# Datasets
SourceDatasets = st.Page("pages/01_Source_Datasets.py", title="Source Datasets", url_path="/source-datasets")
NewDatasets = st.Page("pages/02_New_Datasets.py", title="New Datasets", url_path="/p2f-datasets")
AddDataset = st.Page("new_Add_Dataset.py", title="Add a Dataset", url_path="/add-dataset")
# Legal
PrivacyPolicy = st.Page("Privacy_Policy.py", title="Privacy Policy", url_path="/privacy-policy")
# Hidden nav
DatasetDetail = st.Page("Dataset_Detail.py", title="Dataset Details", url_path="/dataset-detail", visibility="hidden")
LoginPage = st.Page("login.py", title="P2F Login", url_path="/login", visibility="hidden")


nav = st.navigation({"Home": [HomePage],
                     "Datasets": [SourceDatasets, NewDatasets, AddDataset, DatasetDetail], 
                     "Other": [PrivacyPolicy, LoginPage]})
nav.run()
