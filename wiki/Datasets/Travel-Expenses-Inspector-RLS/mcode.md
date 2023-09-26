



# M Code

|Dataset|[Travel Expenses Inspector RLS](./../Travel-Expenses-Inspector-RLS.md)|
| :--- | :--- |
|Workspace|[Reiser](../../Workspaces/Reiser.md)|

## Table: Data


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select * from [rep].[imp_travel_expense]"])
in
    Source
```


## Table: Functions


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select * from rbs.v_travel_expense_job_category"])
in
    Source
```


## Table: Date


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select * from [pub].[dim_date] where datekey >= 20210701 and [Date] <= (select max(period_date) from [sec].[imp_travel_expense] )"]),
    #"Filtered Rows" = Table.SelectRows(Source, each true)
in
    #"Filtered Rows"
```


## Table: Category


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select * from pub.ll_travel_category"])
in
    Source
```


## Table: maxReportDate


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select 'Reporting Period: 07/2021 -  '+  format(max(period_date), 'MM/yyyy') as max_period_date from [sec].[imp_travel_expense]"])
in
    Source
```


## Table: Dim_CC


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="  
        select  sort_id, [platform_id] as cc_id, [platform] as cc_name
		FROM [datahub].[pub].[ll_platform] where active = 1  and ([platform_id] <= 9000 or [platform_id]=9900) order by sort_id"])
in
    Source
```


## Table: Permission_Rule


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select * from rep.[v_travel_expense_permission] where is_admin=0"])
in
    Source
```


## Table: v_travel_expense_permisson_admin


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_travel_expense_permisson_admin = Source{[Schema="rep",Item="v_travel_expense_permisson_admin"]}[Data]
in
    rep_v_travel_expense_permisson_admin
```

