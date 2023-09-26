



# DAX

|Dataset|[Absence Dashboard RLS](./../Absence-Dashboard-RLS.md)|
| :--- | :--- |
|Workspace|[Mentor [Prod]](../../Workspaces/Mentor-[Prod].md)|

## Table: dim_employee

### Calculated Columns:


```dax
mentor_email = LOOKUPVALUE(dim_employee[email],dim_employee[emp_id],dim_employee[mentor_emp_id])
```



```dax
pa_email = LOOKUPVALUE(dim_employee[email],dim_employee[emp_id],dim_employee[pa_emp_id])
```



```dax
mentor_pa_email = LOOKUPVALUE(dim_employee[email],dim_employee[emp_id],LOOKUPVALUE(dim_employee[pa_emp_id],dim_employee[emp_id],dim_employee[mentor_emp_id]))
```


## Table: fact_employee_target_absence_training

### Measures:


```dax
timetype = CALCULATE( MIN(fact_employee_target_absence_training[Time_type]))
```


### Calculated Columns:


```dax
Time_type = CONCATENATE(if(fact_employee_target_absence_training[vacation_hours]>0,"V", if(fact_employee_target_absence_training[illness_hours]>0, "S", if(fact_employee_target_absence_training[leave_hours]>0, "L", if(fact_employee_target_absence_training[vacation_hours_in_approval]>0,"IA", if(fact_employee_target_absence_training[is_not_public_holiday]=0, "P",if(fact_employee_target_absence_training[is_not_weekend]=0, "W", "-")))))),if(fact_employee_target_absence_training[absence_hours]=0 , "", if (fact_employee_target_absence_training[absence_hours]>=fact_employee_target_absence_training[target_hours],"F","P")))
```



```dax
vacation_day = IFERROR(
  
   IF(fact_employee_target_absence_training[vacation_hours] >0 , fact_employee_target_absence_training[vacation_hours]/fact_employee_target_absence_training[target_hours],0), 1)
```



```dax
illness_day = IFERROR(
  
   IF(fact_employee_target_absence_training[illness_hours] >0 , fact_employee_target_absence_training[illness_hours]/fact_employee_target_absence_training[target_hours],0), 1)
```



```dax
leave_day = IFERROR(
  
   IF(fact_employee_target_absence_training[leave_hours] >0 , fact_employee_target_absence_training[leave_hours]/fact_employee_target_absence_training[target_hours],0), 1)
```



```dax
vacation_in_approval_day = IFERROR(
  
   IF(fact_employee_target_absence_training[vacation_hours_in_approval] >0 , fact_employee_target_absence_training[vacation_hours_in_approval]/fact_employee_target_absence_training[target_hours],0), 1)
```


## Table: fact_employee_time_blanace

### Measures:


```dax
Entitlement this year = TOTALYTD(sum(fact_employee_time_blanace[time_account_posting]),fact_employee_time_blanace[bookable_from],FILTER(fact_employee_time_blanace,fact_employee_time_blanace[posting_type_id]="3"||fact_employee_time_blanace[posting_type_id]="4"))
```



```dax
Carry Forward last year = TOTALYTD(sum(fact_employee_time_blanace[time_account_posting]),fact_employee_time_blanace[bookable_from],FILTER(fact_employee_time_blanace,fact_employee_time_blanace[posting_type_id]="7"))
```



```dax
Vacation planned this year = TOTALYTD(sum(fact_employee_time_blanace[time_account_posting]),fact_employee_time_blanace[bookable_from],FILTER(fact_employee_time_blanace,fact_employee_time_blanace[posting_type_id]="2"&&fact_employee_time_blanace[posting_date]>TODAY()))
```



```dax
Vacation taken ytd = TOTALYTD(sum(fact_employee_time_blanace[time_account_posting]),fact_employee_time_blanace[bookable_from],FILTER(fact_employee_time_blanace,fact_employee_time_blanace[posting_type_id]="2" && fact_employee_time_blanace[posting_date]<=TODAY()))
```



```dax
Balance this year = CALCULATE([Entitlement this year]+[Carry Forward last year]+[Vacation planned this year]+[Vacation taken ytd])
```


## Table: MeasureTable

### Measures:


```dax
cellcolor = CALCULATE(MIN(ll_report_color[TextColor]))
```



```dax
Vacation_total = sum(fact_employee_target_absence_training[vacation_day])
```



```dax
Illness_total = SUM(fact_employee_target_absence_training[illness_day])
```



```dax
leave_total = SUM(fact_employee_target_absence_training[leave_day])
```



```dax
Vacation in approval this year = TOTALYTD(sum(fact_employee_target_absence_training[vacation_in_approval_day]), fact_employee_target_absence_training[calendar_day] )
```

