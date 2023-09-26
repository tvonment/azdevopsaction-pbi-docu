



# DAX

|Dataset|[Emissions Impact Dashboard for Microsoft 365](./../Emissions-Impact-Dashboard-for-Microsoft-365.md)|
| :--- | :--- |
|Workspace|[Emissions Impact Dashboard for Microsoft 365](../../Workspaces/Emissions-Impact-Dashboard-for-Microsoft-365.md)|

## Table: Slider


```dax
GENERATESERIES(0, 1.01, 0.05)
```


### Measures:


```dax
Slider Value = SELECTEDVALUE('Slider'[Slider])
```


## Table: MTDMeasures


```dax
Row("Column", BLANK())
```


### Measures:


```dax
Updated = 
Var updated_date = FORMAT(LASTDATE(LastRefreshTable[LastRefresh]),"mmm dd, yyyy")
Return
CONCATENATE("Most recent data available:  ",updated_date)
```



```dax
Actual Emissions = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope1" || 'TenantEmission'[ScopeName] = "Scope2" || 'TenantEmission'[ScopeName] = "Scope3" || 'TenantEmission'[ScopeName] = "Scope2Loc")
```



```dax
Total Emissions Scope 12 = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope1" || 'TenantEmission'[ScopeName] = "Scope2")

return emission
//if (emission=BLANK(),0,emission)
```



```dax
Emissions123 MTD P = 

var p = TOTALMTD([Total Emissions Scope 123], PREVIOUSMONTH(LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 123])))
return p





```



```dax
Comparison_MTDEmissionsScope1,2&3 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions123 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions123 MTD P]
var perdif = ABS(DIVIDE ((latestmonth-prevmonth),prevmonth,0))*100
var p= round(perdif,0)&"%"&" compared to previous month"
var f1= if(perdif=BLANK(),"0% compared to previous month",p)
Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", f1)
//if(maxmonth<=CALCULATE(MIN(GHGEmission[DateId Year]),ALL(DimDate[Date].[Year]))," ",f1)))
```



```dax
Emissions123 MTD = 

var p = TOTALMTD([Total Emissions Scope 123], LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 123]))
return p
```



```dax
Total Emissions Scope 123 = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] <> "Scope2Loc")
return emission
```



```dax
Arrow_Comparison_MTDEmissionsScope1,2&3 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions123 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions123 MTD P]
var differencevalue = latestmonth - prevmonth
Var arrow = If (differencevalue >0,UNICHAR(9650),UNICHAR(9660))

Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", arrow)
```



```dax
Emissions12 MTD = 

var p = TOTALMTD([Total Emissions Scope 12], LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 12]))
return p
```



```dax
Emissions12 MTD P = 

var p = TOTALMTD([Total Emissions Scope 12], PREVIOUSMONTH(LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 12])))
return p

```



```dax
Comparison_MTDEmissionsScope1,2 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions12 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions12 MTD P]
var perdif = ABS(DIVIDE ((latestmonth-prevmonth),prevmonth,0))*100
var p= round(perdif,0)&"%"&" compared to previous month"
var f1= if(perdif=BLANK(),"0% compared to previous month",p)
Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", f1)
//if(maxmonth<=CALCULATE(MIN(GHGEmission[DateId Year]),ALL(DimDate[Date].[Year]))," ",f1)))
```



```dax
Arrow_Comparison_MTDEmissionsScope1,2 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions12 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions12 MTD P]
var differencevalue = latestmonth - prevmonth
Var arrow = If (differencevalue >0,UNICHAR(9650),UNICHAR(9660))

Return
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", arrow)
```



```dax
Total Usage = 
VAR usage = Calculate(SUM(TenantUsage[NumberOfUsers]), TenantUsage[ApplicationName]="M365")
return usage
```



```dax
Total Carbon Intensity per user = 
var intensity = (DIVIDE([Total Emissions Scope 123], [Total Usage], 0)) * 1000000

return intensity

```



```dax
Intensity MTD = 

var p = TOTALMTD([Total Carbon Intensity per user], LASTNONBLANK(DateTable[Dates], [Total Carbon Intensity per user]))
return p
```



```dax
Intensity MTD P = 

var p = TOTALMTD([Total Carbon Intensity per user], PREVIOUSMONTH(LASTNONBLANK(DateTable[Dates], [Total Carbon Intensity per user])))
return p





```



```dax
Comparison_MTD_Intensity = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Intensity MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Intensity MTD P]
var perdif = ABS(DIVIDE ((latestmonth-prevmonth),prevmonth,0))*100
var p= round(perdif,0)&"%"&" compared to previous month"
var f1= if(perdif=BLANK(),"0% compared to previous month",p)
Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", f1)
//if(maxmonth<=CALCULATE(MIN(GHGEmission[DateId Year]),ALL(DimDate[Date].[Year]))," ",f1)))
```



```dax
Arrow_Comparison_MTD_Intensity = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Intensity MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Intensity MTD P]
var differencevalue = latestmonth - prevmonth
Var arrow = If (differencevalue >0,UNICHAR(9650),UNICHAR(9660))

Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", arrow)
```



```dax
Usage MTD = 

var p = TOTALMTD([Total Usage], LASTNONBLANK(DateTable[Dates], [Total Usage]))
return p
```



```dax
Usage MTD P = 

var p = TOTALMTD([Total Usage], PREVIOUSMONTH(LASTNONBLANK(DateTable[Dates], [Total Usage])))
return p





```



```dax
Comparison_MTD_Usage = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Usage MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Usage MTD P]
var perdif = ABS(DIVIDE ((latestmonth-prevmonth),prevmonth,0))*100
var p= round(perdif,0)&"%"&" compared to previous month"
var f1= if(perdif=BLANK(),"0% compared to previous month",p)
Return 
if(maxmonth <= CALCULATE(MIN(TenantUsage[Date]), ALL(DateTable[Dates])), " ", f1)
//if(maxmonth<=CALCULATE(MIN(GHGEmission[DateId Year]),ALL(DimDate[Date].[Year]))," ",f1)))
```



```dax
Arrow_Comparison_MTD_Usage = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Usage MTD], DateTable[Dates] = maxmonth)
var prevmonth = round([Usage MTD P],1)
var differencevalue = latestmonth - prevmonth
Var arrow = If (differencevalue >0,UNICHAR(9650),UNICHAR(9660))

Return 
if(maxmonth <= CALCULATE(MIN(TenantUsage[Date]), ALL(DateTable[Dates])), " ", arrow)
```



```dax
HighestEmissionService = 
var service = 
CALCULATE(SELECTEDVALUE(DimApplication[ApplicationName]),
TOPN(1, SUMMARIZE(DimApplication, DimApplication[ApplicationName], "Total Emissions", [Total Emissions Scope 123]), [Total Emissions Scope 123], DESC))
return if(service==BLANK(), "No Data Available", service)


```



```dax
Total Emissions Scope 123 _KPI = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] <> "Scope2Loc")

return 
if(emission = BLANK(), 0, emission)
```



```dax
Total Emissions Scope 12_KPI = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope1" || 'TenantEmission'[ScopeName] = "Scope2")

return
if (emission=BLANK(),0,emission)
```



```dax
Total Carbon Intensity_KPI = 
var usageperthousand = DIVIDE([Total Usage], 1000, 0)
var intensity = DIVIDE([Total Emissions Scope 123], usageperthousand, 0)

return 
if(intensity = BLANK(), 0, intensity)
```



```dax
Total Usage_KPI = 
VAR usage = [Total Usage]

return 
if(usage = BLANK(), 0, usage)
```



