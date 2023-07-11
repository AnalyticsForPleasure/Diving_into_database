# Path 1: Convertion table number 1

SELECT CaseId, Properties
FROM DetectiveCases
WHERE EventType = 'CaseOpened';

# Path 2: Convertion table number 2

Select CaseId,  EventType
from DetectiveCases
WHERE EventType = 'CaseSolved';


#####################################################################################################

## Finding the caseid which have been solved at the last transaction - by adding the max over the time_stamp 

SELECT CaseId
FROM DetectiveCases
WHERE EventType = 'CaseSolved'
GROUP BY CaseId
HAVING MAX(Time_stamp) = (SELECT MAX(Time_stamp)
						  FROM DetectiveCases
						  WHERE EventType = 'CaseSolved'
						  GROUP BY CaseId);
                          
