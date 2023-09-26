



# M Code

|Dataset|[public_holidays](./../public_holidays.md)|
| :--- | :--- |
|Workspace|[Public](../../Workspaces/Public.md)|

## Table: pub ll_location_public_holiday


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_ll_location_public_holiday = Source{[Schema="pub",Item="ll_location_public_holiday"]}[Data]
in
    pub_ll_location_public_holiday
```


## Table: ll_location_weekend_days


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_ll_location_weekend_days = Source{[Schema="pub",Item="ll_location_weekend_days"]}[Data]
in
    pub_ll_location_weekend_days
```

