



# DAX

|Dataset|[Agile Cloud Migration](./../Agile-Cloud-Migration.md)|
| :--- | :--- |
|Workspace|[IT_Agile_Cloud_Migration](../../Workspaces/IT_Agile_Cloud_Migration.md)|

## Table: All epics

### Measures:


```dax
Link = "https://dev.azure.com/RolandBerger-IT/Agile%20cloud%20migration/_workitems/edit/" & SELECTEDVALUE('All epics'[Work Item Id])
```


## Table: All user stories

### Measures:


```dax
Compl. = IF(ISNUMBER(DIVIDE(calculate(count('All user stories'[Work Item Id]),'All user stories'[State]="Closed"), COUNT('All user stories'[Work Item Id]))),DIVIDE(calculate(count('All user stories'[Work Item Id]),'All user stories'[State]="Closed"), COUNT('All user stories'[Work Item Id])),0)
```

