



# M Code

|Dataset|[Travel Costs](./../Travel-Costs.md)|
| :--- | :--- |
|Workspace|[Travel & Mobility](../../Workspaces/Travel-&-Mobility.md)|

## Table: Data


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select * from [rep].[imp_travel_expense]"]),
    #"Gefilterte Zeilen" = Table.SelectRows(Source, each [period_date] > #datetime(2022, 12, 31, 0, 0, 0))
in
    #"Gefilterte Zeilen"
```


## Table: Date


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select * from [pub].[dim_date] where datekey >= 20230101 and [Date] <= (select max(period_date) from [sec].[imp_travel_expense] )"]),
    #"Filtered Rows" = Table.SelectRows(Source, each true)
in
    #"Filtered Rows"
```


## Table: maxReportDate


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="select 'Reporting Period: 01/2023 -  '+  format(max(period_date), 'MM/yyyy') as max_period_date from [sec].[imp_travel_expense]"])
in
    Source
```


## Table: Email


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="SELECT [emp_id]#(lf)      ,[email]#(lf)  FROM [datahub].[sec].[imp_hr_employee]#(lf)  WHERE [emp_status]  = 'A';", CreateNavigationProperties=false])
in
    Source
```


## Roles

### Security


Model Permission: Read

Email

```m
'Email'[email] = UserPrincipalName()
```

