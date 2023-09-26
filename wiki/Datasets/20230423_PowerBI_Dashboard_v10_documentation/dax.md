



# DAX

|Dataset|[20230423_PowerBI_Dashboard_v10_documentation](./../20230423_PowerBI_Dashboard_v10_documentation.md)|
| :--- | :--- |
|Workspace|[MAN \| Fixkostenreduktion](../../Workspaces/MAN-\|-Fixkostenreduktion.md)|

## Table: DetailedAnalysis_cobra_20230426

### Measures:


```dax
VALUE_EUR_2 divided by MA_GESAMT_LEIHARBEITER = 
DIVIDE(
	SUM('DetailedAnalysis_cobra_20230426'[VALUE_EUR_2]),
	AVERAGE('DetailedAnalysis_cobra_20230426'[MA_GESAMT_LEIHARBEITER])
)
```



```dax
VALUE_EUR_2 divided by VALUE_UMSATZ = 
DIVIDE(
	SUM('DetailedAnalysis_cobra_20230426'[VALUE_EUR_2]),
	AVERAGE('DetailedAnalysis_cobra_20230426'[VALUE_UMSATZ])
)
```



```dax
ma_share = 
DIVIDE(
	SUM('DetailedAnalysis_cobra_20230426'[VALUE_EUR_2]),
	AVERAGE('DetailedAnalysis_cobra_20230426'[MA_GESAMT_LEIHARBEITER])
)
```
