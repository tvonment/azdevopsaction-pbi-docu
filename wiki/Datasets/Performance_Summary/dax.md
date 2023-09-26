



# DAX

|Dataset|[Performance_Summary](./../Performance_Summary.md)|
| :--- | :--- |
|Workspace|[Test_4_Michael_Mueller](../../Workspaces/Test_4_Michael_Mueller.md)|

## Table: Sheet1

### Calculated Columns:


```dax
Utilization_Delta = ((Sheet1[Utilization_week 0]-Sheet1[Utilization target])*100)
```



```dax
Utilization Forecast = Sheet1[Utilization_week 0]*1.1
```



```dax
Utilization_week -1 = Sheet1[Utilization_week 0]*0.95
```



```dax
Timesheet target = 100/100
```



```dax
Timesheet actual = Sheet1[Timesheet target]*RAND()
```



```dax
FTE_Last year = 2400
```



```dax
FTE_Current = 2800
```



```dax
FTE_Plan = 2900
```



```dax
Region = if(Sheet1[Country]="DACH","EMEA",if(Sheet1[Country]="France","EMEA",if(Sheet1[Country]="Italy","EMEA",if(Sheet1[Country]="US","Americas","Asia"))))
```

