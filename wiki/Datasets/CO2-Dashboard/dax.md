



# DAX

|Dataset|[CO2 Dashboard](./../CO2-Dashboard.md)|
| :--- | :--- |
|Workspace|[Travel & Mobility](../../Workspaces/Travel-&-Mobility.md)|

## Table: Calendar


```dax

ADDCOLUMNS (
CALENDAR(MIN(co2kg[date]), max(co2kg[date]) ),
"DateAsInteger", FORMAT ( [Date], "YYYYMMDD" ),
"Year", YEAR ( [Date] ),
"Monthnumber", FORMAT ( [Date], "MM" ),
"YearMonthnumber", year([DATE]) *100 + month([DATE]), -- FORMAT ( [Date], "YYYY/MM" ),
"YearMonthShort", FORMAT ( [Date], "YYYY/mmm" ),
"MonthNameShort", FORMAT ( [Date], "mmm" ),
"MonthNameLong", FORMAT ( [Date], "mmmm" ),
"DayOfWeekNumber", WEEKDAY ( [Date] ),
"DayOfWeek", FORMAT ( [Date], "dddd" ),
"DayOfWeekShort", FORMAT ( [Date], "ddd" ),
"Quarter", "Q" & FORMAT ( [Date], "Q" ),
"YearQuarter", FORMAT ( [Date], "YYYY" ) & "/Q" & FORMAT ( [Date], "Q" ),
"Week Number", WEEKNUM ( [Date] , 2),
"YearWeekNumber", YEAR ( [Date] ) & 100 + WEEKNUM ( [Date], 2 )
)
```


### Calculated Columns:


```dax
Month Offset = 
var _curMonth= 'Calendar'[YearMonthnumber]
var _statusMonth = min(_meta[Status month])
return  _curMonth - _statusMonth
```



```dax
In YTD = 
var _curDate= 'Calendar'[Date]
var _statusdate = min(_meta[DateTo])

return if(year (_curDate) = year(_statusdate) && month(_curDate) <= month(_statusdate), 1, 0)
```


## Table: co2kg

### Measures:


```dax
Sum co2kg = sum(co2kg[co2kg])
```



```dax
# entries = COUNTROWS(values(co2kg[Index]))
```



```dax
# flight entries = calculate([# entries], co2kg[type] = "Flight")
```



```dax
co2kg for single employee = if(HASONEVALUE('rls own user'[emp_id]), 
     CALCULATE( [Sum co2kg], TREATAS(values('rls own user'[emp_id]), employee[emp_id] ))
    , blank()
)
```



```dax
co2kg avg for peer = 
if(HASONEVALUE('rls own user'[emp_id]), 
    var _peerGroup = SELECTEDVALUE('rls own user'[peer_group])
    var _peerIds = CALCULATETABLE(values(employee[emp_id]), employee[peer_group] = _peerGroup) 
    var _peers = CALCULATETABLE( values(co2kg[emp_id]), all(co2kg), TREATAS(_peerIds, co2kg[emp_id]) )

    return  divide( calculate( sumx(_peers,  [Sum co2kg]),  REMOVEFILTERS(employee[Employee]))
    ,
     countrows(_peerIds) 
    //countrows(_peers)
    )
    , blank()
)
```



```dax
cumulative co2kg = 
var _max = max('Calendar'[Date])
var _min = calculate(MIN('Calendar'[Date]), ALLCROSSFILTERED('Calendar'))

return CALCULATE( [Sum co2kg], REMOVEFILTERS('Calendar'), 'Calendar'[Date]>= _min && 'Calendar'[Date] <= _max)

```



```dax
cumulative for single employee = if(HASONEVALUE('rls own user'[emp_id]), calculate([cumulative co2kg], TREATAS(values('rls own user'[emp_id]), employee[emp_id] )), blank())
```



```dax
cumulative co2kg peer = 
[_peer rt co2 per month]
/*
var _max = max('Calendar'[Date])
var _min = calculate(MIN('Calendar'[Date]), ALLCROSSFILTERED('Calendar'))

return CALCULATE(sumx( values('Calendar'[YearMonthnumber]), [co2kg avg for peer])  , REMOVEFILTERS('Calendar'), 'Calendar'[Date]>= _min && 'Calendar'[Date] <= _max)
*/
```



```dax
co2 flight for single = CALCULATE([co2kg for single employee], co2kg[type] = "Flight")
```



```dax
science-based target = 
var _cur = max('Calendar'[Date])

var _dates = CALCULATETABLE(values('Calendar'[Date]), ALLSELECTED('Calendar'))
var _before = Filter(_dates, 'Calendar'[Date]<= _cur)

var _months = calculatetable(values('rls own hr_statistics'[validfrom_date]), _before)

return countrows(_months) * 622 //143
```



```dax
avoidable = sum(co2kg[avoidable_emissions])
```



