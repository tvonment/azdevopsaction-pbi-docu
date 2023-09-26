



# DAX

|Dataset|[Client Satisfaction Report](./../Client-Satisfaction-Report.md)|
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
Recommendation Likelihood = CALCULATE(SUM(msfp_questionresponses[msfp_response_numeric]), FILTER(msfp_questions, msfp_questions[msfp_name]="How likely are you to recommend Roland Berger to a colleague or friend?"))
```



```dax
Average Expectation Satisfaction = CALCULATE(SUM(msfp_questionresponses[msfp_response_numeric]), FILTER(msfp_questions, msfp_questions[msfp_sourceparentquestionidentifier]="rb8d0e0a1efba4c4c825b51dcd6673fc9"))/CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questions, msfp_questions[msfp_sourceparentquestionidentifier]="rb8d0e0a1efba4c4c825b51dcd6673fc9"))
```



```dax
Rank Perfect Feedbacks = CALCULATE(SUM(msfp_surveyresponses[msfp_sourceresponseidentifier]), FILTER(msfp_surveyresponses, AND([Recommendation Likelihood]=10, [Average Expectation Satisfaction]=5)))
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
NPS = 100 * (CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, AND(msfp_questionresponses[msfp_response_numeric]>=9, TRUE)))/COUNT(msfp_questionresponses[msfp_questionresponseid]) - CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, AND(msfp_questionresponses[msfp_response_numeric]<=6, TRUE)))/COUNT(msfp_questionresponses[msfp_questionresponseid])) +0
```



```dax
count_yes = CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, msfp_questionresponses[msfp_response]="Yes"))
```



```dax
nxtgn_projects_nxtgn_project_planned_enddate_calendar = CALENDAR(DATE(2022,01,01), DATE(2023,01,01))
```



```dax
Promotors = CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, AND(msfp_questionresponses[msfp_response_numeric]>=9, TRUE)))/COUNT(msfp_questionresponses[msfp_questionresponseid]) +0
```



```dax
Detractors = CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, AND(msfp_questionresponses[msfp_response_numeric]<=6, TRUE)))/COUNT(msfp_questionresponses[msfp_questionresponseid]) +0
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


## Table: nxtgn_projects

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



```dax
nxtgn_budget_base_bucket = IF(nxtgn_projects[nxtgn_budget_base] < 100000, "< 100.000 EUR", ">= 100.000 EUR")
```


## Table: nxtgn_customersurveytriggers

### Measures:


```dax
Count of Survey Triggers = COUNT(nxtgn_customersurveytriggers[nxtgn_customersurveytriggerid])+0
```



```dax
Handling Rate = [Handled Surveys]/[Total Projects Unfiltered]
```



```dax
Sent Surveys = CALCULATE([Count of Survey Triggers], FILTER(nxtgn_customersurveytriggers, nxtgn_customersurveytriggers[nxtgn_surveystatus_meta (groups)] in {"Requested", "Received"}))+0
```



```dax
Total Projects Filtered = CALCULATE(DISTINCTCOUNT(nxtgn_customersurveytriggers[_nxtgn_projectid_value]))+0
```



```dax
Handled Surveys = CALCULATE(DISTINCTCOUNT(nxtgn_customersurveytriggers[_nxtgn_projectid_value]), FILTER(nxtgn_customersurveytriggers, nxtgn_customersurveytriggers[nxtgn_surveystatus_meta_due_handled]="Handled"))+0
```



```dax
Total Projects Unfiltered = CALCULATE(DISTINCTCOUNT(nxtgn_customersurveytriggers[_nxtgn_projectid_value]), REMOVEFILTERS(nxtgn_customersurveytriggers[nxtgn_surveystatus_meta], nxtgn_customersurveytriggers[nxtgn_surveystatus_meta_due_handled], nxtgn_customersurveytriggers[nxtgn_surveystatus_meta_handled]))+0
```



```dax
Send Rate = IF([Count of Survey Triggers]>0, [Sent Surveys]/[Count of Survey Triggers], 0)
```



```dax
Received Surveys = CALCULATE([Count of Survey Triggers], FILTER(nxtgn_customersurveytriggers, nxtgn_customersurveytriggers[nxtgn_surveystatus_meta (groups)]="Received"))+0
```



```dax
Answer Rate = IF([Sent Surveys]>0, [Received Surveys]/[Sent Surveys], 0)
```


### Calculated Columns:


```dax
nxtgn_surveystatus_meta_total = SWITCH(
  TRUE,
  ISBLANK('nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]),
  "(Blank)",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Canceled",
    "No feedback received",
    "Open",
    "Postponed",
    "Ready for sending",
    "Received"},
  "Total",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]
)
```



```dax
nxtgn_surveystatus_meta_due_handled = SWITCH(
  TRUE,
  ISBLANK('nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]),
  "(Blank)",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Open"},
  "Due",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Canceled",
    "No feedback received",
    "Postponed",
    "Ready for sending",
    "Received"},
  "Handled",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]
)
```



```dax
nxtgn_surveystatus_meta_handled = SWITCH(
  TRUE,
  ISBLANK('nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]),
  "(Blank)",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Canceled"},
  "Canceled",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Open"},
  "Open",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Postponed"},
  "Postponed",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"Ready for sending"},
  "Ready for sending",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"No feedback received",
    "Received"},
  "Sent to client",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]
)
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
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta] IN {"No feedback received"},
  "Requested",
  'nxtgn_customersurveytriggers'[nxtgn_surveystatus_meta]
)
```


## Table: nxtgn_projects_nxtgn_project_planned_enddate


```dax
CALENDAR(EOMONTH(TODAY(), -12)+1, EOMONTH(TODAY(), 0))
```


### Calculated Columns:


```dax
nxtgn_project_planned_enddate (bins) = IF(
  ISBLANK('nxtgn_projects_nxtgn_project_planned_enddate'[nxtgn_project_planned_enddate]),
  BLANK(),
  DATE(
    YEAR('nxtgn_projects_nxtgn_project_planned_enddate'[nxtgn_project_planned_enddate]),
    1 + (MONTH('nxtgn_projects_nxtgn_project_planned_enddate'[nxtgn_project_planned_enddate]) - 1),
    1
  )
)
```

