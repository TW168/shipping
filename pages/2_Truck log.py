import streamlit as st
import pandas as pd
# from sqlalchemy import create_engine

# Connect to the database
conn = st.experimental_connection('ws_hub', type='sql')

conn
# Function to insert data into the table
def insert_data(data):
    conn.execute('''
            INSERT INTO truck_log (schd_date, aal, cal, charger, chr, drake, geodis, giltner, hellman, ip, jbht, landair, neon, pdi, qtbk, traf, saia, xpo)
            VALUES (:schd_date, :aal, :cal, :charger, :chr, :drake, :geodis, :giltner, :hellman, :ip, :jbht, :landair, :neon, :pdi, :qtbk, :traf, :saia, :xpo)
        ''', data)



            

