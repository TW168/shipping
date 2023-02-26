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
                # Get input from user
                site = st.text_input('Enter site:')
                product_group = st.text_input('Enter product group:')

                # Query the database
                query = f"SELECT Site, Truck_Appointment_Date, Freight_Amount, Product_Code, Pick_Weight, Number_of_Pallet, Pick_Weight, Number_of_Pallet FROM db3.ipg_ez where Site='{site}' and Product_Group='{product_group}' and BL_Number not like 'WZ%' and Truck_Appointment_Date is not null"
                result_df = pd.read_sql_query(query, conn)

                # Group the result by date and calculate the sum of pick weight
                grouped_by_date = result_df.groupby('Truck_Appointment_Date').agg({'Pick_Weight': 'sum'})

                # Group the result by CSR and calculate the sum of pick weight
                grouped_by_CSR = result_df.groupby('CSR').agg({'Pick_Weight': 'sum'})
                # Display the results
                st.write(grouped_by_CSR)
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
