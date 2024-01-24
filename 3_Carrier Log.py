import streamlit as st
import pandas as pd 

st.set_page_config(page_title="Warship-Carrier", page_icon="📰", layout='wide')
st.title("Stretch Film Carrier Log")

# Connect to the database
conn = st.experimental_connection("ws_hub", type="sql")

with st.expander('Carrier'):
    topcol1, topcol2, topcol3, topcol4, topcol5 = st.columns(5)
    with topcol1:
        my_date = st.date_input('Date:')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        aal = st.number_input('All American Logistics(AAL)',min_value=0)
        cal = st.number_input('California Freight(CAL. FRT.)',min_value=0)
        chr = st.number_input('C.H. Robinson(CHR)',min_value=0)
        drake = st.number_input('DRAKE Transport(DRAKE)',min_value=0)
        giltner = st.number_input('Giltner Transportation(GILTNER)',min_value=0)
    with col2:
        geodis = st.number_input('GEODIS',min_value=0)
        hellman = st.number_input('Hellmann Worldwide Logistics(HELLMAN)',min_value=0)
        ip_truck = st.number_input('IP-TRUCK',min_value=0)
        jb = st.number_input('J.B. Hunt(JBHT-R)',min_value=0)
        pdi = st.number_input('PRIORITY DISTRIBUTION INC.(PDI)',min_value=0)
    with col3:
        qtback = st.number_input('Quarterback Transportation(QTBK)',min_value=0)
        traffix = st.number_input('Traffix(TRAF)',min_value=0)
        charger = st.number_input('Charger Logistics(CHARGER)',min_value=0)
        landair = st.number_input('LANDAIR',min_value=0)
        neon = st.number_input('NEON',min_value=0)
    with col4:
        saia = st.number_input('SAIA', min_value=0)
        xpo = st.number_input('XPO', min_value=0)
    but1 = st.button('Update')
    
st.write(conn)
