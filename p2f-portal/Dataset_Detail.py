from p2f_client.p2f_client import P2F_Client
from p2f_pydantic.harm_data_types import HARM_Data_Type
from portallogs import logger
from assets import disclosure_text
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
import json
import pathlib
import os
from inspect import stack
from datetime import datetime

logger.debug("PAGE ACCESS: Dataset_Detail.py")

de = load_dotenv()

P2F_API_HOSTNAME = os.getenv("P2F_API_HOSTNAME")
P2F_API_PORT = int(os.getenv("P2F_API_PORT", default="443"))
P2F_API_HTTPS_STRING = os.getenv("P2F_API_HTTPS", default="True")
match P2F_API_HTTPS_STRING:
    case "True": 
        P2F_API_HTTPS = True
    case "False":
        P2F_API_HTTPS = False
P2F_PORTAL_EMAIL_ADDRESS = os.getenv("P2F_PORTAL_EMAIL_ADDRESS")
P2F_PORTAL_TOKEN = os.getenv("P2F_PORTAL_TOKEN")

logger.debug(f"API Path from variables (True=https, False=http): {P2F_API_HTTPS}://{P2F_API_HOSTNAME}:{P2F_API_PORT}/")

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png", size="large")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Dataset in Detail")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

parent_folder = pathlib.Path("")
badges_folder = list(parent_folder.rglob("badges"))[0]


def load_SVG(svg_name):
    svg_path = badges_folder / svg_name
    with open(svg_path, "r") as f:
        return f.read()


