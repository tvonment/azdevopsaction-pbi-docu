



# M Code

|Dataset|[KAM Dashboard](./../KAM-Dashboard.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

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
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_opportunityregistrationid", "createdon", "ownerid", "owneridname", "statecodename", "statuscodename", "nxtgn_topic", "nxtgn_accountid", "nxtgn_description", "nxtgn_estclosedate", "nxtgn_estrevenue", "transactioncurrencyid", "nxtgn_probability", "nxtgn_accountidname", "nxtgn_keyaccount", "nxtgn_leadstatusname", "nxtgn_functionccid", "nxtgn_industryccid", "nxtgn_functionccidname", "nxtgn_industryccidname", "nxtgn_relevantforforecastname", "nxtgn_sectorsapid", "nxtgn_themesapid", "nxtgn_themesapidname", "nxtgn_salesunitidname", "nxtgn_sectorsapidname", "nxtgn_salesteam_concatinate", "nxtgn_id_customerquotesap", "nxtgn_actualclosedate", "nxtgn_ordersactualclosedate", "nxtgn_lastsubmissiondate", "nxtgn_totalrevenue_orders_calc_base", "nxtgn_countryid", "nxtgn_countryidname", "nxtgn_closereasons_concatenate", "nxtgn_competitorid", "nxtgn_othercompetitors", "nxtgn_competitoridname"})
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


## Table: accounts


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_opportunityregistration = rolandberger{[Schema="dbo",Item="account"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(dbo_nxtgn_opportunityregistration,{"accountid", "name", "nxtgn_keyaccount", "nxtgn_keyaccountname"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([nxtgn_keyaccount] <> null))
in
    #"Filtered Rows"
```


## Table: salesorders


```m
let
    Source = Sql.Databases("rolandberger.crm4.dynamics.com,5558"),
    rolandberger = Source{[Name="rolandberger"]}[Data],
    dbo_nxtgn_opportunityregistration = rolandberger{[Schema="dbo",Item="salesorder"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(dbo_nxtgn_opportunityregistration,{"salesorderid", "name", "transactioncurrencyid", "statecode", "statecodename", "statuscode", "statuscodename", "submitdate", "accountid", "accountidname", "nxtgn_billtoaccountid", "nxtgn_salesleadid", "nxtgn_salesrevenue", "nxtgn_salesrevenue_base", "nxtgn_uuid", "nxtgn_salesleadidname", "nxtgn_billtoaccountidname", "nxtgn_salesrevenue_net", "nxtgn_salesrevenue_net_base", "nxtgn_id_sap", "nxtgn_netvalueexclexpenses", "nxtgn_netvalueexclexpenses_base", "nxtgn_keyaccount", "nxtgn_keyaccountname", "customerid"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Other Columns",{{"submitdate", type date}})
in
    #"Changed Type"
```

