



# DAX

|Dataset|[test - Kopie](./../test---Kopie.md)|
| :--- | :--- |
|Workspace|[Power BI Report Documentation Test Workspace PremiumPB](../../Workspaces/Power-BI-Report-Documentation-Test-Workspace-PremiumPB.md)|

## Table: Geo

### Calculated Columns:


```dax
Key = Geo[Country]&","&Geo[Postalcode]
```

OpenAI is not configured
## Table: Sales

### Measures:


```dax
Total Units = SUM(Sales[Amount])



```

OpenAI is not configured
### Calculated Columns:


```dax
Key = Sales[Country name]&","&Sales[Postalcode]
```

OpenAI is not configured