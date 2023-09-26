



# DAX

|Dataset|[Sales Funnel Sustainability Team](./../Sales-Funnel-Sustainability-Team.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_opportunityregistrations

### Measures:


```dax
count_won_opportunities = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"))
```



```dax
revenue_conversion_rate = [won_revenue]/([won_revenue]+[lost_revenue]+[dropped_revenue])
```



```dax
won_revenue = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"))+0
```



```dax
lost_revenue = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Lost"))+0
```



```dax
dropped_revenue = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Dropped"))+0
```



```dax
nxtgn_actualclosedate_selected_from = SELECTEDVALUE(nxtgn_opportunityregistrations[nxtgn_actualclosedate])
```



```dax
sum_nxtgn_estrevenue_base_with_millions_m = SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base])
```



```dax
time_frame = CONCATENATE("Time frame: ", CONCATENATE(FORMAT(FIRSTDATE(nxtgn_actualclosedate_table[nxtgn_actualclosedate]), "dd.mm."), CONCATENATE(" - ", FORMAT(LASTDATE(nxtgn_actualclosedate_table[nxtgn_actualclosedate]), "dd.mm."))))
```



```dax
sum_nxtgn_estrevenue_base = SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base])
```


### Calculated Columns:


```dax
sustainability_related = OR(nxtgn_opportunityregistrations[nxtgn_sustainabilityrelated], nxtgn_opportunityregistrations[nxtgn_innovationtopics_meta]="Circular Economy and Climate Action")
```



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
active_in_dyn_365 = OR(AND(OR(nxtgn_opportunityregistrations[statuscode_meta]="Active", nxtgn_opportunityregistrations[statuscode_meta]="Open"), OR(ISBLANK(nxtgn_opportunityregistrations[nxtgn_estclosedate]), EOMONTH(nxtgn_opportunityregistrations[nxtgn_estclosedate], 1)>=TODAY())), AND(nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won", OR(ISBLANK(nxtgn_opportunityregistrations[nxtgn_ordersactualclosedate]), EOMONTH(nxtgn_opportunityregistrations[nxtgn_ordersactualclosedate], 1)>=TODAY())))
```



```dax
limit_to_previous_month = OR(ISBLANK(nxtgn_opportunityregistrations[nxtgn_estclosedate]), EOMONTH(nxtgn_opportunityregistrations[nxtgn_estclosedate], 0)>=EOMONTH(TODAY(), -1))
```



```dax
weightedrevenue_base = nxtgn_opportunityregistrations[nxtgn_estrevenue_base] * nxtgn_opportunityregistrations[nxtgn_probability] / 100
```



```dax
next_friday_nxtgn_estclosedate = IF(WEEKDAY(nxtgn_opportunityregistrations[nxtgn_estclosedate], 2) <= 5, nxtgn_opportunityregistrations[nxtgn_estclosedate] - WEEKDAY(nxtgn_opportunityregistrations[nxtgn_estclosedate], 2) + 5, nxtgn_opportunityregistrations[nxtgn_estclosedate] - WEEKDAY(nxtgn_opportunityregistrations[nxtgn_estclosedate], 2) + 12)
```



```dax
next_friday_nxtgn_actualclose_date = IF(WEEKDAY(nxtgn_opportunityregistrations[nxtgn_actualclosedate], 2) <= 5, nxtgn_opportunityregistrations[nxtgn_actualclosedate] - WEEKDAY(nxtgn_opportunityregistrations[nxtgn_actualclosedate], 2) + 5, nxtgn_opportunityregistrations[nxtgn_actualclosedate] - WEEKDAY(nxtgn_opportunityregistrations[nxtgn_actualclosedate], 2) + 12)
```



```dax
today = CONCATENATE("Snapshot: ", FORMAT(TODAY(), "dd.mm."))
```



```dax
region_sort_order = IF(RELATED(nxtgn_lookupcountryaliases[nxtgn_name])="Americas", 1, IF(RELATED(nxtgn_lookupcountryaliases[nxtgn_name])="Asia", 2, IF(RELATED(nxtgn_lookupcountryaliases[nxtgn_name])="Europe", 3)))
```



```dax
sca_team_involved = OR(CONTAINSSTRING(nxtgn_opportunityregistrations[nxtgn_salesteam_concatinate], "Rabe, Jan"), OR(CONTAINSSTRING(nxtgn_opportunityregistrations[nxtgn_salesteam_concatinate], "Ruf, Yvonne"), OR(CONTAINSSTRING(nxtgn_opportunityregistrations[nxtgn_salesteam_concatinate], "Koroleva, Daria"), OR(CONTAINSSTRING(nxtgn_opportunityregistrations[nxtgn_salesteam_concatinate], "Zuehlke, Hannah"), OR(CONTAINSSTRING(nxtgn_opportunityregistrations[nxtgn_salesteam_concatinate], "Boehler, Christian"), CONTAINSSTRING(nxtgn_opportunityregistrations[nxtgn_salesteam_concatinate], "Frans, David"))))))
```


## Table: nxtgn_actualclosedate_table


```dax
CALENDAR(IF(WEEKDAY(TODAY(), 2) <= 5, TODAY() - WEEKDAY(TODAY(), 2) + 5 - 55, TODAY() - WEEKDAY(TODAY(), 2) + 12 - 55), IF(WEEKDAY(TODAY(), 2) <= 5, TODAY() - WEEKDAY(TODAY(), 2) + 5, TODAY() - WEEKDAY(TODAY(), 2) + 12))
```


### Calculated Columns:


```dax
nxtgn_actualclosedate_next_friday = IF(WEEKDAY(nxtgn_actualclosedate_table[nxtgn_actualclosedate], 2) <= 5, nxtgn_actualclosedate_table[nxtgn_actualclosedate] - WEEKDAY(nxtgn_actualclosedate_table[nxtgn_actualclosedate], 2) + 5, nxtgn_actualclosedate_table[nxtgn_actualclosedate] - WEEKDAY(nxtgn_actualclosedate_table[nxtgn_actualclosedate], 2) + 12)
```

