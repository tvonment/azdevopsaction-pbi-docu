



# DAX

|Dataset|[BU Project Assessment](./../BU-Project-Assessment.md)|
| :--- | :--- |
|Workspace|[BU Project Assessment [Dev]](../../Workspaces/BU-Project-Assessment-[Dev].md)|

## Table: rep v_hr_employee

### Calculated Columns:


```dax
Overall = "Overall"
```



```dax
Overall Y/N = "Overall (Y/N)" 
```


## Table: Calendar


```dax
CALENDAR(DATE(2022, 1, 1), Today() +  7)
```


### Measures:


```dax
Interval = Format( min('Calendar'[Date]), "DDD dd.MM") & " - "  & Format( max('Calendar'[Date]), "DDD dd.MM")
```


### Calculated Columns:


```dax
WEEK = Format( YEAR('Calendar'[Date]), 0) & "-" & WEEKNUM('Calendar'[Date],21)
```



```dax
WeekOffset = 
var _curDate = 'Calendar'[Date]
var _refreshDate = [RefreshDate]
var _todaysWeek  = calculate(min('Calendar'[WEEK]), all ('Calendar'), 'Calendar'[Date] = _refreshDate)
var _endOfTodaysWeek  = calculate(max('Calendar'[Date]), all ('Calendar'), 'Calendar'[WEEK] = _todaysWeek)

return 
if(_curDate > _endOfTodaysWeek, 99,
   -1 * (coalesce(CALCULATE(COUNTROWS(distinct('Calendar'[WEEK])),All('Calendar'), 'Calendar'[Date] <= _endOfTodaysWeek && 'Calendar'[Date] >=_curDate ), 0) -1)
)
```



```dax
IsWeekday = WEEKDAY('Calendar'[Date]) <> 1 && WEEKDAY('Calendar'[Date]) <> 7 
```



```dax
ShiftedWeekOffest = 
var _wd = WEEKDAY('Calendar'[Date])

return if(_wd >= 4 // MI 4, Do 5, Fr 6 , Sa 7
    || _wd = 1 //So
    , 'Calendar'[WeekOffset] + 1
    , 'Calendar'[WeekOffset])


```



```dax
dow = WEEKDAY('Calendar'[Date])
```



```dax
Shifted Weekname = 
var _offset = 'Calendar'[ShiftedWeekOffest]

var _minDate = CALCULATE(min('Calendar'[Date]), all('Calendar'),'Calendar'[ShiftedWeekOffest] = _offset)

return Format( YEAR(_minDate), 0) & "-CW" & Format(WEEKNUM(_minDate, 21), "00")
```


## Table: _Measures

### Measures:


```dax
RefreshDate = min(RefreshDate[RefreshDate])
```



```dax
RefreshDateWeek = LOOKUPVALUE('Calendar'[Shifted Weekname],'Calendar'[Date],[RefreshDate])
```


## Table: Bottom Up

### Measures:


```dax
Number of Assessments = Sum('Bottom Up'[CNT_FORMS])
```



```dax
# detractors = sum('Bottom Up'[CNT_DETRACTORS])
```



```dax
# passives = SUM('Bottom Up'[CNT_PASSIVES])
```



```dax
# ppd total = [# detractors] + [# passives] + [# promoters]
```



```dax
# promoters = sum('Bottom Up'[CNT_PROMOTORS])
```



```dax
% detractors = DIVIDE([# detractors], [# ppd total])
```



```dax
% passives = DIVIDE([# passives], [# ppd total])
```



```dax
% promoters = DIVIDE([# promoters], [# ppd total])
```



```dax
NPS = ([% promoters] - [% detractors]) * 100
```


## Table: Bottom Up Questions

### Measures:


```dax
BottomUpColor = 
if(min('Bottom Up Questions'[Group]) = "Supporter Score"
    ,   "#C2C8CC"
    , if(min('Bottom Up Questions'[Group]) = "Number of assessments"
        ,   "#C2C8CC"
        ,   
            var _result = [result]
            return switch(true()
                , _result < 2, "#FD625E" //rot
                , _result <= 3, "#ECC846" //gelb
                //, _result <= 3, "#F7E9B5"
                //, _result < 3.5, "#ABD4A0"
                , "#73B761" //grün
                )
    )
)
```


## Table: Bottom Up Results

### Measures:


```dax
# of results = sum('Bottom Up Results'[Column Count])
```



```dax
sum of results = sum('Bottom Up Results'[Column Sum])
```



```dax
avg of results = 
 DIVIDE([sum of results], [# of results] )
```



```dax
result = 
var _questionGroup = min( 'Bottom Up Questions'[Group])

return switch(_questionGroup
    ,"Number of assessments", [# of results ranged]
    , "Overall", [Overall result]
    ,  [avg of results])
```



```dax
Overall result = 

if(ISINSCOPE('rep v_hr_employee'[full_name])
, if(CountRows('Bottom Up') > 0
    ,   var _empId = min( 'rep v_hr_employee'[emp_id])
        return CALCULATE(AVERAGEX('Bottom Up Questions', [avg of results]), ALLCROSSFILTERED('Bottom Up Results'), 'Bottom Up Results'[ID_ASSESSEE] = _empId, 'Bottom Up Questions'[InOverall] = 1)
    , blank()
    )
, blank())
```



```dax
# of results ranged = 
var _count =  [# of results]

return switch(true()
    , _count = blank(), blank()
    , _count<5, "<5"
    , _count<10, ">=5" 
    , _count<15, ">=10" 
    , _count<20, ">=15"
    , _count<25, ">=20" 
    , ">=25"
)
```



```dax
DataCount BU = COUNTROWS('Bottom Up Results')
```


## Table: RefreshDate

### Measures:


```dax
BU interval text = Format(min(RefreshDate[BU Start Month]), "MMM YY") & " - " & Format(min(RefreshDate[BU End Month]), "MMM YY")  
```


## Table: employees bu


```dax
'rep v_hr_employee'
```

