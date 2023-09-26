



# M Code

|Dataset|[proClient Datamart](./../proClient-Datamart.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_project


```m
let
    Source = Sql.Database("QK5Q44Q7JBJUVN6KTJWHDIHCJM-L4OEDA3N5UNETJQ5ZV24AK3W7M.datamart.pbidedicated.windows.net", "datamart"),
    table = Source{[Schema = "model", Item = "nxtgn_project"]}[Data]
in
    table
```

