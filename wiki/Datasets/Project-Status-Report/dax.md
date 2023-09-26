



# DAX

|Dataset|[project status report](./../project-status-report.md)|
| :--- | :--- |
|Workspace|[FC_PSR](../../Workspaces/FC_PSR.md)|

## Table: dim_employee

### Measures:


```dax
debug userprincipalname = userprincipalname()
```



```dax
debug is admin user = CONTAINS('rep v_fc_psr_permisson_admin','rep v_fc_psr_permisson_admin'[email], USERPRINCIPALNAME(), 'rep v_fc_psr_permisson_admin'[report_id],100)
```


### Calculated Columns:


```dax
Employee = dim_employee[last_name] & ", " & dim_employee[first_name] 
```



```dax
All Employees = "All"
```



```dax
Employee Id and Name = CONCATENATE(CONCATENATE(dim_employee[emp_id]," - "), dim_employee[Employee])
```


## Table: dim_project

### Measures:


```dax
Project Name (short) = 
var title =  min(dim_project[project_name]) 
return if(
    HASONEVALUE(dim_project[project_name])
    , if(LEN(title) <=20, title, CONCATENATE( LEFT(title,17), "..."))
    , "")
```



```dax
Client (short) = 
var title =  min(dim_project[project_client]) 
return if(
    HASONEVALUE(dim_project[project_client])
    , if(LEN(title) <=20, title, CONCATENATE( LEFT(title,17), "..."))
    , "")
```


### Calculated Columns:


```dax
Main Project Number = CALCULATE(min(dim_project_hierarchy[master_project_number]),dim_project_hierarchy[project_number] = earlier(dim_project[project_number]))
```



```dax
IsMaster = CONTAINS(dim_project_hierarchy, dim_project_hierarchy[project_number], dim_project[project_number], dim_project_hierarchy[is_master], TRUE())
```



```dax
MP Project Name = if(dim_project[IsMaster],dim_project[project_name],Blank())
```



```dax
PM Name = LOOKUPVALUE(dim_employee[last_name], dim_employee[emp_id], dim_project[pm_emp_id]) & ", "  & LOOKUPVALUE(dim_employee[first_name], dim_employee[emp_id], dim_project[pm_emp_id])
```



```dax
Accounting Responsible = dim_project[responsible_accounting]
```



```dax
IsMasterFormat = if(dim_project[IsMaster],1,Blank())
```



```dax
Project Time Completion Col = //percent completed, 1 if closed, otherwise calculated by dates
var res = IF(dim_project[project_status]="Closed",1,IF(DIVIDE(DATEDIFF(NOW(),dim_project[project_startdate],DAY),DATEDIFF(dim_project[project_startdate],dim_project[project_planned_end],DAY))>0,1,DIVIDE(DATEDIFF(dim_project[project_startdate],NOW(),DAY),DATEDIFF(dim_project[project_startdate],dim_project[project_planned_end],DAY))))

var res2  = if(res > 1, 1, res) 
return res2
```



```dax
Fee Budget (part) = if(dim_project[IsMaster]=TRUE()
    , CALCULATE([Fee Budget],ALLEXCEPT(dim_project, dim_project[Main Project Number]), dim_project[IsMaster]) - CALCULATE([Fee Budget],ALLEXCEPT(dim_project, dim_project[Main Project Number]), dim_project[IsMaster]=false)
    ,[Fee Budget]) 
```



```dax
IE Budget (part) = if(dim_project[IsMaster]=TRUE()
    , CALCULATE([IE Budget],ALLEXCEPT(dim_project, dim_project[Main Project Number]), dim_project[IsMaster]) - CALCULATE([IE Budget],ALLEXCEPT(dim_project, dim_project[Main Project Number]), dim_project[IsMaster]=false)
    ,[IE Budget]) 
```



```dax
Total Budget (part) = dim_project[Fee Budget (part)] + dim_project[IE Budget (part)]
```



```dax
Invoiced Fee (part) = if(dim_project[IsMaster]=TRUE()
    ,Blank()
    ,[Invoiced Fee]) 
```



```dax
Invoiced IE (part) = if(dim_project[IsMaster]=TRUE()
    ,Blank()
    ,[Invoiced IE]) 
```



