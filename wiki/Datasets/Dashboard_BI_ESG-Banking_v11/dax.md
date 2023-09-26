



# DAX

|Dataset|[Dashboard_BI_ESG-Banking_v11](./../Dashboard_BI_ESG-Banking_v11.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: df_summary_NACE2

### Measures:


```dax
Measure = max(df_summary_NACE1[DarlehenID])
```



```dax
Display = 
SWITCH (
    SELECTEDVALUE ( 'df_summary_NACE2'[sector_Adj]),
    1, [Measure])
```



```dax
Display2 = 
SWITCH (
    SELECTEDVALUE ( 'df_summary_NACE2'[DarlehenID]),
    1, [Measure])
```


## Table: df_summary_NACE2_Timeseries

### Measures:


```dax
Differenz ausgewählter Zeitraum = 
IF (
    ISFILTERED ( df_summary_NACE2_Timeseries[EntwicklungSumme finanzierte Emissionen[tCO2e]]]),
    ERROR ( "Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column." ),
    VAR __PREV_MONTH =
        CALCULATE (
            [Entwicklung],
            DATEADD (
                df_summary_NACE2_Timeseries[Jahr],
                DATEDIFF ( MIN ( df_summary_NACE2_Timeseries[Jahr]), MAX ( df_summary_NACE2_Timeseries[Jahr], YEAR ),YEAR
            )
        )
    RETURN
        DIVIDE ( [Entwicklung] - __PREV_MONTH, __PREV_MONTH )
)
```

