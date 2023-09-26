



# DAX

|Dataset|[New Work Dashboard](./../New-Work-Dashboard.md)|
| :--- | :--- |
|Workspace|[New Work [Prod]](../../Workspaces/New-Work-[Prod].md)|

## Table: DailyTimeRecording

### Measures:


```dax
#DTR = 
if(SELECTEDVALUE(FromIntervals[From Interval]) = "no answer" || SELECTEDVALUE(EndIntervals[End Interval]) = "no answer"
  ,  [# no answer (DTR)]
  ,  COUNTROWS(DailyTimeRecording)
)

```



```dax
#DTR (0) = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),

    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return 
    coalesce(calculate([#DTR], _emps) , 0)
,
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return 
    coalesce(calculate([#DTR], _emps) , 0)
    )
```



```dax
# no answer (DTR) = 

//if(HASONEVALUE('rep v_hr_employee'[email])
//    , 888 // blank()
//    ,


var _from = min('Calendar'[Date])
var _to = max('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),
    var _staffing =  CALCULATETABLE(values('Staffing by Employee'[EmployeeID]),
         'Staffing by Employee'[StartDate] <= _to && 'Staffing by Employee'[EndDate] >= _from
         , treatas(values(Projetcs[ProjectNumber]),'Staffing by Employee'[ProjectNumber]))

    var _part =  calculatetable(
                values(Participants[participant_email])
                , REMOVEFILTERS('Calendar')
                , Treatas(_staffing, 'rep v_hr_employee'[emp_id])
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 

    var _days = CALCULATETABLE( values( 'Calendar'[Date]), REMOVEFILTERS(), 'Calendar'[IsWeekday] =  true,WEEKDAY('Calendar'[Date]) <> 2 /*monday not relevant*/,  'Calendar'[Date] >= _from && 'Calendar'[Date] <= _to)

    var res =  sumx(
            _days, 
            
            calculate(
                countrows(_part)
                - 
                calculate(coalesce(COUNTROWS(DailyTimeRecording),0), REMOVEFILTERS(FromIntervals), REMOVEFILTERS(EndIntervals))
                , _emps
            )
        )
    return res
,
    var _part =  calculatetable(
                values(Participants[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 

    var _days = CALCULATETABLE( values( 'Calendar'[Date]), REMOVEFILTERS(), 'Calendar'[IsWeekday] =  true,WEEKDAY('Calendar'[Date]) <> 2 /*monday not relevant*/,  'Calendar'[Date] >= _from && 'Calendar'[Date] <= _to)

    var res =  sumx(
            _days, 
            
            calculate(
                countrows(_part)
                - 
                calculate(coalesce(COUNTROWS(DailyTimeRecording),0), REMOVEFILTERS(FromIntervals), REMOVEFILTERS(EndIntervals))
                , _emps
            )
        )
    return res
)

```


### Calculated Columns:


```dax
From Interval = 
switch(TRUE()
    , hour( DailyTimeRecording[From]) <= 5, "5 AM and earlier"
    , hour( DailyTimeRecording[From]) < 7, "before 7 AM"
    , hour( DailyTimeRecording[From]) >= 7, "7 AM or later"
    , "No answer")
```



```dax
End Interval = 
switch(TRUE()
    , hour( DailyTimeRecording[To]) >= 5 && hour( DailyTimeRecording[To]) <= 20, "8 PM and earlier"
    , hour( DailyTimeRecording[To]) >= 5 && hour( DailyTimeRecording[To]) < 22, "later than 8 PM"
    , hour( DailyTimeRecording[To]) >= 5 && hour( DailyTimeRecording[To]) <=23, "10 PM and later"
    , hour( DailyTimeRecording[To]) < 5, "12 AM and later" //TODO: check other day?
    , "No answer")
```



```dax
end hour = hour( DailyTimeRecording[To])
```


## Table: Q3 DidYouWorkLessThan12Hours

### Measures:


```dax
#12h less = calculate(COUNTROWS('Q3 DidYouWorkLessThan12Hours'), 'Q3 DidYouWorkLessThan12Hours'[Did you work less than 12 hours yesterday?] = true)
```



```dax
#12h more = calculate(COUNTROWS('Q3 DidYouWorkLessThan12Hours'), 'Q3 DidYouWorkLessThan12Hours'[Did you work less than 12 hours yesterday?] = false)
```



```dax
Q3 = AVERAGE('Q3 DidYouWorkLessThan12Hours'[Q3 Value])
```



```dax
#emp 12h 0-1xYes = 

var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

var _tbl = ADDCOLUMNS(_emp, "@countMore", calculate([#12h less]))

var _f = filter(_tbl, [@countMore] <= 1)
return COUNTROWS(_f)
```



```dax
#emp 12h 2xYes = 

var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

var _tbl = ADDCOLUMNS(_emp, "@countMore", calculate([#12h less]))

var _f = filter(_tbl, [@countMore] = 2)
return COUNTROWS(_f)
```



```dax
#emp 12h 3xYes+ = 

var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

var _tbl = ADDCOLUMNS(_emp, "@countMore", calculate([#12h less]))

var _f = filter(_tbl, [@countMore] >= 3)
return COUNTROWS(_f)
```



```dax
#emp 12h n/a = 

var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

var _tbl = ADDCOLUMNS(_emp, "@countLess", calculate([#12h less]), "@countMore", calculate([#12h more]))

var _f = filter(_tbl, [@countMore] = 0 &&  [@countLess] = 0)
return COUNTROWS(_f)
```



```dax
Q3 per employee = 


if(SELECTEDVALUE(Projetcs[ProjectName]) = "no project assignment" || (not ISFILTERED(Projetcs) && not HASONEVALUE(Projetcs[ProjectName]))
,
var _part = calculatetable(values(Participants[participant_email]))
    var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))
    var _ansewerCount = if(HASONEVALUE('rep v_hr_employee'[email]), 0, 1)

    var _relevantEmp = filter(
            ADDCOLUMNS(_emp, "@answesCount", calculate(countrows('Q3 DidYouWorkLessThan12Hours')))
            , [@answesCount] >  _ansewerCount
        )
    return 
        Averagex(_relevantEmp, [Q3] ) 
        
,
    var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
    var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))
    var _ansewerCount = if(HASONEVALUE('rep v_hr_employee'[email]), 0, 1)

    var _relevantEmp = filter(
            ADDCOLUMNS(_emp, "@answesCount", calculate(countrows('Q3 DidYouWorkLessThan12Hours')))
            , [@answesCount] >  _ansewerCount
        )
    return 
        Averagex(_relevantEmp, [Q3] )  
)
```



```dax
#emp Q3 red = 

//var _cGreen = "#73B761"
//var _cOrange = "#ECC846"
var _c = "#FD625E"

var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

var _tbl = ADDCOLUMNS(_emp, "@color", calculate([MatrixColor (hist)]))

var _f = filter(_tbl, [@color] = _c)
return COUNTROWS(_f)
```



```dax
#emp Q3 yellow = 

//var _cGreen = "#73B761"
var _c = "#ECC846"
//var _cRed = "#FD625E"

var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

var _tbl = ADDCOLUMNS(_emp, "@color", calculate([MatrixColor (hist)]))

var _f = filter(_tbl, [@color] = _c)
return COUNTROWS(_f)
```



```dax
#emp Q3 green = 

var _c = "#73B761"
//var _cYellow = "#ECC846"
//var _cRed = "#FD625E"

var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

var _tbl = ADDCOLUMNS(_emp, "@color", calculate([MatrixColor (hist)]))

var _f = filter(_tbl, [@color] = _c)
return COUNTROWS(_f)
```



```dax
#emp Q3 gray = 

var _c = [Color_Insufficient]

return if(ISFILTERED(Projetcs)
,
    var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
    var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

    var _tbl = ADDCOLUMNS(_emp, "@color", calculate([MatrixColor (hist)]))

    var _f = filter(_tbl, [@color] = _c)
    return COUNTROWS(_f)
    ,
    var _part = calculatetable(values(Participants[participant_email]))
    var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

    var _tbl = ADDCOLUMNS(_emp, "@color", calculate([MatrixColor (hist)]))

    var _f = filter(_tbl, [@color] = _c)
    return COUNTROWS(_f)
)
```



```dax
#emp Q3 n/a = 

var _c = blank()

var _part = calculatetable(values(Participants[participant_email]), Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id]))
var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))

var _tbl = ADDCOLUMNS(_emp, "@color", calculate([MatrixColor (hist)]))

var _f = filter(_tbl, [@color] = blank())
return COUNTROWS(_f)
```


### Calculated Columns:


```dax
Q3 Value = if('Q3 DidYouWorkLessThan12Hours'[Did you work less than 12 hours yesterday?], 1, 0)
```


## Table: Q2 DidYouWorkOnTheWeekend

