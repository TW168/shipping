stacker3_custom_made = """
select * from udclog
limit 10
"""

create_shipment_table = """ use ws_hub; 

use ws_hub;
CREATE TABLE ipg_ez (
	id INT PRIMARY KEY AUTO_INCREMENT,
    Site VARCHAR(50),
    BL_Number VARCHAR(50),
    Truck_Appointment_Date DATE,
    BL_weight FLOAT,
    Freight_Amount FLOAT,
    Truck_Appt_Time TIME,
    Pickup_Date DATE,
    State VARCHAR(50),
    Ship_to_City VARCHAR(50),
    Ship_to_Customer VARCHAR(50),
    Order_Number varchar(50),
    Order_Item int,
    CSR varchar(50),
    Freight_Term varchar(50),
    Require_Date DATE,
    Schedule_Date DATE,
    Unshipped_Weight int,
    Product_Code varchar(50),
    Pick_Weight FLOAT,
    Number_of_Pallet INTEGER,
    Pickup_by VARCHAR(50),
    Change_Date DATE,
    Carrier_ID VARCHAR(50),
    Arrange_by VARCHAR(50),
    Unit_Freight FLOAT,
    Waybill_Number VARCHAR(50),
    Sales_Code VARCHAR(50),
    Transportation_Code VARCHAR(50),
    transaction_type VARCHAR(50),
    Product_Group VARCHAR(50),
    rpt_run_date DATE,
    rpt_run_time TIME,
    file_name VARCHAR(50),
    uploaded_date_time DATETIME
);
"""

cfp_pallets = """
use cfp;
select indatetime, fpcpdt, pallet, ordno, orditm, quality, od, width, length, rolls, grswgt, tarwgt, filler, note from pallets
limit 10
"""

# insert new lat lon
# INSERT INTO `db3`.`us_cities`
# (
# `city_ascii`,
# `state_id`,

# `lat`,
# `lon`
# )
# VALUES
# ("Pewaukee",
# "WI",
# "43.054206",
# "-88.216903"

# );