```dax
avoidable lm = 
var lm = min(_meta[DateTo])
return CALCULATE([avoidable for single employee], year(co2kg[date]) = year(lm) && Month(co2kg[date]) = month(lm))
```



```dax
avoidable ytd = 
var lm = min(_meta[DateTo])
return CALCULATE([avoidable for single employee], year(co2kg[date]) = year(lm) && Month(co2kg[date]) <= month(lm))
```



```dax
avoidable for single employee = if(HASONEVALUE('rls own hr_statistics'[emp_id]), 
     CALCULATE( [avoidable], TREATAS(values('rls own hr_statistics'[emp_id]), employee[emp_id] ))
    , blank()
)
```



```dax
avoidable lm 0 = coalesce([avoidable lm],0)
```



```dax
avoidable ytd 0 = coalesce([avoidable ytd], 0)
```



```dax
Measure 2 = Not available
```



```dax
peer group of user in month = min(hr_statistics[peer_group]) 
```



```dax
_co2 own emp = if(HASONEVALUE('rls own hr_statistics'[emp_id]), 
     CALCULATE( [Sum co2kg], TREATAS(values('rls own hr_statistics'[emp_id]), employee[emp_id] ))
    , blank()
)
```



```dax
_peer own single month = if(HASONEVALUE('rls own hr_statistics'[emp_id]) && HASONEVALUE('Calendar'[YearMonthnumber]), 
     min('rls own hr_statistics'[peer_group])
    , blank()
)
```



```dax
_peer avg co2 per month = 
sumx(
    values('Calendar'[YearMonthnumber])
    , 
    var _peer =  if(HASONEVALUE('rls own hr_statistics'[emp_id]) && HASONEVALUE('Calendar'[YearMonthnumber]), 
                    min('rls own hr_statistics'[peer_group])
                    , blank()
                )
    var _fom = min ('Calendar'[Date])
    
    return 
        Divide (calculate(sum(co2kg[co2kg]), REMOVEFILTERS('Calendar'[Date]), co2kg[peer_group] = _peer , 'Calendar'[Date] = _fom  )
            ,  calculate(Countrows(Values(hr_statistics[emp_id])),REMOVEFILTERS('Calendar'[Date]), hr_statistics[peer_group] = _peer , 'Calendar'[Date] = _fom  )
            , blank())
)
```



```dax
_peer rt co2 per month = 
var _curMonth = max( 'Calendar'[Monthnumber])

return sumx(
    
    calculatetable(values('Calendar'[YearMonthnumber]), All('Calendar'), 'Calendar'[Monthnumber] <= _curMonth )
    , 
    var _ymn = 'Calendar'[YearMonthnumber]
    var _fom = calculate(min ('Calendar'[Date]), all('Calendar'), 'Calendar'[YearMonthnumber] = _ymn)
    var _peer =  if(HASONEVALUE('rls own hr_statistics'[emp_id]) , 
                    calculate(min('rls own hr_statistics'[peer_group]), all('rls own hr_statistics'),  'rls own hr_statistics'[validfrom_date] = _fom )
                    , blank()
                )
    
    
    return   
        Divide (
            calculate(sum(co2kg[co2kg]), REMOVEFILTERS('Calendar'), co2kg[peer_group] = _peer , co2kg[FirstOfMonth] = _fom  )
           ,   calculate(Countrows(Values(hr_statistics[emp_id])), REMOVEFILTERS('Calendar'), hr_statistics[peer_group] = _peer,  hr_statistics[validfrom_date] = _fom)
           , blank())
)
```



```dax
dbg avg = 
var _peer = SELECTEDVALUE(co2kg[peer_group])

return DIVIDE(calculate(sum(co2kg[co2kg])),  calculate( COUNTROWS(values(hr_statistics[emp_id])), hr_statistics[peer_group] = _peer )) 
```



```dax
check month = 
var _curMonth = max( 'Calendar'[Monthnumber])

return minx(
    calculatetable(values('Calendar'[YearMonthnumber]), All('Calendar'), 'Calendar'[Monthnumber] <= _curMonth )
    , 
    var _ymn = calculate(SELECTEDVALUE('Calendar'[YearMonthnumber]))
    return   _ymn
)
```


## Table: _meta

### Measures:


```dax
Measure = DATEADD(_meta[DateTo], -1, year)
```



```dax
_title ye lm = "Your emissions last month (" & calculate(min( 'Calendar'[MonthNameLong])) &")"
```



```dax
_max total value = 
var _peer = CALCULATE([_peer rt co2 per month], REMOVEFILTERS(co2kg[type]))
var _your = CALCULATE( [co2kg for single employee], REMOVEFILTERS(co2kg[type]))

return if(_peer>= _your, _peer, _your)
```



```dax
percentage = divide( [co2kg for single employee] - [_peer rt co2 per month] , [_peer rt co2 per month])
```



```dax
mor or less = if([co2kg for single employee] > [_peer rt co2 per month], "more", "less")
```