```dax
Total Invoiced Revenue (part) = dim_project[Invoiced Fee (part)] + dim_project[Invoiced IE (part)]
```



```dax
Main Project Filter = if(dim_project[IsMaster]=FALSE(),Blank(), dim_project[Main Project Number] & " -- " & dim_project[project_client] & " -- " & dim_project[MP Project Name] & " -- " & dim_project[project_status])
```


## Table: fact_project_invoices_ppo

### Measures:


```dax
Cleared Invoice Amount = sum(fact_project_invoices_ppo[cleared_amount])
```



```dax
Net Value = Sum(fact_project_invoices_ppo[net_value]) 

```


## Table: fact_project_oview_budget_costs

### Measures:


```dax
Indicative IE Rev Incomplete = CALCULATE(if([IE internal costs] > [IE Budget], [IE Budget], [IE internal costs]), dim_project[project_status] <>"Closed")
```



```dax
Indicative IE Rev Completed = CALCULATE([Invoiced IE], dim_project[project_status]="Closed")
```



```dax
Indicative Fee Completed = CALCULATE([Invoiced Fee],dim_project[project_status] = "Closed")
```



```dax
Indicative Fee Incomplete = 
var _states = ALLSELECTED(dim_project[project_status]) //could be filtered i.e. Closed
    
return Calculate(
    sum(fact_project_oview_budget_costs[Indicative Rev. Col])
    , _states
    ,dim_project[project_status]<>"Closed"
    , Filter(all(fact_project_oview_budget_costs[accounting_period_date]), fact_project_oview_budget_costs[accounting_period_date]<= ReportingDates[Reporting Date])
)

```



```dax
Internal (not I/C) costs = sum(fact_project_oview_budget_costs[internal_costs_not_ic_eur])
```



```dax
Indicative IE Rev Incomplete (main) = CALCULATE(if([IE internal costs incl. Sub] > [IE Budget], [IE Budget], [IE internal costs incl. Sub]), dim_project[project_status] <>"Closed")
```



```dax
Product97 = CALCULATE( sum(fact_project_oview_budget_costs[invoiced_fee_eur]), FILTER(fact_project_oview_budget_costs, fact_project_oview_budget_costs[product_id] = 97))
```


### Calculated Columns:


```dax
Indicative Rev. Col = 
    if(fact_project_oview_budget_costs[project_status]="Closed", 
        fact_project_oview_budget_costs[budget_fee_eur],
         fact_project_oview_budget_costs[budget_fee_eur] * DIVIDE(fact_project_oview_budget_costs[project_completion_fee]
          , 100))
```



```dax
Fee value depending on product = if(fact_project_oview_budget_costs[product_id] = 97, fact_project_oview_budget_costs[revenue_eur],  fact_project_oview_budget_costs[budget_fee_eur]* fact_project_oview_budget_costs[project_completion] /100 )
```


## Table: fact_project_time_recording

### Measures:


```dax
Actual Days = sum(fact_project_time_recording[actual_work_days])
```



```dax
Actual Days To Date = CALCULATE([Actual Days], Filter(all(fact_project_time_recording[day_of_work]), fact_project_time_recording[day_of_work]<= max(fact_project_time_recording[day_of_work]))) 
```


## Table: fact_project_time_planned

### Measures:


```dax
Planned Days = sum(fact_project_time_planned[estimated_work_days])
```


## Table: fact_sales_order_items

### Measures:


```dax
Planned OD Fee = 
if(HASONEVALUE(dim_project[Main Project Number])
    ,MAX(fact_sales_order_items[planned_od_budget_sheet]) / 100
    , Blank()
)
```


## Table: _Project Measures (budget/cost)

### Measures:


```dax
Actual IE Ratio as of Fee = DIVIDE([IE internal costs],[Fee Budget])
```



```dax
Actual OD Fee = [Fee internal costs @100%] - [Indicative Fee Revenue]
```



```dax
Actual OD Fee % = DIVIDE([Actual OD Fee], [Indicative Fee Revenue])
```



```dax
Actual Overdraft IE = [IE internal costs] - [IE Budget]
```



