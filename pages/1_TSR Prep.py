import streamlit as st
from datetime import datetime
import pandas as pd
from helper import extract_EZ_rpt_date_time, connect_to_database, clean_uploaded_IPG_EZ


st.set_page_config(page_title="TSR Prep", page_icon="📈", layout='wide')

st.markdown("# TSR Prep")
st.sidebar.header("TSR Prep")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

with st.container():
    with st.expander("upload", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader('Choose a file ', accept_multiple_files=False, type=["xlsx", "xls"], key="uploaded_file_key" )
        with col2:
            st.write('Upload the daily IPG/EZ from email')

        # check if file has already been uploaded
        if uploaded_file is not None:
            file_name = uploaded_file.name
            file_size = uploaded_file.size
            conn = connect_to_database('db3_db')
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
    

            

st.write('outside of container')





# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
# st.button("Re-run")