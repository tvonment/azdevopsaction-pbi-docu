



# DAX

|Dataset|[Central Graphics Statistic](./../Central-Graphics-Statistic.md)|
| :--- | :--- |
|Workspace|[Central Graphics](../../Workspaces/Central-Graphics.md)|

## Table: vEmpStaffingDetail_Report

### Measures:


```dax
ReportYear = Not available
```


### Calculated Columns:


```dax
HoursBookedInternalActivity = if('vEmpStaffingDetail_Report'[CategoryID] =3,vEmpStaffingDetail_Report[HoursBooked],0)
```



```dax
HomeVsOtherCtry = if(vEmpStaffingDetail_Report[ContactCountryCode] = vEmpStaffingDetail_Report[CountryCode],"Home", "Other")
```



```dax
CategoryGroup2 = if(AND(vEmpStaffingDetail_Report[CategoryGroupID]=1,vEmpStaffingDetail_Report[BookingTypeID]=10),"Booked hours (Central Graphics)",vEmpStaffingDetail_Report[CategoryGroup])
```



```dax
HoursCategory = if(vEmpStaffingDetail_Report[HoursBooked] > 8,"> 8h",CONCATENATE(ROUNDUP(vEmpStaffingDetail_Report[HoursBooked],0),"h"))
```



```dax
HoursCategoryId = if(vEmpStaffingDetail_Report[HoursBooked] > 8,9,ROUNDUP(vEmpStaffingDetail_Report[HoursBooked],0))
```


## Table: pub dim_date

### Calculated Columns:


```dax
MonthYearShort = Format([Date],"MMM yyyy")
```



```dax
isBeforeCurrentMonth = IF('pub dim_date'[Date]<DATE(YEAR(TODAY()), MONTH(TODAY()), 1), true, FALSE)
```



```dax
isCurrentReportMonth = IF(AND('pub dim_date'[Date] >= EOMONTH(TODAY(),-2)+1, 'pub dim_date'[Date] <= EOMONTH(TODAY(),-1)),true,false)
```


## Table: PercentageHoursBookedInternal


```dax
SUMMARIZE(FILTER(vEmpStaffingDetail_Report,vEmpStaffingDetail_Report[OperatorName] <> "Waiting, List")  
      , vEmpStaffingDetail_Report[validfrom_date], vEmpStaffingDetail_Report[CountryCode]
      , "HoursBookedTotal", SUM(vEmpStaffingDetail_Report[HoursBooked])  
      , "HoursBookedInternal", SUM(vEmpStaffingDetail_Report[HoursBookedInternalActivity])
      , "PercentageOfInternalHours", DIVIDE(SUM(vEmpStaffingDetail_Report[HoursBookedInternalActivity]),SUM(vEmpStaffingDetail_Report[HoursBooked]))
      ) 
```


## Table: vOrderFeedback_Report

### Measures:


```dax
%OfRatedFeedback = 
VAR __BASELINE_VALUE =
	CALCULATE(
		SUM('vOrderFeedback_Report'[CountFeedback]),
		'vOrderFeedback_Report'[ScoreGroupSortID] IN { 2 }
	)
VAR __MEASURE_VALUE = SUM('vOrderFeedback_Report'[CountFeedback])
RETURN
	IF(
		NOT ISBLANK(__MEASURE_VALUE),
		DIVIDE(__BASELINE_VALUE, __MEASURE_VALUE)
	)
```


### Calculated Columns:


```dax
CountFeedback = 1
```