```dax
Fee internal costs @100% = 
calculate(
    Sum(fact_project_oview_budget_costs[fee_internal_costs_100pct_eur])
    //[Σ Fee Used]
    , Filter(all(fact_project_oview_budget_costs[accounting_period_date]), fact_project_oview_budget_costs[accounting_period_date]<= ReportingDates[Reporting Date])
    )
```



```dax
Fee Budget = 
var calc=
calculate(
    SUM(fact_project_oview_budget_costs[budget_fee_eur] )
    , Filter(all(fact_project_oview_budget_costs[accounting_period_date]), fact_project_oview_budget_costs[accounting_period_date]<= ReportingDates[Reporting Date])
    )

return if(calc=blank(),0,calc)
```



```dax
IE internal costs = 
 calculate(
     //[Σ IE Used]
    Sum(fact_project_oview_budget_costs[ie_internal_costs_eur])
    , Filter(all(fact_project_oview_budget_costs[accounting_period_date]), fact_project_oview_budget_costs[accounting_period_date]<= ReportingDates[Reporting Date])
    ) 
```



```dax
IE Budget = 
 calculate(
    SUM(fact_project_oview_budget_costs[budget_ie_eur])
    , Filter(all(fact_project_oview_budget_costs[accounting_period_date]), fact_project_oview_budget_costs[accounting_period_date]<= ReportingDates[Reporting Date])
    )
```



```dax
Indicative Fee Revenue = 
    if(
        min(dim_project[project_status]) = "Released"
            , sum(fact_project_oview_budget_costs[Fee value depending on product])
            , [Indicative Fee Completed] + [Indicative Fee Incomplete] + if(min(dim_project[project_status]) = "Released", [Product97], 0)
    )
```



```dax
Indicative IE Revenue = [Indicative IE Rev Completed] + [Indicative IE Rev Incomplete]
```



```dax
Internal (not I/C) costs @ 100% = [Σ Fee Used] + [Σ IE Used]// [Fee internal costs @100%] + [IE internal costs]
```



```dax
Invoiced and Paid = [Net Value]
```



```dax
Invoiced Fee = 
calculate(
    SUM(fact_project_oview_budget_costs[invoiced_fee_eur])
    , Filter(all(fact_project_oview_budget_costs[accounting_period_date]), fact_project_oview_budget_costs[accounting_period_date]<= ReportingDates[Reporting Date])
    )
```



```dax
Invoiced IE = 
calculate(
    SUM(fact_project_oview_budget_costs[invoiced_ie_eur])
    , Filter(all(fact_project_oview_budget_costs[accounting_period_date]), fact_project_oview_budget_costs[accounting_period_date]<= ReportingDates[Reporting Date])
    )
```



```dax
Invoiced Revenue = [Invoiced Fee] + [Invoiced IE] 
```



```dax
Open WIP Fee = [Indicative Fee Revenue]-[Invoiced Fee]
```



```dax
Planned IE Ratio as of Fee = DIVIDE([IE Budget],[Fee Budget])
```



```dax
Project Fee Completion = 
if(HASONEVALUE(dim_project[Main Project Number])
    ,If(FIRSTNONBLANK(dim_project[project_status],1)="Closed",1,Divide([Indicative Fee Incomplete],[Fee Budget])) 
    ,AVERAGEX(dim_project, If(FIRSTNONBLANK(dim_project[project_status],1)="Closed",1,Divide([Indicative Fee Incomplete],[Fee Budget])) )
    )
```



```dax
Project IE Completion = 
if(HASONEVALUE(dim_project[Main Project Number])
    ,If(FIRSTNONBLANK(dim_project[project_status], 1)="Closed",1,DIVIDE([IE internal costs],[IE Budget]))
    ,AVERAGEX(dim_project, If(FIRSTNONBLANK(dim_project[project_status], 1)="Closed",1,DIVIDE([IE internal costs],[IE Budget])) )
    )
```



```dax
Project Margin = [Invoiced Revenue] - [Internal (not I/C) costs]
```



```dax
Project Margin % = Divide ([Project Margin], [Invoiced Revenue])
```



```dax
Project Time Completion = AVERAGE(dim_project[Project Time Completion Col])
```



