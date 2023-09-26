



# DAX

|Dataset|[Usage Metrics Report](./../Usage-Metrics-Report.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: Report views

### Calculated Columns:


```dax
Date = DATE(YEAR('Report views'[CreationTime]), MONTH('Report views'[CreationTime]), DAY('Report views'[CreationTime]))
```



```dax
ConsumptionMethod = 
SWITCH('Report views'[OriginalConsumptionMethod],
    "Embedding for your customers", "Embedded",
    "Embedding for your organization", "Embedded",
    "Power BI mobile", "Mobile",
    "Power BI web", "PowerBI.com",
    "Simplified embedding", "Embedded",
    "", "Not specified",
    BLANK(), "Not specified",
    "Other")

```


## Table: Model measures

### Measures:


```dax
Report views = COUNTROWS('Report views') + 0
```



```dax
Report viewers = DISTINCTCOUNT('Report views'[UserKey]) + 0
```



```dax
Page view share = DIVIDE(COUNTROWS('Report page views'), CALCULATE(COUNTROWS('Report page views'), ALL('Report pages'[SectionName])), 0)
```



```dax
View trend = 
var numberOfDays = DATEDIFF(MIN('Report views'[Date]), MAX('Report views'[Date]),DAY) + 1
var periodLength = INT(numberOfDays/2) - 1
var firstPeriod = CALCULATE([Report views], DATESBETWEEN('Report views'[Date], MIN('Report views'[Date]), MIN('Report views'[Date]) + periodLength))
var secondPeriod = CALCULATE([Report views], DATESBETWEEN('Report views'[Date], MAX('Report views'[Date]) - periodLength, MAX('Report views'[Date])))
return DIVIDE(secondPeriod - firstPeriod, firstPeriod)  + 0
```



```dax
P-50 = PERCENTILE.INC('Report load times'[loadTime], 0.5) + 0
```



```dax
P-50 7d = CALCULATE([P-50], ALL(Dates), DATESINPERIOD('Report load times'[Date], max('Report load times'[Date]), -7, DAY)) + 0
```



```dax
P-25 = PERCENTILE.INC('Report load times'[loadTime], 0.25) + 0
```



```dax
P-10 = PERCENTILE.INC('Report load times'[loadTime], 0.1) + 0
```



```dax
P-90 7d = CALCULATE([P-90], ALL(Dates), DATESINPERIOD('Report load times'[Date], max('Report load times'[Date]), -7, DAY)) + 0
```



```dax
P-10 7d = CALCULATE([P-10], DATESINPERIOD('Report load times'[Date], max('Report load times'[Date]), -7, DAY)) + 0
```



```dax
Typical report opening interval = IF(ISBLANK(MAX('Report load times'[loadTime]) ), 
    "This report has no performance measurements.",
    IF(HASONEVALUE('Report load times'[loadTime]), 
        "This report only has a single performance measurement. The load time was " & MAX('Report load times'[loadTime]) & " seconds.", 
        IF([P-10] = [P-50] = [P-25], 
            "Across all measurements, this report loaded in  " & MAX('Report load times'[loadTime]) & " seconds.", 
            "For most of the users your report opens within " & INT([P-10 7d]) & " and " & INT([P-90 7d]) & " seconds." )))
```



```dax
Rank string = IF(HASONEVALUE(Reports[ReportGuid]), IF(ISBLANK(MAX('Report rank'[ReportRank])), "", "Rank " & MAX('Report rank'[ReportRank]) & " across "& [Total Org Report Count] & " reports in the organization"), "")
```



```dax
Performance trend = 
var numberOfDays = DATEDIFF(MIN('Report views'[Date]), MAX('Report views'[Date]),DAY) + 1
var periodLength = INT(numberOfDays/2) - 1
var firstPeriod = CALCULATE([P-50], DATESBETWEEN('Report load times'[Date], MIN('Report load times'[Date]), MIN('Report load times'[Date]) + periodLength))
var secondPeriod = CALCULATE([P-50], DATESBETWEEN('Report load times'[Date], MAX('Report load times'[Date]) - periodLength, MAX('Report load times'[Date])))
return DIVIDE(secondPeriod - firstPeriod, firstPeriod) + 0 * -1
```



```dax
Typical report opening time = [P-50] & " sec"
```



```dax
Workspace report viewers = DISTINCTCOUNT('Workspace views'[UserKey]) + 0
```



```dax
Workspace inactive reports = CALCULATE(DISTINCTCOUNT('Workspace reports'[ReportGuid]), 'Workspace reports'[Days with usage] = 0) + 0
```



```dax
Workspace views = SUM('Workspace views'[Views]) + 0
```



```dax
Workspace active days per report = DISTINCTCOUNT('Report views'[Date]) + 0
```



```dax
Workspace reports = DISTINCTCOUNT('Report views'[ReportId])
```



```dax
Workspace active reports = DISTINCTCOUNT('Workspace views'[ReportId]) + 0
```



```dax
Workspace report view % = DIVIDE([Workspace views], CALCULATE([Workspace views], ALL('Workspace views')))
```



```dax
Covered time display string = IF(ISBLANK(MAX('Report views'[CreationTime])), "No usage data", "Report usage based on data from " & 
DATE(
  YEAR(MIN('Report views'[CreationTime])),
  MONTH(MIN('Report views'[CreationTime])),
  DAY(MIN('Report views'[CreationTime]))
)
 & " to " & 
DATE(
  YEAR(MAX('Report views'[CreationTime])),
  MONTH(MAX('Report views'[CreationTime])),
  DAY(MAX('Report views'[CreationTime]))
))
```



```dax
Embedding for your organziation = CALCULATE([Report views], 'Report views'[OriginalConsumptionMethod] = "Embedding for your organization")
```



```dax
Embedding for your customers = CALCULATE([Report views], 'Report views'[OriginalConsumptionMethod] = "Embedding for your customers")
```



```dax
Simplified embedding = CALCULATE([Report views], 'Report views'[OriginalConsumptionMethod] = "Simplified embedding")
```



```dax
Workspace view trend = 
var startDate = CALCULATE(MIN('Dates'[Date]), ALL('Dates'))
var endDate = CALCULATE(MAX('Dates'[Date]), ALL('Dates'))
var numberOfDays = DATEDIFF(startDate, endDate, DAY) + 1
var periodLength = INT(numberOfDays/2) - 1
var middleDate1 =  CALCULATE(LASTDATE(DATESBETWEEN('Dates'[Date], startDate, startDate + periodLength)) , ALL('Dates'))
var middleDate2 =  CALCULATE(FIRSTDATE(DATESBETWEEN('Report views'[Date], endDate - periodLength, endDate)), ALL('Dates'))
var firstPeriod = CALCULATE([Report views], ALL('Dates'), DATESBETWEEN('Report views'[Date], startDate, middleDate1))
var secondPeriod = CALCULATE([Report views], ALL('Dates'), DATESBETWEEN('Report views'[Date], middleDate2, endDate))
//return startDate & "  " & middleDate1 & " " & middleDate2 & "  " & numberOfDays & ", " & periodLength & ": " & firstPeriod & "  " & secondPeriod
return DIVIDE(secondPeriod - firstPeriod, firstPeriod, 0)
```



```dax
Last refresh time display string = IF(ISBLANK(MAX('Refresh Stats'[Last Refresh])), 
	"Usage data has not been imported yet. Check the refresh history and data source credentials in the Usage Metrics Report dataset settings.", 
	IF(DATEVALUE(MAX('Refresh Stats'[Last Refresh])) < DATE(2019,11,20),
	"Usage data has not been imported yet. Check the refresh history and data source credentials in the Usage Metrics Report dataset settings.", 
	IF(DATEDIFF(MAX('Refresh Stats'[Last Refresh]), TODAY(), day ) > 4, 
		"The usage data is outdated. Check the refresh history and data source credentials in the Usage Metrics Report dataset settings.", 
		"Dataset last refreshed: " & MAX('Refresh Stats'[Last Refresh]) & " (UTC)")))
```



```dax
Report title = "Usage Metrics" & IF(HASONEVALUE(Reports[ReportGuid]), ": " & MAX('Reports'[ReportName]), " (Multiple reports selected)")
```



```dax
Report Id = IF(HASONEVALUE(Reports[ReportGuid]), MAX('Reports'[ReportGuid]), IF(DISTINCTCOUNT(Reports[ReportGuid]) = 0, "No reports selected", "Multiple reports selected"))
```



```dax
Covered perf time display string = IF(ISBLANK(MAX('Report load times'[Timestamp])), "No open report performance data", "Report performance based on data from " & 
DATE(
  YEAR(MIN('Report load times'[Timestamp])),
  MONTH(MIN('Report load times'[Timestamp])),
  DAY(MIN('Report load times'[Timestamp]))
)
 & " to " & 
DATE(
  YEAR(MAX('Report load times'[Timestamp])),
  MONTH(MAX('Report load times'[Timestamp])),
  DAY(MAX('Report load times'[Timestamp]))
))
```



```dax
P-25 7d = CALCULATE([P-25], ALL(Dates), DATESINPERIOD('Report load times'[Date], max('Report load times'[Date]), -7, DAY)) + 0
```



```dax
P-90 = PERCENTILE.INC('Report load times'[loadTime], 0.9) + 0
```



```dax
P-75 = PERCENTILE.INC('Report load times'[loadTime], 0.75) + 0
```



```dax
P-75 7d = CALCULATE([P-75], ALL(Dates), DATESINPERIOD('Report load times'[Date], max('Report load times'[Date]), -7, DAY)) + 0
```



```dax
Total page views = COUNTROWS('Report page views')
```



```dax
Total page users = DISTINCTCOUNT('Report page views'[UserKey])
```



```dax
Weekly Viewers = 
    var sop = CALCULATE(MIN('Dates'[Date]), ALL('Dates'), Dates[DoW] = 1)
    var eop = CALCULATE(MAX('Dates'[Date]), ALL('Dates'), Dates[DoW] = 7)
return
    IF(AND(MIN('Dates'[Date]) >= sop, MAX('Dates'[Date]) <= eop),
    CALCULATE(DISTINCTCOUNT('Report views'[UserKey]), DATESBETWEEN(Dates[Date], Min(Dates[fDoW]), MAX(Dates[lDoW]))),
    BLANK())
```



```dax
Weekly Views = 
    var sop = CALCULATE(MIN('Dates'[Date]), ALL('Dates'), Dates[DoW] = 1)
    var eop = CALCULATE(MAX('Dates'[Date]), ALL('Dates'), Dates[DoW] = 7)
return
    IF(AND(MIN('Dates'[Date]) >= sop, MAX('Dates'[Date]) <= eop),
    CALCULATE(COUNTROWS('Report views'), DATESBETWEEN(Dates[Date], Min(Dates[fDoW]), MAX(Dates[lDoW]))),
    BLANK())
```



```dax
P-10 trend = 
var numberOfDays = DATEDIFF(MIN('Report views'[Date]), MAX('Report views'[Date]),DAY) + 1
var periodLength = INT(numberOfDays/2) - 1
var firstPeriod = CALCULATE([P-10], DATESBETWEEN('Report load times'[Date], MIN('Report load times'[Date]), MIN('Report load times'[Date]) + periodLength))
var secondPeriod = CALCULATE([P-10], DATESBETWEEN('Report load times'[Date], MAX('Report load times'[Date]) - periodLength, MAX('Report load times'[Date])))
return DIVIDE(secondPeriod - firstPeriod, firstPeriod) + 0 * -1
```



```dax
P-25 trend = 
var numberOfDays = DATEDIFF(MIN('Report views'[Date]), MAX('Report views'[Date]),DAY) + 1
var periodLength = INT(numberOfDays/2) - 1
var firstPeriod = CALCULATE([P-25], DATESBETWEEN('Report load times'[Date], MIN('Report load times'[Date]), MIN('Report load times'[Date]) + periodLength))
var secondPeriod = CALCULATE([P-25], DATESBETWEEN('Report load times'[Date], MAX('Report load times'[Date]) - periodLength, MAX('Report load times'[Date])))
return DIVIDE(secondPeriod - firstPeriod, firstPeriod) + 0 * -1
```



```dax
P-75 trend = 
var numberOfDays = DATEDIFF(MIN('Report views'[Date]), MAX('Report views'[Date]),DAY) + 1
var periodLength = INT(numberOfDays/2) - 1
var firstPeriod = CALCULATE([P-75], DATESBETWEEN('Report load times'[Date], MIN('Report load times'[Date]), MIN('Report load times'[Date]) + periodLength))
var secondPeriod = CALCULATE([P-75], DATESBETWEEN('Report load times'[Date], MAX('Report load times'[Date]) - periodLength, MAX('Report load times'[Date])))
return DIVIDE(secondPeriod - firstPeriod, firstPeriod) + 0 * -1
```



```dax
P-90 trend = 
var numberOfDays = DATEDIFF(MIN('Report views'[Date]), MAX('Report views'[Date]),DAY) + 1
var periodLength = INT(numberOfDays/2) - 1
var firstPeriod = CALCULATE([P-90], DATESBETWEEN('Report load times'[Date], MIN('Report load times'[Date]), MIN('Report load times'[Date]) + periodLength))
var secondPeriod = CALCULATE([P-90], DATESBETWEEN('Report load times'[Date], MAX('Report load times'[Date]) - periodLength, MAX('Report load times'[Date])))
return DIVIDE(secondPeriod - firstPeriod, firstPeriod) + 0 * -1
```



```dax
Report view share = DIVIDE(COUNTROWS('Report views'), CALCULATE(COUNTROWS('Report views'), ALL('Report views')), 0)
```



```dax
Workspace report days with usage = SUM('Workspace reports'[Days with usage]) + 0
```



```dax
Workspace viewed reports = DISTINCTCOUNT('Workspace views'[ReportId]) + 0
```



```dax
Page views = COUNTROWS('Report page views') + 0
```


## Table: Report rank

### Measures:


```dax
Total Org Report Count = IF(COUNTROWS('Report rank') = 0, 0, FIRSTNONBLANK('Report rank'[TotalReportCount], 0))
```


## Table: Report page views

### Calculated Columns:


```dax
Date = DATE(YEAR('Report page views'[Timestamp]), MONTH('Report page views'[Timestamp]), DAY('Report page views'[Timestamp]))
```


## Table: Report load times

### Calculated Columns:


```dax
loadTime = DATEDIFF('Report load times'[StartTime], 'Report load times'[EndTime], SECOND)
```



```dax
Date = DATE(YEAR('Report load times'[Timestamp]), MONTH('Report load times'[Timestamp]), DAY('Report load times'[Timestamp]))
```



```dax
Browser = 
SWITCH(TRUE(),
        LEFT('Report load times'[DeviceBrowserVersion], 4) = "Edge", "Edge Classic",
        LEFT('Report load times'[DeviceBrowserVersion], 3) = "Edg", "Edge Chromium",
        LEFT('Report load times'[DeviceBrowserVersion], 21) = "Chrome Mobile Webview", "Chrome Mobile Webview",
        LEFT('Report load times'[DeviceBrowserVersion], 13) = "Chrome Mobile", "Chrome Mobile",
        LEFT('Report load times'[DeviceBrowserVersion], 6) = "Chrome", "Chrome",
        LEFT('Report load times'[DeviceBrowserVersion], 7) = "Firefox", "Firefox",
        LEFT('Report load times'[DeviceBrowserVersion], 17) = "Internet Explorer", "Internet Explorer",
        LEFT('Report load times'[DeviceBrowserVersion], 13) = "Mobile Safari", "Mobile Safari",
        LEFT('Report load times'[DeviceBrowserVersion], 3) = "Safari", "Safari",
        LEFT('Report load times'[DeviceBrowserVersion], 8) = "Electron", "Electron",
        LEFT('Report load times'[DeviceBrowserVersion], 16) = "Samsung Internet", "Samsung Internet",
        "other")
```


## Table: Dates


```dax

    var startDate = TODAY() - 31
    var lastRefreshDate = DATEVALUE(MAX('Refresh Stats'[Last Refresh]))
return
    CALENDAR(startDate, IF(OR(ISBLANK(lastRefreshDate), lastRefreshDate <= startDate), TODAY(), lastRefreshDate))
```


### Calculated Columns:


```dax
DoW = WEEKDAY('Dates'[Date])
```



```dax
fDoW = 'Dates'[Date] - 'Dates'[DoW] + 1
```



```dax
lDoW = 'Dates'[fDoW] + 6
```


## Table: Workspace views


```dax
SUMMARIZE('Report views', 'Report views'[ReportId], 'Report views'[UserKey], 'Report views'[UserId], 'Report views'[DistributionMethod], 'Report views'[ConsumptionMethod], "Views", [Report views])
```


### Calculated Columns:


```dax
UniqueUser = IF('Workspace views'[UserId] = "Unnamed User", "Unnamed User " & 'Workspace views'[UserKey], 'Workspace views'[UserId])
```


## Table: Workspace reports


```dax
ADDCOLUMNS(DISTINCT(Reports[ReportGuid]), 
                            "trend", [Workspace view trend], 
                            "active days", [Workspace active days per report])
```


### Measures:


```dax
IsSelectedReport = IF(SELECTEDVALUE('Workspace reports'[ReportGuid]) = SELECTEDVALUE(Reports[ReportGuid]), 1, 0)
```


### Calculated Columns:


```dax
ReportName = LOOKUPVALUE(Reports[ReportName], Reports[ReportGuid], 'Workspace reports'[ReportGuid])
```



```dax
IsUsageMetricsReportWS = LOOKUPVALUE(Reports[IsUsageMetricsReport], Reports[ReportGuid], 'Workspace reports'[ReportGuid])
```


## Table: Users


```dax
SUMMARIZE('Report views', 'Report views'[UserId], 'Report views'[UserKey])
```


### Calculated Columns:


```dax
UserGuid = LOOKUPVALUE(Users_ReportPageView[UserId], Users_ReportPageView[UserKey], Users[UserKey], Users[UserID])
```



```dax
UniqueUser = IF(Users[UserId] = "Unnamed User", "Unnamed User " & Users[UserKey], Users[UserId])
```


## Table: Users_ReportPageView


```dax
SUMMARIZE('Report page views', 'Report page views'[UserId], 'Report page views'[UserKey])
```

