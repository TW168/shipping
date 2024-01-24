import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px


# Page configuration
st.set_page_config(page_title="Warehouse", page_icon="🏢", layout="wide")
st.title("Warehouse")

def fetch_UDC_data(start_date, end_date):
    # UDC Log URL
    base_url = "http://172.17.8.96/cfpwh/udcs?_token=CaR4OweWoYnkEAbc9x1ZymzDRQdxeQB3g7Sa1IrQ&udate={}&utype=All"

    date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]

    # Iterate over dates, fetch data, and concatenate into a single DataFrame
    dfs = []
    for date in date_range:
        formatted_date = date.strftime("%Y-%m-%d")
        url = base_url.format(formatted_date)
        df = pd.read_html(url)[0]  # Assuming the table you want is the first one, adjust if needed
        dfs.append(df)

    result_df = pd.concat(dfs, ignore_index=True)

    # Convert Date, Start, End to proper Date and Time format
    result_df['Date_cvt'] = pd.to_datetime(result_df['Date'])
    result_df['Start_cvt'] = pd.to_datetime(result_df['Start'], format='%H:%M:%S')
    result_df['End_cvt'] = pd.to_datetime(result_df['End'], format='%H:%M:%S')

    # Add one day to 'End' time if it's less than 'Start' time
    result_df.loc[result_df['End_cvt'] < result_df['Start_cvt'], 'End_cvt'] += pd.Timedelta(days=1)

    result_df['Duration'] = result_df['End_cvt'] - result_df['Start_cvt']
    result_df['Duration_sec'] = result_df['Duration'].dt.total_seconds()
    result_df['Duration_minutes'] = result_df['Duration'].dt.total_seconds() / 60
    # Combine 'Date' and 'Start' into one column
    result_df['DateTime'] = pd.to_datetime(result_df['Date'].astype(str) + ' ' + result_df['Start'])
    # Convert 'DateTime' to the desired format
    result_df['DateTime'] = pd.to_datetime(result_df['DateTime'])
    result_df['Hour'] = result_df['DateTime'].dt.hour
    # Save the combined DataFrame to a CSV file
    # result_df.to_csv("november_2023_data.csv", index=False)
    # st.dataframe(result_df)

def today_UDC_data():
    """
    This function fetches the UDC log data from a specific URL, formats the date and time data, 
    calculates the duration of each UDC in seconds and minutes, and returns the data as a pandas DataFrame.

    Returns:
        df (pd.DataFrame): A DataFrame containing the UDC log data with additional columns for formatted date/time and duration.
    """
    # UDC Log URL
    base_url = "http://172.17.8.96/cfpwh/udcs?_token=CaR4OweWoYnkEAbc9x1ZymzDRQdxeQB3g7Sa1IrQ&udate={}&utype=All"
    today = datetime.today().strftime("%Y-%m-%d")
    url = base_url.format(today)
    df = pd.read_html(url)[0]  # Assuming the table you want is the first one, adjust if needed
    # Convert Date, Start, End to proper Date and Time format
    df['Date_cvt'] = pd.to_datetime(df['Date'])
    df['Start_cvt'] = pd.to_datetime(df['Start'], format='%H:%M:%S')
    df['End_cvt'] = pd.to_datetime(df['End'], format='%H:%M:%S')
    df['Duration'] = df['End_cvt'] - df['Start_cvt']
    df['Duration_sec'] = df['Duration'].dt.total_seconds()
    df['Duration_minutes'] = df['Duration'].dt.total_seconds() / 60
 
    return df

with st.expander('Stacker Entry and Exit', expanded=True):
    with st.spinner('Fetching data...'):
        df = today_UDC_data()
        # st.dataframe(df)

    # Convert 'Duration_minutes' to numeric
    df['Duration_minutes'] = pd.to_numeric(df['Duration_minutes'], errors='coerce')
    
    # Filter DataFrame where Status is 'Done' and pallet1 and pallet2 are not equal to 9999999999
    df_done = df[(df['Status'] == 'Done') & (df['Pallet 1'] != 9999999999) & (df['Pallet 2'] != 9999999999)]
    # Group by 'Stacker' and 'Mission', then calculate the mean of 'Duration_minutes'
    average_duration = df_done.groupby(['Stacker', 'Mission'])['Duration_minutes'].mean()
    st.write(average_duration)
    
with st.expander('Untitled', expanded=True):
    warehouse_activity = pd.read_excel(r"D:\Shipping_Daily_Report\DAILY_DATA_AUTO_WAREHOUSE_All.xlsx", sheet_name='All')
    # Convert 'Date' column to datetime if it's not already
    warehouse_activity['Date'] = pd.to_datetime(warehouse_activity['Date'])

    # Create 'YearMonth' column
    warehouse_activity['YearMonth'] = warehouse_activity['Date'].dt.to_period('M').astype(str)

    # Group by 'YearMonth' and calculate the average
    avg_df = warehouse_activity.groupby('YearMonth').agg({
        'Pallet Entry': 'mean',
        'Pallet Exit': 'mean',
        'Pallets Shipped': 'mean'
    }).reset_index()

    # Plot using Plotly Express
    fig = px.line(avg_df, x='YearMonth', y=['Pallet Entry', 'Pallet Exit', 'Pallets Shipped'],
                labels={'value': 'Average(PLT)', 'YearMonth': 'Year-Month'},
                title='Average Pallet Entry, Pallet Exit, and Pallets Shipped Over Time')
    st.plotly_chart(fig, use_container_width=True)
    
    # Display the average values in a st.metric with formatting
    avg_pallet_entry = "{:.0f}".format(avg_df['Pallet Entry'].mean())
    avg_pallet_exit = "{:.0f}".format(avg_df['Pallet Exit'].mean())
    avg_pallets_shipped = "{:.0f}".format(avg_df['Pallets Shipped'].mean())
    # Display the metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        col1.metric(label='Average Pallet Entry per Day', value=avg_pallet_entry)
    with col2:
        col2.metric(label='Average Pallet Exit per Day', value=avg_pallet_exit)
    with col3:
        col3.metric(label='Average Pallets Shipped per Day', value=avg_pallets_shipped)
    buff = st.number_input('How many pallet in BUFF?',min_value=0, max_value=1500) 
    buff_decrease = int(avg_pallet_entry)-int(avg_pallets_shipped)
    # Calculate the number of days to clear the buffer
    days_to_clear_buffer = round(buff / buff_decrease)
    # Display the result
    st.write(f'It will take approximately {days_to_clear_buffer} working days to clear the BUFF.')
    