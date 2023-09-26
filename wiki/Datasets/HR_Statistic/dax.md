



# DAX

|Dataset|[HR_Statistic](./../HR_Statistic.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_statistic_job_category

### Calculated Columns:


```dax
job_category_short = UPPER(Left('rep v_hr_statistic_job_category'[job_category],4))
```


## Table: pub dim_date

### Calculated Columns:


```dax
MonthNameShort = FORMAT([Date],"MMM")
```



```dax
MonthYearShort = Format([Date],"MMM yyyy")
```


## Table: rep v_hr_statistic

### Measures:


```dax
count_emp_id = DISTINCTCOUNT('rep v_hr_statistic'[emp_id])
```



```dax
headcount_fte = SWITCH( VALUES( SwitchTable[Measure]),"FTE",[sum_fte],"Headcount",[count_emp_id],[count_emp_id])
```



```dax
count_emp_id_dec_py = CALCULATE('rep v_hr_statistic'[count_emp_id],PREVIOUSYEAR('pub dim_date'[Date]),month('pub dim_date'[Date])=12)
```



```dax
delta_to_dec_py = 'rep v_hr_statistic'[count_emp_id_dec_py]-'rep v_hr_statistic'[count_emp_id]
```



```dax
sum_fte = SUM('rep v_hr_statistic'[fte])
```



```dax
count_emp_id_same_period_py = CALCULATE([count_emp_id],SAMEPERIODLASTYEAR('pub dim_date'[Date]))   
```



```dax
delta_to_same_period_py = 'rep v_hr_statistic'[count_emp_id]-'rep v_hr_statistic'[count_emp_id_same_period_py]
```



```dax
count_emp_id_jan_ay = CALCULATE('rep v_hr_statistic'[count_emp_id],YEAR('pub dim_date'[Date])=YEAR(TODAY()),month('pub dim_date'[Date])=1)
```



```dax
delta_to_jan_ay = 'rep v_hr_statistic'[count_emp_id]-'rep v_hr_statistic'[count_emp_id_jan_ay]
```



```dax
count_emp_female = CALCULATE(COUNT('rep v_hr_statistic'[emp_id]),FILTER('rep v_hr_statistic','rep v_hr_statistic'[sex]="F"))
```



```dax
count_female_vs_all = CALCULATE(DIVIDE('rep v_hr_statistic'[count_emp_female],'rep v_hr_statistic'[count_emp_id],0))
```



```dax
delta_headcount_vs_fte = 'rep v_hr_statistic'[count_emp_id]-'rep v_hr_statistic'[sum_fte]
```


### Calculated Columns:


```dax
headcount = 1
```


## Table: rep v_hr_entry_exit

### Measures:


```dax
count_emp_hir_act = CALCULATE(COUNT('rep v_hr_entry_exit'[emp_id]),FILTER('rep v_hr_entry_exit','rep v_hr_entry_exit'[action_typeid] =20))
```



```dax
count_emp_hir_ytd = TOTALYTD([count_emp_hir_act],'pub dim_date'[Date])
```



```dax
count_emp_ter_act = CALCULATE(COUNT('rep v_hr_entry_exit'[emp_id]),FILTER('rep v_hr_entry_exit','rep v_hr_entry_exit'[action_typeid] =10))
```



```dax
count_emp_ter_ytd = TOTALYTD([count_emp_ter_act],'pub dim_date'[Date])
```



```dax
count_emp_ter_ytd-3M = CALCULATE([count_emp_ter_ytd],DATEADD('pub dim_date'[Date],-2,MONTH))  -- -2 , da aktueller Monat auch betrachtet wird
```



```dax
count_emp_ter_delta_ytd_ytd-3M = [count_emp_ter_ytd] - [count_emp_ter_ytd-3M]
```



```dax
fluktuationsquote_% = DIVIDE([count_emp_ter_ytd],DIVIDE([count_emp_id_dec_py] + [count_emp_id],2))
```



```dax
forecast_faktor = DIVIDE(12,MAX('pub dim_date'[Month]))
```



```dax
fluktuationsquote_forecast_% = [fluktuationsquote_%] * [forecast_faktor]
```



```dax
fluktuations_quote_last_3M = DIVIDE([count_emp_ter_delta_ytd_ytd-3M],[avg_count_emp_id-3M_count_emp_id])
```



```dax
avg_count_emp_id-3M_count_emp_id = DIVIDE(CALCULATE([count_emp_id],DATEADD('pub dim_date'[Date],-2,MONTH)) + [count_emp_id],2)
```


### Calculated Columns:


```dax
count_emp_hir-ter_act = CALCULATE([count_emp_hir_act] - [count_emp_ter_act])
```


## Table: TenuresPerEmployee


```dax
SUMMARIZE('rep v_hr_statistic','rep v_hr_statistic'[emp_id],'rep v_hr_statistic'[jobcode_id]
,"Tenure",Count('rep v_hr_statistic'[validfrom_date])
,"MaxMonth",MAX('rep v_hr_statistic'[validfrom_date])
)
```


## Table: Distinct_JobCategories


```dax
Filter(values('rep v_hr_statistic_job_category'[job_subcategory_short]), 'rep v_hr_statistic_job_category'[job_subcategory_short] <> Blank())
```


### Measures:


```dax
AVG number of months by JobSubCategory calculated by employee = 
var dateMaxFilter = max('pub dim_date'[Date])
var curSubCategory = min('Distinct_JobCategories'[job_subcategory_short])

return 
AVERAGEX('Distinct_Employees', 
    calculate
    (
        Count('rep v_hr_statistic'[validfrom_date])
        , Filter(All('pub dim_date'[Date]), 'pub dim_date'[Date] <= dateMaxFilter)
        , 'rep v_hr_statistic'[emp_id] = EARLIER('Distinct_Employees'[emp_id])
        , 'rep v_hr_statistic_job_category'[job_subcategory_short] = curSubCategory
    )
)
```


### Calculated Columns:


```dax
Sort = LOOKUPVALUE('rep v_hr_statistic_job_category'[job_subcategory_sort_id], 'rep v_hr_statistic_job_category'[job_subcategory_short], 'Distinct_JobCategories'[job_subcategory_short]) 
```



```dax
Job Subcategory = 'Distinct_JobCategories'[job_subcategory_short]
```


## Table: Distinct_Employees


```dax
Values('rep v_hr_statistic'[emp_id]) 
```

