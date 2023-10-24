-- This view fetches distinct shipment from ipg_ez table
-- data from AmTopp Pickup Report for Shipping, daily email
-- using Truck_Appointment_Date, BL_number, MAX(rpt_run_date) AS max_rpt_run_date
-- and rpt_run_time = '16:00:00'
-- This view is similar to  AS400 Stretch Film Daily Shipment Log 
CREATE VIEW v_my_stretch_film_daily_shipment_log AS
SELECT 
    lt.Truck_Appointment_Date,
    lt.BL_Number,
    rt.site,
    rt.Product_Group,
    rt.Product_Code,
    rt.id,
    rt.Freight_Amount,
    rt.State,
    rt.Ship_to_City,
    rt.Ship_to_Customer,
    rt.Order_Number,
    rt.Order_Item,
    rt.Pick_Weight,
    rt.Number_of_Pallet,
    rt.Carrier_ID,
    rt.Pickup_by,
    rt.Arrange_by,
    rt.Waybill_Number
FROM (
    SELECT Truck_Appointment_Date, BL_number, MAX(rpt_run_date) AS max_rpt_run_date
    FROM ipg_ez
    WHERE Truck_Appointment_Date IS NOT NULL AND rpt_run_time = '16:00:00'
    GROUP BY Truck_Appointment_Date, BL_number
) AS lt
LEFT JOIN ipg_ez AS rt
ON lt.Truck_Appointment_Date = rt.Truck_Appointment_Date
AND lt.BL_number = rt.BL_Number
AND lt.max_rpt_run_date = rt.rpt_run_date
WHERE rt.rpt_run_time = '16:00:00';

