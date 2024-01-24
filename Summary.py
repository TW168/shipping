
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd 
from helper import ship_tomorrow, ship_tomorrow_to_houston, ship_tomorrow_to_remington, ez_analyst, get_popular_products
import plotly.graph_objs as go
import plotly.express as px

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
            # combined_query = """
            # SELECT
            #     SUM(CASE WHEN BL_Number NOT LIKE 'WZ%' AND BL_Number LIKE 'W%' AND Truck_Appointment_Date IS NULL THEN Pick_Weight ELSE 0 END) AS 'Avail. to ship',
            #     SUM(CASE WHEN BL_Number LIKE 'WZ%' THEN Pick_Weight ELSE 0 END) AS 'WZ',
            #     DATE_FORMAT(rpt_run_date, '%Y-%m') AS 'Year-Month',
            #     rpt_run_time
            # FROM
            #     ipg_ez
            # WHERE
            #     site = 'AMJK'
            #     AND Product_Group = 'SW'
            #     AND rpt_run_time = '09:00:00'
            # GROUP BY
            #     DATE_FORMAT(rpt_run_date, '%Y-%m'),
            #     rpt_run_time;
            # """
            # # Execute the query and load data into DataFrames
            # df = conn.query(combined_query)

#             # Format columns to include commas for thousands separator
#             df['Avail. to ship'] = df['Avail. to ship'].apply(lambda x:"{:,.0f}".format(x))
#             df['WZ'] = df['WZ'].apply(lambda x: "{:,.0f}".format(x))

#             # Rename the columns for clarity
#             df.rename(columns={'Avail. to ship':'Available to Ship','WZ': 'WZ (lbs)'}, inplace=True)
            
#             # Create a bar chart using Plotly
#             fig = go.Figure()

#             # Add 'Avail. to ship' as a bar
#             fig.add_trace(go.Bar(x=df['Year-Month'], y=df['Available to Ship'], name='Available to Ship'))

#             # Add 'WZ' as a bar
#             fig.add_trace(go.Bar(x=df['Year-Month'], y=df['WZ (lbs)'], name='WZ (lbs)'))

#             # Update layout for the chart
#             fig.update_layout(
#                 barmode='group',  # This will group the bars
#                 title='Avail. to Ship and WZ by Year-Month'
#             )

#             # Display the chart using Streamlit
#             # st.title('Avail. to Ship and WZ Data')
#             st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    print (datetime.now(), e)

# with st.container():
#     with st.expander('New Expander'):
#         # Open your SQL file
#         with open('sql\AMJK_SW_TruckAppointmentSummary.sql', 'r') as sql_file:
#             sql_qry = sql_file.read()
#         df = conn.query(sql_qry)
        
#         # Convert the 'Truck_Appointment_Date' column to datetime format
#         df['Truck_Appointment_Date'] = pd.to_datetime(df['Truck_Appointment_Date'])
#         df['Appointment_Date'] = pd.to_datetime(df['Truck_Appointment_Date']).dt.date
#         # Extract the year month from the Truck_Appointment_Date
#         df['Year'] = df['Truck_Appointment_Date'].dt.year
#         df['Month'] = df['Truck_Appointment_Date'].dt.month
#         years = [2022, 2023] # Hard code the years because too many input error in the ipg_ez report
#         # Create a selectbox for the years
#         selected_year = st.selectbox('Select a Year', options=years)
#         # Filter the dataframe based on the selected year
#         df_filtered = df[df['Year'] == selected_year]
#         # Display the filtered dataframe
#         df_filtered['lbs'] = df_filtered['lbs'].apply(lambda x:"{:,.0f}".format(x))
#         df_filtered['plt'] = df_filtered['plt'].apply(lambda x:"{:,.0f}".format(x))
#         st.dataframe(df_filtered[['Appointment_Date', 'Year', 'Month','BL_Number', 'lbs', 'plt', 'Truck_Appointment_Date']])
        


        


