from datetime import datetime
import streamlit as st
import pandas as pd
from helper import get_data_cfpwh,  convert_to_date, convert_df_to_csv
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# page config
st.set_page_config(page_title='Experimental', page_icon= "🔩", layout='wide')
st.markdown('# Experimental')
#####################

with st.container():
    with st.expander('Real Time Shipping Data', expanded=True):
        df= get_data_cfpwh()
        df = df[df['dqabdt'].apply(lambda x: str(x).isdigit())]
        df['date'] = df['dqabdt'].apply(convert_to_date)
        st.table(df)
        st.download_button('Donwload', data=convert_df_to_csv(df), file_name='Experimental.csv', mime='text/csv')