```dax
Comparison_Info_tooltip_text = 

var metricname = SELECTEDVALUE(MetricToolTips[MetricName])

Var descrition1 = 
If(metricname="Carbon Emissions 123 MOM% comparison"," Your carbon emissions changed by ",If(metricname="Carbon Emissions 12 MOM% comparison"," Your carbon emissions changed by ",If(metricname="Carbon Intensity MOM% comparison"," Your carbon intensity changed by ",if(metricname="Carbon Emissions for highest service QOQ% comparison"," From last quarter " & [HighestEmissionService] & " changed by ", if(metricname="Carbon Emissions 1 MOM% comparison"," Your carbon emissions changed by ", if(metricname="Carbon Emissions 2 MOM% comparison"," Your carbon emissions changed by ", if(metricname="Carbon Emissions 3 MOM% comparison"," Your carbon emissions changed by " )))))))

var measurevalue = 
If(metricname="Carbon Emissions 123 MOM% comparison",[Comparison_MTDEmissionsScope1,2&3_tooltip],If(metricname="Carbon Emissions 12 MOM% comparison",[Comparison_MTDEmissionsScope1,2_tooltip],if(metricname="Carbon Intensity MOM% comparison",[Comparison_MTD_Intensity_tooltip],if(metricname="Carbon Emissions for highest service QOQ% comparison",[Comparison_QTDEmissionsScope1,2&3_tooltip], If(metricname="Carbon Emissions 1 MOM% comparison",[Comparison_MTDEmissionsScope1_tooltip], If(metricname="Carbon Emissions 2 MOM% comparison",[Comparison_MTDEmissionsScope2_tooltip], If(metricname="Carbon Emissions 3 MOM% comparison",[Comparison_MTDEmissionsScope3_tooltip])))))))
 
 var measurevalue2 = if(measurevalue=BLANK(),0,measurevalue)

//Var reasoncodelogic = 
//CALCULATE(MIN(InfoBubbleToolTips[Reason1]),FILTER(InfoAboutToolTips,InfoAboutToolTips[Metric]=metricname))

Var descrition2 = 
If(metricname="Carbon Emissions 123 MOM% comparison"," this past month.",If(metricname="Carbon Emissions 12 MOM% comparison"," this past month.",if(metricname="Carbon Intensity MOM% comparison"," over the past month. ", If(metricname="Carbon Emissions 1 MOM% comparison"," this past month.", If(metricname="Carbon Emissions 2 MOM% comparison"," this past month.", If(metricname="Carbon Emissions 3 MOM% comparison"," this past month.", if(metricname="Carbon Emissions for highest service QOQ% comparison", ". ")))))))

Return 
descrition1 & round(measurevalue2*100,2) & "%" &descrition2 &unichar(10) 
```



```dax
Comparison_MTDEmissionsScope1,2&3_tooltip = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions123 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions123 MTD P]
var perdif = DIVIDE ((latestmonth-prevmonth),prevmonth,0)

Return perdif
```



```dax
Comparison_MTDEmissionsScope1,2_tooltip = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions12 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions12 MTD P]
var perdif = DIVIDE ((latestmonth-prevmonth),prevmonth,0)

Return perdif

```



```dax
Comparison_MTD_Intensity_tooltip = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Intensity MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Intensity MTD P]
var perdif = DIVIDE ((latestmonth-prevmonth),prevmonth,0)

Return perdif

```



```dax
Total Carbon Intensity_1000 = 
var usageperthousand = DIVIDE([Total Usage], 1000, 0)
var intensity = DIVIDE([Total Emissions Scope 123], usageperthousand, 0)

return intensity

```



```dax
Total Emissions Scope 123_PrepReport = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] <> "Scope2Loc")

return emission




```



```dax
Total Emissions Scope 123 for map visual = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] <> "Scope2Loc",  'TenantEmission'[Emissions] > 0.001)

return emission
```



```dax
Total Emissions Scope 1 _KPI = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope1")

return 
if(emission = BLANK(), 0, emission)
```



```dax
Total Emissions Scope 2 _KPI = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope2")

return 
if(emission = BLANK(), 0, emission)
```



```dax
Total Emissions Scope 3 _KPI = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope3")

return 
if(emission = BLANK(), 0, emission)
```



```dax
Total Emissions Scope 1 = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope1" )

return emission
```



```dax
Total Emissions Scope 2 = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope2" )

return emission
```



```dax
Total Emissions Scope 3 = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope3" )

return emission
```



```dax
Emissions1 MTD = 

var p = TOTALMTD([Total Emissions Scope 1], LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 1]))
return p
```



```dax
Emissions2 MTD = 

var p = TOTALMTD([Total Emissions Scope 2], LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 2]))
return p
```



```dax
Emissions3 MTD = 

var p = TOTALMTD([Total Emissions Scope 3], LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 3]))
return p
```



```dax
Emissions1 MTD P = 

var p = TOTALMTD([Total Emissions Scope 1], PREVIOUSMONTH(LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 1])))
return p
```



```dax
Emissions2 MTD P = 

var p = TOTALMTD([Total Emissions Scope 2], PREVIOUSMONTH(LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 2])))
return p
```



```dax
Emissions3 MTD P = 

var p = TOTALMTD([Total Emissions Scope 3], PREVIOUSMONTH(LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 3])))
return p
```



```dax
Comparison_MTDEmissionsScope1 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions1 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions1 MTD P]
var perdif = ABS(DIVIDE ((latestmonth-prevmonth),prevmonth,0))*100
var p= round(perdif,0)&"%"&" compared to previous month"
var f1= if(perdif=BLANK(),"0% compared to previous month",p)
Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", f1)
```



```dax
Arrow_Comparison_MTDEmissionsScope1 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions1 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions1 MTD P]
var differencevalue = latestmonth - prevmonth
Var arrow = If (differencevalue >0,UNICHAR(9650),UNICHAR(9660))

Return
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", arrow)
```



```dax
Comparison_MTDEmissionsScope2 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions2 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions2 MTD P]
var perdif = ABS(DIVIDE ((latestmonth-prevmonth),prevmonth,0))*100
var p= round(perdif,0)&"%"&" compared to previous month"
var f1= if(perdif=BLANK(),"0% compared to previous month",p)
Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", f1)
```



```dax
Comparison_MTDEmissionsScope3 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions3 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions3 MTD P]
var perdif = ABS(DIVIDE ((latestmonth-prevmonth),prevmonth,0))*100
var p= round(perdif,0)&"%"&" compared to previous month"
var f1= if(perdif=BLANK(),"0% compared to previous month",p)
Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", f1)
```



```dax
Arrow_Comparison_MTDEmissionsScope2 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions2 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions2 MTD P]
var differencevalue = latestmonth - prevmonth
Var arrow = If (differencevalue >0,UNICHAR(9650),UNICHAR(9660))

Return
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", arrow)
```



```dax
Arrow_Comparison_MTDEmissionsScope3 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions3 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions3 MTD P]
var differencevalue = latestmonth - prevmonth
Var arrow = If (differencevalue >0,UNICHAR(9650),UNICHAR(9660))

Return
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", arrow)
```



```dax
Comparison_MTDEmissionsScope1_tooltip = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions1 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions1 MTD P]
var perdif = DIVIDE ((latestmonth-prevmonth),prevmonth,0)

Return perdif

```



```dax
Comparison_MTDEmissionsScope2_tooltip = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions2 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions2 MTD P]
var perdif = DIVIDE ((latestmonth-prevmonth),prevmonth,0)

Return perdif

```



