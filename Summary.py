import streamlit as st
import pandas as pd 
from helper import connect_to_database
from datetime import datetime
import plotly.express as px

DB = 'db3_db'

st.set_page_config(page_title="Summary", page_icon="📰", layout='wide')
st.markdown("# Summary")




try:
    with st.container():
        
        conn = connect_to_database(DB)
        qry = """ select Site, BL_Number, Truck_Appointment_Date, State, Ship_to_City, Ship_to_Customer, CSR, Product_Code, Pick_Weight, Number_of_Pallet, Carrier_ID, Unit_Freight, rpt_run_date  FROM db3.ipg_ez """
        summary_df = pd.read_sql_query(qry, conn)

        Not_WZ_by_date_4PM_qry = """ SELECT  rpt_run_date, sum(Pick_Weight) as "Avail to ship" from db3.ipg_ez
                    where Site='AMJK' and Product_Group='SW' and BL_Number not like "WZ%" and Truck_Appointment_Date = rpt_run_date and rpt_run_time='16:00:00'
                    group by  rpt_run_date
                    order by  rpt_run_date;  """
        
        Not_WZ_by_date_9AM_qry = """ SELECT rpt_run_date, sum(Pick_Weight) as "Scheduled" FROM db3.ipg_ez
                                where Site='AMJK' and Product_Group='SW' and BL_Number not like "WZ%" and Truck_Appointment_Date is null and rpt_run_time='09:00:00'
                                group by rpt_run_date
                                order by rpt_run_date; """
        
        Not_WZ_by_date_4PM_df = pd.read_sql_query(Not_WZ_by_date_4PM_qry, conn)
        Not_WZ_by_date_9AM_df = pd.read_sql_query(Not_WZ_by_date_9AM_qry, conn)

        df = pd.merge(Not_WZ_by_date_9AM_df, Not_WZ_by_date_4PM_df, how= 'left', on="rpt_run_date")
        formatted_df = df.style.format({"Scheduled":"{:,.0f}", "Avail to ship":"{:,.0f}"})
        plot_df = formatted_df.data
        st.dataframe(formatted_df)

        fig = px.bar(plot_df, x="rpt_run_date", y=["Scheduled", "Avail to ship"], barmode='group', width=1200)
        st.plotly_chart(fig)

    # # End of day truck log
    # qry = """SELECT * FROM ezs WHERE rpt_run_date BETWEEN '{begin}' AND '{end}' and SITE='{site}' and `Product Group`='{group}' and rpt_run_time='{hour}'""".format(begin=begin, end=end, site=site, group=group, hour=hour)
    # data = pd.read_sql_query(qry, conn)
except Exception as e:
    print (e)
    st.warning(f"No Data Available")
