



# DAX

|Dataset|[test - Kopie](./../test---Kopie.md)|
| :--- | :--- |
|Workspace|[Power BI Report Documentation Test Workspace PremiumPB](../../Workspaces/Power-BI-Report-Documentation-Test-Workspace-PremiumPB.md)|

## Table: Geo

### Calculated Columns:


```dax
Key = Geo[Country]&","&Geo[Postalcode]
```


## Table: Sales

### Measures:


```dax
Total Units = SUM(Sales[Amount])



```


### Calculated Columns:


```dax
Key = Sales[Country name]&","&Sales[Postalcode]
```

