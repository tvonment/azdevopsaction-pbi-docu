



# DAX

|Dataset|[proEvaluation Report](./../proEvaluation-Report.md)|
| :--- | :--- |
|Workspace|[proEvaluation [Prod]](../../Workspaces/proEvaluation-[Prod].md)|

## Table: v_napta_staffing_project_days_per_week

### Measures:


```dax
total days = CALCULATE(
    SUM(v_napta_staffing_project_days_per_week[DaysAssigned]),
    ALL('rep v_napta_staffing_project_days_per_week')
)+0
```



```dax
projectIsInRange old = 
var project_start = CALCULATE(
    min(v_napta_staffing_project_days_per_week[dt_week_start]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number],v_napta_staffing_project_days_per_week[EmployeeID])
)
var project_end = CALCULATE(
    max(v_napta_staffing_project_days_per_week[dt_week_end]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number],v_napta_staffing_project_days_per_week[EmployeeID])
)
var slicer_start = CALCULATE(
    min('pub dim_date'[Date]),
    ALL('temp pub dim_date_assignments'[Date])
)
var slicer_end = CALCULATE(
    max('pub dim_date'[Date]),
    ALL('temp pub dim_date_assignments'[Date])
)
return
if(project_start <= slicer_end && project_end >= slicer_start,1,0)
```



```dax
<dev>projectStart = 
var project_start = CALCULATE(
    min(v_napta_staffing_project_days_per_week[dt_week_start]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number])
)
return project_start
```



```dax
<dev>projectEnd = 
var project_end = CALCULATE(
    max(v_napta_staffing_project_days_per_week[dt_week_end]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number])
)
return project_end
```



```dax
DaysAssigned_Dynamic = 
var slicer_start = CALCULATE(
    min('temp pub dim_date_assignments'[Date]),
    ALL('pub dim_date'[Date])
)
var slicer_end = CALCULATE(
    max('temp pub dim_date_assignments'[Date]),
    ALL('pub dim_date'[Date])
)
return 
SUMX(
    FILTER(v_napta_staffing_project_days_per_week, 
        v_napta_staffing_project_days_per_week[dt_week_start] <= slicer_end && v_napta_staffing_project_days_per_week[dt_week_end] >= slicer_start),
    v_napta_staffing_project_days_per_week[DaysAssigned]
)+0
```



```dax
project assignment start old = 
CALCULATE(
    min(v_napta_staffing_project_days_per_week[dt_week_start]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number],
        v_napta_staffing_project_days_per_week[EmployeeID])
)
```



```dax
project assignment end old = 
CALCULATE(
    max(v_napta_staffing_project_days_per_week[dt_week_end]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number],
        v_napta_staffing_project_days_per_week[EmployeeID])
)
```



```dax
project assignment end = 
CALCULATE(
    max(v_napta_staffing_project_days_per_week[max_staffing_end_date]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number],
        v_napta_staffing_project_days_per_week[EmployeeID])
)
```



```dax
project assignment start = 
CALCULATE(
    min(v_napta_staffing_project_days_per_week[min_staffing_start_date]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number],
        v_napta_staffing_project_days_per_week[EmployeeID])
)
```



```dax
projectIsInRange = 
var project_start = CALCULATE(
    min(v_napta_staffing_project_days_per_week[min_staffing_start_date]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number],v_napta_staffing_project_days_per_week[EmployeeID])
)
var project_end = CALCULATE(
    max(v_napta_staffing_project_days_per_week[max_staffing_end_date]),
    ALLEXCEPT(v_napta_staffing_project_days_per_week,v_napta_staffing_project_days_per_week[project_number],v_napta_staffing_project_days_per_week[EmployeeID])
)
var slicer_start = CALCULATE(
    min('pub dim_date'[Date]),
    ALL('temp pub dim_date_assignments'[Date])
)
var slicer_end = CALCULATE(
    max('pub dim_date'[Date]),
    ALL('temp pub dim_date_assignments'[Date])
)
return
if(project_start <= slicer_end && project_end >= slicer_start,1,0)
```



```dax
test assigned vs total = IF([DaysAssigned_Dynamic] > SUM(v_napta_staffing_per_period[days_assigned]), 1, 0)
```


## Table: temp pub dim_date_assignments


```dax
CALENDARAUTO()
```