```dax
Total Actual Overdraft = [Actual OD Fee] + [Actual Overdraft IE] 
```



```dax
Total Budget = [Fee Budget] + [IE Budget]
```



```dax
Total Indicative Revenue = [Indicative Fee Revenue] + [Indicative IE Revenue] 
```



```dax
Unpaid Invoices = [Invoiced Revenue] - [Invoiced and Paid]
```



```dax
Fee internal costs @100% incl. Sub = 
if(HASONEVALUE(dim_project[Main Project Number])
    ,CALCULATE([Σ Fee Used], filter(All(dim_project), dim_project[Main Project Number] = max(dim_project[Main Project Number])))
    ,CALCULATE([Σ Fee Used], filter(All(dim_project), dim_project[Main Project Number] in Values(dim_project[Main Project Number])))
)
```



```dax
IE internal costs incl. Sub = 
CALCULATE([Σ IE Used], filter(All(dim_project), dim_project[Main Project Number] in Values(dim_project[Main Project Number]) ), All(dim_employee))
```



```dax
Internal (not I/C) costs @ 100% incl. Sub = [Fee internal costs @100% incl. Sub] + [IE internal costs incl. Sub]
```



```dax
Actual OD Fee incl. Sub = [Fee internal costs @100% incl. Sub] - [Indicative Fee Revenue]
```



```dax
Actual Overdraft IE incl. Sub = [IE internal costs incl. Sub] - [IE Budget]
```



```dax
Total Actual Overdraft incl. Sub = [Actual OD Fee incl. Sub] + [Actual Overdraft IE incl. Sub] 
```



```dax
Actual IE Ratio as of Fee incl. Sub = DIVIDE([IE internal costs incl. Sub],[Fee Budget])
```



```dax
Project Margin incl. Sub = if(and(HASONEVALUE(dim_project[project_status]),min(dim_project[project_status])="Closed"),[Invoiced Revenue] -([Fee internal costs @100% incl. Sub] + [IE internal costs incl. Sub]- [Fee internal costs @100% employee incl. Sub]*0.35), Blank())
```



```dax
Internal (not I/C) costs incl. Sub = 
CALCULATE([Internal (not I/C) costs], filter(All(dim_project), dim_project[Main Project Number] in Values(dim_project[Main Project Number])))
```



```dax
Project Margin % incl. Sub = Divide ([Project Margin incl. Sub], [Invoiced Revenue])
```



```dax
Actual OD Fee % incl. Sub = DIVIDE([Actual OD Fee incl. Sub], [Indicative Fee Revenue])
```



```dax
Indicative IE Revenue (main) = [Indicative IE Rev Completed] + [Indicative IE Rev Incomplete (main)]
```



```dax
Total Indicative Revenue (main) = [Indicative Fee Revenue] + [Indicative IE Revenue (main)] 
```



```dax
Project IE Completion (main) = 
if(HASONEVALUE(dim_project[Main Project Number])
    ,If(FIRSTNONBLANK(dim_project[project_status], 1)="Closed",1,DIVIDE([IE internal costs incl. Sub],[IE Budget]))
    ,AVERAGEX(dim_project, If(FIRSTNONBLANK(dim_project[project_status], 1)="Closed",1,DIVIDE([IE internal costs incl. Sub],[IE Budget])) )
    )
```



```dax
TOOLTIP_PATTERN = 
"                                                           "
```



```dax
SEMI_TRANSPARENT = "#55555555"
```



```dax
Fee Indicative Remaining (main) = [Fee Budget] - [Indicative Fee Revenue]
```



```dax
Measure = min (dim_project[project_status])
```



```dax
Project Margin incl. Sub 2 = if(and(HASONEVALUE(dim_project[project_status]),min(dim_project[project_status])="Closed"),[Invoiced Revenue] - [Internal (not I/C) costs incl. Sub], Blank())
```



```dax
Fee internal costs @100% employee incl. Sub = 
if(HASONEVALUE(dim_project[Main Project Number])
    ,CALCULATE([Σ Fee Used employee], filter(All(dim_project), dim_project[Main Project Number] = max(dim_project[Main Project Number] )))
    ,CALCULATE([Σ Fee Used employee], filter(All(dim_project), dim_project[Main Project Number] in Values(dim_project[Main Project Number])))
)
```


