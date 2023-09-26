



# M Code

|Dataset|[CRM Key Account Mapping](./../CRM-Key-Account-Mapping.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: account


```m
let
    Source = Sql.Database("QK5Q44Q7JBJUVN6KTJWHDIHCJM-3LIYXXN73UJURMKGSWUNTCULIM.datamart.pbidedicated.windows.net", "datamart"),
    table = Source{[Schema = "model", Item = "account"]}[Data]
in
    table
```

