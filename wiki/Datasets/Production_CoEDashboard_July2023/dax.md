



# DAX

|Dataset|[Production_CoEDashboard_July2023](./../Production_CoEDashboard_July2023.md)|
| :--- | :--- |
|Workspace|[CenterOfExcellenceReport](../../Workspaces/CenterOfExcellenceReport.md)|

## Table: Environment

### Measures:


```dax
Combined Flows = COUNT(Flow[admin_flowid]) + COUNT(RPA[admin_rpaid])
```



```dax
Environment Makers = DISTINCTCOUNT(Environment[Env Maker Name])
```



```dax
ResourceCount = Count(App[admin_appid]) + Count(Flow[admin_flowid])
```



```dax
DBCapacity = LOOKUPVALUE('Environment Capacity'[admin_actualconsumption], 'Environment Capacity'[admin_capacitytype], "Database")
```


### Calculated Columns:


```dax
Env Maker Name = if(Environment[admin_environmentmakerdisplayname]="System", "System", LOOKUPVALUE(Maker[admin_displayname], Maker[admin_makerid], Environment[admin_maker]))
```



```dax
EnvironmentPermissionURL = Environment[admin_environmentcdsinstanceurl] & "tools/adminsecurity/adminsecurity_area.aspx"
```



```dax
EnvironmentURL = "https://admin.powerplatform.microsoft.com/environments/environment/" & Environment[admin_environmentid] & "/hub"
```



```dax
TeamsNumber = Count(App[admin_appid]) + Count(Flow[admin_flowid])
```


## Table: App

### Measures:


```dax
Sessions per month = CALCULATE(Count('Audit Log'[admin_appid]),DATESBETWEEN('Audit Log'[admin_creationtime].[Date],DATE(YEAR(TODAY()), MONTH(TODAY()), 1),EOMONTH(today(),0)))
```



```dax
Production App = If(App[Unique users per month] > 5 || App[Sessions per month] > 50, "Yes", "No")
```



```dax
Unique users per month = CALCULATE(DISTINCTCOUNT('Audit Log'[admin_userupn]),DATESBETWEEN('Audit Log'[admin_creationtime].[Date],DATE(YEAR(TODAY()), MONTH(TODAY()), 1),EOMONTH(today(),0)))
```



```dax
Production App Count = CALCULATE(COUNTA(App[admin_appid]), Filter(App, [Production App] = "Yes" ))
```



```dax
New users = 

VAR currentCustomers = VALUES('Audit Log'[admin_userupn])
VAR currentDate = MIN('Audit Log'[admin_creationtime])

VAR pastCustomers = CALCULATETABLE(VALUES('Audit Log'[admin_userupn]), 
    ALL('Audit Log'[admin_creationtime].[Month],'Audit Log'[admin_creationtime].[MonthNo],'Audit Log'[admin_creationtime].[Year])
    , 'Audit Log'[admin_creationtime]<currentDate)

VAR newCustomers = EXCEPT(currentCustomers,pastCustomers)

RETURN COUNTROWS(newCustomers)
```



```dax
Count of admin_appid YoY% = 
IF(
	ISFILTERED('App'[admin_appcreatedon]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_YEAR =
		CALCULATE(
			COUNTA('App'[admin_appid]),
			DATEADD('App'[admin_appcreatedon].[Date], -1, YEAR)
		)
	RETURN
		DIVIDE(COUNTA('App'[admin_appid]) - __PREV_YEAR, __PREV_YEAR)
)
```


### Calculated Columns:


```dax
Days Since Modified = DATEDIFF(App[admin_appmodifiedon],TODAY(),DAY)
```



```dax
Days Since Published = DATEDIFF(App[admin_apppublished],TODAY(),DAY)
```



```dax
Environment Display Name = RELATED(Environment[admin_displayname])
```



```dax
City = RELATED(Maker[admin_city])
```



```dax
App Department = RELATED(Maker[admin_department])
```



```dax
AppMaker = if(ISBLANK(LOOKUPVALUE(Maker[admin_displayname], Maker[admin_makerid], App[admin_appowner])), App[admin_appownerdisplayname], LOOKUPVALUE(Maker[admin_displayname], Maker[admin_makerid], App[admin_appowner]))
```



```dax
AgeScore = if(App[Days Since Modified]>720,3,if(App[Days Since Modified]>360,2,IF(App[Days Since Modified]>120,1,0)))
```



