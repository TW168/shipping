stacker3_custom_made = """
select * from udclog
limit 10
"""

create_shipment_table = """ use ws_hub; 

CREATE TABLE shipment (
    site VARCHAR(50),
    bl_number VARCHAR(50),
    truck_appointment_date DATE,
    bl_weight FLOAT,
    freight_amount FLOAT,
    truck_appt_time TIME,
    pickup_date DATE,
    state VARCHAR(50),
    ship_to_city VARCHAR(50),
    ship_to_customer VARCHAR(50),
    pick_weight FLOAT,
    num_pallet INTEGER,
    pickup_by VARCHAR(50),
    change_date DATE,
    carrier_id VARCHAR(50),
    arrange_by VARCHAR(50),
    unit_freight FLOAT,
    waybill_number VARCHAR(50),
    sales_code VARCHAR(50),
    transportation_code VARCHAR(50),
    transaction_type VARCHAR(50),
    product_group VARCHAR(50),
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