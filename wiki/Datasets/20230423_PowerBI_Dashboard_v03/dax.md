



# DAX

|Dataset|[20230423_PowerBI_Dashboard_v03](./../20230423_PowerBI_Dashboard_v03.md)|
| :--- | :--- |
|Workspace|[MAN \| Fixkostenreduktion](../../Workspaces/MAN-\|-Fixkostenreduktion.md)|

## Table: DetailedAnalysis_cobra_20230425_2

### Measures:


```dax
Kosten_Umsatz = DIVIDE(DetailedAnalysis_cobra_20230425_2[VALUE_EUR_2], DetailedAnalysis_cobra_20230425_2[VALUE_UMSATZ])
```

