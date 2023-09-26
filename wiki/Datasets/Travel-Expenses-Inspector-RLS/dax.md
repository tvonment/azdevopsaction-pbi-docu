



# DAX

|Dataset|[Travel Expenses Inspector RLS](./../Travel-Expenses-Inspector-RLS.md)|
| :--- | :--- |
|Workspace|[Reiser](../../Workspaces/Reiser.md)|

## Table: Data

### Measures:


```dax
EmpID = DISTINCTCOUNT([emp_id])
```



```dax
Count = count(Data[emp_id])
```



```dax
Amount this year = sum(Data[amount_eur])
```



```dax
Amount last year = CALCULATE([Amount this year],SAMEPERIODLASTYEAR('Date'[Date]))
```



```dax
EmpID last year = CALCULATE([EmpID], SAMEPERIODLASTYEAR('Date'[Date]))
```



```dax
Diff amount this year vs last year = [Amount this year]- [Amount last year]
```



```dax
Diff count employee this year vs last year = [EmpID]- [EmpID last year]
```



```dax
Diff Amount pct = ([Amount this year]- [Amount last year])/ [Amount last year]
```



```dax
Diff count pct = ([EmpID]- [EmpID last year])/[EmpID]
```


### Calculated Columns:


```dax
PIDName = [project_number] &" - " & [project_client] &" - " & [project_name] 
```

