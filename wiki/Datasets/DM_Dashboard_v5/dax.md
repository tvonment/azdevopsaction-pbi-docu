



# DAX

|Dataset|[DM_Dashboard_v5](./../DM_Dashboard_v5.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Segment_RFM

### Measures:


```dax
AVG_PCT = 
CALCULATE(
    DIVIDE(
        SUMX(Segment_RFM,'Segment_RFM'[ABS]),
        CALCULATE(SUM([ABS]),REMOVEFILTERS()),
        1
    ),
    ALLEXCEPT(Segment_RFM,Segment_RFM[RFM Sektor]))*100
```

