



# DAX

|Dataset|[2023-07-01 NFR Forecast - Dashboard](./../2023-07-01-NFR-Forecast---Dashboard.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: PREP_NFR_Projection_All

### Measures:


```dax
Sales after Discount = SUM(Sales[SalesAmount]) - (SUM(Sales[SalesAmount]) * 'Discount percentage' [Discount percentage Value])
```


## Table: SRC_Budget

### Measures:


```dax
NFR Budget plus NFR Budget = 
SUM('SRC_Budget'[NFR Budget]) + SUM('SRC_Budget'[NFR Budget])
```


## Table: PREP_NFR_Target_Aggregated

### Measures:


```dax
Sum of NFR Projection = 
VAR SelectedParameter = SELECTEDVALUE(PARAM_Slicer[Parameter])
RETURN
    IF(
        SelectedParameter < MIN('PREP_NFR_Target_Aggregated'[SRC_Actuals.Month]),
        MAXX(
            FILTER('PREP_NFR_Target_Aggregated', 'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] > SelectedParameter),
            'PREP_NFR_Target_Aggregated'[PREP_NFR.NFR Projection]
        ),
        BLANK()
    )
```



```dax
Sum of NFR Actuals = 
VAR SelectedParameter = SELECTEDVALUE(PARAM_Slicer[Parameter])
RETURN
    IF(
        SelectedParameter >= MIN('PREP_NFR_Target_Aggregated'[SRC_Actuals.Month]),
        MAXX(
            FILTER('PREP_NFR_Target_Aggregated', 'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] <= SelectedParameter),
            'PREP_NFR_Target_Aggregated'[SRC_NFR_Actuals.NFR Actuals]
        ),
        BLANK()
    )
```



```dax
Cumulative NFR Budget = CALCULATE(SUM('PREP_NFR_Target_Aggregated'[NFR Budget]), FILTER(ALL('PREP_NFR_Target_Aggregated'), 'PREP_NFR_Target_Aggregated'[Year-Month] <= MAX('PREP_NFR_Target_Aggregated'[Year-Month])))
```



```dax
Cumulative NFR Actuals 1 = 
VAR SelectedValue = SELECTEDVALUE(PARAM_Slicer[Parameter])
VAR CumulativeValues =
    ADDCOLUMNS(
        FILTER(
            'PREP_NFR_Target_Aggregated',
           'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] <= SelectedValue
        ),
        "Cumulative",
            CALCULATE(
                SUM('PREP_NFR_Target_Aggregated'[SRC_NFR_Actuals.NFR Actuals]),
                FILTER(
                    ALL('PREP_NFR_Target_Aggregated'),
                   'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] <= EARLIER('PREP_NFR_Target_Aggregated'[SRC_Actuals.Month])
                )
            )
    )
RETURN
    MAXX(CumulativeValues, [Cumulative])

```



```dax
Cumulative NFR Projection = 
VAR SelectedValue = SELECTEDVALUE(PARAM_Slicer[Parameter])
VAR CumulativeValues =
    ADDCOLUMNS(
        FILTER(
            'PREP_NFR_Target_Aggregated',
            'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] >= SelectedValue
        ),
        "Cumulative",
            CALCULATE(
                SUM('PREP_NFR_Target_Aggregated'[PREP_NFR.NFR Projection]),
                FILTER(
                    ALL('PREP_NFR_Target_Aggregated'),
                    'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] <= EARLIER('PREP_NFR_Target_Aggregated'[SRC_Actuals.Month]) && 'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] > SelectedValue
                )
            )
    )
RETURN
    SUMX(
        CumulativeValues,
        IF('PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] = SelectedValue, 0, [Cumulative])
    )

```



```dax
Cumulative NFR Actuals 2 = 
VAR SelectedValue = SELECTEDVALUE(PARAM_Slicer[Parameter])
VAR CumulativeValues =
    ADDCOLUMNS(
        FILTER(
            ALL('PREP_NFR_Target_Aggregated'[SRC_Actuals.Month]),
            'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] <= SelectedValue
        ),
        "Cumulative",
            CALCULATE(
                SUM('PREP_NFR_Target_Aggregated'[SRC_NFR_Actuals.NFR Actuals]),
                FILTER(
                    ALL('PREP_NFR_Target_Aggregated'),
                   'PREP_NFR_Target_Aggregated'[SRC_Actuals.Month] <= EARLIER('PREP_NFR_Target_Aggregated'[SRC_Actuals.Month])
                )
            )
    )
VAR LastValue = 
    MAXX(
        CumulativeValues,
        [Cumulative]
    )
RETURN
    LastValue


```



```dax
Cumulative NFR Actuals = 
VAR Measure1 = 'PREP_NFR_Target_Aggregated'[Cumulative NFR Actuals 1]
VAR Measure2 = 'PREP_NFR_Target_Aggregated'[Cumulative NFR Actuals 2]
VAR CombinedValues =
    UNION(
        ROW("Value", 'PREP_NFR_Target_Aggregated'[Cumulative NFR Actuals 1]),
        ROW("Value", 'PREP_NFR_Target_Aggregated'[Cumulative NFR Actuals 2])
    )
VAR Result =
    MINX(
        CombinedValues,
        [Value]
    )
RETURN
    Result
```



```dax
Cumulative NFR Actuals & Projection = 
'PREP_NFR_Target_Aggregated'[Cumulative NFR Actuals] + 'PREP_NFR_Target_Aggregated'[Cumulative NFR Projection]
```


## Table: PARAM_Slicer


```dax
GENERATESERIES(1, 12, 1)
```


### Measures:


```dax
Parameter Value = SELECTEDVALUE('PARAM_Slicer'[Parameter])
```

