



# DAX

|Dataset|[WeeklyReport](./../WeeklyReport.md)|
| :--- | :--- |
|Workspace|[Project Commitments [Prod]](../../Workspaces/Project-Commitments-[Prod].md)|

## Table: DimDate

### Calculated Columns:


```dax
MonthNameShort = FORMAT([Date],"MMM")
```



```dax
MonthYearShort = Format([Date],"MMM yyyy")
```



```dax
Prev7Days = DATEADD('DimDate'[Date], -7, DAY)
```


## Table: DimProjectSurvey

### Calculated Columns:


```dax
CurrentWeek = 
var project = DimProjectSurvey[ProjectNumber]

var maxSurveyDate = CALCULATE(max(FactSurveyQ[DateKey]),all(FactSurveyQ), Filter(all(DimProjectSurvey),DimProjectSurvey[ProjectNumber]=project))
var maxYearkw = LOOKUPVALUE('DimDate'[ISOWeekOfYearNameInCal], 'DimDate'[DateKey], maxSurveyDate)
return maxYearkw
```



```dax
LastWeek = 
var project = DimProjectSurvey[ProjectNumber]

var maxSurveyDateKey = CALCULATE(max(FactSurveyQ[DateKey]),all(FactSurveyQ), Filter(all(DimProjectSurvey),DimProjectSurvey[ProjectNumber]=project))
var maxSurveyDatePrev = CALCULATE(min('DimDate'[Prev7Days]),Filter(all('DimDate'), 'DimDate'[DateKey] = maxSurveyDateKey))

var maxYearkw = LOOKUPVALUE('DimDate'[ISOWeekOfYearNameInCal], 'DimDate'[Date], maxSurveyDatePrev)
return maxYearkw
```



```dax
RLS Code: Current User is In Team = if(LOOKUPVALUE( DimParticipants[EmployeeEmail],DimParticipants[EmployeeEmail], [RLS Userprincipalname], DimParticipants[ProjectSurveyID], DimProjectSurvey[ProjectSurveyID],  Blank()) <> Blank(), True(), False())
```


## Table: RLS Measures

### Measures:


```dax
RLS Is Admin = false //if('RLS Measures'[RLS Current User Mail] = "claudia.fischer-mayer@rolandberger.com"; true(); false())
```



```dax
RLS Current User Mail = 
    if(
       //USERPRINCIPALNAME() = "claudia.fischer-mayer@rolandberger.com", "jan-oliver.sestak@rolandberger.com"
        USERPRINCIPALNAME() = "florian.zrenner@org.rolandberger.com", "claudia.fischer-mayer@rolandberger.com"
       , USERPRINCIPALNAME() //change to test other user    
    )


```



```dax
User is member of RLS admin group = COUNTROWS(CheckMemberOfRlsAdminGroup) > 0
```


## Table: FactSurveyQ

### Measures:


```dax
Avg Value = if(SELECTEDVALUE('Calculation'[Mode]) ="Team"
, //team calculation // get Responsible PM for current user and selected project --> filter this value 
  [Average for Team]
, [Avg Min 3 values])
```



