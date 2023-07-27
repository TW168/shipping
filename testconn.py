import streamlit as st

st.write("Test Experimental Database Connection")

conn = st.experimental_connection('ws_hub', type='sql')

# View the connection contents.
conn

df = conn.query("select * from ipg_ez limit 100")
st.dataframe(df)