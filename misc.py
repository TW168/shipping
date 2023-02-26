import streamlit as st 
import pandas as pd 
from helper import connect_to_database

DB='db3_db'
conn = connect_to_database(DB)

qry = """ select * from ipg_ez """
df = pd.read_sql_query(qry, con=conn)
st.dataframe(df)
conn.close()