```dax
Number of Answers by Value in Current Week = 
VAR cw =
    MIN ( DimProjectSurvey[CurrentWeek] )
VAR currentWeekValues =
    FILTER ( ALL ( 'DimDate' ), 'DimDate'[ISOWeekOfYearNameInCal] = cw )
VAR filterValue =
    VALUES ( 'Values'[Values] )
VAR selectedProject =
    SELECTEDVALUE ( DimProjectSurvey[ProjectSurveyID] )
VAR responsiblePm =
    LOOKUPVALUE (
        Teams[ResponsiblePMEmail],
        Teams[ProjectSurveyId], selectedProject,
        Teams[EmployeeMail], 'RLS Measures'[RLS Current User Mail]
    )
VAR numberOfSubmits =
    IF (
        SELECTEDVALUE ( 'Calculation'[Mode] ) = "Team",
        CALCULATE (
            COUNT ( FactSurveyQ[Question] ),
            FILTER ( DimParticipants, DimParticipants[ResponsiblePMEmail] = responsiblePm ),
            currentWeekValues
        ),
        CALCULATE ( COUNT ( FactSurveyQ[Question] ), currentWeekValues )
    )
RETURN
    IF (
        numberOfSubmits < 2,
        BLANK (),
        IF (
            SELECTEDVALUE ( 'Calculation'[Mode] ) = "Team",
            CALCULATE (
                COUNT ( FactSurveyQ[Question] ),
                FILTER (
                    ALLEXCEPT ( 'FactSurveyQ', FactSurveyQ[Question], FactSurveyQ[ProjectSurveyID] ),
                    FactSurveyQ[Value] IN filterValue
                ),
                FILTER (
                    DimParticipants,
                    DimParticipants[ResponsiblePMEmail] = responsiblePm
                        && DimParticipants[IsReponsiblePm] = FALSE ()
                ),
                currentWeekValues,
                FILTER ( DimProjectSurvey, DimProjectSurvey[ProjectSurveyID] = selectedProject )
            ),
            CALCULATE (
                COUNT ( FactSurveyQ[Question] ),
                FILTER (
                    ALLEXCEPT ( 'FactSurveyQ', FactSurveyQ[Question], FactSurveyQ[ProjectSurveyID] ),
                    FactSurveyQ[Value] IN filterValue
                ),
                DimParticipants[IsReponsiblePm] = FALSE (),
                currentWeekValues,
                FILTER ( DimProjectSurvey, DimProjectSurvey[ProjectSurveyID] = selectedProject )
            )
        )
    )

```



```dax
Avg Answer in Current Week = 
var cw = min(DimProjectSurvey[CurrentWeek])
var currentWeekValues = Filter (all('DimDate'),'DimDate'[ISOWeekOfYearNameInCal]=cw)

var result = CALCULATE([Avg Value], Filter(All(FactSurveyQ[Question]),FactSurveyQ[Question] = min(FactSurveyQ[Question])), currentWeekValues)
return if(result = blank(),"n.a.", result)
```



```dax
_Green = if([Avg Current Or Last Week (by visual filter)]>=3.5,[Avg Current Or Last Week (by visual filter)], 0)
```



```dax
_Yellow = if(and([Avg Current Or Last Week (by visual filter)]>=2,[Avg Current Or Last Week (by visual filter)]<3.5), [Avg Current Or Last Week (by visual filter)], 0)
```



```dax
_Red = if([Avg Current Or Last Week (by visual filter)]<2, [Avg Current Or Last Week (by visual filter)], 0)
```



```dax
Avg Answer in Last Week = 
var lw = min(DimProjectSurvey[LastWeek])
var currentWeekValues = Filter (all('DimDate'), 'DimDate'[ISOWeekOfYearNameInCal] = lw)
var result = CALCULATE([Avg Value],Filter(All(FactSurveyQ[Question]),FactSurveyQ[Question] = min(FactSurveyQ[Question])), currentWeekValues) 
return if(result=Blank(),"n.a.",result)
```



```dax
Avg Current Or Last Week (by visual filter) = 
if(and( HASONEVALUE(WeekFilterParameter[FilterParam]),SELECTEDVALUE( WeekFilterParameter[FilterParam]) = "Last Week")
            , [Avg Answer in Last Week]
            , [Avg Answer in Current Week]
            )
            
```



```dax
Diff Avg Cw to LW = if(ISNUMBER([Avg Answer in Current Week]) && ISNUMBER([Avg Answer in Last Week]), DIVIDE([Avg Answer in Current Week] - [Avg Answer in Last Week], [Avg Answer in Last Week])
,"")
```



```dax
Average for Team = 
var selectedProject = SELECTEDVALUE(DimProjectSurvey[ProjectSurveyID])
//var responsiblePm = LOOKUPVALUE(Teams[ResponsiblePMEmail],Teams[ProjectSurveyId], selectedProject, Teams[EmployeeMail], [RLS Current User Mail]) 
var responsiblePm = FactSurveyQ[Responsible PM]
return calculate([Avg Min 3 values],Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = responsiblePm))  
```



```dax
Avg Min 3 values = if(COUNTROWS(FactSurveyQ) < 2 , blank(), AVERAGE(FactSurveyQ[Value])) 
```



