



# DAX

|Dataset|[SAMI_AAI_Dashboard](./../SAMI_AAI_Dashboard.md)|
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



```dax
show_in_gantt_chart = var is_filtered =IF(ISFILTERED(Stream_Master[Workstream_filter]),1,0)
var selected_stream = IF(is_filtered=1,SELECTEDVALUE(Stream_Master[Stream #]),0)
var show_if_filtered = IF(is_filtered=1 && VALUE(SELECTEDVALUE('Master progress'[Stream #])) = selected_stream,1,-1)
return if(is_filtered=1,show_if_filtered,0)
```


### Calculated Columns:


```dax
Due_Date_Formatted = FORMAT('Master progress'[Due date].[Date],"dd-mm-yyyy")
```



```dax
Workstream_filter = 'Master progress'[Stream #] & " - " & 'Master progress'[Stream]
```



```dax
Milestone-matrix = 'Master progress'[Milestone #] & " - " & 'Master progress'[Milestone]
```



```dax
Action_display = --'Master progress'[Stream #] &"." & FORMAT(VALUE(IF(ISERROR(VALUE('Master progress'[Milestone #])),UNICODE('Master progress'[Milestone #]),'Master progress'[Milestone #])),"00") & "." & 
FORMAT(VALUE(IF(ISERROR(VALUE('Master progress'[Action #])),UNICODE('Master progress'[Action #]),'Master progress'[Action #])),"00") &" - " & 'Master progress'[Action]
```



```dax
Stream_Milestone_Display = FORMAT('Master progress'[Stream #],"00") & "." & FORMAT(VALUE(IF(ISERROR(VALUE('Master progress'[Milestone #])),UNICODE('Master progress'[Milestone #]),'Master progress'[Milestone #])),"00") & " " &'Master progress'[Stream] & " - " & 'Master progress'[Milestone]
```



```dax
Action_UID_Formatted = FORMAT('Master progress'[Stream #],"00") &"." & FORMAT(VALUE(IF(ISERROR(VALUE('Master progress'[Milestone #])),UNICODE('Master progress'[Milestone #]),'Master progress'[Milestone #])),"00") & "." & FORMAT(VALUE(IF(ISERROR(VALUE('Master progress'[Action #])),UNICODE('Master progress'[Action #]),'Master progress'[Action #])),"00")
```



```dax
Stream_Milestone_Action_Display = 'Master progress'[Stream #] & "." & 'Master progress'[Milestone #]& " " &'Master progress'[Stream] & " - " & 'Master progress'[Milestone] & " - " & 'Master progress'[Action #] & " - " & 'Master progress'[Action]
```



```dax
gantt_Sort_order = FORMAT('Master progress'[Stream #],"00") & "." & FORMAT(VALUE(IF(ISERROR(VALUE('Master progress'[Milestone #])),UNICODE('Master progress'[Milestone #]),'Master progress'[Milestone #])),"00") & "." & FORMAT(VALUE(IF(ISERROR(VALUE('Master progress'[Action #])),UNICODE('Master progress'[Action #]),'Master progress'[Action #])),"00")
```


## Table: Issues & risks tracker

### Measures:


```dax
Issue_Count = var a = CALCULATE(COUNT('Issues & risks tracker'[Issue or risks #]), 'Issues & risks tracker'[Flag (1-issue, 2-risk)] =1)
return IF(ISBLANK(a),0,a)
```



```dax
RiskCount = var a = CALCULATE(COUNT('Issues & risks tracker'[Issue or risks #]), 'Issues & risks tracker'[Flag (1-issue, 2-risk)] =2)
return IF(ISBLANK(a),0,a)
```



```dax
Issue_and_Risk_Count = var a = COUNT('Issues & risks tracker'[Issue or risks #])
return IF(ISBLANK(a),0,a)
```


### Calculated Columns:


```dax
Workstream_filter = 'Issues & risks tracker'[Stream #] & " - " & 'Issues & risks tracker'[Stream]
```


## Table: Stream_Master

### Calculated Columns:


```dax
Workstream_filter = FORMAT('Stream_Master'[Stream #],"00") & " - " & 'Stream_Master'[Stream]
```

