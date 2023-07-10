# Path 1: Convertion table number 1

SELECT CaseId, Properties
FROM DetectiveCases
WHERE EventType = 'CaseOpened';

# Path 2: Convertion table number 2

Select CaseId,  EventType
from DetectiveCases
WHERE EventType = 'CaseSolved';
