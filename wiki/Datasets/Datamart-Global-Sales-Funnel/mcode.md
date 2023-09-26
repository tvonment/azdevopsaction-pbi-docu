



# M Code

|Dataset|[Datamart Global Sales Funnel](./../Datamart-Global-Sales-Funnel.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: nxtgn_opportunityregistration


```m
let
  Source = Sql.Database("QK5Q44Q7JBJUVN6KTJWHDIHCJM-AQZYAXJJICSEFHFSWGDGZOBEDI.datamart.pbidedicated.windows.net", "datamart"),
  table = Source{[Schema = "model", Item = "nxtgn_opportunityregistration"]}[Data]
in
  table

```


## Table: nxtgn_shareofwallet


```m
let
  Source = Sql.Database("QK5Q44Q7JBJUVN6KTJWHDIHCJM-AQZYAXJJICSEFHFSWGDGZOBEDI.datamart.pbidedicated.windows.net", "datamart"),
  table = Source{[Schema = "model", Item = "nxtgn_shareofwallet"]}[Data]
in
  table

```

