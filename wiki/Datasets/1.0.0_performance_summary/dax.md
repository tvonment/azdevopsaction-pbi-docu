



# DAX

|Dataset|[1.0.0_performance_summary](./../1.0.0_performance_summary.md)|
| :--- | :--- |
|Workspace|[MSR Navigation](../../Workspaces/MSR-Navigation.md)|

## Table: msr v_employee_utilization

### Measures:


```dax
Utilization_target_hours = SUM('msr v_employee_utilization'[target_hours_adj])
```



```dax
Utilization_hours_on_client_project = SUM('msr v_employee_utilization'[productive_hours])
```



```dax
Utilization_absolute = [Utilization_hours_on_client_project] / 'msr v_employee_utilization'[Utilization_target_hours]
```



```dax
Utilization % = 
DIVIDE(
	[Utilization_hours_on_client_project],
	[Utilization_target_hours]
)
```



```dax
Utilization Target = 0.8
```



```dax
Utilization Performance = 'msr v_employee_utilization'[Utilization %] - 'msr v_employee_utilization'[Utilization Target]
```



```dax
Utilization Performance String = "(" & 'msr v_employee_utilization'[Utilization Performance Short] & "ppt.)"
```



```dax
Utilization Performance Short = FIXED('msr v_employee_utilization'[Utilization Performance] * 100, 0)
```



```dax
Utilization Target String = "Target: " & 'msr v_employee_utilization'[Utilization Target] * 100 & "%"
```



```dax
Utilization Target & Performance = [Utilization Target String] & " " & [Utilization Performance String]
```

