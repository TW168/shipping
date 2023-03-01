use db3;
SELECT 
    Site,
    Product_Group,
    BL_Number,
    CSR,
    Truck_Appointment_Date,
    Ship_to_Customer,
    Ship_to_City,
    State,
    SUM(Pick_Weight) AS WGT,
    SUM(Number_of_Pallet) AS PLT,
    rpt_run_date,
    rpt_run_time,
    u.lat,
    u.lon
FROM
    ipg_ez i
left join us_cities u on i.State=u.state_id and i.Ship_to_City=u.city_ascii
where site= 'AMJK' and Product_Group= 'SW' and rpt_run_date = '2023-02-20' and rpt_run_time= '09:00:00' and BL_Number not like "WZ%" and Product_Code not like "INSTER%" and Truck_Appointment_Date is null
group by BL_Number, Site, Product_Group, CSR,
    Ship_to_Customer,
    Ship_to_City,
    State,
    Truck_Appointment_Date,
    rpt_run_date,
    rpt_run_time,
    lat,
    lon
order by State, Ship_to_City;