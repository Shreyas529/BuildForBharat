CREATE TABLE PINCODE_MERCHANT (
    PINCODE INT,
    MERCHANT_ID VARCHAR(40),
    Primary Key (PINCODE, MERCHANT_ID)
);
-- Run copy_data_to_csv and generate the csv files to copy data
\copy PINCODE_MERCHANT From 'path/to/merchants.csv' DELIMITER ',' CSV;