



# DAX

|Dataset|[20210315_TR_Cost_Data_Master_MC_adj_v02](./../20210315_TR_Cost_Data_Master_MC_adj_v02.md)|
| :--- | :--- |
|Workspace|[TÜV Rheinland](../../Workspaces/TÜV-Rheinland.md)|

## Table: Cost_data

### Measures:


```dax
Wert Measure = 
SUM('Cost_data'[Wert]) 
```


## Table: FTE

### Measures:


```dax
FTE (incl. splits) plus 30.06.2020 = 
SUM('FTE'[FTE (incl. splits)])
```

