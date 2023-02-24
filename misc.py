import streamlit as st 
import pandas as pd 
from helper import connect_to_database
from sql_qry import stacker3_custom_made



conn = connect_to_database('cfpwh_db')


df = pd.read_sql_query(stacker3_custom_made, con=conn)
st.dataframe(df)