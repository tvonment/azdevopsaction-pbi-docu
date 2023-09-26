



# DAX

|Dataset|[Sales Funnel & Order Book - MD, Region Head, Country Head](./../Sales-Funnel-&-Order-Book---MD,-Region-Head,-Country-Head.md)|
| :--- | :--- |
|Workspace|[IFRS_Reporting [QA]](../../Workspaces/IFRS_Reporting-[QA].md)|

## Table: rep v_hr_employee

### Measures:


```dax
Partner_count = COUNTROWS(FILTER('rep v_hr_employee', FIND("Partner", 'rep v_hr_employee'[jobcode],,0)>0))
```


## Table: pub dim_date

### Measures:


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
CurrentWeek = CALCULATE(
                FIRSTNONBLANK('pub dim_date'[Calendarweek], ""), 
                FILTER(ALL('pub dim_date'), 'pub dim_date'[Date] = TODAY()))
```



```dax
CurrentDayWeek = [CurrentDay] & " (" & [CurrentWeek] & ")"
```



```dax
CurrentYear = YEAR(TODAY())
```


### Calculated Columns:


```dax
Calendarweek = "CW-" & 'pub dim_date'[WeekOfYear]
```



```dax
UpToCurrentMonth = 
    VAR current_month = MONTH(TODAY())
    VAR result = IF('pub dim_date'[Date].[MonthNo] <= current_month, 1, 0)
RETURN
    result
```



```dax
IsLast8CalendarWeeks = 
    VAR firstWeek = WEEKNUM(TODAY())-7
    VAR lastWeek = WEEKNUM(TODAY())
RETURN
    IF('pub dim_date'[Year] = YEAR(TODAY()), IF('pub dim_date'[WeekOfYear] >= firstWeek && 'pub dim_date'[WeekOfYear] <= lastWeek, true, false), false)
```



```dax
IsCurrentMonth = IF(YEAR(TODAY())='pub dim_date'[Year], IF(MONTH(TODAY())-1='pub dim_date'[Month], true, false), false)
```


## Table: msr v_fc_order_income_accumulated

### Measures:


```dax
OI_Monthly = CALCULATE(SUM('msr v_fc_order_income_accumulated'[order_income_current_dax]), MONTH('msr v_fc_order_income_accumulated'[report_month]) <= MONTH(TODAY())-1)
```



```dax
OI_Cumulated = SUM('msr v_fc_order_income_accumulated'[order_income_total])
```



```dax
OI_YTD = TOTALYTD('msr v_fc_order_income_accumulated'[OI_Monthly_for_YTD], 'pub dim_date'[Date])
```



```dax
OI_Monthly_BUD_C = SUM(OI_Budget_Countries[OI_Budget])
//    var check_industry = calculate(isfiltered(platforms_industry[platform_1_name]) , allselected())
//    var check_function = calculate(isfiltered(platforms_function[platform_1_name]) , allselected())
//return
//    if(check_industry || check_function, BLANK(), SUM(OI_Budget_Countries[OI_Budget]))
```



```dax
OI_YTD_BUD_C = TOTALYTD([OI_Monthly_BUD_C], 'pub dim_date'[Date])
```



```dax
OI_Monthly_PY = CALCULATE([OI_Monthly], SAMEPERIODLASTYEAR('pub dim_date'[Date]))
```



```dax
OI_YTD_PY = CALCULATE([OI_YTD], SAMEPERIODLASTYEAR('pub dim_date'[Date]))
```



```dax
OI_ΔBUD_C = 
    VAR delta_BUD = DIVIDE([OI_Monthly], [OI_Monthly_BUD_C]) - 1
RETURN
    IF(delta_BUD < -0.9, "", delta_BUD)
