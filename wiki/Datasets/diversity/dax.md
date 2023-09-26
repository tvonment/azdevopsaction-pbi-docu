



# DAX

|Dataset|[diversity](./../diversity.md)|
| :--- | :--- |
|Workspace|[HR Head](../../Workspaces/HR-Head.md)|

## Table: fact hr statistics

### Measures:


```dax
# female = sum('fact hr statistics'[FemaleCount])
```



```dax
# male = sum('fact hr statistics'[MaleCount])
```



```dax
# total = [# female] + [# male]
```



```dax
% female = divide([# female], [# total] )
```



```dax
% male = divide([# male], [# total] )
```



```dax
# active f = calculate( COUNTROWS('fact hr statistics'), 'fact hr statistics'[sex] = "F")
```



```dax
# active m = calculate( COUNTROWS('fact hr statistics'), 'fact hr statistics'[sex] = "M")
```



```dax
# total active = [# active f] + [# active m]
```


## Table: fact entry exit

### Measures:


```dax
# female hires = calculate(sum('fact entry exit'[FemaleCount]),  'fact entry exit'[FemaleCount] > 0 && 'fact entry exit'[action_typeid] = 20 )// 'entry exit'[sex] = "F", 'entry exit'[action] = "HIR" || 'entry exit'[action] = "REH")
```



```dax
# male hires = calculate(sum('fact entry exit'[MaleCount]),  'fact entry exit'[MaleCount] > 0 )
```



```dax
# total hires = [# female hires] + [# male hires]
```



```dax
% female hires = coalesce(DIVIDE([# female hires], [# total hires]) ,0)
```



```dax
# female exits td = 
var _maxDate = [MaxDateExcluding] //  min(RefreshInfo[RefreshDate])

return coalesce(calculate(sum('fact entry exit'[FemaleCount]),  'fact entry exit'[FemaleCount] < 0,'fact entry exit'[effective_date] < _maxDate, REMOVEFILTERS(DimStatisticalRelevant[statistic_relevant])) * -1,0)
```



```dax
# male exits td = 
var _maxDate = [MaxDateExcluding] //min(RefreshInfo[RefreshDate])
return calculate(sum('fact entry exit'[MaleCount]),  'fact entry exit'[MaleCount] < 0, 'fact entry exit'[effective_date] < _maxDate,REMOVEFILTERS(DimStatisticalRelevant[statistic_relevant]) ) * -1
```



```dax
attrition f = divide([# female exits td] ,   [# active f] + [# female exits td])
```



```dax
attrition m = divide([# male exits td] ,   [# active m] + [# male exits td])
```



```dax
% male hires = coalesce(DIVIDE([# male hires], [# total hires]) ,0)
```


## Table: CurrentMonth

### Measures:


```dax
MaxDateExcluding = Date(2021, 8, 1)
```


## Table: DimDate


```dax
CALENDAR(
    if(min('fact entry exit'[effective_date]) < min('fact hr statistics'[validfrom_date]), min('fact entry exit'[effective_date]), min('fact hr statistics'[validfrom_date]))
    , if(max('fact entry exit'[effective_date]) > max('fact hr statistics'[validfrom_date]), max('fact entry exit'[effective_date]), max('fact hr statistics'[validfrom_date])))
```


### Calculated Columns:


```dax
Year = Year(DimDate[Date])
```



```dax
YearOffset = DimDate[Year] -  min(CurrentYear[CurrentYear]) 
```



```dax
Month = month(DimDate[Date])
```



```dax
MonthOffest = -1 * ( ((min(CurrentYear[CurrentYear]) - Year(DimDate[Date]))*12) +  min(CurrentMonth[CurrentMonth]) - Month(DimDate[Date]))
```


## Table: fact utilization by month

### Measures:


```dax
Utilisation rate = 

 divide([util productive hours], [util target hours adj])
```



```dax
util productive hours = sum('fact utilization by month'[productive_hours])
```



```dax
util target hours adj = sum('fact utilization by month'[target_hours_adj])
```


## Table: InvervalHelper