```dax
Comparison_MTDEmissionsScope3_tooltip = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var latestmonth = CALCULATE([Emissions3 MTD], DateTable[Dates] = maxmonth)
var prevmonth = [Emissions3 MTD P]
var perdif = DIVIDE ((latestmonth-prevmonth),prevmonth,0)

Return perdif

```



```dax
Company Name = 
var orgname = MIN(TenantEmission[TenantName])
return
CONCATENATE("Company Name: ", orgname)
```



```dax
ID = 
var enroll = min(TenantEmission[TenantId])

return 
CONCATENATE("Tenant ID: ",enroll)
```



```dax
Percentagetotals_measure = 
var emissionvalue = [Total Emissions Scope 123]//SUMX(filter(TenantEmission, TenantEmission[ScopeName]<> "Scope2Loc"),  TenantEmission[Emissions])
var totalemissions = CALCULATE([Total Emissions Scope 123], ALLSELECTED(TenantEmission))
return 
DIVIDE (emissionvalue, totalemissions,0)
```



```dax
Percentage_totals_format = 
var percentagetotal = [Percentagetotals_measure]*100

return
 if(percentagetotal<1, "<1%", CONCATENATE(round(percentagetotal, 2), "%")
)
```



```dax
Total Scope 2 Carbon Intensity per user = 
//var usageperthousand = DIVIDE([Total Usage], 1000, 0)
var intensity = (DIVIDE([Total Emissions Scope 2], [Total Usage], 0)) * 1000000

return intensity

```



```dax
Total Scope 2 Carbon intensity per user_recent month text = 
var emission = [Total Scope 2 Carbon intensity per user_recent month]

return CONCATENATE(round(emission,2), " grams per user")
```



```dax
Miles_driven_Emissions = 
var miles = Divide([Total Carbon intensity per user_recent month], 404, 0)
var km = miles * 1.60934
return "Driving " & round(miles,3) &" miles (equivalent to " & round(km,3) & " kilometers) in a gas-powered car"
```



```dax
Total Scope 2 Carbon intensity per user_recent month = 
var recentmonth = LASTDATE(all('TenantEmission'[Date]))
var emission = CALCULATE([Total Scope 2 Carbon Intensity per user], all(DateTable),DateTable[Dates] = recentmonth)

return 
round(emission,2)
```



```dax
Trees_carbon sequestered = 
var carbon_sequestered = Divide([Total Carbon intensity per user_recent month], 60000, 0)

return "Carbon sequestered by " & round(carbon_sequestered,3) & " trees"
```



```dax
Phones charged = 
var charged = Divide([Total Carbon intensity per user_recent month], 8, 0)

return "Charging " & roundup(charged,0) & " smartphones"
```



```dax
Total Scope 2 Carbon Intensity per user _%diff = 
var maxyr = LASTDATE(All(TenantEmission[Date]))
var minyr = DATEADD(maxyr,-3,MONTH)
var c = [Total Scope 2 Carbon intensity per user_recent month]
var p = CALCULATE([Total Scope 2 Carbon Intensity per user], all(DateTable), DateTable[Dates] = minyr)
var perdiff = round(divide((c-p),p) *100,0)
return if(perdiff = BLANK()," ", CONCATENATE(perdiff," % from one year ago"))

```



```dax
Total LY Scope 2 Carbon Intensity per user_ly = 
var maxyr = LASTDATE(TenantEmission[Date])
var minyr = DATEADD(maxyr,-3,MONTH)
var c = CALCULATE([Total Scope 2 Carbon intensity per user], DateTable[Dates] = maxyr)
var p = CALCULATE([Total Scope 2 Carbon Intensity per user], all(DateTable), DateTable[Dates] = minyr)
var perdiff = (c-p)
return p

```



```dax
Total Emissions per Methodology = 
IF (
    SELECTEDVALUE ( ScopeMethodology[Methodology] ) = "Market-based",
    CALCULATE (
        SUM ( TenantEmission[Emissions] ),
        FILTER (
            TenantEmission,
            TenantEmission[ScopeName] IN { "Scope1", "Scope2", "Scope3" }
        )
    ),
    IF (
        SELECTEDVALUE ( ScopeMethodology[Methodology] ) = "Location-based",
        CALCULATE (
            SUM ( TenantEmission[Emissions] ),
            FILTER (
                TenantEmission,
                TenantEmission[ScopeName] IN { "Scope1", "Scope2Loc", "Scope3" }
            )
        )
    )
)

```



```dax
Percentagetotals_measure_scopecategory = 
var emissionvalue = [Total Emissions per Methodology]//SUMX(filter(TenantEmission, TenantEmission[ScopeName]<> "Scope2Loc"),  TenantEmission[Emissions])
var totalemissions = CALCULATE([Total Emissions per Methodology], ALLSELECTED(TenantEmission))
return 
DIVIDE (emissionvalue, totalemissions,0)
```



```dax
Percentage_totals_scopecategory_format = 
var percentagetotal = [Percentagetotals_measure_scopecategory]*100

return
 if(percentagetotal<1, "<1%", CONCATENATE(round(percentagetotal, 2), "%")
)
```



```dax
Total Emissions Scope 2 per Methodology = 
IF (
    SELECTEDVALUE ( ScopeMethodology[Methodology] ) = "Market-based",
    CALCULATE (
        SUM ( TenantEmission[Emissions] ),
        FILTER (
            TenantEmission,
            TenantEmission[ScopeName] = "Scope2"
        )
    ),
    IF (
        SELECTEDVALUE ( ScopeMethodology[Methodology] ) = "Location-based",
        CALCULATE (
            SUM ( TenantEmission[Emissions] ),
            FILTER (
                TenantEmission,
                TenantEmission[ScopeName] = "Scope2Loc"
            )
        )
    )
)

```



```dax
Total Scope 2 Carbon Intensity per user_Methodology = 
//var usageperthousand = DIVIDE([Total Usage], 1000, 0)
var intensity = (DIVIDE([Total Emissions Scope 2 per Methodology], [Total Usage], 0)) * 1000000

return intensity

```



```dax
Total Scope 2 Carbon intensity per user_recent month_methodology = 
var recentmonth = LASTDATE(all(('TenantEmission'[Date])))
var emission = CALCULATE([Total Scope 2 Carbon Intensity per user_Methodology], all(DateTable),DateTable[Dates] = recentmonth)

return round(emission,2)
```



```dax
Total Scope 2 Carbon intensity per user_recent month text_methodology = 
var emission = [Total Scope 2 Carbon intensity per user_recent month_methodology]

return CONCATENATE(round(emission,2), " grams per user")
```



```dax
Total Scope 2 Carbon Intensity per user _%diff_methodology = 
var maxyr = LASTDATE(All(TenantEmission[Date]))
var minyr = DATEADD(maxyr,-3,MONTH)
var c = [Total Scope 2 Carbon intensity per user_recent month_methodology]
var p = CALCULATE([Total Scope 2 Carbon Intensity per user_Methodology], all(DateTable), DateTable[Dates] = minyr)
var perdiff = round(divide((c-p),p) *100,0)
return if(perdiff = BLANK()," ", CONCATENATE(perdiff," % from one year ago"))

```



```dax
Tenant_name_header = 
var tenantname = MIN(TenantEmission[TenantName])
return
CONCATENATE("Currently displaying data for the following tenant: ", tenantname)



```



