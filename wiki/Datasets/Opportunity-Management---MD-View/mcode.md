



# M Code

|Dataset|[Opportunity Management - MD View](./../Opportunity-Management---MD-View.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_opportunityregistrations


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_opportunityregistrations = Source{[Name="nxtgn_opportunityregistrations",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_opportunityregistrations,{"nxtgn_opportunityregistrationid", "createdon", "_ownerid_value", "statecode", "statuscode", "nxtgn_topic", "_nxtgn_accountid_value", "nxtgn_estclosedate", "nxtgn_estrevenue", "_transactioncurrencyid_value", "nxtgn_probability", "nxtgn_leadstatus", "nxtgn_id_customerquotesap", "nxtgn_totalrevenue_orders_calc_base", "nxtgn_actualclosedate", "nxtgn_ordersactualclosedate", "_nxtgn_countryid_value", "_nxtgn_industryccid_value", "_nxtgn_sectorsapid_value", "_nxtgn_functionccid_value", "_nxtgn_themesapid_value", "nxtgn_innovationtopics"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "nxtgn_leadstatus_meta", each if [nxtgn_leadstatus]<>null then Value.Metadata([nxtgn_leadstatus])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "accountid_value", each Value.Metadata([_nxtgn_accountid_value])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "nxtgn_countryid_value", each if [_nxtgn_countryid_value]<>null then Value.Metadata([_nxtgn_countryid_value])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom5" = Table.AddColumn(#"Added Custom4", "_nxtgn_industryccid_value_meta", each if [_nxtgn_industryccid_value]<>null then Value.Metadata([_nxtgn_industryccid_value])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom6" = Table.AddColumn(#"Added Custom5", "_nxtgn_sectorsapid_value_meta", each if [_nxtgn_sectorsapid_value]<>null then Value.Metadata([_nxtgn_sectorsapid_value])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom7" = Table.AddColumn(#"Added Custom6", "_nxtgn_functionccid_value_meta", each if [_nxtgn_functionccid_value]<>null then Value.Metadata([_nxtgn_functionccid_value])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom8" = Table.AddColumn(#"Added Custom7", "_nxtgn_themesapid_value_meta", each if [_nxtgn_themesapid_value]<>null then Value.Metadata([_nxtgn_themesapid_value])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom9" = Table.AddColumn(#"Added Custom8", "nxtgn_innovationtopics_meta", each if [nxtgn_innovationtopics]<>null then Value.Metadata([nxtgn_innovationtopics])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom9", each ([statuscode_meta] <> "Inactive" and [statuscode_meta] <> "Inactive - Closed")),
    #"Sorted Rows" = Table.Sort(#"Filtered Rows",{{"nxtgn_estclosedate", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: systemusers (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers = Source{[Name="systemusers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(systemusers,{"systemuserid", "fullname", "nxtgn_platformid", "nxtgn_lookupcountryid"}),
    #"Expanded nxtgn_platformid" = Table.ExpandRecordColumn(#"Removed Other Columns", "nxtgn_platformid", {"nxtgn_name"}, {"nxtgn_platformid.nxtgn_name"}),
    #"Expanded nxtgn_lookupcountryid" = Table.ExpandRecordColumn(#"Expanded nxtgn_platformid", "nxtgn_lookupcountryid", {"nxtgn_name", "nxtgn_lookupcountryid"}, {"nxtgn_lookupcountryid.nxtgn_name", "nxtgn_lookupcountryid.nxtgn_lookupcountryid"}),
    #"Added Conditional Column" = Table.AddColumn(#"Expanded nxtgn_lookupcountryid", "platform_sort_order", each if [nxtgn_platformid.nxtgn_name] = "Industrials (IND)" then 1 else if [nxtgn_platformid.nxtgn_name] = "Operations (OPS)" then 2 else if [nxtgn_platformid.nxtgn_name] = "Regulated & Infrastructure (R&I)" then 3 else if [nxtgn_platformid.nxtgn_name] = "Health & Consumer (H&C)" then 4 else if [nxtgn_platformid.nxtgn_name] = "Services (SER)" then 5 else if [nxtgn_platformid.nxtgn_name] = "RPT (RPT)" then 6 else if [nxtgn_platformid.nxtgn_name] = "Investor Support (INV)" then 7 else if [nxtgn_platformid.nxtgn_name] = "Digital (DIG)" then 8 else 9)
in
    #"Added Conditional Column"
```


## Table: nxtgn_shareofwallets


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_shareofwallets = Source{[Name="nxtgn_shareofwallets",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_shareofwallets,{"nxtgn_shareofwalletid", "nxtgn_countryid", "_nxtgn_salesleadid_value", "nxtgn_countrypercentage", "nxtgn_iscountry"}),
    #"Expanded nxtgn_countryid" = Table.ExpandRecordColumn(#"Removed Other Columns", "nxtgn_countryid", {"nxtgn_name", "nxtgn_lookupcountryid"}, {"nxtgn_countryid.nxtgn_name", "nxtgn_countryid.nxtgn_lookupcountryid"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded nxtgn_countryid", each [nxtgn_iscountry] = true and [nxtgn_countrypercentage] <> null),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"nxtgn_shareofwalletid"}, #"nxtgn_shareofwallets (2)", {"_nxtgn_parentsowid_value"}, "nxtgn_shareofwallets (2)", JoinKind.LeftOuter),
    #"Expanded nxtgn_shareofwallet (2)" = Table.ExpandTableColumn(#"Merged Queries", "nxtgn_shareofwallets (2)", {"nxtgn_percentage", "nxtgn_platformid.nxtgn_name", "platform_sort_order"}, {"nxtgn_shareofwallets (2).nxtgn_percentage", "nxtgn_shareofwallets (2).nxtgn_platformid.nxtgn_name", "nxtgn_shareofwallets (2).platform_sort_order"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Expanded nxtgn_shareofwallet (2)",{"nxtgn_shareofwalletid", "nxtgn_countryid.nxtgn_lookupcountryid", "_nxtgn_salesleadid_value", "nxtgn_countryid.nxtgn_name", "nxtgn_countrypercentage", "nxtgn_shareofwallets (2).nxtgn_percentage", "nxtgn_shareofwallets (2).nxtgn_platformid.nxtgn_name", "nxtgn_shareofwallets (2).platform_sort_order"})
in
    #"Reordered Columns"
```


## Table: nxtgn_lookupcountryalias (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountryalias = Source{[Name="nxtgn_lookupcountryaliases",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountryalias, each ([nxtgn_name] = "Americas (RB)" or [nxtgn_name] = "Asia (RB)" or [nxtgn_name] = "EMEA (RB)")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_name", "nxtgn_countryid"}),
    #"Expanded nxtgn_countryid" = Table.ExpandRecordColumn(#"Removed Other Columns", "nxtgn_countryid", {"nxtgn_lookupcountryid"}, {"nxtgn_countryid.nxtgn_lookupcountryid"})
in
    #"Expanded nxtgn_countryid"
```


## Table: nxtgn_lookupcountries


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountry = Source{[Name="nxtgn_lookupcountries",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountry, each ([statuscode] = 1)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_lookupcountryid", "nxtgn_name"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_shareofwallets (3)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_shareofwallets = Source{[Name="nxtgn_shareofwallets",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_shareofwallets,{"nxtgn_shareofwalletid", "nxtgn_countryid", "_nxtgn_salesleadid_value", "nxtgn_countrypercentage", "nxtgn_iscountry"}),
    #"Expanded nxtgn_countryid" = Table.ExpandRecordColumn(#"Removed Other Columns", "nxtgn_countryid", {"nxtgn_name", "nxtgn_lookupcountryid"}, {"nxtgn_countryid.nxtgn_name", "nxtgn_countryid.nxtgn_lookupcountryid"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded nxtgn_countryid", each [nxtgn_iscountry] = true and [nxtgn_countrypercentage] <> null),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"nxtgn_shareofwalletid"}, #"nxtgn_shareofwallets (2)", {"_nxtgn_parentsowid_value"}, "nxtgn_shareofwallets (2)", JoinKind.LeftOuter),
    #"Expanded nxtgn_shareofwallet (2)" = Table.ExpandTableColumn(#"Merged Queries", "nxtgn_shareofwallets (2)", {"nxtgn_percentage", "nxtgn_platformid.nxtgn_name", "platform_sort_order"}, {"nxtgn_shareofwallets (2).nxtgn_percentage", "nxtgn_shareofwallets (2).nxtgn_platformid.nxtgn_name", "nxtgn_shareofwallets (2).platform_sort_order"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Expanded nxtgn_shareofwallet (2)",{"nxtgn_shareofwalletid", "nxtgn_countryid.nxtgn_lookupcountryid", "_nxtgn_salesleadid_value", "nxtgn_countryid.nxtgn_name", "nxtgn_countrypercentage", "nxtgn_shareofwallets (2).nxtgn_percentage", "nxtgn_shareofwallets (2).nxtgn_platformid.nxtgn_name", "nxtgn_shareofwallets (2).platform_sort_order"})
in
    #"Reordered Columns"
```


## Table: nxtgn_opportunityregistrations (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_opportunityregistrations = Source{[Name="nxtgn_opportunityregistrations",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_opportunityregistrations,{"nxtgn_opportunityregistrationid", "createdon", "_ownerid_value", "statecode", "statuscode", "nxtgn_topic", "_nxtgn_accountid_value", "nxtgn_estclosedate", "nxtgn_estrevenue", "_transactioncurrencyid_value", "nxtgn_probability", "nxtgn_leadstatus", "nxtgn_id_customerquotesap", "nxtgn_totalrevenue_orders_calc_base", "nxtgn_actualclosedate", "nxtgn_ordersactualclosedate", "_nxtgn_countryid_value"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "nxtgn_leadstatus_meta", each if [nxtgn_leadstatus]<>null then Value.Metadata([nxtgn_leadstatus])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "accountid_value", each Value.Metadata([_nxtgn_accountid_value])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "nxtgn_countryid_value", each if [_nxtgn_countryid_value]<>null then Value.Metadata([_nxtgn_countryid_value])[OData.Community.Display.V1.FormattedValue] else ""),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom4", each ([statuscode_meta] <> "Inactive" and [statuscode_meta] <> "Inactive - Closed")),
    #"Sorted Rows" = Table.Sort(#"Filtered Rows",{{"nxtgn_estclosedate", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: transactioncurrencies


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    transactioncurrencies = Source{[Name="transactioncurrencies",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(transactioncurrencies,{"transactioncurrencyid", "exchangerate", "currencyname"})
in
    #"Removed Other Columns"
```


## Table: transactioncurrencies (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    transactioncurrencies = Source{[Name="transactioncurrencies",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(transactioncurrencies,{"transactioncurrencyid", "exchangerate", "currencyname"})
in
    #"Removed Other Columns"
```


## Table: Country Budgets


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger-my.sharepoint.com/personal/christoph_kecht_rolandberger_com1/Documents/20230210_CountryBudgets2023.xlsx"), null, true),
    Values_Sheet = Source{[Item="Values",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Values_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Country", type text}, {"Country ID", type text}, {"Valid From", type date}, {"Valid To", type date}, {"Budget", Int64.Type}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type",{"Country", "Country ID", "Valid From", "Valid To", "Budget"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupcountryalias (3)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountryalias = Source{[Name="nxtgn_lookupcountryaliases",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountryalias, each ([nxtgn_name] = "Americas (RB)" or [nxtgn_name] = "Asia (RB)" or [nxtgn_name] = "EMEA (RB)")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_name", "nxtgn_countryid"}),
    #"Expanded nxtgn_countryid" = Table.ExpandRecordColumn(#"Removed Other Columns", "nxtgn_countryid", {"nxtgn_lookupcountryid"}, {"nxtgn_countryid.nxtgn_lookupcountryid"})
in
    #"Expanded nxtgn_countryid"
```


## Table: Industry Platform Budgets


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger-my.sharepoint.com/personal/christoph_kecht_rolandberger_com1/Documents/20230413_PlatformBudgets2023.xlsx"), null, true),
    Values_Sheet = Source{[Item="Values",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Values_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Platform", type text}, {"Platform ID", type text}, {"Valid From", type date}, {"Valid To", type date}, {"Budget", Int64.Type}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type",{"Platform", "Platform ID", "Valid From", "Valid To", "Budget"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([Platform] = "Health & Consumer (H&C)" or [Platform] = "Industrials (IND)" or [Platform] = "Regulated & Infrastructure (R&I)" or [Platform] = "Services (SER)"))
in
    #"Filtered Rows"
```


## Table: nxtgn_lookupindustryccs


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountryalias = Source{[Name="nxtgn_lookupindustryccs",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountryalias, each [statuscode] = 1),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_lookupindustryccid", "nxtgn_name", "_nxtgn_platformid_value"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupfunctionccs


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountryalias = Source{[Name="nxtgn_lookupfunctionccs",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountryalias, each [statuscode] = 1),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_lookupfunctionccid", "nxtgn_name", "_nxtgn_platformid_value"})
in
    #"Removed Other Columns"
```


## Table: Functional Platform Budgets


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger-my.sharepoint.com/personal/christoph_kecht_rolandberger_com1/Documents/20230413_PlatformBudgets2023.xlsx"), null, true),
    Values_Sheet = Source{[Item="Values",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Values_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Platform", type text}, {"Platform ID", type text}, {"Valid From", type date}, {"Valid To", type date}, {"Budget", Int64.Type}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type",{"Platform", "Platform ID", "Valid From", "Valid To", "Budget"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([Platform] <> "Health & Consumer (H&C)" and [Platform] <> "Industrials (IND)" and [Platform] <> "Regulated & Infrastructure (R&I)" and [Platform] <> "Services (SER)"))
in
    #"Filtered Rows"
```