```dax

var cy = min(CurrentYear[CurrentYear])
return {(FORMAT(cy-2, ""), Date(cy-2, 1, 1), "Prev" )
            , (FORMAT(cy-1, ""), Date(cy-1, 1, 1), "Prev" )
         , (FORMAT(cy, "") & "-01", Date( cy,1,1), "Current") 
         , (FORMAT(cy, "") & "-02", Date( cy,2,1), "Current") 
         , (FORMAT(cy, "") & "-03", Date( cy,3,1), "Current") 
         , (FORMAT(cy, "") & "-04", Date( cy,4,1), "Current") 
         , (FORMAT(cy, "") & "-05", Date( cy,5,1), "Current") 
         , (FORMAT(cy, "") & "-06", Date( cy,6,1), "Current") 

         , (FORMAT(cy, "") & "-07", Date( cy,7,1), "Current") 
         , (FORMAT(cy, "") & "-08", Date( cy,8,1), "Current") 
         , (FORMAT(cy, "") & "-09", Date( cy,9,1), "Current") 
         , (FORMAT(cy, "") & "-10", Date( cy,10,1), "Current") 
         , (FORMAT(cy, "") & "-11", Date( cy,11,1), "Current") 
         , (FORMAT(cy, "") & "-12", Date( cy,12,1), "Current") 
         
         } 
```


### Measures:


```dax
% female hires for interval = 



var dateFrom = min(InvervalHelper[From])
var dateTo = max(InvervalHelper[To])

var totalHires = CALCULATE([# total hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo))

return  if(totalHires = 0, "-", CALCULATE([% female hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo)))
//var female = CALCULATE([# female hires], filter( all(DimDate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo))
//var male = CALCULATE([# male hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo))

//return divide (female , female + male, 0)
```



```dax
# female hires for interval = 
var dateFrom = min(InvervalHelper[From])
var dateTo =max(InvervalHelper[To])

return coalesce(CALCULATE([# female hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo)), 0)
```



```dax
# male hires for interval = 
var dateFrom = min(InvervalHelper[From])
var dateTo =max(InvervalHelper[To])

return coalesce(CALCULATE([# male hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo)), 0)
```



```dax
% male hires for interval = 



var dateFrom = min(InvervalHelper[From])
var dateTo = max(InvervalHelper[To])

var totalHires = CALCULATE([# total hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo))

return  if(totalHires = 0, "-", CALCULATE([% male hires], filter( all(dimdate), DimDate[Date] >= dateFrom && DimDate[Date] <= dateTo)))
```


### Calculated Columns:


```dax
To = if(InvervalHelper[YearType] ="Prev", ENDOFYEAR(DimDate[Date]), ENDOFMONTH(DimDate[Date]))
```



```dax
Display = if(year(InvervalHelper[From])< min(CurrentYear[CurrentYear]) || month(InvervalHelper[From]) <= min( CurrentMonth[CurrentMonth]), 1, 0)
```


## Table: project_assessment

### Measures:


```dax
assessment = AVERAGE(project_assessment[average])
```



```dax
Delta = 
 (1 - divide([f assessment] , [m assessment])) * -1
```



```dax
m assessment = CALCULATE(project_assessment[assessment], project_assessment[gender] ="M")
```



```dax
f assessment = CALCULATE(project_assessment[assessment], project_assessment[gender] ="F")
```


## Table: flags

### Measures:


```dax
Selected Country Flag = 
var flagData =if(HASONEVALUE('dim region country'[country_company]),min(flags[flag]), blank())
return COALESCE(flagData, "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
```


## Table: v_rep_data_diverstiy

### Measures:


```dax
# of applications = COUNTROWS(values(v_rep_data_diverstiy[Application ID]))
```



```dax
# values = sum(v_rep_data_diverstiy[Value])
```



```dax
# of applications (0) = COALESCE([# of applications],0) 
```


### Calculated Columns:


```dax
Value = if(RELATED(ll_funnel_status[Funnel_Status]) in {"Reject", "No Success", "No Succes", "Declined Offer"}, -1, 1)
```


## Table: peakon_mapping_country

### Measures:


```dax
Selected Country = SELECTEDVALUE(peakon_mapping_country[short])
```



```dax
Error multiple companies or regions = if(Countrows(Values(peakon_mapping_country[segment_id]))>1, "Please select only one company or region","")
```


## Table: peakon_results

### Measures:


```dax
Participation rate = divide( AVERAGE(peakon_results[participation_rate]) , 100)
```



```dax
Latest  participation rate = CALCULATE([Participation rate],Filter('peakon rounds', [mRank] = 1))
```



```dax
Previous participation rate = CALCULATE([Participation rate],Filter('peakon rounds', [mRank] = 2))
```



```dax
Latest EngScore = CALCULATE(AVERAGE(peakon_results[score]),Filter('peakon rounds', [mRank] = 1))
```



```dax
Latest EngScoreM = CALCULATE(AVERAGE(peakon_results[score_m]),Filter('peakon rounds', [mRank] = 1))
```



```dax
Latest EngScoreF = CALCULATE(AVERAGE(peakon_results[score_f]),Filter('peakon rounds', [mRank] = 1))
```



