from sqlalchemy import create_engine
import configparser
from datetime import time
from datetime import datetime
import re
import pandas as pd
import streamlit as st





DB= 'ws_hub_db'

def connect_to_database(section="DEFAULT", dbms="mysql"):
    """
    Connect to a database using connection information from a config file.

    Parameters:
        section (str): The name of the section in the config file that contains the connection information.
        dbms (str): The name of the database management system (DBMS) to use (default is 'mysql').

    Returns:
        sqlalchemy.engine.Connection: A connection object that can be used to execute SQL queries.

    Raises:
        ValueError: If the specified section is not found in the config file.
    """
    config = configparser.ConfigParser()
    config.read("config.py")
    if section not in config.sections():
        raise ValueError(f"Section {section} not found in config.py")

    # Get the connection information from the specified section
    user = config[section]["user"]
    password = config[section]["password"]
    host = config[section]["host"]
    port = int(config[section]["port"])
    database = config[section]["database"]

    # Create a connection string using sqlalchemy and the specified DBMS
    connection_string = f"{dbms}+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    # Create an engine object with the connection string
    engine = create_engine(connection_string)
    # Test the connection by executing a simple query
    conn = engine.connect()
    print(f"Successfully connected to {dbms.upper()} database: {database}")

    return conn


def extract_hour(filename):
    """
    Extracts the hour value from a filename in the format "AmTopp Current Pickup Detail Report as of yyyy-mm-dd H#M#.xlsx".

    Parameters:
    filename (str): A string representing the filename.

    Returns:
    datetime.time: The hour value extracted from the filename between the 'H' and 'M' characters, as a time object.

    Example:
    >>> extract_hour("AmTopp Current Pickup Detail Report as of 2023-2-24 H9M0.xlsx")
    9
    """
    start_index = filename.find("H") + 1
    end_index = filename.find("M")
    hour = int(filename[start_index:end_index])
    return time(hour=hour, minute=0, second=0)


def extract_EZ_rpt_date_time(file_name):
    """
    Extracts the date and time information from a file name that matches the
    expected pattern.
    "AmTopp Current Pickup Detail Report as of yyyy-mm-dd H#M#.xlsx"

    Args:
        file_name (str): The name of the file to extract information from.

    Returns:
        A tuple containing the extracted date and time information in the
        format (date, time), where date is a string in the format 'YYYY-MM-DD'
        and time is a string in the format 'H:MM'.

        If the file name does not match the expected pattern, returns None.
    """
    pattern = r"AmTopp Current Pickup Detail Report as of (\d{4}-\d{1,2}-\d{1,2}) H(\d{1,2})M(\d{1,2})\.xlsx"
    match = re.search(pattern, file_name)
    if match:
        date = match.group(1)
        time = f"{match.group(2)}:{match.group(3)}"
        return (date, time)
    else:
        return None


