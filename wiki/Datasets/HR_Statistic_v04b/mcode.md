



# M Code

|Dataset|[HR_Statistic_v04b](./../HR_Statistic_v04b.md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: SwitchTable


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WcgtxVYrViVbySE1MSc4vzStRio0FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Measure = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Measure", type text}})
in
    #"Changed Type"
```


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
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each [Date] > #date(2016, 12, 1))
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


## Table: pub ll_cc


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_ll_cc = Source{[Schema="pub",Item="ll_cc"]}[Data]
in
    pub_ll_cc
```


## Table: rep v_hr_ll_age_cluster


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_ll_age_cluster = Source{[Schema="rep",Item="v_hr_ll_age_cluster"]}[Data]
in
    rep_v_hr_ll_age_cluster
```


## Table: platforms


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202308_platforms.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"platform_1_id", Int64.Type}, {"platform_1_name", type text}})
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


## Table: country test


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202309_Test user.xlsx"), null, true),
    #"country test_Sheet" = Source{[Item="country test",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"country test_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"company_id", Int64.Type}, {"email", type text}, {"platform_1_id", Int64.Type}})
in
    #"Changed Type"
```


## Table: platform test


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714505\OneDrive - Roland Berger Holding GmbH\Data, reports\PowerBI\202309_Test user.xlsx"), null, true),
    #"platform test_Sheet" = Source{[Item="platform test",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"platform test_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"company_id", Int64.Type}, {"email", type text}, {"platform_1_id", Int64.Type}})
in
    #"Changed Type"
```


## Roles

### Country View


Model Permission: Read

country test

```m
[email] = USERPRINCIPALNAME()
```


### Platform View


Model Permission: Read

platform test

```m
[email] = USERPRINCIPALNAME()
```