## Table: DisplayProjectTableData

### Measures:


```dax
Dynamic Table Value = 
Switch(min(DisplayProjectTableData[Field])
    ,"Fee Budget", [Fee Budget]
    , "IE Budget", [IE Budget]
    ,"Total Budget", [Total Budget]

    ,"Fee Invoiced", [Invoiced Fee]
    ,"IE Invoiced", [Invoiced IE]
    ,"Total Invoiced", [Invoiced Revenue]

    ,"Fee Used", [Fee internal costs @100% incl. Sub]
    
    ,"IE used", [IE internal costs incl. Sub]
    ,"Total Used", [Internal (not I/C) costs @ 100% incl. Sub]

    ,"FEE Actual OD", [Actual OD Fee incl. Sub]
    ,"IE Actual OD", [Actual Overdraft IE incl. Sub]
    ,"Total Actual OD", [Total Actual Overdraft incl. Sub]

    ,"Total Invoice Paid", [Invoiced and Paid]
    ,"Total Invoice Unpaid", [Unpaid Invoices]

    ,"Open WIP Fee", [Open WIP Fee]

    ,"Fee Indicative Revenue", [Indicative Fee Revenue]
    ,"IE Indicative Revenue", [Indicative IE Revenue (main)]
    ,"Total Indicative Revenue",[Total Indicative Revenue (main)]
    ,"Project Margin", [Project Margin incl. Sub]
    ,"Fee Indicative Remaining", if(min(dim_project[project_status]) = "Closed" ,"-", [Fee Budget] - [Indicative Fee Revenue])
    
    
    , "") 

```



```dax
Dynamic Table Percent = 
Switch(min(DisplayProjectTableData[Field])
    ,"Fee Actual OD", [Actual OD Fee % incl. Sub]
    ,"Fee Completion", [Project Fee Completion]
    ,"Planned OD Fee",[Planned OD Fee]
    ,"Time Completion", [Project Time Completion]
    ,"IE Completion", [Project IE Completion (main)]
    ,"IE Planned in % of Fee", [Planned IE Ratio as of Fee]
    ,"IE Actual in % of Fee", [Actual IE Ratio as of Fee incl. Sub]
    ,"Project Margin", [Project Margin % incl. Sub]
, Blank()) 
```



```dax
Dynamic Table Value Meta = 
Switch(min(DisplayProjectTableData[Field])    ,"RB Company",min(dim_project[responsible_unit_cou])        ,"Project ID", min(dim_project[project_number]),"Sales Order ID", min(dim_project[sales_order_id])    ,"Currency of Sales Order", min(dim_project[sales_order_currency])    ,"Start Date", min(dim_project[project_startdate])
    ,"End Date", min(dim_project[project_planned_end])    ,"Project Status", min(dim_project[project_status])


    ,"Project Title", min(dim_project[project_name])
    ,"Customer", min(dim_project[project_client])
    ,"Industry", min(dim_project[dm_cc])
    ,"Project Manager", min(dim_project[PM Name])
    ,"Delivery Manager", min(dim_project[delivery_manager])
    ,"Controlling", min(dim_project[responsible_accounting])
    ,"Industry platform", min(dim_project[industry])  ,"Function platform", min(dim_project[function])  ,"Sector", min(dim_project[sector])  ,"Theme", min(dim_project[theme])
    , "")  

```


## Table: Distinct Main Project Numbers


```dax
Filter(VALUES(dim_project[Main Project Number]), dim_project[Main Project Number] <> Blank())
```


### Measures:


```dax
Selected Main Project = if(HASONEVALUE('Distinct Main Project Numbers'[Main Project Number]), min('Distinct Main Project Numbers'[Main Project Filter]),"Project Selection")
```