```



```dax
OI_YTD_full_number = [OI_YTD] * 1000
```



```dax
OI_YTD_formatted = DIVIDE([OI_YTD], 1000)
```



```dax
OI_YTD_PY_formatted = DIVIDE([OI_YTD_PY], 1000)
```



```dax
OI_YTD_BUD_C_formatted = DIVIDE([OI_YTD_BUD_C], 1000)
```



```dax
Spacer (act vs bud vs py) = REPT("l", 33)
```



```dax
OI_YTD_formatted_0.00 = DIVIDE([OI_YTD], 1000)
```



```dax
OI_PY = CALCULATE([OI_Monthly], ALL('pub dim_date'[Date]), 'pub dim_date'[Year] = YEAR(TODAY())-1)
```



```dax
OI_CY = CALCULATE([OI_Monthly], 'pub dim_date'[Year] = YEAR(TODAY()))
```



```dax
OI_Monthly_BUD_C_no_future = CALCULATE([OI_Monthly_BUD_C], MONTH(OI_Budget_Countries[FirstDayOfMonth]) <= MONTH(TODAY())-1)
```



```dax
OI_PY_formatted = DIVIDE([OI_PY], 1000)
```



```dax
OI_Delta_%_PY = ([OI_Monthly] - [OI_Monthly_PY]) / [OI_Monthly_PY]
```



```dax
OI_Delta_%_BUD_C = ([OI_Monthly] - [OI_Monthly_BUD_C]) / [OI_Monthly_BUD_C]
```



```dax
OI_YTD_no_future = CALCULATE([OI_YTD], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY())-1)

//IF(MAX('pub dim_date'[Date]) <= TODAY(), [OI_YTD], BLANK())
```



```dax
OI_YTD_no_future_formatted = DIVIDE([OI_YTD_no_future], 1000)
```



```dax
OI_function_operations = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[function] = "Operations")
```



```dax
OI_function_digital = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[function] = "Digital")
```



```dax
OI_function_investor_support = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[function] = "Investor Support")
```



```dax
OI_function_rpt = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[function] = "RPT")
```



```dax
OI_function_strategy_others = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[function] = "Strategy & Others")
```



```dax
OI_YTD_historical = CALCULATE(SUM('msr v_fc_order_income_accumulated'[order_income_current]), ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY())-1)
```



```dax
OI_YTD_historical_formatted = DIVIDE([OI_YTD_historical], 1000)
```



```dax
OI_YTD_historical_2 = CALCULATE([OI_YTD], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY()))
```



```dax
OI_YTD_historical_2_formatted = DIVIDE([OI_YTD_historical_2], 1000)
```



```dax
OI_YTD_historical_3 = CALCULATE(SUM('msr v_fc_order_income_accumulated'[order_income_current]), ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY()))
```



```dax
OI_industry_industrials = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[industry] = "Industrials")
```



```dax
OI_industry_regulated_infrastructure = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[industry] = "Regulated & Infrastructure")
```



```dax
OI_industry_health_consumer = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[industry] = "Health & Consumer")
```



```dax
OI_industry_services = CALCULATE([OI_Monthly_formatted], 'msr v_fc_order_income_accumulated'[industry] = "Services")
```



```dax
OI_Monthly_formatted = DIVIDE([OI_Monthly], 1000)
```



```dax
OI_YTD_BUD_C_no_future = CALCULATE([OI_YTD_BUD_C], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] < MONTH(TODAY()))
```



```dax
OI_YTD_BUD_C_no_future_formatted = DIVIDE([OI_YTD_BUD_C_no_future], 1000)
```



```dax
OI_Monthly_BUD_C_no_future_formatted = DIVIDE([OI_Monthly_BUD_C_no_future], 1000)
```



```dax
OI_Monthly_BUD_C_formatted = DIVIDE([OI_Monthly_BUD_C], 1000)
```



```dax
OI_PY_YTD = CALCULATE([OI_Monthly], ALL('pub dim_date'[Date]), 'pub dim_date'[Year] = YEAR(TODAY())-1, 'pub dim_date'[Month] <= MONTH(TODAY())-1)
```



```dax
OI_PY_YTD_formatted = DIVIDE([OI_PY_YTD], 1000)
```



```dax
OI_per_P = DIVIDE([OI_Monthly], [Partner_count])
```



```dax
OI_per_P_PY_YTD = DIVIDE([OI_PY_YTD], CALCULATE([Partner_count], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY()), 'pub dim_date'[Year] = YEAR(TODAY())-1))
```



```dax
OI_per_P_test = CALCULATE(DISTINCTCOUNT('msr v_fc_order_income_accumulated'[project_number]), ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY()), 'pub dim_date'[Year] = YEAR(TODAY())-1)
```



```dax
OI_YTD_BUD_C_2 = CALCULATE(SUM(OI_Budget_Countries[OI_Budget]), ALL('pub dim_date'[Date]), 'pub dim_date'[Month] < MONTH(TODAY()))
```



```dax
OI_per_P_BUD_combined_YTD = IF([OI_Monthly_BUD_combined_no_future] = "", BLANK(), DIVIDE([OI_Monthly_BUD_combined_no_future], CALCULATE([Partner_count], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] <= MONTH(TODAY()), 'pub dim_date'[Year] = YEAR(TODAY())-1)))
```



```dax
order_income_GROSS_PY_formatted = IF(SUM('msr v_fc_order_income_accumulated'[order_income_GROSS_formatted]) > 0, CALCULATE(SUM('msr v_fc_order_income_accumulated'[order_income_GROSS_formatted]), SAMEPERIODLASTYEAR('pub dim_date'[Date])), 0)
```



```dax
OI_absolute = SUM('msr v_fc_order_income_accumulated'[order_income_current]) * 1000
```



```dax
Measure 1 = 
    var check_industry = calculate(isfiltered('msr v_fc_order_income_accumulated'[industry]) , allselected())
    var check_function = calculate(isfiltered('msr v_fc_order_income_accumulated'[function]) , allselected())

