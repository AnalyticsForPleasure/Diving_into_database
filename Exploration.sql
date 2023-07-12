###############################################################################################
# Path 1: Convertion table number 1

SELECT CaseId, Properties 
FROM DetectiveCases 
WHERE EventType = 'CaseOpened';

# Path 2: Convertion table number 2

Select CaseId,  EventType
from DetectiveCases
WHERE EventType = 'CaseSolved';
#####################################################################################################

# Finding the caseid which have been solved at the last transaction - by adding the max over the time_stamp 
# In other words, the last transaction recorded for that case is 'CaseSolved'.

SELECT CaseId 
FROM DetectiveCases
WHERE EventType = 'CaseSolved'
GROUP BY CaseId
HAVING MAX(Time_stamp) = (SELECT MAX(Time_stamp)
						  FROM DetectiveCases
						  WHERE EventType = 'CaseSolved'
						  GROUP BY CaseId);



#####################################################################################################

### Here I used the same subquery I wrote -The only thing I added  is the output "DetectiveId" + Entered 'DetectiveId' into the group of the outer query

# First approach : Retrieving CaseId, DetectiveId - by using subquary + Having  

SELECT CaseId, DetectiveId
FROM DetectiveCases
WHERE EventType = 'CaseSolved'
GROUP BY CaseId , DetectiveId
HAVING MAX(Time_stamp) = (SELECT MAX(Time_stamp)
						  FROM DetectiveCases
						  WHERE EventType = 'CaseSolved'
						  GROUP BY CaseId);
                          
#####################################################################################################     

# Second approach : Retrieving CaseId, DetectiveId - by using Inner Join  + Where 

SELECT DetectiveC.CaseId, DetectiveC.DetectiveId
FROM DetectiveCases as DetectiveC
JOIN (SELECT CaseId, MAX(Time_stamp) AS max_timestamp
	  FROM DetectiveCases
	  WHERE EventType = 'CaseSolved'
	  GROUP BY CaseId) sub 
ON DetectiveC.CaseId = sub.CaseId AND
 DetectiveC.Time_stamp = sub.max_timestamp # In order to find the last line of the time_stamp for a specific CaseId
WHERE DetectiveC.EventType = 'CaseSolved'; # The 'WHERE' here is a continuation for the outer query 


#####################################################################################################
# Top 5 Detective_IDs who have earned the most money during 2022

SELECT DetectiveC.CaseId, DetectiveC.DetectiveId, DetectiveC.Properties
FROM ( SELECT CaseId, DetectiveId, SUM(Properties) AS Total_Bounty
	   FROM DetectiveCases
       WHERE EventType = 'CaseOpened' # EventType = 'CaseSolved' OR 
       GROUP BY CaseId, DetectiveId ) DetectiveC
JOIN (SELECT CaseId, MAX(Time_stamp) AS max_timestamp
      FROM DetectiveCases
      WHERE EventType = 'CaseSolved'
      GROUP BY CaseId) sub
ON DetectiveC.CaseId = sub.CaseId
WHERE DetectiveC.DetectiveId IS NOT NULL
AND DetectiveC.Total_Bounty > 0
ORDER BY DetectiveC.Total_Bounty DESC  # The "Order by" line is for selecting the top 5 highest bounties given 
LIMIT 5;


#############################################################################################################

# In the next code here below I created 2 temprary tables in order to solve the same question.
# The first temporary table will be called temp_total_bounty.
# The Second temporary table will be called temp_last_transaction.
Afterwards, I will present the final query using the temporary tables which I  built.	
	

## Path 1 :  Create a temporary table to store the total bounty earned for each detective on each case
	
CREATE TEMPORARY TABLE temp_total_bounty AS
SELECT CaseId, DetectiveId, SUM(Properties) AS Total_Bounty
FROM DetectiveCases
WHERE EventType IN ('CaseOpened') # 'CaseSolved'
GROUP BY CaseId, DetectiveId;


## Path 2 : Create a temporary table to store the last transaction (CaseSolved) for each case
	
CREATE TEMPORARY TABLE temp_last_transaction AS
SELECT temp_bounty.CaseId, temp_bounty.DetectiveId, temp_bounty.SUM(Properties)
FROM temp_total_bounty temp_bounty
JOIN (SELECT CaseId, MAX(Time_stamp) AS max_timestamp
      FROM DetectiveCases
      WHERE EventType = 'CaseSolved'
      GROUP BY CaseId) sub 
ON temp_bounty.CaseId = sub.CaseId 
AND temp_bounty.Total_Bounty > 0;


## Path 3 : Retrieve the top 5 Detective IDs with the highest total bounty on each 'CaseSolved'
	
SELECT CaseId, DetectiveId, Total_Bounty
FROM temp_last_transaction
ORDER BY Total_Bounty DESC
LIMIT 5;

## Path 4 : Dropping the temporary tables
	
DROP TABLE IF EXISTS temp_total_bounty;
DROP TABLE IF EXISTS temp_last_transaction;







