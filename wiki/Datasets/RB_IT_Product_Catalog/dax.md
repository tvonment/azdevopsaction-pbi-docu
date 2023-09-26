



# DAX

|Dataset|[RB_IT_Product_Catalog](./../RB_IT_Product_Catalog.md)|
| :--- | :--- |
|Workspace|[Idea & Demand](../../Workspaces/Idea-&-Demand.md)|

## Table: New Requests

### Measures:


```dax
CountSolution = counta('New Requests'[Title])
```


## Table: Apps&Solutions

### Measures:


```dax
CountAppSolution = COUNT('Apps&Solutions'[Title])
```