def get_dataset(dataset_id):
    logger.debug(f"{stack()[0][3]}({dataset_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    logger.debug(client.base_url)
    dataset = client.datasets.get_remote_dataset(dataset_id)
    return dataset


def get_subdatasets(doi):
    logger.debug(f"{stack()[0][3]}({doi})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    logger.debug(client.base_url)
    subdatasets = client.datasets.list_remote_datasets(is_sub_dataset=True, doi=doi)
    return subdatasets


def get_dataset_datatypes(dataset_id):
    logger.debug(f"{stack()[0][3]}({dataset_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    logger.debug(client.base_url)
    datatypes = client.harm_data_type.list_data_types(dataset_id=dataset_id)
    return datatypes


def make_df_userfriendly_1(datatype: HARM_Data_Type, df: pd.DataFrame):
    datatype_string = f"{datatype.measure} ({datatype.unit_of_measurement}) - {datatype.method} - {datatype.calibration}"
    df[datatype_string] = df["value"]
    df["Record Hash"] = df["fk_data_record"]
    df["datatype_id"] = [str(x) for x in df["fk_data_type"]]
    return df[[x for x in df.columns if x not in ["value", "fk_data_record", "fk_data_type"]]]

def make_df_userfriendly_2(datatypes, df: pd.DataFrame):
    df["Record Hash"] = df["fk_data_record"]
    df["Data Type"] = [datatypes[str(x)] for x in df["fk_data_type"]]
    return df

def get_graphable_data(dataset_id, datatype_id, flatten=True) -> pd.DataFrame | None:
    logger.debug(f"{stack()[0][3]}()")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    statistics = client.harm_numerical.get_numeric_statistics(dataset_id=dataset_id, datatype_id=datatype_id)
    logger.debug(f"Statistics: {statistics}")
    df = None
    if statistics.count_total > 0:
        if statistics.count_float_confidence > 0:
            df = client.harm_numerical.list_harm_numericals(numeric_type="float_confidence", datatype_id=datatype_id, dataset_id=dataset_id, request_as="pandas")["float_confidence"]
        # logger.debug(f"float_confidence dataframe status: {repr(df)}")
        if statistics.count_float > 0:
            request_new_df = client.harm_numerical.list_harm_numericals(numeric_type="float", datatype_id=datatype_id, dataset_id=dataset_id, request_as="pandas")["float"]
            # logger.debug(repr(request_new_df))
            if df == None:
                df = request_new_df
            else:
                df = pd.concat(df, request_new_df)
        # logger.debug(f"float dataframe status: {repr(df)}")
        if statistics.count_int_confidence > 0:
            request_new_df = client.harm_numerical.list_harm_numericals(numeric_type="int_confidence", datatype_id=datatype_id, dataset_id=dataset_id, request_as="pandas")["int_confidence"]
            # logger.debug(repr(request_new_df))
            if df == None:
                df = request_new_df
            else:
                df = pd.concat(df, request_new_df)
        # logger.debug(f"int_confidence dataframe status: {repr(df)}")
        if statistics.count_int > 0:
            request_new_df = client.harm_numerical.list_harm_numericals(numeric_type="int", datatype_id=datatype_id, dataset_id=dataset_id, request_as="pandas")["int"]
            # logger.debug(repr(request_new_df))
            if df == None:
                df = request_new_df
            else:
                df = pd.concat(df, request_new_df)
        # logger.debug(f"int dataframe status: {repr(df)}")
    return df
        


def get_location_data(dataset_id):
    logger.debug(f"{stack()[0][3]}({dataset_id})")
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        token=P2F_PORTAL_TOKEN, 
                        # token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                        email=P2F_PORTAL_EMAIL_ADDRESS)
    locations = client.harm_location.list_harm_locations(dataset_id=dataset_id)
    return locations


def generic_scatter(graphable_data):
    pd.DataFrame()


if "dataset_id" in st.query_params.keys():
    # Get the dataset to inspect from the url parameter
    dataset_id = st.query_params["dataset_id"]
    # Get the dataset from the API
    dataset_data = get_dataset(dataset_id=dataset_id)
    # st.write(dataset_data)
    st.header(dataset_data.title)
    # st.page_link("upload_data.py", 
                #  query_params={"dataset_id": dataset_id})
    mcol_1, mcol_2, mcol_3, mcol_4, mcol_5 = st.columns(5)  # metadata columns
    mcol_1.text(f"Publication Date: {dataset_data.publication_date}")
    if not dataset_data.is_new_p2f:
        mcol_2.image(load_SVG("P2F_DataReUse.svg"))
    if dataset_data.is_new_p2f:
        mcol_2.image(load_SVG("P2F_NewData.svg"))
    st.link_button(
        "View Dataset's Home Repository", url=f"https://doi.org/{dataset_data.doi}"
    )
    # Search for sub-datasets with the client
    subdatasets = get_subdatasets(doi=dataset_data.doi)
    # Create a {dataset_id: pydantic Dataset}
    subdatasets = {
        str(x.dataset_id): get_dataset(x.dataset_id)
        for x in subdatasets
    }
    # If there are sub-datasets
    if len(subdatasets.keys()) > 0:
        # create the sub-dataset header
        st.subheader("Subdatasets")
        # Make the sub-datasets selectable, default is first item in list
        selected_subdataset = st.pills(
            "Subdatasets:",
            options=[x.sub_dataset_name for x in list(subdatasets.values())],
            default=[x.sub_dataset_name for x in subdatasets.values()][0],
        )
        selected_subdataset_uuid = [
                x.dataset_id
                for x in subdatasets.values()
                if x.sub_dataset_name == selected_subdataset
            ][0]

        # Collect together all of the dataset_ids for parent and children
        all_dataset_uuids = [dataset_id]
        all_dataset_uuids += [x for x in list(subdatasets.keys())]
        # st.write(all_dataset_uuids)
        st.header("Data Explorer")
        # Get the data types for the selected sub-dataset
        datatypes = get_dataset_datatypes(
            dataset_id=selected_subdataset_uuid
        )
        # If there are data-types
        if datatypes:
            if len(datatypes) > 0:
                # list a set of the measures 
                measures = list({x.measure for x in datatypes})
                # User selects the measure, default to first measure
                selected_measure = st.pills("Data Types:", options=measures, default=measures[0])

                ### MULTILINE PILLS EXPERIMENT
                measure_suboptions = [x for x in datatypes if x.measure == selected_measure]
                measure_suboptions = {str(x.datatype_id): f"**{x.measure}** ({x.unit_of_measurement})  \nMethod: {x.method}  \nCalib: {x.calibration}  \n*datatype_id: {x.datatype_id}*" for x in measure_suboptions}
                measure_columns_width = 255 * len(measure_suboptions)
                if measure_columns_width > 650:
                    measure_columns_width = "stretch"
                measure_columns = {x: y for x, y in zip(range(len(measure_suboptions)), st.columns(len(measure_suboptions), width=measure_columns_width))}
                measure_suboptions_list = list(measure_suboptions.keys())
                for dtype_id in measure_suboptions_list:
                    with measure_columns[measure_suboptions_list.index(dtype_id)].container(border=True, width=250):
                        st.markdown(measure_suboptions[dtype_id])
                        st.checkbox(label="Include", key=f"datatype_id::{dtype_id}", value=True)
                # get the currently check boxes items from the session state dictionary
                activated_datatypes = {x: y for x, y in st.session_state.items() if x.startswith("datatype_id::")}
                # filter the check boxes if they are checked   #### extra note, x[len("datatype_id::"):] is a way to get the value of x after the datatype_id:: 
                activated_datatypes = [x[len("datatype_id::"):] for x, y in activated_datatypes.items() if y == True]
                # filter out the no-longer active options as there is some stickyness with variable selection
                activated_datatypes = [x for x in activated_datatypes if x in measure_suboptions_list]
                
                graphable_data = {x: get_graphable_data(dataset_id=selected_subdataset_uuid, datatype_id=x) for x in activated_datatypes}
                graphable_data = pd.concat([x for x in graphable_data.values()], ignore_index=True) 

                graphable_data = make_df_userfriendly_2(datatypes=measure_suboptions, df=graphable_data)   

                # # list the methods of measurement
                # measure_methods = list(set([x.method for x in datatypes if x.measure == selected_measure]))
                # # User selects the method, default to first method
                # selected_measure_method = st.pills(
                #     "Method of Measurement:", options=measure_methods, default=measure_methods[0]
                # )
                # # list the calibrations
                # measure_calibration = list(set([x.calibration 
                #                        for x in datatypes 
                #                        if x.measure == selected_measure 
                #                        and x.method == selected_measure_method]))
                # selected_measure_calibration = st.pills("Calibration:", options=measure_calibration, default=measure_calibration[0])

                # selected_data_type_obj = [
                #     x
                #     for x in datatypes
                #     if x.measure == selected_measure 
                #     and x.method == selected_measure_method
                #     and x.calibration == selected_measure_calibration
                # ][0]
                # st.write(selected_data_type_obj)

                # graphable_data = get_graphable_data(
                #     dataset_id=selected_subdataset_uuid, datatype_id=selected_data_type_obj.datatype_id
                # )

                # Transform the dataframe to be more user friendly
                # friendly_graphable_data = make_df_userfriendly(datatype=selected_data_type_obj, df=graphable_data)
                # with st.expander(key="data_frame_container", expanded=True, label="Single Data Type Data Preview"):
                #     st.dataframe(friendly_graphable_data)

                graph_mode_options = ["Violin Plot", "Box Plot", "Histogram"]
                graph_mode = st.pills("How would you like to preview the graph of the data?",
                                      options=graph_mode_options,
                                      default=graph_mode_options[0])
                
                violin = px.violin(
                    graphable_data,
                    x="value",
                    title=f"Data Preview: {selected_measure}",
                    color="Data Type",
                    # subtitle=selected_measure_method,
                    # labels={"value": selected_data_type_obj.unit_of_measurement},
                )
                boxplot = px.box(
                    graphable_data,
                    x="value",
                    title=f"Data Preview: {selected_measure}",
                    color="Data Type"
                    # subtitle=selected_measure_method,
                    # labels={"value": selected_data_type_obj.unit_of_measurement},
                )
                histogram = px.histogram(
                    graphable_data,
                    x="value",
                    title=f"Data Preview: {selected_measure}",
                    color="Data Type"
                    # subtitle=selected_measure_method,
                    # labels={"value": selected_data_type_obj.unit_of_measurement},
                )

                graph_display = {"Violin Plot": violin, "Box Plot": boxplot, "Histogram": histogram,}
                st.plotly_chart(graph_display[graph_mode])

        st.subheader("Data Geography")

        dataset_locations = []
        for dataset_locs in all_dataset_uuids:
            bdata = get_location_data(dataset_locs)
            bdata = [
                x
                for x in bdata
                if str(x.location_id)
                not in [str(y.location_id) for y in dataset_locations]
            ]
            dataset_locations += bdata
        logger.debug(f"Dataset locations after request: {dataset_locations}")
        dataset_locations = [x.model_dump(exclude_unset=True) for x in dataset_locations]
        dataset_locations = pd.DataFrame(dataset_locations)
        # st.dataframe(dataset_locations)
        dataset_map = folium.Map(
            location=[
                0, 0
            ],
            zoom_start=1,
            width=1300,
            height=700,
        )
        for ix, rec in dataset_locations.iterrows():
            # st.write(rec)
            folium.Marker(
                location=[rec.latitude, rec.longitude], tooltip=rec.location_name
            ).add_to(dataset_map)
        st_folium(dataset_map, width="wide", height=700)

else:
    dataset_id = "example"

if dataset_id == "example":
    with open("./p2f-portal/assets/example-new-dataset.json", "r") as f:
        r = f.read()
    example_json = json.loads(r)
    # st.text(example_json)
    st.header(example_json["titles"][0]["title"])
    creators_list = [x["name"] for x in example_json["creators"]]
    st.markdown(f"*{'; '.join(creators_list)}*")
    st.text(example_json["descriptions"][0]["description"])

    ddf = pd.read_excel("./p2f-portal/assets/example-new-dataset.xlsx", sheet_name=None)
    sheet_selection = st.pills(
        "Select a data sheet", options=ddf.keys(), default=list(ddf.keys())[0]
    )
    st.dataframe(ddf[sheet_selection])
    column_selection = st.pills(
        "Select a column to plot", [x for x in ddf[sheet_selection].columns]
    )

    if column_selection:
        plot = px.scatter(ddf[sheet_selection][column_selection])
        st.plotly_chart(plot)

    site_map = folium.Map([31.68, -51.156], zoom_start=2)
    site_982 = folium.Marker(location=[57.517, -15.867], popup="ODP Site 982").add_to(
        site_map
    )
    site_1241 = folium.Marker([5.843, -86.445], popup="ODP Site 1241").add_to(site_map)
    st_folium(site_map, width=725)