### Measures:


```dax
#WeekendWorked = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),

    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return calculate(COUNTROWS('Q2 DidYouWorkOnTheWeekend'), 'Q2 DidYouWorkOnTheWeekend'[Was your last weekend and any holidays last week completely free of work?] = false, _emps)
    ,   
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return calculate(COUNTROWS('Q2 DidYouWorkOnTheWeekend'), 'Q2 DidYouWorkOnTheWeekend'[Was your last weekend and any holidays last week completely free of work?] = false, _emps))
```



```dax
#WeekendFree = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),
    
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return calculate(COUNTROWS('Q2 DidYouWorkOnTheWeekend'), 'Q2 DidYouWorkOnTheWeekend'[Was your last weekend and any holidays last week completely free of work?] = true, _emps)
    ,   
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return calculate(COUNTROWS('Q2 DidYouWorkOnTheWeekend'), 'Q2 DidYouWorkOnTheWeekend'[Was your last weekend and any holidays last week completely free of work?] = true, _emps))
```



```dax
Q2 = AVERAGE('Q2 DidYouWorkOnTheWeekend'[Q2 Value])
```



```dax
Q2 NA = [PartCount] - [#WeekendFree] - [#WeekendWorked]
```


### Calculated Columns:


```dax
Q2 Value = if('Q2 DidYouWorkOnTheWeekend'[Was your last weekend and any holidays last week completely free of work?], 1, 0)
```


## Table: Q1 WereWorkingHoursWithinLimits

### Measures:


```dax
#WeeklyLimitsOk = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),

    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return calculate(COUNTROWS('Q1 WereWorkingHoursWithinLimits'), 'Q1 WereWorkingHoursWithinLimits'[Did your working hours this week stay within weekly limits?] = true, _emps)
    ,   
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return calculate(COUNTROWS('Q1 WereWorkingHoursWithinLimits'), 'Q1 WereWorkingHoursWithinLimits'[Did your working hours this week stay within weekly limits?] = true, _emps)
)
```



```dax
#WeeklyLimitsExceeded = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return calculate(COUNTROWS('Q1 WereWorkingHoursWithinLimits'), 'Q1 WereWorkingHoursWithinLimits'[Did your working hours this week stay within weekly limits?] = false, _emps)
    ,   
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
   
    return calculate(COUNTROWS('Q1 WereWorkingHoursWithinLimits'), 'Q1 WereWorkingHoursWithinLimits'[Did your working hours this week stay within weekly limits?] = false, _emps)
)
```



```dax
Q1 = AVERAGE('Q1 WereWorkingHoursWithinLimits'[Q1 Value])
```



```dax
Q1 NA = [PartCount] - [#WeeklyLimitsExceeded] - [#WeeklyLimitsOk]
```


### Calculated Columns:


```dax
Q1 Value = if('Q1 WereWorkingHoursWithinLimits'[Did your working hours this week stay within weekly limits?], 1, 0)
```


## Table: Q4 WorkloadNext2Weeks

### Measures:


```dax
Q4 +1 = AVERAGE('Q4 WorkloadNext2Weeks'[Q4 Value + 1])
```



```dax
Q4 +2 = AVERAGE('Q4 WorkloadNext2Weeks'[Q4 Value + 2])
```


### Calculated Columns:


```dax
Q4 Value + 1 = switch('Q4 WorkloadNext2Weeks'[NextWeek]
    , "Within weekly limits", 1
    , "Above weekly limits", 0.5
    , 0
    )
```



```dax
Q4 Value + 2 = switch('Q4 WorkloadNext2Weeks'[WeekAfterNextWeek]
    , "Within weekly limits", 1
    , "Above weekly limits", 0.5
    , 0
    )
```


## Table: rep v_hr_employee

### Measures:


```dax
DataCount = COUNTROWS('Q1 WereWorkingHoursWithinLimits') + COUNTROWS('Q2 DidYouWorkOnTheWeekend') + COUNTROWS('Q3 DidYouWorkLessThan12Hours') + COUNTROWS('Q4 WorkloadNext2Weeks' ) + COUNTROWS('Q6 HoursSpentOutsideProjectWorkdays') + COUNTROWS('Q7 HoursSpentOutsideProjectWeekend')
```



```dax
DataCount by Project staffing = 
var _project = min(Projetcs[ProjectName])
var _projectNumber = min(Projetcs[ProjectNumber])
var _minDate = min('Calendar'[Date])
var _maxDate = max('Calendar'[Date])

var _isNoAssignmentBucket = if(_project = "no project assignment", true, false)
var _empIds = CALCULATETABLE(values('rep v_hr_employee'[emp_id]),   TREATAS(values(Participants[participant_email]), 'rep v_hr_employee'[email] ))

return 
     if( _isNoAssignmentBucket, 1, calculate(COUNTROWS(Staffing), Staffing[ProjectNumber] = _projectNumber, TREATAS(_empIds, Staffing[EmployeeID])))

```



```dax
CountEmployeeStaffed = 
var _project = min(Projetcs[ProjectName])
var _projectNumber = min(Projetcs[ProjectNumber])
var _refreshDate = [RefreshDate]
var _empId = min('rep v_hr_employee'[emp_id])

var _isNoAssignmentBucket = if(_project = "no project assignment", true, false)

return if(_isNoAssignmentBucket
    ,
        if(not ISINSCOPE('rep v_hr_employee'[full_name])
            , 1  
            ,
                var _assignedAnyOtherProjects = calculate(COUNTROWS(Project2Employee), ALL(Project2Employee), Project2Employee[EmployeeID]=_empId)
                return if  (_assignedAnyOtherProjects > 0
                ,  _assignedAnyOtherProjects *-1 // blank() //other assignment exists
                ,  calculate(COUNTROWS('rep v_hr_employee'))
                )
        )
    , //calculate(COUNTROWS('rep v_hr_employee'), USERELATIONSHIP(Project2Employee[EmployeeID], 'rep v_hr_employee'[emp_id]))
    calculate(COUNTROWS('rep v_hr_employee'), Intersect(values(Project2Employee[EmployeeID]), values( 'rep v_hr_employee'[emp_id])))
)
```



```dax
CountParticipant = 
var _project = min(Projetcs[ProjectName])
var _projectNumber = min(Projetcs[ProjectNumber])
var _refreshDate = [RefreshDate]
var _empId = min('rep v_hr_employee'[emp_id])

var _isNoAssignmentBucket = if(_project = "no project assignment", true, false)

return calculate(COUNTROWS('rep v_hr_employee'), TREATAS(values(ParticipantsAndStaffing[participant_email]),'rep v_hr_employee'[email]))
/*
if(_isNoAssignmentBucket 
    ,   
        var _from = min('Calendar'[Date])
        var _to = max('Calendar'[Date])
        
        return if(ISINSCOPE('rep v_hr_employee'[full_name])
            , 
            var _partCnt = calculate(COUNTROWS('rep v_hr_employee'), TREATAS(values(Participants[participant_email]),'rep v_hr_employee'[email]))
            var cnt = calculate(countrows('Staffing by Employee'),  'Staffing by Employee'[EmployeeID] = _empId && 'Staffing by Employee'[ProjectNumber] <> _project && 'Staffing by Employee'[StartDate] <= _to && 'Staffing by Employee'[EndDate]>= _from)
            return if(_partCnt = 0 || cnt > 0, -1, 1)
            , calculate(COUNTROWS('rep v_hr_employee'), TREATAS(values(Participants[participant_email]),'rep v_hr_employee'[email]))
        )
    , 
    if(ISFILTERED(Projetcs)
        , calculate(COUNTROWS('rep v_hr_employee'), TREATAS(values(Participants[participant_email]),'rep v_hr_employee'[email]), intersect(Values('rep v_hr_employee'[emp_id]),values( Project2Employee[EmployeeID]))) 
        , calculate(COUNTROWS('rep v_hr_employee'), TREATAS(values(ParticipantsAndStaffing[participant_email]),'rep v_hr_employee'[email]))
    )
)
*/
```



```dax
DataCount by Project staffing (multiple projects) = 
var _project = min(Projetcs[ProjectName])

var _projectNumbers = Values(Projetcs[ProjectNumber])
var _minDate = min('Calendar'[Date])
var _maxDate = max('Calendar'[Date])

var _isNoAssignmentBucket = if(_project = "no project assignment", true, false)
var _empIds = CALCULATETABLE(values('rep v_hr_employee'[emp_id]),   TREATAS(values(Participants[participant_email]), 'rep v_hr_employee'[email] ))

return 
     if( _isNoAssignmentBucket, 1, calculate(COUNTROWS(Staffing), TREATAS(_projectNumbers,  Staffing[ProjectNumber]), TREATAS(_empIds, Staffing[EmployeeID])))

```



