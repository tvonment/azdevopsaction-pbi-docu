



# DAX

|Dataset|[My Client Satisfaction](./../My-Client-Satisfaction.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: msfp_surveyresponses

### Measures:


```dax
Rolling Count of Feedbacks = 
VAR LastSelectedDate = MAX(msfp_surveyresponses[msfp_submitdate (bins)])
VAR Period = DATESINPERIOD(msfp_surveyresponses[msfp_submitdate (bins)], LastSelectedDate, -12, MONTH)
VAR Result =
    CALCULATE(COUNT('msfp_surveyresponses'[msfp_sourceresponseidentifier]),
        Period
    )
RETURN
    Result
```



```dax
Count of Feedbacks = COUNT('msfp_surveyresponses'[msfp_sourceresponseidentifier])+0
```



```dax
Count of Feedbacks LTM = 
CALCULATE(
   [Count of Feedbacks],
   DATESBETWEEN('Calendar'[Date], EDATE(MAX('Calendar'[Date]), -12)+1, MAX('Calendar'[Date]))
)
```



```dax
cnt_ltm_tst_v1 = 
CALCULATE (
   [Count of Feedbacks],
   DATESINPERIOD (
      msfp_surveyresponses[createdon (bins)],          -- returns period from date column
      MAX ( msfp_surveyresponses[createdon (bins)] ),  -- starting from MAX date
      -12,                   -- shifting it back 12 intervals
      MONTH                  -- each interval being a month
    )
)
```



```dax
cnt_ltm_tst_v2 = 
VAR EndDate =
    MAX(msfp_surveyresponses[createdon (bins)])       -- retrieves MAX Date   
                
VAR StartDate =
    EDATE( EndDate, -12 ) + 1 -- shifts EndDate to year beginning
 
VAR Result =
    CALCULATE(
         [Count of Feedbacks],
         -- retrieves the relevant date range
         DATESBETWEEN(msfp_surveyresponses[createdon (bins)], StartDate, EndDate )
    )
RETURN
     Result
```



```dax
Recommendation Likelihood = IF(HASONEVALUE(msfp_surveyresponses[msfp_name]), CALCULATE(SUM(msfp_questionresponses[msfp_response_numeric]), FILTER(msfp_questions, msfp_questions[msfp_name]="How likely are you to recommend Roland Berger to a colleague or friend?")))
```



```dax
Client Quote = CONCATENATE(IF(HASONEVALUE(msfp_surveyresponses[msfp_name]), CALCULATE(CONCATENATEX(msfp_questionresponses, msfp_questionresponses[msfp_response], ""), FILTER(msfp_questions, msfp_questions[msfp_questionid] in {"6e39951c-6dfb-ec11-82e5-000d3a449610", "7039951c-6dfb-ec11-82e5-000d3a449610"})), " "), " ")
```



```dax
Approval for Use = IF(HASONEVALUE(msfp_surveyresponses[msfp_name]), CONCATENATE(CALCULATE(CONCATENATEX(msfp_questionresponses, msfp_questionresponses[msfp_response], ""), FILTER(msfp_questions, msfp_questions[msfp_questionid] in {"6f39951c-6dfb-ec11-82e5-000d3a449610"})), CONCATENATE(UNICHAR(10), CALCULATE(CONCATENATEX(msfp_questionresponses, msfp_questionresponses[msfp_response], ""), FILTER(msfp_questions, msfp_questions[msfp_questionid]="ebe0a548-f117-ed11-b83e-0022488188da")))), " ")
```



```dax
Other Expectations = CONCATENATE(IF(HASONEVALUE(msfp_surveyresponses[msfp_name]), CALCULATE(CONCATENATEX(msfp_questionresponses, msfp_questionresponses[msfp_response], ""), FILTER(msfp_questions, msfp_questions[msfp_questionid] in {"7139951c-6dfb-ec11-82e5-000d3a449610"})), " "), " ")
```



```dax
Project = IF(SELECTEDVALUE(msfp_surveyresponses[msfp_name]), MIN(nxtgn_projects[nxtgn_projecttitleorig]), "")
```



```dax
Account = IF(SELECTEDVALUE(msfp_surveyresponses[msfp_name]), MIN(nxtgn_projects[nxtgn_accountname]), "")
```



```dax
Respondent = IF(SELECTEDVALUE(msfp_surveyresponses[msfp_name]), MIN(msfp_surveyresponses[msfp_respondent]), "")
```



```dax
Feedback Date = IF(SELECTEDVALUE(msfp_surveyresponses[msfp_name]), MIN(msfp_surveyresponses[msfp_submitdate]), "")
```



```dax
Involved in Hiring Decison = IF(SELECTEDVALUE(msfp_surveyresponses[msfp_name]), CALCULATE(MIN(msfp_questionresponses[msfp_response]), FILTER(msfp_questions, msfp_questions[msfp_questionid] in {"6139951c-6dfb-ec11-82e5-000d3a449610"})), " ")
```


### Calculated Columns:


```dax
createdon (bins) = IF(
  ISBLANK('msfp_surveyresponses'[createdon]),
  BLANK(),
  DATE(
    YEAR('msfp_surveyresponses'[createdon]),
    1 + (MONTH('msfp_surveyresponses'[createdon]) - 1),
    1
  )
)
```



```dax
msfp_submitdate (bins) = IF(
  ISBLANK('msfp_surveyresponses'[msfp_submitdate]),
  BLANK(),
  DATE(
    YEAR('msfp_surveyresponses'[msfp_submitdate]),
    1 + (MONTH('msfp_surveyresponses'[msfp_submitdate]) - 1),
    1
  )
)
```



```dax
url = 
// CONCATENATE("https://rolandberger.crm4.dynamics.com/main.aspx?appid=9e3de84b-a781-ea11-a811-000d3a253a0e&newWindow=true&pagetype=entityrecord&etn=msfp_surveyresponse&id=", msfp_surveyresponses[activityid])
CONCATENATE("https://app.powerbi.com/groups/me/apps/01dda475-c69d-41ea-8b49-ba1faac988f8/reports/becd71e0-b898-4ee6-be65-5468490bd52d/ReportSection499234e243e535c996d8?filter=msfp_surveyresponses/msfp_name eq '", CONCATENATE(msfp_surveyresponses[msfp_name], "'"))
```



```dax
name = CONCATENATE(RELATED(nxtgn_customersurveytriggers[nxtgn_name]), CONCATENATE(" (", CONCATENATE(FORMAT(msfp_surveyresponses[msfp_startdate], "Short Date"), CONCATENATE(" ", CONCATENATE(FORMAT(msfp_surveyresponses[msfp_startdate], "Short Time"), ")")))))
```


## Table: msfp_questionresponses

### Measures:


```dax
Average of msfp_response_numeric average per createdon (bins) = 
AVERAGEX(
	KEEPFILTERS(VALUES('msfp_questionresponses'[createdon (bins)])),
	CALCULATE(AVERAGE('msfp_questionresponses'[msfp_response_numeric]))
)
```



```dax
Count of msfp_questionresponseid = COUNT(msfp_questionresponses[msfp_questionresponseid])
```



```dax
Rolling Average NPS (over Months) = 
VAR LastSelectedDate = MAX(msfp_questionresponses[createdon (bins)])
VAR Period = DATESINPERIOD(msfp_questionresponses[createdon (bins)], LastSelectedDate, -12, MONTH)
VAR Result =
    CALCULATE(
        AVERAGEX(
	        KEEPFILTERS(VALUES('msfp_questionresponses'[createdon (bins)])),
	        CALCULATE(AVERAGE('msfp_questionresponses'[msfp_response_numeric]))
        ),
        Period
    )
RETURN
    Result
```



```dax
Rolling Average NPS = 
VAR LastSelectedDate = MAX(msfp_questionresponses[createdon (bins)])
VAR Period = DATESINPERIOD(msfp_questionresponses[createdon (bins)], LastSelectedDate, -12, MONTH)
VAR Result =
    CALCULATE(AVERAGE('msfp_questionresponses'[msfp_response_numeric]),
        Period
    )
RETURN
    Result
```



```dax
count_yes = CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, msfp_questionresponses[msfp_response]="Yes"))
```



```dax
NPS = (SUM(msfp_questionresponses[promoter])/COUNT(msfp_questionresponses[_msfp_surveyresponseid_value]) - SUM(msfp_questionresponses[detractor])/COUNT(msfp_questionresponses[_msfp_surveyresponseid_value])) * 100
```



```dax
NPS LTM = 
CALCULATE (
   [NPS],
   DATESBETWEEN('Calendar'[Date], EDATE(MAX('Calendar'[Date]), -12) + 1, MAX('Calendar'[Date]))
)+0
```



```dax
Global NPS = CALCULATE([NPS], REMOVEFILTERS(systemusers))
```



```dax
Global NPS LTM = CALCULATE([NPS LTM], REMOVEFILTERS(systemusers))
```



```dax
Platform NPS = CALCULATE([NPS], FILTER(ALL(systemusers), systemusers[_nxtgn_platformid_value] IN VALUES(systemusers[_nxtgn_platformid_value])))
```



```dax
Platform NPS LTM = CALCULATE([NPS LTM], FILTER(ALL(systemusers), systemusers[_nxtgn_platformid_value] IN VALUES(systemusers[_nxtgn_platformid_value])))
```



```dax
Country NPS = CALCULATE([NPS], FILTER(ALL(systemusers), systemusers[_nxtgn_lookupcountryid_value] IN VALUES(systemusers[_nxtgn_lookupcountryid_value])))
```



```dax
Country NPS LTM = CALCULATE([NPS LTM], FILTER(ALL(systemusers), systemusers[_nxtgn_lookupcountryid_value] IN VALUES(systemusers[_nxtgn_lookupcountryid_value])))
```



```dax
Satisfaction Level = IF(OR(ISFILTERED(msfp_surveyresponses[name]), ISFILTERED(msfp_surveyresponses[msfp_name])), SUM(msfp_questionresponses[msfp_response_numeric]))
```


### Calculated Columns:


```dax
createdon (bins) = IF(
  ISBLANK('msfp_questionresponses'[createdon]),
  BLANK(),
  DATE(
    YEAR('msfp_questionresponses'[createdon]),
    1 + (MONTH('msfp_questionresponses'[createdon]) - 1),
    1
  )
)
```



```dax
promoter = IF(AND(msfp_questionresponses[_msfp_questionid_value] = "6c39951c-6dfb-ec11-82e5-000d3a449610", msfp_questionresponses[msfp_response_numeric] >= 9), 1, 0)
```



```dax
detractor = IF(AND(msfp_questionresponses[_msfp_questionid_value] = "6c39951c-6dfb-ec11-82e5-000d3a449610", msfp_questionresponses[msfp_response_numeric] <= 6), 1, 0)
```


## Table: msfp_questions

### Calculated Columns:


```dax
sort_expectation_satisfaction = IF(msfp_questions[msfp_sourceparentquestionidentifier]="rb8d0e0a1efba4c4c825b51dcd6673fc9", msfp_questions[msfp_order], 0)
```



```dax
msfp_name_expectation_satisfaction = IF(msfp_questions[msfp_sourceparentquestionidentifier]="rb8d0e0a1efba4c4c825b51dcd6673fc9", msfp_questions[msfp_name], BLANK())
```


## Table: nxtgn_projects

### Measures:


```dax
Reference Country Name = IF(HASONEVALUE(systemusers[systemuserid]), LOOKUPVALUE(nxtgn_lookupcountries[nxtgn_name], nxtgn_lookupcountries[nxtgn_lookupcountryid], MIN(systemusers[_nxtgn_lookupcountryid_value])), "")
```



```dax
Reference Platform Name = IF(HASONEVALUE(systemusers[systemuserid]), LOOKUPVALUE(nxtgn_lookupplatforms[nxtgn_name], nxtgn_lookupplatforms[nxtgn_lookupplatformid], MIN(systemusers[_nxtgn_platformid_value])), "")
```



```dax
Reference Platform = IF(HASONEVALUE(systemusers[systemuserid]), MIN(systemusers[_nxtgn_platformid_value]), "")
```



```dax
Reference Country = IF(HASONEVALUE(systemusers[systemuserid]), MIN(systemusers[_nxtgn_lookupcountryid_value]), "")
```


### Calculated Columns:


```dax
nxtgn_project_planned_enddate (bins) = IF(
  ISBLANK('nxtgn_projects'[nxtgn_project_planned_enddate]),
  BLANK(),
  DATE(
    YEAR('nxtgn_projects'[nxtgn_project_planned_enddate]),
    1 + (MONTH('nxtgn_projects'[nxtgn_project_planned_enddate]) - 1),
    1
  )
)
```


## Table: Calendar


```dax
CALENDAR(DATE(2022, 10, 01), TODAY())
```


### Calculated Columns:


```dax
Month = IF(
  ISBLANK('Calendar'[Date]),
  BLANK(),
  DATE(
    YEAR('Calendar'[Date]),
    1 + (MONTH('Calendar'[Date]) - 1),
    1
  )
)
```


## Table: nxtgn_customersurveytriggers

### Calculated Columns:


```dax
url = CONCATENATE("https://rolandberger.crm4.dynamics.com/main.aspx?appid=9e3de84b-a781-ea11-a811-000d3a253a0e&pagetype=entityrecord&etn=nxtgn_customersurveytrigger&id=", nxtgn_customersurveytriggers[nxtgn_customersurveytriggerid])
```



```dax
nxtgn_surveystatus_meta (groups) = SWITCH(
  TRUE,
  ISBLANK('nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]),
  "(Blank)",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Open"},
  "Due",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Canceled",
    "Postponed",
    "Ready for sending"},
  "Handled (not sent)",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Received"},
  "Received",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Sent"},
  "Requested",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]
)
```


## Table: Switch NPS Benchmark

### Measures:


```dax
Switch Measure = 
SUMX (
'Switch NPS Benchmark',
SWITCH (
[ID],
1, [Benchmark Global NPS LTM],
2, [Benchmark Platform NPS LTM],
3, [NPS LTM],
4, [Benchmark Country NPS LTM]
)
)
```


## Table: msfp_questions_individual

### Measures:


```dax
response = IF(SELECTEDVALUE(msfp_surveyresponses[msfp_name]), IF(CALCULATE(COUNT(msfp_questionresponses_individual[msfp_response])+0, FILTER(msfp_questionresponses_individual, AND(msfp_questionresponses_individual[msfp_response] = SELECTEDVALUE(msfp_questions_individual[msfp_questionchoices_hiring_reasons]), msfp_questionresponses_individual[msfp_sourcequestionidentifier] in {"rbb8f26c4b93e47a0b496c33f2d950976", "ra1d75a442036487996bef3757fbe54bd", "r4947ae3fb4fc4bf2852d9c93763bdbee", "r2a9ca3f84b8a444f86635189bf28bec1"})))>0, "✅", "⬜"), "⬜")
```


### Calculated Columns:


```dax
msfp_questionchoices_hiring_reasons_sort = IF(msfp_questions_individual[msfp_sourcequestionidentifier] in {"rbb8f26c4b93e47a0b496c33f2d950976", "ra1d75a442036487996bef3757fbe54bd", "r4947ae3fb4fc4bf2852d9c93763bdbee", "r2a9ca3f84b8a444f86635189bf28bec1"}, msfp_questions_individual[msfp_questionchoices_order])
```



```dax
msfp_questionchoices_hiring_reasons = IF(msfp_questions_individual[msfp_sourcequestionidentifier] in {"rbb8f26c4b93e47a0b496c33f2d950976", "ra1d75a442036487996bef3757fbe54bd", "r4947ae3fb4fc4bf2852d9c93763bdbee", "r2a9ca3f84b8a444f86635189bf28bec1"}, msfp_questions_individual[msfp_questionchoices])
```


## Table: NPS Benchmark LTM

### Measures:


```dax
Benchmark Global NPS LTM = (SUM('NPS Benchmark LTM'[promoter])/COUNT('NPS Benchmark LTM'[_msfp_surveyresponseid_value]) - SUM('NPS Benchmark LTM'[detractor])/COUNT('NPS Benchmark LTM'[_msfp_surveyresponseid_value])) * 100
```



```dax
Benchmark Country NPS LTM = CALCULATE('NPS Benchmark LTM'[Benchmark Global NPS LTM], FILTER('NPS Benchmark LTM', 'NPS Benchmark LTM'[nxtgn_deliverymanagerid._nxtgn_lookupcountryid_value] = [Reference Country]))
```



```dax
Benchmark Platform NPS LTM = CALCULATE('NPS Benchmark LTM'[Benchmark Global NPS LTM], FILTER('NPS Benchmark LTM', 'NPS Benchmark LTM'[nxtgn_deliverymanagerid._nxtgn_platformid_value] = [Reference Platform]))
```


### Calculated Columns:


```dax
promoter = IF('NPS Benchmark LTM'[msfp_response] >= 9, 1, 0)
```



```dax
detractor = IF('NPS Benchmark LTM'[msfp_response] <= 6, 1, 0)
```


## Table: Project Status Benchmark LTM

### Calculated Columns:


```dax
nxtgn_surveystatus_meta (groups) = SWITCH(
  TRUE,
  ISBLANK('Project Status Benchmark LTM'[nxtgn_surveystatus_meta]),
  "(Blank)",
  'Project Status Benchmark LTM'[nxtgn_surveystatus_meta] IN {"Open"},
  "Due",
  'Project Status Benchmark LTM'[nxtgn_surveystatus_meta] IN {"Canceled",
    "Postponed",
    "Ready for sending"},
  "Handled (not sent)",
  'Project Status Benchmark LTM'[nxtgn_surveystatus_meta] IN {"Received"},
  "Received",
  'Project Status Benchmark LTM'[nxtgn_surveystatus_meta] IN {"Sent"},
  "Requested",
  'Project Status Benchmark LTM'[nxtgn_surveystatus_meta]
)
```

