



# M Code

|Dataset|[Central Graphics Statistic](./../Central-Graphics-Statistic.md)|
| :--- | :--- |
|Workspace|[Central Graphics](../../Workspaces/Central-Graphics.md)|

## Table: vEmpStaffingDetail_Report


```m
let
    Source = Sql.Database("muc-mssql-5", "GGP"),
    dbo_vEmpStaffingDetail_Report = Source{[Schema="dbo",Item="vEmpStaffingDetail_Report"]}[Data]
in
    dbo_vEmpStaffingDetail_Report
```


## Table: pub dim_date


```m
let
    Source = Sql.Database("muc-mssql-2", "Datahub"),
    pub_dim_date = Source{[Schema="pub",Item="dim_date"]}[Data]
in
    pub_dim_date
```


## Table: vStaffingRequestDetail_Report


```m
let
    Source = Sql.Database("muc-mssql-5", "GGP"),
    dbo_vStaffingRequestDetail_Report = Source{[Schema="dbo",Item="vStaffingRequestDetail_Report"]}[Data]
in
    dbo_vStaffingRequestDetail_Report
```


## Table: vOrderFeedback_Report


```m
let
    Source = Sql.Database("muc-mssql-5", "GGP"),
    dbo_vOrderFeedback_Report = Source{[Schema="dbo",Item="vOrderFeedback_Report"]}[Data]
in
    dbo_vOrderFeedback_Report
```

