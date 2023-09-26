



# M Code

|Dataset|[Absence Dashboard RLS](./../Absence-Dashboard-RLS.md)|
| :--- | :--- |
|Workspace|[Mentor [Prod]](../../Workspaces/Mentor-[Prod].md)|

## Table: dim_employee


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="SELECT  [emp_id]#(lf)      ,[last_name]#(lf)      ,[first_name]#(lf)      ,[full_name]#(lf)#(lf)      ,[jobcode_id]#(lf)      ,[jobcode]#(lf)#(lf)      ,[work_location]#(lf)      ,[company_id]#(lf)      ,[company]#(lf)      ,[cc_id]#(lf)      ,[cc_name]#(lf)      ,[mentor_emp_id]#(lf)      ,[mentor_last_name]#(lf)      ,[pa_emp_id]#(lf)      ,[pa_emp_last_name]#(lf)      ,[emp_status]#(lf)#(lf)#(lf)      ,[email]#(lf)      ,[country_code]#(lf)#(lf)  FROM [datahub].[rep].[v_hr_employee] where emp_status = 'A' and [per_org]='EMP' "])
in
    Source
```


## Table: dim_date


```m
let
    dim_date =Sql.Database("muc-mssql-2", "datahub", [Query="select * from [pub].dim_date where year = 2022"])
in
    dim_date
```


## Table: fact_employee_target_absence_training


```m
let
     Source = Sql.Database("muc-mssql-2", "datahub", [Query="
SELECT a.*, b.vacation_hrs  as vacation_hours_in_approval
  FROM [datahub].[rep].[v_employee_utilization] a left join [rep].[v_employee_byd_absence_hours_in_approval] b
  on a.emp_id = b.emp_id and a.[calendar_day] = b.[calendar_day] where year(a.calendar_day) = 2022 "])
in
    Source
```


## Table: fact_employee_time_blanace


```m
let
     Source= Sql.Database("muc-mssql-2", "datahub", [Query="
SELECT *
  FROM [datahub].[rep].v_fc_byd_time_account_balance where year([bookable_from]) = 2022 "])
in
    Source
```


## Table: ll_report_color


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    ll_report_color = datahub{[Schema="pub",Item="ll_report_color"]}[Data]
in
    ll_report_color
```


## Table: MeasureTable


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WckksSVSKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: DataRefreshTable


```m
let 
  Source = Table.FromRecords(
    {  
      [Source = "Datahub", LastRefreshedAT = DateTime.LocalNow()] 
    }
  )
in
  Source
```


## Roles

### EmployeeRLS


Model Permission: Read

dim_employee

```m
or(or(or(LOWER(dim_employee[mentor_email]) = LOWER(USERPRINCIPALNAME()), LOWER(dim_employee[email]) = LOWER(USERPRINCIPALNAME())), LOWER(dim_employee[pa_email])= LOWER(USERPRINCIPALNAME())),LOWER(dim_employee[mentor_pa_email]) =LOWER(USERPRINCIPALNAME()))
```

