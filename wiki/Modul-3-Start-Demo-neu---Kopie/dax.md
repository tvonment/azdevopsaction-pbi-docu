



# DAX

## Table: Geo

### Calculated Columns:


```dax
Key = Geo[Land] & "," & Geo[PLZ]
```

```dax
Land (Gruppen) = SWITCH(
  TRUE,
  ISBLANK('Geo'[Land]),
  "(Leer)",
  'Geo'[Land] IN {"Germany",
    "France"},
  "EU",
  'Geo'[Land] IN {"Mexico"},
  "Mittelamerika",
  'Geo'[Land] IN {"Canada",
    "USA"},
  "Nordamerika",
  "Sonstige"
)
```

```dax
Location = IF(Geo[Land] = "Mexico", "Inland", "Ausland")
```
## Table: Sales

### Measures:


```dax
Total Sales = SUM(Sales[Umsatz])
```
### Calculated Columns:


```dax
Key = Sales[Ländername] &","& Sales[PLZ]
```

```dax
Stückpreis DAX = Sales[Umsatz]/Sales[Menge]
```