import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Constants
TRANSPORTATION_DATA_FILE_PATH = r"D:\dev\shipping\shipping\raw\Transp_Type-2023-08-email - Copy.xlsx"
TRANSPORTATION_SHEET = "trans_pre"
WAREHOUSE_DATA_PATH = r"D:\Shipping_Daily_Report\1-DAILY_DATA_AUTO_WAREHOUSE_2023.xlsx"
WAREHOUSE_SHEET_NAME = "Sheet1"
FREIGHT_HISTORY = r"D:\dev\shipping\shipping\raw\Freight_History.xlsx"

# Page configuration
st.set_page_config(page_title="Warship-Presentation", page_icon="🚚", layout='wide')
st.title("Welcome to Warehouse and Shipping")

def file_exists(filepath):
    """Check if a file exists at a given filepath."""
    return os.path.isfile(filepath)

def load_data():
    """Load volume, freight, and trans_type data from Excel files."""
    if not file_exists(TRANSPORTATION_DATA_FILE_PATH) or \
       not file_exists(WAREHOUSE_DATA_PATH) or \
       not file_exists(FREIGHT_HISTORY):
        st.error("One or more data files not found.")
        return None, None, None

    trans_pre_df = pd.read_excel(TRANSPORTATION_DATA_FILE_PATH, sheet_name=TRANSPORTATION_SHEET)
    warehouse_df = pd.read_excel(WAREHOUSE_DATA_PATH, sheet_name=WAREHOUSE_SHEET_NAME)
    freight_history = pd.read_excel(FREIGHT_HISTORY, sheet_name="Sheet1")
    return trans_pre_df, warehouse_df, freight_history

def preprocess_data(df, value_col_name, product='SW'):
    """Preprocess the data to filter by product and reformat the DataFrame."""
    filtered_df = df[df['Product'] == product].copy()
    filtered_df['Group'] = filtered_df['Product']
    melted_df = pd.melt(filtered_df, id_vars=['Group'], var_name='Date', value_name=value_col_name)
    melted_df['Date'] = pd.to_datetime(melted_df['Date'])
    return melted_df

# Load data
trans_pre_df, warehouse_df, freight_history = load_data()

# Visualizations inside expanders
def display_people():
    with st.expander('People', expanded=False):
        st.image("images\warship_people.jpg", caption="Wareshouse and Shipping Crew", use_column_width=True)
        st.write('FYI:')
        st.write('1. We are shipping every last Saturday of every month')
        st.write('2. The last week of every month, 10 hrs night shift')

def display_work():
    with st.expander('Work', expanded=False):
        st.image("images\Workship_flow.jpg", caption="Wareshouse and Shipping Workflow")

