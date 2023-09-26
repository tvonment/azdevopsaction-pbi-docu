



# DAX

|Dataset|[Performance Summary - Platform Head DACH](./../Performance-Summary---Platform-Head-DACH.md)|
| :--- | :--- |
|Workspace|[IFRS_Reporting [QA]](../../Workspaces/IFRS_Reporting-[QA].md)|

## Table: msr v_employee_utilization

### Measures:


```dax
Utilization_target_hours = SUM('msr v_employee_utilization'[target_hours])
```



```dax
Utilization_hours_on_client_project = SUM('msr v_employee_utilization'[productive_hours_utilization])
```



```dax
Utilization_absolute = [Utilization_hours_on_client_project] / 'msr v_employee_utilization'[Utilization_target_hours]
```



```dax
Utilization % = 
DIVIDE(
	[Utilization_hours_on_client_project],
	[Utilization_target_hours]
)
```



```dax
Utilization Target = 0.8
```



```dax
Utilization Performance = 'msr v_employee_utilization'[Utilization %] - 'msr v_employee_utilization'[Utilization Target]
```



```dax
Utilization Performance String = "(" & 'msr v_employee_utilization'[Utilization Performance Short] & "ppt.)"
```



```dax
Utilization Performance Short = FIXED('msr v_employee_utilization'[Utilization Performance] * 100, 0)
```



```dax
Utilization Target String = "Target: " & 'msr v_employee_utilization'[Utilization Target] * 100 & "%"
```



```dax
Utilization Target & Performance = [Utilization Target String] & " " & [Utilization Performance String]
```



```dax
Utilization % CY = 
var productive_hours_utilization = CALCULATE(SUM('msr v_employee_utilization'[productive_hours_utilization]), DATESYTD('pub dim_date'[Date]))
 
 Return
    productive_hours_utilization
```



```dax
Utilization_target_hours_utilization = SUM('msr v_employee_utilization'[target_hours_utilization])
```



```dax
Utilization_absolute_2 = [Utilization_hours_on_client_project] / 'msr v_employee_utilization'[Utilization_target_hours_utilization]
```



```dax
Utilization %_2 = 
    VAR utilization = DIVIDE(
	                        [Utilization_hours_on_client_project],
	                        [Utilization_target_hours_utilization]
                        )
RETURN
    IF(utilization <= 0, 0, utilization)
```



```dax
Completion rate (all vs th) = DIVIDE(SUM('msr v_employee_utilization'[booked_hours]), SUM('msr v_employee_utilization'[target_hours]))
```



```dax
Completion rate (prod+ill vs adj.) = DIVIDE(SUM('msr v_employee_utilization'[productive_hours_utilization])+SUM('msr v_employee_utilization'[illness_hours]), SUM('msr v_employee_utilization'[TA: Target hours adj.]))
```



```dax
TA: Target hours adj. Total = SUM('msr v_employee_utilization'[TA: Target hours adj.])
```



```dax
Completion rate (reported) = DIVIDE([Hours_reported], [TA: Target hours adj. Total])
```



```dax
Utilization_hours_illness = SUM('msr v_employee_utilization'[illness_hours])
```



```dax
Utilization_hours_illness_bridge = [Utilization_hours_illness] * -1
```



```dax
Utilization_hours_internal = SUM('msr v_employee_utilization'[inp_project_hours_adj])
```



```dax
Utilization_hours_internal_bridge = [Utilization_hours_internal] * -1
```



```dax
Utilization_hours_acq = SUM('msr v_employee_utilization'[acq_project_hours])
```



```dax
Utilization_hours_acq_bridge = [Utilization_hours_acq] * -1
```



```dax
Utilization_hours_training = SUM('msr v_employee_utilization'[training_hours])
```



```dax
Utilization_hours_training_bridge = [Utilization_hours_training] * -1
```



```dax
Utilization_hours_vacation_leave = SUM('msr v_employee_utilization'[vacation_hours]) + SUM('msr v_employee_utilization'[leave_hours])
```



```dax
Utilization_hours_vacation_leave_bridge = [Utilization_hours_vacation_leave] * -1
```



