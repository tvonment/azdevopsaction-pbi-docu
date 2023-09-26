



# DAX

|Dataset|[Dashboard_BI_ESG-Banking_v23 (2)](./../Dashboard_BI_ESG-Banking_v23-(2).md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Emission_zu_Saldo_Total1

### Measures:


```dax
Total_share = SUM(df_credit_portfolio[Financed_Emission_Share])
```


## Table: Emission_zu_Saldo_Total2

### Calculated Columns:


```dax
Bank EN = Emission_zu_Saldo_Total2[Banks]
```


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


## Table: Sample Data incl RB_dim

### Measures:


```dax
id_count = DISTINCTCOUNT('Sample Data incl RB_dim'[id])
```



```dax
IsLanguageFiltered = INT(ISFILTERED('Sample Data incl RB_dim'[language]))
```


### Calculated Columns:


```dax
20words article = IF(
    LEN('Sample Data incl RB_dim'[article]) - LEN(SUBSTITUTE('Sample Data incl RB_dim'[article], " ", "")) >= 19,
    CONCATENATE(LEFT(SUBSTITUTE('Sample Data incl RB_dim'[article], " ", "|", 20), FIND("|", SUBSTITUTE('Sample Data incl RB_dim'[article], " ", "|", 20))-1), "..."),
    'Sample Data incl RB_dim'[article]
)
```


## Table: df_credit_portfolio

### Measures:


```dax
Selected Industry = IF(ISFILTERED(df_credit_portfolio[Bezeichnung]), VALUES(df_credit_portfolio[Bezeichnung]), CONCATENATEX(df_credit_portfolio, df_credit_portfolio[Bezeichnung], ", "))
```



```dax
Top 10 Sectors by Financed_Emission_Share = 
VAR TopCountss = 10
VAR SelectedBezeichnung = SELECTEDVALUE(df_credit_portfolio[Bezeichnung])
RETURN 
IF(
    ISBLANK(SelectedBezeichnung),
    SELECTCOLUMNS(
        TOPN(TopCountss, 
            ADDCOLUMNS(
                SUMMARIZE(df_credit_portfolio, df_credit_portfolio[Bezeichnung], "Financed_Emission_Share", SUM('df_credit_portfolio'[Financed_Emission_Share])),
                "Rank", RANKX(ALL(df_credit_portfolio[Bezeichnung]), [Financed_Emission_Share], , DESC)
            ), 
            [Rank]
        ),
        "Bezeichnung", [Bezeichnung]
    ),
    VALUES(df_credit_portfolio[Bezeichnung])
)
```



```dax
slicer = IF(not ISFILTERED(df_credit_portfolio[Bezeichnung], df_credit_portfolio[Top 10 Sectors by Financed_Emission_Share], ))
```


### Calculated Columns:


```dax
Selected Industry c = IF(ISFILTERED(df_credit_portfolio[Bezeichnung]), VALUES(df_credit_portfolio[Bezeichnung]), CONCATENATEX(df_credit_portfolio, df_credit_portfolio[Bezeichnung], ", "))
```


## Table: Top industries


```dax
GENERATESERIES(5, 10, 1)
```


### Measures:


```dax
Top industries Value = SELECTEDVALUE('Top industries'[Top industries])
```