```dax
DuplicateNames = 
VAR ThisApp = App[admin_displayname]
VAR Result = 
IF(COUNTROWS(
    FILTER(app,App[admin_displayname] = ThisApp)
)>1,1,0)
RETURN
Result
```



```dax
ArchiveLikelihood = int(App[admin_notmodifiedsincecreated] + App[admin_nonprodappnamecheck] + App[DuplicateNames] + App[AgeScore] + App[AppStateScore])
```



```dax
SharePointOnly = If(ISFILTERED(App[admin_sharepointformurl]),1,0)
```



```dax
AppIdentifier = IF(ISBLANK(App[admin_sharepointformurl]), App[admin_displayname], App[admin_sharepointformurl]) & " by " & App[AppMaker] & " in " & App[admin_appenvironmentdisplayname]
```



```dax
AppStateScore = if(App[admin_appstate]="Suspended",2,0)
```



```dax
Country, City = RELATED(Maker[admin_country])& ", " & RELATED(Maker[admin_city])
```


## Table: Flow

### Measures:


```dax
Count of admin_flowid YoY% = 
IF(
	ISFILTERED('Flow'[admin_flowcreatedon]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_YEAR =
		CALCULATE(
			COUNTA('Flow'[admin_flowid]),
			DATEADD('Flow'[admin_flowcreatedon].[Date], -1, YEAR)
		)
	RETURN
		DIVIDE(COUNTA('Flow'[admin_flowid]) - __PREV_YEAR, __PREV_YEAR)
)
```


### Calculated Columns:


```dax
Days Since Modified = DATEDIFF(Flow[admin_flowmodifiedon],TODAY(),DAY)
```



```dax
DuplicateNames = 
VAR ThisApp = Flow[admin_displayname]
VAR Result = 
if(COUNTROWS(
    FILTER(Flow,Flow[admin_displayname] = ThisApp)
)>1,1,0)
RETURN
Result
```



```dax
AgeScore = if(Flow[Days Since Modified]>730,3,if(Flow[Days Since Modified]>360,2,IF(Flow[Days Since Modified]>120,1,0)))
```



```dax
UnknownUserScore = if(Flow[cr5d5_flowisorphaned]="yes",2,0)
```



```dax
ArchiveLikelihood = if(int(Flow[admin_notmodifiedsincecreated] + Flow[admin_nonprodflowcheck] + Flow[FlowStateScore]  + Flow[AgeScore] + Flow[UnknownUserScore] + Flow[DuplicateNames] - Flow[UniqueActionsScore])=-1,0,int(Flow[admin_notmodifiedsincecreated] + Flow[admin_nonprodflowcheck] + Flow[FlowStateScore]  + Flow[AgeScore] + Flow[UnknownUserScore] + Flow[DuplicateNames] - Flow[UniqueActionsScore]))
```



```dax
FlowHTMLLink = "https://flow.microsoft.com/manage/environments/" & "Default-" & Flow[admin_flowenvironment] & "/flows/" & Flow[admin_flowid] & "/analytics"
```



```dax
Number of unique actions = 
COUNTROWS(FILTER('Flow Action Details','Flow Action Details'[admin_flow]=Flow[admin_flowid]))
```



```dax
FlowIdentifier = Flow[admin_displayname] & " by " & Flow[admin_flowmakerdisplayname] & " in " & LOOKUPVALUE(Environment[admin_displayname],Environment[admin_environmentid],Flow[admin_flowenvironment])
```



```dax
UniqueActionsScore = if(Flow[Number of unique actions]>5,1,0)
```



```dax
FlowStateScore = if(Flow[admin_flowstate]="Suspended",2,0) 
```



```dax
Standalone flows = CALCULATE(
DISTINCTCOUNT(Flow[cr5d5_flowtrigger]),
NOT Flow[cr5d5_flowtrigger] IN {"Request : PowerApp", "Request : PowerAppV2"}
)
```


## Table: Maker

### Measures:


```dax
Flows = COUNTROWS(RELATEDTABLE(App))
```



```dax
Apps = COUNTROWS(RELATEDTABLE(App))
```



```dax
Total Maker Flows = Count(Flow[admin_flowid]) + Count(RPA[admin_rpaid])
```



