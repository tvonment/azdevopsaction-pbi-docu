



# DAX

|Dataset|[public_holidays](./../public_holidays.md)|
| :--- | :--- |
|Workspace|[Public](../../Workspaces/Public.md)|

## Table: pub ll_location_public_holiday

### Measures:


```dax
Weekday = Format(min('pub ll_location_public_holiday'[calendar_date]), "ddd")
```


### Calculated Columns:


```dax
Type = switch('pub ll_location_public_holiday'[hours],
8,"Full",
4,"Half",
FORMAT('pub ll_location_public_holiday'[hours],"standard"))
```



```dax
IsWeekend = 

 if(COUNTROWS(FILTER(ll_location_weekend_days, ll_location_weekend_days[location] = 'pub ll_location_public_holiday'[location_code] && WEEKDAY('pub ll_location_public_holiday'[calendar_date]) = ll_location_weekend_days[Weekday] ))>0 
 , 1
 , 0)
```

