import streamlit as st
from src.main import display_message


st.title("Energy Dashboard")

st.write(display_message())