



# DAX

|Dataset|[LeaveReport](./../LeaveReport.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_employee_toe_history

### Measures:


```dax
InDateRange = 
var _rangeStart=FIRSTDATE('pub dim_date'[Date])
var _rangeEnd=LASTDATE('pub dim_date'[Date])
return 
if(
    (SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_from])>=_rangeStart
    &&
    SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_from])<_rangeEnd)
    ||
    (SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to])>_rangeStart
    &&
    SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to])<=_rangeEnd)
    ,
1,0)
```


### Calculated Columns:


```dax
age_at_valid_to = ROUNDDOWN(YEARFRAC('rep v_hr_employee_toe_history'[birthdate],'rep v_hr_employee_toe_history'[valid_to_end],1),0)
```



```dax
valid_to_end = if('rep v_hr_employee_toe_history'[valid_to] = Date(9999,12,31),TODAY(),'rep v_hr_employee_toe_history'[valid_to])
```



```dax
age_cluster = if('rep v_hr_employee_toe_history'[age_at_valid_to] < 30, "<30",if('rep v_hr_employee_toe_history'[age_at_valid_to] >= 30 && 'rep v_hr_employee_toe_history'[age_at_valid_to] <= 35, "30-35",if('rep v_hr_employee_toe_history'[age_at_valid_to] >= 36 && 'rep v_hr_employee_toe_history'[age_at_valid_to] <= 40, "36-40",if('rep v_hr_employee_toe_history'[age_at_valid_to] >= 41 && 'rep v_hr_employee_toe_history'[age_at_valid_to] <= 45, "41-45",if('rep v_hr_employee_toe_history'[age_at_valid_to] >= 46 && 'rep v_hr_employee_toe_history'[age_at_valid_to] <= 50, "46-50",">50")))))
```


## Table: pub dim_date

### Measures:


```dax
MinDate = Min('pub dim_date'[YearMonthnumber])
```



```dax
MaxDate = Max('pub dim_date'[YearMonthnumber])
```


## Table: rep v_hr_employee_job_history

### Measures:


```dax
IsActive_job = 
IF(SELECTEDVALUE('rep v_hr_employee_job_history'[valid_from]) <=SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to]) && SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to])<=SELECTEDVALUE('rep v_hr_employee_job_history'[valid_to]),1,0)
```


## Table: rep v_hr_employee_platform1_history

### Measures:


```dax
IsActive_platform1 = 
IF(SELECTEDVALUE('rep v_hr_employee_platform1_history'[valid_from]) <=SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to]) && SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to])<=SELECTEDVALUE('rep v_hr_employee_platform1_history'[valid_to]),1,0)
```


## Table: rep v_hr_employee_office_history

### Measures:


```dax
IsActive_office = 
IF(SELECTEDVALUE('rep v_hr_employee_office_history'[valid_from]) <=SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to]) && SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to])<=SELECTEDVALUE('rep v_hr_employee_office_history'[valid_to]),1,0)
```


## Table: rep v_hr_employee_costcenterassignment_history

### Measures:


```dax
IsActive_ccostcenter = 
IF(SELECTEDVALUE('rep v_hr_employee_costcenterassignment_history'[valid_from]) <=SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to]) && SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to])<=SELECTEDVALUE('rep v_hr_employee_costcenterassignment_history'[valid_to]),1,0)
```


## Table: rep v_hr_employee_companyassignment_history

### Measures:


```dax
IsActive_comp = 
IF(SELECTEDVALUE('rep v_hr_employee_companyassignment_history'[valid_from]) <=SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to]) && SELECTEDVALUE('rep v_hr_employee_toe_history'[valid_to])<=SELECTEDVALUE('rep v_hr_employee_companyassignment_history'[valid_to]),1,0)
```

