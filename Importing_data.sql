Riddle taken from detective kusto: ( Part 1 of the answer )

Imagine our agency as a buzzing beehive, like StackOverflow on steroids. We have a crazy number of cases popping up every day, each with a juicy bounty attached (yes, cold, hard cash!). And guess what? We've got thousands of Kusto Detectives scattered across the globe, all itching to pick a case and earn their detective stripes. But here's the catch: only the first detective to crack the case gets the bounty and major street cred!

So, your mission, should you choose to accept it, is to dig into the vast archives of our system operation logs from the legendary year 2022. You're on a quest to unearth the absolute legend, the detective with the biggest impact on our business—the one who raked in the most moolah by claiming bounties like a boss!

Feeling a bit rusty or want to level up your Kusto skills? No worries, my friend. We've got your back with the "Train Me" section. It's like a power-up that'll help you sharpen your Kusto-fu to tackle each case head-on. Oh, and if you stumble upon a mind-boggling case and need a little nudge, the "Hints" are there to save the day!

Now, strap on your detective hat, embrace the thrill, and get ready to rock this investigation. The fate of the "Most Epic Detective of the Year" rests in your hands!

Good luck, rookie, and remember to bring your sense of humor along for this wild ride!



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

select count(*)
from DetectiveCases;

# Works well:
# replace "" to {}
-- Here below I am adding and dumping the 3 csv files into the DetectiveCases table: 
#LOAD DATA INFILE '/var/lib/mysql-files/log_00000_new.csv'
#LOAD DATA INFILE '/var/lib/mysql-files/log_00001_new.csv'
LOAD DATA INFILE '/var/lib/mysql-files/log_00002_new.csv' 

INTO TABLE DetectiveCases
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(Time_stamp, EventType,DetectiveId, CaseId, @Properties)
SET Properties = JSON_SET('{}', '$.Bounty', JSON_EXTRACT(@Properties, '$.Bounty'));

# Dumping the entire data into a one table  
SELECT time_stamp, EventType, DetectiveId , CaseId , Properties FROM og_00002_new.csv
UNION ALL
SELECT time_stamp, EventType, DetectiveId , CaseId , Properties FROM og_00002_new.csv
UNION ALL
SELECT time_stamp, EventType, DetectiveId , CaseId , Properties FROM og_00002_new.csv;



select count(*)
from DetectiveCases
limit 5000;



-- SELECT JSON_EXTRACT(Properties, '$.Bounty') AS bounty_value
-- FROM DetectiveCases;


###############################################################################################
