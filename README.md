# Diving_into_database
MySQL_Workshop




CREATE DATABASE investigation_july_2023_db;

use investigation_july_2023_db;

CREATE TABLE investigation_july_2023 (
	date_hour_log_on varchar(21),
    category_case VARCHAR(300),
    code_description VARCHAR(30) ,
    case_number VARCHAR(20)
	);

# 2022-11-07 00:00:00"
LOAD DATA INFILE 'C:\\MySQL_task\\log_00000.csv'
INTO TABLE investigation_july_2023
FIELDS TERMINATED BY ',';

LOAD DATA INFILE 'C:\\MySQL_task\\log_00001.csv'
INTO TABLE investigation_july_2023
FIELDS TERMINATED BY ',';

LOAD DATA INFILE 'C:\\MySQL_task\\log_00002.csv'
INTO TABLE investigation_july_2023
FIELDS TERMINATED BY ',';


select *
from investigation_july_2023;