return
 if(check_industry || check_function, BLANK(), 111)
```



```dax
OI_Monthly_BUD_C_old = SUM(OI_Budget_Countries[OI_Budget])
```



```dax
OI_YTD_DAX = TOTALYTD(SUM('msr v_fc_order_income_accumulated'[order_income_current_dax]), 'pub dim_date'[Date])
```



```dax
OI_Monthly_BUD_FP = 
    var check_region1 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) , allselected())
    var check_region2 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) , allselected())
    var check_region3 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected())
    var check_industry = calculate(isfiltered(platforms_industry[platform_1_name]) , allselected())
    var check_subplatform_industry = CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subplatform]), ALLSELECTED())
    var check_subject_industry = CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subject]), ALLSELECTED())
    var check_subject_function = CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[function_subject]), ALLSELECTED())
return
    if(check_region1 || check_region2 || check_region3 || check_industry || check_subplatform_industry || check_subject_industry || check_subject_function, BLANK(), SUM(OI_Budget_Platforms_Function[OI_Budget]))
```



```dax
OI_Monthly_BUD_IP = 
    var check_region1 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) , allselected())
    var check_region2 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) , allselected())
    var check_region3 = calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected())
    var check_function = calculate(isfiltered(platforms_function[platform_1_name]) , allselected())
    var check_subplatform_industry = CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subplatform]), ALLSELECTED())
    var check_subject_industry = CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subject]), ALLSELECTED())
    var check_subject_function = CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[function_subject]), ALLSELECTED())
return
    if(check_region1 || check_region2 || check_region3 || check_function || check_subplatform_industry || check_subject_industry || check_subject_function, BLANK(), SUM(OI_Budget_Platforms_Industry[OI_Budget]))
```



```dax
OI_YTD_BUD_IP = TOTALYTD([OI_Monthly_BUD_IP], 'pub dim_date'[Date])
```



```dax
OI_YTD_BUD_FP = TOTALYTD([OI_Monthly_BUD_FP], 'pub dim_date'[Date])
```



```dax
OI_Monthly_BUD_combined = 
    var check_region = IF(calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected()), allselected()) , allselected()), "R", "")
    var check_industry = IF(calculate(isfiltered(platforms_industry[platform_1_name]) , allselected()), "I", "")
    var check_function = IF(calculate(isfiltered(platforms_function[platform_1_name]) , allselected()), "F", "")
    var check_subplatform_industry = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subplatform]), ALLSELECTED()), "SI", "")
    var check_subject_industry = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subject]), ALLSELECTED()), "SI", "")
    var check_subject_function = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[function_subject]), ALLSELECTED()), "SF", "")
    var check_combination = check_region & check_industry & check_function & check_subplatform_industry & check_subject_industry & check_subject_function