```dax
Mentor by Employee = 
if(not  HASONEVALUE('rep v_hr_employee'[emp_id])
    , blank()
    , LOOKUPVALUE(Mentors[Mentor],Mentors[mentor_emp_id], SELECTEDVALUE('rep v_hr_employee'[mentor_emp_id]))
)
```


### Calculated Columns:


```dax
Overall = "Overall"
```



```dax
Overall Y/N = "Overall (Y/N)" 
```


## Table: Calendar


```dax
CALENDAR(DATE(2022, 1, 1), Today() +  7)
```


### Measures:


```dax
Interval = Format( min('Calendar'[Date]), "DDD dd.MM") & " - "  & Format( max('Calendar'[Date]), "DDD dd.MM")
```


### Calculated Columns:


```dax
WEEK = Format(  
      if(Month('Calendar'[Date])= 1 && WEEKNUM('Calendar'[Date],21) >=52
        , YEAR('Calendar'[Date])-1
        , YEAR('Calendar'[Date]))
     , 0) & "-" & WEEKNUM('Calendar'[Date],21)
```



```dax
WeekOffset = 
var _curDate = 'Calendar'[Date]
var _refreshDate = [RefreshDate]

var _todaysWeek  = calculate(min('Calendar'[WEEK]), all ('Calendar'), 'Calendar'[Date] = _refreshDate)
var _endOfTodaysWeek  = calculate(max('Calendar'[Date]), all ('Calendar'), 'Calendar'[WEEK] = _todaysWeek)

return 
if(_curDate > _endOfTodaysWeek, 99,
   -1 * (coalesce(CALCULATE(COUNTROWS(distinct('Calendar'[WEEK])),All('Calendar'), 'Calendar'[Date] <= _endOfTodaysWeek && 'Calendar'[Date] >=_curDate ), 0) -1)
)
```



```dax
IsWeekday = WEEKDAY('Calendar'[Date]) <> 1 && WEEKDAY('Calendar'[Date]) <> 7 
```



```dax
ShiftedWeekOffest = 
var _wd = WEEKDAY('Calendar'[Date])

return if(_wd >= 4 // MI 4, Do 5, Fr 6 , Sa 7
    || _wd = 1 //So
    , 'Calendar'[WeekOffset] + 1
    , 'Calendar'[WeekOffset])


```



```dax
Shifted Weekname = 
var _offset = 'Calendar'[ShiftedWeekOffest]

var _minDate = CALCULATE(min('Calendar'[Date]), all('Calendar'),'Calendar'[ShiftedWeekOffest] = _offset)

return Format( YEAR(_minDate), 0) & "-CW" & Format(WEEKNUM(_minDate, 21), "00")
```


## Table: _Measures

### Measures:


```dax
RefreshDate = 
var _rd = min(RefreshDate[RefreshDate])
return if(weekday(_rd) <= 2 //Sunday / Monday)
    , _rd - 2
    , _rd) 
//date(2022,5,14) // min(RefreshDate[RefreshDate])
```



```dax
Color_Insufficient = "#B3B3B3"
```



```dax
Icon Exclamation White = "!" // "❗"  //"❕"    //does not work in Matrix
```



```dax
Icon Exclamation Red = "!" // "❗"
```



```dax
Icon Cross = "x"//"✖"
```



```dax
cGreen = "#73B761"
```



```dax
cOrange = "#ECC846"
```



```dax
cRed = "#FD625E"
```



```dax
CrossFilterEndTime = 
if(ISINSCOPE('rep v_hr_employee'[full_name]) && ISFILTERED(EndIntervals[End Interval])
    ,  [#DTR (0)]
    , 1
)
```



```dax
cGrayFont = "#999999"
```



```dax
staffingCount = Countrows(ParticipantsAndStaffing)
```



```dax
Employee details = if(COUNTROWS('Values by Staffing') > 0 && HASONEVALUE('rep v_hr_employee'[emp_id]) && ISINSCOPE('rep v_hr_employee'[full_name]) 
,SELECTEDVALUE('Values by Staffing'[Employee details] , blank())
)
```


## Table: Participants

### Measures:


```dax
PartCount = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),
      var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
     return calculate(COUNTROWS(_part))
    ,   
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    return calculate(COUNTROWS(_part)))
```


## Table: MatrixColumns

### Measures:


```dax
MatrixState = 

var _intervalSort = min((MatrixColumns[Sort]))
var _intervalIdInGroup = min((MatrixColumns[IdInGroup]))
var _interval = min((MatrixColumns[Interval]))
var _groupId  = min((MatrixColumns[GroupId]))

return if(HASONEVALUE(MatrixColumns[Sort]) && [CountParticipant]>0
       /* && (COUNTROWS('Q3 DidYouWorkLessThan12Hours') > 0 
            || COUNTROWS('Q4 WorkloadNext2Weeks') > 0
            || COUNTROWS('Q2 DidYouWorkOnTheWeekend') > 0 
        )*/
    , switch(_groupId
        , -1 //q8 counteraction
        , switch(_intervalIdInGroup
            , 1
            , var _yes = calculate( [Q8 Yes], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = -1)
                return if(_yes > 0, _yes, -1 * calculate( [Q8 No], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = -1))
            , 2
            , var _yes = calculate( [Q8 Yes], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = 0)
                return if(_yes > 0, _yes, -1 * calculate( [Q8 No], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = 0)
                )
        )
        , 6 //q8 comment
        , [Single Comment]
        , 1
        , switch(_intervalIdInGroup
            , 1
            , calculate( [Q1], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = 0)
            , 2
            , calculate( [Q1], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = -1)
            , 3
            , calculate( [Q1], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = -2)
        )
        , 2 //Q2 free weekend
        , switch(_intervalIdInGroup
            , 1
            , calculate( [Q2], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest]) &&  'Calendar'[ShiftedWeekOffest] = 0)
            , 2
            , calculate( [Q2], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = -1)
            , 3
            , calculate( [Q2], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = -2)
        )
        , 3 --Q3
        , switch(_intervalIdInGroup
            , 1
            , calculate(AVERAGE('Values by Staffing'[Q3 (< 12h)])) //, all('Calendar'), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = 0)
        )
        , 4
        , switch(_intervalIdInGroup
            , 2
            , calculate( [Q4 +1], REMOVEFILTERS('Calendar'[Date]),  not ISBLANK('Calendar'[ShiftedWeekOffest]) && 'Calendar'[ShiftedWeekOffest] = 0)
            , 3
            , calculate( [Q4 +2], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest]) &&  'Calendar'[ShiftedWeekOffest] = 0)
        )
        , 5
        , switch(_intervalIdInGroup
            , 1
            , calculate( [Q6/Q7 Hours], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = 0)
            , 2
            , calculate( [Q6/Q7 Count], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = 0)
        )
))
```



