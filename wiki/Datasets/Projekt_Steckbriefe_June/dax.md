



# DAX

|Dataset|[Projekt_Steckbriefe_June](./../Projekt_Steckbriefe_June.md)|
| :--- | :--- |
|Workspace|[EnBW Prio. -Logik](../../Workspaces/EnBW-Prio.--Logik.md)|

## Table: Steckbrief_Data

### Measures:


```dax
Kennzahl = Not available
```


### Calculated Columns:


```dax
Wirtschaftlichkeitsampel (Container) = IF(
	ISBLANK('Steckbrief_Data'[Wirtschaftlichkeitsampel]),
	BLANK(),
	INT('Steckbrief_Data'[Wirtschaftlichkeitsampel])
)
```
