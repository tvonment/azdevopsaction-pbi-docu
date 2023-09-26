



# M Code

|Dataset|[Cash Pool](./../Cash-Pool.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: CP_CASH_POOL_BALANCES


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "RB_Treasury"),
    dbo_CP_CASH_POOL_BALANCES = Source{[Schema="dbo",Item="CP_CASH_POOL_BALANCES"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(dbo_CP_CASH_POOL_BALANCES,{{"DATE", type date}})
in
    #"Changed Type"
```


## Table: CP_CASH_POOL_BALANCES_YEAR_TO_DATE


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "RB_Treasury"),
    dbo_CP_CASH_POOL_BALANCES_YEAR_TO_DATE = Source{[Schema="dbo",Item="CP_CASH_POOL_BALANCES_YEAR_TO_DATE"]}[Data]
in
    dbo_CP_CASH_POOL_BALANCES_YEAR_TO_DATE
```


## Table: BYD_ROLAND_BERGER_COMPANIES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_ROLAND_BERGER_COMPANIES = ByD_ODP{[Schema="dbo",Item="BYD_ROLAND_BERGER_COMPANIES"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_BYD_ROLAND_BERGER_COMPANIES, each Text.EndsWith([FUNCTIONAL_UNIT_ID], "00000")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"ACCOUNT_ID", "ACCOUNT", "ACT_AS_ORG_UNIT", "COUNTRY_ISO2", "SAP_START", "EXPORTED_ON"}),
    #"Sorted Rows" = Table.Sort(#"Removed Columns",{{"ORGANIZATIONAL_CCENTER_ID", Order.Ascending}}),
    #"Filtered Rows1" = Table.SelectRows(#"Sorted Rows", each ([FUNCTIONAL_UNIT_ID] <> "52200000" and [FUNCTIONAL_UNIT_ID] <> "52300000")),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows1",{{"COUNTRY_ISO3", "Entity"}}),
    #"Filtered Rows2" = Table.SelectRows(#"Renamed Columns", each ([Entity] <> null and [Entity] <> "" and [Entity] <> "HRV" and [Entity] <> "NGA" and [Entity] <> "TUR") and ([COMPANY_NAME] <> "EIB" and [COMPANY_NAME] <> "MezzCo1" and [COMPANY_NAME] <> "PMH" and [COMPANY_NAME] <> "RB Augesco" and [COMPANY_NAME] <> "RB Myanmar" and [COMPANY_NAME] <> "RB RBInvH" and [COMPANY_NAME] <> "RB Tenzing" and [COMPANY_NAME] <> "RB Thailand HOL" and [COMPANY_NAME] <> "RBIH" and [COMPANY_NAME] <> "RBÖ" and [COMPANY_NAME] <> "Spielfeld")),
    #"Added Conditional Column" = Table.AddColumn(#"Filtered Rows2", "Entity Split", each if [ORGANIZATIONAL_CCENTER_ID] = "66000000" then "NLD Tenzing" else [Entity])
in
    #"Added Conditional Column"
```

