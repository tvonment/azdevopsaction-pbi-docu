



# M Code

|Dataset|[Emplyoee list reports_v01](./../Emplyoee-list-reports_v01.md)|
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
    rep_v_hr_entry_exit = Source{[Schema="rep",Item="v_hr_employee_entry_exit"]}[Data],
    #"Filtered Rows: Current exit sonly" = Table.SelectRows(rep_v_hr_entry_exit, each Date.IsInCurrentYear([ter_max_date]) or Date.IsInCurrentMonth([ter_max_date]) or Date.IsInNextMonth([ter_max_date]) or Date.IsInPreviousMonth([ter_max_date]) or [ter_max_date] = null)
in
    #"Filtered Rows: Current exit sonly"
```


## Table: ToE


```m
let
    Source = Excel.Workbook(File.Contents("\\muc-hr-1\hr_daten$\10_0_HR_Analytics\Dashboards\202308_ToEs.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"toe_id_ps", type text}, {"toe_description", type text}})
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


## Table: Refresh_date


```m
let
    Source = #table(type table[Date Last Refreshed=datetime], {{DateTime.LocalNow()}})
in
    Source
```


## Table: pub v_ll_platform_cc_1


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_v_ll_platform_cc = Source{[Schema="pub",Item="v_ll_platform_cc"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(pub_v_ll_platform_cc,{{"platform_id", type text}})
in
    #"Changed Type"
```


## Table: pub v_ll_platform_cc_2


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_v_ll_platform_cc = Source{[Schema="pub",Item="v_ll_platform_cc"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(pub_v_ll_platform_cc,{{"platform_id", type text}})
in
    #"Changed Type"
```


## Roles

### Industrials_1


Model Permission: Read

pub v_ll_platform_cc_1

```m
[platform_id] = "2000"
```


### Industrials_2


Model Permission: Read

pub v_ll_platform_cc_2

```m
[platform_id] = "2000"
```


### Operations_1


Model Permission: Read

pub v_ll_platform_cc_1

```m
[platform_id] = "3000"
```


### Operations_2


Model Permission: Read

pub v_ll_platform_cc_2

```m
[platform_id] = "3000"
```


### RPT_1


Model Permission: Read

pub v_ll_platform_cc_1

```m
[platform_id] = "6000"
```


### RPT_2


Model Permission: Read

pub v_ll_platform_cc_2

```m
[platform_id] = "6000"
```


### Regulated_Infrastructure_1


Model Permission: Read

pub v_ll_platform_cc_1

```m
[platform_id] = "5000"
```


### Regulated_Infrastructure_2


Model Permission: Read

pub v_ll_platform_cc_2

```m
[platform_id] = "5000"
```


### Health_Consumer_1


Model Permission: Read

pub v_ll_platform_cc_1

```m
[platform_id] = "1000"
```


### Health_Consumer_2


Model Permission: Read

pub v_ll_platform_cc_2

```m
[platform_id] = "1000"
```


### Investor_Support_1


Model Permission: Read

pub v_ll_platform_cc_1

```m
[platform_id] = "4000"
```


### Investor_Support_2


Model Permission: Read

pub v_ll_platform_cc_2

```m
[platform_id] = "4000"
```


### Services_1


Model Permission: Read

pub v_ll_platform_cc_1

```m
[platform_id] = "7000"
```


### Services_2


Model Permission: Read

pub v_ll_platform_cc_2

```m
[platform_id] = "7000"
```


### Digital_1


Model Permission: Read

pub v_ll_platform_cc_1

```m
[platform_id] = "8000"
```


### Digital_2


Model Permission: Read

pub v_ll_platform_cc_2

```m
[platform_id] = "8000"
```

