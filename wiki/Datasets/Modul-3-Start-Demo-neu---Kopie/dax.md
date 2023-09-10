



# DAX

|Dataset|[Modul 3 Start Demo neu - Kopie](./../Modul-3-Start-Demo-neu---Kopie.md)|
| :--- | :--- |
|Workspace|[Power BI Report Documentation Test Workspace PremiumPB](../../Workspaces/Power-BI-Report-Documentation-Test-Workspace-PremiumPB.md)|

## Table: Geo

### Calculated Columns:


```dax
Key = Geo[Land] & "," & Geo[PLZ]
```

OpenAI is not configured

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

OpenAI is not configured

```dax
Location = IF(Geo[Land] = "Mexico", "Inland", "Ausland")
```

OpenAI is not configured
## Table: Sales

### Measures:


```dax
Total Sales = SUM(Sales[Umsatz])
```

OpenAI is not configured
### Calculated Columns:


```dax
Key = Sales[Ländername] &","& Sales[PLZ]
```

OpenAI is not configured

```dax
Stückpreis DAX = Sales[Umsatz]/Sales[Menge]
```

OpenAI is not configured