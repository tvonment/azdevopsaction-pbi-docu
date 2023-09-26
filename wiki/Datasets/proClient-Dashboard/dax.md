



# DAX

|Dataset|[proClient Dashboard](./../proClient-Dashboard.md)|
| :--- | :--- |
|Workspace|[proClient](../../Workspaces/proClient.md)|

## Table: pub dim_date

### Calculated Columns:


```dax
isCurrentReportMonth = IF(AND('pub dim_date'[Date] >= EOMONTH(TODAY(),-1)+1, 'pub dim_date'[Date] <= EOMONTH(TODAY(),0)),true,false)
```



```dax
MonthYearShort = Format([Date],"MMM yyyy")
```



```dax
isLast12Month = IF(AND('pub dim_date'[Date] >= EOMONTH(TODAY(),-12)+1, 'pub dim_date'[Date] <= EOMONTH(TODAY(),0)),true,false)
```



```dax
FirstDayOfMonth_PY = DATEADD('pub dim_date'[FirstDayOfMonth], -1,YEAR)
```



```dax
LastDayOfMonth_PY = DATEADD('pub dim_date'[LastDayOfMonth], -1,YEAR)
```



```dax
Date_PY = DATEADD('pub dim_date'[Date], -1,YEAR)
```



```dax
isLast12MonthFB = IF(AND('pub dim_date'[Date] >= EOMONTH(TODAY(),-14)+1, 'pub dim_date'[Date] <= EOMONTH(TODAY(),-2)),true,false)
```


## Table: v_km_proCLIENT_project_unpivot

### Measures:


```dax
count_all = calculate(COUNTROWS('v_km_proCLIENT_project_unpivot'))
```



```dax
number_of_projects = COUNTROWS(VALUES(v_km_proCLIENT_project_unpivot[ID]))
```


### Calculated Columns:


```dax
score_category = SWITCH(v_km_proCLIENT_project_unpivot[Value],0,0,1,-1,2,0,3,1)
```


## Table: nps_calculation

### Measures:


```dax
count_detractors = calculate([count_all],filter(v_km_proCLIENT_project_unpivot,v_km_proCLIENT_project_unpivot[score_category]<0)) 
```



```dax
count_promoters = calculate([count_all],filter(v_km_proCLIENT_project_unpivot,v_km_proCLIENT_project_unpivot[score_category]>0)) 
```



```dax
perc_detractors = DIVIDE([count_detractors],[count_all])
```



```dax
perc_promoters = DIVIDE([count_promoters],[count_all])
```



```dax
nps = ([perc_promoters]-[perc_detractors])*100
```



```dax
mps_prev_12Months = CALCULATE([nps], DATESINPERIOD('pub dim_date'[Date], LASTDATE('pub dim_date'[Date]), -12,MONTH))
```



```dax
count_projects_prev_12Months = CALCULATE([number_of_projects], DATESINPERIOD('pub dim_date'[Date], LASTDATE('pub dim_date'[Date]), -12,MONTH))
```


## Table: rep v_km_ll_country_to_region

### Measures:


```dax
CountryExists = 
var ctry = min(v_km_proCLIENT_project_unpivot[responsible_unit_new])
var cnt = calculate(countrows(v_km_proCLIENT_project_unpivot),  v_km_proCLIENT_project_unpivot[responsible_unit_new] = ctry)
return cnt
```


## Table: rep v_km_proCLIENT_feedback

### Measures:


```dax
number_of_feedbacks = COUNTROWS(VALUES('rep v_km_proCLIENT_feedback'[ID]))
```



```dax
count_survey_sent = calculate([count_all_surveys],filter('rep v_km_proCLIENT_feedback','rep v_km_proCLIENT_feedback'[status_new_sortId]<= 20)) 
```



```dax
count_all_surveys = calculate(COUNTROWS('rep v_km_proCLIENT_feedback'))
```



```dax
perc_survey_sent = DIVIDE([count_survey_sent],[count_all_surveys])
```



```dax
ssr_prev_12Months = CALCULATE([perc_survey_sent], DATESINPERIOD('pub dim_date'[Date], LASTDATE('pub dim_date'[Date]), -12,MONTH))
```