```dax
Completion = 
    IF(ISBLANK(VAR hours_reported = [Utilization_hours_acq] + [Utilization_hours_internal] + [Utilization_hours_illness] + [Utilization_hours_on_client_project]
    VAR target_hours_utilization = [Utilization_target_hours_utilization]
    VAR completion_total = DIVIDE(hours_reported, target_hours_utilization) 
RETURN
    IF(completion_total < 0, 0, completion_total)), 0, (VAR hours_reported = [Utilization_hours_acq] + [Utilization_hours_internal] + [Utilization_hours_illness] + [Utilization_hours_on_client_project]
    VAR target_hours_utilization = [Utilization_target_hours_utilization]
    VAR completion_total = DIVIDE(hours_reported, target_hours_utilization) 
RETURN
    IF(completion_total < 0, 0, completion_total)))
```



```dax
Utilization % PY = CALCULATE([Utilization %_2], SAMEPERIODLASTYEAR('pub dim_date'[Date]))
```



```dax
Utilization_target_hours_formatted = 
    VAR number_decimal = DIVIDE([Utilization_target_hours], 1000)
    VAR number_whole = FIXED(number_decimal, 0)
RETURN
    number_whole & "k h"
```



```dax
Utilization_target_hours_formatted_2 = [Utilization_target_hours]
```



```dax
Utilization_hours_vacation_leave_bridge_formatted = [Utilization_hours_vacation_leave_bridge]
```



```dax
Utilization_target_hours_utilization_formatted = [Utilization_target_hours_utilization]
```



```dax
Utilization_hours_training_bridge_formatted = [Utilization_hours_training_bridge]
```



```dax
Utilization_hours_illness_bridge_formatted = [Utilization_hours_illness_bridge]
```



```dax
Utilization_hours_internal_bridge_formatted = [Utilization_hours_internal_bridge]
```



```dax
Utilization_hours_acq_bridge_formatted = [Utilization_hours_acq_bridge]
```



```dax
Utilization_hours_on_client_project_formatted = [Utilization_hours_on_client_project]
```



```dax
Utilization % AVG_3M = 
    VAR start_3_month = EOMONTH(TODAY(),-4)
    VAR end_3_month = EOMONTH(TODAY(),-1)
    VAR utilization = CALCULATE(
                        DIVIDE(
	                        [Utilization_hours_on_client_project],
	                        [Utilization_target_hours_utilization]),
                        FILTER(
                            ALL('pub dim_date'), 'pub dim_date'[Date] > start_3_month && 'pub dim_date'[Date] <= end_3_month)
                    )
RETURN
    IF(utilization <= 0, 0, utilization)
```



```dax
start_3_month = EOMONTH(TODAY(),-4)
```



```dax
Utilization % AVG_3M_test = 
    VAR start_3_month = EOMONTH(TODAY(),-13)
    VAR end_3_month = EOMONTH(TODAY(),-1)
    VAR utilization = CALCULATE(
        MIN('pub dim_date'[Date]),
        FILTER(
            ALL('pub dim_date'), 'pub dim_date'[Date] > start_3_month && 'pub dim_date'[Date] <= end_3_month))
RETURN
    utilization
```



```dax
Utilization % AVG_12M = 
    VAR start_3_month = EOMONTH(TODAY(),-13)
    VAR end_3_month = EOMONTH(TODAY(),-1)
    VAR utilization = CALCULATE(
                        DIVIDE(
	                        [Utilization_hours_on_client_project],
	                        [Utilization_target_hours_utilization]),
                        FILTER(
                            ALL('pub dim_date'), 'pub dim_date'[Date] > start_3_month && 'pub dim_date'[Date] <= end_3_month)
                    )
RETURN
    IF(utilization <= 0, 0, utilization)
```



```dax
Utilization % AVG_txt = "L12M AVG: " & FORMAT('msr v_employee_utilization'[Utilization % AVG_12M], "0%") & "  |  L3M AVG: " & FORMAT('msr v_employee_utilization'[Utilization % AVG_3M], "0%")
```



```dax
Timesheet_Customer = [Utilization_hours_on_client_project]
```



```dax
Timesheet_Internal_Acq_Sick = ([Utilization_hours_illness_bridge_formatted] + [Utilization_hours_internal_bridge_formatted] + [Utilization_hours_acq_bridge_formatted]) * -1
```



```dax
Timesheet_Vacation_Leave_Training = ([Utilization_hours_vacation_leave_bridge_formatted] + [Utilization_hours_training_bridge_formatted]) * -1
```



```dax
Utilization Target AVG = AVERAGE('rep v_hr_employee'[utilization_target])
```



```dax
Utilization Δ Target = IF([Utilization Target AVG] = 0, 0, ([Utilization Target AVG] - [Utilization %_2]) * -1)
```



```dax
Timesheet_Target_Hours = SUM('msr v_employee_utilization'[target_hours])
```



