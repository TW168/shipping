import streamlit as st
import pandas as pd
from datetime import datetime
# from sqlalchemy import create_engine

# Connect to the database
conn = st.experimental_connection('ws_hub', type='sql')
conn

with st.expander("Expander", expanded=True):
    date_col, col2, col3, col4, col5 = st.columns(5)
    with date_col:
        sche_date = st.date_input("Date", datetime.now())
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        aal = st.number_input("AAL", min_value=0, max_value=10)
        cal = st.number_input("CAL", min_value=0, max_value=10)
        chr = st.number_input("CHR", min_value=0, max_value=10)
    with col2:
        darke = st.number_input("DRAKE", min_value=0, max_value=10)
        giltner = st.number_input("Giltner", min_value=0, max_value=10)
        geodis = st.number_input("GEODIS", min_value=0, max_value=10)

    