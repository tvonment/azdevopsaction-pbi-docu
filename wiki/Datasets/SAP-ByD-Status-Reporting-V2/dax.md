



# DAX

|Dataset|[SAP ByD Status Reporting V2](./../SAP-ByD-Status-Reporting-V2.md)|
| :--- | :--- |
|Workspace|[SAP Business ByDesign](../../Workspaces/SAP-Business-ByDesign.md)|

## Table: TMP Status Report - Budget

### Measures:


```dax
RT_DELTA = CALCULATE(SUM('TMP Status Report - Budget'[H_BUDGET_DELTA]), FILTER(ALL('TMP Status Report - Budget'), 'TMP Status Report - Budget'[ROLLOUT_PROJECT_ID] = SELECTEDVALUE('Rollout Projects'[ROLLOUT_PROJECT_ID]) && 'TMP Status Report - Budget'[DATE_STATUS_REPORT] = SELECTEDVALUE('Status Report'[DATE_STATUS_REPORT]) && 'TMP Status Report - Budget'[SORT_ORDER] <= MAX('TMP Status Report - Budget'[SORT_ORDER])))
```