```dax
Too few submits = 
var cw = min(DimProjectSurvey[CurrentWeek])
var currentWeekValues = Filter (all('DimDate'), 'DimDate'[ISOWeekOfYearNameInCal] = cw)


var selectedProject = SELECTEDVALUE(DimProjectSurvey[ProjectSurveyID])
var responsiblePm = LOOKUPVALUE(Teams[ResponsiblePMEmail],Teams[ProjectSurveyId], selectedProject, Teams[EmployeeMail], 'RLS Measures'[RLS Current User Mail]) 

var numberOfSubmits = if(SELECTEDVALUE('Calculation'[Mode]) = "Team"
    , CALCULATE(count(FactSurveyQ[Question]), Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = responsiblePm), currentWeekValues, Filter(all(FactSurveyQ[Question]), FactSurveyQ[Question] = "Q1")) 
    , CALCULATE(count(FactSurveyQ[Question]), currentWeekValues, Filter(all(FactSurveyQ[Question]), FactSurveyQ[Question] = "Q1"))
    )

return if(numberOfSubmits < 2
//;numberOfSubmits
,  "To secure anonymity this report is only available if ≥ 2 team member participated in the weekly survey and therefore cannot be displayed."
, "")

```



```dax
Number of Total Participants = 
if(SELECTEDVALUE('Calculation'[Mode])="Team"
,[Number of Total Team Participants]
//;COUNTROWS(DimParticipants))
,CALCULATE( COUNTROWS(DimParticipants), FILTER(DimParticipants,DimParticipants[Active] = true())))
```



```dax
Number of Total Team Participants = 
var selectedProject = SELECTEDVALUE(DimProjectSurvey[ProjectSurveyID])
var responsiblePm = FactSurveyQ[Responsible PM] 
return calculate(COUNTROWS(DimParticipants),Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = responsiblePm && DimParticipants[Active]=true()))  
```



```dax
Number of Team Submits = 
var selectedProject = SELECTEDVALUE(DimProjectSurvey[ProjectSurveyID])
var responsiblePm = FactSurveyQ[Responsible PM] 
return calculate(COUNTROWS(FactSurveyQ),Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = responsiblePm), FILTER(FactSurveyQ, FactSurveyQ[Question]="Q1")) 
```



```dax
Number of Submits = if(SELECTEDVALUE('Calculation'[Mode])="Team"
, [Number of Team Submits]
, calculate(COUNTROWS(FactSurveyQ), FILTER(FactSurveyQ, FactSurveyQ[Question]="Q1")))
```



```dax
Number Submits Text = CONCATENATE(
                        CONCATENATE(if([Number of Submits] = Blank(), "X", [Number of Submits]) , "/")
                        , if([Number of Total Participants] = Blank(), "0", [Number of Total Participants]))
```



```dax
Responsible PM = 
var selectedProject = SELECTEDVALUE(DimProjectSurvey[ProjectSurveyID])
//var responsiblePM = LOOKUPVALUE(Teams[ResponsiblePMEmail],Teams[ProjectSurveyId], selectedProject, Teams[EmployeeMail], [RLS Current User Mail]) 
var responsiblePM = 'RLS Measures'[RLS Current User Mail]
return responsiblePM
```


### Calculated Columns:


```dax
IsCurrentWeek = 
var project = RELATED(DimProjectSurvey[ProjectNumber])
var thisYearKw = RELATED('DimDate'[ISOWeekOfYearNameInCal])

var maxSurveyDate = CALCULATE(max(FactSurveyQ[DateKey]),all(FactSurveyQ), Filter(all(DimProjectSurvey),DimProjectSurvey[ProjectNumber]=project))
var maxYearkw = LOOKUPVALUE('DimDate'[ISOWeekOfYearNameInCal], 'DimDate'[DateKey], maxSurveyDate)

return if(thisYearKw == maxYearkw,true(),false()) 
```



