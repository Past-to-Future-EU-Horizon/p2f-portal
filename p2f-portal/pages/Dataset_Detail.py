from assets import disclosure_text
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json

st.set_page_config(layout="wide")

st.logo("./assets/P2F_text_transparent_MR.png")
st.image("./assets/P2F_text_transparent_MR.png")
st.title("Explore Dataset in Detail")

st.sidebar.image("./assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

query_params = st.query_params

if "dataset_id" in query_params:
    dataset_id = query_params["dataset_id"]
else:
    dataset_id = "example"

if dataset_id == "example":
    with open("./assets/example-new-dataset.json", "r") as f:
        r = f.read()
    example_json = json.loads(r)
    # st.text(example_json)
    st.header(example_json["titles"][0]["title"])
    creators_list = [x['name'] for x in example_json["creators"]]
    st.markdown(f"*{'; '.join(creators_list)}*")
    st.text(example_json['descriptions'][0]['description'])

    ddf = pd.read_excel("./assets/example-new-dataset.xlsx", sheet_name=None)
    sheet_selection = st.pills("Select a data sheet",
                                options=ddf.keys(), 
                                default=list(ddf.keys())[0])
    st.dataframe(ddf[sheet_selection])
    site_map = folium.Map([31.68, -51.156], zoom_start=2)
    site_982 = folium.Marker(location=[57.517, -15.867], popup="ODP Site 982").add_to(site_map)
    site_1241 = folium.Marker([5.843, -86.445], popup="ODP Site 1241").add_to(site_map)
    st_folium(site_map, width=725)