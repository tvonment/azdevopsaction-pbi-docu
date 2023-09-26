



# DAX

|Dataset|[Opportunity Management](./../Opportunity-Management.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_shareofwallets

### Measures:


```dax
opportunity_estrevenue_selected_currency_sum_distinct = SUMX(SUMMARIZE(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid], nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base]), COALESCE([nxtgn_opportunityregistrations.nxtgn_estrevenue_base], 0)) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
opportunity_weightedvalue_selected_currency_distinct = SUMX(SUMMARIZE(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid], nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base], nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_probability]), COALESCE(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base], 0) * nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_probability] * 0.01) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
calculatedvalue_selected_currency = SUM(nxtgn_shareofwallets[calculatedvalue_base]) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
weightedcalculatedvalue_selected_currency = SUM(nxtgn_shareofwallets[weightedcalculatedvalue_base]) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
count_won_opportunities = CALCULATE(DISTINCTCOUNT(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid]), FILTER(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Won"))
```



```dax
count_lost_opportunities = CALCULATE(DISTINCTCOUNT(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid]), FILTER(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Lost"))
```



```dax
count_dropped_opportunities = CALCULATE(DISTINCTCOUNT(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid]), FILTER(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Dropped"))
```



```dax
conversion_rate = [count_won_opportunities]/([count_won_opportunities]+[count_lost_opportunities]+[count_dropped_opportunities])
```



```dax
nxtgn_opportunityregistrations.average_lifetime = AVERAGEX(SUMMARIZE(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid], nxtgn_shareofwallets[nxtgn_opportunityregistrations.lifetime]), nxtgn_shareofwallets[nxtgn_opportunityregistrations.lifetime])
```



```dax
sum_won_revenue = CALCULATE(SUM(nxtgn_shareofwallets[calculatedvalue_base]), FILTER(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Won"))
```



```dax
sum_lost_revenue = CALCULATE(SUM(nxtgn_shareofwallets[calculatedvalue_base]), FILTER(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Lost"))
```



```dax
sum_dropped_revenue = CALCULATE(SUM(nxtgn_shareofwallets[calculatedvalue_base]), FILTER(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Dropped"))
```



```dax
conversion_rate_revenue = [sum_won_revenue]/([sum_won_revenue]+nxtgn_shareofwallets[sum_lost_revenue]+[sum_dropped_revenue])
```



```dax
share_closed_won_lost_without_competitor = CALCULATE(DISTINCTCOUNT(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid]), FILTER(nxtgn_shareofwallets, AND(OR(nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Won", nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Lost"), ISBLANK(nxtgn_shareofwallets[nxtgn_opportunityregistrations.competitor]))))/CALCULATE(DISTINCTCOUNT(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid]), FILTER(nxtgn_shareofwallets, OR(nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Won", nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Lost")))+0
```



```dax
show_hide_competition_visuals = IF(OR(SELECTEDVALUE(nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]) = "Closed as Won", SELECTEDVALUE(nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]) = "Closed as Lost"), 0, 1)
```



```dax
opportunity_estrevenue_selected_currency_avg_distinct = AVERAGEX(SUMMARIZE(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid], nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base]), COALESCE([nxtgn_opportunityregistrations.nxtgn_estrevenue_base], 0)) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
opportunity_estrevenue_selected_currency_median_distinct = MEDIANX(SUMMARIZE(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid], nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base]), COALESCE([nxtgn_opportunityregistrations.nxtgn_estrevenue_base], 0)) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
nxtgn_opportunityregistrations.median_lifetime = MEDIANX(SUMMARIZE(nxtgn_shareofwallets, nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid], nxtgn_shareofwallets[nxtgn_opportunityregistrations.lifetime]), nxtgn_shareofwallets[nxtgn_opportunityregistrations.lifetime])
```



```dax
count_opportunities = CALCULATE(DISTINCTCOUNT(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid]))
```



```dax
%_opportunities = DIVIDE([count_opportunities], CALCULATE([count_opportunities], ALLSELECTED()))
```



```dax
%_calculatedvalue_selected_currency = DIVIDE([calculatedvalue_selected_currency], CALCULATE([calculatedvalue_selected_currency], ALLSELECTED()))
```



```dax
%_opportunity_estrevenue_selected_currency_sum_distinct = DIVIDE([opportunity_estrevenue_selected_currency_sum_distinct], CALCULATE([opportunity_estrevenue_selected_currency_sum_distinct], ALLSELECTED()))
```



```dax
count_closed_for_only_other_reason = CALCULATE([count_opportunities], FILTER(nxtgn_shareofwallets, AND(CONTAINSSTRINGEXACT(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_closereasons_concatenate], "Other Reason"), NOT(CONTAINSSTRINGEXACT(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_closereasons_concatenate], " | ")))))
```


### Calculated Columns:


```dax
weightedcalculatedvalue_base = COALESCE(nxtgn_shareofwallets[nxtgn_shareofwallets (2).nxtgn_percentage]/100, 1) * nxtgn_shareofwallets[nxtgn_countrypercentage] * 0.01 * COALESCE(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base], 0) * nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_probability] * 0.01
```



```dax
nxtgn_opportunityregistrations.nxtgn_estclosedate (bins) = IF(
  ISBLANK('nxtgn_shareofwallets'[nxtgn_opportunityregistrations.nxtgn_estclosedate]),
  BLANK(),
  DATE(
    YEAR('nxtgn_shareofwallets'[nxtgn_opportunityregistrations.nxtgn_estclosedate]),
    1 + (MONTH('nxtgn_shareofwallets'[nxtgn_opportunityregistrations.nxtgn_estclosedate]) - 1),
    1
  )
)
```



```dax
nxtgn_opportunityregistrations.has_sap_quote_or_probability_100 = OR(NOT(ISBLANK(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_id_customerquotesap])), nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_probability]=100)
```



```dax
nxtgn_opportunityregistrations.active_in_dyn_365 = OR(AND(OR(nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Active", nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Open"), OR(ISBLANK(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estclosedate]), EOMONTH(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estclosedate], 1)>=TODAY())), AND(nxtgn_shareofwallets[nxtgn_opportunityregistrations.statuscodename]="Closed as Won", OR(ISBLANK(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_ordersactualclosedate]), EOMONTH(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_ordersactualclosedate], 1)>=TODAY())))
```



```dax
nxtgn_opportunityregistrations.limit_to_next_4_months = OR(ISBLANK(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estclosedate]), nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estclosedate]<=EOMONTH(TODAY(), 4))
```



```dax
nxtgn_opportunityregistrations.limit_to_previous_month = OR(ISBLANK(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estclosedate]), EOMONTH(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estclosedate], 0)>=EOMONTH(TODAY(), -1))
```



```dax
url = CONCATENATE("https://rolandberger.crm4.dynamics.com/main.aspx?appid=9e3de84b-a781-ea11-a811-000d3a253a0e&newWindow=true&pagetype=entityrecord&etn=nxtgn_opportunityregistration&id=", nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid])
```



```dax
calculatedvalue_base = COALESCE(nxtgn_shareofwallets[nxtgn_shareofwallets (2).nxtgn_percentage]/100, 1) * nxtgn_shareofwallets[nxtgn_countrypercentage] * 0.01 * COALESCE(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base], 0)
```



```dax
nxtgn_opportunityregistrations.nxtgn_sapstatus = IF(ISBLANK(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_id_customerquotesap]), IF(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_probability]=100, "2) No SAP Quote (100% Probability)", "1) <100% Probability"),IF(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_totalrevenue_orders_calc_base]>0, "4) Has SAP Quote and Order", "3) Has SAP Quote (no Order yet)"))
```



```dax
nxtgn_opportunityregistrations.lifetime = DATEDIFF(nxtgn_shareofwallets[nxtgn_opportunityregistrations.createdon], COALESCE(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_actualclosedate], TODAY()), DAY)
```



```dax
nxtgn_opportunityregistrations.nxtgn_estrevenue_base = nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue] / RELATED('transactioncurrency (2)'[exchangerate])
```



```dax
nxtgn_opportunityregistrations.nxtgn_actualclosedate (bins) = IF(
  ISBLANK('nxtgn_shareofwallets'[nxtgn_opportunityregistrations.nxtgn_actualclosedate]),
  BLANK(),
  DATE(
    YEAR('nxtgn_shareofwallets'[nxtgn_opportunityregistrations.nxtgn_actualclosedate]),
    1 + (MONTH('nxtgn_shareofwallets'[nxtgn_opportunityregistrations.nxtgn_actualclosedate]) - 1),
    1
  )
)
```



```dax
nxtgn_opportunityregistrations.competitor = IF(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_competitoridname] = "Other Competitor", nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_othercompetitors], nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_competitoridname])
```



```dax
nxtgn_opportunityregistrations.nxtgn_estrevenue_bucket = IF(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base] >= 2000000, "4) >= EUR 2M", IF(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base] >= 1000000, "3) >= EUR 1M",IF(nxtgn_shareofwallets[nxtgn_opportunityregistrations.nxtgn_estrevenue_base] >= 500000, "2) >= EUR 500k", "1) < EUR 500k")))
```


## Table: nxtgn_opportunityclosereasons

### Calculated Columns:


```dax
nxtgn_statusreasonidname_concat = CONCATENATE(LEFT(RELATED(nxtgn_lookupopportunitystatusreasons[nxtgn_categoryname]), 2), CONCATENATE( "- ", nxtgn_opportunityclosereasons[nxtgn_statusreasonidname]))
```


## Table: nxtgn_lookupopportunitystatusreasons

### Calculated Columns:


```dax
nxtgn_categoryname_formatted = CONCATENATE(LEFT(nxtgn_lookupopportunitystatusreasons[nxtgn_categoryname], 1), CONCATENATE(") ", LEFT(RIGHT(nxtgn_lookupopportunitystatusreasons[nxtgn_categoryname], LEN(nxtgn_lookupopportunitystatusreasons[nxtgn_categoryname])-1), LEN(nxtgn_lookupopportunitystatusreasons[nxtgn_categoryname])-1)))
```


## Table: [Slicer] Measure Selection

### Measures:


```dax
Result = SWITCH(
    SELECTEDVALUE('[Slicer] Measure Selection'[Option]),
    1, [count_opportunities],
    2, [%_opportunities],
    3, [opportunity_estrevenue_selected_currency_sum_distinct],
    4, [%_opportunity_estrevenue_selected_currency_sum_distinct],
    5, [calculatedvalue_selected_currency],
    6, [%_calculatedvalue_selected_currency]
)
```