```dax
Total Carbon intensity per user_recent month = 
var recentmonth = LASTDATE(all('TenantEmission'[Date]))
var emission = CALCULATE([Total Carbon Intensity per user], all(DateTable), DateTable[Dates] = recentmonth)

return 
round(emission,2)
```



```dax
Total Carbon intensity per user_recent month text = 
var emission = [Total Carbon intensity per user_recent month]

return CONCATENATE(round(emission,0), " grams per user")
```



```dax
Total Carbon Intensity per user _%diff = 
var maxyr = LASTDATE(All(TenantEmission[Date]))
var minyr = DATEADD(maxyr,-11,MONTH)
var testing_m = MONTH(DATE(2022,7,1)) - MONTH(maxyr) 
var testing_qtym = IF(testing_m>12,12,testing_m)
var c = [Total Carbon intensity per user_recent month]
var p = CALCULATE([Total Carbon Intensity per user], all(TenantEmission[Date]),all(DateTable),DateTable[Dates] = minyr)
var diff = c-p
var perdiff = round(divide((c-p),p) *100,0)
return  if(perdiff = BLANK()," ", if(diff>=0, "+" & perdiff &"% from " & testing_qtym & " months ago", perdiff &"% from " & testing_qtym & " months ago" ))

```



```dax
Optout request url ppe = 
var tenantid = MIN(TenantEmission[TenantId])
return
CONCATENATE("https://iks-powerbi-ppe.ideas.microsoft.com/optinout/index.html?id=", tenantid)

```



```dax
Optout request url prod = 
var tenantid = MIN(TenantEmission[TenantId])
return
CONCATENATE("https://iks-powerbi.ideas.microsoft.com/optinout/index.html?id=", tenantid) 

```



```dax
Measure = CALCULATE ( MIN ( MTDMeasures[Total Emissions Scope 123] ) )
```



```dax
Measure 2 = 
var emission = MIN(CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] <> "Scope2Loc"))
return emission
```



```dax
Total Emissions Scope 23 = 
var emission = CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] = "Scope3" || 'TenantEmission'[ScopeName] = "Scope2") 

return emission
//if (emission=BLANK(),0,emission)
```


## Table: DateTable

### Calculated Columns:


```dax
Quarter Name = "Qtr " & DateTable[Quarter]
```


## Table: QTDMeasures


```dax
Row("Column", BLANK())
```


### Measures:


```dax
Emissions123 QTD = 

var p = TOTALQTD([Total Emissions Scope 123], LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 123]))
return p
```



```dax
Emissions123 QTD P = 

var p = TOTALQTD([Total Emissions Scope 123], PREVIOUSQUARTER(LASTNONBLANK(DateTable[Dates], [Total Emissions Scope 123])))
return p





```



```dax
Comparison_QTDEmissionsScope1,2&3 = 

var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var service = [HighestEmissionService]
var latestmonth = CALCULATE([Emissions123 QTD], DateTable[Dates] = maxmonth, DimApplication[ApplicationName] = service)
var prevmonth = CALCULATE([Emissions123 QTD P], DimApplication[ApplicationName] = service)
VAR servicedifference = DIVIDE ((latestmonth-prevmonth),prevmonth)
var perdif = ABS(servicedifference)*100

var p= round(perdif,0)&"%"&" compared to previous quarter"
var f1= if(perdif=BLANK(),"0% compared to previous quarter",p)
Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", f1)

```



```dax
Arrow_Comparison_QTDEmissionsScope1,2&3 = 
var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var service = [HighestEmissionService]
var latestmonth = CALCULATE([Emissions123 QTD], DateTable[Dates] = maxmonth, DimApplication[ApplicationName] = service)
var prevmonth = ROUND(CALCULATE([Emissions123 QTD P], DimApplication[ApplicationName] = service),1)
var differencevalue = latestmonth - prevmonth
Var arrow = If (differencevalue >0,UNICHAR(9650),UNICHAR(9660))

Return 
if(maxmonth <= CALCULATE(MIN('TenantEmission'[Date]), ALL(DateTable[Dates])), " ", arrow)
```



```dax
Comparison_QTDEmissionsScope1,2&3_tooltip = 

var maxmonth = if(ISFILTERED(DateTable[Dates]), LASTDATE(DateTable[Dates]),0)
var minmonth = maxmonth-1
var service = [HighestEmissionService]
var latestmonth = CALCULATE([Emissions123 QTD], DateTable[Dates] = maxmonth, DimApplication[ApplicationName] = service)
var prevmonth = CALCULATE([Emissions123 QTD P], DimApplication[ApplicationName] = service)
VAR servicedifference = DIVIDE ((latestmonth-prevmonth),prevmonth,0)

Return servicedifference
```


## Table: EmissionSavingsMeasures


```dax
Row("Column", BLANK())
```


### Measures:


```dax
MTCO2e from on-premises alternative = 
VAR Onpremises =
     ((
         
            CALCULATE (
                SUM ( 'TenantEmission'[Emissions] ),
                FILTER (
                    'TenantEmission',
                    'TenantEmission'[ScopeName] = "Scope2Loc"
                        && 'TenantEmission'[ApplicationName] = "SharePoint"
                )
            )
                * SUMX (
                    FILTER (
                        EmissionsSavingsMultiplier,
                        EmissionsSavingsMultiplier[ApplicationName] = "SharePoint"
                    ),
                    EmissionsSavingsMultiplier[SavingsMultiplier]
                )
                + CALCULATE (
                     SUM ( 'TenantEmission'[Emissions] ),
                        FILTER (
                            'TenantEmission',
                            'TenantEmission'[ScopeName] = "Scope2Loc"
                            && 'TenantEmission'[ApplicationName] = "Exchange"
                    )
                )
                    * SUMX (
                        FILTER (
                            EmissionsSavingsMultiplier,
                        EmissionsSavingsMultiplier[ApplicationName] = "Exchange"
                    ),
                    EmissionsSavingsMultiplier[SavingsMultiplier]
                    )
                
                 
        
    )
        * ( 1 - SUM ( Slider[Slider] ) ))
        +
        (
         
            CALCULATE (
                SUM ( 'TenantEmission'[Emissions] ),
                FILTER (
                    'TenantEmission',
                    'TenantEmission'[ScopeName] = "Scope1"
                        && 'TenantEmission'[ApplicationName] = "SharePoint"
                )
            )
                * SUMX (
                    FILTER (
                        EmissionsSavingsMultiplier,
                        EmissionsSavingsMultiplier[ApplicationName] = "SharePoint"
                    ),
                    EmissionsSavingsMultiplier[SavingsMultiplier]
                )
                + CALCULATE (
                     SUM ( 'TenantEmission'[Emissions] ),
                        FILTER (
                            'TenantEmission',
                            'TenantEmission'[ScopeName] = "Scope1"
                            && 'TenantEmission'[ApplicationName] = "Exchange"
                    )
                )
                    * SUMX (
                        FILTER (
                            EmissionsSavingsMultiplier,
                        EmissionsSavingsMultiplier[ApplicationName] = "Exchange"
                    ),
                    EmissionsSavingsMultiplier[SavingsMultiplier]
                    )
               
               
        
    )
var prem = if(Onpremises=BLANK(),0,Onpremises)

RETURN 
   

switch((true),
selectedvalue('Efficiency sort'[Efficiency])="Low" || selectedvalue('Efficiency sort'[Efficiency])="Medium" || selectedvalue('Efficiency sort'[Efficiency])="High",prem," ")



```



