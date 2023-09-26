



# DAX

|Dataset|[KYS](./../KYS.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_dandb_adhocqueries

### Measures:


```dax
KYS checks in progress = CALCULATE(COUNT(nxtgn_dandb_adhocqueries[nxtgn_dandb_adhocqueryid]), FILTER(nxtgn_dandb_adhocqueries, nxtgn_dandb_adhocqueries[nxtgn_compliancecheckresultstatus_meta]="In Progress"))
```



```dax
Long-term suppliers = CALCULATE(COUNT(nxtgn_dandb_adhocqueries[nxtgn_dandb_adhocqueryid]), FILTER(nxtgn_dandb_adhocqueries, nxtgn_dandb_adhocqueries[nxtgn_contractorrelationshiphalfyear]=TRUE))
```



```dax
Red flags = CALCULATE(COUNT(nxtgn_dandb_adhocqueries[nxtgn_dandb_adhocqueryid]), FILTER(nxtgn_dandb_adhocqueries, nxtgn_dandb_adhocqueries[trafficlight]="Red"))
```



```dax
KYS checks requested = CALCULATE(COUNT(nxtgn_dandb_adhocqueries[nxtgn_dandb_adhocqueryid]))+0
```


### Calculated Columns:


```dax
trafficlight = IF(
    AND(nxtgn_dandb_adhocqueries[nxtgn_compliancecheckresultstatus_meta] in {"Compliance Action recommended", "Compliance Action required", "Completed"}, nxtgn_dandb_adhocqueries[nxtgn_complianceriskscore_rb] >= 100), "Red",
    IF(AND(nxtgn_dandb_adhocqueries[nxtgn_compliancecheckresultstatus_meta] in {"Compliance Action recommended", "Compliance Action required", "Completed"}, AND(nxtgn_dandb_adhocqueries[nxtgn_complianceriskscore_rb] < 100, nxtgn_dandb_adhocqueries[nxtgn_unassignedcomplianceentries]=0)), "Green",
    "Yellow"
))
```



```dax
nxtgn_unassignedcomplianceentries = nxtgn_dandb_adhocqueries[nxtgn_critical_unassigned_complianceentries] + nxtgn_dandb_adhocqueries[nxtgn_critical_unassigned_complianceentries] + 0
```


## Table: nxtgn_dandb_adhocqueries_createdon


```dax
CALENDARAUTO()
```


### Measures:


```dax
QueriesThisWeek = CALCULATE(COUNT(nxtgn_dandb_adhocqueries[nxtgn_dandb_adhocqueryid]))
```



```dax
QueriesLastWeek = CALCULATE(COUNT(nxtgn_dandb_adhocqueries[nxtgn_dandb_adhocqueryid]), FILTER(ALL(nxtgn_dandb_adhocqueries_createdon), nxtgn_dandb_adhocqueries_createdon[WeekRank]=MAX(nxtgn_dandb_adhocqueries_createdon[WeekRank])-1))
```



```dax
WeeklyChangeRunningTotal = [QueriesRunningTotal]/[QueriesRunningTotalLastWeek] - 1
```



```dax
QueriesRunningTotal = CALCULATE(COUNT(nxtgn_dandb_adhocqueries[nxtgn_dandb_adhocqueryid]), FILTER(ALL(nxtgn_dandb_adhocqueries_createdon), nxtgn_dandb_adhocqueries_createdon[Date] <= MAX(nxtgn_dandb_adhocqueries_createdon[Date])))
```



```dax
QueriesRunningTotalLastWeek = CALCULATE(COUNT(nxtgn_dandb_adhocqueries[nxtgn_dandb_adhocqueryid]), FILTER(ALL(nxtgn_dandb_adhocqueries_createdon), nxtgn_dandb_adhocqueries_createdon[WeekRank]<=MAX(nxtgn_dandb_adhocqueries_createdon[WeekRank])-1))
```


### Calculated Columns:


```dax
WeekNum = WEEKNUM([Date], 21)
```



```dax
WeekStartDate = [Date]+-1*WEEKDAY([Date], 2) +1
```



```dax
WeekEndDate = [Date]+7-1*WEEKDAY([Date], 2)
```



```dax
WeekRank = RANKX(ALL(nxtgn_dandb_adhocqueries_createdon), nxtgn_dandb_adhocqueries_createdon[WeekStartDate], , ASC, Dense)
```

