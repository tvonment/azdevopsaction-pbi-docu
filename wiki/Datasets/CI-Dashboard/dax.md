



# DAX

|Dataset|[CI Dashboard](./../CI-Dashboard.md)|
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



```dax
Approved YTD = 
var _year = SELECTEDVALUE(dimDate[Year])

var _toDate = [CurrentDate]

return calculate([Budget], Filter(allselected(dimdate), dimDate[Date] <= _toDate), 'fact budget'[status] = "Approved")
```



```dax
Approved Total - YTD = [Approved Total] - [Approved YTD]
```



```dax
Planned = calculate([Budget], 'fact budget'[status] = "Planned")
```



```dax
StackedColumnValue = 
switch(min(FormatStackedColumns[ValueType])
, "Approved YTD",[Approved YTD]
, "Approved Total - YTD", [Approved Total - YTD]
, "Planned",[Planned]
, "Actual", [Actual YTD]
, "Remaining", 
    var _res = [Approved Total] + [Planned] - [Actual YTD]
    return if( _res > 0, _res, blank())
)
```



```dax
Approved Total = calculate([Budget], 'fact budget'[status] = "Approved")
```



```dax
Measure = 
var _year = min( dimDate[Year])
var _month = min( Months[Month])
var _toDate = EOMONTH( 
    Date(_year, _month, 1)
    , 0 )

return _toDate
```



```dax
Actual YTD = 
var _year = SELECTEDVALUE(dimDate[Year])

var _toDate = [CurrentDate]
return CALCULATE(sum('fact cost byd'[amount_company]), filter(ALLSELECTED(dimDate), dimDate[Year] = _year && dimDate[date] <=_toDate), TREATAS(values('fact budget'[sap_project_task_id]), 'fact cost byd'[project_task_id]))
```



```dax
Approved YTD by month (no future) = 
var _year = min( dimDate[Year])
var _month = min( dimDate[MonthofYear])
var _toDate = EOMONTH( 
    Date(_year, _month, 1)
    , 0 )

return if(_toDate > [StatusDate]
    , blank()
    , calculate([Budget], Filter(allselected(dimdate), dimDate[Date] <= _toDate), 'fact budget'[status] = "Approved")
)
```



```dax
StatusDate = 
var _year = min( dimDate[Year])
var _month = min( Months[Month])
return EOMONTH( 
    Date(_year, _month, 1)
    , 0 )
```



```dax
Budget Total = [Approved Total] + [Planned]
```



```dax
Actual by Month and project cumulated = 
var _year = SELECTEDVALUE(dimDate[year])
var _maxDate = calculate(MAX(dimDate[Date]), ALLSELECTED(dimDate[Date]))
var _projects = values('project tasks'[project_id])
var _contact = SELECTEDVALUE('dim Contacts'[contact])

var _tasksWithBudget = calculateTable(values('fact budget'[sap_project_task_id]), all('fact budget'), year( 'fact budget'[month] ) = year(_maxDate), 'fact budget'[contact] = _contact )

return if(_maxDate > [CurrentDate] && not(year(_maxDate) = year([CurrentDate]) && month(_maxDate) = month([CurrentDate]) )
    , blank()
    ,  CALCULATE(sum('fact cost byd'[amount_company]), filter(all(dimDate), dimDate[Year] = _year && dimDate[date] <=_maxDate), TREATAS(_tasksWithBudget, 'fact cost byd'[project_task_id]))
)

```



```dax
CurrentDate = Now()
```



```dax
Budget YTD = 
var _year = SELECTEDVALUE(dimDate[Year])

var _toDate = [CurrentDate]

return calculate([Budget], Filter(allselected(dimdate), dimDate[Date] <= _toDate))
```



```dax
Delta YTD = [Budget YTD] - [Actual YTD]
```



```dax
Not Approved = [Budget Total] - [Approved Total]
```



```dax
Filter_HasBudgetData = 
COUNTROWS('fact budget')
```



```dax
Budget YTD (100) = Round( [Budget YTD] / 100,0) * 100
```



```dax
Actual YTD (100) = Round( [Actual YTD] / 100,0) * 100
```



```dax
Delta YTD (100) = Round([Delta YTD] / 100,0) * 100
```



```dax
Budget approved (100) = Round( [Approved Total] / 100,0) * 100
```



```dax
Budget planned (100) = Round( [Planned] / 100,0) * 100
```



```dax
Budget Total (100) = Round( [Budget Total] / 100,0) * 100
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



```dax
Link = if(HASONEVALUE('fact cost byd'[source_document_id]),  "https://my314590-sso.sapbydesign.com/sap/public/ap/ui/runtime?bo_ns=http://sap.com/xi/AP/SupplierInvoicing/Global&bo=SupplierInvoice&node=Root&operation=Open&object_key=" & SELECTEDVALUE( 'fact cost byd'[source_document_id]) & "&key_type=APC_S_BTD_ID")
```


## Table: project tasks

### Measures:


```dax
HasCost = if( [Cost ICS]> 0 || [Cost BYD] > 0 , 1 ,0)
```


### Calculated Columns:


```dax
Project Id and Name = 'project tasks'[project_id] & " " & 'project tasks'[Project]
```

