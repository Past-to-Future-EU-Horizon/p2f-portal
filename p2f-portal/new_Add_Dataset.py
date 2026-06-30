import streamlit as st
from assets import disclosure_text
from p2f_pydantic.harm_timeslices import HARM_Timeslice


st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

st.title("Add a new dataset")

new_dataset = st.form(key="new-dataset")

ds_url = new_dataset.text_input(label="URL")
st.button(label="Get metadata from DOI API")

ds_title = new_dataset.text_input(label="Title")

ds_new_p2f = new_dataset.pills(label="Is this a new dataset by the P2F Consortium?", 
                               options=["Yes", "No"], 
                               default="Yes")

tsc0, tsc1, tsc2 = new_dataset.columns(3)
ds_time_older = tsc0.number_input(label="What is the oldest date in this dataset?")
ds_time_young = tsc1.number_input(label="What is the youngest date in this dataset?")
ds_time_zero = tsc2.pills(label="What is the 0 year?", options=["1950", "2000", "Other"])


timeslices = [
    HARM_Timeslice(timeslice_name="last 7,500 Years", timeslice_age_oldest=7_500, timeslice_age_recent=0),
    HARM_Timeslice(timeslice_name="4,2 aridification event", timeslice_age_mean=4_200),
    HARM_Timeslice(timeslice_name="Mid-Holocene Warm Period/ Holocene Climatic Optimum", timeslice_age_oldest=9_500, timeslice_age_recent=5_500),
    HARM_Timeslice(timeslice_name="Mid-Holocene 6ka", timeslice_age_mean=6_000),
    HARM_Timeslice(timeslice_name="thermal maximum of the Holocene Climatic Maximum", timeslice_age_mean=8_000),
    HARM_Timeslice(timeslice_name="8,2 Ka cold event", timeslice_age_mean=8_200),
    HARM_Timeslice(timeslice_name="Holocene", timeslice_age_oldest=11_700, timeslice_age_recent=0),
    HARM_Timeslice(timeslice_name="Bølling-Allerød transition", timeslice_age_oldest=14_600, timeslice_age_recent=13_000),
    HARM_Timeslice(timeslice_name="Last glacial-interglacial transition (Termination 1, T1)", timeslice_age_oldest=19_000, timeslice_age_recent=8_000),
    HARM_Timeslice(timeslice_name="Last Glacial Maximum (LGM)", timeslice_age_oldest=31_000, timeslice_age_recent=16_000),
    HARM_Timeslice(timeslice_name="Last Glacial Maximum (LGM) snapshot", timeslice_age_oldest=23_000, timeslice_age_recent=19_000),
    HARM_Timeslice(timeslice_name="Last Glacial Period (LGP)", timeslice_age_oldest=115_000, timeslice_age_recent=11_700),
    HARM_Timeslice(timeslice_name="Dansgaard-Oeschger (D-O) events", timeslice_age_oldest=130_000, timeslice_age_recent=11_700),
    HARM_Timeslice(timeslice_name="Last interglacial to glacial transition (MIS 5a to MIS 4)", timeslice_age_oldest=85_000, timeslice_age_recent=65_000),
    HARM_Timeslice(timeslice_name="Last Interglacial/Eemian/MIS 5e", timeslice_age_oldest=130_000, timeslice_age_recent=115_000),
    HARM_Timeslice(timeslice_name="Marine Isotope Stage 5/MIS 5", timeslice_age_oldest=130_000, timeslice_age_recent=80_000),
    HARM_Timeslice(timeslice_name="Penultimate glacial-interglacial transition (T2)", timeslice_age_oldest=140_000, timeslice_age_recent=120_000),
    HARM_Timeslice(timeslice_name="Penultimate interglacial to glacial transition (MIS 7e to MIS 7d)", timeslice_age_oldest=250_000, timeslice_age_recent=225_000),
    HARM_Timeslice(timeslice_name="Marine Isotope Stage 11/MIS 11", timeslice_age_oldest=424_000, timeslice_age_recent=374_000),
    HARM_Timeslice(timeslice_name="Mid-Pleistocene Transition/MPT", timeslice_age_oldest=1_250_000, timeslice_age_recent=700_000),
    # HARM_Timeslice(timeslice_name="late Pliocene and early Pleistocene glacial-interglacial cycles", timeslice_age_oldest=, timeslice_age_recent=), # No dates provided in spreadsheet 
    HARM_Timeslice(timeslice_name="Pre-MPT glacial cycles (MIS 39 to MIS 45)", timeslice_age_oldest=1_400_000, timeslice_age_recent=1_250_000),
    HARM_Timeslice(timeslice_name="MIS 100 (MIS 95 to MIS 101)", timeslice_age_oldest=2_600_000, timeslice_age_recent=2_400_000),
    HARM_Timeslice(timeslice_name="Pliocene-Pleistocene transition", timeslice_age_mean=2_580_000),
    HARM_Timeslice(timeslice_name="Pliocene", timeslice_age_oldest=5_330_000, timeslice_age_recent=2_580_000),
    HARM_Timeslice(timeslice_name="Mid-Piacenzian Warm Period (mPWP)/Mid-Pliocene Warm Period", timeslice_age_oldest=3_300_000, timeslice_age_recent=3_000_000),
    HARM_Timeslice(timeslice_name="KM5c interglacial", timeslice_age_mean=3_205_000),
    # HARM_Timeslice(timeslice_name="KM5c-M2 transition", timeslice_age_oldest=, timeslice_age_recent=), # No dates provided in spreadsheet
    HARM_Timeslice(timeslice_name="M2 glacial", timeslice_age_mean=3_300_000),
    HARM_Timeslice(timeslice_name="Eocene Climatic Optimum/Early Eocene Climatic Optimum/EECO", timeslice_age_oldest=53_000_000, timeslice_age_recent=49_000_000),
]

ds_timeslices = new_dataset.selectbox(label="Which P2F Timeslices does this cover?", 
                                  options=[x.timeslice_name for x in timeslices], )

ds_keywords = new_dataset.text_input(label="Keywords (comma separated)")

ds_seasonality = new_dataset.pills(label="Does the dataset have seasonality?", 
                                   options=["No", "Winter/Summer", "Hot/Cold", "Winter/Spring/Summer/Autumn", "Other"], 
                                   default="No")

auth_email = new_dataset.text_input(label="P2F Authorized Email Address")
auth_token = new_dataset.text_input(label="Your current P2F Token")

submit = new_dataset.form_submit_button("Add dataset")