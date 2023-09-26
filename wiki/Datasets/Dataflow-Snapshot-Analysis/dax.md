



# DAX

|Dataset|[Dataflow Snapshot Analysis](./../Dataflow-Snapshot-Analysis.md)|
| :--- | :--- |
|Workspace|[Dataflow Snapshots](../../Workspaces/Dataflow-Snapshots.md)|

## Table: Diffs

### Measures:


```dax
Differences = VAR _count = COUNTROWS(Diffs) RETURN IF(ISBLANK(_count), 0, _count)
```


## Table: Diffs Details

### Measures:


```dax
Differences Details = VAR _count = COUNTROWS('Diffs Details') RETURN IF(ISBLANK(_count), 0, _count)
```


### Calculated Columns:


```dax
Change Type = VAR _change = 'Diffs Details'[Change] RETURN IF(LEFT(_change, 4) = " -->", "New Record", IF(RIGHT(_change, 4) = " -->", "Missing Record", "Change"))
```


## Table: Snapshots

### Measures:


```dax
Snapshots = COUNTROWS(Snapshots)
```



```dax
Refreshes = DISTINCTCOUNT(Snapshots[Refresh Number])
```


## Table: Calendar


```dax
CALENDAR(MIN(Snapshots[Date]), MAX(Snapshots[Date]))
```


### Calculated Columns:


```dax
Month Val = MONTH('Calendar'[Date])
```



```dax
Month = FORMAT('Calendar'[Date], "MMM")
```



```dax
Year = YEAR('Calendar'[Date])
```



```dax
Day = DAY('Calendar'[Date])
```

