



# M Code

|Dataset|[ParPri ProjectMatrix - ImportQ](./../ParPri-ProjectMatrix---ImportQ.md)|
| :--- | :--- |
|Workspace|[Partner_Principal_Project_Matrix](../../Workspaces/Partner_Principal_Project_Matrix.md)|

## Table: ParPriApp


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="SELECT CONVERT(varchar,[year]) as Year#(lf)      ,[max_month]#(lf)      ,[project_number]#(lf)      ,[project_client]#(lf)      ,[project_name]#(lf)      ,[order_income]#(lf)      ,[acquisition_performance]#(lf)      ,[acquisition_performance_adj]#(lf)      ,[Type]#(lf)  FROM [datahub].[ppa].[v_pri_par_appoint_acp_and_oi_per_year]", CreateNavigationProperties=false])
in
    Source
```