```dax
Count of admin_makerid MoM% = 
IF(
	ISFILTERED('Maker'[createdon]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_MONTH =
		CALCULATE(
			COUNTA('Maker'[admin_makerid]),
			DATEADD('Maker'[createdon].[Date], -1, MONTH)
		)
	RETURN
		DIVIDE(COUNTA('Maker'[admin_makerid]) - __PREV_MONTH, __PREV_MONTH)
)
```



```dax
Count of admin_makerid YoY% = 
IF(
	ISFILTERED('Maker'[createdon]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_YEAR =
		CALCULATE(
			COUNTA('Maker'[admin_makerid]),
			DATEADD('Maker'[createdon].[Date], -1, YEAR)
		)
	RETURN
		DIVIDE(COUNTA('Maker'[admin_makerid]) - __PREV_YEAR, __PREV_YEAR)
)
```


### Calculated Columns:


```dax
mmmyy = FORMAT('Maker'[createdon].[Date], "mmm-yy")
```



```dax
Country, City = Maker[admin_country]& ", " & Maker[admin_city]
```


## Table: Audit Log

### Measures:


```dax
Count of UPN total for ts = 
CALCULATE(DISTINCTCOUNT('Audit Log'[admin_userupn]), ALLSELECTED('Audit Log'[Date].[Date]))
```



```dax
Count of admin_auditlogid YoY% = 
IF(
	ISFILTERED('Audit Log'[admin_creationtime]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_MONTH =
		CALCULATE(
			COUNTA('Audit Log'[admin_auditlogid]),
			DATEADD('Audit Log'[admin_creationtime].[Date], -1, YEAR)
		)
	RETURN
		DIVIDE(
			COUNTA('Audit Log'[admin_auditlogid]) - __PREV_MONTH,
			__PREV_MONTH
		)
)
```



```dax
Count of admin_userupn YoY% = 
IF(
	ISFILTERED('Audit Log'[admin_creationtime]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_MONTH =
		CALCULATE(
			DISTINCTCOUNT('Audit Log'[admin_userupn]),
			DATEADD('Audit Log'[admin_creationtime].[Date], -1, YEAR)
		)
	RETURN
		DIVIDE(
			DISTINCTCOUNT('Audit Log'[admin_userupn]) - __PREV_MONTH,
			__PREV_MONTH
		)
)
```



```dax
MOM New User = VAR currentUsers = VALUES('Audit Log'[admin_userupn])
VAR currentDate = MAX('Audit Log'[admin_creationtime])

VAR pastUsers = CALCULATETABLE(VALUES('Audit Log'[admin_userupn]), 
    ALL('Audit Log'[admin_creationtime].[Month],'Audit Log'[admin_creationtime].[MonthNo],'Audit Log'[admin_creationtime].[Year])
    , 'Audit Log'[admin_creationtime]<currentDate)

VAR newUsers = EXCEPT(currentUsers,pastUsers)

RETURN COUNTROWS(newUsers)
```


### Calculated Columns:


```dax
Date = Date(YEAR('Audit Log'[admin_creationtime]),MONTH('Audit Log'[admin_creationtime]),DAY('Audit Log'[admin_creationtime]))
```



```dax
mmmyyy = 'Audit Log'[admin_creationhour].[Date]
```



```dax
IsCurrentMonth = 
    IF (
        YEAR ( 'Audit Log'[admin_creationtime].[Date] ) = YEAR ( TODAY () )
            && MONTH ( 'Audit Log'[admin_creationtime].[Date] ) = MONTH ( TODAY () ),
        "Yes",
        "No"
    )
```



```dax
NewUsers = COUNTROWS(filter('Audit Log', 'Audit Log'[IsCurrentMonth] = "Yes"))
```


## Table: Connector

### Calculated Columns:


```dax
Test Connector = IF(
	OR(
    ISERROR(
		SEARCH("test", Connector[admin_connectordisplayname])
	),
    
    ISERROR(
		SEARCH("Test", Connector[admin_connectordisplayname])
	)
    ),
	FALSE(),
	TRUE()
)
```



```dax
Demo Connector = IF(
	OR(
    ISERROR(
		SEARCH("demo", Connector[admin_connectordisplayname])
	),
    
    ISERROR(
		SEARCH("Demo", Connector[admin_connectordisplayname])
	)
    ),
	FALSE(),
	TRUE()
)
```



