
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd 
from helper import ship_tomorrow, ship_tomorrow_to_houston, ship_tomorrow_to_remington, ez_analyst, get_popular_products, connect_to_database
import plotly.graph_objs as go
import plotly.express as px

DB='ws_hub_db'
st.set_page_config(page_title="Warship-Summary", page_icon="📰", layout='wide')

# Connect to the database
# conn = st.connection("ws_hub", type="sql")

st.markdown("# Summary")

try:
    with st.container():
        with st.expander("Ship Tomorrow", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                # Defined the dates
                rpt_date = st.date_input("Choose a date: ")
                truck_appt_date = rpt_date+timedelta(days=1)

            st.markdown('### Tomorrow Truck Log')    
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
    
    with st.container():
        with st.expander("AMJK Only Simple Summary", expanded=True):
            rpt_date = st.date_input('Choose a date')
            df = ez_analyst(rpt_date)
            st.dataframe(df)
except Exception as e:
    print (datetime.now(), e)
   
conn = connect_to_database(DB, dbms='mysql') 
am_qry = "SELECT rpt_run_date, SUM(pick_weight) AS AM_ready_to_ship FROM ipg_ez WHERE site = 'AMJK' AND truck_appointment_date IS NULL AND Product_Group = 'SW'AND rpt_run_time = '09:00:00'    AND BL_Number LIKE 'WZ%'    AND Product_Code not like 'INST%'GROUP BY    rpt_run_date;"
am_df = pd.read_sql_query(am_qry, conn)

ship_tomorrow_qry = "SELECT    rpt_run_date,    SUM(pick_weight) AS ship_tomorrow FROM    ipg_ez WHERE    site = 'AMJK'    AND truck_appointment_date IS NOT NULL    AND Product_Group = 'SW'    AND rpt_run_time = '16:00:00'    AND BL_Number NOT LIKE 'WZ%'    AND Product_Code not like 'INST%' GROUP BY    rpt_run_date;"
ship_tmr_df = pd.read_sql_query(ship_tomorrow_qry, conn)
merged_df = pd.merge(am_df, ship_tmr_df, on='rpt_run_date') 
merged_df = merged_df.sort_values(by='rpt_run_date', ascending=False)

# Convert 'rpt_run_date' to datetime format
merged_df['rpt_run_date'] = pd.to_datetime(merged_df['rpt_run_date'])

# Create a new column for year and month
merged_df['Year'] = merged_df['rpt_run_date'].dt.year
merged_df['Month'] = merged_df['rpt_run_date'].dt.month

# Create the Plotly Express line chart
fig = px.line(merged_df, x='rpt_run_date', y=['AM_ready_to_ship', 'ship_tomorrow'],
              labels={'value': 'Count'}, title='Shipments Over Time',
              category_orders={'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]})

# Show the plot
st.plotly_chart(fig, use_container_width=True)
        


