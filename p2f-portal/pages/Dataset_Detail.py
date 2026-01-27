from p2f_client.p2f_client import P2F_Client
from assets import disclosure_text
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd
import json
import pathlib

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png", size="large")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Dataset in Detail")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)


parent_folder = pathlib.Path("")
badges_folder = list(parent_folder.rglob("badges"))[0]

def load_SVG(svg_name):
    svg_path = badges_folder / svg_name
    with open(svg_path, "r") as f:
        return f.read()

def get_datasets(dataset_id):
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    dataset = client.datasets.get_remote_dataset(dataset_id)
    return dataset


if "dataset_id" in st.query_params.keys():
    dataset_id = st.query_params["dataset_id"]
    dataset_data = get_datasets(dataset_id=dataset_id)
    st.write(dataset_data)
    st.header(dataset_data.title)
    mcol_1, mcol_2, mcol_3, mcol_4, mcol_5 = st.columns(5) # metadata columns
    mcol_1.text(f"Publication Date: {dataset_data.publication_date}")
    if not dataset_data.is_new_p2f:
        mcol_2.image(load_SVG("P2F_DataReUse.svg"))
    if dataset_data.is_new_p2f:
        mcol_2.image(load_SVG("P2F_NewData.svg"))
    st.link_button("View Dataset's Home Repository", url=f"https://doi.org/{dataset_data.doi}")
else:
    dataset_id = "example"

if dataset_id == "example":
    with open("./p2f-portal/assets/example-new-dataset.json", "r") as f:
        r = f.read()
    example_json = json.loads(r)
    # st.text(example_json)
    st.header(example_json["titles"][0]["title"])
    creators_list = [x['name'] for x in example_json["creators"]]
    st.markdown(f"*{'; '.join(creators_list)}*")
    st.text(example_json['descriptions'][0]['description'])

    ddf = pd.read_excel("./p2f-portal/assets/example-new-dataset.xlsx", sheet_name=None)
    sheet_selection = st.pills("Select a data sheet",
                                options=ddf.keys(), 
                                default=list(ddf.keys())[0])
    st.dataframe(ddf[sheet_selection])
    column_selection = st.pills("Select a column to plot", 
                                [x for x in ddf[sheet_selection].columns])
    
    if column_selection: 
        plot = px.scatter(ddf[sheet_selection][column_selection])
        st.plotly_chart(plot)

    site_map = folium.Map([31.68, -51.156], zoom_start=2)
    site_982 = folium.Marker(location=[57.517, -15.867], popup="ODP Site 982").add_to(site_map)
    site_1241 = folium.Marker([5.843, -86.445], popup="ODP Site 1241").add_to(site_map)
    st_folium(site_map, width=725)