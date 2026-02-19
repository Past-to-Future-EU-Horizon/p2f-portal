from assets import disclosure_text
import streamlit as st

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Welcome to the Past 2 Future Data Portal")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

welcome_markdown = """
This portal is for the Past 2 Future project, 
grouping together source datasets that will go into our project, 
and the datasets that are produced by the project. 
"""

st.markdown(welcome_markdown)

abstract_markdown = """
**Project Abstract**

Understanding past climate evolution is essential for improving 
predictions of future climate change. Current Earth system models (ESMs) 
rely on 170 years of stable data, but it is necessary to account for 
longer-term changes and critical transitions that impact ecosystems and 
societies. Enhancing our understanding of these processes is crucial 
for making accurate forecasts. In this context, the EU-funded P2F project 
will improve our understanding of the climatic and societal impacts of the 
ongoing climate crisis by integrating paleoenvironmental data, ESMs and 
theoretical approaches. The project will enhance ESM capabilities and 
advance the Climate Model Intercomparison Project model development cycle 
by providing paleo-informed models for future projections and developing 
plausible climate change scenarios based on past events."""

st.markdown(abstract_markdown)

bg1_c1, bg1_c2, bg1_c3, bg1_c4 = st.columns(4)

bg1_c1.link_button(
    "Read more about the project on the EU Website 🇪🇺",
    "https://doi.org/10.3030/101184070",
)

if bg1_c2.button("Explore the datasets we're re-using"):
    st.switch_page("pages/01_Source_Datasets.py")

if bg1_c3.button("Explore the new datasets we've created"):
    st.switch_page("pages/02_New_Datasets.py")

if bg1_c4.button("Explore our project publications"):
    st.switch_page("pages/03_Project_Publications.py")
