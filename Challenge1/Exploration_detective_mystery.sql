-- Riddle taken from detective kusto: ( Part 2 of the answer )

-- Imagine our agency as a buzzing beehive, like StackOverflow on steroids. We have a crazy number of cases popping up every day, each with a juicy bounty attached (yes, cold, hard cash!). And guess what? We've got thousands of Kusto Detectives scattered across the globe, all itching to pick a case and earn their detective stripes. But here's the catch: only the first detective to crack the case gets the bounty and major street cred!

-- So, your mission, should you choose to accept it, is to dig into the vast archives of our system operation logs from the legendary year 2022. You're on a quest to unearth the absolute legend, the detective with the biggest impact on our business—the one who raked in the most moolah by claiming bounties like a boss!

-- Feeling a bit rusty or want to level up your Kusto skills? No worries, my friend. We've got your back with the "Train Me" section. It's like a power-up that'll help you sharpen your Kusto-fu to tackle each case head-on. Oh, and if you stumble upon a mind-boggling case and need a little nudge, the "Hints" are there to save the day!

-- Now, strap on your detective hat, embrace the thrill, and get ready to rock this investigation. The fate of the "Most Epic Detective of the Year" rests in your hands!

-- Good luck, rookie, and remember to bring your sense of humor along for this wild ride!


# CASE_0891321 - First row of 42 rows - case have been close at trasacttion number 21
# CASE_0891345 - First row of 29 rows - case have been close at trasacttion number 16
# CASE_0892368 - First row of 27 rows - case have been close at trasacttion number 16
# CASE_0892441 - First row of 82 rows - case have been close at trasacttion number 42

# Step Num 1 : extracting the bounty value from the properties in order to count the sum of bounties, filtering rows which satisfied the constraint where EventType = 'CaseOpened'

SELECT  EventType , CaseId , JSON_EXTRACT(Properties, '$.Bounty') AS bounty_value
FROM DetectiveCases
WHERE EventType = 'CaseOpened';


#  Step Num 2 : Creating table number 2
Select EventType,  CaseId , DetectiveId
from DetectiveCases
WHERE EventType = 'CaseSolved';


## Step Num 3 : Create a temporary table named 'temp_table_for_bounty'
CREATE TEMPORARY TABLE temp_table_for_bounty AS
SELECT  EventType , CaseId , JSON_EXTRACT(Properties, '$.Bounty') AS bounty_value
FROM DetectiveCases
WHERE EventType = 'CaseOpened';

Select *
from temp_table_for_bounty;


## Step Num 4 : Create a temporary table named 'temp_table_for_case_solved'
CREATE TEMPORARY TABLE temp_table_for_case_solved AS
SELECT MIN(Time_stamp) AS first_CaseSolved, CaseId
FROM DetectiveCases
WHERE EventType = 'CaseSolved'
GROUP BY CaseId ;

Select *
from temp_table_for_case_solved;


## Step Num 5 : Creating a temporary table named - temp_table_case_solved_by_first_Detec ( with 3 fields : first_appearance , CaseId , DetectiveId )

CREATE TEMPORARY TABLE temp_table_case_solved_by_first_Detec AS
SELECT DetectiveCases.Time_stamp AS first_appearance, DetectiveCases.CaseId, DetectiveCases.DetectiveId
FROM   DetectiveCases
INNER JOIN temp_table_for_case_solved ON DetectiveCases.CaseId = temp_table_for_case_solved.CaseId
AND DetectiveCases.Time_stamp = temp_table_for_case_solved.first_CaseSolved;
           
select *
from temp_table_case_solved_by_first_Detec;

## Step Num 6 : applying an inner join between the 2 temporary tables + I added the "order by" in order to see the number of bounties each Detective have

Select temp_table_case_solved_by_first_Detec.DetectiveId , temp_table_case_solved_by_first_Detec.CaseId ,  temp_table_for_bounty.bounty_value
from temp_table_for_bounty
inner join temp_table_case_solved_by_first_Detec
On temp_table_for_bounty.CaseId = temp_table_case_solved_by_first_Detec.CaseId
ORDER BY temp_table_case_solved_by_first_Detec.DetectiveId;



## Step Num 7 : adding a inner join between the 2 temporary tables + I added the order by in order to see the number of bounties each Detective have + adding at the end a new temporary table

CREATE TEMPORARY TABLE temp_table_solve_cases_with_bounty_values AS
Select temp_table_case_solved_by_first_Detec.DetectiveId , temp_table_case_solved_by_first_Detec.CaseId ,  temp_table_for_bounty.bounty_value
from temp_table_for_bounty
inner join temp_table_case_solved_by_first_Detec
On temp_table_for_bounty.CaseId = temp_table_case_solved_by_first_Detec.CaseId
ORDER BY temp_table_case_solved_by_first_Detec.DetectiveId;


select *
from temp_table_solve_cases_with_bounty_values;


## Step Num 8 : applying group by + order by - for see the bounties by using aggregation sum function
select Detectiveid , sum(bounty_value) As sum_bounties_for_each_detective
from temp_table_solve_cases_with_bounty_values
group by Detectiveid
order by sum_bounties_for_each_detective desc;



## Step Num 8 : Dropping the temporary tables
DROP TABLE IF EXISTS temp_table_for_bounty;
DROP TABLE IF EXISTS temp_table_case_solved_by_first_Detec;
DROP TABLE IF EXISTS temp_table_solve_cases_with_bounty_values;
