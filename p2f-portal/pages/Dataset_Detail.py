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

def get_dataset(dataset_id):
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    dataset = client.datasets.get_remote_dataset(dataset_id)
    return dataset

def get_subdatasets(doi):
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    subdatasets = client.datasets.list_remote_datasets(is_sub_dataset=True, doi=doi)
    return subdatasets

def get_dataset_datatypes(dataset_id):
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    datatypes = client.harm_data_type.list_data_types(dataset_id=dataset_id)
    return datatypes

def get_graphable_data(dataset_id, datatype, flatten=True):
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    graphable_data = client.harm_numerical.list_harm_numericals(dataset_id=dataset_id, 
                                                                data_type=datatype)
    if flatten:
        return_data = []
        if graphable_data.data_harmonized_int is not None:
            return_data += graphable_data.data_harmonized_int
        if graphable_data.data_harmonized_int_confidence is not None:
            return_data += graphable_data.data_harmonized_int_confidence
        if graphable_data.data_harmonized_float is not None:
            return_data += graphable_data.data_harmonized_float
        if graphable_data.data_harmonized_float_confidence is not None:
            return_data += graphable_data.data_harmonized_float_confidence
        return return_data
    else:
        return graphable_data
    
def get_location_data(dataset_id):
    client = P2F_Client(hostname="localhost", port=8000, https=False)
    locations = client.harm_location.list_harm_locations(dataset_id=dataset_id)
    return locations

def generic_scatter(graphable_data):
    pd.DataFrame()

if "dataset_id" in st.query_params.keys():
    dataset_id = st.query_params["dataset_id"]
    dataset_data = get_dataset(dataset_id=dataset_id)
    st.write(dataset_data)
    st.header(dataset_data.title)
    mcol_1, mcol_2, mcol_3, mcol_4, mcol_5 = st.columns(5) # metadata columns
    mcol_1.text(f"Publication Date: {dataset_data.publication_date}")
    if not dataset_data.is_new_p2f:
        mcol_2.image(load_SVG("P2F_DataReUse.svg"))
    if dataset_data.is_new_p2f:
        mcol_2.image(load_SVG("P2F_NewData.svg"))
    st.link_button("View Dataset's Home Repository", url=f"https://doi.org/{dataset_data.doi}")
    st.subheader("Subdatasets")
    subdatasets = get_subdatasets(doi=dataset_data.doi)
    subdatasets = {str(x.dataset_identifier): get_dataset(x.dataset_identifier) for x in subdatasets}
    st.write(subdatasets)
    st.pills("Subdatasets:", options=[x.title for x in list(subdatasets.values())])
    all_dataset_uuids = [dataset_id]
    all_dataset_uuids += [x for x in list(subdatasets.keys())]
    st.write(all_dataset_uuids)
    st.header("Data Explorer")
    datatypes = get_dataset_datatypes(dataset_id=dataset_id)
    measures = list({x.measure for x in datatypes})
    selected_measure = st.pills("Data Types:", options=measures, default=measures[0])
    sub_measures = [x.method for x in datatypes if x.measure == selected_measure]
    # st.write(sub_measures)
    selected_sub_data_type = st.pills("Sub Data Types:", options=sub_measures, default=sub_measures[0])
    selected_data_type_obj = [x for x in datatypes if x.measure == selected_measure and x.method == selected_sub_data_type][0]
    st.write(selected_data_type_obj)
    selected_data = get_graphable_data(dataset_id=all_dataset_uuids[-1], datatype=selected_data_type_obj.datatype_id)
    # st.write(selected_data)
    graphable_data = pd.DataFrame([x.model_dump(exclude_unset=True) for x in selected_data])
    st.dataframe(graphable_data)
    violin = px.violin(graphable_data, 
                       x="value",
                       title=f"Data Preview: {selected_measure}",
                       subtitle=selected_sub_data_type,
                       labels={"value": selected_data_type_obj.unit_of_measurement})
    st.plotly_chart(violin)
    dataset_locations = []
    for dataset_locs in all_dataset_uuids:
        bdata = get_location_data(dataset_locs)
        bdata = [x for x in bdata if str(x.location_identifier) not in [str(y.location_identifier) for y in dataset_locations]]
        dataset_locations += bdata
    dataset_locations = [x.model_dump(exclude_unset=True) for x in dataset_locations]
    dataset_locations = pd.DataFrame(dataset_locations)
    # st.dataframe(dataset_locations)
    dataset_map = folium.Map(location=[dataset_locations.latitude.mean(), 
                                       dataset_locations.longitude.mean()],
                                       zoom_start=3, 
                                       width=800)
    for ix, rec in dataset_locations.iterrows():
        # st.write(rec)
        folium.Marker(location=[rec.latitude, rec.longitude]).add_to(dataset_map)
    st_folium(dataset_map, width="wide")
    
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