```dax
Timesheet_Missing_Hours = [Timesheet_Target_Hours] - [Timesheet_Customer] - [Timesheet_Vacation_Leave_Training] - [Timesheet_Internal_Acq_Sick]
```



```dax
Utilization Δ Target for Table = IF([Utilization Target AVG] = 0, 0, ([Utilization Target AVG] - [Utilization %_2]) * -1)
```



```dax
Utilization_hours_missing = [Utilization_target_hours_utilization] - [Utilization_hours_illness] - [Utilization_hours_internal] - [Utilization_hours_acq] - [Utilization_hours_on_client_project]
```



```dax
Utilization_hours_missing_bridge = [Utilization_hours_missing] * -1
```



```dax
Utilization Δ Target pp = ROUND('msr v_employee_utilization'[Utilization Δ Target]*100, 0) & " pp"
```



```dax
Utilization % LM = 
    VAR utilization = CALCULATE(DIVIDE(
	                        [Utilization_hours_on_client_project],
	                        [Utilization_target_hours_utilization]
                        ),
                        'pub dim_date'[Month] = MONTH(TODAY())-1, 'pub dim_date'[Year] = YEAR(TODAY()))
RETURN
    IF(utilization <= 0, 0, utilization)
```



```dax
Utilization % YTD = 
    VAR utilization = CALCULATE(DIVIDE(
	                        [Utilization_hours_on_client_project],
	                        [Utilization_target_hours_utilization]
                        ),
                        'pub dim_date'[UpToCurrentMonth] = 1)
RETURN
    IF(utilization <= 0, 0, utilization)
```



```dax
Utilization Δ Target YTD = IF([Utilization Target AVG] = 0, 0, 
                                CALCULATE(([Utilization Target AVG] - [Utilization %_2]) * -1, FILTER(ALL('pub dim_date'),'pub dim_date'[UpToCurrentMonth] = 1)))
```



```dax
Utilization Δ Target LM = IF([Utilization Target AVG] = 0, 0, 
                                CALCULATE(([Utilization Target AVG] - [Utilization %_2]) * -1, FILTER(ALL('pub dim_date'), 'pub dim_date'[Month] = MONTH(TODAY())-1 && 'pub dim_date'[Year] = YEAR(TODAY()))))
```



```dax
Utilization Δ Target pp YTD = ROUND('msr v_employee_utilization'[Utilization Δ Target YTD]*100, 0)
```



```dax
Utilization Δ Target pp LM = ROUND('msr v_employee_utilization'[Utilization Δ Target LM]*100, 0)
```



```dax
Utilization_hours_reported = Not available
```



```dax
Completion Missing Hours = 
    VAR hours_reported = [Utilization_hours_acq] + [Utilization_hours_internal] + [Utilization_hours_illness] + [Utilization_hours_on_client_project]
    VAR target_hours_utilization = [Utilization_target_hours_utilization]
    VAR missing_hours = target_hours_utilization - hours_reported 
RETURN
    missing_hours
```



```dax
Completion Reported Hours = [Utilization_hours_acq] + [Utilization_hours_internal] + [Utilization_hours_illness] + [Utilization_hours_on_client_project]
```



```dax
Completion Target Hours adj. = [Utilization_target_hours_utilization]
```



```dax
Utilization Δ Target pp YTD formatted = "AVG Δ: " & [Utilization Δ Target pp YTD] & "pp" 
```



```dax
Utilization Δ Target YTD old = IF([Utilization Target AVG] = 0, 0, 
                                CALCULATE(([Utilization Target AVG] - [Utilization %_2]) * -1, 'pub dim_date'[UpToCurrentMonth] = 1))
```



```dax
Utilization Δ Target pp LM formatted = "AVG Δ: " & [Utilization Δ Target pp LM] & "pp" 
```



```dax
Utilization Δ Target pp YTD formatted_table = "AVG Δ Year to date: " & [Utilization Δ Target pp YTD] & "pp" 
```



```dax
Utilization Δ Target pp LM formatted_table = "AVG Δ Last Month: " & [Utilization Δ Target pp LM] & "pp" 
```



```dax
Utilization_target_days = SUM('msr v_employee_utilization'[target_hours])/8
```



```dax
Utilization_target_days_utilization = SUM('msr v_employee_utilization'[target_hours_utilization])/8
```



```dax
Utilization_days_on_client_project = SUM('msr v_employee_utilization'[productive_hours_utilization])/8
```



