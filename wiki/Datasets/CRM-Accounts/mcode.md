



# M Code

|Dataset|[CRM Accounts](./../CRM-Accounts.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: accounts


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    accounts_table = Source{[Name="accounts",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(accounts_table,{"websiteurl", "nxtgn_compliancecheckresultstatus", "nxtgn_dqapproved", "_nxtgn_industrycrmid_value", "nxtgn_compliancecheckstatus", "statuscode", "accountnumber", "address1_country", "nxtgn_blacklistaccount", "statecode", "name", "nxtgn_syncwithsap", "accountid", "nxtgn_dunsnumber", "_nxtgn_subindustrycrmid_value", "address1_line1", "createdon", "nxtgn_lastcompliancecheck", "parentaccountid", "nxtgn_industrycrmid", "nxtgn_subindustrycrmid", "nxtgn_globalultimateaccountid", "_nxtgn_suggestedindustrycrmid_value", "_nxtgn_suggestedsubindustrycrmid_value", "_nxtgn_suggestedindustrylinkedin_value", "_nxtgn_suggestedsubindustrylinkedin_value", "_nxtgn_suggestednumberofemployees_value"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom5" = Table.AddColumn(#"Added Custom2", "nxtgn_blacklistaccount_meta", each if [nxtgn_blacklistaccount] is null then "" else Value.Metadata([nxtgn_blacklistaccount])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom6" = Table.AddColumn(#"Added Custom5", "nxtgn_compliancecheckstatus_meta", each if [nxtgn_compliancecheckstatus] is null then "In Progress" else Value.Metadata([nxtgn_compliancecheckstatus])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom7" = Table.AddColumn(#"Added Custom6", "nxtgn_compliancecheckresultstatus_meta", each if [nxtgn_compliancecheckresultstatus] is null then "In Progress" else Value.Metadata([nxtgn_compliancecheckresultstatus])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom8" = Table.AddColumn(#"Added Custom7", "nxtgn_dqapproved_meta", each Value.Metadata([nxtgn_dqapproved])[OData.Community.Display.V1.FormattedValue])
in
    #"Added Custom8"
```


## Table: nxtgn_lookupindustrycrms


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupindustrycrms_table = Source{[Name="nxtgn_lookupindustrycrms",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupindustrycrms_table,{"nxtgn_name", "nxtgn_lookupindustrycrmid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupsubindustrycrms


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupsubindustrycrms_table = Source{[Name="nxtgn_lookupsubindustrycrms",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupsubindustrycrms_table,{"nxtgn_lookupsubindustrycrmid", "nxtgn_name", "_nxtgn_industrycrmid_value"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupcountries


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountries_table = Source{[Name="nxtgn_lookupcountries",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountries_table, each ([statuscode] = 1)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_name", "nxtgn_lookupcountryid", "cra2a_businessprohibited"})
in
    #"Removed Other Columns"
```


## Table: contacts


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    contacts_table = Source{[Name="contacts",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(contacts_table,{"contactid", "_parentcustomerid_value"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_foreignkeies


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    nxtgn_foreignkeies_table = Source{[Name="nxtgn_foreignkeies",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_foreignkeies_table, each ([_nxtgn_accountid_value] <> null) and ([nxtgn_sourcesystem] = 204030000)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"_nxtgn_accountid_value", "nxtgn_foreignkeyid", "nxtgn_key", "nxtgn_sapprimaryaddress"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_opportunityregistrations


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    nxtgn_opportunityregistrations_table = Source{[Name="nxtgn_opportunityregistrations",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_opportunityregistrations_table,{"nxtgn_opportunityregistrationid", "_nxtgn_accountid_value", "_nxtgn_actualaccountid_value"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_projects


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    nxtgn_projects_table = Source{[Name="nxtgn_projects",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_projects_table,{"nxtgn_projectid", "_nxtgn_accountid_value"})
in
    #"Removed Other Columns"
```


## Table: opportunities


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    opportunities_table = Source{[Name="opportunities",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(opportunities_table,{"opportunityid", "_customerid_value", "_parentaccountid_value"})
in
    #"Removed Other Columns"
```


## Table: salesorders


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    salesorders_table = Source{[Name="salesorders",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(salesorders_table,{"salesorderid", "_customerid_value", "_nxtgn_billtoaccountid_value"})
in
    #"Removed Other Columns"
```


## Table: quotes


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    quotes_table = Source{[Name="quotes",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(quotes_table,{"quoteid", "_customerid_value", "_nxtgn_billtoaccountid_value"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupindustrycrms (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupindustrycrms_table = Source{[Name="nxtgn_lookupindustrycrms",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupindustrycrms_table,{"nxtgn_name", "nxtgn_lookupindustrycrmid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupsubindustrycrms (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupsubindustrycrms_table = Source{[Name="nxtgn_lookupsubindustrycrms",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupsubindustrycrms_table,{"nxtgn_lookupsubindustrycrmid", "nxtgn_name", "_nxtgn_industrycrmid_value"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupindustrylinkedins


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupindustrylinkedins_table = Source{[Name="nxtgn_lookupindustrylinkedins",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupindustrylinkedins_table,{"nxtgn_name", "nxtgn_lookupindustrylinkedinid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupsubindustrylinkedins


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupindustrylinkedins_table = Source{[Name="nxtgn_lookupsubindustrylinkedins",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_lookupindustrylinkedins_table,{"nxtgn_name", "nxtgn_lookupsubindustrylinkedinid"})
in
    #"Removed Other Columns"
```

