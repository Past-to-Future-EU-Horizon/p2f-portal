from assets import disclosure_text
from p2f_client.p2f_client import P2F_Client
import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime

de = load_dotenv()

P2F_API_HOSTNAME = os.getenv("P2F_API_HOSTNAME")
P2F_API_PORT = int(os.getenv("P2F_API_PORT", default="443"))
P2F_API_HTTPS = bool(os.getenv("P2F_API_HTTPS", default="True"))
P2F_PORTAL_EMAIL_ADDRESS = os.getenv("P2F_PORTAL_EMAIL_ADDRESS")
P2F_PORTAL_TOKEN = os.getenv("P2F_PORTAL_TOKEN")


st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Explore Publications from the Project")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                    port=P2F_API_PORT, 
                    https=P2F_API_HTTPS, 
                    token=P2F_PORTAL_TOKEN, 
                    token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                    email=P2F_PORTAL_EMAIL_ADDRESS)