



# DAX

|Dataset|[test dashboard](./../test-dashboard.md)|
| :--- | :--- |
|Workspace|[Test Dashboards for tutorial](../../Workspaces/Test-Dashboards-for-tutorial.md)|

## Table: activeKBases table

### Calculated Columns:


```dax
count (operation) = COUNTROWS(FILTER(Table1, Table1[SiteUrl]='activeKBases table'[SiteUrl]))
```

