



# DAX

|Dataset|[NFR Bridge](./../NFR-Bridge.md)|
| :--- | :--- |
|Workspace|[FC_NFR](../../Workspaces/FC_NFR.md)|

## Table: _measures

### Measures:


```dax
NFR max. = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[abs target_time_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Leave/Vacation/Training = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    ('nfr absolut'[abs leave_time_lc] + 'nfr absolut'[abs vacation_time_lc] + 'nfr absolut'[abs training_time_lc])
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
NFR max. adj. = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[abs target_time_adj_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Aquisition = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[abs acquisition_time_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Internal work = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    ('nfr absolut'[abs internal_time_lc] + 'nfr absolut'[abs diff_target_time_vs_booked_time_lc])
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
NFR gross = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[abs client_time_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Planned OD = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[abs planned_od_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Add. OD = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[abs add_od_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
NFR net consulting (Acc. NFR) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[abs acc_nfr_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Capture rate = [NFR net consulting (Acc. NFR)] / [NFR max. adj.]
```



```dax
h client time = sum('nfr absolut'[abs hours_worked_on_client_projects])
```



```dax
h adj. target hours = sum('nfr absolut'[abs target_hours_adj])
```



```dax
Utilization = [h client time] / [h adj. target hours]
```



```dax
Overdraft = ([Planned OD] + [Add. OD]) / [NFR net consulting (Acc. NFR)]
```



```dax
NumberOfDataRows = COUNTROWS('nfr absolut')
```



```dax
IsRelevantCurrency = 
var _cur = min(currencies[target_currency])

return if(_cur in {"EUR", "USD"}
    , 1
    , if(_cur in values(companies[currency]), 1, 0)
)
```



```dax
TestColor = "#AAFFFF55"
```



```dax
NFR max. (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[target_time_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Leave/Vacation/Training (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    ('nfr absolut'[leave_time_lc] + 'nfr absolut'[vacation_time_lc] + 'nfr absolut'[training_time_lc])
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
NFR max. adj. (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[target_time_adj_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Aquisition (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[acquisition_time_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Internal work (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    ('nfr absolut'[internal_time_lc] + 'nfr absolut'[diff_target_time_vs_booked_time_lc])
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
NFR gross (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[client_time_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Planned OD (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[planned_od_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Add. OD (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[add_od_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
NFR net consulting (Acc. NFR) (ytd) = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[acc_nfr_lc] 
    * 'nfr absolut'[rate to EUR]   // to euro
    * calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month) //to target
)
```



```dax
Capture rate (ytd) = [NFR net consulting (Acc. NFR) (ytd)] / [NFR max. adj. (ytd)]
```



```dax
Utilization (ytd) = [h client time (ytd)] / [h adj. target hours (ytd)]
```



```dax
h client time (ytd) = sum('nfr absolut'[hours_worked_on_client_projects])
```



```dax
h adj. target hours (ytd) = sum('nfr absolut'[target_hours_adj])
```



```dax
Overdraft (ytd) = ([Planned OD (ytd)] + [Add. OD (ytd)]) / [NFR net consulting (Acc. NFR) (ytd)]
```



```dax
dbg (ytd) local curr = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])

return Sumx(
     'nfr absolut'
    , 
    var _report_month = 'nfr absolut'[report_month]
    return 
    'nfr absolut'[target_time_lc] 
)
```



```dax
dbg (ytd) rate to euro = 

var _targetCurrency = SELECTEDVALUE(currencies[target_currency])
var _report_month = min( 'nfr absolut'[report_month])

var _toTargetCurr = calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month)

return 1 /  _toTargetCurr //min('nfr absolut'[rate to EUR])
```



```dax
dbg (ytd) rate to target = 
var _targetCurrency = SELECTEDVALUE(currencies[target_currency])
var _report_month = min( 'nfr absolut'[report_month])

var _toTargetCurr = calculate(min('exchange rates'[exchange_rate]), 'exchange rates'[target_currency] = _targetCurrency && 'exchange rates'[report_month] =  _report_month)

return  _toTargetCurr
```