```dax
MatrixStateText = 

var _intervalSort = min((MatrixColumns[Sort]))
var _intervalIdInGroup = min((MatrixColumns[IdInGroup]))
var _interval = min((MatrixColumns[Interval]))
var _groupId  = min((MatrixColumns[GroupId]))

return 

if(HASONEVALUE(MatrixColumns[Sort])
    && [CountParticipant] > 0
   /* && (COUNTROWS('Q3 DidYouWorkLessThan12Hours') > 0 
        || COUNTROWS('Q4 WorkloadNext2Weeks') > 0
        || COUNTROWS('Q2 DidYouWorkOnTheWeekend') > 0

    )*/
    ,
    if( ISINSCOPE('rep v_hr_employee'[full_name]) || ISINSCOPE(Projetcs[Project])
    ,
    //employee level 
    switch(_groupId
         , 5
            , if(not ISBLANK([MatrixState]), FORMAT([MatrixState], "#"), "")
         , -1 //q8 yes/no
            , if(ISINSCOPE('rep v_hr_employee'[full_name]),
                switch(_intervalIdInGroup
                    , 2, if([MatrixState]> 0, [Icon Exclamation Red],  if( [MatrixState]< 0, [Icon Cross],""))
                    , 1, if([MatrixState]> 0, [Icon Exclamation White],if( [MatrixState]< 0, [Icon Cross],""))
                )
            )
         , 6 //q8 comment
         ,  if(ISINSCOPE('rep v_hr_employee'[full_name]),[MatrixState],"")
         
         , "" //FORMAT([MatrixState], "#") //"" //default
         )
    , 
    //totals
    switch(_groupId
        , -1 //Q8 counteractions
            , switch(_intervalIdInGroup
                , 2, if([MatrixState]> 0, [Icon Exclamation Red])
                , 1, if([MatrixState]> 0, [Icon Exclamation White])
            )
        , 1
        , switch(_intervalIdInGroup
            , 1
            , calculate( [#WeeklyLimitsOk], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest]) && 'Calendar'[ShiftedWeekOffest] = 0) & "/" & calculate( [#WeeklyLimitsExceeded], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest]) && 'Calendar'[ShiftedWeekOffest] = 0)
            , 2
            , calculate( [#WeeklyLimitsOk], REMOVEFILTERS('Calendar'[Date]), 'Calendar'[ShiftedWeekOffest] = -1) & "/" & calculate( [#WeeklyLimitsExceeded], REMOVEFILTERS('Calendar'[Date]), 'Calendar'[ShiftedWeekOffest] = -1)
            , 3
            , calculate( [#WeeklyLimitsOk], REMOVEFILTERS('Calendar'[Date]), 'Calendar'[ShiftedWeekOffest] = -2) & "/" & calculate( [#WeeklyLimitsExceeded], REMOVEFILTERS('Calendar'[Date]), 'Calendar'[ShiftedWeekOffest] = -2)
        )
        , 2 //Q2 free weekend
        , switch(_intervalIdInGroup
            , 1
            , calculate( [#WeekendFree], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest]) && 'Calendar'[ShiftedWeekOffest] = 0) & "/" & calculate( [#WeekendWorked], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest]) && 'Calendar'[ShiftedWeekOffest] = 0)
            , 2
            , calculate( [#WeekendFree], REMOVEFILTERS('Calendar'[Date]), 'Calendar'[ShiftedWeekOffest] = -1) & "/" & calculate( [#WeekendWorked], REMOVEFILTERS('Calendar'[Date]), 'Calendar'[ShiftedWeekOffest] = -1)
            , 3
            , calculate( [#WeekendFree], REMOVEFILTERS('Calendar'[Date]), 'Calendar'[ShiftedWeekOffest] = -2) & "/" & calculate( [#WeekendWorked], REMOVEFILTERS('Calendar'[Date]), 'Calendar'[ShiftedWeekOffest] = -2)
        )
        , 3 --Q3 Q4
        , "" --no data wanted
        , 4
        , ""
        , 5
        , FORMAT([MatrixState], "#")
        //switch(_intervalIdInGroup
            //   , 1
            //   , [12h state]
        //    , 2
            //   , 'Q4 WorkloadNext2Weeks'[WorkloadWeek+1]
            //   , 3
            //   , 'Q4 WorkloadNext2Weeks'[WorkloadWeek+2]
        //)
        )
    )
)
```



```dax
Show project or employee based on staffing and participant = 
var _project = min(Projetcs[ProjectName])
var _projectNumber = min(Projetcs[ProjectNumber])
var _refreshDate = [RefreshDate]
var _empId = min('rep v_hr_employee'[emp_id])
var _empMail = min('rep v_hr_employee'[email])

var _isNoAssignmentBucket = if(_project = "no project assignment", true, false)

return Switch(true()
    , ISINSCOPE('rep v_hr_employee'[full_name])
    , // Employee
     if(calculate(COUNTROWS(Staffing), Staffing[EmployeeID] = _empId &&  Staffing[ProjectNumber] = _projectNumber &&  Staffing[StartDate] <= _refreshDate && Staffing[EndDate] >= _refreshDate) > 0
        , 1
        , if(_isNoAssignmentBucket 
            && (calculate(COUNTROWS(Participants), Participants[participant_email] =  _empMail) > 0
                || calculate(COUNTROWS(Staffing), Staffing[EmployeeID] = _empId &&  Staffing[StartDate] <= _refreshDate && Staffing[EndDate] >= _refreshDate) = 0)
            , 1
            ,   if(_empMail = "florian.zrenner@org.rolandberger.com", 1, blank())
            )
        )
    , ISINSCOPE(Projetcs[Project])
    , //project
     if( _isNoAssignmentBucket || calculate(COUNTROWS(Staffing), Staffing[ProjectNumber] = _projectNumber && Staffing[StartDate] <= _refreshDate && Staffing[EndDate] >= _refreshDate) > 0, 1, blank())
    , blank()
)

```



```dax
MatrixState (hist) = 

var _weekOffset = min('Calendar'[ShiftedWeekOffest])

var _intervalSort = min((MatrixColumns[Sort]))
var _intervalIdInGroup = min((MatrixColumns[IdInGroup]))
var _interval = min((MatrixColumns[Interval]))
var _groupId  = min((MatrixColumns[GroupId]))

return if(HASONEVALUE(MatrixColumns[Sort]) && [CountParticipant]>0
       /* && (COUNTROWS('Q3 DidYouWorkLessThan12Hours') > 0 
            || COUNTROWS('Q4 WorkloadNext2Weeks') > 0
            || COUNTROWS('Q2 DidYouWorkOnTheWeekend') > 0 
        )*/
    , switch(_groupId
        , -1 //q8 counteraction
        , switch(_intervalIdInGroup
            , 1
            , var _yes = calculate( [Q8 Yes], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = _weekOffset -1)
                return if(_yes >0, _yes, -1 *  calculate( [Q8 No], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = _weekOffset -1))
            , 2
            , var _yes = calculate( [Q8 Yes], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = _weekOffset + 0)
            return if (_yes >0, _yes, -1 * calculate( [Q8 No], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = _weekOffset + 0))
        )
        , 6 //q8 comment
        , calculate([Single Comment Short], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = _weekOffset)

        , 1
        , switch(_intervalIdInGroup
            , 1
            , calculate( [Q1], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = _weekOffset + 0)
            , 2
            , calculate( [Q1], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = _weekOffset -1)
            , 3
            , calculate( [Q1], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = _weekOffset -2)
        )
        , 2 //Q2 free weekend
        , switch(_intervalIdInGroup
            , 1
            , calculate( [Q2], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest]) &&  'Calendar'[ShiftedWeekOffest] = _weekOffset + 0)
            , 2
            , calculate( [Q2], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = _weekOffset -1)
            , 3
            , calculate( [Q2], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = _weekOffset -2)
        )
        , 3 --Q3
        , switch(_intervalIdInGroup
            , 1
            , calculate([Q3 per employee], all('Calendar'), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = _weekOffset +0)
        )
        , 4
        , switch(_intervalIdInGroup
            , 2
            , calculate( [Q4 +1], REMOVEFILTERS('Calendar'[Date]),  not ISBLANK('Calendar'[ShiftedWeekOffest]) && 'Calendar'[ShiftedWeekOffest] = _weekOffset + 0)
            , 3
            , calculate( [Q4 +2], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest]) &&  'Calendar'[ShiftedWeekOffest] = _weekOffset +0)
        )
        , 5
        , switch(_intervalIdInGroup
            , 1
            , calculate( [Q6/Q7 Hours], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = _weekOffset+ 0)
            , 2
            , calculate( [Q6/Q7 Count], REMOVEFILTERS('Calendar'[Date]), not ISBLANK('Calendar'[ShiftedWeekOffest])  && 'Calendar'[ShiftedWeekOffest] = _weekOffset+0)
        )
))
```



```dax
MatrixColor (hist) = 

var _value = [MatrixState (hist)]
var _cGreen = "#73B761"
var _cOrange = "#ECC846"
var _cRed = "#FD625E"


RETURN 
    if(not ISBLANK(_value),
    if(HASONEVALUE('rep v_hr_employee'[full_name])
    ,//single employee
        switch(min(MatrixColumns[Question])
        , "Q1" //weekly limits
        , switch(true()
            , _value = 0, _cRed
            , _value = 1, _cGreen
            , _cOrange
            )
        ,"Q2" //weekend, holiday off
        , switch(true()
            , _value = 0, _cRed
            , _value = 1, _cGreen
            , _cOrange
            )
        , "Q3" //max 12h
        , 
        var _answerCount = calculate(COUNTROWS('Q3 DidYouWorkLessThan12Hours'))
        return switch(_answerCount
        , 0, blank()
        , 1,  [Color_Insufficient] -- gray
        , 2, 
            switch(true()
            , _value < 0.5, _cRed 
            , _value < 1, _cOrange
            , _cGreen
            )
        , 3, 
            switch(true()
            , _value < 0.5, _cRed 
            //, _value < 0.75, _cOrange
            , _cGreen
            )
        , 4, 
            switch(true()
            , _value < 0.5, _cRed 
            , _value < 0.75, _cOrange
            , _cGreen
            )
        )
        , "Q4" //next weeks
        , switch(true()
            , _value = 0, _cRed
            , _value < 1, _cOrange
            , _cGreen
            )
        )
    , //aggregated, multiple employees
        switch(min(MatrixColumns[Question])
            , "Q1" //weekly limits
            , switch(true()
                , _value < 0.34, _cRed
                , _value < 0.67, _cOrange
                , _cGreen
                )
            ,"Q2" //weekend, holiday off
            , switch(true()
                , _value < 0.34, _cRed
                , _value < 0.67, _cOrange
                , _cGreen
                )
            , "Q3" //max 12h
            , switch(true()
                , _value <= 0.5, _cRed 
                , _value <= 0.75, _cOrange
                , _cGreen
                )
            , "Q4" //next weeks
            , switch(true()
                , _value < 0.34, _cRed
                , _value < 0.67, _cOrange
                , _cGreen
                )
            )
    )
)

```


