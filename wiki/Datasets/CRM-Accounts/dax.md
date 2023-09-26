



# DAX

|Dataset|[CRM Accounts](./../CRM-Accounts.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: accounts

### Measures:


```dax
count_industry = COUNTX(accounts, [_nxtgn_industrycrmid_value])
```



```dax
count_subindustry = COUNTX(accounts, [_nxtgn_subindustrycrmid_value])
```



```dax
count_address1_line1 = COUNTX(accounts, [address1_line1])
```



```dax
count_websiteurl = COUNTX(accounts, [websiteurl])
```



```dax
count_accounts = COUNT(accounts[accountid])+0
```



```dax
count_correct_suggested_industry = CALCULATE(accounts[count_accounts], FILTER(accounts, accounts[_nxtgn_industrycrmid_value]=accounts[_nxtgn_suggestedindustrycrmid_value]))+0
```



```dax
count_correct_suggested_subindustry = CALCULATE(accounts[count_accounts], FILTER(accounts, accounts[_nxtgn_subindustrycrmid_value]=accounts[_nxtgn_suggestedsubindustrycrmid_value]))+0
```


### Calculated Columns:


```dax
createdon (week) = CONCATENATE(YEAR(accounts[createdon]), CONCATENATE(" - CW ", WEEKNUM(accounts[createdon], 2)))
```



```dax
nxtgn_lastcompliancecheck (week) = CONCATENATE(YEAR(accounts[nxtgn_lastcompliancecheck]), CONCATENATE(" - CW ", WEEKNUM(accounts[nxtgn_lastcompliancecheck], 2)))
```



```dax
mismatch_industry_subindustry = IF(ISBLANK(accounts[_nxtgn_subindustrycrmid_value]), FALSE, RELATED(nxtgn_lookupsubindustrycrms[_nxtgn_industrycrmid_value]) <> accounts[_nxtgn_industrycrmid_value])
```



```dax
url = CONCATENATE("https://rolandberger.crm4.dynamics.com/main.aspx?appid=9e3de84b-a781-ea11-a811-000d3a253a0e&forceUCI=1&newWindow=true&pagetype=entityrecord&etn=account&id=", accounts[accountid])
```



```dax
invalid_country = ISBLANK(LOOKUPVALUE(nxtgn_lookupcountries[nxtgn_name], nxtgn_lookupcountries[nxtgn_name], accounts[address1_country]))
```



```dax
data_quality_issue = OR(accounts[mismatch_industry_subindustry], OR(accounts[invalid_country], NOT(accounts[nxtgn_dqapproved])))
```



```dax
nxtgn_nextcompliancecheck = EDATE(accounts[nxtgn_lastcompliancecheck], 6)
```



```dax
count_contacts = CALCULATE(COUNTROWS(contacts), FILTER(contacts, contacts[_parentcustomerid_value] = accounts[accountid]))+0
```



```dax
count_account_foreignkeies = CALCULATE(COUNTROWS(nxtgn_foreignkeies), FILTER(nxtgn_foreignkeies, nxtgn_foreignkeies[_nxtgn_accountid_value] = accounts[accountid]))+0
```



```dax
count_nxtgn_opportunityregistrations = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[_nxtgn_accountid_value] = accounts[accountid]))+0
```



```dax
count_nxtgn_opportunityregistrations_target = CALCULATE(COUNTROWS(nxtgn_opportunityregistrations), FILTER(nxtgn_opportunityregistrations, nxtgn_opportunityregistrations[_nxtgn_actualaccountid_value] = accounts[accountid]))+0
```



```dax
count_opportunities = CALCULATE(COUNTROWS(opportunities), FILTER(opportunities, opportunities[_customerid_value] = accounts[accountid]))+0
```



```dax
count_opportunities_parent = CALCULATE(COUNTROWS(opportunities), FILTER(opportunities, opportunities[_parentaccountid_value] = accounts[accountid]))+0
```



```dax
count_quotes = CALCULATE(COUNTROWS(quotes), FILTER(quotes, quotes[_customerid_value] = accounts[accountid]))+0
```



```dax
count_quotes_billto = CALCULATE(COUNTROWS(quotes), FILTER(quotes, quotes[_nxtgn_billtoaccountid_value] = accounts[accountid]))+0
```



```dax
count_salesorders = CALCULATE(COUNTROWS(salesorders), FILTER(salesorders, salesorders[_customerid_value] = accounts[accountid]))+0
```



```dax
count_salesorders_billto = CALCULATE(COUNTROWS(salesorders), FILTER(salesorders, salesorders[_nxtgn_billtoaccountid_value] = accounts[accountid]))+0
```



```dax
count_projects = CALCULATE(COUNTROWS(nxtgn_projects), FILTER(nxtgn_projects, nxtgn_projects[_nxtgn_accountid_value] = accounts[accountid]))+0
```



```dax
deletion_candidate = AND(accounts[nxtgn_syncwithsap]=FALSE(), AND(ISBLANK(accounts[accountnumber]), accounts[count_contacts] + accounts[count_account_foreignkeies] + accounts[count_nxtgn_opportunityregistrations] + accounts[count_nxtgn_opportunityregistrations_target] + accounts[count_opportunities] + accounts[count_opportunities_parent] + accounts[count_quotes] + accounts[count_quotes_billto] + accounts[count_salesorders] + accounts[count_salesorders_billto] + accounts[count_projects] = 0))
```


## Table: nxtgn_lookupindustrycrms

### Calculated Columns:


```dax
count_suggested_accounts = CALCULATE(COUNTROWS(accounts), FILTER(accounts, accounts[_nxtgn_suggestedindustrycrmid_value] = nxtgn_lookupindustrycrms[nxtgn_lookupindustrycrmid]))+0
```



```dax
suggestion_accuracy = IF(accounts[count_accounts]>0, [count_correct_suggested_industry]/accounts[count_accounts])
```


## Table: nxtgn_lookupsubindustrycrms

### Calculated Columns:


```dax
nxtgn_name_incl_parent = CONCATENATE(nxtgn_lookupsubindustrycrms[nxtgn_name], CONCATENATE(" (", CONCATENATE(LOOKUPVALUE(nxtgn_lookupindustrycrms[nxtgn_name], nxtgn_lookupindustrycrms[nxtgn_lookupindustrycrmid], nxtgn_lookupsubindustrycrms[_nxtgn_industrycrmid_value]), ")")))
```



```dax
count_suggested_accounts = CALCULATE(COUNTROWS(accounts), FILTER(accounts, accounts[_nxtgn_suggestedsubindustrycrmid_value] = nxtgn_lookupsubindustrycrms[nxtgn_lookupsubindustrycrmid]))+0
```



```dax
suggestion_accuracy = IF(accounts[count_accounts]>0, [count_correct_suggested_subindustry]/accounts[count_accounts])
```