```dax
Multiple Selected Main Projects = 

VAR ConCat =
    CALCULATE (
        CONCATENATEX (
            VALUES ( dim_project[Main Project Filter])
            ,dim_project[Main Project Filter]
            ,",
"
        ), Filter(all(Dates),True())
    )
VAR IsItFiltered =
    IF ( or(or(ISFILTERED ( dim_project[Main Project Filter] ),ISFILTERED ( dim_project[project_client] )),ISFILTERED ( dim_project[delivery_manager] ))
    , ConCat
    , "Please select one or more projects" )

RETURN
    IsItFiltered

```



```dax
Selected Client = 

 
if(ISFILTERED('Distinct Main Project Numbers'[Main Project Filter]),
    ""
,   
if(ISFILTERED('Distinct Main Project Numbers'[Project Client])
    ,calculate(CONCATENATEX(values('Distinct Main Project Numbers'[Project Client]), 'Distinct Main Project Numbers'[Project Client], ",
"))
    ,"[optionally filter by selecting one or more clients]")
 )
```



```dax
Multiple Selected Client = 

if(ISFILTERED('dim_project'[project_client])
    ,calculate(CONCATENATEX(values('dim_project'[project_client]), 'dim_project'[project_client], ",
"))
    ,"[optionally filter by selecting one or more clients]")

```



```dax
Multiple Scelected Delivery Manager = if(ISFILTERED('dim_project'[delivery_manager])
    ,calculate(CONCATENATEX(values('dim_project'[delivery_manager]), 'dim_project'[delivery_manager], ",
"))
    ,"[optionally filter by selecting one or more delivery managers]")
```



```dax
Multiple Projects - nothing selected = 
VAR IsItFiltered =
    IF ( or(or(ISFILTERED ( dim_project[Main Project Filter] ),ISFILTERED ( dim_project[project_client] )),ISFILTERED ( dim_project[delivery_manager] ))
    , ""
    , "Please select one or more projects" )

RETURN
    IsItFiltered
```


### Calculated Columns:


```dax
Main Project Filter = LOOKUPVALUE(dim_project[Main Project Filter],dim_project[project_number],'Distinct Main Project Numbers'[Main Project Number])
```



```dax
StartDate = LOOKUPVALUE(dim_project[project_startdate], dim_project[project_number], 'Distinct Main Project Numbers'[Main Project Number]) 
```



```dax
Project Client = LOOKUPVALUE(dim_project[project_client], dim_project[project_number], 'Distinct Main Project Numbers'[Main Project Number]) 
```



```dax
Project Status = LOOKUPVALUE(dim_project[project_status], dim_project[project_number], 'Distinct Main Project Numbers'[Main Project Number]) 
```



```dax
Has Success Fee = 
var lu = LOOKUPVALUE(dim_project[has_success_fee], dim_project[project_number], 'Distinct Main Project Numbers'[Main Project Number]) 
return if (lu = blank(), "No", lu)
```


## Table: _progressMeasures by status date

### Measures:


```dax
PGR Earliest Start = min(dim_project[project_startdate])
```



```dax
PGR Latest Finish = max(dim_project[project_planned_end])
```



```dax
PGR Total Days = DATEDIFF([PGR Earliest Start], [PGR Latest Finish], DAY)
```



```dax
PGR Days to Status Date = 
if([PGR Earliest Start] > [StatusDate]
    ,Blank()
    ,if([PGR Latest Finish] > [StatusDate]
        , DATEDIFF([PGR Earliest Start], [StatusDate],DAY)
        , [PGR Total Days]
      )
)
```



```dax
PGR Remaining Days = [PGR Total Days] - [PGR Days to Status Date]
```



```dax
PGR Progress by Status Date = DIVIDE([PGR Days to Status Date], [PGR Total Days], 0) 
```



```dax
Linear Planned Days to Status = if(
    or(max(Dates[Date]) < [PGR Earliest Start], min(Dates[Date])>[StatusDate])
        ,blank(),  [PGR Progress by Status Date] * [Planned Days])
```



```dax
PGR Progess by Actuals vs Planned by Status Date = DIVIDE([PGR Actual Days To Status Date] , [Linear Planned Days to Status], 0)
```



```dax
StatusDate = 
var _lastActual = max(fact_project_time_recording[day_of_work])
return 
   if (Today() > _lastActual, TODAY(),_lastActual)

```



