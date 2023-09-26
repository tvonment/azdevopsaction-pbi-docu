



# DAX

|Dataset|[CRM Contacts](./../CRM-Contacts.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: contact

### Measures:


```dax
count_dq_approved = 
CALCULATE(
	COUNTA('contact'[contactid]),
	'contact'[nxtgn_dqapproved] IN { TRUE }
)+0
```



```dax
count_prebounced = 
CALCULATE(
	COUNTA('contact'[contactid]),
	'contact'[nxtgn_prebounced] IN { TRUE }
)+0
```



```dax
count_postbounced = 
CALCULATE(
	COUNTA('contact'[contactid]),
	'contact'[nxtgn_postbounced] IN { TRUE }
)+0
```



```dax
count_left_company = 
CALCULATE(
	COUNTA('contact'[contactid]),
	'contact'[statuscodename]
		IN { "Left Company – Change in Dyn365" }
)+0
```



```dax
count_missing_email = 
CALCULATE(COUNTA('contact'[contactid]), ISBLANK('contact'[emailaddress1]))+0
```



```dax
count_optoutfromall = 
CALCULATE(
	COUNTA('contact'[contactid]),
	'contact'[donotsendmarketingmaterialname] IN { "Yes" }
)+0
```



```dax
count_missing_gender = 
CALCULATE(COUNTA('contact'[contactid]), ISBLANK('contact'[gendercodename]))+0
```



```dax
count_linkedin_not_at_company = 
CALCULATE(
	COUNTA('contact'[contactid]),
	'contact'[msdyn_orgchangestatusname] IN { "Not at Company" }
)+0
```



```dax
count_dq_not_approved = 
CALCULATE(
	COUNTA('contact'[contactid]),
	OR(ISBLANK('contact'[nxtgn_dqapprovedname]), NOT(contact[nxtgn_dqapproved]))
)+0
```



```dax
share_postbounced = 
DIVIDE([count_postbounced], COUNTA('contact'[contactid]))
```



```dax
share_postbounced_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), 'contact'[nxtgn_postbounced], ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
count_postbounced_overall = CALCULATE(COUNTA(contact[contactid]), contact[nxtgn_postbounced], ALL())+0
```



```dax
share_prebounced = 
DIVIDE([count_prebounced], COUNTA('contact'[contactid]))
```



```dax
share_prebounced_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), 'contact'[nxtgn_prebounced], ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
count_dq_not_approved_overall = 
CALCULATE(
	COUNTA('contact'[contactid]),
	OR(ISBLANK('contact'[nxtgn_dqapprovedname]), NOT(contact[nxtgn_dqapproved])),
    ALL()
)+0
```



```dax
share_dq_not_approved_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]),
	OR(ISBLANK('contact'[nxtgn_dqapprovedname]), NOT(contact[nxtgn_dqapproved])),
    ALL()
), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
share_dq_not_approved = 
DIVIDE([count_dq_not_approved], COUNTA('contact'[contactid]))
```



```dax
share_optoutfromall_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), 'contact'[donotsendmarketingmaterialname]="Yes", ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
share_optoutfromall = DIVIDE(contact[count_optoutfromall], COUNTA(contact[contactid]))
```



```dax
share_left_company = 
DIVIDE([count_left_company], COUNTA('contact'[contactid]))
```



```dax
share_left_company_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), 'contact'[statuscodename] IN { "Left Company – Change in Dyn365" }, ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
share_linkedin_not_at_company = 
DIVIDE([count_linkedin_not_at_company], COUNTA('contact'[contactid]))
```



```dax
share_linkedin_not_at_company_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), 'contact'[msdyn_orgchangestatusname]="Not at Company", ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
share_missing_email = DIVIDE(contact[count_missing_email], COUNTA(contact[contactid]))
```



```dax
share_missing_gender = DIVIDE(contact[count_missing_gender], COUNTA(contact[contactid]))
```



```dax
share_missing_email_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), ISBLANK(contact[emailaddress1]), ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
share_missing_gender_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), ISBLANK(contact[gendercodename]), ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
share_postbounced_included_in_mailing = DIVIDE(CALCULATE(COUNTA(contact[contactid]), contact[nxtgn_postbounced]), CALCULATE(COUNTA(contact[contactid]), NOT(ISBLANK(contact[lastusedincampaign]))))+0
```



```dax
share_optoutfromall_included_in_mailing = DIVIDE(CALCULATE(COUNTA(contact[contactid]), contact[donotsendmarketingmaterialname]="Yes"), CALCULATE(COUNTA(contact[contactid]), NOT(ISBLANK(contact[lastusedincampaign]))))+0
```



```dax
share_dq_issue = DIVIDE(CALCULATE(COUNTA(contact[contactid]), contact[dq_issue]), COUNTA(contact[contactid]))
```



```dax
delta_dq_not_approved_overall = 
[share_dq_not_approved_overall] - [share_dq_not_approved]
```



```dax
delta_prebounced = 
[share_prebounced_overall] - [share_prebounced]
```



```dax
delta_postbounced = [share_postbounced_overall] - [share_postbounced]
```



```dax
delta_left_company = 
[share_left_company_overall] - [share_left_company]
```



```dax
delta_linkedin_not_at_company = 
[share_linkedin_not_at_company_overall] - [share_linkedin_not_at_company]
```



```dax
delta_missing_email = 
[share_missing_email_overall] - [share_missing_email]
```



```dax
delta_missing_gender = 
[share_missing_gender_overall] - [share_missing_gender]
```



```dax
delta_optoutfromall = 
[share_optoutfromall_overall] - [share_optoutfromall]
```



```dax
share_dq_issue_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), contact[dq_issue], ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
count_dq_issue = 
CALCULATE(
	COUNTA('contact'[contactid]),
	contact[dq_issue]
)+0
```



```dax
share_classification_issue = DIVIDE(CALCULATE(COUNTA(contact[contactid]), contact[classification_issue]), COUNTA(contact[contactid]))
```



```dax
share_classification_issue_overall = DIVIDE(CALCULATE(
	COUNTA('contact'[contactid]), contact[classification_issue], ALL()), CALCULATE(COUNTA(contact[contactid]), ALL()))
```



```dax
color_dq_not_approved = IF([delta_dq_not_approved_overall]<0, "#E01B22", IF(contact[count_dq_approved]=0, "#37A42C", "#F08A00"))
```



```dax
color_missing_gender = IF([delta_missing_gender]<0, "#E01B22", IF(contact[count_missing_gender]=0, "#37A42C", "#F08A00"))
```



```dax
color_left_company = IF([delta_left_company]<0, "#E01B22", IF(contact[count_left_company]=0, "#37A42C", "#F08A00"))
```



```dax
color_linkedin_not_at_company = IF([delta_linkedin_not_at_company]<0, "#E01B22", IF(contact[count_linkedin_not_at_company]=0, "#37A42C", "#F08A00"))
```



```dax
color_missing_email = IF([delta_missing_email]<0, "#E01B22", IF(contact[count_missing_email]=0, "#37A42C", "#F08A00"))
```



```dax
color_prebounced = IF([delta_prebounced]<0, "#E01B22", IF(contact[count_prebounced]=0, "#37A42C", "#F08A00"))
```



```dax
color_postbounced = IF([delta_postbounced]<0, "#E01B22", IF(contact[count_postbounced]=0, "#37A42C", "#F08A00"))
```



```dax
color_optoutfromall = IF([delta_optoutfromall]<0, "#E01B22", IF(contact[count_optoutfromall]=0, "#37A42C", "#F08A00"))
```


### Calculated Columns:


```dax
sync_with_outlook = OR(contact[nxtgn_dqapproved], AND(NOT(contact[nxtgn_dqapproved]), contact[nxtgn_approvalreverted]))
```



```dax
lastusedincampaign (bins) = IF(
  ISBLANK('contact'[lastusedincampaign]),
  BLANK(),
  DATE(
    YEAR('contact'[lastusedincampaign]),
    1 + (MONTH('contact'[lastusedincampaign]) - 1),
    1
  )
)
```



```dax
url = CONCATENATE("https://rolandberger.crm4.dynamics.com/main.aspx?appid=9e3de84b-a781-ea11-a811-000d3a253a0e&forceUCI=1&pagetype=entityrecord&etn=contact&id=", contact[contactid])
```



```dax
dq_issue = OR(NOT(contact[nxtgn_dqapproved]), OR(contact[nxtgn_prebounced], OR(contact[nxtgn_postbounced], OR(contact[statuscodename]="Left Company – Change in Dyn365", OR(ISBLANK(contact[emailaddress1]), OR(ISBLANK(contact[gendercodename]), contact[msdyn_orgchangestatusname]="Not at Company"))))))
```



```dax
classification_issue = OR(ISBLANK(RELATED(account[nxtgn_industrycrmidname])), ISBLANK(contact[nxtgn_vipidname]))
```


## Table: account

### Measures:


```dax
active_contacts = COUNTROWS(RELATEDTABLE(contact))
```


## Table: nxtgn_hubspotactivity

### Calculated Columns:


```dax
scheduledend (bins) = IF(
  ISBLANK('nxtgn_hubspotactivity'[scheduledend]),
  BLANK(),
  DATE(
    YEAR('nxtgn_hubspotactivity'[scheduledend]),
    1 + (MONTH('nxtgn_hubspotactivity'[scheduledend]) - 1),
    1
  )
)
```


## Table: lead

### Measures:


```dax
List of nxtgn_campaignshortname values = 
VAR __DISTINCT_VALUES_COUNT = DISTINCTCOUNT('lead'[nxtgn_campaignshortname])
VAR __MAX_VALUES_TO_SHOW = 100
RETURN
	IF(
		__DISTINCT_VALUES_COUNT > __MAX_VALUES_TO_SHOW,
		CONCATENATE(
			CONCATENATEX(
				TOPN(
					__MAX_VALUES_TO_SHOW,
					VALUES('lead'[nxtgn_campaignshortname]),
					'lead'[nxtgn_campaignshortname],
					ASC
				),
				'lead'[nxtgn_campaignshortname],
				", ",
				'lead'[nxtgn_campaignshortname],
				ASC
			),
			", etc."
		),
		CONCATENATEX(
			VALUES('lead'[nxtgn_campaignshortname]),
			'lead'[nxtgn_campaignshortname],
			", ",
			'lead'[nxtgn_campaignshortname],
			ASC
		)
	)
```



```dax
avg_engagement_score = AVERAGEX(SUMMARIZE('lead', 'lead'[nxtgn_linkhubspotcontact], 'lead'[nxtgn_engagementscore]), 'lead'[nxtgn_engagementscore])
```


### Calculated Columns:


```dax
url = CONCATENATE("https://rolandberger.crm4.dynamics.com/main.aspx?appid=9e3de84b-a781-ea11-a811-000d3a253a0e&forceUCI=1&pagetype=entityrecord&etn=lead&id=", 'lead'[leadid])
```