```dax
Location-based emissions = 
sumx(filter('TenantEmission','TenantEmission'[ScopeName] = "Scope2Loc" && (('TenantEmission'[ApplicationName] = "SharePoint") || ('TenantEmission'[ApplicationName] = "Exchange"))), 'TenantEmission'[Emissions] ) + sumx(filter('TenantEmission','TenantEmission'[ScopeName] = "Scope1" && (('TenantEmission'[ApplicationName] = "SharePoint") || ('TenantEmission'[ApplicationName] = "Exchange"))),'TenantEmission'[Emissions])
```



```dax
MTCO2e saved from Microsoft efficiencies = 
var negreduction= ([MTCO2e from on-premises alternative]-[Location-based emissions])* -1
return 
switch((true),
selectedvalue('Efficiency sort'[Efficiency])="Low" || selectedvalue('Efficiency sort'[Efficiency])="Medium" || selectedvalue('Efficiency sort'[Efficiency])="High",negreduction," ")
```



```dax
MTCO2e emissions from switch to Exchange Online and Sharepoint Online = 
var marketbased=
sumx(filter('TenantEmission','TenantEmission'[ScopeName] = "Scope2"&& (('TenantEmission'[ApplicationName] = "SharePoint") || ('TenantEmission'[ApplicationName] = "Exchange"))),'TenantEmission'[Emissions]) + sumx(filter('TenantEmission','TenantEmission'[ScopeName] = "Scope1" && (('TenantEmission'[ApplicationName] = "SharePoint") || ('TenantEmission'[ApplicationName] = "Exchange"))),'TenantEmission'[Emissions])
var market= if(ISBLANK(marketbased),0,marketbased)
return 
switch((true),
selectedvalue('Efficiency sort'[Efficiency])="Low" || selectedvalue('Efficiency sort'[Efficiency])="Medium" || selectedvalue('Efficiency sort'[Efficiency])="High",market," ") 
```



```dax
MTCO2e saved from Microsoft renewable energy purchases = 
var renewable = ([Location-based emissions]-[MTCO2e emissions from switch to Exchange Online and Sharepoint Online])*-1
return 
switch((true),
selectedvalue('Efficiency sort'[Efficiency])="Low" || selectedvalue('Efficiency sort'[Efficiency])="Medium" || selectedvalue('Efficiency sort'[Efficiency])="High",renewable," ")
```



```dax
Avoided emissions = 
[MTCO2e from on-premises alternative]-[MTCO2e emissions from switch to Exchange Online and Sharepoint Online]

```



```dax
Percent savings = [Avoided emissions] / [MTCO2e from on-premises alternative]
```



```dax
Carbon emissions saved (MTCO2e)% = 
var p = iferror(concatenate(round([Percent savings]*100,2),"%"),"%")
var q= if([Avoided emissions]=0,CONCATENATE(0,"%"),p)

return 
switch((true),
selectedvalue('Efficiency sort'[Efficiency])="Low" || selectedvalue('Efficiency sort'[Efficiency])="Medium" || selectedvalue('Efficiency sort'[Efficiency])="High",q," ")

```



```dax
Carbon emissions saved (MTCO2e) = 
var avoidedemissions = [Avoided emissions]
return 
switch((true),
selectedvalue('Efficiency sort'[Efficiency])="Low" || selectedvalue('Efficiency sort'[Efficiency])="Medium" || selectedvalue('Efficiency sort'[Efficiency])="High",avoidedemissions," ")
```



```dax
distance = [Avoided emissions] *2445
```



```dax
Distance in KM = [distance]*1.60934
```



```dax
Carbon emissions saved in driven distance = 
var distance=
switch(true(),
SELECTEDVALUE('Distance Convert Table'[Distance])="ML",[distance],
SELECTEDVALUE('Distance Convert Table'[Distance])="KM",[Distance in KM])
return
switch((true),
((selectedvalue('Efficiency sort'[Efficiency])="Low" || selectedvalue('Efficiency sort'[Efficiency])="Medium" || selectedvalue('Efficiency sort'[Efficiency])="High") && (SELECTEDVALUE('Distance Convert Table'[Distance])="ML" || SELECTEDVALUE('Distance Convert Table'[Distance])="KM")),distance," ")

```



```dax
Down_Triangle_Shape = UNICHAR(9660)
```



```dax
Dynamictitle = "MTCO2e emissions from switch to Exchange Online"
```



```dax
Dynamictext_Switch to M365 cloud = 
if(SELECTEDVALUE(DimApplication[ApplicationName]) = "Exchange", "MTCO2e emissions from switch to Exchange Online.", if(SELECTEDVALUE(DimApplication[ApplicationName])= "SharePoint", "MTCO2e emissions from switch to SharePoint Online.", "MTCO2e emissions from switch to Exchange Online and SharePoint Online."))
```


## Table: AccessibilityMeasures


```dax
Row("Column", BLANK())
```


### Measures:


```dax
Emissiondetails button = "Emissions details, page 2 of 9"
```



```dax
Dashboard button = "Dashboard, page 1 of 9"
```



```dax
Emissionsavings button = "Emissions savings, page 3 of 9"
```



```dax
GHGPreparaionReport button = "GHG Preparation report, page 4 of 9"
```



```dax
Usage button = "Usage report, page 5 of 9"
```



```dax
Calculationmetholdology button = "Calculation methodology, page 6 of 9"
```



```dax
Learnmore button = "Learn more, page 7 of 9"
```



```dax
Legalinformation button = "Legal information, page 8 of 9"
```



```dax
Legalinfo_pagetitle = 
"Legal Information 
This page is provided for your convenience as an overview of the terms and conditions that govern use of the Emissions Impact Dashboard for Microsoft 365 online service."
```



```dax
Alt_text_EmissionsScope1,2&3 = 
var e = [Total Emissions Scope 123 _KPI]
return CONCATENATE(e," ")
```



```dax
Alt_text_EmissionsScope1,2 = 
var e = [Total Emissions Scope 12_KPI]
return CONCATENATE(e," ")
```



```dax
Alt_text_Intensity = 
var e = [Total Carbon Intensity_KPI]
return CONCATENATE(e," ")
```



```dax
Alt_text_chart_nav = 
"To access the export function for the chart, press alt+shift+f10 and select export from the more options menu."
```



```dax
Alt_text_HighestService = 
var e = [HighestEmissionService]
return CONCATENATE(e," ")
```



```dax
Alt_Text_MTCO2e from on-premises alternative = 
var f=CONCATENATE([MTCO2e from on-premises alternative]," MTCO2e from on-premises alternative ")
return CONCATENATE(f," ")
```



```dax
Alt_Text_MTCO2e saved from Microsoft efficiencies = 
var f= CONCATENATE([MTCO2e saved from Microsoft efficiencies]," MTCO2e saved from Microsoft efficiencies") 
return CONCATENATE(f," ")
```



```dax
Alt_Text_MTCO2e saved from Microsoft renewable energy purchases = 
var f= CONCATENATE([MTCO2e saved from Microsoft renewable energy purchases]," MTCO2e saved from Microsoft renewable energy purchases")
return CONCATENATE(f," ")
```



```dax
Alt_Text_MTCO2e emissions from switch to Exchange and Sharepoint = 
var f=CONCATENATE([MTCO2e emissions from switch to Exchange Online and Sharepoint Online]," MTCO2e emissions from switch to Exchange Online and Sharepoint Online")
return CONCATENATE(f," ")
```



```dax
Alt_Text_Carbon emissions saved (MTCO2e)% = 
var f= CONCATENATE([Carbon emissions saved (MTCO2e)%]," Carbon emissions saved (MTCO2e)")
return CONCATENATE(f," ")
```



