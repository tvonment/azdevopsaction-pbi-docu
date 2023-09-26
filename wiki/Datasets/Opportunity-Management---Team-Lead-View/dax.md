



# DAX

|Dataset|[Opportunity Management - Team Lead View](./../Opportunity-Management---Team-Lead-View.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_opportunityregistrations

### Measures:


```dax
nxtgn_estrevenue_selected_currency = SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
nxtgn_weightedcalculatedvalue_selected_currency = SUMX(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[nxtgn_estrevenue_base]/100 * nxtgn_opportunityregistrations[nxtgn_probability]) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
conversion_rate = [count_won_opportunities]/([count_won_opportunities]+[count_lost_opportunities]+[count_dropped_opportunities])
```



```dax
count_won_opportunities = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscodename]="Closed as Won"))
```



```dax
count_lost_opportunities = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscodename]="Closed as Lost"))
```



```dax
count_dropped_opportunities = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscodename]="Closed as Dropped"))
```



```dax
conversion_rate_revenue = [sum_won_revenue]/([sum_won_revenue]+[sum_lost_revenue]+[sum_dropped_revenue])
```



```dax
sum_won_revenue = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscodename]="Closed as Won"))
```



```dax
sum_lost_revenue = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscodename]="Closed as Lost"))
```



```dax
sum_dropped_revenue = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscodename]="Closed as Dropped"))
```



```dax
share_closed_won_lost_without_competitor = CALCULATE(DISTINCTCOUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, AND(OR(nxtgn_opportunityregistrations[statuscodename]="Closed as Won", nxtgn_opportunityregistrations[statuscodename]="Closed as Lost"), ISBLANK(nxtgn_opportunityregistrations[competitor]))))/CALCULATE(DISTINCTCOUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, OR(nxtgn_opportunityregistrations[statuscodename]="Closed as Won", nxtgn_opportunityregistrations[statuscodename]="Closed as Lost")))+0
```



```dax
average_nxtgn_estrevenue_selected_currency = AVERAGE(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]) * SELECTEDVALUE(transactioncurrency[exchangerate])
```



```dax
median_nxtgn_estrevenue_selected_currency = MEDIAN(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]) * SELECTEDVALUE(transactioncurrency[exchangerate])
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
nxtgn_estrevenue_base = COALESCE(nxtgn_opportunityregistrations[nxtgn_estrevenue] / RELATED('transactioncurrency (2)'[exchangerate]), 0)
```



```dax
limit_to_previous_month = OR(ISBLANK([nxtgn_estclosedate]), EOMONTH([nxtgn_estclosedate], 0)>=EOMONTH(TODAY(), -1))
```



```dax
nxtgn_opportunityregistrations.nxtgn_sapstatus = IF(ISBLANK([nxtgn_id_customerquotesap]), IF([nxtgn_probability]=100, "2) No SAP Quote (100% Probability)", "1) <100% Probability"),IF([nxtgn_totalrevenue_orders_calc_base]>0, "4) Has SAP Quote and Order", "3) Has SAP Quote (no Order yet)"))
```



```dax
url = CONCATENATE("https://rolandberger.crm4.dynamics.com/main.aspx?appid=9e3de84b-a781-ea11-a811-000d3a253a0e&newWindow=true&pagetype=entityrecord&etn=nxtgn_opportunityregistration&id=", [nxtgn_opportunityregistrationid])
```



```dax
lifetime = DATEDIFF([createdon], COALESCE([nxtgn_actualclosedate], TODAY()), DAY)
```



```dax
competitor = IF(nxtgn_opportunityregistrations[nxtgn_competitoridname] = "Other Competitor", nxtgn_opportunityregistrations[nxtgn_othercompetitors], nxtgn_opportunityregistrations[nxtgn_competitoridname])
```



```dax
nxtgn_estrevenue_bucket = IF(nxtgn_opportunityregistrations[nxtgn_estrevenue_base] >= 2000000, "4) >= EUR 2M", IF(nxtgn_opportunityregistrations[nxtgn_estrevenue_base] >= 1000000, "3) >= EUR 1M",IF(nxtgn_opportunityregistrations[nxtgn_estrevenue_base] >= 500000, "2) >= EUR 500k", "1) < EUR 500k")))
```



```dax
nxtgn_opportunityregistrations.limit_to_previous_month = OR(ISBLANK(nxtgn_opportunityregistrations[nxtgn_estclosedate]), EOMONTH(nxtgn_opportunityregistrations[nxtgn_estclosedate], 0)>=EOMONTH(TODAY(), -1))
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