## Table: Cal


```dax
CALENDARAUTO()
```


### Calculated Columns:


```dax
Year = Year(Cal[Date])
```



```dax
Month = Month(Cal[Date]) 
```


## Table: nfr absolut

### Calculated Columns:


```dax
abs target_time_lc = 'nfr absolut'[target_time_lc] - 'nfr absolut'[prev.target_time_lc]
```



```dax
abs leave_time_lc = 'nfr absolut'[leave_time_lc] - 'nfr absolut'[prev.leave_time_lc]
```



```dax
abs vacation_time_lc = 'nfr absolut'[vacation_time_lc] - 'nfr absolut'[prev.vacation_time_lc]
```



```dax
abs training_time_lc = 'nfr absolut'[training_time_lc] -'nfr absolut'[prev.training_time_lc]
```



```dax
abs internal_time_lc = 'nfr absolut'[internal_time_lc] - 'nfr absolut'[prev.internal_time_lc]
```



```dax
abs diff_target_time_vs_booked_time_lc = 'nfr absolut'[diff_target_time_vs_booked_time_lc] -'nfr absolut'[prev.diff_target_time_vs_booked_time_lc]
```



```dax
abs client_time_lc = 'nfr absolut'[client_time_lc] - 'nfr absolut'[prev.client_time_lc]
```



```dax
abs target_time_adj_lc = 'nfr absolut'[target_time_adj_lc] - 'nfr absolut'[prev.target_time_adj_lc]
```



```dax
abs acc_nfr_lc = 'nfr absolut'[acc_nfr_lc] - 'nfr absolut'[prev.acc_nfr_lc]
```



```dax
abs planned_od_lc = 'nfr absolut'[planned_od_lc] - 'nfr absolut'[prev.planned_od_lc]
```



```dax
abs add_od_lc = 'nfr absolut'[add_od_lc] - 'nfr absolut'[prev.add_od_lc]
```



```dax
abs acquisition_time_lc = 'nfr absolut'[acquisition_time_lc] - 'nfr absolut'[prev.acquisition_time_lc]
```



```dax
abs target_hours_adj = 'nfr absolut'[target_hours_adj]- 'nfr absolut'[prev.target_hours_adj]
```



```dax
abs hours_worked_on_client_projects = 'nfr absolut'[hours_worked_on_client_projects]- 'nfr absolut'[prev.hours_worked_on_client_projects]
```



```dax
rate to EUR = 1 / 'nfr absolut'[rate from EUR]
```


## Table: Formatting

### Measures:


```dax
Value = 
var _key =SELECTEDVALUE(Formatting[key])

return
switch(_key
    , "max", [NFR max.]
    , "l_v_t", [Leave/Vacation/Training] * -1
    , "max_adj", [NFR max. adj.]
    , "acq", [Aquisition] * -1
    , "iw", [Internal work] * -1
    , "gross", [NFR gross]
    , "p_od", [Planned OD] * -1
    , "a_od", [Add. OD] * -1
    , "acc", [NFR net consulting (Acc. NFR)]

    , "ofi", blank()
    , "reported", blank()
    , "e_rev", blank()
    , "n_rev", blank()
)
```



```dax
Value (ytd) = 
var _key =SELECTEDVALUE(Formatting[key])

return
switch(_key
    , "max", [NFR max. (ytd)]
    , "l_v_t", [Leave/Vacation/Training (ytd)] * -1
    , "max_adj", [NFR max. adj. (ytd)]
    , "acq", [Aquisition (ytd)] * -1
    , "iw", [Internal work (ytd)] * -1
    , "gross", [NFR gross (ytd)]
    , "p_od", [Planned OD (ytd)] * -1
    , "a_od", [Add. OD (ytd)] * -1
    , "acc", [NFR net consulting (Acc. NFR) (ytd)]

    , "ofi", blank()
    , "reported", blank()
    , "e_rev", blank()
    , "n_rev", blank()
)
```

