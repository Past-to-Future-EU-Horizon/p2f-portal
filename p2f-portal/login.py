from assets import disclosure_text
from p2f_client.p2f_client import P2F_Client
import streamlit as st
import os
from dotenv import load_dotenv

de = load_dotenv()

P2F_API_HOSTNAME = os.getenv("P2F_API_HOSTNAME")
P2F_API_PORT = int(os.getenv("P2F_API_PORT", default="443"))
P2F_API_HTTPS = bool(os.getenv("P2F_API_HTTPS", default="True"))
P2F_PORTAL_EMAIL_ADDRESS = os.getenv("P2F_PORTAL_EMAIL_ADDRESS")
P2F_PORTAL_TOKEN = os.getenv("P2F_PORTAL_TOKEN")

st.set_page_config(layout="wide")

st.logo("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.image("./p2f-portal/assets/P2F_text_transparent_MR.png")
st.title("Welcome to the Past 2 Future Data Portal")

st.sidebar.image("./p2f-portal/assets/EN_FundedbytheEU_RGB_POS.png")
st.sidebar.text(disclosure_text.disclosure_text)

def request_token():
    st.code(st.session_state)
    client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                        port=P2F_API_PORT, 
                        https=P2F_API_HTTPS, 
                        email=st.session_state["email_token_request"])
    client.request_token()

with st.sidebar.container(border=True):
    st.markdown("""The Past to Future Portal is being developed open source
                and is available on GitHub, see all the components at the
                link below:""")
    st.link_button(label="GitHub", url="https://github.com/Past-to-Future-EU-Horizon")

set_auth = st.form(key="authentication")
email_set_address = set_auth.text_input("Email address: ", key="email")
token = set_auth.text_input("Token from email: ", key="token")
set_auth.form_submit_button("Set Credentials")

tokreq = st.form(key="token-request")
tokreq.text_input("Email address: ", key="email_token_request")
tokreq.form_submit_button("Request token", 
                          on_click=request_token)