```dax
PGR Actual Days To Date = 
if(And(max(Dates[Date]) > [PGR Latest Finish] , max(Dates[Date]) > max(fact_project_time_recording[day_of_work]))
     , Blank()  
     ,
     if(min(Dates[Date]) > [lastActualDate by date]
        , blank()
        ,CALCULATE([Actual Days], Filter(all(Dates[Date]), Dates[Date]<= [StatusDate] && Dates[Date] <= max(Dates[Date])))
     )
)
     
```



```dax
Max stat date = max(Dates[Date]) 
```



```dax
PGR Days to Date = 
if([PGR Earliest Start] > [Max stat date]
    ,Blank()
    ,if([PGR Latest Finish] > [Max stat date]
        , DATEDIFF([PGR Earliest Start], [Max stat date],DAY)
        , [PGR Total Days]
      )
)
```



```dax
PGR Progress by Date = if(max(Dates[Date])>[PGR Latest Finish],blank(), DIVIDE([PGR Days to Date], [PGR Total Days], 0) )
```



```dax
Linear Planned Days to Date = if(max(Dates[Date])> [PGR Latest Finish],blank(), [PGR Progress by Date] * [Planned Days])
```



```dax
AvgActualsPerDay = 
if([Total Actuals (date independent)] > 0
    , DIVIDE([Total Actuals (date independent)] , DATEDIFF([firstActualDate by date], [lastActualDate by date],DAY), Blank())
    , [LinearPlannedPerDay])
```



```dax
PGR Actual Days To Status Date = 
     CALCULATE([Actual Days], Filter(all(Dates[Date]), Dates[Date]<= [StatusDate] && Dates[Date] <= max(Dates[Date])))

```



```dax
PGR Progess by Actuals vs Planned by Status Date (valid dates) = if(max(Dates[Date])> [lastActualDate by date],blank(), [PGR Progess by Actuals vs Planned by Status Date] )
```



```dax
Goal 100% = if(or( max(Dates[Date])> [lastActualDate by date], max(Dates[Date])<[PGR Earliest Start]) ,blank(), 1)
```



```dax
LinearPlannedPerDay = DIVIDE( [Planned Days], [PGR Total Days], Blank())
```



```dax
linear Forecast until planned project end = 
var calcDate = max(Dates[Date])
var lastActualDate = [lastActualDate by date]
var startDate = if(ISBLANK(lastActualDate), [PGR Earliest Start], lastActualDate)
return if(or(or(or( calcDate > [PGR Latest Finish], lastActualDate >= calcDate), calcDate < [PGR Earliest Start]), calcDate < Today())
    , blank()
    , [Total Actuals (date independent)]  + [AvgActualsPerDay] * DATEDIFF(startDate, calcDate,DAY)
)
```



```dax
lastActualDate by date = 
var _max = calculate(max(fact_project_time_recording[day_of_work]), All(Dates[Date]))
return if(_max < TODAY(), TODAY(),  _max)
```



```dax
Total Actuals (date independent) = CALCULATE([Actual Days], All(Dates[Date]))
```



```dax
Forecast Result = 
if(min(dim_project[project_status]) = "Closed"
    , [Total Actuals (date independent)]
    , CALCULATE([linear Forecast until planned project end], Filter(All(Dates[Date]),Dates[Date] =[PGR Latest Finish]))
     )
```



```dax
Max of Status or Finish Date = 
   if ([PGR Latest Finish] > [StatusDate]
    , [PGR Latest Finish]
    , [StatusDate]
   )
```



```dax
Forecast Result (bar) = 
if(min(dim_project[project_status]) = "Closed"
    , blank()
    , [Forecast Result]
     )
```



```dax
PGR Actual Days To Last Actual = if(min(Dates[Date])> [lastActualDate by date], blank(), 
     CALCULATE([Actual Days], Filter(all(Dates[Date]), Dates[Date]<= [StatusDate] && Dates[Date] <= max(Dates[Date]))))
```



```dax
Forecast Result (trend) = 
if(min(Dates[Date]) <  [lastActualDate by date]
    , [PGR Actual Days To Date]
    , if(min(Dates[Date])> [PGR Latest Finish], blank(), 
    CALCULATE([linear Forecast until planned project end], Filter(All(Dates[Date]),Dates[Date] <= max(Dates[Date])))
     ))
```



