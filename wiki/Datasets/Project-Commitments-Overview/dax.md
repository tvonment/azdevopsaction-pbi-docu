



# DAX

|Dataset|[Project Commitments Overview](./../Project-Commitments-Overview.md)|
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



```dax
WeeksInPast = DATEDIFF(DimDate[StartOfWeek],TODAY() - WEEKDAY(TODAY() ,2) +1, WEEK)

//DATEDIFF(DimDate[Date],TODAY(), WEEK)
```



```dax
Year-CW = switch(true
            , DimDate[ISOWeekOfYear] = 53 && DimDate[Month] = 1
                , REPLACE(DimDate[ISOWeekOfYearNameInCal], 1, 4, Format(DimDate[Year] - 1, "#"))
            , DimDate[ISOWeekOfYear] = 52 && DimDate[Month] = 1
                , REPLACE(DimDate[ISOWeekOfYearNameInCal], 1, 4, Format(DimDate[Year] - 1, "#"))

                , DimDate[ISOWeekOfYearNameInCal]
                )
```



```dax
StartOfWeek = DimDate[Date] - WEEKDAY(DimDate[Date],2) +1
```



```dax
Period = if(DimDate[WeeksInPast] = 1, "latest week",  
            if(DimDate[WeeksInPast] > 0, "past weeks", "future"))
```


## Table: DimProjectSurvey

### Measures:


```dax
# Expected Commitments in week = 
var startDate = min (dimdate[date])
var endDate = max (dimdate[date])

//var num = calculate ([# Commitments in project], DimProjectSurvey[SurveyStartDate] <= endDate ,  DimProjectSurvey[SurveyEndDate] >= startDate )
//var num = calculate (Sum(SurveyCampaign[NumberOfActiveCommitments_bak]), SurveyCampaign[CreatedAt] <= endDate ,  SurveyCampaign[CreatedAt] >= startDate )
var num = calculate ([NumberOfActiveCommitments by PM], SurveyCampaign[CreatedAt] <= endDate ,  SurveyCampaign[CreatedAt] >= startDate )

return num
```



```dax
# Commitments in project = sum(DimParticipants[# of commitments for participant])
```



```dax
% Degree of Fulfillment per week = if([# Expected Participants in week] = 0
                                , blank()
                                , divide(COALESCE([# Yes], 0)
                                    , [# Expected Commitments in week] //COALESCE([# Yes], 0) + COALESCE([# No], 0) + COALESCE([# n. a. or no response], 0)
                                    ,0
                                    )
                                )
```



```dax
# Expected Participants in week = 
var startDate = min (dimdate[date])
var endDate = max (dimdate[date])

//var num = calculate ([# Teilnehmer], DimProjectSurvey[SurveyStartDate] <= endDate ,  DimProjectSurvey[SurveyEndDate] >= startDate )
//var num = calculate (Sum(SurveyCampaign[NumberOfActiveParticipants_bak]), SurveyCampaign[CreatedAt] <= endDate ,  SurveyCampaign[CreatedAt] >= startDate )

var num = calculate ([NumberOfActiveParticipants by PM], SurveyCampaign[CreatedAt] <= endDate ,  SurveyCampaign[CreatedAt] >= startDate )

return num
```



```dax
# Teilnehmer = COUNTROWS(DimParticipants)
```



```dax
# Actual Participants in week = 
var startDate = min (dimdate[date])
var endDate = max (dimdate[date])

var num = calculate (COUNTROWS(values(FactSurvey[SurveyParticipantID])), DimProjectSurvey[SurveyStartDate] <= endDate ,  DimProjectSurvey[SurveyEndDate] >= startDate )

return num
```



```dax
# Missing Participants in week = coalesce([# Expected Participants in week] - [# Actual Participants in week], 0)
```



```dax
Exists in last weeks = Not available
```



```dax
Started within visible weeks = 

var since = min(DimDate[Date])

var relevant = if( min(DimProjectSurvey[SurveyEndDate]) < since, 0, 1)
return relevant
```



```dax
# Survey Starts = 
var _from = min(DimDate[Date])
var _to = min(DimDate[Date])

var res = calculate(COUNTROWS(DimProjectSurvey), DimProjectSurvey[SurveyStartDate] >= _from && DimProjectSurvey[SurveyStartDate] <= _to)
return if(isblank(res), 0, res)
```



```dax
# active surveys in week = 
var _from = min(DimDate[Date])
var _to = max(DimDate[Date])

return // coalesce(CALCULATE(COUNTROWS(SurveyCampaign), SurveyCampaign[CreatedAt] <= _to , SurveyCampaign[CreatedAt] >= _from), 0) 
coalesce(CALCULATE(COUNTROWS(DimProjectSurvey), DimProjectSurvey[SurveyStartDate] <= _to , DimProjectSurvey[SurveyEndDate] >= _from), 0)
```



```dax
avg. Degree of Fulfillment = 

var expected = CALCULATE(SUMX(values(DimDate[Year-CW]), [# Expected Commitments in week]), ALLSELECTED(DimDate))
var yes = CALCULATE(SUMX(values(DimDate[Year-CW]), [# Yes]), ALLSELECTED(DimDate))
var no = CALCULATE(SUMX(values(DimDate[Year-CW]), [# No]), ALLSELECTED(DimDate))
 
return divide( yes, yes + no, 0)
```



