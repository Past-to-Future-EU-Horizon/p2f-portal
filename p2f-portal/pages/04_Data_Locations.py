from assets import disclosure_text
from p2f_client.p2f_client import P2F_Client
import streamlit as st
from streamlit_folium import st_folium
import folium
from dotenv import load_dotenv
import os
from datetime import datetime

de = load_dotenv()

P2F_API_HOSTNAME = os.getenv("P2F_API_HOSTNAME")
P2F_API_PORT = int(os.getenv("P2F_API_PORT", default="443"))
P2F_API_HTTPS = bool(os.getenv("P2F_API_HTTPS", default="True"))
P2F_PORTAL_EMAIL_ADDRESS = os.getenv("P2F_PORTAL_EMAIL_ADDRESS")
P2F_PORTAL_TOKEN = os.getenv("P2F_PORTAL_TOKEN")

client = P2F_Client(hostname=P2F_API_HOSTNAME, 
                    port=P2F_API_PORT, 
                    https=P2F_API_HTTPS, 
                    token=P2F_PORTAL_TOKEN, 
                    token_expiration=datetime(2026, 4, 30, 23, 59, 59), 
                    email=P2F_PORTAL_EMAIL_ADDRESS)