```dax
additional text = 
var _you = [cumulative for single employee]
var _peer = [cumulative co2kg peer] 
var _science = [science-based target]

return 
switch(true
    , _you > _science && _you < _peer
    , "yet, you’re still " &  format(divide(_you-_science, _science, 0)*100, "#") & "% above the RB travel emission target"
    , _you <= _science && _you <= _peer
    ,"and your emissions are below the RB travel emission target"
    ,_you > _science && _you > _peer
    , "and are still " &  format(divide(_you-_science, _science, 0) * 100, "#") & "% above the RB travel emission target"
    ,_you < _science && _you > _peer
    , "while beating the RB travel emission targets by " &  format(divide(_you-_science, _science, 0) * 100, "#") & "%"
)
//& "  " & format(_you, "#")  & " - " & format(_peer, "#") & " - " & format(_science , "#")
```


### Calculated Columns:


```dax
DateTo = max(co2kg[date]) 
```



```dax
Status month = 
var _to = _meta[DateTo]
return calculate(min('Calendar'[YearMonthnumber]),'Calendar'[Date] = _to)
```


## Table: employee

### Calculated Columns:


```dax
Employee = employee[full_name] &" (" & employee[emp_id] & ")"
```


## Table: Types

### Measures:


```dax
co2kg by type = 
var _who = SELECTEDVALUE(Who[Who])
var _type = SELECTEDVALUE(Types[Type])

return 
    switch(true()
        , _who = "You" && _type = "Total", [co2kg for single employee]
        , _who = "Peer" && _type = "Total", [co2kg avg for peer]

        , _who = "You", CALCULATE( [co2kg for single employee], co2kg[type] = _type)
        , _who = "Peer", CALCULATE( [co2kg avg for peer], co2kg[type] = _type)
)

```


### Calculated Columns:


```dax
Type_ = 
VAR TypeLength = LEN(Types[Type])
VAR FillLength = 9 - TypeLength
RETURN switch( Types[Type], 
 "Flight", Types[Type] & REPT(" ", 6)
 , "Taxi", Types[Type] & REPT(" ", 9)
 , Types[Type]
)
```


## Table: rls own user

### Calculated Columns:


```dax
Employee = 'rls own user'[full_name] &" (" & 'rls own user'[emp_id] & ")"
```


## Table: Texts

### Measures:


```dax
txt could have saved = "could have saved"
```



```dax
txt Last month, no avoidable emissions identified. = "Last month, no avoidable emissions identified. "
```



```dax
txt No avoidable emissions = "No avoidable emissions identified that you could have saved by travelling by train instead of flying."
```



```dax
dtxt lm start = 
var av_ytd = [avoidable ytd]
var av_lm = [avoidable lm]

return if(av_ytd>0
    ,  if(av_lm > 0
        , //last month > 0
        "You could have saved "
        , // lm = 0, but total
        [txt Last month, no avoidable emissions identified.]
        )
        , //total = 0
        [txt No avoidable emissions]
    )
```



```dax
txt  However, your total avoidable emissions this year are = " However, your total avoidable emissions this year are "
```



```dax
txt . By travelling by train on these distances, you could have benefited from our railway incentive. = ". By travelling by train on these distances, you could have benefited from our railway incentive."
```



```dax
dtxt lm value = 

var av_lm = [avoidable lm]

return 
    if(av_lm > 0
        , //last month > 0
        Format(av_lm, "0.00") & " kg"
        ,
        
        ""
    )    
```



```dax
dtxt lm end = 
var av_ytd = [avoidable ytd]
var av_lm = [avoidable lm]

return 
      if(av_lm > 0
        , //last month > 0
        " of CO2 emissions last month and "
        , // lm = 0, but total
        ""
        )
        
```



```dax
dtxt ytd start = 
var av_ytd = [avoidable ytd]
var av_lm = [avoidable lm]
 
return if(av_ytd>0
    ,  if(av_lm > 0
        , //last month > 0
        "" //value first
        , // lm = 0, but total
        "However, your total avoidable emissions this year are "
        )
        , //total = 0
        ""
    )
```



```dax
dtxt ytd value = 
var av_ytd = [avoidable ytd]

return 
    if(av_ytd > 0
        , //last month > 0
        Format(av_ytd, "0.00") & " kg"
        ,
        
        ""
    ) 
```



```dax
dtxt ytd end = 
var av_ytd = [avoidable ytd]
var av_lm = [avoidable lm]
 
return if(av_ytd>0
    ,  if(av_lm > 0
        , //last month > 0
        "this year in total by travelling by train instead of flying. This way, you could have benefited from our railway incentive."
        , // lm = 0, but total
        ". By travelling by train on these distances, you could have benefited from our railway incentive. "
        )
        , //total = 0
        ""
    )
```


## Table: peer_groups


```dax
values(hr_statistics[peer_group])
```

