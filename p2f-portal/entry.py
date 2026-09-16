import streamlit as st

HomePage = st.Page("Past_2_Future_Portal.py", title="Past 2 Future Portal", url_path=None, icon="🏡")
# Datasets
SourceDatasets = st.Page("pages/01_Source_Datasets.py", title="Source Datasets", url_path="/source-datasets", icon="♻️")
NewDatasets = st.Page("pages/02_New_Datasets.py", title="New Datasets", url_path="/p2f-datasets", icon="🆕")
AddDataset = st.Page("new_Add_Dataset.py", title="Add a Dataset", url_path="/add-dataset", icon="➕")
# Legal
PrivacyPolicy = st.Page("Privacy_Policy.py", title="Privacy Policy", url_path="/privacy-policy", icon="🔒")
# Hidden nav
DatasetDetail = st.Page("Dataset_Detail.py", title="Dataset Details", url_path="/dataset-detail", visibility="hidden", icon="🔍")
LoginPage = st.Page("login.py", title="P2F Login", url_path="/login", icon="🪵")
UploadData = st.Page("upload_data.py", title="Upload Data", url_path="/upload-data", visibility="hidden", icon="⬆️")


nav = st.navigation({"Home": [HomePage],
                     "Datasets": [SourceDatasets, NewDatasets, AddDataset, DatasetDetail, UploadData], 
                     "Other": [PrivacyPolicy, LoginPage]})
nav.run()
