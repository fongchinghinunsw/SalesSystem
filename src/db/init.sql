CREATE DATABASE sales;

CREATE USER 'sales'@'%' IDENTIFIED BY 'SECURE_SALES_PWD';
GRANT * ON sales.* TO 'sales'@'%';