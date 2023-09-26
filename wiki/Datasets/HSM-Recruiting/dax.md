



# DAX

|Dataset|[HSM Recruiting](./../HSM-Recruiting.md)|
| :--- | :--- |
|Workspace|[Global Recruiting](../../Workspaces/Global-Recruiting.md)|

## Table: DimDate


```dax
CALENDAR (
    DATE ( 2020, 9, 1 ),
    MAX(v_rep_data_diverstiy[Application Creation Date])
)
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
# YTD of applications = CALCULATE( COUNTROWS(values(v_rep_data_diverstiy[Application ID])), YEAR(v_rep_data_diverstiy[Application Creation Date]) =2021)
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



```dax
# of appl. (0 if none for selected country) = 

var _selectedCountries = ALLSELECTED('dim region country'[country])

return if(ISINSCOPE('dim region country'[country]) && ISINSCOPE(ll_target_university[UniversityName])
&&
 (calculate (COUNTROWS(v_rep_data_diverstiy), _selectedCountries)>1
|| SELECTEDVALUE(ll_target_university[UniversityName]) = "Other"
 )
, 
    COALESCE([# of applications],0)
    , blank())
```


### Calculated Columns:


```dax
Value = if(RELATED(ll_funnel_status[Funnel_Status]) in {"Reject", "No Success", "No Succes", "Declined Offer"}, -1, 1)
```


## Table: ll_target_university

### Measures:


```dax
# Apply = CALCULATE([# of applications], ll_funnel_status[Funnel_Status] = "Apply")
```



```dax
# Invite = CALCULATE([# of applications], ll_funnel_status[Funnel_Status] = "Invite")
```



```dax
# Offer = CALCULATE([# of applications], ll_funnel_status[Funnel_Status] = "Offer")
```



```dax
# Hire = CALCULATE([# of applications], ll_funnel_status[Funnel_Status] = "Hire")
```



```dax
% Invite = divide ([# Invite], [# Apply])
```



```dax
% Hire / Offer = DIVIDE([# Hire], [# Offer])
```



```dax
% Hire / Invite = DIVIDE([# Hire], [# Invite])
```


### Calculated Columns:


```dax
UniType = if(ll_target_university[UniversityName] == "Other", "Sonstige Universitäten", "Zieluniversitäten")
```



```dax
Column = "GT"
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