```dax
Alt_Text_Carbon emissions saved (MTCO2e) = 
var f=CONCATENATE([Carbon emissions saved (MTCO2e)]," Carbon emissions saved (MTCO2e)")
return CONCATENATE(f," ")
```



```dax
Alt_Text_Carbon emissions saved in driven distance = 
var distance = switch(true(),
SELECTEDVALUE('Distance Convert Table'[Distance])="ML",CONCATENATE([Carbon emissions saved in driven distance]," Carbon emissions saved in miles driven distance"),
SELECTEDVALUE('Distance Convert Table'[Distance])="KM",CONCATENATE([Carbon emissions saved in driven distance]," Carbon emissions saved in kilo meters driven distance"))
var f=
switch((true),
((selectedvalue('Efficiency sort'[Efficiency])="Low" || selectedvalue('Efficiency sort'[Efficiency])="Medium" || selectedvalue('Efficiency sort'[Efficiency])="High") && (SELECTEDVALUE('Distance Convert Table'[Distance])="ML" || SELECTEDVALUE('Distance Convert Table'[Distance])="KM")),distance,"  Both the Efficiency scale slicer and distance converter slicer should be selected with one option each for getting carbon emissions saved in driven distance")
return CONCATENATE(f," ")
```



```dax
Savings_Text1 = "  How to select your on-premises characteristics.Efficiency
  This calculation estimates emissions that result from your use of Exchange Online, and SharePoint Online services, savings relative to   provision of these same services at low, medium, and high efficiency on-premises deployments, and the renewable energy projects in  which Microsoft invests."
```



```dax
Savings_Text2 = "Low efficiency
Physical servers and direct attached storage in a small localized data center (500-1,999 square feet)."
```



```dax
Savings_Text3 = "Medium efficiency
Mix of physical and virtualized servers and attached, dedicated storage in a mid-tier internal data center (2,000-20,000 square feet)."
```



```dax
Savings_Text4 = "High efficiency
Virtualized servers and dedicated storage in a high-end internal data center (> 20,000 square feet).	"
```



```dax
Savings_Text5 = "
  The estimated emissions for your switch to the Microsoft cloud include Scope 1 and Scope 2 emissions only. The figure accounts for Microsoft’s renewable energy power purchases and includes energy used to transmit data over the internet.
  Renewable energy purchases
  Specify a percentage of renewable energy purchases used at your on-premises datacenter. If your on-premises datacenters reside in    multiple geographies, please specify an average of the geographies based on power consumption."
```



```dax
CDP_Text = "This Preparation report is based on preliminary data. Usage for emissions calculations may or may not equal your Microsoft usage for billing purposes. The findings, interpretations, and conclusions presented in the report are for informational purposes only.  This report is not intended and should not be used for legal compliance, marketing, or reporting purposes."
```



```dax
CalcMethod_Text1 = 
"Application:

This methodology is designed to calculate the carbon emissions associated with the use of Microsoft’s Microsoft 365 cloud computing resources. It covers Scope 1, 2, and 3 carbon emissions as calculated from manufacture, packaging, transportation, use, and end of life phases of datacenter hardware in all Microsoft owned and leased datacenters. The emissions and usage measured by this methodology are for Microsoft’s Microsoft 365 cloud only. The methodology is limited to emissions associated with usage of Exchange Online, SharePoint, OneDrive, Microsoft Teams, Word, Excel, PowerPoint and Outlook.



Calculation standards:

1. At Microsoft, we segment our greenhouse gas (GHG) emissions into three categories consistent with the Greenhouse Gas Protocol, a globally recognized standard for the calculation methodology and reporting of Greenhouse Gas (GHG) emissions: 

     a. Scope 1: Direct emissions – Emissions from stationary and mobile combustion, as well as process and fugitive emissions. 

     b. Scope 2: Indirect emissions - Emissions from the consumption of electricity, heat, or steam. 

     c. Scope 3: Other indirect emissions - Manufacturing and end-of-life emissions (supply chain related). The scope of this tool is scope 3 categories 1, 2, 4, 5, 9, and 12. 

2. Material related carbon emissions are based on ISO 14067:2018. Greenhouse gases — Carbon footprint of products — Requirements and guidelines for quantification.  

3. Operational emissions are based on ISO 14064-1:2006. Greenhouse gases — Part 1: Specification with guidance at the organization level for quantification and reporting of greenhouse gas emissions and removals. 

4. Verification and validation are based on ISO 14064-3:2006. Greenhouse gases – Part 3: Specification with guidance for the validation and verification of greenhouse gas assertions.  

 

The calculations represented in this tool are the product of a Life Cycle Evaluation that assessed the energy use associated with cloud computing operations, as well as the carbon emissions associated with the manufacture, transportation, and end of management of materials used in the Microsoft 365 Cloud. Both are outlined in the respective calculation section below.  

"
```



```dax
CalcMethod_Text2 = 
"Included emission sources

GHG emissions are classified into Scope 1, 2, and 3 emissions based on the level of control that an organization has over the sources of those emissions. Figure 1 shows these classifications graphically. 



Scope 1  

GHG emissions include emissions from the combustion of diesel fuel and fugitive emissions from the use of refrigerants for cooling of our data centers.  

 

Scope 2  

GHG emissions include emissions from direct power consumption used to power our global datacenters that are leased and owned by Microsoft. We invest in renewable energy Power Purchase Agreements (PPAs) globally, and plan on being powered by 100% renewable energy and eliminating fossil fuels from backup power by 2025. 

 

Scope 3 

GHG emissions include emissions that result from raw material extraction, product manufacturing and packaging, product transport, warehouse storage, and end-of-life (EOL) management (e.g. recycling, landfill, or composting) of hardware devices, such as servers and network equipment, used in our leased and owned datacenters. This tool includes the emissions from the manufacturing of the different parts and components that make up the hardware devices and its packaging, using material composition and emissions resulting

from all product life cycle stages. 

 

By their nature, scope 1, 2 and 3 emissions are all relative to the reporting entity; one company’s scope 1 emissions will be another’s scope 3 emissions. This tool reflects Microsoft’s combined scope 1, 2, and 3 emissions associated with the delivery of Microsoft 365 core cloud services. These emissions reflect a customer’s scope 3 emissions from the customer’s use of Microsoft cloud services. This is reflected in figure 2.  

 

Calculation Methodology 

As previously stated, Microsoft bases its calculation methodology on principles from the Greenhouse Gas Protocol and use of widely accepted ISO standards.  



Scope 1 and 2 

The full methodology for Scopes 1 and 2 is based on a Life Cycle evaluation conducted for a 2018 Microsoft study and published here: The Carbon Benefits of Cloud Computing: A Study on the Microsoft Cloud. 

 

The Scope 2 methodology calculates the energy and carbon impacts for each datacenter over time, taking into consideration a variety of factors such as datacenter and server efficiency, grid emission factors, renewable energy purchases, and infrastructure power usage."
```



