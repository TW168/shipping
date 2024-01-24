SELECT 
    BL_Number,
    Truck_Appointment_Date,
    sum(Pick_Weight) as 'lbs',
    sum(Number_of_Pallet) as 'plt',
    rpt_run_date
FROM
    ws_hub.ipg_ez
WHERE
    site = 'AMJK' AND Product_Group = 'SW'
        AND BL_Number NOT LIKE 'WZ%'
        AND Truck_Appointment_Date IS NOT NULL
        AND rpt_run_time = '16:00:00'
group by BL_Number, Truck_Appointment_Date, rpt_run_date;