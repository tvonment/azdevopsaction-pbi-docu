



# DAX

|Dataset|[Recruiting Hires](./../Recruiting-Hires.md)|
| :--- | :--- |
|Workspace|[Global Recruiting](../../Workspaces/Global-Recruiting.md)|

## Table: DimDate


```dax
CALENDAR (
    DATE ( 2021, 1, 1 ),
    MAX(v_rep_hire[Application Creation Date])
)
```


### Measures:


```dax
CurrentDate = Today() 
```


### Calculated Columns:


```dax
Year = Year(DimDate[Date])
```



```dax
Month = month(DimDate[Date])
```



```dax
EndofMonth = ENDOFMONTH(DimDate[Date]) 
```



```dax
Last 12 Months = 
var _today = TODAY()
var _startOfMonth = DATE(year(_today), month(_today), 1)
var _startOfLast12Months = EDATE(_startOfMonth, -13)

return SWITCH(true
        , DimDate[Date] > _today, "Futute"
        , DimDate[Date] >= _startOfLast12Months, "Last 12 Months"
        , "Older"
)
```



```dax
YTD = 
var _today = TODAY()
var _curYear = year(_today)


return SWITCH(true
        , DimDate[Date] > _today, "Futute"
        , year(DimDate[Date]) = _curYear, "YTD"
        , "Older"
)
```


## Table: v_rep_hire

### Measures:


```dax
# of applications = COUNTROWS(values(v_rep_hire[Application ID]))
```



```dax
# of Application Female = CALCULATE( DISTINCTCOUNT(v_rep_hire[Application ID]), FILTER(v_rep_hire, v_rep_hire[Gender]="f"))
```



```dax
# of Application Male = CALCULATE( DISTINCTCOUNT(v_rep_hire[Application ID]), FILTER(v_rep_hire, v_rep_hire[Gender]="m"))
```



```dax
# of Applicaton Other = CALCULATE( DISTINCTCOUNT(v_rep_hire[Application ID]), FILTER(v_rep_hire, v_rep_hire[Gender]="Other"))
```



```dax
# YTD of applications = 
var _curYear =  year([CurrentDate])
return CALCULATE( COUNTROWS(values(v_rep_hire[Application ID])), YEAR(v_rep_hire[Application Creation Date]) =_curYear)
```



```dax
# YTD Female Application = CALCULATE( [# YTD of applications], FILTER(v_rep_hire, v_rep_hire[Gender]="f"))
```



```dax
# YTD Male Application = CALCULATE( [# YTD of applications], FILTER(v_rep_hire, v_rep_hire[Gender]="m"))
```



```dax
# YTD Other Application = CALCULATE( [# YTD of applications], FILTER(v_rep_hire, v_rep_hire[Gender]="Other"))
```



```dax
# accepted (by creation date) = CALCULATE([# of applications],v_rep_hire[Application Status] = "HIRED"||v_rep_hire[Application Status] = "WITHDRAWN"  )
```



```dax
# hired (by start date) = calculate(DISTINCTCOUNT(v_rep_hire[Application ID]),ll_funnel_status[Funnel_Status] = "Hired")
```



```dax
acceptance rate = DIVIDE(v_rep_hire[# hired], [# offered])
```



```dax
# hired = calculate(DISTINCTCOUNT(v_rep_hire[Application ID]),v_rep_hire[Application Status] = "HIRED")
```



```dax
# withdrawn = calculate(DISTINCTCOUNT(v_rep_hire[Application ID]), v_rep_hire[Application Status] = "WITHDRAWN")
```



```dax
# offered = [# hired] + [# withdrawn]
```


### Calculated Columns:


```dax
Final = if(Related(ll_ats_status[IsFinal]), "Yes", "No")
```



```dax
Candidate = v_rep_hire[Candidate Last Name] &", " & v_rep_hire[Candidate First Name]
```


## Table: DateSelection


```dax
DISTINCT(DimDate[EndofMonth])
```


## Table: _Measures

### Measures:


```dax
# Last12Month Application = VAR currentDate = MAX(DateSelection[End of Month Date]) VAR previousDate = DATE(YEAR(currentDate), MONTH(currentDate)-12, DAY(currentDate) ) VAR Result = CALCULATE(v_rep_hire[# of applications], FILTER(DimDate, DimDate[EndofMonth]>= previousDate && DimDate[EndofMonth]<=currentDate)) Return Result
```



```dax
#Last12Mon_Female = CALCULATE([# Last12Month Application], FILTER(v_rep_hire, v_rep_hire[Gender]="f"))
```



```dax
#Last12Mon_Male = CALCULATE([# Last12Month Application], FILTER(v_rep_hire, v_rep_hire[Gender]="m"))
```



```dax
#Last12Mon_Other = CALCULATE([# Last12Month Application], FILTER(v_rep_hire, v_rep_hire[Gender]="Other"))
```


## Table: DimDateStart


```dax
CALENDAR (
    DATE ( 2021, 1, 1 ),
    MAX(v_rep_hire[Application Start Date])
)
```


### Calculated Columns:


```dax
EndofMonth = ENDOFMONTH(DimDateStart[Date]) 
```

