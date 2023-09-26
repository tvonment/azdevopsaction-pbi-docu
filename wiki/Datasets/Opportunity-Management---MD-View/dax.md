



# DAX

|Dataset|[Opportunity Management - MD View](./../Opportunity-Management---MD-View.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_opportunityregistrations

### Measures:


```dax
count_opportunities = COUNTROWS(nxtgn_opportunityregistrations)+0
```



```dax
count_opportunities_missing_estclosedate = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, ISBLANK(nxtgn_opportunityregistrations[nxtgn_estclosedate])))+0
```



```dax
share_opportunities_missing_estclosedate = 
DIVIDE(
	[count_opportunities_missing_estclosedate],
	[count_opportunities]
)
```



```dax
count_opportunities_missing_estrevenue = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, ISBLANK(nxtgn_opportunityregistrations[nxtgn_estrevenue_base])))+0
```



```dax
share_opportunities_missing_estrevenue = 
DIVIDE([count_opportunities_missing_estrevenue], [count_opportunities])
```



```dax
count_open_or_won_opportunities = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, OR(nxtgn_opportunityregistrations[statuscode_meta]="Open", nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won")))+0
```



```dax
conversion_rate = DIVIDE([count_won_opportunities], [count_opportunities])
```



```dax
count_won_opportunities = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"))+0
```



```dax
average_cycle_time_won_opportunities_ltm = CALCULATE(AVERAGE(nxtgn_opportunityregistrations[cycle_time]), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won", nxtgn_opportunityregistrations[limit_to_last_12_months])))+0
```



```dax
average_cycle_time_lost_opportunities_ltm = CALCULATE(AVERAGE(nxtgn_opportunityregistrations[cycle_time]), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[statuscode_meta]="Closed as Lost", nxtgn_opportunityregistrations[limit_to_last_12_months])))+0
```



```dax
revenue_conversion_rate_value = [revenue_conversion_rate_ltm] * SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base_open_won_limit_to_previous_month])
```



```dax
delta_weighted_conversion_rate = DIVIDE(SUM(nxtgn_opportunityregistrations[nxtgn_weightedvalue_base_open_won_limit_to_previous_month]), [revenue_conversion_rate_value]) - 1
```



```dax
count_open_or_won_opportunities_limit_to_previous_month = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[limit_to_previous_month], OR(nxtgn_opportunityregistrations[statuscode_meta]="Open", nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"))))+0
```



```dax
count_opportunities_ltm = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[limit_to_last_12_months]))+0
```



```dax
count_won_opportunities_ltm = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[limit_to_last_12_months], nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won")))+0
```



```dax
conversion_rate_ltm = DIVIDE([count_won_opportunities_ltm], [count_opportunities_ltm])
```



```dax
count_open_opportunities_limit_to_previous_month = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[limit_to_previous_month], nxtgn_opportunityregistrations[statuscode_meta]="Open")))+0
```



```dax
sum_won_opportunities_ltm = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[limit_to_last_12_months], nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won")))+0
```



```dax
sum_lost_opportunities_ltm = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[limit_to_last_12_months], nxtgn_opportunityregistrations[statuscode_meta]="Closed as Lost")))+0
```



```dax
sum_dropped_opportunities_ltm = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[limit_to_last_12_months], nxtgn_opportunityregistrations[statuscode_meta]="Closed as Dropped")))+0
```



```dax
revenue_conversion_rate_ltm = DIVIDE([sum_won_opportunities_ltm], [sum_won_opportunities_ltm] + [sum_lost_opportunities_ltm] + [sum_dropped_opportunities_ltm])
```



```dax
median_cycle_time_won_opportunities_ltm = CALCULATE(MEDIAN(nxtgn_opportunityregistrations[cycle_time]), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won", nxtgn_opportunityregistrations[limit_to_last_12_months])))+0
```



```dax
median_cycle_time_lost_opportunities_ltm = CALCULATE(MEDIAN(nxtgn_opportunityregistrations[cycle_time]), FILTER(nxtgn_opportunityregistrations, AND(nxtgn_opportunityregistrations[statuscode_meta]="Closed as Lost", nxtgn_opportunityregistrations[limit_to_last_12_months])))+0
```



```dax
expected_conversion_rate_limit_to_previous_month = DIVIDE(SUM(nxtgn_opportunityregistrations[nxtgn_weightedvalue_base_open_won_limit_to_previous_month]), SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base_open_won_limit_to_previous_month]))
```



```dax
monthly_budget = CALCULATE(SUM('Country Budgets'[Budget]), FILTER('Country Budgets', AND(MAX(nxtgn_opportunityregistrations[nxtgn_estclosedate]) <= 'Country Budgets'[Valid To], MIN(nxtgn_opportunityregistrations[nxtgn_estclosedate]) >= 'Country Budgets'[Valid From])))
```



```dax
delta_weighted_conversion_rate_2 = DIVIDE(CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_weightedvalue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta] in {"Closed as Won", "Open"})), CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta] in {"Closed as Won", "Open"})) * [revenue_conversion_rate]) - 1
```



```dax
revenue_conversion_rate = COALESCE(DIVIDE(CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"))+0, CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta] in {"Closed as Won", "Closed as Dropped", "Closed as Lost"}))+0),0)
```



```dax
expected_conversion_rate = DIVIDE(SUM(nxtgn_opportunityregistrations[nxtgn_weightedvalue_base]), SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]))
```


### Calculated Columns:


```dax
nxtgn_estclosedate (bins) = IF(
  ISBLANK('nxtgn_opportunityregistrations'[nxtgn_estclosedate]),
  BLANK(),
  DATE(
    YEAR('nxtgn_opportunityregistrations'[nxtgn_estclosedate]),
    1 + (MONTH('nxtgn_opportunityregistrations'[nxtgn_estclosedate]) - 1),
    1
  )
)
```



```dax
nxtgn_weightedvalue_base = nxtgn_opportunityregistrations[nxtgn_probability] * 0.01 * nxtgn_opportunityregistrations[nxtgn_estrevenue_base]
```



```dax
cycle_time = DATEDIFF(nxtgn_opportunityregistrations[createdon], nxtgn_opportunityregistrations[nxtgn_actualclosedate], DAY)
```



```dax
estclosedate_bucket_max_3_months = 
VAR month = SWITCH(MONTH([nxtgn_estclosedate]),
    1, "-01",
    2, "-02",
    3, "-03",
    4, "-04",
    5, "-05",
    6, "-06",
    7, "-07",
    8, "-08",
    9, "-09",
    10, "-10",
    11, "-11",
    12, "-12"
)
VAR month_in_3_months = SWITCH(MONTH(EOMONTH(TODAY(), 3)),
    1, "-01",
    2, "-02",
    3, "-03",
    4, "-04",
    5, "-05",
    6, "-06",
    7, "-07",
    8, "-08",
    9, "-09",
    10, "-10",
    11, "-11",
    12, "-12"
)
VAR month_bucket = CONCATENATE(YEAR([nxtgn_estclosedate]), month)
RETURN IF(nxtgn_opportunityregistrations[nxtgn_estclosedate]<=EOMONTH(TODAY(), 2), month_bucket, CONCATENATE(CONCATENATE(YEAR(EOMONTH(TODAY(), 3)), month_in_3_months), " or later"))
```



```dax
limit_to_previous_month = OR(ISBLANK(nxtgn_opportunityregistrations[nxtgn_estclosedate]), EOMONTH(nxtgn_opportunityregistrations[nxtgn_estclosedate], 0)>=EOMONTH(TODAY(), -1))
```



```dax
nxtgn_estrevenue_base_open_won = IF(OR(nxtgn_opportunityregistrations[statuscode_meta]="Open", nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"), nxtgn_opportunityregistrations[nxtgn_estrevenue_base], 0)
```



```dax
nxtgn_weightedvalue_base_open_won = IF(OR(nxtgn_opportunityregistrations[statuscode_meta]="Open", nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"), nxtgn_opportunityregistrations[nxtgn_weightedvalue_base], 0)
```



```dax
nxtgn_estrevenue_base_open_won_limit_to_previous_month = IF(AND(nxtgn_opportunityregistrations[limit_to_previous_month], OR(nxtgn_opportunityregistrations[statuscode_meta]="Open", nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won")), nxtgn_opportunityregistrations[nxtgn_estrevenue_base], 0)
```



```dax
nxtgn_weightedvalue_base_open_won_limit_to_previous_month = IF(AND(nxtgn_opportunityregistrations[limit_to_previous_month], OR(nxtgn_opportunityregistrations[statuscode_meta]="Open", nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won")), nxtgn_opportunityregistrations[nxtgn_weightedvalue_base], 0)
```



```dax
limit_to_last_12_months = AND(EOMONTH(nxtgn_opportunityregistrations[nxtgn_estclosedate], 0)>=EOMONTH(TODAY(), -12), EOMONTH(nxtgn_opportunityregistrations[nxtgn_estclosedate], 0)<=EOMONTH(TODAY(), 0))
```



```dax
total_opportunities_descr = "Total Opportunities"
```



```dax
estclosedate_bucket_max_5_months = 
VAR month = SWITCH(MONTH([nxtgn_estclosedate]),
    1, "-01",
    2, "-02",
    3, "-03",
    4, "-04",
    5, "-05",
    6, "-06",
    7, "-07",
    8, "-08",
    9, "-09",
    10, "-10",
    11, "-11",
    12, "-12"
)
VAR month_in_5_months = SWITCH(MONTH(EOMONTH(TODAY(), 5)),
    1, "-01",
    2, "-02",
    3, "-03",
    4, "-04",
    5, "-05",
    6, "-06",
    7, "-07",
    8, "-08",
    9, "-09",
    10, "-10",
    11, "-11",
    12, "-12"
)
VAR month_bucket = CONCATENATE(YEAR([nxtgn_estclosedate]), month)
RETURN IF(nxtgn_opportunityregistrations[nxtgn_estclosedate]<=EOMONTH(TODAY(), 4), month_bucket, CONCATENATE(CONCATENATE(YEAR(EOMONTH(TODAY(), 5)), month_in_5_months), " or later"))
```



```dax
nxtgn_probability (bins) = IF(nxtgn_opportunityregistrations[nxtgn_probability]>=80,"1) >=80%",IF(nxtgn_opportunityregistrations[nxtgn_probability]>=60,"2) 80-60%", IF(nxtgn_opportunityregistrations[nxtgn_probability]>=0, "3) <60%", "")))
```



```dax
nxtgn_countryid_value (groups) = SWITCH(
  TRUE,
  ISBLANK('nxtgn_opportunityregistrations'[nxtgn_countryid_value]),
  "(Blank)",
  'nxtgn_opportunityregistrations'[nxtgn_countryid_value] IN {"Austria",
    "Germany",
    "Switzerland"},
  "DACH",
  'nxtgn_opportunityregistrations'[nxtgn_countryid_value] IN {"Bahrain",
    "Qatar",
    "Saudi Arabia",
    "United Arab Emirates"},
  "Middle East",
  'nxtgn_opportunityregistrations'[nxtgn_countryid_value] IN {"Indonesia",
    "Malaysia",
    "Singapore",
    "Thailand"},
  "South East Asia",
  'nxtgn_opportunityregistrations'[nxtgn_countryid_value]
)
```



```dax
nxtgn_estrevenue_base = nxtgn_opportunityregistrations[nxtgn_estrevenue] / RELATED('transactioncurrencies'[exchangerate])
```



```dax
nxtgn_estrevenue_base_bucket = IF(nxtgn_opportunityregistrations[nxtgn_estrevenue_base] >= 2000000, "1) >= EUR 2.0 m", IF(nxtgn_opportunityregistrations[nxtgn_estrevenue_base] >= 1000000, "2) < EUR 2.0 m - >= EUR 1.0 m", IF(nxtgn_opportunityregistrations[nxtgn_estrevenue_base] >= 500000, "3) < EUR 1.0 m - >= EUR 0.5 m", "4) < EUR 0.5 m")))
```



```dax
nxtgn_weightedrevenue_base_bucket = IF(nxtgn_opportunityregistrations[nxtgn_weightedvalue_base] >= 1000000, "1) >= EUR 1.0 m", IF(nxtgn_opportunityregistrations[nxtgn_weightedvalue_base] >= 500000, "2) < EUR 1.0 m - >= EUR 0.5 m", "3) < EUR 0.5 m"))
```


## Table: systemusers (2)

### Calculated Columns:


```dax
nxtgn_dachplatformidname = IF(OR('systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]="Austria", OR('systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]="Germany",'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]="Switzerland")), 'systemusers (2)'[nxtgn_platformid.nxtgn_name], "")
```



```dax
nxtgn_dachcountryidname = IF(OR('systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]="Austria", OR('systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]="Germany",'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]="Switzerland")), "DACH", 'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name])
```



```dax
nxtgn_countryplatformname = IF(NOT('systemusers (2)'[nxtgn_dachplatformidname]=""), CONCATENATE("DACH - ", 'systemusers (2)'[nxtgn_dachplatformidname]), 'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name])
```



```dax
dachcountry_platform_sort_order = CONCATENATE('systemusers (2)'[nxtgn_dachcountryidname], IF('systemusers (2)'[nxtgn_dachcountryidname]="DACH", 'systemusers (2)'[platform_sort_order], ""))
```



```dax
nxtgn_lookupcountryid.nxtgn_name (groups) = SWITCH(
  TRUE,
  ISBLANK('systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]),
  "(Blank)",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name] IN {"Austria",
    "Germany",
    "Switzerland"},
  "DACH",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name] IN {"Bahrain",
    "Qatar",
    "Saudi Arabia",
    "United Arab Emirates"},
  "Middle East",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name] IN {"Indonesia",
    "Malaysia",
    "Singapore",
    "Thailand",
    "Vietnam"},
  "South East Asia",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]
)
```



```dax
nxtgn_lookupcountryid.nxtgn_name (budget_groups) = SWITCH(
  TRUE,
  ISBLANK('systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]),
  "(Blank)",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name] IN {"China",
    "Hong Kong"},
  "China & Hong Kong",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name] IN {"Austria",
    "Germany",
    "Switzerland"},
  "DACH",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name] IN {"Sweden"},
  "Norway & Sweden",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name] IN {"Malaysia",
    "Singapore",
    "Thailand",
    "Vietnam"},
  "South East Asia",
  'systemusers (2)'[nxtgn_lookupcountryid.nxtgn_name]
)
```


## Table: nxtgn_shareofwallets

### Calculated Columns:


```dax
weightedcalculatedvalue_base = COALESCE(nxtgn_shareofwallets[nxtgn_shareofwallets (2).nxtgn_percentage] * 0.01, 1) * nxtgn_shareofwallets[nxtgn_countrypercentage] * 0.01 * COALESCE(RELATED(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), 0) * RELATED(nxtgn_opportunityregistrations[nxtgn_probability]) * 0.01
```



```dax
calculatedvalue_base = COALESCE(nxtgn_shareofwallets[nxtgn_shareofwallets (2).nxtgn_percentage] * 0.01, 1) * nxtgn_shareofwallets[nxtgn_countrypercentage] * 0.01 * COALESCE(RELATED(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), 0)
```



```dax
nxtgn_countryidname_dach = IF(OR(nxtgn_shareofwallets[nxtgn_countryid.nxtgn_name]="Austria", OR(nxtgn_shareofwallets[nxtgn_countryid.nxtgn_name]="Germany", nxtgn_shareofwallets[nxtgn_countryid.nxtgn_name]="Switzerland")), "DACH", nxtgn_shareofwallets[nxtgn_countryid.nxtgn_name])
```



```dax
ica_shareofwallet = RELATED(nxtgn_opportunityregistrations[nxtgn_countryid_value (groups)]) <> nxtgn_shareofwallets[nxtgn_countryid.nxtgn_name (groups)]
```



```dax
nxtgn_countryid.nxtgn_name (groups) = SWITCH(
  TRUE,
  ISBLANK('nxtgn_shareofwallets'[nxtgn_countryid.nxtgn_name]),
  "(Blank)",
  'nxtgn_shareofwallets'[nxtgn_countryid.nxtgn_name] IN {"Austria",
    "Germany",
    "Switzerland"},
  "DACH",
  'nxtgn_shareofwallets'[nxtgn_countryid.nxtgn_name] IN {"Bahrain",
    "Qatar",
    "Saudi Arabia",
    "United Arab Emirates"},
  "Middle East",
  'nxtgn_shareofwallets'[nxtgn_countryid.nxtgn_name] IN {"Indonesia",
    "Malaysia",
    "Singapore",
    "Thailand",
    "Vietnam"},
  "South East Asia",
  'nxtgn_shareofwallets'[nxtgn_countryid.nxtgn_name]
)
```


## Table: nxtgn_lookupcountryalias (2)

### Calculated Columns:


```dax
region = SUBSTITUTE('nxtgn_lookupcountryalias (2)'[nxtgn_name], " (RB)", "")
```


## Table: nxtgn_lookupcountries

### Measures:


```dax
delta_revenue_streams = SUM('nxtgn_shareofwallets (3)'[weightedcalculatedvalue_base]) - SUM(nxtgn_shareofwallets[weightedcalculatedvalue_base])
```



```dax
sum_incoming_revenue_streams = SUM('nxtgn_shareofwallets (3)'[weightedcalculatedvalue_base])
```


### Calculated Columns:


```dax
nxtgn_name (groups) = SWITCH(
  TRUE,
  ISBLANK('nxtgn_lookupcountries'[nxtgn_name]),
  "(Blank)",
  'nxtgn_lookupcountries'[nxtgn_name] IN {"Austria",
    "Germany",
    "Switzerland"},
  "DACH",
  'nxtgn_lookupcountries'[nxtgn_name] IN {"Bahrain",
    "Lebanon",
    "Qatar",
    "Saudi Arabia",
    "United Arab Emirates"},
  "Middle East",
  'nxtgn_lookupcountries'[nxtgn_name] IN {"Indonesia",
    "Malaysia",
    "Myanmar",
    "Singapore",
    "Thailand",
    "Vietnam"},
  "South East Asia",
  'nxtgn_lookupcountries'[nxtgn_name]
)
```


## Table: nxtgn_shareofwallets (3)

### Calculated Columns:


```dax
ica_shareofwallet = RELATED('nxtgn_opportunityregistrations (2)'[nxtgn_countryid_value (groups)]) <> 'nxtgn_shareofwallets (3)'[nxtgn_countryid.nxtgn_name (groups)]
```



```dax
nxtgn_countryid.nxtgn_name (groups) = SWITCH(
  TRUE,
  ISBLANK('nxtgn_shareofwallets (3)'[nxtgn_countryid.nxtgn_name]),
  "(Blank)",
  'nxtgn_shareofwallets (3)'[nxtgn_countryid.nxtgn_name] IN {"Austria",
    "Germany",
    "Switzerland"},
  "DACH",
  'nxtgn_shareofwallets (3)'[nxtgn_countryid.nxtgn_name] IN {"Bahrain",
    "Qatar",
    "Saudi Arabia",
    "United Arab Emirates"},
  "Middle East",
  'nxtgn_shareofwallets (3)'[nxtgn_countryid.nxtgn_name] IN {"Indonesia",
    "Malaysia",
    "Singapore",
    "Thailand",
    "Vietnam"},
  "South East Asia",
  'nxtgn_shareofwallets (3)'[nxtgn_countryid.nxtgn_name]
)
```



```dax
weightedcalculatedvalue_base = COALESCE('nxtgn_shareofwallets (3)'[nxtgn_shareofwallets (2).nxtgn_percentage] * 0.01, 1) * 'nxtgn_shareofwallets (3)'[nxtgn_countrypercentage] * 0.01 * COALESCE(RELATED('nxtgn_opportunityregistrations (2)'[nxtgn_estrevenue_base]), 0) * RELATED('nxtgn_opportunityregistrations (2)'[nxtgn_probability]) * 0.01
```


## Table: nxtgn_opportunityregistrations (2)

### Calculated Columns:


```dax
nxtgn_countryid_value (groups) = SWITCH(
  TRUE,
  ISBLANK('nxtgn_opportunityregistrations (2)'[nxtgn_countryid_value]),
  "(Blank)",
  'nxtgn_opportunityregistrations (2)'[nxtgn_countryid_value] IN {"Austria",
    "Germany",
    "Switzerland"},
  "DACH",
  'nxtgn_opportunityregistrations (2)'[nxtgn_countryid_value] IN {"Bahrain",
    "Qatar",
    "Saudi Arabia",
    "United Arab Emirates"},
  "Middle East",
  'nxtgn_opportunityregistrations (2)'[nxtgn_countryid_value] IN {"Indonesia",
    "Malaysia",
    "Singapore",
    "Thailand"},
  "South East Asia",
  'nxtgn_opportunityregistrations (2)'[nxtgn_countryid_value]
)
```



```dax
limit_to_previous_month = OR(ISBLANK('nxtgn_opportunityregistrations (2)'[nxtgn_estclosedate]), EOMONTH('nxtgn_opportunityregistrations (2)'[nxtgn_estclosedate], 0)>=EOMONTH(TODAY(), -1))
```



```dax
nxtgn_estrevenue_base = 'nxtgn_opportunityregistrations (2)'[nxtgn_estrevenue] / RELATED('transactioncurrencies (2)'[exchangerate])
```


## Table: Country Budgets

### Measures:


```dax
weighted_order_income_measure = CALCULATE(SUM(nxtgn_shareofwallets[weightedcalculatedvalue_base]), FILTER(nxtgn_shareofwallets, AND(nxtgn_shareofwallets[nxtgn_countryid.nxtgn_lookupcountryid] = MAX('Country Budgets'[Country ID]), AND(RELATED(nxtgn_opportunityregistrations[nxtgn_estclosedate]) >= MAX('Country Budgets'[Valid From]), RELATED(nxtgn_opportunityregistrations[nxtgn_estclosedate]) <= MAX('Country Budgets'[Valid To])))))
```



```dax
progress = DIVIDE(SUM('Country Budgets'[weighted_order_income_calculated_column]), SUM('Country Budgets'[Budget]))
```



```dax
pipeline_reach = DIVIDE(SUM('Country Budgets'[weighted_order_income_calculated_column]), SUM('Country Budgets'[Budget])/12)
```



```dax
progress_2 = DIVIDE(SUM(nxtgn_opportunityregistrations[nxtgn_weightedvalue_base]), SUM('Country Budgets'[Budget]))
```


### Calculated Columns:


```dax
Valid From Bucket = 
VAR month = SWITCH(MONTH([Valid From]),
    1, "-01",
    2, "-02",
    3, "-03",
    4, "-04",
    5, "-05",
    6, "-06",
    7, "-07",
    8, "-08",
    9, "-09",
    10, "-10",
    11, "-11",
    12, "-12"
)
RETURN CONCATENATE(YEAR([Valid From]), month)
```



```dax
weighted_order_income_calculated_column = CALCULATE(SUM(nxtgn_shareofwallets[weightedcalculatedvalue_base]), FILTER(nxtgn_shareofwallets, AND(nxtgn_shareofwallets[nxtgn_countryid.nxtgn_lookupcountryid] = 'Country Budgets'[Country ID], AND(RELATED(nxtgn_opportunityregistrations[nxtgn_estclosedate]) >= 'Country Budgets'[Valid From], AND(RELATED(nxtgn_opportunityregistrations[nxtgn_estclosedate]) <= 'Country Budgets'[Valid To], OR(RELATED(nxtgn_opportunityregistrations[statuscode_meta]) = "Open", RELATED(nxtgn_opportunityregistrations[statuscode_meta]) = "Closed as Won"))))))
```



```dax
last_current_next_three_month = AND(EOMONTH('Country Budgets'[Valid From], -1) >= EOMONTH(TODAY(), -2), EOMONTH('Country Budgets'[Valid From], 0) <= EOMONTH(TODAY(), 3))
```



```dax
Country (groups) = SWITCH(
	TRUE,
	ISBLANK('Country Budgets'[Country]),
	"(Blank)",
	'Country Budgets'[Country] IN {"Austria",
		"Germany",
		"Switzerland"},
	"DACH",
	'Country Budgets'[Country] IN {"Norway",
		"Sweden"},
	"Norway & Sweden",
	'Country Budgets'[Country] IN {"Hong Kong",
		"Indonesia",
		"Malaysia",
		"Singapore",
		"Thailand",
		"Vietnam"},
	"South East Asia",
	'Country Budgets'[Country]
)
```


## Table: nxtgn_lookupcountryalias (3)

### Calculated Columns:


```dax
region = SUBSTITUTE('nxtgn_lookupcountryalias (3)'[nxtgn_name], " (RB)", "")
```


## Table: calendar_nxtgn_estclosedate


```dax
CALENDAR(MIN(nxtgn_opportunityregistrations[nxtgn_estclosedate]), EOMONTH(TODAY(), 12))
```


### Calculated Columns:


```dax
nxtgn_estclosedate (bins) = IF(
  ISBLANK('calendar_nxtgn_estclosedate'[nxtgn_estclosedate]),
  BLANK(),
  DATE(
    YEAR('calendar_nxtgn_estclosedate'[nxtgn_estclosedate]),
    1 + (MONTH('calendar_nxtgn_estclosedate'[nxtgn_estclosedate]) - 1),
    1
  )
)
```


## Table: Industry Platform Budgets

### Measures:


```dax
Industry Market Performance Progress = DIVIDE(SUM('Industry Platform Budgets'[Market Performance (Industry)]), SUM('Industry Platform Budgets'[Budget]))
```


### Calculated Columns:


```dax
Market Performance (Industry) = CALCULATE(SUM('nxtgn_opportunityregistrations'[nxtgn_weightedvalue_base]), FILTER(nxtgn_opportunityregistrations, AND(RELATED(nxtgn_lookupindustryccs[_nxtgn_platformid_value]) = 'Industry Platform Budgets'[Platform ID], AND(nxtgn_opportunityregistrations[nxtgn_estclosedate] >= 'Industry Platform Budgets'[Valid From], AND(nxtgn_opportunityregistrations[nxtgn_estclosedate] <= 'Industry Platform Budgets'[Valid To], OR(nxtgn_opportunityregistrations[statuscode_meta] = "Open", nxtgn_opportunityregistrations[statuscode_meta] = "Closed as Won"))))))
```



```dax
Valid From Bucket = 
VAR month = SWITCH(MONTH([Valid From]),
    1, "-01",
    2, "-02",
    3, "-03",
    4, "-04",
    5, "-05",
    6, "-06",
    7, "-07",
    8, "-08",
    9, "-09",
    10, "-10",
    11, "-11",
    12, "-12"
)
RETURN CONCATENATE(YEAR([Valid From]), month)
```



```dax
last_current_next_three_month = AND(EOMONTH('Industry Platform Budgets'[Valid From], -1) >= EOMONTH(TODAY(), -2), EOMONTH('Industry Platform Budgets'[Valid From], 0) <= EOMONTH(TODAY(), 3))
```


## Table: Functional Platform Budgets

### Measures:


```dax
Functional Market Performance Progress = DIVIDE(SUM('Functional Platform Budgets'[Market Performance (Function)]), SUM('Functional Platform Budgets'[Budget]))
```


### Calculated Columns:


```dax
last_current_next_three_month = AND(EOMONTH('Functional Platform Budgets'[Valid From], -1) >= EOMONTH(TODAY(), -2), EOMONTH('Functional Platform Budgets'[Valid From], 0) <= EOMONTH(TODAY(), 3))
```



```dax
Market Performance (Function) = CALCULATE(SUM('nxtgn_opportunityregistrations'[nxtgn_weightedvalue_base]), FILTER(nxtgn_opportunityregistrations, AND(RELATED(nxtgn_lookupfunctionccs[_nxtgn_platformid_value]) = 'Functional Platform Budgets'[Platform ID], AND(nxtgn_opportunityregistrations[nxtgn_estclosedate] >= 'Functional Platform Budgets'[Valid From], AND(nxtgn_opportunityregistrations[nxtgn_estclosedate] <= 'Functional Platform Budgets'[Valid To], OR(nxtgn_opportunityregistrations[statuscode_meta] = "Open", nxtgn_opportunityregistrations[statuscode_meta] = "Closed as Won"))))))
```



```dax
Valid From Bucket = 
VAR month = SWITCH(MONTH([Valid From]),
    1, "-01",
    2, "-02",
    3, "-03",
    4, "-04",
    5, "-05",
    6, "-06",
    7, "-07",
    8, "-08",
    9, "-09",
    10, "-10",
    11, "-11",
    12, "-12"
)
RETURN CONCATENATE(YEAR([Valid From]), month)
```

