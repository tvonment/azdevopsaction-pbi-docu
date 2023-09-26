



# DAX

|Dataset|[20210512 RB Kundensegmentierung dmAT Dashboard](./../20210512-RB-Kundensegmentierung-dmAT-Dashboard.md)|
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

