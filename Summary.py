import streamlit as st
import pandas as pd 
from helper import connect_to_database
from datetime import datetime
DB = 'db3_db'

st.set_page_config(page_title="Summary", page_icon="📰", layout='wide')
st.markdown("# Summary")




try:
    with st.container():
        with st.expander('Choose dates'):

            conn = connect_to_database(DB)
            qry = """ select Site, BL_Number, Truck_Appointment_Date, State, Ship_to_City, Ship_to_Customer, CSR, Product_Code, Pick_Weight, Number_of_Pallet, Carrier_ID, Unit_Freight, rpt_run_date  FROM db3.ipg_ez """
            summary_df = pd.read_sql_query(qry, conn)

            # Get the earliest and latest report date
            min_date = summary_df["rpt_run_date"].min()
            max_date = summary_df["rpt_run_date"].max()
            if min_date < max_date:
                selected_range = st.slider(
                    "Select a range of dates",
                    min_date,
                    max_date,
                    (min_date, max_date),
                )
                # Filter the data based on the selected date range
                mask = (summary_df['Truck_Appointment_Date'] >= selected_range[0]) & (summary_df['Truck_Appointment_Date'] <= selected_range[1])
                filtered_df = summary_df.loc[mask]

                # Group the data by Site and calculate the sum of Pick_Weight
                groupby_site = filtered_df.groupby(['Site','Product_Group'])['Pick_Weight'].sum()

                # Display the results
                st.write(groupby_site)
            else:
                st.error("Error: End date must be after start date.")

            begin = selected_range[0]
            end = selected_range[1]
            
            
    # # End of day truck log
    # qry = """SELECT * FROM ezs WHERE rpt_run_date BETWEEN '{begin}' AND '{end}' and SITE='{site}' and `Product Group`='{group}' and rpt_run_time='{hour}'""".format(begin=begin, end=end, site=site, group=group, hour=hour)
    # data = pd.read_sql_query(qry, conn)
except Exception as e:
    print (e)
    st.warning(f"No Data Available")
