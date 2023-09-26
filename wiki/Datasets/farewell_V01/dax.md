



# DAX

|Dataset|[farewell_V01](./../farewell_V01.md)|
| :--- | :--- |
|Workspace|[Farewell](../../Workspaces/Farewell.md)|

## Table: _measures

### Measures:


```dax
number of responses = 
 COUNTROWS(Source)
```



```dax
MinNumberThreshold = 3
```



```dax
IsVisibleDueToThreshold = 
if(calculate(COUNTROWS(Source), ALLSELECTED(Source)) >= [MinNumberThreshold],  COUNTROWS(Source), BLANK())
```



```dax
max 100 = 100 
```



```dax
min -100 = -100
```



```dax
mid 0 = 0
```


## Table: Recommend as employer

### Measures:


```dax
Promoters (employer) = Calculate(COUNTROWS('Recommend as employer'), 'Recommend as employer'[Type] = "Promoters")
```



```dax
Detractors (employer) = Calculate(COUNTROWS('Recommend as employer'), 'Recommend as employer'[Type] = "Detractors")
```



```dax
Passives (employer) = Calculate(COUNTROWS('Recommend as employer'), 'Recommend as employer'[Type] = "Passives")
```



```dax
NPS (employer) = 

if([IsVisibleDueToThreshold] >0
,
var _total = [Promoters (employer)] + [Passives (employer)] + [Detractors (employer)]
var _pro = [Promoters (employer)]
var _det = [Detractors (employer)]

return  (divide(_pro, _total , blank()) - divide(_det, _total , blank()) ) * 100
)
```


## Table: Recommend as client

### Measures:


```dax
Passives (client) = Calculate(COUNTROWS('Recommend as client'), 'Recommend as client'[Type] = "Passives")
```



```dax
Detractors (client) = Calculate(COUNTROWS('Recommend as client'), 'Recommend as client'[Type] = "Detractors")
```



```dax
Promoters (client) = Calculate(COUNTROWS('Recommend as client'), 'Recommend as client'[Type] = "Promoters")
```



```dax
NPS (client) = 

if([IsVisibleDueToThreshold] >0
,
var _total = [Promoters (client)] + [Passives (client)] + [Detractors (client)]
var _pro = [Promoters (client)]
var _det = [Detractors (client)]

return (divide(_pro, _total , blank()) - divide(_det, _total , blank())) * 100 
)
```

