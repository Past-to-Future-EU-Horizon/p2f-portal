import streamlit as st

HomePage = st.Page("Past_2_Future_Portal.py", title="Past 2 Future Portal", url_path=None)
SourceDatasets = st.Page("pages/01_Source_Datasets.py", title="Source Datasets", url_path="/source-datasets")
NewDatasets = st.Page("pages/02_New_Datasets.py", title="New Datasets", url_path="/new-datasets")
DatasetDetail = st.Page("Dataset_Detail.py", title="Dataset Details", url_path="/dataset-detail", visibility="hidden")

nav = st.navigation({"Home": [HomePage],
               "Datasets": [SourceDatasets, NewDatasets]})
nav.run()
