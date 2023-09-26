



# DAX

|Dataset|[Country, Platform Heads_v01](./../Country,-Platform-Heads_v01.md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: rep v_ll_unit_responsible

### Measures:


```dax
All emails = CONCATENATEX (VALUES('rep v_ll_unit_responsible'[email_responsible]), 'rep v_ll_unit_responsible'[email_responsible], ", ")
```

