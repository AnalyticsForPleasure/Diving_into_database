show databases;
create database Kusto_Detective_tasks;
use Kusto_Detective_tasks;


# enca -L none log_00000_new.csv
# sed 's/\r//' log_00000.csv > log_00000_new.csv

show tables;
use Kusto_Detective_season2;
show variables like "secure_file_priv";
show variables like "local_infile";

drop table DetectiveCases;

CREATE TABLE DetectiveCases (
	Time_stamp datetime,
    EventType TEXT,
    DetectiveId TEXT ,
    CaseId TEXT,
    Properties json
);


# Works well:
# replace "" to {}
LOAD DATA INFILE '/var/lib/mysql-files/log_00002_new.csv'
INTO TABLE DetectiveCases
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(Time_stamp, EventType,DetectiveId, CaseId, @Properties)
SET Properties = JSON_SET('{}', '$.Bounty', JSON_EXTRACT(@Properties, '$.Bounty'));


select * from DetectiveCases
limit 200;

