



# DAX

|Dataset|[Projekt_Steckbriefe](./../Projekt_Steckbriefe.md)|
| :--- | :--- |
|Workspace|[EnBW Prio. -Logik](../../Workspaces/EnBW-Prio.--Logik.md)|

## Table: Table19 (2)

### Measures:


```dax
Kennzahl = Not available
```


### Calculated Columns:


```dax
Wirtschaftlichkeitsampel (Container) = IF(
	ISBLANK('Table19 (2)'[Wirtschaftlichkeitsampel]),
	BLANK(),
	INT('Table19 (2)'[Wirtschaftlichkeitsampel])
)
```

