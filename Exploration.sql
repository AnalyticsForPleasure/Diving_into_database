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
                      

### Here I used the same subquery I wrote -The only thing I added  is the output "DetectiveId" +  Entered 'DetectiveId' into the group of the outer query

	
SELECT CaseId, DetectiveId
FROM DetectiveCases
WHERE EventType = 'CaseSolved'
GROUP BY CaseId , DetectiveId # added DetectiveId
HAVING MAX(Time_stamp) = (SELECT MAX(Time_stamp)
						  FROM DetectiveCases
						  WHERE EventType = 'CaseSolved'
						  GROUP BY CaseId);


# Let's to for a different approach - Using join + nested subqeury
	
SELECT DetectiveC.CaseId, DetectiveC.DetectiveId
FROM DetectiveCases DetectiveC
JOIN (SELECT CaseId, MAX(Time_stamp) AS max_timestamp
	  FROM DetectiveCases
	  WHERE EventType = 'CaseSolved'
	  GROUP BY CaseId) sub 
ON DetectiveC.CaseId = sub.CaseId AND
 DetectiveC.Time_stamp = sub.max_timestamp # This line is used  - In order to find the last line of the time_stamp for a specific CaseId
WHERE DetectiveC.EventType = 'CaseSolved'; # The 'WHERE' here is a continuation for the outer query 


                          
