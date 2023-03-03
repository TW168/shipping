
-- Ship to customer based on rpt run date 16:00hrs and truck appointment date 
SELECT Truck_Appointment_Date, Product_Group , Site,  sum(Pick_Weight) as 'Ship to Customer' FROM ipg_ez
            where rpt_run_date= '2023-03-03' and rpt_run_time='16:00:00' and Truck_Appointment_Date= '2023-03-06' and Product_Code not like "INSER%" and Ship_to_Customer not in ('INTEPLAST GROUP CORP. (AMTOPP)', 'INTEPLAST GROUP CORP. (AMTOPP)')
            group by Truck_Appointment_Date, Product_Group, Site
            order by Truck_Appointment_Date, product_Group, Site;



-- Ship to Remington based on rpt run date 16:00hrs and truck appointment date 
SELECT Truck_Appointment_Date , Product_Group as 'Group', Site,  sum(Pick_Weight) as 'Consignment to Remington' FROM ipg_ez
            where rpt_run_date= '2023-03-03' and rpt_run_time='16:00:00' and Truck_Appointment_Date= '2023-03-06' and Product_Code not like "INSER%" and Ship_to_Customer="INTEPLAST GROUP CORP. (AMTOPP)"
            group by Truck_Appointment_Date,Product_Group, Site
            order by product_Group, Site;