```dax
Utilization_days_vacation_leave_bridge = [Utilization_hours_vacation_leave]/8 * -1
```



```dax
Utilization_days_training_bridge = [Utilization_hours_training]/8 * -1
```



```dax
Utilization_days_illness_bridge = [Utilization_hours_illness]/8 * -1
```



```dax
Utilization_days_internal_bridge = [Utilization_hours_internal]/8 * -1
```



```dax
Utilization_days_acq_bridge = [Utilization_hours_acq]/8 * -1
```



```dax
Utilization_days_missing_bridge = [Utilization_hours_missing]/8 * -1
```



```dax
Flag Single Employee Selected = 
var emp = SELECTEDVALUE('rep v_hr_employee'[emp_id],"multiple")
return
if(emp = "multiple",0,1)
```



```dax
Text Special Time Model = if([Flag Single Employee Selected] && [Flag Special Time Model],"Values > 100% may be due to special time models","")
```



```dax
Flag Special Time Model = if(max('msr v_employee_utilization'[Utilization % Day]) > 1, 1,0)
```



```dax
Utilization Δ Target pp PY = ROUND(CALCULATE('msr v_employee_utilization'[Utilization Δ Target pp], SAMEPERIODLASTYEAR('pub dim_date'[Date]))*100, 0)& " pp"
```



```dax
Δ pp PY = ROUND(('msr v_employee_utilization'[Utilization %_2] - 'msr v_employee_utilization'[Utilization % PY]) *100, 0) & " pp"
```



```dax
Utilization_eur_vacation_leave_bridge = SUMX('msr v_employee_utilization',[Utilization_days_vacation_leave_bridge]*[daily_rate_eur])
```



```dax
Utilization_target_eur = SUMX('msr v_employee_utilization',[Utilization_target_days]*[daily_rate_eur])
```



```dax
Utilization_eur_training_bridge = SUMX('msr v_employee_utilization',[Utilization_days_training_bridge]*[daily_rate_eur])
```



```dax
Utilization_target_eur_utilization = SUMX('msr v_employee_utilization',[Utilization_target_days_utilization]*[daily_rate_eur])
```



```dax
Utilization_eur_illness_bridge = SUMX('msr v_employee_utilization',[Utilization_days_illness_bridge]*[daily_rate_eur])
```



```dax
Utilization_eur_internal_bridge = SUMX('msr v_employee_utilization',[Utilization_days_internal_bridge]*[daily_rate_eur])
```



```dax
Utilization_eur_acq_bridge = SUMX('msr v_employee_utilization',[Utilization_days_acq_bridge]*[daily_rate_eur])
```



```dax
Utilization_eur_missing_bridge = SUMX('msr v_employee_utilization',[Utilization_days_missing_bridge]*[daily_rate_eur])
```



```dax
Utilization_eur_on_client_project = SUMX('msr v_employee_utilization',[Utilization_days_on_client_project]*[daily_rate_eur])
```



```dax
Utilization_days_missing = ([Utilization_target_hours_utilization] - [Utilization_hours_illness] - [Utilization_hours_internal] - [Utilization_hours_acq] - [Utilization_hours_on_client_project])/8
```



```dax
Utilization_hours_missing % = 
    VAR missing = DIVIDE(
	                        [Utilization_hours_missing],
	                        [Utilization_target_hours_utilization]
                        )
RETURN
    IF(missing <= 0, 0, missing)
```



```dax
utilization_hours_acq_internal_illness = [Utilization_hours_acq] + [Utilization_hours_internal] + [Utilization_hours_illness]
```



```dax
utilization_hours_acq_internal_illness % = 
    VAR utilization = DIVIDE(
	                        [utilization_hours_acq_internal_illness],
	                        [Utilization_target_hours_utilization]
                        )
RETURN
    IF(utilization <= 0, 0, utilization)
```


### Calculated Columns:


```dax
TA: Vacation & other leave = 'msr v_employee_utilization'[vacation_hours] + 'msr v_employee_utilization'[leave_hours]
```



```dax
TA: Target hours adj. = 'msr v_employee_utilization'[target_hours] - 'msr v_employee_utilization'[TA: Vacation & other leave] - 'msr v_employee_utilization'[training_hours]
```



```dax
booked_hours = 'msr v_employee_utilization'[absence_hours] + 'msr v_employee_utilization'[training_hours] + 'msr v_employee_utilization'[productive_hours_utilization]
```



