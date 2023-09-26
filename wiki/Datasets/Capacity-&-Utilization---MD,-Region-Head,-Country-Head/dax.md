



# DAX

|Dataset|[Capacity & Utilization - MD, Region Head, Country Head](./../Capacity-&-Utilization---MD,-Region-Head,-Country-Head.md)|
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
    IF(utilization <= 0, BLANK(), utilization)
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
Utilization_hours_internal = SUM('msr v_employee_utilization'[inp_project_hours_adj]) + SUM('msr v_employee_utilization'[hr_project_hours])
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
Completion = DIVIDE([Utilization_hours_recorded], SUM('msr v_employee_utilization'[target_hours]))
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
Utilization Target AVG = AVERAGE('msr v_employee_utilization'[utilization_target])
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
Utilization_hours_missing = [Utilization_target_hours] - [Utilization_hours_recorded]
```



```dax
Utilization_hours_missing_bridge = [Utilization_hours_missing] * -1
```



```dax
Utilization Δ Target pp = IF(ISBLANK('msr v_employee_utilization'[Utilization %_2]), BLANK(), ROUND('msr v_employee_utilization'[Utilization Δ Target]*100, 0) & " pp")
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
Utilization Δ Target pp YTD formatted_table = "AVG Δ year to date: " & [Utilization Δ Target pp YTD] & "pp" 
```



```dax
Utilization Δ Target pp LM formatted_table = "AVG Δ last month: " & [Utilization Δ Target pp LM] & "pp" 
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
Δ pp PY = 
var PY = 'msr v_employee_utilization'[Utilization % PY]
var CY = 'msr v_employee_utilization'[Utilization %_2]

return
IF(CY > 0 ,IF(PY > 0, 
    ROUND(('msr v_employee_utilization'[Utilization %_2] - 'msr v_employee_utilization'[Utilization % PY]) *100, 0) & " pp",
    "N/A"), BLANK())
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
Utilization_days_missing = [Utilization_hours_missing]/8
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



```dax
Spacer = REPT("l", 15)
```



```dax
Completion_OLD = 
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
Utilization_hours_recorded = [Utilization_hours_vacation_leave] + [Utilization_hours_training] + [Utilization_hours_illness] + [Utilization_hours_internal] + [Utilization_hours_acq] + [Utilization_hours_on_client_project]
```



```dax
Utilization Target AVG_OLD = AVERAGE('rep v_hr_employee'[utilization_target])
```



```dax
Utilization Target AVG_NEW = AVERAGE('msr v_employee_utilization'[utilization_target])
```



```dax
Tooltip_Timetheet_analysis = "based on target hours adjusted"
```