## Table: Q6 HoursSpentOutsideProjectWorkdays

### Measures:


```dax
Q6 Hours = sum('Q6 HoursSpentOutsideProjectWorkdays'[Hours])
```



```dax
Q6 Count = CALCULATE(COUNTROWS('Q6 HoursSpentOutsideProjectWorkdays'), 'Q6 HoursSpentOutsideProjectWorkdays'[Hours] > 0)
```



```dax
Q6/Q7 Hours = [Q6 Hours]+ [Q7 Hours]
```



```dax
Q6/Q7 Count = 

var _calc = [Q6 Count]+ [Q7 Count]

return if(not ISBLANK(_calc)
            ,  _calc
            ,
            //
            0
)
```



```dax
Q6/7 Count employees 0-5 h = 
var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    
    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
    var _empsCluster = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), Filter(_emps, not isblank([Q6/Q7 Hours]) && [Q6/Q7 Hours] <= 5),_emps)
return countrows(_empsCluster)
,
var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
    var _empsCluster = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), Filter(_emps, not isblank([Q6/Q7 Hours]) && [Q6/Q7 Hours] <= 5),_emps)
    return countrows(_empsCluster)
)
```



```dax
Q6/7 Count employees 5-10 h = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
    var _empsCluster = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), Filter(_emps, [Q6/Q7 Hours] > 5 && [Q6/Q7 Hours]  <= 10),_emps)
    return countrows(_empsCluster)
,
        var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
    var _empsCluster = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), Filter(_emps, [Q6/Q7 Hours] > 5 && [Q6/Q7 Hours]  <= 10),_emps)

    return countrows(_empsCluster)
)

```



```dax
Q6/7 Count employees > 10 h = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),

    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    
    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
    var _empsCluster = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), Filter(_emps, [Q6/Q7 Hours] > 10),_emps)
    return countrows(_empsCluster)
,
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )

    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
    var _empsCluster = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), Filter(_emps, [Q6/Q7 Hours] > 10),_emps)

    return countrows(_empsCluster)
)
```



```dax
Q6/7 NA = 

var _offest = min('Calendar'[ShiftedWeekOffest])
var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),

    var _part =  calculatetable(
                values(ParticipantsAndStaffing[emp_id])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    
    var _answers = DISTINCT(  union( calculatetable(values('Q6 HoursSpentOutsideProjectWorkdays'[Mail]),   Treatas(_part, 'rep v_hr_employee'[emp_id]))
                    , calculatetable(values('Q7 HoursSpentOutsideProjectWeekend'[Mail]),   Treatas(_part, 'rep v_hr_employee'[emp_id])))
                    
    )              
    return   if(countrows(_part) = 0, blank(), max( countrows(_part) - countrows(_answers), 0))
,
    var _part =  countrows(calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    )

    var _answers = DISTINCT(  union( calculatetable(values('Q6 HoursSpentOutsideProjectWorkdays'[Mail]))
                    , calculatetable(values('Q7 HoursSpentOutsideProjectWeekend'[Mail])))
    )              
    return    if(_part = 0, blank(), max( _part - countrows(_answers), 0))
)
```



```dax
Q6/7 Count >12 employees 0-5 h = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),

    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
            
    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 

    var _emps_gt_12h_ac = ADDCOLUMNS(_emps, "@count", CALCULATE([Q3 #emp by state],'Q3 12h States'[State] = "Mostly no", MatrixColumns[Question] = "Q3" ))
    var _emps_gt_12h =  Filter(_emps_gt_12h_ac, [@count] > 0)
    var _empsCluster = Filter(_emps_gt_12h, not isblank([Q6/Q7 Hours]) && [Q6/Q7 Hours] <= 5)
    return countrows(_empsCluster)
,
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 

    var _emps_gt_12h_ac = ADDCOLUMNS(_emps, "@count", CALCULATE([Q3 #emp by state],'Q3 12h States'[State] = "Mostly no", MatrixColumns[Question] = "Q3" ))
    var _emps_gt_12h =  Filter(_emps_gt_12h_ac, [@count] > 0)
    var _empsCluster = Filter(_emps_gt_12h, not isblank([Q6/Q7 Hours]) && [Q6/Q7 Hours] <= 5)
    return countrows(_empsCluster)
)
```



```dax
Q6/7 Count >12 employees 5-10 h = 

var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),

    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 
    
    var _emps_gt_12h_ac = ADDCOLUMNS(_emps, "@count", CALCULATE([Q3 #emp by state],'Q3 12h States'[State] = "Mostly no", MatrixColumns[Question] = "Q3" ))

    var _emps_gt_12h =  Filter(_emps_gt_12h_ac, [@count] > 0)
    var _empsCluster = Filter(_emps_gt_12h, [Q6/Q7 Hours] > 5 && [Q6/Q7 Hours] <= 10)
    return countrows(_empsCluster)
, var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 

    var _emps_gt_12h_ac = ADDCOLUMNS(_emps, "@count", CALCULATE([Q3 #emp by state],'Q3 12h States'[State] = "Mostly no", MatrixColumns[Question] = "Q3" ))
    var _emps_gt_12h =  Filter(_emps_gt_12h_ac, [@count] > 0)
    var _empsCluster = Filter(_emps_gt_12h, [Q6/Q7 Hours] > 5 && [Q6/Q7 Hours] <= 10)
    return countrows(_empsCluster)
)
```



```dax
Q6/7 Count >12 employees >10 h = 
var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])
var _offest = min('Calendar'[ShiftedWeekOffest])

return if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),

    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
            
    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 

   var _emps_gt_12h_ac = ADDCOLUMNS(_emps, "@count", CALCULATE([Q3 #emp by state],'Q3 12h States'[State] = "Mostly no", MatrixColumns[Question] = "Q3" ))
    var _emps_gt_12h =  Filter(_emps_gt_12h_ac, [@count] > 0)
    var _empsCluster = Filter(_emps_gt_12h, [Q6/Q7 Hours] > 10)
    return countrows(_empsCluster)
,
    var _part =  calculatetable(
                values(ParticipantsAndStaffing[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    var _emps = CALCULATETABLE(values('rep v_hr_employee'[emp_id]), TREATAS(_part,'rep v_hr_employee'[email])) 

    var _emps_gt_12h_ac = ADDCOLUMNS(_emps, "@count", CALCULATE([Q3 #emp by state],'Q3 12h States'[State] = "Mostly no", MatrixColumns[Question] = "Q3" ))
    var _emps_gt_12h =  Filter(_emps_gt_12h_ac, [@count] > 0)
    var _empsCluster = Filter(_emps_gt_12h, [Q6/Q7 Hours] > 10)
    return countrows(_empsCluster)
)
```



```dax
Q6/7 answers = 

var _offest = min('Calendar'[ShiftedWeekOffest])
var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])

return if(ISFILTERED(Projetcs),
    var _staffing =  CALCULATETABLE(values('Staffing by Employee'[EmployeeID]),
         'Staffing by Employee'[StartDate] <= _to && 'Staffing by Employee'[EndDate] >= _from
         , treatas(values(Projetcs[ProjectNumber]),'Staffing by Employee'[ProjectNumber]))


    var _part =  countrows(calculatetable(
                values(Participants[participant_email])
                , REMOVEFILTERS('Calendar')
                --, Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id])
                , Treatas(_staffing, 'rep v_hr_employee'[emp_id])
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    )

    var _answers = DISTINCT(  union( calculatetable(values('Q6 HoursSpentOutsideProjectWorkdays'[Mail]),   Treatas(_staffing, 'rep v_hr_employee'[emp_id]))
                    , calculatetable(values('Q7 HoursSpentOutsideProjectWeekend'[Mail]),   Treatas(_staffing, 'rep v_hr_employee'[emp_id])))
                    
    )              
    return  countrows(_answers) //_part //  if(_part = 0, blank(), max( _part - countrows(_answers), 0))
,
    var _part =  countrows(calculatetable(
                values(Participants[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    )

    var _answers = DISTINCT(  union( calculatetable(values('Q6 HoursSpentOutsideProjectWorkdays'[Mail]))
                    , calculatetable(values('Q7 HoursSpentOutsideProjectWeekend'[Mail])))
    )              
    return    if(_part = 0, blank(), max( _part - countrows(_answers), 0))
)
```