```dax
Utilization % Day = 
if('msr v_employee_utilization'[target_hours] = 0 && 'msr v_employee_utilization'[productive_hours_utilization] > 0, 8,
DIVIDE('msr v_employee_utilization'[productive_hours_utilization], 'msr v_employee_utilization'[target_hours],0))
```


## Table: rep v_hr_employee

### Measures:


```dax
Partner_count = COUNTROWS(FILTER('rep v_hr_employee', FIND("Partner", 'rep v_hr_employee'[jobcode],,0)>0))
```


### Calculated Columns:


```dax
Country-Jobcode = 'rep v_hr_employee'[country_code_iso3] & "-" & 'rep v_hr_employee'[jobcode_id]
```



```dax
utilization_target = RELATED(utilization_budgets[utilization_target])
```



```dax
fullname_joblevel4 = 'rep v_hr_employee'[full_name] & " - " & 'rep v_hr_employee'[job_reporting_level4]
```



```dax
employee_joblevel4_mentor = 'rep v_hr_employee'[full_name] & " - " & 'rep v_hr_employee'[job_reporting_level4] & " - " & 'rep v_hr_employee'[mentor_full_name]
```


## Table: pub dim_date

### Measures:


```dax
temp_CurrentWeek = WEEKNUM(TODAY())
```



```dax
temp_FirstWeek = WEEKNUM(TODAY())-3
```



```dax
temp_Lastweek = WEEKNUM(TODAY())+4
```



```dax
Column_width = REPT("0", 7)
```



```dax
ActiveMonthList = 
    CONCATENATEX (
        VALUES ('pub dim_date'[MonthNameShort] ),
        'pub dim_date'[MonthNameShort],
        ", "
    )
```



```dax
CurrentDay = TODAY()
```



```dax
CurrentDayWeek = [CurrentDay] & " (" & [CurrentWeek] & ")"
```



```dax
CurrentWeek = CALCULATE(
                FIRSTNONBLANK('pub dim_date'[Calendarweek], ""), 
                FILTER(ALL('pub dim_date'), 'pub dim_date'[Date] = TODAY()))
```



```dax
ActiveWeekList = 
    CONCATENATEX (
        VALUES ('pub dim_date'[Calendarweek] ),
        'pub dim_date'[Calendarweek],
        ", "
    )
```



```dax
CurrentMonth = FORMAT (TODAY(),"MMMM")
```


### Calculated Columns:


```dax
Calendarweek = "CW-" & 'pub dim_date'[WeekOfYear]
```



```dax
UpToCurrentMonth = 
    VAR current_year = YEAR(TODAY())
    VAR current_month = MONTH(TODAY())
    VAR result = IF('pub dim_date'[Date].[Year] = current_year, 
                    IF('pub dim_date'[Date].[MonthNo] <= current_month,
                        1,
                        0),0)
RETURN
    result
```



```dax
Last4Next4Weeks = 
    VAR current_year = YEAR(TODAY())
    VAR firstWeek = WEEKNUM(TODAY())-4
    VAR lastWeek = WEEKNUM(TODAY())+3
    VAR result = IF('pub dim_date'[Date].[Year] = current_year,
                    IF('pub dim_date'[WeekOfYear] >= firstWeek, 
                        IF('pub dim_date'[WeekOfYear] <= lastWeek,
                            1,
                            0),0),0)
RETURN
    result
```



```dax
Color_current_month = IF(MONTH(TODAY()) = 'pub dim_date'[Date].[MonthNo], "#008080", "#66B3B3")
```



```dax
Color_current_week = IF(WEEKNUM(TODAY()+1) = 'pub dim_date'[WeekOfYear], "#008080", "#66B3B3")
```


## Table: Refresh_Timestamp

### Calculated Columns:


```dax
Calendarweek = "CW-" & WEEKNUM(Refresh_Timestamp[Last_refresh_local])
```


## Table: utilization_budgets

### Calculated Columns:


```dax
Country-Jobcode = utilization_budgets[country_code_iso3] & "-" & utilization_budgets[jobcode_id]
```


## Table: msr v_fc_order_income_accumulated

### Measures:


```dax
OI_Monthly = SUM('msr v_fc_order_income_accumulated'[order_income_current])
```



```dax
OI_PY_YTD = CALCULATE([OI_Monthly], ALL('pub dim_date'[Date]), 'pub dim_date'[Year] = YEAR(TODAY())-1, 'pub dim_date'[Month] <= MONTH(TODAY()))
```



