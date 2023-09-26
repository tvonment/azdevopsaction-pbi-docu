



# DAX

|Dataset|[CI_Inspector](./../CI_Inspector.md)|
| :--- | :--- |
|Workspace|[CorporateInvestments](../../Workspaces/CorporateInvestments.md)|

## Table: dimDate


```dax
CALENDAR (DATE (2020, 1, 1), DATE (2023, 12, 31))
```


### Measures:


```dax
isCurrentYear = if(year(max(dimDate[Date])) =  [Year], 1, 0)
```


### Calculated Columns:


```dax
Year = Year([Date])
```



```dax
Day = FORMAT([Date],"DDDD")
```



```dax
DayofMonth = DAY([date])
```



```dax
MonthofYear = MONTH([date])
```



```dax
Month = FORMAT([date],"MMM")&" "&[Year]
```



```dax
QuarterofYear = ROUNDUP (MONTH([Date])/3,0)
```



```dax
Quarter = "Q" & [QuarterofYear] & " " & [Year]
```



```dax
OrdinalDate = DATEDIFF([Year]&",1,1",[Date],DAY)+1
```



```dax
DayofWeek = WEEKDAY([Date],2)
```



```dax
WeekEnding = [Date] + (7- [DayofWeek])
```


## Table: Months

### Calculated Columns:


```dax
MonthName = FORMAT(DATEVALUE("2020-"& Months[Month] &"-1"),"MMM")
```


## Table: _measures

### Measures:


```dax
CY = 2021
```



```dax
LY = [CY] -1
```



```dax
Year = 2020 
```



```dax
ValueColor = if(ISINSCOPE('project tasks'[project_task_id]), "#dbedf4", if(ISINSCOPE('project tasks'[project_id]), "#99Adc2"))
```



```dax
MaxDate = max(dimDate[Date])
```


## Table: fact cost ics

### Measures:


```dax
Cost ICS = Sum('fact cost ics'[Costs]) 
```



```dax
CostToDate = if(min(dimDate[Date]) > TODAY()
                , blank()
                ,   CALCULATE([Cost ICS], filter(all(dimDate), dimDate[Date] <= max(dimDate[Date]) ))
            )
```



```dax
DeltaToToday = [PlannedToToday] - [CostToToday]
```



```dax
DeltaCY = [Plan] - [Cost]
```



```dax
Expected CY = [CostToToday] + [Plan rem] 
```



```dax
Delta exp = [Plan] - [Expected CY]
```



```dax
has  value = if(COUNTROWS(factPlanningByMonth) > 0 || COUNTROWS(factCost) > 0, 1, 0)
```


### Calculated Columns:


```dax
isCurrentYearCost = if(year('fact cost ics'[CostDate]) = [Year], 1, 0) 
```


## Table: fact budget

### Measures:


```dax
Cost ICS (by budget) = 
//var _ciids =ALLSELECTED('rep ci_budget'[CIID])
//var ciid =SELECTEDVALUE('rep ci_budget'[CIID])

//return 
sum('fact cost ics'[Costs])
//return CALCULATE(sum(factCost[Costs]),factCost[CIID] = ciid)
//return if(HASONEVALUE('rep ci_budget'[CIID])
//            , CALCULATE(sum(factCost[Costs]),factCost[CIID] = ciid)
//            , calculate(sum(factCost[Costs]), TREATAS(_ciids, factCost[CIID])))
```



```dax
Budget = sum('fact budget'[budget_month]) * 1000 
```



```dax
Delta ICS = 'fact budget'[Budget] - [Cost ICS (by budget)]
```



```dax
Cost BYD (by budget) = 
if(ISINSCOPE('CIIDs'[CIID]), blank(), sum('fact cost byd'[amount_company]))
```



```dax
Delta BYD = if(ISINSCOPE(CIIDs[CIID]),blank(),'fact budget'[Budget] - [Cost BYD (by budget)])
```



```dax
Cost ICS matched = CALCULATE([Cost ICS (by budget)], TREATAS(values('fact budget'[CIID]), 'fact cost ics'[CIID]))
```



```dax
Cost BYD matched = calculate([Cost BYD (by budget)], TREATAS(values('fact budget'[sap_project_task_id]), 'fact cost byd'[project_task_id])) 
```



```dax
Budget to month = 
var mon = SELECTEDVALUE(Months[Month])
return CALCULATE([Budget],filter(allselected(dimDate), month(dimDate[Date]) <= mon))
```



```dax
Delta to month = 
[Budget to month] - [Cost BYD matched to month]
```



```dax
Cost BYD matched to month = 
var mon = SELECTEDVALUE(Months[Month])
return CALCULATE([Cost BYD matched],filter(allselected(dimDate), month(dimDate[Date]) <= mon))
```



```dax
Budget Remaining after month = [Budget] - [Cost BYD matched to month]
```



```dax
Budget planned after month = 
var mon = SELECTEDVALUE(Months[Month])
return CALCULATE([Budget],filter(allselected(dimDate), month(dimDate[Date]) > mon))
```



```dax
Budget running total = 
var toDate = max(dimDate[Date])

return 
     calculate([Budget], Filter(allselected(dimdate), dimDate[Date] <= toDate))
   
```



```dax
Cost BYD matched running total (hide fututre) = 
var toDate = max(dimDate[Date])
var fromDate = min(dimDate[Date])
var stateMonth = SELECTEDVALUE(Months[Month])

return if(month(fromDate)<= stateMonth
    , [Cost BYD matched running total]
    , blank()
)
```



```dax
Cost BYD matched running total = 
var toDate = max(dimDate[Date])
var _year = SELECTEDVALUE(dimDate[Year])
var soy = DATE(_year, 1 ,1)

return  calculate([Cost BYD matched], FILTER(allselected(dimDate[Date]),dimDate[Date]  <= toDate && dimDate[Date] >= soy))
```



```dax
Cost BYD Forecast running = 
var fromDate = min(dimDate[Date])
var toDate = max(dimDate[Date])
var stateMonth = SELECTEDVALUE(Months[Month])
var _soy = date(SELECTEDVALUE(dimDate[Year]), 1,1)

var actuals = CALCULATE([Cost BYD matched running total (hide fututre)], dimDate[Date] <= toDate && dimDate[Date] >= _soy)
var forecast = CALCULATE([Budget], Filter(allselected(dimDate), dimDate[Date] <= toDate && month(dimDate[Date]) > stateMonth && dimDate[Date] >= _soy ))

return  actuals + forecast
```


## Table: fact cost byd

### Measures:


```dax
Cost BYD = Sum('fact cost byd'[amount_company])
```


## Table: project tasks

### Measures:


```dax
HasCost = if( [Cost ICS]> 0 || [Cost BYD] > 0 , 1 ,0)
```

