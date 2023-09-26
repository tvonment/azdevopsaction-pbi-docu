



# DAX

|Dataset|[ParPri ProjectMatrix - ImportQ](./../ParPri-ProjectMatrix---ImportQ.md)|
| :--- | :--- |
|Workspace|[Partner_Principal_Project_Matrix](../../Workspaces/Partner_Principal_Project_Matrix.md)|

## Table: ParPriApp

### Measures:


```dax
Project no. 2 = MAX(ParPriApp[project_number])
```



```dax
FilterIsSet = if(ISFILTERED(ParPriApp[project_number]),1,0)
```

