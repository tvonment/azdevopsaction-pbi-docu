



# DAX

|Dataset|[20230529_Sawaher Dashbaord_v10.2](./../20230529_Sawaher-Dashbaord_v10.2.md)|
| :--- | :--- |
|Workspace|[Sawaher-Test](../../Workspaces/Sawaher-Test.md)|

## Table: Project

### Calculated Columns:


```dax
Project Name = CONCATENATE(Project[Project #], CONCATENATE(" ", Project[Project]))
```


## Table: Stream

### Calculated Columns:


```dax
Stream Name = CONCATENATE(Stream[Stream #], CONCATENATE(" ", Stream[Stream]))
```


## Table: Task

### Measures:


```dax
TodayDate = TODAY()
```


### Calculated Columns:


```dax
Task Progress Status Legend = 
SWITCH(
    TRUE(),
    Task[Progress Status] = 0, "Not Started",
    AND(Task[Progress Status] >0, Task[Progress Status] <0.75), "Delayed",
    AND(Task[Progress Status]>=0.75, Task[Progress Status]<1), "At Risk",
    "On Track")
```



```dax
Task Name = CONCATENATE(Task[Task #] , CONCATENATE(" ", Task[Task]))
```


## Table: Milestone

### Measures:


```dax
No. of Complete Milestones = 
CALCULATE(
	COUNTA('Milestone'[Milestone Name]),
	'Milestone'[Milestone Status] IN { "Complete" }
)
```



```dax
No. of Milestone Target = 
CALCULATE(
	COUNTA('Milestone'[Milestone Name]),
	'Milestone'[Milestone Status] IN { "Overdue" }
) + 
[No. of Complete Milestones]
```



```dax
Milestone Progress Status = [No. of Complete Milestones]/[No. of Milestone Target]
```


### Calculated Columns:


```dax
Milestone Name = CONCATENATE(Milestone[Milestone #], CONCATENATE(" ", Milestone[Milestone]))
```



```dax
show_in_gantt_chart = var diff = DATEDIFF(Milestone[Due Date],Task[TodayDate],DAY)
return  if (diff<90 && diff >-30, 1, 0)
```