```dax
CustConnMaker = if(ISBLANK(Connector[admin_connectorcreatordisplayname]), LOOKUPVALUE(Maker[admin_displayname], Maker[admin_makerid], Connector[admin_maker]), Connector[admin_connectorcreatordisplayname])
```



```dax
ConnectorType = if(Connector[admin_iscustomapi], "Custom Connector", [admin_tier])
```


## Table: Virtual Agent

### Measures:


```dax
Count of admin_pvaid YoY% = 
IF(
	ISFILTERED('Virtual Agent'[admin_pvacreatedon]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_YEAR =
		CALCULATE(
			COUNTA('Virtual Agent'[admin_pvaid]),
			DATEADD('Virtual Agent'[admin_pvacreatedon].[Date], -1, YEAR)
		)
	RETURN
		DIVIDE(COUNTA('Virtual Agent'[admin_pvaid]) - __PREV_YEAR, __PREV_YEAR)
)
```


### Calculated Columns:


```dax
BotIdentifier = 'Virtual Agent'[admin_pvadisplayname] & " in " & 'Virtual Agent'[admin_pvaenvironmentdisplayname]
```


## Table: RPA

### Measures:


```dax
Failed Runs = CALCULATE(COUNTA('RPA Sessions'[admin_rpasessionsid]),FILTER('RPA Sessions','RPA Sessions'[admin_statuscode]="Failed"))
```



```dax
Succeeded Runs = COUNTX('RPA Sessions', 'RPA Sessions'[admin_statuscode]="Succeeded")
```



```dax
Count of admin_rpaid YoY% = 
IF(
	ISFILTERED('RPA'[admin_rpacreatedon]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_YEAR =
		CALCULATE(
			COUNTA('RPA'[admin_rpaid]),
			DATEADD('RPA'[admin_rpacreatedon].[Date], -1, YEAR)
		)
	RETURN
		DIVIDE(COUNTA('RPA'[admin_rpaid]) - __PREV_YEAR, __PREV_YEAR)
)
```


### Calculated Columns:


```dax
Days Since Modified = DATEDIFF(RPA[admin_rpacreatedon],TODAY(),DAY)
```



```dax
AgeScore = if(RPA[Days Since Modified]>720,3,if(RPA[Days Since Modified]>360,2,IF(RPA[Days Since Modified]>120,1,0)))
```



```dax
ArchiveLikelihood = int(RPA[admin_notmodifiedsincecreated] + RPA[admin_nonprodappnamecheck] + RPA[DuplicateNames] + RPA[AgeScore])
```



```dax
DuplicateNames = 
VAR ThisApp = RPA[admin_displayname]
VAR Result = 
IF(COUNTROWS(
    FILTER(app,RPA[admin_displayname] = ThisApp)
)>1,1,0)
RETURN
Result
```



```dax
FlowURL = "https://flow.microsoft.com/manage/environments/" & RPA[admin_rpaenvironment] & "/uiflows/" & RPA[admin_rpaid] & "/details"
```



```dax
UIFlowIdentifier = RPA[admin_displayname] & " in " & LOOKUPVALUE(Environment[admin_displayname],Environment[admin_environmentid],RPA[admin_rpaenvironment])
```


## Table: RPA Sessions

### Measures:


```dax
Color Value = VAR RunStatus = SELECTEDVALUE('RPA Sessions'[admin_statuscode])
    RETURN IF(RunStatus = "Failed", "lightcoral", "palegreen")
```


### Calculated Columns:


```dax
TimeDiff = 'RPA Sessions'[admin_completedon] - 'RPA Sessions'[admin_startedon]
```



```dax
CompletedDay = FORMAT('RPA Sessions'[admin_completedon].[Day], "dd/mm/yyyy")
```


## Table: Portals

### Calculated Columns:


```dax
Environment = LOOKUPVALUE(Environment[admin_displayname], Environment[admin_environmentid], Portals[admin_portalenvironment])
```



```dax
Maker Department = LOOKUPVALUE(Maker[admin_department], Maker[admin_makerid], Portals[admin_portalowner])
```


## Table: Environment Capacity

### Calculated Columns:


```dax
Environment Name = LOOKUPVALUE(Environment[admin_displayname], Environment[admin_environmentid], 'Environment Capacity'[admin_environment])
```


## Table: Connection Reference Identity

### Calculated Columns:


```dax
AccountOrg = (RIGHT([admin_accountname], LEN([admin_accountname])-FIND("@", [admin_accountname], 1, 0)))
```