def clean_uploaded_IPG_EZ(
    df, rpt_run_date, rpt_run_time, file_name, file_size, current_time
):
    """
    Cleans and pre-processes a pandas DataFrame containing IPG/EZ data.

    Parameters:
    df (pandas.DataFrame): A DataFrame containing IPG/EZ data.
    rpt_run_date (datetime.date): The date the IPG/EZ report was run.
    rpt_run_time (datetime.time): The time the IPG/EZ report was run.
    file_name (str): The name of the file that the data was extracted from.
    file_size (int): The size of the file that the data was extracted from.
    current_time (datetime.datetime): The current time.

    Returns:
    pandas.DataFrame: A cleaned and pre-processed DataFrame.

    """
    # Drop the last column
    last_column_name = df.columns[-1]
    df = df.drop(columns=[last_column_name])
    # Select rows where 'SITE' column is not None
    df = df[df["SITE"].notna()]
    # Define the format string for the date columns
    date_format = "%y/%m/%d"
    # Convert date columns to the appropriate date type
    date_columns = [
        "Truck Appointment Date (YY/MM/DD)",
        "PickUp Date (YY/MM/DD)",
        "Require Date (YY/MM/DD)",
        "Schedule Date (YY/MM/DD)",
        "Change Date (YY/MM/DD)",
    ]
    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column], format=date_format, errors="coerce"
        ).dt.date
    # Add the date and time information from the filename and uploaded file to the DataFrame
    df["rpt_run_date"] = rpt_run_date
    df["rpt_run_time"] = rpt_run_time
    df["file_name"] = file_name
    df["file_size"] = file_size
    df["uploaded_date_time"] = datetime.now()
    # Rename columns
    df = df.rename(
        columns={
            "B/L Number": "BL_Number",
            "Truck Appointment Date (YY/MM/DD)": "Truck_Appointment_Date",
            "B/L Weight (LB)": "BL_Weight",
            "Freight Amount ($)": "Freight_Amount",
            "Truck Appt. Time": "Truck_Appt_Time",
            "PickUp Date (YY/MM/DD)": "Pickup_Date",
            "State": "State",
            "Ship to City": "Ship_to_City",
            "Ship to Customer": "Ship_to_Customer",
            "Order Number": "Order_Number",
            "Order Item": "Order_Item",
            "CSR": "CSR",
            "Freight Term": "Freight_Term",
            "Require Date (YY/MM/DD)": "Require_Date",
            "Schedule Date (YY/MM/DD)": "Schedule_Date",
            "Unshipped Weight (Lb)": "Unshipped_Weight",
            "Product Code": "Product_Code",
            "Pick Weight (Lb)": "Pick_Weight",
            "Number of Pallet": "Number_of_Pallet",
            "Pickup By": "Pickup_By",
            "Change Date (YY/MM/DD)": "Change_Date",
            "Carrier ID": "Carrier_ID",
            "Arrange By": "Arrange_By",
            "Unit Freight (cent/Lb)": "Unit_Freight",
            "Waybill Number": "Waybill_Number",
            "Sales Code": "Sales_Code",
            "Transportation Code": "Transportation_Code",
            "Transaction Type": "Transaction_Type",
            "Product Group": "Product_Group",
        }
    )
    return df


def avail_to_ship(site, group, run_date, run_time):
    conn = connect_to_database(DB)
    qry_available_ship_list = """ 
    SELECT Site, BL_Number, CSR, Truck_Appointment_Date, Ship_to_Customer, Ship_to_City, State, SUM(Pick_Weight) AS WGT, SUM(Number_of_Pallet) AS PLT, u.lat, u.lon
    FROM ipg_ez i
    left join us_cities u on i.State=u.state_id and i.Ship_to_City=u.city_ascii
    where Site= %s and Product_Group= %s and BL_Number not like "WZ%" and rpt_run_date = %s and rpt_run_time= %s and  Product_Code not like '%INSER%' and Truck_Appointment_Date is null
    group by BL_Number, Site, CSR,
        Ship_to_Customer,
        Ship_to_City,
        State,
        Truck_Appointment_Date,
        lat,
        lon
    order by State, Ship_to_City;
    """
    # execute the query with the selected user inputs and convert the result to a DataFrame
    avail_to_ship_df = pd.read_sql_query(qry_available_ship_list, conn, params=[site, group, run_date, run_time])
    #print (avail_to_ship_df)
    return avail_to_ship_df



def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def ship_tomorrow(rpt_date, truck_dt):
    conn = connect_to_database(DB, dbms='mysql')
    qry = """ SELECT Product_Group, Site,  sum(Pick_Weight), sum(Number_of_Pallet) FROM ipg_ez
            where rpt_run_date= %s and rpt_run_time='16:00:00' and Truck_Appointment_Date= %s and Product_Code not like "INSER%"
            group by Product_Group, Site
            order by product_Group, Site;"""
    ship_tomorrow = pd.read_sql(qry, conn, params=[rpt_date, truck_dt])

    return ship_tomorrow
