show databases;
create database Kusto_Detective_tasks;
use Kusto_Detective_tasks;


# enca -L none log_00000_new.csv
# sed 's/\r//' log_00000.csv > log_00000_new.csv

show tables;
use Kusto_Detective_season2;
show variables like "secure_file_priv";
show variables like "local_infile";

drop table consumption_df;

-- Dealing with the first table of the detective kusto challenge -  "consumption_df" :
CREATE TABLE consumption_df
(
Time_stamp datetime,
    EventType TEXT,
    HouseholdId TEXT,
    Consumed TEXT
);


drop table cost_df;

-- Dealing with the second table of the detective kusto challenge -  "Reference table" :
CREATE TABLE cost_df
(
MeterType TEXT,
    Unit TEXT,
    Cost double
);

INSERT INTO cost_df
(MeterType, Unit, Cost)
Values ('Water','Liter','0.001562'),  
  ('Electricity','kwH','0.3016');



select *
from consumption_df;
