



# DAX

|Dataset|[ProjectMatrix](./../ProjectMatrix.md)|
| :--- | :--- |
|Workspace|[Public](../../Workspaces/Public.md)|

## Table: rep v_fc_project_data

### Measures:


```dax
Top50Rows = 
VAR t =
    TOPN ( 50, ALLSELECTED ('rep v_fc_project_data'), 'rep v_fc_project_data'[Project],ASC)
RETURN
    COUNTROWS ( INTERSECT ( t, 'rep v_fc_project_data' ) )
```



```dax
FilterIsSet = if(ISFILTERED('rep v_fc_project_data'[Client])||ISFILTERED('rep v_fc_project_data'[Company id])||ISFILTERED('rep v_fc_project_data'[Company])||ISFILTERED('rep v_fc_project_data'[Delivery manager])||ISFILTERED('rep v_fc_project_data'[Platform])||ISFILTERED('rep v_fc_project_data'[Project manager])||ISFILTERED('rep v_fc_project_data'[Project number])||ISFILTERED('rep v_fc_project_data'[Project]),1,0)
```


### Calculated Columns:


```dax
Project number 2 = 'rep v_fc_project_data'[Project number]
```



```dax
Project 2 = 'rep v_fc_project_data'[Project]
```



```dax
Client 2 = 'rep v_fc_project_data'[Client]
```



```dax
Project manager 2 = 'rep v_fc_project_data'[Project manager]
```



```dax
Delivery manager 2 = 'rep v_fc_project_data'[Delivery manager]
```



```dax
Platform 2 = 'rep v_fc_project_data'[Platform]
```



```dax
Company id 2 = 'rep v_fc_project_data'[Company id]
```



```dax
Company 2 = 'rep v_fc_project_data'[Company]
```