```dax
IsLastWeek = 
 
var project = RELATED(DimProjectSurvey[ProjectNumber])
var thisYearKw = RELATED('DimDate'[ISOWeekOfYearNameInCal])

var maxSurveyDate = CALCULATE(max(FactSurveyQ[DateKey]),all(FactSurveyQ), Filter(all(DimProjectSurvey),DimProjectSurvey[ProjectNumber]=project))
var prevDate = LOOKUPVALUE('DimDate'[Prev7Days], 'DimDate'[DateKey], maxSurveyDate)

var maxYearkw = LOOKUPVALUE('DimDate'[ISOWeekOfYearNameInCal], 'DimDate'[Date], prevDate)
//return maxSurveyDate
return if(thisYearKw == maxYearkw,true(),false())
```


## Table: FactSurveyC

### Measures:


```dax
CommitmentIndicator = 
VAR __radius = 10
VAR __opacity = 0.75
VAR __color = Switch( Min(FactSurveyC[Value]),0,"Gray",1,"Green",-1,"Red")


 VAR __header = "data:image/svg+xml;utf8," &
              "<svg xmlns='http://www.w3.org/2000/svg' x='0px' y='0px' width='20' height='20'>"
VAR __footer = "</svg>"
VAR __shapeTextCircle = "<circle cx='10' cy='10' r='" & __radius & "' fill='" & __color & "' fill-opacity='" & __opacity & "' />"

VAR __shapeText = __shapeTextCircle
    
VAR __return = __header & __shapeText & __footer


RETURN if(count(FactSurveyC[Commitment]) > 0, __return, Blank())
```



```dax
Anzahl Ja = CALCULATE(COUNTROWS(FactSurveyC),Filter(FactSurveyC, FactSurveyC[Value] = 1),Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = 'RLS Measures'[RLS Current User Mail]))
```



```dax
Anzahl Gesamt = Calculate(COUNTROWS(FactSurveyC),Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = 'RLS Measures'[RLS Current User Mail]))
```



```dax
Anteil Ja = DIVIDE([Anzahl Ja], [Anzahl Gesamt], Blank())
```



```dax
CommitmentIndicator for TeamPM = 
CALCULATE([CommitmentIndicator], Filter(DimParticipants, [User is member of RLS admin group] = TRUE() || DimParticipants[ResponsiblePMEmail] = 'RLS Measures'[RLS Current User Mail]))
//CALCULATE([CommitmentIndicator], Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = 'RLS Measures'[RLS Current User Mail]))
```


### Calculated Columns:


```dax
CommitmentComment Current Week = if(FactSurveyC[IsCurrentWeekComment],FactSurveyC[Comment],Blank())
```



```dax
IsCurrentWeekComment = 
var project = RELATED(DimProjectSurvey[ProjectNumber])
var thisYearKw = RELATED('DimDate'[ISOWeekOfYearNameInCal])

var maxSurveyDate = CALCULATE(max(FactSurveyQ[DateKey]),all(FactSurveyC), Filter(all(DimProjectSurvey),DimProjectSurvey[ProjectNumber]=project))
var maxYearkw = LOOKUPVALUE('DimDate'[ISOWeekOfYearNameInCal], 'DimDate'[DateKey], maxSurveyDate)

return if(thisYearKw == maxYearkw,true(),false())
```


## Table: FactSurveyComments

### Measures:


```dax
Measure = 1
```


### Calculated Columns:


```dax
IsCurrentWeekComment = 
var project = RELATED(DimProjectSurvey[ProjectNumber])
var thisYearKw = RELATED('DimDate'[ISOWeekOfYearNameInCal])

var maxSurveyDate = CALCULATE(max(FactSurveyQ[DateKey]),all(FactSurveyQ), Filter(all(DimProjectSurvey),DimProjectSurvey[ProjectNumber]=project))
var maxYearkw = LOOKUPVALUE('DimDate'[ISOWeekOfYearNameInCal], 'DimDate'[DateKey], maxSurveyDate)

return if(thisYearKw == maxYearkw,true(),false())
```


## Table: Calculation

### Measures:


```dax
CommentTest = "das ist ein
Test für einen 
Kommentar"
```


## Table: Teams


```dax
SELECTCOLUMNS(DimParticipants, "EmployeeMail", DimParticipants[EmployeeEmail], "ProjectSurveyId", DimParticipants[ProjectSurveyID],  "ResponsiblePMEmail" , DimParticipants[ResponsiblePMEmail])
```

