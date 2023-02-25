import streamlit as st 
import pandas as pd 
from helper import connect_to_database


conn = connect_to_database('sakila_db')

qry = """ select * from actor """
df = pd.read_sql_query(qry, con=conn)
st.dataframe(df)
conn.close()