



# DAX

|Dataset|[IMF Weo Dashboard_v2](./../IMF-Weo-Dashboard_v2.md)|
| :--- | :--- |
|Workspace|[RBI's Dashboards](../../Workspaces/RBI's-Dashboards.md)|

## Table: Sheet1

### Calculated Columns:


```dax
Scale = if(isblank(Sheet1[Scale_orig])," ",Sheet1[Scale_orig])
```



```dax
Forecast_Dummy = IF (Sheet1[Date] >= Date(2021,01,01),"FC","No FC")

```



```dax
FC = IF (Sheet1[Date] >= Date(2021,01,01),Sheet1[Value],Blank())
```



```dax
No_FC = IF (Sheet1[Date] <= Date(2021,01,01),Sheet1[Value],Blank())
```