```dax
Planned Days (in project duration) = 
if(or(max(Dates[Date]) < [PGR Earliest Start] ,min(Dates[Date]) > [PGR Latest Finish]), blank(), [Planned Days])
```



```dax
firstActualDate by date = 
var _min = calculate(min(fact_project_time_recording[day_of_work]), All(Dates[Date]))
return  _min
```



```dax
Difference = //f([Planned Days] == blank(), blank(), [Planned Days] - [Actual Days])
[Planned Days] - [Actual Days]
```


## Table: Dates


```dax
CALENDAR(Date(2018,01,01), DATE(2023,12,31 ))
```


## Table: ReportingDates


```dax
CALENDAR(min(fact_project_oview_budget_costs[accounting_period_date]), max(fact_project_oview_budget_costs[accounting_period_date]))
```


### Measures:


```dax
Reporting Date = max(ReportingDates[Date])
```


### Calculated Columns:


```dax
YearMonth = CONCATENATE( Format(Year(ReportingDates[Date]),"####"), Format(Month(ReportingDates[Date]),"00"))
```



```dax
Period = CONCATENATE(Format(ReportingDates[Date],"MMMM"), Format(YEAR(ReportingDates[Date])," ####"))
```


## Table: rep v_fc_psr_invoice

### Measures:


```dax
OPEN AMOUNT = sumx('rep v_fc_psr_invoice', if('rep v_fc_psr_invoice'[STATUS]="Canceled",0, 'rep v_fc_psr_invoice'[AMOUNT_TC] -  'rep v_fc_psr_invoice'[CLEARED_AMOUNT_TC] ))
```


## Table: v_fc_psr_byd_project_internal_incurred_costs

### Measures:


```dax
fee internal costs 100 by employee = 
if(HASONEVALUE(dim_employee[emp_id]) && HASONEVALUE(dim_service[service_desc]) && (not ISBLANK([Planned Days]) || not ISBLANK(sum(fact_project_time_recording[actual_work_days])) )
    , calculate(Sum(v_fc_psr_byd_project_internal_incurred_costs[fee_internal_costs_100pct_eur])
        ,Filter(v_fc_psr_byd_project_internal_incurred_costs,v_fc_psr_byd_project_internal_incurred_costs[employee_id] = min(dim_employee[emp_id]) 
                                                            //&& v_fc_psr_byd_project_internal_incurred_costs[service] = min(dim_service[service_desc])
                                                            && v_fc_psr_byd_project_internal_incurred_costs[service_id] = min(dim_service[service_id])
                ))
    , if(HASONEVALUE(dim_employee[country_code]), Blank(), Sum(v_fc_psr_byd_project_internal_incurred_costs[fee_internal_costs_100pct_eur]))
    )
```



```dax
Σ Fee Used = calculate(Sum(v_fc_psr_byd_project_internal_incurred_costs[fee_internal_costs_100pct_eur]))
```



```dax
Σ IE Used = Sum(v_fc_psr_byd_project_internal_incurred_costs[ie_internal_costs_eur])
```



```dax
Σ Total Used = [Σ Fee Used] + [Σ IE Used]
```



```dax
Σ Fee Used employee = calculate(Sum(v_fc_psr_byd_project_internal_incurred_costs[fee_internal_costs_100pct_eur]),Filter(dim_employee, dim_employee[emp_id] <> blank() && dim_employee[emp_id] <> "-999"))
```


## Table: v_fc_psr_byd_sales_order_acquisition_performance

### Calculated Columns:


```dax
Employee = LOOKUPVALUE(dim_employee[Employee Id and Name], dim_employee[emp_id], v_fc_psr_byd_sales_order_acquisition_performance[emp_id])
```



```dax
ParPriCluster = 
var job = LOOKUPVALUE(dim_employee[jobcode], dim_employee[emp_id], v_fc_psr_byd_sales_order_acquisition_performance[emp_id])

return switch(true()
        , CONTAINSSTRING(job, "partner"), " PAR"
        , CONTAINSSTRING(job, "principal"), " PRI"
        , "other"
)

```