```dax
OI_YTD_BUD_2 = CALCULATE(SUM(OI_Budget_Countries[OI_Budget]), ALL('pub dim_date'[Date]), 'pub dim_date'[Month] < MONTH(TODAY()))
```



```dax
OI_per_P = DIVIDE([OI_Monthly], [Partner_count])
```



```dax
OI_per_P_BUD_YTD = DIVIDE([OI_YTD_BUD_2], CALCULATE(DISTINCTCOUNT('msr v_fc_order_income_accumulated'[project_number]), ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY()), 'pub dim_date'[Year] = YEAR(TODAY())-1))
```



```dax
OI_per_P_PY_YTD_formatted = DIVIDE([OI_per_P_PY_YTD], 1000)
```



```dax
OI_PY_YTD_formatted = DIVIDE([OI_PY_YTD], 1000)
```



```dax
OI_Monthly_formatted = DIVIDE([OI_Monthly], 1000)
```



```dax
OI_Monthly_BUD_C = 
    var check_industry = calculate(isfiltered(Dim_Industries[industry]) , allselected())
    var check_function = calculate(isfiltered(Dim_Functions[function]) , allselected())
return
    if(check_industry || check_function, BLANK(), SUM(OI_Budget_Countries[OI_Budget]))
```



```dax
OI_Monthly_BUD_C_formatted = DIVIDE([OI_Monthly_BUD_C], 1000)
```



```dax
OI_Monthly_BUD_FP = 
    var check_region1 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) , allselected())
    var check_region2 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) , allselected())
    var check_region3 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected())
    var check_industry = calculate(isfiltered(Dim_Industries[industry]) , allselected())
return
    if(check_region1 || check_region2 || check_region3 || check_industry, BLANK(), SUM(OI_Budget_Platforms_Function[OI_Budget]))
```



```dax
OI_Monthly_BUD_IP = 
    var check_region1 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) , allselected())
    var check_region2 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) , allselected())
    var check_region3 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected())
    var check_function = calculate(isfiltered(Dim_Functions[function]) , allselected())
return
    if(check_region1 || check_region2 || check_region3 || check_function, BLANK(), SUM(OI_Budget_Platforms_Industry[OI_Budget]))
```



```dax
OI_YTD_BUD_C = TOTALYTD([OI_Monthly_BUD_C], 'pub dim_date'[Date])
```



```dax
OI_YTD_BUD_C_no_future = CALCULATE([OI_YTD_BUD_C], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] < MONTH(TODAY()))
```



```dax
OI_YTD_BUD_C_no_future_formatted = DIVIDE([OI_YTD_BUD_C_no_future], 1000)
```



```dax
OI_YTD_BUD_IP = TOTALYTD([OI_Monthly_BUD_IP], 'pub dim_date'[Date])
```



```dax
OI_YTD_BUD_IP_no_future = CALCULATE([OI_YTD_BUD_IP], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] < MONTH(TODAY()))
```



```dax
OI_YTD_BUD_FP = TOTALYTD([OI_Monthly_BUD_FP], 'pub dim_date'[Date])
```



```dax
OI_YTD_BUD_FP_no_future = CALCULATE([OI_YTD_BUD_FP], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] < MONTH(TODAY()))
```



```dax
OI_YTD_BUD_combined_no_future = 
    var check_region = IF(calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected()), allselected()) , allselected()), "R", "")
    var check_industry = IF(calculate(isfiltered(Dim_Industries[industry]) , allselected()), "I", "")
    var check_function = IF(calculate(isfiltered(Dim_Functions[function]) , allselected()), "F", "")
    var check_combination = check_region & check_industry & check_function
return
    IF(check_combination = "" || check_combination = "R", [OI_YTD_BUD_C_no_future_formatted], 
        IF(check_combination = "I", [OI_YTD_BUD_IP_no_future],
            IF(check_combination = "F", [OI_YTD_BUD_FP_no_future], "")))
```



```dax
OI_per_P_formatted = DIVIDE([OI_per_P], 1000)
```



```dax
OI_per_P_PY_YTD = DIVIDE([OI_PY_YTD], CALCULATE([Partner_count], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY()), 'pub dim_date'[Year] = YEAR(TODAY())-1))
```



```dax
OI_per_P_BUD_combined_YTD = IF([OI_YTD_BUD_combined_no_future] = "", BLANK(), DIVIDE([OI_YTD_BUD_combined_no_future], CALCULATE([Partner_count], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY()), 'pub dim_date'[Year] = YEAR(TODAY())-1)))
```

