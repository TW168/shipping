import streamlit as st
import pandas as pd 
from helper import ship_tomorrow, ship_tomorrow_houston, ship_tomorrow_remington,site_lst, group_lst
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
            with col2:
                pass
                # site = st.selectbox('Choose a Site: ', options=site_lst)
                # group = st.selectbox('Choose a Group', group_lst)
            # Ship tomorrow truck log
            st.write(f"ship on {truck_appt_date}")

            ship_tomorrow_df = ship_tomorrow(rpt_date, truck_appt_date)
            ship_tomorrow_df['LBS'] = ship_tomorrow_df['LBS'].astype(int).map('{:,.0f}'.format)
            st.dataframe(ship_tomorrow_df)
            # Ship tomorrow consignment to Houston
            ship_tomorrow_houston_df = ship_tomorrow_houston(rpt_date, truck_appt_date)
            ship_tomorrow_houston_df['Consignment to Houston'] = ship_tomorrow_houston_df['Consignment to Houston'].astype(int).map('{:,.0f}'.format)
            st.dataframe(ship_tomorrow_houston_df)
            # ship tomorrow consignment to Remington
            ship_tomorrow_remington_df = ship_tomorrow_remington(rpt_date, truck_appt_date)
            ship_tomorrow_remington_df['Consignment to Remington'] = ship_tomorrow_remington_df['Consignment to Remington'].astype(int).map('{:,.0f}'.format)
            st.dataframe(ship_tomorrow_remington_df)

except Exception as e:
    print (e)
    