import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
from helper import extract_EZ_rpt_date_time, connect_to_database, clean_uploaded_IPG_EZ, avail_to_ship, convert_df_to_csv

DB = 'db3_db'

st.set_page_config(page_title="TSR Prep", page_icon="🚚", layout='wide')

st.markdown("# TSR Prep")
st.sidebar.header("TSR Prep")
st.write(
    """ Update twice a day approx. 8AM and 4PM CST """
)

with st.container():
    with st.expander("Upload", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader('Choose a file (e.g. AmTopp Current Pickup Detail Report as of yyyy-m-dd H#9M#0.xlsx)', accept_multiple_files=False, type=["xlsx", "xls"], key="uploaded_file_key", help="This app only accept Excel file from IPG EZ Report / Inteplast Management Improvement <ezreport@inteplast.com>" )
        with col2:
            pass

        # check if file has already been uploaded
        if uploaded_file is not None:
            file_name = uploaded_file.name
            file_size = uploaded_file.size
            conn = connect_to_database(DB)
            result = conn.execute("SELECT * FROM ipg_ez WHERE file_name = %s AND file_size = %s", (file_name, file_size)).fetchone()

            if result:
                st.error("This file has already been uploaded.")
            else:
                # extract file data and process the file
                rpt_date_time = extract_EZ_rpt_date_time(file_name)
                rpt_run_date = datetime.strptime(rpt_date_time[0], "%Y-%m-%d").date()
                rpt_run_time = datetime.strptime(rpt_date_time[1], "%H:%M").time()
                current_time = datetime.now()
                df = pd.read_excel(uploaded_file)
                cleaned_df = clean_uploaded_IPG_EZ(df,rpt_run_date,rpt_run_time, file_name, file_size, current_time)
                #Append the data to the MySQL table
                cleaned_df['file_name'] = file_name
                cleaned_df['file_size'] = file_size
                cleaned_df.to_sql('ipg_ez', con=conn, if_exists='append', index=False)
                conn.close()
    
with st.container():
    conn = connect_to_database(DB)
    with st.expander("Ship list", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            # Extract distinct site from ipg_ez convert result to list and display items in select box
            site_result = conn.execute("SELECT distinct Site FROM ipg_ez;").fetchall()
            items = [str(item[0]) for item in site_result]
            selected_site = st.selectbox("Choose a Site", items)
        
            # Extract distinct group from ipg_ez, convert result to list and display items in select box
            group_result = conn.execute("select distinct Product_Group from ipg_ez;").fetchall()
            items = [str(item[0]) for item in group_result]
            selected_group = st.selectbox("Choose a Group", items)
        with col2:
            # Use calendar to repesent  rpt_run_date from ipg_ez
            selected_date = st.date_input("Choose a date" )
            # Extract distinct rpt_run_time from ipg_ez, convert result to list and display items in select box
            # rpt_time_result = conn.execute("select distinct rpt_run_time from ipg_ez;").fetchall()
            # items = [str(item[0]) for item in rpt_time_result] 
            selected_time = st.selectbox("Choose a time", options=["09:00:00", "16:00:00"])
            
        avail_to_ship_df= avail_to_ship(selected_site, selected_group, selected_date, selected_time)
        st.dataframe(avail_to_ship_df)

        
        st.download_button(
        label="Download",
        data=convert_df_to_csv(avail_to_ship_df),
        file_name='TSR_Prep_List.csv',
        mime='text/csv',
        )


try:
    with st.container():
        with st.expander('Map', expanded=True):
            avail_to_ship_df["hover_text"] = (
                                            ""
                                            + avail_to_ship_df["BL_Number"].astype(str)
                                            + "<br>PLT: "
                                            + avail_to_ship_df["PLT"].astype(str)
                                            + "<br>"
                                            + avail_to_ship_df["Ship_to_Customer"].astype(str)
            )
            px.set_mapbox_access_token(open(".mapbox_token").read())
            fig = px.scatter_mapbox(avail_to_ship_df, lat=avail_to_ship_df["lat"], lon=avail_to_ship_df["lon"], hover_name="hover_text", size="WGT", size_max=15, zoom=4, center={"lat": 37.09054375, "lon": -96.6249135},
                    width=1200, height=750, title="BL Number Location")
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r":0, "t":50, "l":0, "b":10})

            st.plotly_chart(fig)
except Exception as e:
    print(e)
    st.warning(f"No data available")



st.write('outside of container')