return
    IF(check_combination = "R", [OI_Monthly_BUD_C_formatted], 
        IF(check_combination = "" || check_combination = "I", [OI_Monthly_BUD_IP],
            IF(check_combination = "F", [OI_Monthly_BUD_FP], "")))
```



```dax
OI_Monthly_BUD_IP_no_future = CALCULATE([OI_Monthly_BUD_IP], MONTH(OI_Budget_Platforms_Industry[FirstDayOfMonth]) <= MONTH(TODAY())-1)

//IF(MAX('pub dim_date'[Date]) <= TODAY(), [OI_Monthly_BUD_IP], BLANK())
```



```dax
OI_Monthly_BUD_FP_no_future = CALCULATE([OI_Monthly_BUD_FP], MONTH(OI_Budget_Platforms_Function[FirstDayOfMonth]) <= MONTH(TODAY())-1)

//IF(MAX('pub dim_date'[Date]) <= TODAY(), [OI_Monthly_BUD_FP], BLANK())
```



```dax
OI_YTD_BUD_combined = 
    var check_region = IF(calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected()), allselected()) , allselected()), "R", "")
    var check_industry = IF(calculate(isfiltered(platforms_industry[platform_1_name]) , allselected()), "I", "")
    var check_function = IF(calculate(isfiltered(platforms_function[platform_1_name]) , allselected()), "F", "")
    var check_subplatform_industry = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subplatform]), ALLSELECTED()), "SI", "")
    var check_subject_industry = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subject]), ALLSELECTED()), "SI", "")
    var check_subject_function = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[function_subject]), ALLSELECTED()), "SF", "")
    var check_combination = check_region & check_industry & check_function & check_subplatform_industry & check_subject_industry & check_subject_function
return
    IF(check_combination = "R", [OI_YTD_BUD_C_formatted], 
        IF(check_combination = "" || check_combination = "I", [OI_YTD_BUD_IP],
            IF(check_combination = "F", [OI_YTD_BUD_FP], "")))
```



```dax
OI_CY_formatted = DIVIDE([OI_CY], 1000)
```



```dax
OI_YTD_BUD_combined_no_future = 
    var check_region = IF(calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected()), allselected()) , allselected()), "R", "")
    var check_industry = IF(calculate(isfiltered(platforms_industry[platform_1_name]) , allselected()), "I", "")
    var check_function = IF(calculate(isfiltered(platforms_function[platform_1_name]) , allselected()), "F", "")
    var check_subplatform_industry = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subplatform]), ALLSELECTED()), "SI", "")
    var check_subject_industry = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subject]), ALLSELECTED()), "SI", "")
    var check_subject_function = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[function_subject]), ALLSELECTED()), "SF", "")
    var check_combination = check_region & check_industry & check_function & check_subplatform_industry & check_subject_industry & check_subject_function
return
    IF(check_combination = "R", [OI_YTD_BUD_C_no_future_formatted], 
        IF(check_combination = "" || check_combination = "I", [OI_YTD_BUD_IP_no_future],
            IF(check_combination = "F", [OI_YTD_BUD_FP_no_future], "")))
