



# M Code

|Dataset|[Opportunity Management - Team Lead View](./../Opportunity-Management---Team-Lead-View.md)|
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


## Table: nxtgn_lookupcountryaliases


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_lookupcountryalias = rolandberger{[Schema="dbo",Item="nxtgn_lookupcountryalias"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_lookupcountryalias, each ([nxtgn_name] = "Americas (RB)" or [nxtgn_name] = "Asia (RB)" or [nxtgn_name] = "EMEA (RB)")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_name", "nxtgn_countryid", "nxtgn_countryidname"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Other Columns"," (RB)","",Replacer.ReplaceText,{"nxtgn_name"})
in
    #"Replaced Value"
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


## Table: nxtgn_opportunityregistrations


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_opportunityregistration = rolandberger{[Schema="dbo",Item="nxtgn_opportunityregistration"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_opportunityregistration, each ([statuscodename] <> "Inactive" and [statuscodename] <> "Inactive - Closed")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_opportunityregistrationid", "createdon", "ownerid", "owneridname", "statecodename", "statuscodename", "nxtgn_topic", "nxtgn_accountid", "nxtgn_description", "nxtgn_estclosedate", "nxtgn_estrevenue", "transactioncurrencyid", "nxtgn_probability", "nxtgn_accountidname", "nxtgn_leadstatusname", "nxtgn_functionccid", "nxtgn_industryccid", "nxtgn_functionccidname", "nxtgn_industryccidname", "nxtgn_relevantforforecastname", "nxtgn_sectorsapid", "nxtgn_themesapid", "nxtgn_themesapidname", "nxtgn_salesunitidname", "nxtgn_sectorsapidname", "nxtgn_salesteam_concatinate", "nxtgn_id_customerquotesap", "nxtgn_actualclosedate", "nxtgn_ordersactualclosedate", "nxtgn_lastsubmissiondate", "nxtgn_totalrevenue_orders_calc_base", "nxtgn_countryid", "nxtgn_countryidname", "nxtgn_closereasons_concatenate", "nxtgn_competitorid", "nxtgn_othercompetitors", "nxtgn_competitoridname"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupsectors


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_lookupsector = rolandberger{[Schema="dbo",Item="nxtgn_lookupsector"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_lookupsector, each ([statecode] = 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_lookupsectorid", "nxtgn_name", "nxtgn_industryccid", "nxtgn_industryccidname"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Other Columns",{{"nxtgn_lookupsectorid", "nxtgn_id"}, {"nxtgn_industryccid", "nxtgn_ccid"}, {"nxtgn_industryccidname", "nxtgn_ccidname"}})
in
    #"Renamed Columns"
```


## Table: nxtgn_lookupthemes


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_lookuptheme = rolandberger{[Schema="dbo",Item="nxtgn_lookuptheme"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_nxtgn_lookuptheme, each ([statecode] = 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_lookupthemeid", "nxtgn_name", "nxtgn_functionccid", "nxtgn_functionccidname"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Other Columns",{{"nxtgn_lookupthemeid", "nxtgn_id"}, {"nxtgn_functionccid", "nxtgn_ccid"}, {"nxtgn_functionccidname", "nxtgn_ccidname"}})
in
    #"Renamed Columns"
```


## Table: systemusers (2)


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_systemuser = rolandberger{[Schema="dbo",Item="systemuser"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_systemuser, each ([nxtgn_islicensed] = true) and ([isdisabled] = false)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"systemuserid", "fullname", "nxtgn_lookupcountryidname", "nxtgn_lookupcountryid", "nxtgn_platformidname", "nxtgn_costcenteridname"})
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

