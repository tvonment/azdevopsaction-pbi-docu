



# DAX

|Dataset|[SAMI_ERP_Way_Forward_Dashboard](./../SAMI_ERP_Way_Forward_Dashboard.md)|
| :--- | :--- |
|Workspace|[SAMI ERP](../../Workspaces/SAMI-ERP.md)|

## Table: Master progress

### Measures:


```dax
Total_Actions = var a  = COUNT('Master progress'[Action #])
return IF(ISBLANK(a),0,a)
```



```dax
Action_Count = var a  = CALCULATE(COUNT('Master progress'[Action #]))
return IF(ISBLANK(a),0,a)
```



```dax
Progress% = var a = (SUMX('Master progress','Master progress'[Planned days] * 'Master progress'[Progress (%)]))/ 100
var b = CALCULATE(SUM('Master progress'[Planned days]))
return IF(ISBLANK(a/b),0,a/b)
```



```dax
Target_Progress_display% = var a = IF(ISBLANK([Target_Progress_%]),0,[Target_Progress_%])
 return "Target progess: " & FORMAT(a,"0%")
```



```dax
Target_Progress_% = var a = (SUMX('Master progress','Master progress'[Planned days] * 'Master progress'[Target progress (%)]))/ 100
var b = CALCULATE(SUM('Master progress'[Planned days]))
var c = IF(ISBLANK(a/b),0,a/b)
return c
```



```dax
Target_Progress_Color = DIVIDE('Master progress'[Progress%],[Target_Progress_%],1)
```



```dax
show_in_table_when_filtered = IF(SELECTEDVALUE('Master progress'[Status]) = "Planned" && [Target_Progress_%] = 0,1,IF([Target_Progress_%] > 0,1,0))
```


### Calculated Columns:


```dax
Due_Date_Formatted = FORMAT('Master progress'[Planned due date],"dd-mm-yyyy")
```



```dax
Updated_Due_Date_Formatted = FORMAT('Master progress'[Updated due date],"dd-mm-yyyy")
```



```dax
Workstream_filter = 'Master progress'[Stream #] & " - " & 'Master progress'[Stream]
```



```dax
Milestone-matrix = 'Master progress'[Milestone #] & " - " & 'Master progress'[Milestone]
```



```dax
Current_Due_date = FORMAT(MAX('Master progress'[Planned due date],'Master progress'[Updated due date]),"dd-mm-yyyy")
```



```dax
Start_Date_Formatted = FORMAT('Master progress'[Start date],"dd-mm-yyyy")
```



```dax
Action_display = 'Master progress'[Action #] & "-" & 'Master progress'[Action]
```


## Table: Issues & risks tracker

### Measures:


```dax
Issue_Count = var a = CALCULATE(COUNT('Issues & risks tracker'[Action]), 'Issues & risks tracker'[Flag (1-issue, 2-risk)] =1)
return IF(ISBLANK(a),0,a)
```



```dax
RiskCount = var a = CALCULATE(COUNT('Issues & risks tracker'[Action]), 'Issues & risks tracker'[Flag (1-issue, 2-risk)] =2)
return IF(ISBLANK(a),0,a)
```



```dax
Issue_and_Risk_Count = var a = COUNT('Issues & risks tracker'[Action])
return IF(ISBLANK(a),0,a)
```


### Calculated Columns:


```dax
Workstream_filter = 'Issues & risks tracker'[Stream #] & " - " & 'Issues & risks tracker'[Stream]
```



```dax
Date_Raised_Formatted = FORMAT('Issues & risks tracker'[Date raised],"dd-mm-yyyy")
```



```dax
Mitigation_Date_Formatted = FORMAT('Issues & risks tracker'[Mitigation date],"dd-mm-yyyy")
```


## Table: Stream_Master

### Calculated Columns:


```dax
Workstream_filter = 'Stream_Master'[Stream #] & " - " & 'Stream_Master'[Stream]
```


## Table: Milestone progress- required columns

### Measures:


```dax
milestone_Progress_Curr_Week% = var a = CALCULATE((SUMX('Milestone progress- required columns','Milestone progress- required columns'[Weight] * 'Milestone progress- required columns'[Progress - Curr Week])))
var b = CALCULATE(SUM('Milestone progress- required columns'[Weight]))
return IF(ISBLANK(a/b),0,a/b)
```



```dax
milestone_Progress_Prev_Week% = var a = CALCULATE((SUMX('Milestone progress- required columns','Milestone progress- required columns'[Weight] * 'Milestone progress- required columns'[Progress - Prev Week])))
var b = CALCULATE(SUM('Milestone progress- required columns'[Weight]))
return IF(ISBLANK(a/b),0,a/b)
```


### Calculated Columns:


```dax
matrix-milestone = 'Milestone progress- required columns'[WBS#] & " - " & 'Milestone progress- required columns'[Activity]
```