```dax
CalcMethod_Text3 = 
"Scope 3  

The calculation of scope 3 emissions is best summarized by Figure 3. We start with the Life Cycle evaluation of materials used in our data center infrastructure and calculate carbon emissions by data center. We then can segment this sum based on customer usage of each data center.   



This methodology for Scope 3 emissions calculates the energy and carbon impacts for each data center over time, using the following: 

• Most common materials used to manufacture the IT infrastructure used in our data centers. 

• Most common parts that make up cloud infrastructure (hard disks, FPGA, steel racks). 

• Complete inventory of all the assets (as categorized by Microsoft Bill of Materials) in our data centers by region. 

• Carbon factors for cloud infrastructure across each life stage (raw material extraction, manufacture, packaging, transport, warehouse storage, usage, and end-of-life disposal). 



Calculation Variables: 

• Lifetime of equipment defaults to 6 years but users may change this variable based on end-of-life management options. 

• Emissions due to transportation are calculated as an average across shipments; however, default data may be replaced with actual transportation emissions data where available. 

• Critical infrastructure, such as the data center facility, is not included in the methodology at this time but may be added as data becomes available. 

• Embedded emissions for IT equipment not exclusively used by the modeled core cloud service, such as datacenter switches not located in the server racks, are not included in the methodology at this time. 

• Proxy usage measures are used in the place of true server-side compute and storage usage to apportion total carbon emissions, and may be replaced as data becomes available. 

• Validation of our methodology is third-party verified and the approach to scope 3 emissions is included in Microsoft’s full white paper published on www.microsoft.com/sustainability. 

 

Customer attributions and calculations for carbon emissions  

Emissions are allocated for a specific customer based on their actual usage – active usage and/or data storage - of Microsoft 365 core cloud services. The algorithm calculates a usage factor, which provides emissions per unit of customer usage in a specific Azure data center region. Emissions are then directly calculated based on this factor and mapped to the corresponding Microsoft 365 region. This process of attribution is shown graphically in Figure 3. 

 



"

```



```dax
Legal_Text = "Terms of Use

Your use of the Emissions Impact Dashboard for Microsoft 365 is governed by the Microsoft Terms of Use. 

 

Privacy Statement 

The Microsoft Privacy Statement describes the privacy policy and practices that govern your use of Microsoft's software and services, unless otherwise provided. The Microsoft Dynamics Insider Program Agreement or the Supplemental Preview Terms may specify a different privacy statement for the Emissions Impact Dashboard for Microsoft 365 online service. 

 

Third Party notice 

The Emissions Impact Dashboard for Microsoft 365 online service contains or interacts with the following third party materials (collectively Third Party Materials): 

 

• Public sector information from the UK Government Digital Services licensed under the Open Government Licence v1.0:  

https://www.nationalarchives.gov.uk/. 

• Ecoinvent database or any ecoinvent dataset for recycled content, recycling rates, and efficiencies from ecoinvent association under this end user license agreement: 

https://aka.ms/m365-emissions-ecoinvent. 

 

While Microsoft is not the original author of the Third-Party Materials, Microsoft licenses such Third Party Materials under the terms set forth in the Terms of Use. Unless applicable law gives you more rights, Microsoft reserves all other rights not expressly granted under the Terms of Use, whether by implication, estoppel or otherwise. 

 

Disclaimer 

The Emissions Impact Dashboard for Microsoft 365 is based on industry standards for carbon calculation of servers and provides general estimates to help organizations gain insights into the carbon emissions of their IT infrastructure associated with the use of Microsoft 365 core cloud services.  

 

The findings, interpretations, and conclusions presented in connection with the Emissions Impact Dashboard for Microsoft 365 online service, including the calculations, are for informational purposes only and are not specific advice or recommendations. Emissions Impact Dashboard for Microsoft 365 is not intended and should not be used for legal compliance, marketing, or reporting purposes. Information and views expressed may change without notice. You bear the risk of using it. The Emissions Impact Dashboard for Microsoft 365 is provided as is, without any representation or warranty of any kind, either express or implied, including without limitation any representations or endorsements regarding the use of, the results of, or performance of the Emissions Impact Dashboard for Microsoft 365, its appropriateness, accuracy, reliability, or correctness. The entire risk as to the use of Emissions Impact Dashboard for Microsoft 365 are assumed by you. Microsoft does not assume liability for the use of the Emissions Impact Dashboard for Microsoft 365. In no event will Microsoft be liable for additional direct or indirect damages including any lost profits, lost savings, or other incidental or consequential damages arising from any defects, or the use or inability to use the Emissions Impact Dashboard for Microsoft 365, even if Microsoft has been advised of the possibility of such damages. 

 

This document does not provide you with any legal rights to any intellectual property in any Microsoft product. You may copy and use this document for your internal, reference purposes. This document is confidential and proprietary to Microsoft and should be not shared with any other third parties. 



Emissions savings calculation  

The findings, interpretations, and conclusions presented in connection with the emissions savings calculations and any resulting savings, are for informational purposes only and are not specific advice or recommendations. Your organization's savings may vary depending on the on-premises device configurations and the carbon emissions associated with available power sources in the region where those devices are located. The emissions savings calculation is not intended and should not be used for legal compliance, marketing, or reporting purposes. You bear the risk of using it. The emissions savings calculations (Emissions Impact Dashboard for Microsoft 365) is provided as is, without any representation or warranty of any kind, either express or implied, including without limitation any representations or endorsements regarding the use of, the results of, or performance of the emissions savings calculations (Emissions Impact Dashboard for Microsoft 365), its appropriateness, accuracy, reliability, or correctness. The entire risk as to the use of emissions savings calculations (Emissions Impact Dashboard for Microsoft 365) are assumed by you. Microsoft does not assume liability for the use of the emissions savings calculations (Emissions Impact Dashboard for Microsoft 365). In no event will Microsoft be liable for additional direct or indirect damages including any lost profits, lost savings, or other incidental or consequential damages arising from any defects, or the use or inability to use the emissions savings calculations (Emissions Impact Dashboard for Microsoft 365), even if Microsoft has been advised of the possibility of such damages. 

 

(c) 2021 Microsoft Corporation. All rights reserved. This document and the Emissions Impact Dashboard for Microsoft 365 are provided as-is. 

Last updated: 10/12/2022 
"
```



```dax
Info_text_emissions12_MOM = 
var maxmonth = if(ISFILTERED(DateTable[Dates]),LASTDATE(DateTable[Dates]),0)
var e= CALCULATE((CONCATENATE(VALUES(MetricToolTips[Title]),[Comparison_Info_tooltip_text])),MetricToolTips[MetricName]="Carbon Emissions 12 MOM% comparison")
var f= if(maxmonth<=CALCULATE(MIN('TenantEmission'[Date]),ALL(DateTable[Dates])),"This card shows month over month comparisons. This value is blank when all months are selected in the date slicer", e)
return CONCATENATE(f," ")
```



```dax
Info_text_emissions123_MOM = 
var maxmonth = if(ISFILTERED(DateTable[Dates]),LASTDATE(DateTable[Dates]),0)
var e= CALCULATE((CONCATENATE(VALUES(MetricToolTips[Title]),[Comparison_Info_tooltip_text])),MetricToolTips[MetricName]="Carbon Emissions 123 MOM% comparison")
var f= if(maxmonth<=CALCULATE(MIN('TenantEmission'[Date]),ALL(DateTable[Dates])),"This card shows month over month comparisons. This value is blank when all months are selected in the date slicer", e)
return CONCATENATE(f," ")
```



```dax
Info_text_intensity_MOM = 
var maxmonth = if(ISFILTERED(DateTable[Dates]),LASTDATE(DateTable[Dates]),0)
var e= CALCULATE((CONCATENATE(VALUES(MetricToolTips[Title]),[Comparison_Info_tooltip_text])),MetricToolTips[MetricName]="Carbon Intensity MOM% comparison")
var f= if(maxmonth<=CALCULATE(MIN('TenantEmission'[Date]),ALL(DateTable[Dates])),"This card shows month over month comparisons. This value is blank when all months are selected in the date slicer", e)
return f
```



