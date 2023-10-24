import streamlit as st
import pandas as pd
import plotly_express as px
import datetime


st.set_page_config(page_title="Warship-Ship Log", page_icon="📰", layout='wide')
st.title("Stretch Film Shipment Log")

# Connect to the database
conn = st.experimental_connection("ws_hub", type="sql")

# show daily Stretch film shipment log
with st.expander('Stretch Film Shipment Log', expanded=True):
    sites = conn.query("select site from v_sites")
    groups = conn.query("select product_group from v_groups")
    col1, col2, col3 = st.columns(3)
    with col1:
        pass
        
    with col2:
        pass
          
    ship_to_sites_qry = """SELECT 
        Truck_Appointment_Date, 
        Ship_to_customer, 
    
        sum(Pick_Weight) as "LBS", 
        sum(Number_of_pallet) as "PLT" 
    FROM 
        ws_hub.v_my_stretch_film_daily_shipment_log
    WHERE 
        Ship_to_Customer IN (
            'AMTOPP WAREHOUSE - HOUSTON', -- Ship to Houston
            'INTEPLAST GROUP CORP. (AMTOPP)', -- Ship to Remington
            'Pinnacle films', -- ship to Charlotte
            'INTEPLAST GROUP CORP.(AMTOPP ( CFP)' -- ship to Phenix
        )
    GROUP BY 
        Truck_Appointment_Date, 
        Ship_to_customer
        
    ORDER BY 
        Ship_to_customer, 
        Truck_Appointment_Date;
    """      
    ship_to_sites_df = conn.query(ship_to_sites_qry)
    # Assuming ship_to_sites_df['Truck_Appointment_Date'] is of type datetime
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    # Convert 'Truck_Appointment_Date' to datetime 
    ship_to_sites_df['Truck_Appointment_Date'] = pd.to_datetime(ship_to_sites_df['Truck_Appointment_Date'])
    # Now filter for the current month
    ship_to_sites_df = ship_to_sites_df[
        (ship_to_sites_df['Truck_Appointment_Date'].dt.month == current_month) & 
        (ship_to_sites_df['Truck_Appointment_Date'].dt.year == current_year)
    ]
    # Convert 'Truck_Appointment_Date' to datetime
    ship_to_sites_df['Truck_Appointment_Date'] = pd.to_datetime(ship_to_sites_df['Truck_Appointment_Date']).dt.date
    # st.dataframe(ship_to_sites_df)
    # Create the new DataFrame using only the needed columns
    df = ship_to_sites_df[['Ship_to_Customer', 'LBS']].copy()
    # Rename the columns
    df.rename(columns={'Ship_to_Customer': 'Customers'}, inplace=True)
    # Ensure 'Customers' is string
    df['Customers'] = df['Customers'].astype(str)
    df['LBS'] = df['LBS'].astype(int)
    # Group by 'Customers' and sum 'LBS'
    df_grouped = df.groupby('Customers').agg({'LBS': 'sum'}).reset_index()
    # Format 'LBS' column again to have commas as thousands separators and no decimals
    df_grouped['LBS'] = df_grouped['LBS'].apply(lambda x: '{:,.0f}'.format(x))
    st.dataframe(df_grouped, use_container_width=True)