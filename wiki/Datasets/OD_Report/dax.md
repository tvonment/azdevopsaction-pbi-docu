



# DAX

|Dataset|[OD_Report](./../OD_Report.md)|
| :--- | :--- |
|Workspace|[F&C](../../Workspaces/F&C.md)|

## Table: NFR

### Measures:


```dax
Monthly_OD = if(MONTH(MAX(NFR[report_month]))=1,sum(NFR[sum_od_lc]),sum(NFR[sum_od_lc])-CALCULATE(sum(NFR[sum_od_lc]),PREVIOUSMONTH('Calendar'[Date])))
```



```dax
Monthly_NFR = if(MONTH(min(NFR[report_month]))=1,sum(NFR[acc_nfr_lc]),sum(NFR[acc_nfr_lc])-CALCULATE(sum(NFR[acc_nfr_lc]),PREVIOUSMONTH('Calendar'[Date])))
```



```dax
Monthly_OD_alternative = 
var _max = EOMONTH(max('Calendar'[Date]),-1)
var _min1  = EOMONTH(max('Calendar'[Date]),-2) +1
var _min = if( YEAR(_min1) <> YEAR(max('Calendar'[Date])) ,_max+1, _min1)
return
CALCULATE(SUM(NFR[sum_od_lc]), DATESMTD('Calendar'[Date])) - CALCULATE(SUM(NFR[sum_od_lc]),DATESBETWEEN('Calendar'[Date],_min, _max))
```



```dax
LTM_OD = 
CALCULATE( sumx(VALUES('Calendar'[SortMonth]), [Monthly_OD]), DATESINPERIOD('Calendar'[Date], max('Calendar'[Date]), -12, MONTH))
```



```dax
LTM_NFR = 
CALCULATE( sumx(VALUES('Calendar'[SortMonth]), [Monthly_NFR]), DATESINPERIOD('Calendar'[Date], max('Calendar'[Date]), -12, MONTH))
```



```dax
LTM_OD% = [LTM_OD]/[LTM_NFR]
```



```dax
Monthly_OD% = [Monthly_OD]/[Monthly_NFR]
```



```dax
Monthly_TargetHours = if(MONTH(MAX(NFR[report_month]))=1,sum(NFR[target_time_adj_lc]),sum(NFR[target_time_adj_lc])-CALCULATE(sum(NFR[target_time_adj_lc]),PREVIOUSMONTH('Calendar'[Date])))
```



```dax
Monthly_CaptureRate% = [Monthly_NFR]/[Monthly_TargetHours]
```



```dax
LTM_TargetHours = 
CALCULATE( sumx(VALUES('Calendar'[SortMonth]), [Monthly_TargetHours]), DATESINPERIOD('Calendar'[Date], max('Calendar'[Date]), -12, MONTH))
```



```dax
LTM_CaptureRate% = [LTM_NFR]/[LTM_TargetHours]
```



```dax
YTD_OD% = CALCULATE(sum(NFR[sum_od_lc])/sum(NFR[acc_nfr_lc]))
```



```dax
YTD_CaptureRate% = CALCULATE(sum(NFR[acc_nfr_lc])/sum(NFR[target_time_adj_lc]))
```


## Table: Calendar


```dax
ADDCOLUMNS(CALENDAR(min(NFR[report_month]),max(NFR[report_month])),"Month - Year", FORMAT([Date],"mmm - yyyy"),"SortMonth",FORMAT([Date],"yyyymm"), "SortID", (YEAR([Date]) * 12 + MONTH([Date])) * -1)
```