```dax
Tooltip_completion = "based on target hours"
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



```dax
full_name_job_reporting_level4 = 'msr v_employee_utilization'[full_name] & " - " & 'msr v_employee_utilization'[job_reporting_level4]
```



```dax
employee_date_key = 'msr v_employee_utilization'[emp_id] & "-" & 'msr v_employee_utilization'[calendar_day]
```



```dax
toe_description = RELATED('msr v_hr_employee_job_matrix'[toe_description])
```



```dax
cost_center_id = RELATED('msr v_hr_employee_job_matrix'[cost_center_id])
```



```dax
company_id_byd = RELATED('msr v_hr_employee_job_matrix'[company_id_byd])
```



```dax
office = RELATED('msr v_hr_employee_job_matrix'[office])
```



```dax
platform_1_id = RELATED('msr v_hr_employee_job_matrix'[platform_1_id])
```



```dax
country_code_iso3 = RELATED('msr v_hr_employee_job_matrix'[country_code_iso3])
```



```dax
job.Im Scope = RELATED('msr v_hr_employee_job_matrix'[job.Im Scope])
```



```dax
job.Bezeichnung = RELATED('msr v_hr_employee_job_matrix'[job.Bezeichnung])
```



```dax
job.Kurz-Bezeichnung = RELATED('msr v_hr_employee_job_matrix'[job.Kurz-Bezeichnung])
```



```dax
job.JobGroup = RELATED('msr v_hr_employee_job_matrix'[job.JobGroup])
```



```dax
daily_rate_eur = RELATED('msr v_hr_employee_job_matrix'[daily_rate_eur])
```



```dax
utilization_target = RELATED('msr v_hr_employee_job_matrix'[utilization_target])
```



```dax
platform_1_name = RELATED('msr v_hr_employee_job_matrix'[platform_1_name])
```



```dax
platform_1_name_short = RELATED('msr v_hr_employee_job_matrix'[platform_1_name_short])
```



```dax
platform_1_sort = RELATED('msr v_hr_employee_job_matrix'[platform_1_sort])
```



```dax
region_reporting_level1 = RELATED('msr v_hr_employee_job_matrix'[region_reporting_level1])
```



```dax
region_reporting_level2 = RELATED('msr v_hr_employee_job_matrix'[region_reporting_level2])
```



```dax
region_reporting_level3 = RELATED('msr v_hr_employee_job_matrix'[region_reporting_level3])
```



```dax
region_reporting_level1_sort = RELATED('msr v_hr_employee_job_matrix'[region_reporting_level1_sort])
```



```dax
full_name = RELATED('msr v_hr_employee_job_matrix'[full_name])
```



```dax
job_reporting_level1 = RELATED('msr v_hr_employee_job_matrix'[job_reporting_level1])
```



```dax
job_reporting_level2 = RELATED('msr v_hr_employee_job_matrix'[job_reporting_level2])
```



```dax
job_reporting_level3 = RELATED('msr v_hr_employee_job_matrix'[job_reporting_level3])
```



```dax
job_reporting_level4 = RELATED('msr v_hr_employee_job_matrix'[job_reporting_level4])
```



```dax
job_reporting_level1_sort = RELATED('msr v_hr_employee_job_matrix'[job_reporting_level1_sort])
```



```dax
job_reporting_level2_sort = RELATED('msr v_hr_employee_job_matrix'[job_reporting_level2_sort])
```



```dax
job_reporting_level3_sort = RELATED('msr v_hr_employee_job_matrix'[job_reporting_level3_sort])
```



```dax
job_reporting_level4_sort = RELATED('msr v_hr_employee_job_matrix'[job_reporting_level4_sort])
```


## Table: msr v_hr_employee_job_matrix

### Calculated Columns:


```dax
employee_date_key = 'msr v_hr_employee_job_matrix'[emp_id] & "-" & 'msr v_hr_employee_job_matrix'[key_date]
```


## Table: rep v_hr_employee

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


### Calculated Columns:


```dax
Calendarweek = "CW-" & 'pub dim_date'[WeekOfYear]
```



```dax
UpToCurrentMonth = 
    VAR current_year = YEAR(TODAY())
    VAR current_month = MONTH(TODAY())
    VAR result = IF('pub dim_date'[Date].[Year] = current_year, 
                    IF('pub dim_date'[Date].[MonthNo] <= current_month, //temporary switched from <= to < only
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


## Table: msr v_employee_project_hours

### Measures:


```dax
Hours_in_approval = CALCULATE(SUM('msr v_employee_project_hours'[recorded_time])+0, 'msr v_employee_project_hours'[approval_status] IN {"In Approval"})
```



```dax
Hours_approved = CALCULATE(SUM('msr v_employee_project_hours'[recorded_time]), 'msr v_employee_project_hours'[approval_status] IN {"Approved", "Approval not Necessary"})
```



```dax
Hours_reported = CALCULATE(SUM('msr v_employee_project_hours'[recorded_time]), 'msr v_employee_project_hours'[approval_status] IN {"Approved", "Approval not Necessary", "In Approval"})
```



```dax
Hours_in_approval_% = DIVIDE([Hours_in_approval], [Hours_reported])
```



```dax
Hours_in_approval_CP = CALCULATE([Hours_in_approval]+0, 'msr v_employee_project_hours'[project_type] IN {"CP"})
```



```dax
Sum_recorded_time_hours = SUM('msr v_employee_project_hours'[recorded_time])
```



```dax
Sum_recorded_time_days = SUM('msr v_employee_project_hours'[recorded_time])/8
```



```dax
Days_in_approval = CALCULATE(SUM('msr v_employee_project_hours'[recorded_time])/8+0, 'msr v_employee_project_hours'[approval_status] IN {"In Approval"})
```



```dax
Days_in_approval_CP = CALCULATE([Days_in_approval]+0, 'msr v_employee_project_hours'[project_type] IN {"CP"})
```



```dax
Text Hours in Approval = "Hours currently in approval: " & FORMAT([Hours_in_approval],"0") & " (CP: " & FORMAT([Hours_in_approval_CP],"0") & ")"
```



```dax
Text Days in Approval = "Days currently in approval: " & FORMAT([Days_in_approval],"0") & " (CP: " & FORMAT([Days_in_approval_CP],"0") & ")"
```



```dax
Euros_in_approval = CALCULATE(SUMX('msr v_employee_project_hours',[recorded_time]/8*[daily_rate_eur])+0, 'msr v_employee_project_hours'[approval_status] IN {"In Approval"})
```



```dax
Euros_in_approval_CP = CALCULATE([Euros_in_approval]+0, 'msr v_employee_project_hours'[project_type] IN {"CP"})
```



```dax
Text Euros in Approval = "Euros currently in approval: " & SUBSTITUTE(FORMAT([Euros_in_approval], "#,##,,.0M"),".",",") & " (CP: " & SUBSTITUTE(FORMAT([Euros_in_approval_CP],"#,##,,.0M"),".",",") & ")"
```



```dax
Dynamic_in_approval = SWITCH(
    SELECTEDVALUE('D/H Slicer'[D/H]),
    "Days", [Days_in_approval],
    "Hours",[Hours_in_approval],
    0
)
```



```dax
Dynamic_in_approval_CP = SWITCH(
    SELECTEDVALUE('D/H Slicer'[D/H]),
    "Days", [Days_in_approval_CP],
    "Hours",[Hours_in_approval_CP],
    0
)
```


### Calculated Columns:


```dax
mentor_full_name_old = RELATED('rep v_hr_employee'[mentor_full_name])
```



```dax
project_title = IF('msr v_employee_project_hours'[time_type_category] IN {"Productive Time", "Training"}, 'msr v_employee_project_hours'[project_number] & " - " & 'msr v_employee_project_hours'[project_name], 'msr v_employee_project_hours'[time_type_category])
```



```dax
approver = IF('msr v_employee_project_hours'[time_type_category] IN {"Productive Time", "Training"}, 'msr v_employee_project_hours'[project_manager], 'msr v_employee_project_hours'[mentor_full_name])
```



```dax
employee_date_key = 'msr v_employee_project_hours'[emp_id] & "-" & 'msr v_employee_project_hours'[calendar_day]
```


## Table: Comparison_Table


```dax
SELECTCOLUMNS('rep v_hr_employee', 
                        "emp_id", 'rep v_hr_employee'[emp_id],
                        "Employee", 'rep v_hr_employee'[full_name], 
                        "Target", 'rep v_hr_employee'[utilization_target])
```


### Measures:


```dax
Info Button = UNICHAR(128712)
```


### Calculated Columns:


```dax
Utilization_YTD = CALCULATE([Utilization % YTD], ALLEXCEPT(Comparison_Table, Comparison_Table[emp_id]))
```



```dax
Utilization_LM = CALCULATE([Utilization % LM], ALLEXCEPT(Comparison_Table, Comparison_Table[emp_id]))
```



```dax
Delta_YTD = (Comparison_Table[Target] - Comparison_Table[Utilization_YTD]) * -1
```



```dax
Delta_LM = (Comparison_Table[Target] - Comparison_Table[Utilization_LM]) * -1
```



```dax
Delta_rounded_0.05_YTD = CEILING(Comparison_Table[Delta_YTD], 0.05)
```



```dax
Delta_rounded_0.05_LM = CEILING(Comparison_Table[Delta_LM], 0.05)
```



```dax
Delta_pp_YTD = Comparison_Table[Delta_rounded_0.05_YTD]*100
```



```dax
Delta_pp_LM = Comparison_Table[Delta_rounded_0.05_LM]*100
```



```dax
Delta_pp_YTD_table = ROUND(Comparison_Table[Delta_YTD] * 100, 0)
```



```dax
Delta_pp_LM_table = ROUND(Comparison_Table[Delta_LM] * 100, 0)
```


## Table: utilization_budgets

### Calculated Columns:


```dax
Country-Jobcode = utilization_budgets[country_code_iso3] & "-" & utilization_budgets[jobcode_id]
```


## Table: D/H Utilization Deepdive


```dax
{
    ("Target hours", NAMEOF('msr v_employee_utilization'[Utilization_target_hours]), 0),
    ("Target hours adj.", NAMEOF('msr v_employee_utilization'[Utilization_target_hours_utilization]), 1),
    ("Target days", NAMEOF('msr v_employee_utilization'[Utilization_target_days]), 0),
    ("Target days adj.", NAMEOF('msr v_employee_utilization'[Utilization_target_days_utilization]), 1),
    ("Client projects", NAMEOF('msr v_employee_utilization'[Utilization_hours_on_client_project]), 2),
    ("Client projects", NAMEOF('msr v_employee_utilization'[Utilization_days_on_client_project]), 2)
}
```


### Calculated Columns:


```dax
D/H = SWITCH(
    TRUE(),
    CONTAINSSTRING('D/H Utilization Deepdive'[Fields], "hours"), "Hours","Days"
)
```


## Table: D/H Utilization Drillthrough


```dax
{ --And Time in Approval
    ("Hours", NAMEOF('msr v_employee_project_hours'[Sum_recorded_time_hours]), 1,"Hours"),
    ("Days", NAMEOF('msr v_employee_project_hours'[Sum_recorded_time_days]), 0,"Days")
}
```


## Table: D/H Slicer


```dax
{("Days"),("Hours")}
```


## Table: D/H Timesheet Analysis


```dax
{
    ("Target days", NAMEOF('msr v_employee_utilization'[Utilization_target_days]), 0, "Days"),
    ("Vacation & leave", NAMEOF('msr v_employee_utilization'[Utilization_days_vacation_leave_bridge]), 1, "Days"),
    ("Training", NAMEOF('msr v_employee_utilization'[Utilization_days_training_bridge]), 2, "Days"),
    ("Target days adj.", NAMEOF('msr v_employee_utilization'[Utilization_target_days_utilization]), 3, "Days"),
    ("Sickness", NAMEOF('msr v_employee_utilization'[Utilization_days_illness_bridge]), 4, "Days"),
    ("Internal", NAMEOF('msr v_employee_utilization'[Utilization_days_internal_bridge]), 5, "Days"),
    ("Acq", NAMEOF('msr v_employee_utilization'[Utilization_days_acq_bridge]), 6, "Days"),
    ("Missing days", NAMEOF('msr v_employee_utilization'[Utilization_days_missing_bridge]), 7, "Days"),
    ("Client projects", NAMEOF('msr v_employee_utilization'[Utilization_days_on_client_project]), 8, "Days"),

    ("Target hours", NAMEOF('msr v_employee_utilization'[Utilization_target_hours]), 0, "Hours"),
    ("Vacation & leave", NAMEOF('msr v_employee_utilization'[Utilization_hours_vacation_leave_bridge]), 1, "Hours"),
    ("Training", NAMEOF('msr v_employee_utilization'[Utilization_hours_training_bridge]), 2, "Hours"),
    ("Target hours adj.", NAMEOF('msr v_employee_utilization'[Utilization_target_hours_utilization]), 3, "Hours"),
    ("Sickness", NAMEOF('msr v_employee_utilization'[Utilization_hours_illness_bridge]), 4, "Hours"),
    ("Internal", NAMEOF('msr v_employee_utilization'[Utilization_hours_internal_bridge]), 5, "Hours"),
    ("Acq", NAMEOF('msr v_employee_utilization'[Utilization_hours_acq_bridge]), 6, "Hours"),
    ("Missing hours", NAMEOF('msr v_employee_utilization'[Utilization_hours_missing_bridge]), 7, "Hours"),
    ("Client projects", NAMEOF('msr v_employee_utilization'[Utilization_hours_on_client_project]), 8, "Hours")   
}
```


### Measures:


```dax
Text Button Details Hours/Days = "Details " & LOWER(SELECTEDVALUE('D/H Slicer'[D/H]))
```


## Table: D/H Approval Textbox


```dax
{
    ("Text days in approval", NAMEOF('msr v_employee_project_hours'[Text Days in Approval]), 0, "Days"),
    ("Text dours in approval", NAMEOF('msr v_employee_project_hours'[Text Hours in Approval]), 1, "Hours")
}
```


## Table: D/H Completion Deepdive


```dax
{
    ("Days missing", NAMEOF('msr v_employee_utilization'[Utilization_days_missing]), 0, "Days"),
    ("Hours missing", NAMEOF('msr v_employee_utilization'[Utilization_hours_missing]), 1, "Hours")
}
```


## Table: Platform Slicer


```dax
DISTINCT('msr v_employee_utilization'[platform_1_name])
```