def display_numbers(trans_pre_df, warehouse_df, freight_history):
    with st.expander('Numbers', expanded=False):
        # Shipping volume and freight
        # Filter data to only show rows where Group is 'SW'
        df = freight_history[freight_history['Group'] == 'SW']
        # Create line chart
        fig = go.Figure()
        # Plotting Freight($) on y-axis (y1)
        fig.add_trace(go.Scatter(x=df['YYYY-MM'], y=df['Freight($)'], mode='lines+markers', name='Freight($)', line=dict(color='green'), yaxis='y1'))
        # Plotting Shipped WT(lbs) on a secondary y-axis (y2)
        fig.add_trace(go.Scatter(x=df['YYYY-MM'], y=df['Volume(lbs)'], mode='lines+markers', name='Volume(lbs)', line=dict(color='blue'), yaxis='y2'))
        # Layout adjustments for the secondary y-axis
        fig.update_layout(
            title='Shipping Volume(lbs) and Freight($)',
            yaxis=dict(title='Freight($)'),
            yaxis2=dict(title='Volume(lbs)', overlaying='y', side='right')
        )
        st.plotly_chart(fig, use_container_width=True)
        # Caption
        st.caption('Data source: AMJK Frt cost breakdown by plants')

        # Transpose the DataFrame
        df_transposed = trans_pre_df.transpose()
        # Set the first column as the index
        df_transposed.columns = df_transposed.iloc[0]
        df_transposed = df_transposed.iloc[1:]
        # Assuming df is your DataFrame and the index is of type 'datetime'
        if not isinstance(df_transposed.index, pd.DatetimeIndex):
            df_transposed.index = pd.to_datetime(df_transposed.index)
        # Extract year and month from the index and reset the index to create new columns
        df_transposed['Year'] = df_transposed.index.year
        df_transposed['Month'] = df_transposed.index.month
        df_transposed.reset_index(drop=True, inplace=True)
        # Group by Year and Month
        grouped_df = df_transposed.groupby(['Year', 'Month']).sum().reset_index()
        # Convert the values to percentage
        for column in grouped_df.columns[2:]:
            grouped_df[column] = grouped_df[column] * 100
        # Create the bar plot
            fig = px.bar(
            grouped_df, 
            x="Month", 
            y=grouped_df.columns[2:].tolist(), 
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={'value':'Percentage'},
            animation_frame='Year',
            title='Transportation Type',
            barmode='stack'
        )
        st.plotly_chart(fig, use_container_width=True)
        # Caption
        st.caption('Data source: Monthly Unit Freight Cost')

        # Warehose data
        # Convert the 'date_column' to datetime dtype
        warehouse_df['Date'] = pd.to_datetime(warehouse_df['Date'])
        warehouse_df['YMD'] = warehouse_df['Date'].dt.strftime('%Y-%m-%d')
        # Extract year and month from the 'Date' column and create new columns
        warehouse_df['Year'] = warehouse_df['Date'].dt.year
        warehouse_df['Month'] = warehouse_df['Date'].dt.month
        # Group by year and month, then aggregate
        grouped_df = warehouse_df.groupby(['Year', 'Month']).agg({
            'Pallet Entry': 'sum',
            'Pallet Exit': 'sum',
            'Pallets Shipped': 'sum'
        }).reset_index()
        # Formatting the columns to have comma separated numbers
        grouped_df['Pallet Entry'] = grouped_df['Pallet Entry'].apply(lambda x: "{:,.0f}".format(x))
        grouped_df['Pallet Exit'] = grouped_df['Pallet Exit'].apply(lambda x: "{:,.0f}".format(x))
        grouped_df['Pallets Shipped'] = grouped_df['Pallets Shipped'].apply(lambda x: "{:,.0f}".format(x))
        # Create a combined year-month column for visualization purposes
        grouped_df['Year-Month'] = grouped_df['Year'].astype(str) + '-' + grouped_df['Month'].astype(str).str.zfill(2)

        # Visualize aggregated data
        fig = go.Figure()

        # Line charts for Pallet Entry, Pallet Exit, and Pallets Shipped
        fig.add_trace(go.Scatter(x=grouped_df['Year-Month'], y=grouped_df['Pallet Entry'], mode='lines+markers', name='Pallet Entry', line=dict(color='teal')))
        fig.add_trace(go.Scatter(x=grouped_df['Year-Month'], y=grouped_df['Pallet Exit'], mode='lines+markers', name='Pallet Exit', line=dict(color='coral')))
        fig.add_trace(go.Scatter(x=grouped_df['Year-Month'], y=grouped_df['Pallets Shipped'], mode='lines+markers', name='Pallets Shipped', line=dict(color='black')))

        # Update layout
        fig.update_layout(
            yaxis=dict(title='Pallet Counts'),
            title='Pallet Entry, Exit, and Shipped',
            xaxis=dict(title='Year-Month')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.table(grouped_df)
        st.caption("Data Source:1-DAILY_DATA_AUTO_WAREHOUSE ")
        

# Call the display functions
display_people()
display_work()
display_numbers(trans_pre_df, warehouse_df, freight_history)