```dax
Q6/7 part = 

var _offest = min('Calendar'[ShiftedWeekOffest])
var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])

return if(ISFILTERED(Projetcs),
    var _staffing =  CALCULATETABLE(values('Staffing by Employee'[EmployeeID]),
         'Staffing by Employee'[StartDate] <= _to && 'Staffing by Employee'[EndDate] >= _from
         , treatas(values(Projetcs[ProjectNumber]),'Staffing by Employee'[ProjectNumber]))


    var _part =  countrows(calculatetable(
                values(Participants[participant_email])
                , REMOVEFILTERS('Calendar')
                --, Treatas(values(Project2Employee[EmployeeID]), 'rep v_hr_employee'[emp_id])
                , Treatas(_staffing, 'rep v_hr_employee'[emp_id])
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    )

    var _answers = DISTINCT(  union( calculatetable(values('Q6 HoursSpentOutsideProjectWorkdays'[Mail]),   Treatas(_staffing, 'rep v_hr_employee'[emp_id]))
                    , calculatetable(values('Q7 HoursSpentOutsideProjectWeekend'[Mail]),   Treatas(_staffing, 'rep v_hr_employee'[emp_id])))
                    
    )              
    return  _part //  if(_part = 0, blank(), max( _part - countrows(_answers), 0))
,
    var _part =  countrows(calculatetable(
                values(Participants[participant_email])
                , REMOVEFILTERS('Calendar')
                , 'Calendar'[ShiftedWeekOffest] = _offest
            )
    )

    var _answers = DISTINCT(  union( calculatetable(values('Q6 HoursSpentOutsideProjectWorkdays'[Mail]))
                    , calculatetable(values('Q7 HoursSpentOutsideProjectWeekend'[Mail])))
    )              
    return    if(_part = 0, blank(), max( _part - countrows(_answers), 0))
)
```


## Table: Q7 HoursSpentOutsideProjectWeekend

### Measures:


```dax
Q7 Hours = sum('Q7 HoursSpentOutsideProjectWeekend'[Hours])
```



```dax
Q7 Count = CALCULATE(COUNTROWS('Q7 HoursSpentOutsideProjectWeekend'), 'Q7 HoursSpentOutsideProjectWeekend'[Hours]>0)
```


## Table: Staffing by Employee


```dax
Staffing
```


### Measures:


```dax
VisibleInGantt = 
var _minDateVisible = EDATE([RefreshDate], -1)
var _maxDateVisible = EDATE([RefreshDate], 1) //max('Calendar'[Date])

var _startDate = min('StaffingAll'[StartDate])
var _endDate = min('StaffingAll'[EndDate])

return if(_startDate <= _maxDateVisible && _endDate >= _minDateVisible, 1, 0)

```


### Calculated Columns:


```dax
DM = LOOKUPVALUE('rep v_hr_employee'[full_name],'rep v_hr_employee'[emp_id], 'Staffing by Employee'[EmployeeIDDM])
```



```dax
PM = LOOKUPVALUE('rep v_hr_employee'[full_name],'rep v_hr_employee'[emp_id], 'Staffing by Employee'[EmployeeIDPM])
```



```dax
Mail = LOOKUPVALUE('rep v_hr_employee'[email],'rep v_hr_employee'[emp_id], 'Staffing by Employee'[EmployeeID]) 
```


## Table: Q3 12h States

### Measures:


```dax
Q3 #emp by state = 
var _c = SELECTEDVALUE('Q3 12h States'[StateColor])

var _offest = min('Calendar'[ShiftedWeekOffest])
var _from = min('Calendar'[Date])
var _to = min('Calendar'[Date])

return if(isblank(_c)
        , blank()
        , 
    if(ISFILTERED(Projetcs) || HASONEVALUE(Projetcs[EmployeeIDPM] ) || HASONEVALUE('Staffing by Employee'[EmployeeIDDM]),
        /*var _staffing =  CALCULATETABLE(values('Staffing by Employee'[EmployeeID]),
            'Staffing by Employee'[StartDate] <= _to && 'Staffing by Employee'[EndDate] >= _from
            , treatas(values(Projetcs[ProjectNumber]),'Staffing by Employee'[ProjectNumber]))


        var _part = calculatetable(
                    values(Participants[participant_email])
                    , REMOVEFILTERS('Calendar')
                    , Treatas(_staffing, 'rep v_hr_employee'[emp_id])
                    , 'Calendar'[ShiftedWeekOffest] = _offest
                )
                */
        var _part = calculatetable(
                    values(ParticipantsAndStaffing[participant_email])
                    , REMOVEFILTERS('Calendar')
                    , 'Calendar'[ShiftedWeekOffest] = _offest
                )
    
        var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_part,'rep v_hr_employee'[email]))
        var _tbl = ADDCOLUMNS(_emp, "@color", calculate([MatrixColor (hist)], MatrixColumns[Question]="Q3"))
        var _f = filter(_tbl, [@color] = _c)
        return COUNTROWS(_f)
        ,

        var _partAll = calculatetable(values(ParticipantsAndStaffing[participant_email]))
        var _emp = CALCULATETABLE(values('rep v_hr_employee'[email]), TREATAS(_partAll,'rep v_hr_employee'[email]))
        var _tbl = ADDCOLUMNS(_emp, "@color", calculate([MatrixColor (hist)], MatrixColumns[Question]="Q3"))

        var _f = filter(_tbl, [@color] = _c)
        return COUNTROWS(_f)
)
)

```


## Table: Roles

### Measures:


```dax
CanUserSeeDetailsByRole = 
    if(
        [UserIsAdmin]
        || [UserIsConsultant] && min(ParticipantsAndStaffing[email_mentor]) = USERPRINCIPALNAME()
        || [UserIsCountry] 
            && 
            (
                min(ParticipantsAndStaffing[country_code]) in values('rls country'[permission_to]) || min(ParticipantsAndStaffing[country_code]) = LOOKUPVALUE('rep v_hr_employee'[country_code], 'rep v_hr_employee'[email], USERPRINCIPALNAME())
            )
        || [UserIsCountryProject] 
            && 
            (
                min(ParticipantsAndStaffing[country_code_dm]) in values('rls country project'[permission_to]) || min(ParticipantsAndStaffing[country_code_dm]) = LOOKUPVALUE('rep v_hr_employee'[country_code], 'rep v_hr_employee'[email], USERPRINCIPALNAME())
            )
        || [UserIsCountryOnly] 
            && 
            (
                min(ParticipantsAndStaffing[country_code]) in values('rls countryOnly'[permission_to])
            )
        || [UserIsCountryOnlyProject] 
            && 
            (
                min(ParticipantsAndStaffing[country_code_dm]) in values('rls countryOnly project'[permission_to])
            )
        || [UserIsPlatform] 
            && 
            (   min(ParticipantsAndStaffing[platform_1_id]) = calculate(min('rep v_hr_employee'[platform_1_id]), 'rep v_hr_employee'[email] = USERPRINCIPALNAME(), All('rep v_hr_employee'))
            ||
                min(ParticipantsAndStaffing[platform_1_id]) in values('rls platform'[permission_to])
            ||
                min(ParticipantsAndStaffing[platform_1_id]) in values('rls platform DACH'[permission_to])
            )
    
        || [UserIsPilotRole] && min(ParticipantsAndStaffing[pilot_group]) in values('rls pilot group permission'[permission_to])
        || [UserIsClientTeam] && min(ParticipantsAndStaffing[practice_group]) in values('rls clientteam'[permission_to])
        || SELECTEDVALUE(Participants[participant_email]) = USERPRINCIPALNAME()
        , 1
        , 0)
```



```dax
CanSeeDetailsText = if([CanUserSeeDetailsByRole], "", "Infotext: You do not have access to this view - Please use the filters on the 'Key indicators' page for historical data")
```



```dax
UserIsAdmin = "Admin" in Values(Roles[Role])
```



```dax
UserIsConsultant = "Consultant" in Values(Roles[Role])
```



```dax
UserIsCountry = "Country" in Values(Roles[Role])
```



```dax
UserIsPlatform = "Platform" in Values(Roles[Role])
```



```dax
UserIsPilotRole = "Pilot" in Values(Roles[Role])
```



```dax
UserIsClientTeam = "Client-Team" in Values(Roles[Role])
```



```dax
UserIsCountryOnly = "CountryOnly" in Values(Roles[Role])
```



```dax
UserIsCountryProject = "CountryProject" in Values(Roles[Role])
```



```dax
UserIsCountryOnlyProject = "CountryOnlyProject" in Values(Roles[Role])
```


## Table: Q8 CounterActions

### Measures:


```dax
Q8 Yes = calculate(COUNTROWS('Q8 CounterActions'), 'Q8 CounterActions'[Counteraction needed] = "Yes")
```



```dax
Single Comment = 
var _c=  Trim(SELECTEDVALUE('Q8 CounterActions'[Comment]))
return  coalesce(_c,"")
```



```dax
Single Comment Short = if(ISBLANK([Single Comment]) || [Single Comment] = "", blank(),  left([Single Comment], 6) & "..")
```



