import streamlit as st
import pandas as pd 
from helper import ship_tomorrow, ship_tomorrow_to_houston, ship_tomorrow_to_remington
from datetime import datetime
import datetime
import plotly.express as px


st.set_page_config(page_title="Summary", page_icon="📰", layout='wide')
st.markdown("# Summary")


try:
    with st.container():
        with st.expander("Ship Tomorrow", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                # Defined the dates
                rpt_date = st.date_input("Choose a date: ")
                truck_appt_date = rpt_date+datetime.timedelta(days=1)

            st.markdown('### Truck Log')    
            col1, col2, col3 = st.columns(3)
        
            with col1: 
                # Ship tomorrow truck log
                ship_tomorrow_df = ship_tomorrow(rpt_date, truck_appt_date)
                ship_tomorrow_df['LBS'] = ship_tomorrow_df['LBS'].astype(int).map('{:,.0f}'.format)
                st.dataframe(ship_tomorrow_df)
            with col2:
                # Ship tomorrow consignment to Houston
                ship_tomorrow_houston_df = ship_tomorrow_to_houston(rpt_date, truck_appt_date)
                ship_tomorrow_houston_df['To Houston'] = ship_tomorrow_houston_df['To Houston'].astype(int).map('{:,.0f}'.format)
                st.dataframe(ship_tomorrow_houston_df)
            with col3:
                # ship tomorrow consignment to Remington
                ship_tomorrow_remington_df = ship_tomorrow_to_remington(rpt_date, truck_appt_date)
                ship_tomorrow_remington_df['To Remington'] = ship_tomorrow_remington_df['To Remington'].astype(int).map('{:,.0f}'.format)
                st.dataframe(ship_tomorrow_remington_df)
    

except Exception as e:
    print (e)