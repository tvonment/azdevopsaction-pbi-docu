



# DAX

|Dataset|[Emplyoee list reports_v01](./../Emplyoee-list-reports_v01.md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: rep v_job

### Calculated Columns:


```dax
job_category_short = UPPER(Left('rep v_job'[jobcode_short],4))
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
sum_fte = SUM('rep v_hr_statistic'[fte_capacity])
```



```dax
count_emp_id_same_period_py = CALCULATE([count_emp_id], SAMEPERIODLASTYEAR('pub dim_date'[Date]))   
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
count_emp_female = CALCULATE(COUNT('rep v_hr_statistic'[emp_id]),FILTER('rep v_hr_statistic','rep v_hr_statistic'[gender]="F"))
```



```dax
count_female_vs_all = CALCULATE(DIVIDE('rep v_hr_statistic'[count_emp_female],'rep v_hr_statistic'[count_emp_id],0))
```



```dax
delta_headcount_vs_fte = 'rep v_hr_statistic'[count_emp_id]-'rep v_hr_statistic'[sum_fte]
```



```dax
delta_ppt_to_same_period_py = [delta_to_same_period_py]/'rep v_hr_statistic'[count_emp_id_same_period_py]
```



```dax
count_emp_id_dec_2py = CALCULATE('rep v_hr_statistic'[count_emp_id],PREVIOUSYEAR(PREVIOUSYEAR('pub dim_date'[Date])),month('pub dim_date'[Date])=12)
```



```dax
count_emp_id_py = CALCULATE([count_emp_id], SAMEPERIODLASTYEAR('pub dim_date'[Date]))   
```



```dax
count_emp_id_same_period_pm = CALCULATE([count_emp_id], PREVIOUSMONTH('pub dim_date'[Date]))   
```



```dax
count_emp_id_p2y = CALCULATE([count_emp_id], SAMEPERIODLASTYEAR(SAMEPERIODLASTYEAR('pub dim_date'[Date])))   
```


### Calculated Columns:


```dax
headcount = 1
```



```dax
platform_1_name (groups) = SWITCH(
	TRUE,
	ISBLANK('rep v_hr_statistic'[platform_1_name]),
	"(Blank)",
	'rep v_hr_statistic'[platform_1_name] IN {"Group Function A,G,IT,R",
		"Group Function Administration",
		"Group Function Assistants",
		"Group Function F&C",
		"Group Function Graphics",
		"Group Function HR",
		"Group Function IT",
		"Group Function Marketing",
		"Group Function RB N3XT",
		"Group Function Research"},
	"Group Functions",
	'rep v_hr_statistic'[platform_1_name]
)
```


## Table: rep v_hr_entry_exit

### Measures:


```dax
count_emp_hir_act = CALCULATE(COUNT('rep v_hr_entry_exit'[emp_id]),FILTER('rep v_hr_entry_exit','rep v_hr_entry_exit'[event_type] ="HIR"))
```



```dax
count_emp_hir_ytd = TOTALYTD([count_emp_hir_act],'pub dim_date'[Date])
```



```dax
count_emp_ter_act = CALCULATE(COUNT('rep v_hr_entry_exit'[emp_id]),FILTER('rep v_hr_entry_exit','rep v_hr_entry_exit'[event_type] ="TER"))
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
fluktuationsquote_ytd_% = DIVIDE([count_emp_ter_ytd],DIVIDE([count_emp_id_dec_py] + [count_emp_id],2))
```



```dax
forecast_faktor = DIVIDE(12,MAX('pub dim_date'[Month]))
```



```dax
fluktuationsquote_forecast_% = [fluktuationsquote_ytd_%] * [forecast_faktor]
```



```dax
fluktuations_quote_last_3M = DIVIDE([count_emp_ter_delta_ytd_ytd-3M],[avg_count_emp_id-3M_count_emp_id])
```



```dax
avg_count_emp_id-3M_count_emp_id = DIVIDE(CALCULATE([count_emp_id],DATEADD('pub dim_date'[Date],-2,MONTH)) + [count_emp_id],2)
```



```dax
count_emp_ter_act_py = CALCULATE([count_emp_ter_act],SAMEPERIODLASTYEAR('pub dim_date'[Date]))   
```



```dax
count_emp_ter_ytd_py = 
VAR DataMaxDate =  CALCULATE ( MAX ( 'pub dim_date'[Date] ), ALL ( 'pub dim_date') )
RETURN
    CALCULATE ([count_emp_ter_ytd],
        SAMEPERIODLASTYEAR (
            INTERSECT (
                VALUES ( 'pub dim_date'[Date] ),
                DATESBETWEEN ( 'pub dim_date'[Date], BLANK (), DataMaxDate )
            )
        )
    )
```



```dax
fluktuationsquote_ytd_py_% = DIVIDE([count_emp_ter_ytd_py],DIVIDE([count_emp_id_dec_py] + [count_emp_id_dec_2py],2))
```



```dax
fluktuationsquote_act_% = DIVIDE([count_emp_ter_act],DIVIDE([count_emp_id_same_period_pm] + [count_emp_id],2))
```



```dax
fluktuationsquote_act_py_%_CHECK = DIVIDE([count_emp_ter_act_py],DIVIDE([count_emp_id_same_period_py] + [count_emp_id_py_pm],2))
```



```dax
count_emp_id_py_pm = CALCULATE([count_emp_id_same_period_py],DATEADD('pub dim_date'[Date],-1,MONTH)) 
```



```dax
count_emp_hir_ytd for F = 
CALCULATE([count_emp_hir_ytd], 'pub ll_gender'[gender] IN { "F" })
```



```dax
count_emp_ter_ytd for F = 
CALCULATE([count_emp_ter_ytd], 'pub ll_gender'[gender] IN { "F" })
```



```dax
fluktuationsquote_act_py_% = DIVIDE([count_emp_ter_act_py],DIVIDE([count_emp_id_same_period_py] + [count_emp_id_py],2))
```


### Calculated Columns:


```dax
count_emp_hir-ter_act = CALCULATE([count_emp_hir_act] - [count_emp_ter_act])
```



```dax
platform_1_name (groups) = SWITCH(
	TRUE,
	ISBLANK('rep v_hr_entry_exit'[platform_1_name]),
	"(Blank)",
	'rep v_hr_entry_exit'[platform_1_name] IN {"Group Function Administration",
		"Group Function Assistants",
		"Group Function F&C",
		"Group Function Graphics",
		"Group Function HR",
		"Group Function IT",
		"Group Function Marketing",
		"Group Function RB N3XT",
		"Group Function Research"},
	"Group Functions",
	'rep v_hr_entry_exit'[platform_1_name] IN {"Automotive",
		"Belgium",
		"Brazil",
		"Canada",
		"CEI & CP",
		"CEI & Pharma",
		"Chemicals",
		"China 44",
		"Civil Economics, Energy&Infrastr., Chemical&Pharma",
		"Consumer Goods & Retail",
		"Cross-CC-Entry",
		"Czech Republic",
		"Digital Lighthouse",
		"Engineered Products & High Tech",
		"Expert Network",
		"Financial Services",
		"France",
		"Great Britain",
		"Hong Kong",
		"Hungary",
		"India",
		"Indonesia",
		"Industrial Products & Services",
		"Italy",
		"Japan",
		"Korea",
		"Malaysia",
		"Middle East",
		"Morocco",
		"Myanmar",
		"Netherlands",
		"Operations Strategy",
		"Poland",
		"Portugal",
		"Qatar",
		"Restructuring & Corporate Finance",
		"Restructuring, Performance, Transform.&Transaction",
		"Restructuring, Performance, Transformation & Transaction",
		"Romania",
		"Russia",
		"Saudi Arabia",
		"Singapore",
		"Spain",
		"Sweden",
		"Thailand",
		"Transportation",
		"Ukraine",
		"United States"},
	"old CCs",
	'rep v_hr_entry_exit'[platform_1_name]
)
```



```dax
ter_max_date Months = IF(
	ISBLANK('rep v_hr_entry_exit'[ter_max_date]),
	BLANK(),
	DATE(
		YEAR('rep v_hr_entry_exit'[ter_max_date]),
		1 + (MONTH('rep v_hr_entry_exit'[ter_max_date]) - 1),
		1
	)
)
```



```dax
last_hire_date_Months = IF(
	ISBLANK('rep v_hr_entry_exit'[last_hire_date]),
	BLANK(),
	DATE(
		YEAR('rep v_hr_entry_exit'[last_hire_date]),
		1 + (MONTH('rep v_hr_entry_exit'[last_hire_date]) - 1),
		1
	)
)
```


## Table: ToE

### Calculated Columns:


```dax
toe_description_exemption grouped = SWITCH(
	TRUE,
	ISBLANK('ToE'[toe_description]),
	"(Blank)",
	'ToE'[toe_description] IN {"End of wage continuation",
		"Exemption with exit",
		"Other Exemption"},
	"Other leave",
	'ToE'[toe_description]
)
```


## Table: rep v_hr_employee_active

### Measures:


```dax
count_emp_id_active = DISTINCTCOUNT('rep v_hr_employee_active'[emp_id])
```

