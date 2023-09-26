



# DAX

|Dataset|[DevOps-Power BI Demo Report x](./../DevOps-Power-BI-Demo-Report-x.md)|
| :--- | :--- |
|Workspace|[Power BI Report Documentation Test Workspace PremiumPB](../../Workspaces/Power-BI-Report-Documentation-Test-Workspace-PremiumPB.md)|

## Table: Geo

### Calculated Columns:


```dax
Berechnete Spalte in DAX = 1
```


## Table: Kalender als DAX Tabelle


```dax

ADDCOLUMNS (
CALENDAR (DATE(2018,1,1), DATE(2022,12,31)),
"DateAsInteger", FORMAT ( [Date], "YYYYMMDD" ),
"Year", YEAR ( [Date] ),
"Monthnumber", FORMAT ( [Date], "MM" ),
"YearMonthnumber", FORMAT ( [Date], "YYYY/MM" ),
"YearMonthShort", FORMAT ( [Date], "YYYY/mmm" ),
"MonthNameShort", FORMAT ( [Date], "mmm" ),
"MonthNameLong", FORMAT ( [Date], "mmmm" ),
"DayOfWeek", FORMAT ( [Date], "dddd" ),
"DayOfWeekShort", FORMAT ( [Date], "ddd" ),
"Quarter", "Q" & FORMAT ( [Date], "Q" ),
"YearQuarter", FORMAT ( [Date], "YYYY" ) & "/Q" & FORMAT ( [Date], "Q" ),
"YearWeekNum", FORMAT ( [Date], "YYYY" ) & "/" & FORMAT (WEEKNUM( [Date] ), "00" ),
"WeekNum", WEEKNUM( [Date] ) )

```