```dax
Q8 No = calculate(COUNTROWS('Q8 CounterActions'), 'Q8 CounterActions'[Counteraction needed] = "No")
```


## Table: StaffingAll

### Calculated Columns:


```dax
DM = LOOKUPVALUE('rep v_hr_employee'[full_name],'rep v_hr_employee'[emp_id], StaffingAll[EmployeeIDDM])
```



```dax
PM = LOOKUPVALUE('rep v_hr_employee'[full_name],'rep v_hr_employee'[emp_id], StaffingAll[EmployeeIDPM])
```


## Table: Values by Staffing


```dax
ADDCOLUMNS(ParticipantsAndStaffing
, "xx", 1
 )
```


### Measures:


```dax
# distinct employees = Countrows(values('Values by Staffing'[emp_id])) 
```



```dax
_Q3 value = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , AVERAGE('Values by Staffing'[Q3 (< 12h)])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])

        return LOOKUPVALUE('Values by Project'[Q3], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
```



```dax
_Q3 color = 
if(not  HASONEVALUE('Calendar'[ShiftedWeekOffest]), "#FFFFFF",
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q3 (< 12h) Color])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])
        return LOOKUPVALUE('Values by Project'[Q3 color], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate) 
    )
)
)
```



```dax
_Q4 color = 
if(not  HASONEVALUE('Calendar'[ShiftedWeekOffest]), "#FFFFFF",
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q4 (next weeks) Color])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])
        return LOOKUPVALUE('Values by Project'[Q4 color], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
)
```



```dax
_Q4 value = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , AVERAGE('Values by Staffing'[Q4 (next weeks)])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])

        return LOOKUPVALUE('Values by Project'[Q4], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
```



```dax
_Q1 value = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , AVERAGE('Values by Staffing'[Q1])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])

        return LOOKUPVALUE('Values by Project'[Q1], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
```



```dax
_Q1 (-1) value = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , AVERAGE('Values by Staffing'[Q1 (-1)])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])

        return LOOKUPVALUE('Values by Project'[Q1(-1)], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
```



```dax
_Q1 (-2) value = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , AVERAGE('Values by Staffing'[Q1 (-2)])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])

        return LOOKUPVALUE('Values by Project'[Q1(-2)], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
```



```dax
_Q1 color = 
if(not  HASONEVALUE('Calendar'[ShiftedWeekOffest]), "#FFFFFF",
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q1 Color])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])
        return LOOKUPVALUE('Values by Project'[Q1 color], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
)
```



```dax
_Q1 (-1) color = 
if(not  HASONEVALUE('Calendar'[ShiftedWeekOffest]), "#FFFFFF",
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q1 (-1) Color])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])
        return LOOKUPVALUE('Values by Project'[Q1 (-1) color], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
)
```



```dax
_Q1 (-2) color = 
if(not  HASONEVALUE('Calendar'[ShiftedWeekOffest]), "#FFFFFF",
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q1 (-2) Color])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])
        return LOOKUPVALUE('Values by Project'[Q1 (-2) color], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
)
```



```dax
_Q2 value = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , AVERAGE('Values by Staffing'[Q2])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])

        return LOOKUPVALUE('Values by Project'[Q2], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
```



```dax
_Q2 (-1) value = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , AVERAGE('Values by Staffing'[Q2 (-1)])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])

        return LOOKUPVALUE('Values by Project'[Q2(-1)], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
```



```dax
_Q2 (-2) value = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , AVERAGE('Values by Staffing'[Q2 (-2)])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])

        return LOOKUPVALUE('Values by Project'[Q2(-2)], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
```



```dax
_Q2 color = 
if(not  HASONEVALUE('Calendar'[ShiftedWeekOffest]), "#FFFFFF",
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q2 Color])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])
        return LOOKUPVALUE('Values by Project'[Q2 color], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
)
```



```dax
_Q2 (-1) color = 
if(not  HASONEVALUE('Calendar'[ShiftedWeekOffest]), "#FFFFFF",
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q2 (-1) Color])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])
        return LOOKUPVALUE('Values by Project'[Q2 (-1) color], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
)
```



```dax
_Q2 (-2) color = 
if(not  HASONEVALUE('Calendar'[ShiftedWeekOffest]), "#FFFFFF",
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q2 (-2) Color])
    ,  if(ISINSCOPE(Projetcs[Project]), 
        var _projectNumber = min(Projetcs[ProjectNumber])
        var _refDate = min('Values by Staffing'[Reference Date])
        return LOOKUPVALUE('Values by Project'[Q2 (-2) color], 'Values by Project'[ProjectNumber], _projectNumber, 'Values by Project'[Reference Date], _refDate)
    )
)
)
```



```dax
_Q8 icon = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q8 CA icon])
)
```



```dax
_Q8 (-1) icon = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q8 CA - 1 icon])
)
```



```dax
_Q8 comment = 
if(ISINSCOPE('rep v_hr_employee'[full_name])
    , min('Values by Staffing'[Q8 Comment])
)
```


### Calculated Columns:


```dax
Q3 (< 12h) = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

return  calculate([Q3], all('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset)
```



```dax
Q3 (< 12h) Color = 

var _value = 'Values by Staffing'[Q3 (< 12h)]
var _emp_id = 'Values by Staffing'[emp_id]

var _answerCount =  'Values by Staffing'[Q3 answerCount]
        return switch(_answerCount
        , blank(), "#FFFFFF"
        , 0, "#FFFFFF"
        , 1,  [Color_Insufficient] -- gray
        , 2, 
            switch(true()
            , _value < 0.5, [cRed] 
            , _value < 1, [cOrange]
            , [cGreen]
            )
        , 3, 
            switch(true()
            , _value < 0.5, [cRed] 
            //, _value < 0.75, _cOrange
            , [cGreen]
            )
        , 4, 
            switch(true()
            , _value < 0.5, [cRed] 
            , _value < 0.75, [cOrange]
            , [cGreen]
            )
        ,  
            switch(true()
            , _value < 0.5, [cRed] 
            , _value < 0.75, [cOrange]
            , [cGreen]
            )
        )
```



```dax
Q3 answerCount = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

return calculate(COUNTROWS('Q3 DidYouWorkLessThan12Hours'), All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q3 DidYouWorkLessThan12Hours'[Mail] = _emp_mail ) 
```



```dax
Q4 (next weeks) = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

return calculate( [Q4 +1], All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q4 WorkloadNext2Weeks'[Mail] = _emp_mail )
```



```dax
Q4 (next weeks) Color = 
var _value = 'Values by Staffing'[Q4 (next weeks)]
return switch(true()
            , isblank(_value), blank()
            , _value = 0, [cRed]
            , _value < 1, [cOrange]
            , [cGreen]
            )
```



```dax
Q1 = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

return calculate( [Q1], REMOVEFILTERS('Calendar'[Date]), REMOVEFILTERS('Q1 WereWorkingHoursWithinLimits'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q1 WereWorkingHoursWithinLimits'[Mail] = _emp_mail)
```



```dax
Q1 (-1) = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate) - 1

return calculate( [Q1], REMOVEFILTERS('Calendar'[Date]), REMOVEFILTERS('Q1 WereWorkingHoursWithinLimits'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q1 WereWorkingHoursWithinLimits'[Mail] = _emp_mail)
```



```dax
Q1 (-2) = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate) - 2

return calculate( [Q1], REMOVEFILTERS('Calendar'[Date]), REMOVEFILTERS('Q1 WereWorkingHoursWithinLimits'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q1 WereWorkingHoursWithinLimits'[Mail] = _emp_mail)
```



```dax
Q2 = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

return calculate( [Q2], REMOVEFILTERS('Calendar'[Date]), REMOVEFILTERS('Q2 DidYouWorkOnTheWeekend'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q2 DidYouWorkOnTheWeekend'[Mail] = _emp_mail)
```



```dax
Q2 (-1) = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate) - 1

return calculate( [Q2], REMOVEFILTERS('Calendar'[Date]), REMOVEFILTERS('Q2 DidYouWorkOnTheWeekend'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q2 DidYouWorkOnTheWeekend'[Mail] = _emp_mail)
```



```dax
Q2 (-2) = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate) - 2

return calculate( [Q2], REMOVEFILTERS('Calendar'[Date]), REMOVEFILTERS('Q2 DidYouWorkOnTheWeekend'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q2 DidYouWorkOnTheWeekend'[Mail] = _emp_mail)
```



```dax
Q6/Q7 Hours = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

var _res =  calculate([Q6/Q7 Hours], All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q6 HoursSpentOutsideProjectWorkdays'[Mail] = _emp_mail,  'Q7 HoursSpentOutsideProjectWeekend'[Mail] = _emp_mail )
return if(_res = 0, Blank(), _res)
```



