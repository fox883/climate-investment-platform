import streamlit as st
from services.utils import show_connection_status, show_disclaimer
from services.utils import button_to


st.set_page_config(page_title="Welcome", page_icon="🌱")

show_connection_status()
show_disclaimer()

st.markdown("---")
st.markdown("\u27A1\uFE0F Please **go to the sidebar** and click **Login** to begin registration or access your project.")