```



```dax
OI_YTD_BUD_FP_no_future = CALCULATE([OI_YTD_BUD_FP], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] < MONTH(TODAY()))
```



```dax
OI_YTD_BUD_IP_no_future = CALCULATE([OI_YTD_BUD_IP], ALL('pub dim_date'[Date]), 'pub dim_date'[Month] < MONTH(TODAY()))
```



```dax
OI_per_P_formatted = DIVIDE([OI_per_P], 1000)
```



```dax
OI_per_P_BUD_C_YTD_formatted = DIVIDE([OI_per_P_BUD_combined_YTD], 1000)
```



```dax
OI_per_P_PY_YTD_formatted = DIVIDE([OI_per_P_PY_YTD], 1000)
```



```dax
aaa_monthly_unequal_ytd = IF([OI_Monthly] <> CALCULATE(SUM('msr v_fc_order_income_accumulated'[order_income_total]), 'msr v_fc_order_income_accumulated'[report_month_id] = "06.2023"), 1, 0)
```



```dax
aaa_oi_07_2023 = CALCULATE(SUM('msr v_fc_order_income_accumulated'[order_income_total]), 'msr v_fc_order_income_accumulated'[report_month_id] = "07.2023")
```



```dax
aaa_7_but_no_6 = IF(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "07.2023")) && NOT(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "06.2023"))), 1, 
                    IF(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "06.2023")) && NOT(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "05.2023"))), 1,
                    IF(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "05.2023")) && NOT(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "04.2023"))), 1,
                    IF(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "04.2023")) && NOT(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "03.2023"))), 1,
                    IF(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "03.2023")) && NOT(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "02.2023"))), 1,
                    IF(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "02.2023")) && NOT(ISBLANK(CALCULATE([aaa_sum_total], 'msr v_fc_order_income_accumulated'[report_month_id] = "01.2023"))), 1,
                    0))))))
```



```dax
aaa_sum_total = SUM('msr v_fc_order_income_accumulated'[order_income_total])
```



```dax
OI_Monthly_BUD_combined_no_future = 
    var check_region = IF(calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level1]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level2]) || calculate(isfiltered('pub v_ll_company_to_region'[region_reporting_level3]) , allselected()), allselected()) , allselected()), "R", "")
    var check_industry = IF(calculate(isfiltered(platforms_industry[platform_1_name]) , allselected()), "I", "")
    var check_function = IF(calculate(isfiltered(platforms_function[platform_1_name]) , allselected()), "F", "")
    var check_subplatform_industry = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subplatform]), ALLSELECTED()), "SI", "")
    var check_subject_industry = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[industry_subject]), ALLSELECTED()), "SI", "")
    var check_subject_function = IF(CALCULATE(ISFILTERED('msr v_fc_order_income_accumulated'[function_subject]), ALLSELECTED()), "SF", "")
    var check_combination = check_region & check_industry & check_function & check_subplatform_industry & check_subject_industry & check_subject_function
return
    IF(check_combination = "R", [OI_Monthly_BUD_C_no_future_formatted], 
        IF(check_combination = "" || check_combination = "I", [OI_Monthly_BUD_IP_no_future],
            IF(check_combination = "F", [OI_Monthly_BUD_FP_no_future], "")))
