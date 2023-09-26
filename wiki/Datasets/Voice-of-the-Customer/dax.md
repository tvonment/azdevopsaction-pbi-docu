



# DAX

|Dataset|[Voice of the Customer](./../Voice-of-the-Customer.md)|
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
NPS = 100 * CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, AND(msfp_questionresponses[msfp_response_numeric]>=9, TRUE)))/COUNT(msfp_questionresponses[msfp_questionresponseid]) - CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, AND(msfp_questionresponses[msfp_response_numeric]<=6, TRUE)))/COUNT(msfp_questionresponses[msfp_questionresponseid]) +0
```



```dax
count_yes = CALCULATE(COUNT(msfp_questionresponses[msfp_questionresponseid]), FILTER(msfp_questionresponses, msfp_questionresponses[msfp_response]="Yes"))
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


## Table: nxtgn_opportunityclosereasons

### Measures:


```dax
share_reason = DISTINCTCOUNT(nxtgn_opportunityclosereasons[_nxtgn_opportunityid_value])/CALCULATE([count_won_opportunities]+[count_lost_opportunities]+[count_dropped_opportunities], REMOVEFILTERS(nxtgn_lookupopportunitystatusreasons[nxtgn_name], nxtgn_lookupopportunitystatusreasons[nxtgn_category_meta]))
```



```dax
share_category = DISTINCTCOUNT(nxtgn_opportunityclosereasons[_nxtgn_opportunityid_value])/CALCULATE([count_won_opportunities]+[count_lost_opportunities]+[count_dropped_opportunities], REMOVEFILTERS(nxtgn_lookupopportunitystatusreasons[nxtgn_category_meta]))
```


## Table: nxtgn_opportunityregistrations

### Measures:


```dax
count_won_opportunities = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"))+0
```



```dax
count_lost_opportunities = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Lost"))+0
```



```dax
count_dropped_opportunities = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Dropped"))+0
```



```dax
conversion_rate = [count_won_opportunities]/([count_won_opportunities]+[count_lost_opportunities]+[count_dropped_opportunities])
```



```dax
sum_won_revenue_base = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won"))+0
```



```dax
sum_lost_revenue_base = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Lost"))+0
```



```dax
sum_dropped_revenue_base = CALCULATE(SUM(nxtgn_opportunityregistrations[nxtgn_estrevenue_base]), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[statuscode_meta]="Closed as Dropped"))+0
```



```dax
conversion_rate_revenue = [sum_won_revenue_base]/([sum_won_revenue_base]+[sum_lost_revenue_base]+[sum_dropped_revenue_base])
```



```dax
share_won_opportunities = [count_won_opportunities]/COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid])
```



```dax
share_closed_won_lost_without_competitor = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, AND(OR(nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won", nxtgn_opportunityregistrations[statuscode_meta]="Closed as Lost"), ISBLANK(nxtgn_opportunityregistrations[competitor]))))/CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]), FILTER(nxtgn_opportunityregistrations, OR(nxtgn_opportunityregistrations[statuscode_meta]="Closed as Won", nxtgn_opportunityregistrations[statuscode_meta]="Closed as Lost")))+0
```



```dax
count_opportunities = CALCULATE(COUNT(nxtgn_opportunityregistrations[nxtgn_opportunityregistrationid]))+0
```


### Calculated Columns:


```dax
nxtgn_actualclosedate (bins) = IF(
  ISBLANK('nxtgn_opportunityregistrations'[nxtgn_actualclosedate]),
  BLANK(),
  DATE(
    YEAR('nxtgn_opportunityregistrations'[nxtgn_actualclosedate]),
    1 + (MONTH('nxtgn_opportunityregistrations'[nxtgn_actualclosedate]) - 1),
    1
  )
)
```



```dax
nxtgn_actualclosedate (year) = IF(
  ISBLANK('nxtgn_opportunityregistrations'[nxtgn_actualclosedate]),
  BLANK(),
  DATE(YEAR('nxtgn_opportunityregistrations'[nxtgn_actualclosedate]), 1, 1)
)
```



```dax
competitor = IF(RELATED(competitors[name]) = "Other Competitor", nxtgn_opportunityregistrations[nxtgn_othercompetitors], RELATED(competitors[name]))
```



```dax
count_close_reasons = COUNTROWS(RELATEDTABLE(nxtgn_opportunityclosereasons))+0
```



```dax
nxtgn_closereasons_concatenate_wo_other_reasons = SUBSTITUTE(nxtgn_opportunityregistrations[nxtgn_closereasons_concatenate], "Other Reasons ", "", 1)
```



```dax
nxtgn_estrevenue_base_buckets = IF(nxtgn_opportunityregistrations[nxtgn_estrevenue_base] >= 400000, ">= 400.000 €", "< 400.000 €")
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
Count of Survey Triggers = CALCULATE(COUNTROWS(nxtgn_customersurveytriggers), REMOVEFILTERS(nxtgn_customersurveytriggers[nxtgn_surveystatus_meta_due_handled], nxtgn_customersurveytriggers[nxtgn_surveystatus_meta_handled]))
```



```dax
Handling Rate = [Handled Surveys]/[Total Projects Unfiltered]
```



```dax
Sent Surveys = CALCULATE(DISTINCTCOUNT(nxtgn_customersurveytriggers[_nxtgn_projectid_value]), FILTER(nxtgn_customersurveytriggers, nxtgn_customersurveytriggers[nxtgn_surveystatus_meta_handled]="Sent to client"))
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
Send Rate = [Sent Surveys]/[Handled Surveys]
```



```dax
Received Surveys = CALCULATE(DISTINCTCOUNT(nxtgn_customersurveytriggers[_nxtgn_projectid_value]), FILTER(nxtgn_customersurveytriggers, nxtgn_customersurveytriggers[nxtgn_surveystatus_meta]="Received"))+0
```



```dax
Return Rate = [Received Surveys]/[Sent Surveys]
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

