



# M Code

|Dataset|[Exit_List_v01](./../Exit_List_v01.md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: pub v_ll_company


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_statistic_company_group = Source{[Schema="pub",Item="v_ll_company"]}[Data]
in
    rep_v_hr_statistic_company_group
```


## Table: rep v_job


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_statistic_job_category = Source{[Schema="pub",Item="v_ll_job"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_hr_statistic_job_category, each ([is_job_active] = true))
in
    #"Filtered Rows"
```


## Table: pub dim_date


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_dim_date = Source{[Schema="pub",Item="dim_date"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_dim_date, each true),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each [Date] > #date(2019, 12, 1))
in
    #"Filtered Rows1"
```


## Table: rep v_hr_statistic


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_statistic = Source{[Schema="rep",Item="v_hr_employee_statistic"]}[Data]
in
    rep_v_hr_statistic
```


## Table: pub ll_gender


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_ll_gender = Source{[Schema="pub",Item="ll_gender"]}[Data]
in
    pub_ll_gender
```


## Table: rep v_hr_entry_exit


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_entry_exit = Source{[Schema="rep",Item="v_hr_employee_entry_exit"]}[Data]
in
    rep_v_hr_entry_exit
```


## Table: platform_1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202308_platforms.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="platform_1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"platform_1_id", type text}, {"platform_1_name", type text}})
in
    #"Changed Type"
```


## Table: ToE


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202308_ToEs.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"toe_id_ps", type text}, {"toe_description", type text}})
in
    #"Changed Type"
```


## Table: platform_2


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202308_platforms.xlsx"), null, true),
    platform_2_Sheet = Source{[Item="platform_2",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(platform_2_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"platform_2_id", type text}, {"platform_2_name", type text}})
in
    #"Changed Type"
```


## Table: rep v_hr_employee_active


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_active = Source{[Schema="rep",Item="v_hr_employee_active"]}[Data]
in
    rep_v_hr_employee_active
```


## Table: platform test


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202309_Test user.xlsx"), null, true),
    #"platform test_Sheet" = Source{[Item="platform test",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"platform test_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"company_id", Int64.Type}, {"email", type text}, {"platform_1_id", type text}})
in
    #"Changed Type"
```


## Roles

### Industrials


Model Permission: Read

platform_1

```m
[platform_1_id] = "2000"
```



platform_2

```m
[platform_2_id] = "2000"
```


### Industrials_1


Model Permission: Read

platform_1

```m
[platform_1_id] = "2000"
```


### Industrials_2


Model Permission: Read

platform_2

```m
[platform_2_id] = "2000"
```