```



```dax
OI_Monthly_BUD_C_no_future_OLD = IF(MAX('pub dim_date'[Date]) <= TODAY(), [OI_Monthly_BUD_C], BLANK())
```



```dax
OI_Monthly_PY_formatted = DIVIDE([OI_Monthly_PY], 1000)
```



```dax
OI_YTD_PY_NEW = TOTALYTD([OI_Monthly_for_YTD], 'pub dim_date'[Date])
```



```dax
OI_YTD_PY_NEW_2 = CALCULATE([OI_YTD_PY_NEW], SAMEPERIODLASTYEAR('pub dim_date'[Date]))
```



```dax
OI_Monthly_for_YTD = SUM('msr v_fc_order_income_accumulated'[order_income_current_dax])
```



```dax
OI_Monthly_Completion = DIVIDE([OI_Monthly_formatted], [OI_Monthly_BUD_combined_no_future])
```



```dax
OI_Monthly_Completion_Max = 1.2
```


### Calculated Columns:


```dax
order_income_current_dax_formatted = DIVIDE('msr v_fc_order_income_accumulated'[order_income_current_dax], 1000)
```



```dax
order_income_GROSS_formatted = DIVIDE('msr v_fc_order_income_accumulated'[order_income_GROSS], 1000)
```



```dax
order_income_current_dax = IF(MONTH('msr v_fc_order_income_accumulated'[report_month_previous]) = 12, 'msr v_fc_order_income_accumulated'[order_income_total], 'msr v_fc_order_income_accumulated'[order_income_total] - 'msr v_fc_order_income_accumulated'[order_income_previous])
```


## Table: Refresh_Timestamp

### Calculated Columns:


```dax
Calendarweek = "CW-" & WEEKNUM(Refresh_Timestamp[Last_refresh_local])
```


## Table: OI_Budget_Countries

### Measures:


```dax
RLS_country = 0--IF(SUM(RLS_active_role[role_id])=3, TRUE(), FALSE())
```


## Table: pub v_ll_company_to_region

### Calculated Columns:


```dax
mapping_budget = IF('pub v_ll_company_to_region'[company] = "RB Int", "Global Adjustment", IF('pub v_ll_company_to_region'[region_reporting_level1] IN {"Non-operational companies", "Other RB companies", "Holding"}, BLANK(), 'pub v_ll_company_to_region'[country_code_iso3]))
```


## Table: msr v_fc_project_data

### Calculated Columns:


```dax
project_client_short = IF(CONTAINSSTRING('msr v_fc_project_data'[project_client], "Roland Berger"), LOOKUPVALUE('pub v_ll_company_to_region'[region_reporting_level3], 'pub v_ll_company_to_region'[org_unit_id], 'msr v_fc_project_data'[responsible_unit_byd_id]), 'msr v_fc_project_data'[project_client])
```


## Table: sec acp_orderIncome_byMonth

### Calculated Columns:


```dax
orderIncome_formatted = DIVIDE('sec acp_orderIncome_byMonth'[orderIncome], 1000)
```


## Table: nxtgn_opportunityregistrations

### Calculated Columns:


```dax
estrevenue_base = nxtgn_opportunityregistrations[nxtgn_estrevenue] / RELATED(transactioncurrencies[exchangerate])
```


## Table: nxtgn_shareofwallets

### Measures:


```dax
Weighted Forecast Calculated = CALCULATE(
    SUM(nxtgn_shareofwallets[weighted_order_income]), 
    FILTER(
        nxtgn_opportunityregistrations, 
        AND(
            nxtgn_opportunityregistrations[statuscode] in {204030004, 204030000},
            AND(
                IF(
                    ISFILTERED('msr v_fc_order_income_accumulated'[industry_subject]),
                    nxtgn_opportunityregistrations[nxtgn_SectorSAPId.nxtgn_name] in ALLSELECTED('msr v_fc_order_income_accumulated'[industry_subject]),
                    TRUE()
                ),
                IF(
                    ISFILTERED('msr v_fc_order_income_accumulated'[function_subject]),
                    nxtgn_opportunityregistrations[nxtgn_ThemeSAPId.nxtgn_name] in ALLSELECTED('msr v_fc_order_income_accumulated'[function_subject]),
                    TRUE()
                )
            )
        )
    )
)
```



```dax
Weighted Forecast Formatted = [Weighted Forecast Calculated] * 0.001 * 0.001
```


### Calculated Columns:


```dax
expected_order_income = nxtgn_shareofwallets[nxtgn_countrypercentage] * 0.01 * RELATED(nxtgn_opportunityregistrations[estrevenue_base])
```



```dax
weighted_order_income = RELATED(nxtgn_opportunityregistrations[nxtgn_probability]) * 0.01 * nxtgn_shareofwallets[expected_order_income]
```


## Table: Top Clients/Projects/DMs


```dax
{
    ("Top clients", NAMEOF('msr v_fc_project_data'[project_client_short]), 0),
    ("Top projects", NAMEOF('msr v_fc_order_income_accumulated'[project_name]), 1),
    ("Top DMs", NAMEOF('msr v_fc_project_data'[delivery_manager_short]), 2)
}
```


### Measures:


```dax
Chart Title Gross = SELECTEDVALUE('Top Clients/Projects/DMs'[Name]) & " (gross)"
```



```dax
Chart Title Net = SELECTEDVALUE('Top Clients/Projects/DMs'[Name]) & " (net)"
```


### Calculated Columns:


```dax
Name = 'Top Clients/Projects/DMs'[Top Clients/Projects/DMs]
```


## Table: sec imp_fc_order_income_accumulated_weekly

### Measures:


```dax
OI_Weekly_formatted = DIVIDE(SUM('sec imp_fc_order_income_accumulated_weekly'[order_income_current_week]), 1000)
```