```dax
Q6/Q7 Count = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

var _res = calculate([Q6/Q7 Count], All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q6 HoursSpentOutsideProjectWorkdays'[Mail] = _emp_mail,  'Q7 HoursSpentOutsideProjectWeekend'[Mail] = _emp_mail )
return if(_res = 0, Blank(), _res) 
```



```dax
Q8 Comment = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

var _res = calculate([Single Comment], All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q8 CounterActions'[Mail] = _emp_mail)
return _res 
```



```dax
Q8 CA = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

var _res = calculate(if( [Q8 Yes]>0,[Q8 Yes], -1 * [Q8 No]), All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q8 CounterActions'[Mail] = _emp_mail )
return  _res
```



```dax
Q8 CA icon = 
if('Values by Staffing'[Q8 CA] > 0, [Icon Exclamation Red],  if ('Values by Staffing'[Q8 CA] < 0 , [Icon Cross], ""))
```



```dax
Q8 CA - 1 = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate) - 1

var _res = calculate(if( [Q8 Yes]>0,[Q8 Yes], -1 * [Q8 No]), All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q8 CounterActions'[Mail] = _emp_mail )
return  _res
```



```dax
Q8 CA - 1 icon = 
if('Values by Staffing'[Q8 CA - 1] > 0, [Icon Exclamation Red],  if ('Values by Staffing'[Q8 CA - 1] < 0 , [Icon Cross], ""))
```



```dax
Q4 (next weeks) state = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

return coalesce( calculate( min('Q4 WorkloadNext2Weeks'[NextWeek]), All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q4 WorkloadNext2Weeks'[Mail] = _emp_mail ), "no answer")
```



```dax
Q1 Color = 
var _value = 'Values by Staffing'[Q1]
return switch(true()
    , isblank(_value), blank()
    , _value = 0, [cRed]
    , _value = 1, [cGreen]
    , [cOrange]
)
```



```dax
Q1 (-1) Color = 
var _value = 'Values by Staffing'[Q1 (-1)]
return switch(true()
    , isblank(_value), blank()
    , _value = 0, [cRed]
    , _value = 1, [cGreen]
    , [cOrange]
)
```



```dax
Q1 (-2) Color = 
var _value = 'Values by Staffing'[Q1 (-2)]
return switch(true()
    , isblank(_value), blank()
    , _value = 0, [cRed]
    , _value = 1, [cGreen]
    , [cOrange]
)
```



```dax
Q2 Color = 
var _value = 'Values by Staffing'[Q2]
return switch(true()
    , isblank(_value), blank()
    , _value = 0, [cRed]
    , _value = 1, [cGreen]
    , [cOrange]
)
```



```dax
Q2 (-1) Color = 
var _value = 'Values by Staffing'[Q2 (-1)]
return switch(true()
    , isblank(_value), blank()
    , _value = 0, [cRed]
    , _value = 1, [cGreen]
    , [cOrange]
)
```



```dax
Q2 (-2) Color = 
var _value = 'Values by Staffing'[Q2 (-2)]
return switch(true()
    , isblank(_value), blank()
    , _value = 0, [cRed]
    , _value = 1, [cGreen]
    , [cOrange]
)
```



```dax
Employee details = "Mentor: " & [Mentor by Employee] & "
Platform: " & 'Values by Staffing'[platform_1_name] & "
Country: " & 'Values by Staffing'[country]
```



```dax
Absence days = 
var _emp_id = 'Values by Staffing'[emp_id]
var _reference_date = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _reference_date)

var _week_start = calculate(min('Calendar'[Date]), All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset)
var _week_end = calculate(max('Calendar'[Date]), All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset)

var _absence_staffing = CALCULATETABLE(StaffingAll, StaffingAll[EmployeeID] = _emp_id, ( StaffingAll[Status] = 6 || StaffingAll[Status] = 58), StaffingAll[StartDate] <= _week_end && StaffingAll[EndDate] >= _week_start) 

var _sum = sumX(_absence_staffing
    , 
            VAR MaxStart = MAX(_week_start, StaffingAll[StartDate])
            VAR MinEnd = MIN(_week_end, StaffingAll[EndDate])
            RETURN
                IF(MaxStart <= MinEnd, MinEnd - MaxStart + 1, 0)
    )
return _sum
```



```dax
Q1 state = 
var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

return coalesce( 
    switch( calculate( min('Q1 WereWorkingHoursWithinLimits'[Q1 Value]), All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q1 WereWorkingHoursWithinLimits'[Mail] = _emp_mail )
    , 1, "Yes"
    , 0, "No"
), "n/a")
```



```dax
Q6/Q7 state = 

var _emp_mail = 'Values by Staffing'[participant_email]
var _refDate = 'Values by Staffing'[Reference Date]

var _shifted_week_offset = LOOKUPVALUE('Calendar'[ShiftedWeekOffest], 'Calendar'[Date], _refDate)

var _res = calculate(COUNTROWS('Q6 HoursSpentOutsideProjectWorkdays') + COUNTROWS('Q7 HoursSpentOutsideProjectWeekend'), All('Calendar'), 'Calendar'[ShiftedWeekOffest] = _shifted_week_offset, 'Q6 HoursSpentOutsideProjectWorkdays'[Mail] = _emp_mail,  'Q7 HoursSpentOutsideProjectWeekend'[Mail] = _emp_mail )

return switch(true
, ISBLANK(_res), "n/a" 
, 'Values by Staffing'[Q6/Q7 Hours] <= 5, "0-5h" 
, 'Values by Staffing'[Q6/Q7 Hours] <= 10, "5,01-10h"
, 'Values by Staffing'[Q6/Q7 Hours] > 10, ">10h"
, "n/aaa"
)
```


## Table: Values by Project


```dax

SUMMARIZE('Values by Staffing'
    , 'Values by Staffing'[Reference Date], Projetcs[ProjectNumber]
    , "Q3", calculate(AVERAGEX ('Values by Staffing', 'Values by Staffing'[Q3 (< 12h)]), 'Values by Staffing'[Q3 answerCount] >=2)  
    //, "Q3", AVERAGE('Values by Staffing'[Q3 (< 12h)])  
    , "Q4", AVERAGE('Values by Staffing'[Q4 (next weeks)])  
    , "Q1", AVERAGE('Values by Staffing'[Q1])  
    , "Q1(-1)", AVERAGE('Values by Staffing'[Q1 (-1)])
    , "Q1(-2)", AVERAGE('Values by Staffing'[Q1 (-2)])
    , "Q2", AVERAGE('Values by Staffing'[Q2])  
    , "Q2(-1)", AVERAGE('Values by Staffing'[Q2 (-1)])
    , "Q2(-2)", AVERAGE('Values by Staffing'[Q2 (-2)])
)
```


### Calculated Columns:


```dax
Q3 color = 
var _value = 'Values by Project'[Q3]
return switch(true()
    , _value = blank(), "#FFFFFF"
    , _value <= 0.33, [cRed]
    , _value <= 0.66, [cOrange]
    , [cGreen]
)
```



```dax
Q4 color = 
var _value = 'Values by Project'[Q4]
return switch(true()
    , isblank(_value), "#FFFFFF"
    , _value < 0.34, [cRed]
    , _value < 0.67, [cOrange]
    , [cGreen]
)
```



```dax
Q1 color = 
var _value = 'Values by Project'[Q1]
return switch(true()
    , isblank(_value),  "#FFFFFF"
    , _value < 0.34, [cRed]
    , _value < 0.67, [cOrange]
    , [cGreen]
)
```



```dax
Q1 (-1) color = 
var _value = 'Values by Project'[Q1(-1)]
return switch(true()
    , isblank(_value),  "#FFFFFF"
    , _value < 0.34, [cRed]
    , _value < 0.67, [cOrange]
    , [cGreen]
)
```



```dax
Q1 (-2) color = 
var _value = 'Values by Project'[Q1(-2)]
return switch(true()
    , isblank(_value),  "#FFFFFF"
    , _value < 0.34, [cRed]
    , _value < 0.67, [cOrange]
    , [cGreen]
)
```



```dax
Q2 color = 
var _value = 'Values by Project'[Q2]
return switch(true()
    , isblank(_value),  "#FFFFFF"
    , _value < 0.34, [cRed]
    , _value < 0.67, [cOrange]
    , [cGreen]
)
```



```dax
Q2 (-1) color = 
var _value = 'Values by Project'[Q2(-1)]
return switch(true()
    , isblank(_value),  "#FFFFFF"
    , _value < 0.34, [cRed]
    , _value < 0.67, [cOrange]
    , [cGreen]
)
```



```dax
Q2 (-2) color = 
var _value = 'Values by Project'[Q2(-2)]
return switch(true()
    , isblank(_value),  "#FFFFFF"
    , _value < 0.34, [cRed]
    , _value < 0.67, [cOrange]
    , [cGreen]
)
```

