



# DAX

|Dataset|[PowerPlatformGovernance_CoEDashboard_February2023](./../PowerPlatformGovernance_CoEDashboard_February2023.md)|
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
UnknownUserScore = if(Flow[admin_flowmakerdisplayname]="Unknown",2,0)
```



```dax
ArchiveLikelihood = if(int(Flow[admin_notmodifiedsincecreated] + Flow[admin_nonprodflowcheck] + Flow[FlowStateScore]  + Flow[AgeScore] + Flow[UnknownUserScore] + Flow[DuplicateNames] - Flow[UniqueActionsScore])=-1,0,int(Flow[admin_notmodifiedsincecreated] + Flow[admin_nonprodflowcheck] + Flow[FlowStateScore]  + Flow[AgeScore] + Flow[UnknownUserScore] + Flow[DuplicateNames] - Flow[UniqueActionsScore]))
```



```dax
FlowHTMLLink = "https://australia.flow.microsoft.com/manage/environments/" & "Default-" & Flow[admin_flowenvironment] & "/flows/" & Flow[admin_flowid] & "/analytics"
```



```dax
FlowIdentifier = Flow[admin_displayname] & " by " & Flow[admin_flowmakerdisplayname] & " in " & LOOKUPVALUE(Environment[admin_displayname],Environment[admin_environmentid],Flow[admin_flowenvironment])
```



```dax
FlowStateScore = if(Flow[admin_flowstate]="Suspended",2,0) 
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


### Calculated Columns:


```dax
mmmyy = FORMAT('Maker'[createdon].[Date], "mmm-yy")
```



```dax
Country, City = Maker[admin_country]& ", " & Maker[admin_city]
```



```dax
MailTo = "mailto:" & Maker[admin_userprincipalname]
```


## Table: Audit Log

### Measures:


```dax
Count of UPN total for ts = 
CALCULATE(DISTINCTCOUNT('Audit Log'[admin_userupn]), ALLSELECTED('Audit Log'[Date].[Date]))
```



```dax
Count of admin_auditlogid MoM% = 
IF(
	ISFILTERED('Audit Log'[admin_creationtime]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_MONTH =
		CALCULATE(
			COUNTA('Audit Log'[admin_auditlogid]),
			DATEADD('Audit Log'[admin_creationtime].[Date], -1, MONTH)
		)
	RETURN
		DIVIDE(
			COUNTA('Audit Log'[admin_auditlogid]) - __PREV_MONTH,
			__PREV_MONTH
		)
)
```



```dax
Count of admin_userupn MoM% = 
IF(
	ISFILTERED('Audit Log'[admin_creationtime]),
	ERROR("Time intelligence quick measures can only be grouped or filtered by the Power BI-provided date hierarchy or primary date column."),
	VAR __PREV_MONTH =
		CALCULATE(
			DISTINCTCOUNT('Audit Log'[admin_userupn]),
			DATEADD('Audit Log'[admin_creationtime].[Date], -1, MONTH)
		)
	RETURN
		DIVIDE(
			DISTINCTCOUNT('Audit Log'[admin_userupn]) - __PREV_MONTH,
			__PREV_MONTH
		)
)
```



```dax
MOM New User = Not available
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



```dax
UserName = (LEFT([admin_userupn], if(FIND("@", [admin_userupn], 1, -1) > 1, FIND("@", [admin_userupn], 1, LEN([admin_userupn]))-1, FIND("@", [admin_userupn], 1, LEN([admin_userupn])))))
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


## Table: Environment Capacity

### Calculated Columns:


```dax
Environment Name = LOOKUPVALUE(Environment[admin_displayname], Environment[admin_environmentid], 'Environment Capacity'[admin_environment])
```

