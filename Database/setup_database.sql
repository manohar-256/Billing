CREATE DATABASE IF NOT EXISTS billing_system;
USE billing_system;

-- Table for Inventory
CREATE TABLE IF NOT EXISTS raw_inventory (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    product_cat VARCHAR(100),
    product_subcat VARCHAR(100),
    stock INT,
    mrp DECIMAL(10, 2),
    cost_price DECIMAL(10, 2),
    vendor_phn VARCHAR(20)
);

-- Table for Employees
CREATE TABLE IF NOT EXISTS employee (
    emp_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    contact_num VARCHAR(20),
    address TEXT,
    aadhar_num VARCHAR(20),
    password VARCHAR(50),
    designation VARCHAR(50)
);

-- Table for Bills
CREATE TABLE IF NOT EXISTS bill (
    bill_no VARCHAR(50) PRIMARY KEY,
    date VARCHAR(50),
    customer_name VARCHAR(100),
    customer_no VARCHAR(20),
    bill_details TEXT
);

-- Insert a Default Admin User (Required to login for the first time)
-- Username: EMPAdmin, Password: password123
INSERT INTO employee (emp_id, name, contact_num, address, aadhar_num, password, designation)
VALUES ('EMPAdmin', 'Super Admin', '9999999999', 'Admin Office', '000000000000', 'password123', 'Admin')
ON DUPLICATE KEY UPDATE name=name;