



# DAX

|Dataset|[Recruiting Dashboard](./../Recruiting-Dashboard.md)|
| :--- | :--- |
|Workspace|[Global Recruiting](../../Workspaces/Global-Recruiting.md)|

## Table: DimDate


```dax
CALENDAR (
    DATE ( 2021, 1, 1 ),
    MAX(v_rep_data_diverstiy[Application Creation Date])
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
YearOffset = DimDate[Year] -  min(CurrentYear[CurrentYear]) 
```



```dax
Month = month(DimDate[Date])
```



```dax
MonthOffest = -1 * ( ((min(CurrentYear[CurrentYear]) - Year(DimDate[Date]))*12) +  min(CurrentMonth[CurrentMonth]) - Month(DimDate[Date]))
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


## Table: InvervalHelper


```dax

var cy = min(CurrentYear[CurrentYear])
return {(FORMAT(cy-2, ""), Date(cy-2, 1, 1), "Prev" )
            , (FORMAT(cy-1, ""), Date(cy-1, 1, 1), "Prev" )
         , (FORMAT(cy, "") & "-1", Date( cy,1,1), "Current") 
         , (FORMAT(cy, "") & "-2", Date( cy,2,1), "Current") 
         , (FORMAT(cy, "") & "-3", Date( cy,3,1), "Current") 
         , (FORMAT(cy, "") & "-4", Date( cy,4,1), "Current") 
         , (FORMAT(cy, "") & "-5", Date( cy,5,1), "Current") 
         , (FORMAT(cy, "") & "-6", Date( cy,6,1), "Current") 

         , (FORMAT(cy, "") & "-7", Date( cy,7,1), "Current") 
         , (FORMAT(cy, "") & "-8", Date( cy,8,1), "Current") 
         , (FORMAT(cy, "") & "-9", Date( cy,9,1), "Current") 
         , (FORMAT(cy, "") & "-10", Date( cy,10,1), "Current") 
         , (FORMAT(cy, "") & "-11", Date( cy,11,1), "Current") 
         , (FORMAT(cy, "") & "-12", Date( cy,12,1), "Current") 
         
         } 
```


### Measures:


```dax
% female hires for interval = 



var dateFrom = min(InvervalHelper[From])
var dateTo = max(InvervalHelper[To])

var totalHires = CALCULATE([# total hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo))

return  if(totalHires = 0, "-", CALCULATE([% female hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo)))
//var female = CALCULATE([# female hires], filter( all(DimDate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo))
//var male = CALCULATE([# male hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo))

//return divide (female , female + male, 0)
```



```dax
# female hires for interval = 
var dateFrom = min(InvervalHelper[From])
var dateTo =max(InvervalHelper[To])

return coalesce(CALCULATE([# female hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo)), 0)
```



```dax
# male hires for interval = 
var dateFrom = min(InvervalHelper[From])
var dateTo =max(InvervalHelper[To])

return coalesce(CALCULATE([# male hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo)), 0)
```



```dax
% male hires for interval = 



var dateFrom = min(InvervalHelper[From])
var dateTo = max(InvervalHelper[To])

var totalHires = CALCULATE([# total hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo))

return  if(totalHires = 0, "-", CALCULATE([% male hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo)))
```


### Calculated Columns:


```dax
To = if(InvervalHelper[YearType] ="Prev", ENDOFYEAR(DimDate[Date]), ENDOFMONTH(DimDate[Date]))
```



```dax
Display = if(year(InvervalHelper[From])< min(CurrentYear[CurrentYear]) || month(InvervalHelper[From]) <= min( CurrentMonth[CurrentMonth]), 1, 0)
```


## Table: v_rep_data_diverstiy

### Measures:


```dax
# of applications = COUNTROWS(values(v_rep_data_diverstiy[Application ID]))
```



```dax
# values = sum(v_rep_data_diverstiy[Value])
```



```dax
# of Application Female = CALCULATE( COUNTROWS(values(v_rep_data_diverstiy[Application ID])), FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="f"))
```



```dax
# of Application Male = CALCULATE( COUNTROWS(values(v_rep_data_diverstiy[Application ID])), FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="m"))
```



```dax
# of Applicaton Other = CALCULATE( COUNTROWS(values(v_rep_data_diverstiy[Application ID])), FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="Other"))
```



```dax
# YTD of applications = 
var _curYear =  year([CurrentDate])
return CALCULATE( COUNTROWS(values(v_rep_data_diverstiy[Application ID])), YEAR(v_rep_data_diverstiy[Application Creation Date]) =_curYear)
```



```dax
# YTD Female Application = CALCULATE( [# YTD of applications], FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="f"))
```



```dax
# YTD Male Application = CALCULATE( [# YTD of applications], FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="m"))
```



```dax
# YTD Other Application = CALCULATE( [# YTD of applications], FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="Other"))
```


### Calculated Columns:


```dax
Value = if(RELATED(ll_funnel_status[Funnel_Status]) in {"Reject", "No Success", "No Succes", "Declined Offer"}, -1, 1)
```



```dax
Final = if(v_rep_data_diverstiy[IsFinal], "Yes", "No")
```


## Table: DateSelection


```dax
DISTINCT(DimDate[EndofMonth])
```


## Table: _Measures

### Measures:


```dax
# Last12Month Application = VAR currentDate = MAX(DateSelection[End of Month Date]) VAR previousDate = DATE(YEAR(currentDate), MONTH(currentDate)-12, DAY(currentDate) ) VAR Result = CALCULATE(v_rep_data_diverstiy[# of applications], FILTER(DimDate, DimDate[EndofMonth]>= previousDate && DimDate[EndofMonth]<=currentDate)) Return Result
```



```dax
#Last12Mon_Female = CALCULATE([# Last12Month Application], FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="f"))
```



```dax
#Last12Mon_Male = CALCULATE([# Last12Month Application], FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="m"))
```



```dax
#Last12Mon_Other = CALCULATE([# Last12Month Application], FILTER(v_rep_data_diverstiy, v_rep_data_diverstiy[Gender]="Other"))
```