```dax
# PC Projects = 
var minDate = min(DimDate[Date])
var maxDate = max(DimDate[Date])

return CALCULATE(COUNTROWS(DimProjectSurvey), DimProjectSurvey[SurveyStartDate]<= maxDate, DimProjectSurvey[SurveyEndDate] >= minDate)
```



```dax
# Active Surveys = 
var _from = min(DimDate[Date])
var _to = min(DimDate[Date])

var res = calculate(COUNTROWS(DimProjectSurvey), Filter(DimProjectSurvey, DimProjectSurvey[SurveyStartDate] <= _from && DimProjectSurvey[SurveyEndDate] >= _to))
return if(isblank(res), 0, res)
```



```dax
# all active survey campaigns in week = 
var _from = min(DimDate[Date])
var _to = max(DimDate[Date])

return  coalesce(CALCULATE
                    (COUNTROWS(distinct(SurveyCampaign[projectnumber_adj]))
                    //, ALLEXCEPT(SurveyCampaign, SurveyCampaign[Survey Type])
                    , SurveyCampaign[CreatedAt] <= _to && SurveyCampaign[CreatedAt] >= _from)
                , 0) 
```



```dax
% Utilization rate = divide(COALESCE([# all active survey campaigns in week], 0), DimProjects[# CP Projects])
```



```dax
% Degree of Fulfillment to total per week = divide(COALESCE([# Yes], 0), COALESCE([# Expected Commitments in week], 0))
```



```dax
# all active projects with survey campaigns in week = 
var _from = min(DimDate[Date])
var _to = max(DimDate[Date])

return  coalesce(CALCULATE
                    (COUNTROWS(values(SurveyCampaign[projectnumber_adj]))
                    //, ALLEXCEPT(SurveyCampaign, SurveyCampaign[Survey Type])
                    , SurveyCampaign[CreatedAt] <= _to && SurveyCampaign[CreatedAt] >= _from)
                , 0) 
```


### Calculated Columns:


```dax
Project = DimProjectSurvey[ProjectNumber] & " - " & DimProjectSurvey[ProjectName]
```



```dax
End Date = 
var _pnr = DimProjectSurvey[projectnumber_adj]
return calculate(max(DimProjectSurvey[SurveyEndDate]), DimProjectSurvey[projectnumber_adj] = _pnr)
```



```dax
TeamPMs = CONCATENATEX(RELATEDTABLE(DimPMs), DimPMs[Name], " / ")
```


## Table: DimParticipants

### Calculated Columns:


```dax
# of commitments for participant = if(ISBLANK(DimParticipants[Commitment1]), 0, 1) + if(ISBLANK(DimParticipants[Commitment2]), 0, 1)
```



```dax
Participant = DimParticipants[LastName] & ", " & DimParticipants[FirstName]
```


## Table: RLS Measures

### Measures:


```dax
RLS Is Admin = false //if('RLS Measures'[RLS Current User Mail] = "claudia.fischer-mayer@rolandberger.com"; true(); false())
```



```dax
RLS Current User Mail = 
        USERPRINCIPALNAME() 
    //if(
    //    USERPRINCIPALNAME() = "florian.zrenner@org.rolandberger.com" || USERPRINCIPALNAME() = "claudia.fischer-mayer@rolandberger.com"
    //    , "dorina.jaeger@rolandberger.com"//"claudia.fischer-mayer@rolandberger.com" //switch to
    //   , USERPRINCIPALNAME() //change to test other user    
    //)

```



```dax
User is member of RLS admin group = COUNTROWS(CheckMemberOfRlsAdminGroup) > 0
```



```dax
RLS Country Has Filter = calculate(COUNTROWS(RLS_Country), Filter(RLS_Country,  RLS_Country[UserMail] = [RLS Current User Mail])) > 0
```



```dax
RLS CC Has Filter = calculate(COUNTROWS(RLS_CC), Filter(RLS_CC,  RLS_CC[UserMail] = [RLS Current User Mail])) > 0
```



```dax
RLS Has Filter = [RLS CC Has Filter] || [RLS Country Has Filter]
```



