



# DAX

|Dataset|[09_Projekt_Steckbriefe_September_v3](./../09_Projekt_Steckbriefe_September_v3.md)|
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

