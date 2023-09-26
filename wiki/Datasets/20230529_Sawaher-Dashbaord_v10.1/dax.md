



# DAX

|Dataset|[20230529_Sawaher Dashbaord_v10.1](./../20230529_Sawaher-Dashbaord_v10.1.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

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

### Calculated Columns:


```dax
Progress Status Legend = 
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

