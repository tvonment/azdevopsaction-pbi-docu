



# DAX

|Dataset|[BEM](./../BEM.md)|
| :--- | :--- |
|Workspace|[HR_BEM](../../Workspaces/HR_BEM.md)|

## Table: Query1

### Measures:


```dax
Today = TODAY()
```


### Calculated Columns:


```dax
KW = WEEKNUM(Query1[CALENDAR_DAY])
```



```dax
Name = CONCATENATE(RELATED(vEMPLOYEES[LAST_NAME]), " " & RELATED(vEMPLOYEES[FIRST_NAME]))
```



```dax
Column = COUNTAX(FILTER(Query1,Query1[EMPLOYEE_ID]=Query1[EMPLOYEE_ID]), Query1[ILLNESS])/COUNTAX(FILTER(Query1,Query1[EMPLOYEE_ID]=Query1[EMPLOYEE_ID]), Query1[CALENDAR_DAY])
```



```dax
Year-KW = year(Query1[CALENDAR_DAY]) & "-" & Format(Query1[KW], "00")
```



```dax
Year = Year(Query1[CALENDAR_DAY])
```



```dax
Übersicht = "Übersicht" 
```



```dax
IsInCompleetWeekIntervals = if(Query1[CALENDAR_DAY] >= [First Complete Week] && (Query1[CALENDAR_DAY] <= [Last Complete Week]), 1)
```


## Table: vEMPLOYEES

### Measures:


```dax
SickDays = calculate(COUNTROWS(values(Query1[CALENDAR_DAY])), Query1[ILLNESS]>0)
```



```dax
WorkDays = calculate(COUNTROWS(values(Query1[CALENDAR_DAY])))
```



```dax
%Sick per week = 
if(HASONEVALUE(Query1[Year-KW]),
 Divide([SickDays], [WorkDays] )
,   var _weeks = calculatetable(values(Query1[Year-KW]), Query1[IsInCompleetWeekIntervals] >= 1)
    return CALCULATE(SUMX(_weeks, Divide([SickDays], [WorkDays] )))
)
```



```dax
Is one  employee selected = 
if(calculate(HASONEVALUE(vEMPLOYEES[Name]), ALLSELECTED(vEMPLOYEES[Name])), 1)
```



```dax
Anzahl Mitarbeiter = COUNTrows(values(vEMPLOYEES[EMPLID]))
```


### Calculated Columns:


```dax
Name = vEMPLOYEES[LAST_NAME] & " " & vEMPLOYEES[FIRST_NAME]
```



```dax
% Total Sick = 
CALCULATE(sum(AggregatedData[%Sick]))

```



```dax
WochenCluster = 
var _sick =  [%Sick per week] *100
return coalesce(calculate(min(WochenCluster[Anzahl Wochen Arbeitsunfähigkeit]), _sick >= WochenCluster[biggerOrEqual] && ( isblank(WochenCluster[smallerThan] ) ||  _sick < WochenCluster[smallerThan] ))
, "2 to < 3")
    

```



```dax
WochenClusterValue = 
 [%Sick per week] *100
```



```dax
IsExit = if( not isblank(vEMPLOYEES[ter_max_date]) && vEMPLOYEES[ter_max_date] < [Last Complete Week], true)
```



```dax
Firmenzugehörigkeit Jahre = DATEDIFF(vEMPLOYEES[last_hire_date],NOW(),YEAR)
```



```dax
Firmenzugehörigkeit = 
Switch(TRUE()
    , vEMPLOYEES[Firmenzugehörigkeit Jahre] < 2, "< 2 years"
    , vEMPLOYEES[Firmenzugehörigkeit Jahre] < 5, "2 to < 5 years"
    , vEMPLOYEES[Firmenzugehörigkeit Jahre] < 10, "5 to < 10 years"
    , "10 and more"
)
```


## Table: AggregatedData

### Calculated Columns:


```dax
%Sick = AggregatedData[SickDays]/AggregatedData[WorkDays]
```



```dax
Date = DATE(AggregatedData[Year],AggregatedData[Month],1)
```


## Table: WochenclusterFilter


```dax
WochenCluster
```


## Table: Calculated Date Filter

### Measures:


```dax
First Complete Week = min('Calculated Date Filter'[First Complete Week Column])
```



```dax
Last Complete Week = max('Calculated Date Filter'[Last Complete Week Column])
```


### Calculated Columns:


```dax
First Complete Week Column = calculate(min(Query1[CALENDAR_DAY]), Weekday(Query1[CALENDAR_DAY], 2) = 1)
```



```dax
Last Complete Week Column = calculate(max(Query1[CALENDAR_DAY]), Weekday(Query1[CALENDAR_DAY], 2) = 5)
```

