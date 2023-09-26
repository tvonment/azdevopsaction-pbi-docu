



# M Code

|Dataset|[Opportunity Management](./../Opportunity-Management.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: teams


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558", [CommandTimeout=#duration(0, 0, 15, 0)]),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    teams_table = rolandberger{[Schema="dbo",Item="team"]}[Data],
    #"Filtered Rows" = Table.SelectRows(teams_table, each ([teamtemplateid] = "2B89066D-15C2-EA11-A812-000D3AAB4F6F")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"teamid", "regardingobjectid"})
in
    #"Removed Other Columns"
```


## Table: systemusers


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_systemuser = rolandberger{[Schema="dbo",Item="systemuser"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_systemuser, each ([nxtgn_islicensed] = true) and ([isdisabled] = false)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"systemuserid", "fullname", "nxtgn_lookupcountryidname", "nxtgn_platformidname", "nxtgn_costcenteridname"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_shareofwallets


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_shareofwallet = rolandberger{[Schema="dbo",Item="nxtgn_shareofwallet"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_shareofwallet, each [nxtgn_iscountry] = true),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_shareofwalletid", "nxtgn_countryid", "nxtgn_salesleadid", "nxtgn_countryidname", "nxtgn_countrypercentage", "nxtgn_rblegalunitccid", "nxtgn_rblegalunit"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Other Columns", {"nxtgn_shareofwalletid"}, #"nxtgn_shareofwallets (2)", {"nxtgn_parentsowid"}, "nxtgn_shareofwallets (2)", JoinKind.LeftOuter),
    #"Expanded nxtgn_shareofwallet (2)" = Table.ExpandTableColumn(#"Merged Queries", "nxtgn_shareofwallets (2)", {"nxtgn_percentage", "nxtgn_platformid", "nxtgn_platformidname", "nxtgn_parentsowid"}, {"nxtgn_shareofwallets (2).nxtgn_percentage", "nxtgn_shareofwallets (2).nxtgn_platformid", "nxtgn_shareofwallets (2).nxtgn_platformidname", "nxtgn_shareofwallets (2).nxtgn_parentsowid"}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded nxtgn_shareofwallet (2)", {"nxtgn_salesleadid"}, nxtgn_opportunityregistrations, {"nxtgn_opportunityregistrationid"}, "nxtgn_opportunityregistrations", JoinKind.Inner),
    #"Reordered Columns" = Table.ReorderColumns(#"Merged Queries1",{"nxtgn_opportunityregistrations", "nxtgn_shareofwalletid", "nxtgn_countryid", "nxtgn_salesleadid", "nxtgn_countryidname", "nxtgn_countrypercentage", "nxtgn_shareofwallets (2).nxtgn_percentage", "nxtgn_shareofwallets (2).nxtgn_platformid", "nxtgn_shareofwallets (2).nxtgn_platformidname", "nxtgn_shareofwallets (2).nxtgn_parentsowid"}),
    #"Expanded nxtgn_opportunityregistrations" = Table.ExpandTableColumn(#"Reordered Columns", "nxtgn_opportunityregistrations", {"nxtgn_opportunityregistrationid", "createdon", "owneridname", "statecodename", "statuscodename", "nxtgn_topic", "nxtgn_accountid", "nxtgn_description", "nxtgn_estclosedate", "nxtgn_estrevenue", "transactioncurrencyid", "nxtgn_probability", "nxtgn_leadstatusname", "nxtgn_functionccidname", "nxtgn_industryccidname", "nxtgn_relevantforforecastname", "nxtgn_themesapidname", "nxtgn_salesunitidname", "nxtgn_sectorsapidname", "nxtgn_salesteam_concatinate", "nxtgn_id_customerquotesap", "nxtgn_totalrevenue_orders_calc_base", "nxtgn_actualclosedate", "nxtgn_ordersactualclosedate", "nxtgn_closereasons_concatenate", "nxtgn_competitorid", "nxtgn_othercompetitors", "nxtgn_competitoridname", "nxtgn_lastsubmissiondate", "nxtgn_innovationtopicsname", "nxtgn_sustainabilityrelated", "nxtgn_lead_priorityname", "nxtgn_keyaccountname", "nxtgn_notes"}, {"nxtgn_opportunityregistrations.nxtgn_opportunityregistrationid", "nxtgn_opportunityregistrations.createdon", "nxtgn_opportunityregistrations.owneridname", "nxtgn_opportunityregistrations.statecodename", "nxtgn_opportunityregistrations.statuscodename", "nxtgn_opportunityregistrations.nxtgn_topic", "nxtgn_opportunityregistrations.nxtgn_accountid", "nxtgn_opportunityregistrations.nxtgn_description", "nxtgn_opportunityregistrations.nxtgn_estclosedate", "nxtgn_opportunityregistrations.nxtgn_estrevenue", "nxtgn_opportunityregistrations.transactioncurrencyid", "nxtgn_opportunityregistrations.nxtgn_probability", "nxtgn_opportunityregistrations.nxtgn_leadstatusname", "nxtgn_opportunityregistrations.nxtgn_functionccidname", "nxtgn_opportunityregistrations.nxtgn_industryccidname", "nxtgn_opportunityregistrations.nxtgn_relevantforforecastname", "nxtgn_opportunityregistrations.nxtgn_themesapidname", "nxtgn_opportunityregistrations.nxtgn_salesunitidname", "nxtgn_opportunityregistrations.nxtgn_sectorsapidname", "nxtgn_opportunityregistrations.nxtgn_salesteam_concatinate", "nxtgn_opportunityregistrations.nxtgn_id_customerquotesap", "nxtgn_opportunityregistrations.nxtgn_totalrevenue_orders_calc_base", "nxtgn_opportunityregistrations.nxtgn_actualclosedate", "nxtgn_opportunityregistrations.nxtgn_ordersactualclosedate", "nxtgn_opportunityregistrations.nxtgn_closereasons_concatenate", "nxtgn_opportunityregistrations.nxtgn_competitorid", "nxtgn_opportunityregistrations.nxtgn_othercompetitors", "nxtgn_opportunityregistrations.nxtgn_competitoridname", "nxtgn_opportunityregistrations.nxtgn_lastsubmissiondate", "nxtgn_opportunityregistrations.nxtgn_innovationtopicsname", "nxtgn_opportunityregistrations.nxtgn_sustainabilityrelated", "nxtgn_opportunityregistrations.nxtgn_lead_priorityname", "nxtgn_opportunityregistrations.nxtgn_keyaccountname", "nxtgn_opportunityregistrations.nxtgn_notes"})
in
    #"Expanded nxtgn_opportunityregistrations"
```


## Table: nxtgn_lookupcountryaliases


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_lookupcountryalias = rolandberger{[Schema="dbo",Item="nxtgn_lookupcountryalias"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(dbo_nxtgn_lookupcountryalias,{"nxtgn_name", "nxtgn_countryid", "nxtgn_countryidname"})
in
    #"Removed Other Columns"
```


## Table: teammemberships


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_teammembership = rolandberger{[Schema="dbo",Item="teammembership"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(dbo_teammembership,{"systemuserid", "teamid"})
in
    #"Removed Other Columns"
```


## Table: transactioncurrency


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_transactioncurrency = rolandberger{[Schema="dbo",Item="transactioncurrency"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_transactioncurrency, each [currencyname] = "Euro" or [currencyname] = "United States Dollar" or [currencyname] = "円" or [currencyname] = "ꎆꃀ" or [currencyname] = "원" or [currencyname] = "Pound Sterling" or [currencyname] = "Dollar canadien" or [currencyname] = "Svensk krona"),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows", "currencydisplayname", each Text.Combine({[currencyname], " (", [isocurrencycode], ")"}), type text),
    #"Removed Other Columns" = Table.SelectColumns(#"Inserted Merged Column",{"exchangerate", "currencydisplayname"})
in
    #"Removed Other Columns"
```


## Table: transactioncurrency (2)


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_transactioncurrency = rolandberger{[Schema="dbo",Item="transactioncurrency"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(dbo_transactioncurrency,{"transactioncurrencyid", "currencyname", "exchangerate"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_opportunityclosereasons


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_opportunityregistration = rolandberger{[Schema="dbo",Item="nxtgn_opportunityclosereason"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_opportunityregistration, each [statecode] = 0),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_statusreasonidname", "nxtgn_statusreasonid", "nxtgn_opportunityid", "nxtgn_opportunityclosereasonid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupopportunitystatusreasons


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_opportunityregistration = rolandberger{[Schema="dbo",Item="nxtgn_lookupopportunitystatusreason"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_opportunityregistration, each [statecode] = 0),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_outcomename", "nxtgn_outcome", "nxtgn_order", "nxtgn_categoryname", "nxtgn_category", "nxtgn_name", "nxtgn_lookupopportunitystatusreasonid"}),
    #"Sorted Rows" = Table.Sort(#"Removed Other Columns",{{"nxtgn_order", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: account


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_account = rolandberger{[Schema="dbo",Item="account"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(dbo_account,{"accountid", "name", "nxtgn_classificationidname"})
in
    #"Removed Other Columns"
```


## Table: [Slicer] Measure Selection


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUVJW8C8oyC8qKc3LLMlMLQaKuKfmpRYl5ij4leYmpRYpxepEKxkBhVUV8tMUMFUHpBYlp+aVgJUZA/muFQV6CmGJOaWpCvoKIfklQIP8PYHizqVFRal5yZVghSYw83CpRjbVFGaqX2oJUBao0NHNCd1EMxQT0VTCTYsFAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Option = _t, Value = _t, Format = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Option", Int64.Type}, {"Value", type text}})
in
    #"Changed Type"
```