```dax
Prev EngScore = CALCULATE(AVERAGE(peakon_results[score]),Filter('peakon rounds', [mRank] = 2))
```



```dax
Prev EngScoreM = CALCULATE(AVERAGE(peakon_results[score_m]),Filter('peakon rounds', [mRank] = 2))
```



```dax
Prev EngScoreF = CALCULATE(AVERAGE(peakon_results[score_f]),Filter('peakon rounds', [mRank] = 2))
```



```dax
Latest nps = CALCULATE(AVERAGE(peakon_results[nps]),Filter('peakon rounds', [mRank] = 1))
```



```dax
Latest npsM = CALCULATE(AVERAGE(peakon_results[nps_m]),Filter('peakon rounds', [mRank] = 1))
```



```dax
Latest npsF = CALCULATE(AVERAGE(peakon_results[nps_f]),Filter('peakon rounds', [mRank] = 1))
```



```dax
Prev nps = CALCULATE(AVERAGE(peakon_results[nps]),Filter('peakon rounds', [mRank] = 2))
```



```dax
Prev npsM = CALCULATE(AVERAGE(peakon_results[nps_m]),Filter('peakon rounds', [mRank] = 2))
```



```dax
Prev npsF = CALCULATE(AVERAGE(peakon_results[nps_f]),Filter('peakon rounds', [mRank] = 2))
```


## Table: peakon_results_by_driver

### Measures:


```dax
top 3 driver avg = calculate(AVERAGEX(peakon_results_by_driver, peakon_results_by_driver[score]), TOPN(3,peakon_results_by_driver, AVERAGE(peakon_results_by_driver[score]), Desc))
```



```dax
bottom 3 driver avg = calculate(AVERAGEX(peakon_results_by_driver, peakon_results_by_driver[score]), TOPN(3,peakon_results_by_driver, AVERAGE(peakon_results_by_driver[score]), Asc))
```



```dax
sum d score = sum(peakon_results_by_driver[score])
```



```dax
DriverBottom3Threshold = 
var _date = SELECTEDVALUE(peakon_results_by_driver[closed_at])

VAR t = calculatetable(TOPN( 3, peakon_results_by_driver, [sum d score], ASC)
                        , All (peakon_driver_displayNames),  peakon_results_by_driver[closed_at] = _date)

RETURN  calculate(maxx(t, [sum d score]))
```



```dax
IsBottom3 = 
var _th = [DriverBottom3Threshold]
var _s = [sum d score]
return if(_s <= _th, 1)
```



```dax
DriverTop3Threshold = 
var _date = SELECTEDVALUE(peakon_results_by_driver[closed_at])

VAR t = calculatetable(TOPN( 3, peakon_results_by_driver, [sum d score], Desc)
                        , All (peakon_driver_displayNames),  peakon_results_by_driver[closed_at] = _date)

RETURN  calculate(minx(t, [sum d score]))
```



```dax
IsTop3 = 
var _th = [DriverTop3Threshold]
var _s = [sum d score]
return if(_s >= _th, 1)
```


## Table: peakon rounds


```dax
values(peakon_results[closed_at]) 
```


### Measures:


```dax
Latest Round = max('peakon rounds'[closed_at])
```



```dax
vs rounds = CONCATENATEX('peakon rounds', Format('peakon rounds'[closed_at], "mmmm 'yy"), " vs ")
```



```dax
mRank = 
var _current = min('peakon rounds'[closed_at])

return RANKX(ALLSELECTED( 'peakon rounds'), 'peakon rounds'[closed_at], _current ,DESC)
```



```dax
Latest round txt = Format(max('peakon rounds'[closed_at]), "mmm 'yy")
```



```dax
previous round txt = Format(calculate(max('peakon rounds'[closed_at]), Filter('peakon rounds', [mRank] = 2)), "mmm 'yy")
```


### Calculated Columns:


```dax
Rank = RANKX('peakon rounds', 'peakon rounds'[closed_at], , desc)
```



```dax
Interval = if('peakon rounds'[Rank] <= 2, "Latest", "Previous")
```


## Table: peakon compare


```dax
'peakon rounds'
```


## Table: peakon_levels_for_report

### Measures:


```dax
level nps = 
var _count= COUNTROWS(peakon_results_by_level)
var _nps = CALCULATE(AVERAGE(peakon_results_by_level[nps]))
var _prependChar = "‏‏‎ ‎"
var _value = if( _nps = blank(), if( _count = 0
            , "n/a", "0")
            , Format(_nps, "#")
)

var _prepend = REPT(_prependChar, 11 - len(_value))

return _prepend & _value & _prepend

```

