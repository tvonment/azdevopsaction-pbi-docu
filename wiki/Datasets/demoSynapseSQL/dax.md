



# DAX

|Dataset|[demoSynapseSQL](./../demoSynapseSQL.md)|
| :--- | :--- |
|Workspace|[Corporate_Reporting_Synapse_PoC](../../Workspaces/Corporate_Reporting_Synapse_PoC.md)|

## Table: nxtgn_opportunityregistraion_T

### Calculated Columns:


```dax
date_snapshot_dynamic = IF([date_snapshot] = MAX([date_snapshot]), "Newest", FORMAT([date_snapshot], "YYYY-MM-DD"))
```



```dax
estrevenue_randomized = nxtgn_opportunityregistraion_T[nxtgn_estrevenue] * nxtgn_opportunityregistraion_T[randomizer]
```



```dax
randomizer = RANDBETWEEN(95,105)/100
```