```dax
RLS Display Survey = 
var curCountry = min(DimProjectSurvey[CountryCode])
var curCC = min(DimProjectSurvey[CCID])
var cu = 'RLS Measures'[RLS Current User Mail]

var ret =
    if( [RLS Has Filter] 
            , if([RLS Country Has Filter] && calculate(COUNTROWS(RLS_Country), RLS_Country[CountryCode] = curCountry, RLS_Country[UserMail] = cu) > 0
                , TRUE()
                ,  if([RLS CC Has Filter] && calculate(COUNTROWS(RLS_CC), RLS_CC[CCID] = curCC) > 0
                    , TRUE()                    
                    , FALSE()
                    )
                ) 
            , FALSE() // no config for user 
    )

return 
    if( [RLS Has Filter] 
            , if([RLS Country Has Filter] && calculate(COUNTROWS(RLS_Country), RLS_Country[CountryCode] = curCountry) > 0
                , "visible by country"
                ,  if([RLS CC Has Filter] && calculate(COUNTROWS(RLS_CC), RLS_CC[CCID] = curCC) > 0
                    , "visible by cc"                    
                    , "no country and no cc config"
                    )
                ) 
            , "invalid rls config" // no config for user 
    )
    


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
var cw = min(DimProjectSurvey[CurrentWeek])
var currentWeekValues = Filter (all('DimDate'), 'DimDate'[ISOWeekOfYearNameInCal] = cw)
var filterValue = values(('Values'[Values]))

var selectedProject = SELECTEDVALUE(DimProjectSurvey[ProjectSurveyID])
var responsiblePm = LOOKUPVALUE(Teams[ResponsiblePMEmail],Teams[ProjectSurveyId], selectedProject, Teams[EmployeeMail], 'RLS Measures'[RLS Current User Mail]) 

var numberOfSubmits = if(SELECTEDVALUE('Calculation'[Mode]) = "Team"
    , CALCULATE(count(FactSurveyQ[Question]), Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = responsiblePm), currentWeekValues) 
    , CALCULATE(count(FactSurveyQ[Question]),  currentWeekValues)
    )

return if(numberOfSubmits < 3, blank()
, if(SELECTEDVALUE('Calculation'[Mode]) = "Team"
    ,CALCULATE(count(FactSurveyQ[Question]), Filter(ALLEXCEPT('FactSurveyQ',FactSurveyQ[Question],FactSurveyQ[ProjectSurveyID]), FactSurveyQ[Value] in filterValue), Filter(DimParticipants, DimParticipants[ResponsiblePMEmail] = responsiblePm), currentWeekValues, Filter(DimProjectSurvey, DimProjectSurvey[ProjectSurveyID] = selectedProject))
    ,CALCULATE(count(FactSurveyQ[Question]), Filter(ALLEXCEPT('FactSurveyQ',FactSurveyQ[Question],FactSurveyQ[ProjectSurveyID]), FactSurveyQ[Value] in filterValue), currentWeekValues, Filter(DimProjectSurvey, DimProjectSurvey[ProjectSurveyID] = selectedProject))))
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
Diff Avg Cw to LW = if([Avg Answer in Last Week]<>"n.a" && [Avg Answer in Last Week] <> "n.a.", DIVIDE([Avg Answer in Current Week] - [Avg Answer in Last Week], [Avg Answer in Last Week])
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
Avg Min 3 values = if(COUNTROWS(FactSurveyQ) < 3 , blank(), AVERAGE(FactSurveyQ[Value])) 
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

return if(numberOfSubmits < 3
//;numberOfSubmits
,  "This report cannot be displayed because the number of survey participants was below 3"
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



```dax
Anzahl Q Responses = COUNTROWS(FactSurveyQ)
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
# Yes = coalesce( Calculate(COUNTROWS(FactSurveyC), FactSurveyC[Value] = 1), 0)
```



```dax
Anzahl C Responses = Calculate(COUNTROWS(FactSurveyC))
```



```dax
Anteil Ja = DIVIDE([# Yes], [Anzahl C Responses], Blank())
```



```dax
# No = Calculate(COUNTROWS(FactSurveyC), FactSurveyC[Value] = -1)
```



```dax
# n. a. = Calculate(COUNTROWS(FactSurveyC), FactSurveyC[Value] = 0)
```



```dax
# n. a. or no response = 
var _na = [# n. a.]
var _tmp = _na + ([# Expected Commitments in week] - [# Yes] - [# No] - _na)

return if(_tmp = 0 && _na > 0, _na, _tmp)

```



```dax
# Fullfilled (in week) = if([# Actual Participants in week] > 0, [# Yes], Blank())
```



```dax
# Not fullfilled (in week) = if([# Actual Participants in week] > 0, coalesce([# No], 0), Blank())
```



```dax
# n.a or no response (in week) = if([# Actual Participants in week] > 0, [# n. a. or no response], Blank())
```



```dax
% fulfillment rate per week = if([# Actual Participants in week] > 0
                                    , [% Degree of Fulfillment per week] //divide(COALESCE([# Fullfilled (in week)], 0), COALESCE([# Fullfilled (in week)], 0) + COALESCE([# Not fullfilled (in week)], 0) + COALESCE([# n.a or no response (in week)], 0),0)
                                    , blank())
```


### Calculated Columns:


```dax
Commitment Answer = switch(FactSurveyC[Value], 0 , "n.a.", 1, "Yes", "No")
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


## Table: DimProjects

### Measures:


```dax
# CP Projects = 
var minDate = min(DimDate[Date])
var maxDate = max(DimDate[Date])

var _isSurveyFiltered = ISFILTERED(DimProjectSurvey[Project])

return if (_isSurveyFiltered, [# all active projects with survey campaigns in week], CALCULATE(COUNTROWS(distinct(DimProjects[project_number])), DimProjects[project_startdate] <= maxDate, coalesce( DimProjects[project_planned_end], date(9999,12,31)) >= minDate))
```



```dax
minDate = 
 min(DimDate[Date])

```



```dax
maxDate = 
 max(DimDate[Date])
```



```dax
is a current client project = 
var minDate = DimProjects[minDate]
var maxDate = DimProjects[maxDate]

var relevant = if( Min(DimProjects[project_startdate]) <= maxDate && coalesce( Max(DimProjects[project_enddate]), date(9999,12,31)) >= minDate, "yes", "no")

return relevant
```



```dax
Project commitments used on this project = 
var _from = min(DimDate[Date])
var _to = max(DimDate[Date])
//var numRows = coalesce(CALCULATE(COUNTROWS(RELATEDTABLE(DimProjectSurvey)), DimProjectSurvey[SurveyStartDate] <= _to , DimProjectSurvey[SurveyEndDate] >= _from),0)
var numRows = coalesce(CALCULATE(COUNTROWS(RELATEDTABLE(SurveyCampaign)), SurveyCampaign[CreatedAt] <= _to , SurveyCampaign[CreatedAt] >= _from),0)
return if(numRows=0,"no","yes")
```



```dax
# of Project Commitments used on this project = 
var _from = min(DimDate[Date])
var _to = max(DimDate[Date])
//var numRows = coalesce(CALCULATE(COUNTROWS(RELATEDTABLE(DimProjectSurvey)), DimProjectSurvey[SurveyStartDate] <= _to , DimProjectSurvey[SurveyEndDate] >= _from),0)
var numRows = coalesce(CALCULATE(COUNTROWS(RELATEDTABLE(SurveyCampaign)), SurveyCampaign[CreatedAt] <= _to , SurveyCampaign[CreatedAt] >= _from),0)
return if(numRows=0,0,numRows)
```



```dax
project with project commitments = 

var minDate = DimProjects[minDate]
var maxDate = DimProjects[maxDate]
var relevant = if( Min(DimProjects[project_startdate]) <= maxDate && coalesce( Max(DimProjects[project_enddate]), date(9999,12,31)) >= minDate || DimProjects[# of Project Commitments used on this project] > 0, 1, 0)
return relevant
```



```dax
PC active = 
var _from = [Selected Week Min Date]
var _to = [Selected Week Max Date]

var _pcEnd = max(DimProjectSurvey[SurveyEndDate])
var _pnr = max(DimProjectSurvey[projectnumber_adj])

var _isvalidCombination = if(CALCULATE(COUNTROWS(DimProjectSurvey), All(DimProjectSurvey), DimProjectSurvey[projectnumber_adj] = _pnr && DimProjectSurvey[SurveyEndDate] = _pcEnd)> 0, true(), false())
//var numRows = coalesce(CALCULATE(COUNTROWS(RELATEDTABLE(DimProjectSurvey)), DimProjectSurvey[SurveyStartDate] <= _to , DimProjectSurvey[SurveyEndDate] >= _from),0)

var numCampaigns = coalesce(CALCULATE(COUNTROWS(RELATEDTABLE(SurveyCampaign)), SurveyCampaign[CreatedAt] <= _to && SurveyCampaign[CreatedAt] >= _from),0)
var numActiveParticipants = coalesce(CALCULATE(COUNTROWS(RELATEDTABLE(DimParticipants)),DimParticipants[Active] = true),0)

//var numActivePC = dimProjects does only contain projects PC has not been deactivateed

return if(_isvalidCombination , if(numCampaigns>0 && numActiveParticipants > 0
        ,"yes"
        , "no"), blank())
```



```dax
IsRelevant project in selected week = 

var minDate = [Selected Week Min Date]
var maxDate = [Selected Week Max Date]
var projectStart = min(DimProjects[project_startdate])
var projectEnd = coalesce((max(DimProjects[project_planned_end])), date(9999,12,31))

var relevant = if( (projectStart <= maxDate) && (projectEnd >= minDate), 1, 0)
return relevant
```



```dax
IsRelevant pc in selected week = //include ProjectSurvey State

var minDate = [Selected Week Min Date]
var maxDate = [Selected Week Max Date]
var _pnr = min(DimProjects[ProjectNumber_adj])

var _surveyStart = calculate(min(DimProjectSurvey[SurveyStartDate]))
var _surveyEnd =  coalesce(calculate(min(DimProjectSurvey[SurveyEndDate])), _surveyStart)

var relevant = if( _surveyStart <> Blank() && (_surveyStart <= maxDate) && (_surveyEnd >= minDate), 1, 0)
return relevant

```



```dax
IsRelevant in selected week TEST = 
if(     [IsRelevant project in selected week] 
        &&
            (
                [IsRelevant pc in selected week] && [PC active] = "yes"
                ||
                [IsRelevant pc in selected week] && min(DimProjects[Number PCs for project]) > 1
            )
        ||
        [IsRelevant project in selected week] 
        &&
            (
                [PC active] = "no" &&  min(DimProjects[Number PCs for project]) = 1
            )
        || [IsRelevant pc in selected week]
    ,1
    , 0)
```



```dax
IsRelevant in selected week = 
if([IsRelevant project in selected week] || [IsRelevant pc in selected week] 
    ,1
    , 0)
```


### Calculated Columns:


```dax
Project Display Name = DimProjects[project_number] & " - " & DimProjects[project_name] 
```



```dax
isRelevant = 
var minDate = [minDate]
var maxDate = [maxDate]
var projectStart = DimProjects[project_startdate]
var projectEnd = coalesce((DimProjects[project_planned_end]), date(9999,12,31))

var relevant = if( (projectStart <= maxDate) && (projectEnd >= minDate), 1, 0)
return relevant
```



```dax
IsRelevantPC = //include ProjectSurvey State

var minDate = [minDate]
var maxDate = [maxDate]
var _pnr = min(DimProjects[ProjectNumber_adj])

var _surveyStart = calculate(min(DimProjectSurvey[SurveyStartDate]))
var _surveyEnd =  coalesce(calculate(min(DimProjectSurvey[SurveyEndDate])), _surveyStart)

var relevant = if( _surveyStart <> Blank() && (_surveyStart <= maxDate) && (_surveyEnd >= minDate), 1, 0)
return relevant

```



```dax
Number PCs for project = 
var _pnr = DimProjects[ProjectNumber_adj]
return calculate(COUNTROWS(DimProjectSurvey), ALL(DimProjectSurvey), DimProjectSurvey[projectnumber_adj] = _pnr)
```


## Table: FactSurvey

### Measures:


```dax
% Participation Rate = if([# Expected Participants in week] = 0, blank(), coalesce(divide([# Actual Participants in week], [# Expected Participants in week]), 0))
```



```dax
Return Rate = if([# Actual Participants in week] > 0, Format([# Actual Participants in week],"#"), "0") & " / " & Format([# Expected Participants in week], "#")
```



```dax
1. Workload and stress = if([# Actual Participants in week] >= [min needed return rate], AVERAGE(FactSurvey[Q1]), Blank())
```



```dax
2. Feedback = if([# Actual Participants in week] >= [min needed return rate], AVERAGE(FactSurvey[Q2]), Blank())
```



```dax
3. Development = if([# Actual Participants in week] >= [min needed return rate], AVERAGE(FactSurvey[Q3]), Blank())
```



```dax
4. Team = if([# Actual Participants in week] >= [min needed return rate], AVERAGE(FactSurvey[Q4]), Blank())
```



```dax
5. Culture = if([# Actual Participants in week] >= [min needed return rate], AVERAGE(FactSurvey[Q5]), Blank())
```



```dax
6. Overall project = if([# Actual Participants in week] >= [min needed return rate], AVERAGE(FactSurvey[Q6]), Blank())
```



```dax
Overall Average = 

if(ISINSCOPE(DimParticipants[Participant])
    ,  divide(AVERAGE(FactSurvey[Q1]) + AVERAGE(FactSurvey[Q2]) + AVERAGE(FactSurvey[Q3]) + AVERAGE(FactSurvey[Q4]) + AVERAGE(FactSurvey[Q5]) + AVERAGE(FactSurvey[Q6]) , 6)
    , divide([1. Workload and stress] + [2. Feedback] + [3. Development] + [4. Team] + [5. Culture] + [6. Overall project] , 6)
)
```



```dax
avg. Participation rate = 

var expected = CALCULATE(SUMX(values(DimDate[Year-CW]), [% Participation Rate]), ALLSELECTED(DimDate))
var yes = CALCULATE(SUMX(values(DimDate[Year-CW]), [# Yes]), ALLSELECTED(DimDate))
return expected
//return divide( yes, expected, 0)

```



```dax
min needed return rate = 2
```



```dax
Return Rate (1/3) = 
if(ISINSCOPE(DimParticipants[Project manager])
    , 
    var _pm = min(DimParticipants[Project manager])
    var _pmMail = min (DimParticipants[ResponsiblePMEmail])
    var _projectCom = CALCULATETABLE(values(DimProjectSurvey[ProjectSurveyID]))
    var _pmsForProject = CALCULATETABLE(values(DimParticipants[Project manager]), REMOVEFILTERS(DimParticipants[Project manager]), _projectCom)

    return if(CALCULATE([# Expected Participants in week (1/3)], REMOVEFILTERS(DimParticipants[Project manager]), _projectCom) > 0 && _pm in _pmsForProject
        ,   if(CALCULATE([# Expected Participants in week (1/3)], SurveyCampaignNumOfParticipantsPerPM[ResponsiblePMEmail] = _pmMail) > 0,
                if([# Actual Participants in week (1/3)] > 0, Format([# Actual Participants in week (1/3)],"#"), "0") & " / " & Format(calculate([# Expected Participants in week (1/3)], SurveyCampaignNumOfParticipantsPerPM[ResponsiblePMEmail] = _pmMail), "#")
                , blank()
            )
        ,   blank()) 
    
    ,
    if([# Expected Participants in week (1/3)] > 0,
        if([# Actual Participants in week (1/3)] > 0, Format([# Actual Participants in week (1/3)],"#"), "0") & " / " & Format([# Expected Participants in week (1/3)], "#")
        , blank()
    )
)
```



```dax
Overall Average @participant = 
var _emp = min(DimParticipants[EmployeeID])
var _partId = min( FactSurvey[SurveyParticipantID])

var _name = min(DimParticipants[Name])

var _Projectsurvey = min( DimParticipants[ProjectSurveyID] )
            
var _pnr = min(DimProjectSurvey[ProjectNumber])
var _yearcw = min(DimDate[Year-CW])
var _minDate = min(DimProjectSurvey[SurveyStartDate])
var _maxDate = max(DimProjectSurvey[SurveyEndDate])

var _doShowWeek = [DoShowThisWeek]

var _activeCount = if(_doShowWeek = 1, Calculate(COUNTROWS(FactSurvey),all(FactSurvey), all(DimDate), all(DimProjects), all(DimProjectSurvey), FactSurvey[SurveyParticipantID] = _partId, DimDate[Date] >= _minDate && DimDate[Date] <= _maxDate))
var _active = if(_activeCount >0, 99, 
    if(_name = "Tengel" && _doShowWeek = 1, "xx",  blank())
)

return if(ISINSCOPE(DimParticipants[Participant]) && ISINSCOPE(DimProjectSurvey[ProjectNumber]) && ISINSCOPE(DimDate[Year-CW])
    ,  var _res = divide(AVERAGE(FactSurvey[Q1]) + AVERAGE(FactSurvey[Q2]) + AVERAGE(FactSurvey[Q3]) + AVERAGE(FactSurvey[Q4]) + AVERAGE(FactSurvey[Q5]) + AVERAGE(FactSurvey[Q6]) , 6)
       return if(Not IsBlank(_res)
            , _res
            ,   _active
            //Participant belongs to survey
            
//            if(Calculate(COUNTROWS(FactSurvey),FactSurvey[SurveyParticipantID] = _partId, DimDate[Date] >= _minDate && DimDate[Date] <= _maxDate) > 0
   //             , 99
   //             , blank()
            
            //&& survey was active
            //if(_pnr = "CP21118" && _par = "Ahmad, Nour" && _yearcw = "2022-CW04", 99)
       )
    ,  divide([1. Workload and stress] + [2. Feedback] + [3. Development] + [4. Team] + [5. Culture] + [6. Overall project] , 6)
)
```



```dax
Project Q1 = 
if(calculate([# Actual Participants in week], REMOVEFILTERS(DimParticipants[Participant], DimParticipants[jobcode])) < [min needed return rate], blank()
,
    var _cw = Values(DimDate[Year-CW])
    var _project = values(DimProjectSurvey[ProjectSurveyID])

    return  calculate(Average(FactSurvey[Q1]), All(FactSurvey), _cw, _project)
)
```



```dax
Project Q2 = 
if(calculate([# Actual Participants in week], REMOVEFILTERS(DimParticipants[Participant], DimParticipants[jobcode])) < [min needed return rate], blank()
,
    var _cw = Values(DimDate[Year-CW])
    var _project = values(DimProjectSurvey[ProjectSurveyID])

    return  calculate(Average(FactSurvey[Q2]), All(FactSurvey), _cw, _project)
)
```



```dax
Project Q3 = 
if(calculate([# Actual Participants in week], REMOVEFILTERS(DimParticipants[Participant], DimParticipants[jobcode])) < [min needed return rate], blank()
,
    var _cw = Values(DimDate[Year-CW])
    var _project = values(DimProjectSurvey[ProjectSurveyID])

    return  calculate(Average(FactSurvey[Q3]), All(FactSurvey), _cw, _project)
)
```



```dax
Project Q4 = 
if(calculate([# Actual Participants in week], REMOVEFILTERS(DimParticipants[Participant], DimParticipants[jobcode])) < [min needed return rate], blank()
,
    var _cw = Values(DimDate[Year-CW])
    var _project = values(DimProjectSurvey[ProjectSurveyID])

    return  calculate(Average(FactSurvey[Q4]), All(FactSurvey), _cw, _project)
)
```



```dax
Project Q5 = 
if(calculate([# Actual Participants in week], REMOVEFILTERS(DimParticipants[Participant], DimParticipants[jobcode])) < [min needed return rate], blank()
,
    var _cw = Values(DimDate[Year-CW])
    var _project = values(DimProjectSurvey[ProjectSurveyID])

    return  calculate(Average(FactSurvey[Q5]), All(FactSurvey), _cw, _project)
)
```



```dax
Project Q6 = 
if(calculate([# Actual Participants in week], REMOVEFILTERS(DimParticipants[Participant], DimParticipants[jobcode])) < [min needed return rate], blank()
,
    var _cw = Values(DimDate[Year-CW])
    var _project = values(DimProjectSurvey[ProjectSurveyID])

    return  calculate(Average(FactSurvey[Q6]), All(FactSurvey), _cw, _project)
)
```



```dax
Project Overall = 
if(calculate([# Actual Participants in week], REMOVEFILTERS(DimParticipants[Participant], DimParticipants[jobcode])) < [min needed return rate], blank()
,
    Divide([Project Q1]+ [Project Q2] + [Project Q3] + [Project Q4] + [Project Q5] + [Project Q6], 6, blank())
)
```


## Table: SurveyCampaign

### Measures:


```dax
# Expected Participants in week (1/3) = 
var startDate = min (dimdate[date])
var endDate = max (dimdate[date])


//var projects = calculatetable (values(SurveyCampaign[ProjectSurveyID]), SurveyCampaign[CreatedAt] <= endDate ,  SurveyCampaign[CreatedAt] >= startDate, SurveyCampaign[SurveyTypeID] = 1 ||  SurveyCampaign[SurveyTypeID] = 3)
//var num =  calculate (sum(SurveyCampaign[NumberOfActiveParticipants_bak]), SurveyCampaign[CreatedAt] <= endDate ,  SurveyCampaign[CreatedAt] >= startDate, SurveyCampaign[SurveyTypeID] = 1 ||  SurveyCampaign[SurveyTypeID] = 3)

var num =  
//if(ISINSCOPE(DimParticipants[Project manager])
//    , calculate ([NumberOfActiveParticipants by PM], SurveyCampaign[CreatedAt] <= endDate 
//        , SurveyCampaign[CreatedAt] >= startDate, SurveyCampaign[SurveyTypeID] = 1 ||  SurveyCampaign[SurveyTypeID] = 3, SurveyCampaignNumOfParticipantsPerPM[ResponsiblePMEmail] = min(DimParticipants[Project manager])) +1
//    , 
    calculate ([NumberOfActiveParticipants by PM], SurveyCampaign[CreatedAt] <= endDate ,  SurveyCampaign[CreatedAt] >= startDate, SurveyCampaign[SurveyTypeID] = 1 ||  SurveyCampaign[SurveyTypeID] = 3)
//)



//return calculate(COUNTROWS(DimParticipants), DimParticipants[ProjectSurveyID] in projects)
return num
```



```dax
# Actual Participants in week (1/3) = 
var startDate = min (dimdate[date])
var endDate = max (dimdate[date])

var num = calculate (COUNTROWS(values(FactSurvey[SurveyParticipantID])), DimProjectSurvey[SurveyStartDate] <= endDate ,  DimProjectSurvey[SurveyEndDate] >= startDate )


var campaigns = calculatetable (values(SurveyCampaign[ID]), SurveyCampaign[CreatedAt] <= endDate ,  SurveyCampaign[CreatedAt] >= startDate, SurveyCampaign[SurveyTypeID] = 1 ||  SurveyCampaign[SurveyTypeID] = 3)
//var num = calculate ([# Teilnehmer], projects)

return calculate(COUNTROWS(values(FactSurvey[SurveyParticipantID])), FactSurvey[SurveyCampaignID] in campaigns)
```


### Calculated Columns:


```dax
projectnumber_adj = LOOKUPVALUE(DimProjectSurvey[projectnumber_adj], DimProjectSurvey[ProjectSurveyID], SurveyCampaign[ProjectSurveyID])
```


## Table: DateSelection


```dax


    Selectcolumns(
        CALCULATETABLE(DimDate, DimDate[WeeksInPast] >= 1 && DimDate[WeeksInPast] <= 12 + 4 - 1)
        , "Date", DimDate[Date]
        , "Year-CW", DimDate[Year-CW]
        , "Period", DimDate[Period]
        , "WeeksInPast", DimDate[WeeksInPast])

```


### Measures:


```dax
Selected Week Max Date = max(DateSelection[Date])
```



```dax
Selected Week = if(HASONEVALUE(DateSelection[Year-CW]), SELECTEDVALUE(DateSelection[Year-CW]), "ERR")
```



```dax
Number of weeks to show = 4
```



```dax
Selection Min Date to show = 

var shifted = CALCULATETABLE(ADDCOLUMNS(DateSelection, "start",  DATEADD(DateSelection[Date], -7 * ([Number of weeks to show]-1), DAY)))
return minx(shifted, [start])
```



```dax
Selection first week to show = 
var dat = [Selection Min Date to show]

return Calculate(min(DateSelection[Year-CW]), all(DateSelection), DateSelection[Date] = dat)
```



```dax
Interval Label = if(HASONEVALUE(DateSelection[Year-CW]), DateSelection[Selection first week to show] & " to " & DateSelection[Selected Week], "please select a week")
```



```dax
Utilization Rate current week = 
var _selectedWeek = [Selected Week]
return calculate([% Utilization rate], all(dimdate), DimDate[Year-CW] = _selectedWeek)
```



```dax
Utilization Rate all weeks = 

var _minDate = [Selection Min Date to show]
var _maxDate = DateSelection[Selected Week Max Date]

var weeks = calculatetable(values(DimDate[Year-CW]),All(DimDate), DimDate[Date]>= _minDate && DimDate[Date]<= _maxDate)
var weeklyValues = CALCULATETABLE(ADDCOLUMNS(weeks, "@util", [% Utilization rate]))

return AVERAGEX(weeklyValues, coalesce([@util], 0))
```



```dax
Participation Rate current week = 
var _selectedWeek = [Selected Week]
return calculate([% Participation Rate], all(dimdate), DimDate[Year-CW] = _selectedWeek)
```



```dax
Participatiopn Rate all weeks = 

var _minDate = [Selection Min Date to show]
var _maxDate = DateSelection[Selected Week Max Date]

var weeks = calculatetable(values(DimDate[Year-CW]),All(DimDate), DimDate[Date]>= _minDate && DimDate[Date]<= _maxDate)
var weeklyValues = CALCULATETABLE(ADDCOLUMNS(weeks, "@part", [% Participation Rate]))

return AVERAGEX(weeklyValues, [@part])
```



```dax
DoShowThisWeek = 
var _minDate = [Selection Min Date to show]
var _maxDate = DateSelection[Selected Week Max Date]

var minDate = min(DimDate[Date])

return if(minDate >= _minDate && minDate<= _maxDate, 1, blank())


```



```dax
Fulfillment Rate current week = 
var _selectedWeek = [Selected Week]
return calculate([% Degree of Fulfillment per week], all(dimdate), DimDate[Year-CW] = _selectedWeek)
```



```dax
Fulfillment Rate all weeks = 

var _minDate = [Selection Min Date to show]
var _maxDate = DateSelection[Selected Week Max Date]

var weeks = calculatetable(values(DimDate[Year-CW]),All(DimDate), DimDate[Date]>= _minDate && DimDate[Date]<= _maxDate)
var weeklyValues = CALCULATETABLE(ADDCOLUMNS(weeks, "@ful", [% Degree of Fulfillment per week]))

return AVERAGEX(weeklyValues, coalesce([@ful], blank()))
```



```dax
Utilization Rate all weeks Company = 

CALCULATE([Utilization Rate all weeks], REMOVEFILTERS(DimCC), REMOVEFILTERS(DimProjectSurvey[ProjectName]), REMOVEFILTERS(DimCountry))
```



```dax
Participation Rate all weeks Company = 

CALCULATE([Participatiopn Rate all weeks], REMOVEFILTERS(DimCC), REMOVEFILTERS(DimProjectSurvey[ProjectName]), REMOVEFILTERS(DimCountry))
```



```dax
Fulfillment Rate all weeks Company = 

CALCULATE([Fulfillment Rate all weeks], REMOVEFILTERS(DimCC), REMOVEFILTERS(DimProjectSurvey[ProjectName]), REMOVEFILTERS(DimCountry))
```



```dax
Min target = 0.45
```



```dax
Max target = 0.75
```



```dax
Selected Week Min Date = min(DateSelection[Date])
```


## Table: BarometerCluster

### Measures:


```dax
Q1 Cluster = 

var _cluster = SELECTEDVALUE(BarometerCluster[Cluster])
var _fromEqual = SELECTEDVALUE(BarometerCluster[From])
var _toLower = SELECTEDVALUE(BarometerCluster[To])
var _minDate = min(DimDate[Date])
var _maxDate = max(DimDate[Date])

var _activeSurveysInWeek = Filter(DimProjectSurvey,  [# Expected Participants in week (1/3)] > 0) --DimProjectSurvey[SurveyStartDate] <= _maxDate && DimProjectSurvey[SurveyEndDate] >= _minDate)

var _byProject = CALCULATETABLE( ADDCOLUMNS(values(DimProjectSurvey[ProjectNumber])
                , "@avg", coalesce([6. Overall project], 0)
                , "@numberOfActualParticipants", coalesce([# Actual Participants in week], 0)
                ), _activeSurveysInWeek)

var _projectsWithEnoughResponses = Filter(_byProject, [@numberOfActualParticipants] >= 2)
var _projectsWithToLittleResponses = Filter(_byProject, [@numberOfActualParticipants] < 2)

var _projectsInCluster = Filter(_projectsWithEnoughResponses, [@avg] >= _fromEqual && [@avg] < _toLower)

return  --COUNTROWS(_activeSurveysInWeek) --coalesce(CALCULATE(COUNTROWS(DimProjectSurvey), DimProjectSurvey[SurveyStartDate] <= _minDate , DimProjectSurvey[SurveyEndDate] >= _maxDate), 0)
    if(_cluster == "Gray"
        , COUNTROWS(_projectsWithToLittleResponses)
        , COUNTROWS(_projectsInCluster))

--CONCATENATEX(_projectsWithToLittleResponses, DimProjectSurvey[ProjectNumber], " - ")
```



```dax
Q Cluster = 

var _cluster = SELECTEDVALUE(BarometerCluster[Cluster])
var _fromEqual = SELECTEDVALUE(BarometerCluster[From])
var _toLower = SELECTEDVALUE(BarometerCluster[To])
var _minDate = min(DimDate[Date])
var _maxDate = max(DimDate[Date])

var _activeSurveysInWeek = Filter(DimProjectSurvey,  [# Expected Participants in week (1/3)] > 0) --DimProjectSurvey[SurveyStartDate] <= _maxDate && DimProjectSurvey[SurveyEndDate] >= _minDate)

var _byProject = CALCULATETABLE( ADDCOLUMNS(values(DimProjectSurvey[ProjectSurveyID])
                , "@avg", coalesce(calculate(AVERAGE(FactSurveyQ[Value])), 0)
                , "@numberOfActualParticipants", coalesce([# Actual Participants in week (1/3)], 0)
                ), _activeSurveysInWeek)

var _projectsWithEnoughResponses = Filter(_byProject, [@numberOfActualParticipants] >= 2)
var _projectsWithToLittleResponses = Filter(_byProject, [@numberOfActualParticipants] < 2)

var _projectsInCluster = Filter(_projectsWithEnoughResponses, [@avg] >= _fromEqual && [@avg] < _toLower)

return  --COUNTROWS(_activeSurveysInWeek) --coalesce(CALCULATE(COUNTROWS(DimProjectSurvey), DimProjectSurvey[SurveyStartDate] <= _minDate , DimProjectSurvey[SurveyEndDate] >= _maxDate), 0)
    if(_cluster == "Gray"
        , COUNTROWS(_projectsWithToLittleResponses)
        , COUNTROWS(_projectsInCluster))

--CONCATENATEX(_projectsWithToLittleResponses, DimProjectSurvey[ProjectNumber], " - ")
```


## Table: DimRejected

### Measures:


```dax
# Rejected = COUNTROWS(DISTINCT(DimRejected[projectnumber_adj]))
```



```dax
Reason = if(HASONEVALUE(DimProjects[ProjectNumber_adj]), LOOKUPVALUE(DimRejected[SurveyReasonID], DimRejected[projectnumber_adj], SELECTEDVALUE(DimProjects[ProjectNumber_adj])))
```


## Table: SurveyCampaignNumOfParticipantsPerPM

### Measures:


```dax
NumberOfActiveParticipants by PM = sum(SurveyCampaignNumOfParticipantsPerPM[NumberOfActiveParticipants])
```



```dax
NumberOfActiveCommitments by PM = sum(SurveyCampaignNumOfParticipantsPerPM[NumberOfActiveCommitments]) 
```


## Table: SurveyParticipantsPerCampaign

### Measures:


```dax
IsParticipantActiveInWeek = 
var _week = Selectedvalue(DimDate[Year-CW])
var _partId = Selectedvalue(DimParticipants[SurveyParticipantID])
var _over = [Overall Average]

return   calculate( COUNTROWS(SurveyParticipantsPerCampaign), SurveyParticipantsPerCampaign[ParticipantID] = _partId)
```


### Calculated Columns:


```dax
Participant = LOOKUPVALUE(DimParticipants[Participant], DimParticipants[SurveyParticipantID], SurveyParticipantsPerCampaign[ParticipantID]) 
```



```dax
jobcode = LOOKUPVALUE(DimParticipants[jobcode], DimParticipants[SurveyParticipantID], SurveyParticipantsPerCampaign[ParticipantID]) 
```

