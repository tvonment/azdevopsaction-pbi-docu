



# DAX

|Dataset|[RB_IT_Product_Catalog_nodata](./../RB_IT_Product_Catalog_nodata.md)|
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

