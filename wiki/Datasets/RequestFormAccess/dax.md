



# DAX

|Dataset|[RequestFormAccess](./../RequestFormAccess.md)|
| :--- | :--- |
|Workspace|[Central Graphics](../../Workspaces/Central-Graphics.md)|

## Table: Logging

### Measures:


```dax
# AppStarts = COUNTROWS(Logging) 
```



```dax
# distinct user = DISTINCTCOUNT(Logging[AppUser]) 
```



```dax
# cumulative distinct app user = 
 var currentDate = max(Logging[Date])
 var minDate = calculate(min(Logging[Date]),  ALLSELECTED(Logging[Date]))
 return calculate( COUNTROWS(values(Logging[AppUser])  ), ALLSELECTED(Logging[Date]), Logging[Date]<= currentDate && Logging[Date]>= minDate )
```



```dax
# new app user = 
 var currentDate = max(Logging[Date])
 var minDate = calculate(min(Logging[Date]),  ALLSELECTED(Logging[Date]))

 var checkUser = calculatetable( values(Logging[AppUser]  ), ALLSELECTED(Logging[Date]), Logging[Date]= currentDate )
 var checkNew = ADDCOLUMNS(checkUser, "NumberBefore",
    var curUser = SELECTEDVALUE(Logging[AppUser])
    return CALCULATE(COUNTROWS(Logging), Logging[Date] < currentDate &&  Logging[Date] >= minDate)
 )

 return Countrows(Filter(checkNew, [NumberBefore] =0))
```



```dax
# Errors = CALCULATE(COUNTROWS(Logging), Logging[Title] = "AppError")  /4
```



```dax
# loaded = CALCULATE(COUNTROWS(Logging), Logging[Title] = "Contacts loaded") 
```



```dax
# saves = 
 var currentDate = max(Logging[Date])
 var minDate = calculate(min(Logging[Date]),  ALLSELECTED(Logging[Date]))

return calculate (COUNTROWS(Logging), Logging[Title] = "saved")
```



```dax
# cumulative saved = 
var currentDate = max(Logging[Date])
var minDate = calculate(min(Logging[Date]),  ALLSELECTED(Logging[Date]))
return calculate( COUNTROWS(values(Logging[ID])  ), ALLSELECTED(Logging[Date]), Logging[Date]<= currentDate && Logging[Date]>= minDate, Logging[Title]="saved" ) 
```


### Calculated Columns:


```dax
Date = Date(year(Logging[Modified]),Month(Logging[Modified]),day(Logging[Modified])) 
```



```dax
Hour = Hour(Logging[Modified]) 
```



```dax
TenMinuteInterval = Rounddown( MINUTE(Logging[Modified]) / 10, 0)  * 10
```

