import streamlit as st
import pandas as pd 
from helper import connect_to_database, ship_tomorrow
from datetime import datetime
import datetime
import plotly.express as px



st.set_page_config(page_title="Summary", page_icon="📰", layout='wide')
st.markdown("# Summary")


try:
    with st.container():
        with st.expander("Ship Tomorrow"):
            #conn = connect_to_database(DB, "mysql")
            rpt_date = st.date_input("Choose a date: ")
            truck_appt_date = rpt_date+datetime.timedelta(days=1) 
            ship_tomorrow_df = ship_tomorrow(rpt_date, truck_appt_date)
            ship_tomorrow_df['sum(Pick_Weight)'] = ship_tomorrow_df['sum(Pick_Weight)'].astype(int).map('{:,.0f}'.format)
            ship_tomorrow_df['sum(Number_of_Pallet)'] = ship_tomorrow_df['sum(Number_of_Pallet)'].astype(int).map('{:,.0f}'.format)
            st.write(ship_tomorrow_df)
        
        
        
except Exception as e:
    print (e)
    st.warning(f"No Data Available")
