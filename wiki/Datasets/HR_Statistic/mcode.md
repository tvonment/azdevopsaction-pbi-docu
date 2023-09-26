



# M Code

|Dataset|[HR_Statistic](./../HR_Statistic.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: SwitchTable


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WcgtxVYrViVbySE1MSc4vzStRio0FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Measure = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Measure", type text}})
in
    #"Changed Type"
```


## Table: rep v_hr_statistic_company_group


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_statistic_company_group = Source{[Schema="rep",Item="v_hr_statistic_company_group"]}[Data]
in
    rep_v_hr_statistic_company_group
```


## Table: rep v_hr_statistic_job_category


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_statistic_job_category = Source{[Schema="rep",Item="v_hr_statistic_job_category"]}[Data]
in
    rep_v_hr_statistic_job_category
```


## Table: pub dim_date


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_dim_date = Source{[Schema="pub",Item="dim_date"]}[Data]
in
    pub_dim_date
```


## Table: rep v_hr_statistic


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_statistic = Source{[Schema="rep",Item="v_hr_statistic"]}[Data]
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
    rep_v_hr_entry_exit = Source{[Schema="rep",Item="v_hr_entry_exit"]}[Data]
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

