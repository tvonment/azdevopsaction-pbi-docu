



# M Code

|Dataset|[Sales Funnel Sustainability Team](./../Sales-Funnel-Sustainability-Team.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_opportunityregistrations


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_opportunityregistrations_table = Source{[Name="nxtgn_opportunityregistrations",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_opportunityregistrations_table,{"_nxtgn_functionccid_value", "nxtgn_topic", "nxtgn_estrevenue_base", "nxtgn_innovationtopics", "statecode", "_transactioncurrencyid_value", "nxtgn_probability", "nxtgn_ordersactualclosedate", "nxtgn_sustainabilityrelated", "_nxtgn_themesapid_value", "nxtgn_estrevenue", "_nxtgn_industryccid_value", "nxtgn_opportunityregistrationid", "_nxtgn_accountid_value", "nxtgn_estclosedate", "_nxtgn_sectorsapid_value", "nxtgn_salesteam_concatinate", "statuscode", "nxtgn_leadstatus", "_nxtgn_countryid_value", "createdon", "nxtgn_actualclosedate", "_ownerid_value", "nxtgn_closereasons_concatenate"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "nxtgn_accountid_meta", each Value.Metadata([_nxtgn_accountid_value])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "nxtgn_leadstatus_meta", each if [nxtgn_leadstatus]<> null then Value.Metadata([nxtgn_leadstatus])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "nxtgn_innovationtopics_meta", each if [nxtgn_innovationtopics]<>null then Value.Metadata([nxtgn_innovationtopics])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom5" = Table.AddColumn(#"Added Custom4", "nxtgn_industryccid_value", each if [_nxtgn_industryccid_value]<>null then Value.Metadata([_nxtgn_industryccid_value])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom6" = Table.AddColumn(#"Added Custom5", "nxtgn_functionccid_value", each if [_nxtgn_functionccid_value]<>null then Value.Metadata([_nxtgn_functionccid_value])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom7" = Table.AddColumn(#"Added Custom6", "nxtgn_countryid_value", each if [_nxtgn_countryid_value]<>null then Value.Metadata([_nxtgn_countryid_value])[OData.Community.Display.V1.FormattedValue] else "")
in
    #"Added Custom7"
```


## Table: systemusers


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers_table = Source{[Name="systemusers",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(systemusers_table, each ([nxtgn_islicensed] = true)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"systemuserid", "fullname", "_nxtgn_lookupcountryid_value"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupcountryaliases


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountryaliases_table = Source{[Name="nxtgn_lookupcountryaliases",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountryaliases_table, each ([nxtgn_name] = "Americas (RB)" or [nxtgn_name] = "Asia (RB)" or [nxtgn_name] = "EMEA (RB)")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_name", "nxtgn_lookupcountryaliasid", "_nxtgn_countryid_value"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Other Columns"," (RB)","",Replacer.ReplaceText,{"nxtgn_name"}),
    #"Added Conditional Column" = Table.AddColumn(#"Replaced Value", "region_sort_order", each if [nxtgn_name] = "EMEA" then 3 else if [nxtgn_name] = "Americas" then 1 else if [nxtgn_name] = "Asia" then 2 else null, type number)
in
    #"Added Conditional Column"
```

