



# DAX

|Dataset|[Portfolio_Dashboard](./../Portfolio_Dashboard.md)|
| :--- | :--- |
|Workspace|[EnBW Prio. -Logik](../../Workspaces/EnBW-Prio.--Logik.md)|

## Table: 1a_Kalk_Liste_Hard_Copy_PBI

### Measures:


```dax
Count Region Mitte = CALCULATE(COUNTROWS('1a_Kalk_Liste_Hard_Copy_PBI'), '1a_Kalk_Liste_Hard_Copy_PBI'[Region] = "M")
```



```dax
Count Region Nord = CALCULATE(COUNTROWS('1a_Kalk_Liste_Hard_Copy_PBI'), '1a_Kalk_Liste_Hard_Copy_PBI'[Region] = "N")
```



```dax
Count Region Ost = CALCULATE(COUNTROWS('1a_Kalk_Liste_Hard_Copy_PBI'), '1a_Kalk_Liste_Hard_Copy_PBI'[Region] = "O")
```



```dax
Count Region Süd = CALCULATE(COUNTROWS('1a_Kalk_Liste_Hard_Copy_PBI'), '1a_Kalk_Liste_Hard_Copy_PBI'[Region] = "S")
```



```dax
Average Plan Abschluss Dynamic = 
VAR SelectedStatus = SELECTEDVALUE('1a_Kalk_Liste_Hard_Copy_PBI'[RG_Ganzzahl])
RETURN
(CALCULATE(
AVERAGE('1a_Kalk_Liste_Hard_Copy_PBI'[Plan Abschluss].[Date]),
'1a_Kalk_Liste_Hard_Copy_PBI',
'1a_Kalk_Liste_Hard_Copy_PBI'[RG_Ganzzahl] = SelectedStatus
) - TODAY()) /365

```



```dax
01_Text_Wirtschaft = "Wirtschaftlichkeit"
```



```dax
01_Text_Planungsrecht = "Planungsrecht"
```



```dax
01_Text_Zeitplan = "Zeitplan"
```

