



# DAX

|Dataset|[CRM Onboarding](./../CRM-Onboarding.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: systemusers

### Measures:


```dax
#active_contacts = CALCULATE(DISTINCTCOUNT(contacts[contactid]), FILTER(contacts, contacts[statuscode_meta]="Active"))+0
```


### Calculated Columns:


```dax
onboarded = IF(systemusers[nxtgn_privacyconsentconfirmed], IF(systemusers[outlook_sync_activated], systemusers[islicensed], FALSE()), FALSE())
```



```dax
outlook_sync_activated = RELATED(mailboxes[actstatus_meta])="Success"
```



```dax
group_function_director = AND(LEFT(systemusers[title], LEN("Director"))="Director", LEFT(systemusers[nxtgn_platformid.nxtgn_name], LEN("Group Function"))="Group Function")
```