```dax
Info_text_highestservice_QOQ = 
var maxmonth = if(ISFILTERED(DateTable[Dates]),LASTDATE(DateTable[Dates]),0)
var e= CALCULATE((CONCATENATE(VALUES(MetricToolTips[Title]),[Comparison_Info_tooltip_text])),MetricToolTips[MetricName]="Carbon Emissions for highest service QOQ% comparison")
var f= if(maxmonth<=CALCULATE(MIN('TenantEmission'[Date]),ALL(DateTable[Dates])),"This card shows quarter over quarter comparisons. This value is blank when all months are selected in the date slicer", e)
return CONCATENATE(f,"  End of the report page.")
```



```dax
Footer Text = "Emissions for each month will be available by the 14th day after the end of that month. Currently this report only includes emissions associated with Exchange Online, SharePoint Online, OneDrive for Business, and Microsoft Teams. For more information. go to Calculation methodology or visit our technical documentation. End of this report page."
```



```dax
Alt_text_EmissionsScope1 = 
var e = [Total Emissions Scope 1 _KPI]
return CONCATENATE(e," ")
```



```dax
Alt_text_EmissionsScope2 = 
var e = [Total Emissions Scope 2 _KPI]
return CONCATENATE(e," ")
```



```dax
Alt_text_EmissionsScope3 = 
var e = [Total Emissions Scope 3 _KPI]
return CONCATENATE(e," ")
```



```dax
Info_text_emissions1_MOM = 
var maxmonth = if(ISFILTERED(DateTable[Dates]),LASTDATE(DateTable[Dates]),0)
var e= CALCULATE((CONCATENATE(VALUES(MetricToolTips[Title]),[Comparison_Info_tooltip_text])),MetricToolTips[MetricName]="Carbon Emissions 1 MOM% comparison")
var f= if(maxmonth<=CALCULATE(MIN('TenantEmission'[Date]),ALL(DateTable[Dates])),"This card shows month over month comparisons. This value is blank when all months are selected in the date slicer", e)
return CONCATENATE(f," ")
```



```dax
Info_text_emissions2_MOM = 
var maxmonth = if(ISFILTERED(DateTable[Dates]),LASTDATE(DateTable[Dates]),0)
var e= CALCULATE((CONCATENATE(VALUES(MetricToolTips[Title]),[Comparison_Info_tooltip_text])),MetricToolTips[MetricName]="Carbon Emissions 2 MOM% comparison")
var f= if(maxmonth<=CALCULATE(MIN('TenantEmission'[Date]),ALL(DateTable[Dates])),"This card shows month over month comparisons. This value is blank when all months are selected in the date slicer", e)
return CONCATENATE(f," ")
```



```dax
Info_text_emissions3_MOM = 
var maxmonth = if(ISFILTERED(DateTable[Dates]),LASTDATE(DateTable[Dates]),0)
var e= CALCULATE((CONCATENATE(VALUES(MetricToolTips[Title]),[Comparison_Info_tooltip_text])),MetricToolTips[MetricName]="Carbon Emissions 3 MOM% comparison")
var f= if(maxmonth<=CALCULATE(MIN('TenantEmission'[Date]),ALL(DateTable[Dates])),"This card shows month over month comparisons. This value is blank when all months are selected in the date slicer", e)
return CONCATENATE(f," ")
```



```dax
Manage data button = "Manage data, page 9 of 9"
```



```dax
Optout_text = "  To opt out of the Emissions Impact Dashboard for Microsoft 365, click the Opt Out button below. You will be taken to a separate webpage to complete the process. 
Within 48 hours of completing the opt out process, please delete this app and ensure no manual or scheduled refreshes occur. Any refresh request that occurs more than 48 hours after you complete the opt out process will cause your tenant to be opted back in to emissions processing. 
In the future you can opt back in by re-installing the app, but historical data will not initially be available. 
"
```



```dax
ALert text = "Please note: Availability of your emissions data for the month of February 2022 will be delayed due to a data quality issue."
```



```dax
CalcMethod_Text4 = "This methodology of segmentation by customer usage is consistent across scope 1, 2, and 3 carbon calculation.  



Carbon Intensity  

The Carbon Intensity index is a common sustainability term providing a ratio between emissions and another variable. The index is the total carbon dioxide equivalent emissions over usage, measured in grams of CO₂e per user.

The purpose of this index is to explain carbon emissions in relation to the usage of Microsoft 365 core cloud services. A smaller number is desired for the Carbon Intensity index.  

 

Keeping Pace in a Changing World  

Carbon accounting practices are evolving rapidly. We commit to evolving, revising, and refining our methodologies over time to incorporate science-based, validated approaches as they become available and relevant to assessing the carbon emissions associated with the Microsoft 365 cloud.  

 




"
```



```dax
CalcMethod_Text5 = "Disclaimer 

(c) 2021 Microsoft Corporation. All rights reserved.  



The findings, interpretations, and conclusions presented in this document are for informational purposes only and are based on assumptions and methodologies that are subject to change without notice. This tool and document are not intended and should not be used for legal compliance, marketing, or reporting purposes. Information contained in this document may change without notice. The tool is provided as is, without any representation or warranty of any kind, either express or implied, including without limitation any representations or endorsements regarding the use of, the results of, or performance of the services associated with the tool, its appropriateness, accuracy, reliability, or correctness. The entire risk as to the use of these services and the tool are assumed by you. Microsoft does not assume liability for the use of these services and the tool. In no event will Microsoft be liable for additional direct or indirect damages including any lost profits, lost savings, or other incidental or consequential damages arising from any defects, or the use or inability to use these services and/or the tool, even if Microsoft has been advised of the possibility of such damages. 

 

This document does not provide you with any legal rights to any intellectual property in any Microsoft product. You may copy and use this document for your internal, reference purposes only. This document is confidential and proprietary to Microsoft and should be not shared with any other third parties. "
```


## Table: DimApplication


```dax
DISTINCT(TenantEmission[ApplicationName])
```


## Table: DimOfficeRegion


```dax
DISTINCT(TenantEmission[OfficeRegionName])
```


## Table: DimScope


```dax
DISTINCT(SELECTCOLUMNS(TenantEmission,"ScopeName",[ScopeName]))
```


### Calculated Columns:


```dax
Scope Order = RANKX(ALL(DimScope),DimScope[ScopeName],,ASC)
```



```dax
Scope = 
IF(DimScope[ScopeName]="Scope1","Scope 1",
IF(DimScope[ScopeName]=="Scope2","Scope 2",
IF(DimScope[ScopeName]=="Scope2Loc","Scope 2 Location",
IF(DimScope[ScopeName]=="Scope3","Scope 3"))))
```


## Table: UItools


```dax
Row("Column", BLANK())
```


### Measures:


```dax
MinScale_for_ActiveUsers = MIN(TenantEmissionsSummary[Emissions])
```



```dax
Scale_for_ActiveUsers = AVERAGE((TenantEmissionsSummary[Emissions]))/12
```



```dax
MaxScale_for_ActiveUsers = MAX(TenantEmissionsSummary[Emissions])
```



```dax
TotalMaxScale = [MaxScale_for_ActiveUsers]+([Scale_for_ActiveUsers])
```


### Calculated Columns:


```dax
TotalMinScale = [MinScale_for_ActiveUsers]-[Scale_for_ActiveUsers]
```


## Table: TenantEmissionsSummary


```dax

SUMMARIZE(
   'TenantEmission',
   'TenantEmission'[Date],
   "Emissions", CALCULATE(SUM('TenantEmission'[Emissions]), 'TenantEmission'[ScopeName] <> "Scope2Loc")
)
```

