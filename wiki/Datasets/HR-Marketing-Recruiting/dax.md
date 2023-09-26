



# DAX

|Dataset|[HR Marketing Recruiting](./../HR-Marketing-Recruiting.md)|
| :--- | :--- |
|Workspace|[Global Recruiting](../../Workspaces/Global-Recruiting.md)|

## Table: time recording

### Measures:


```dax
n.o. days = 
if(HASONEVALUE(employee[emp_id])
    , DISTINCTCOUNT('time recording'[day_of_work])
    , blank()
)
```

