



# M Code

|Dataset|[proClient Dashboard](./../proClient-Dashboard.md)|
| :--- | :--- |
|Workspace|[proClient](../../Workspaces/proClient.md)|

## Table: pub dim_date


```m
let
    Source = Sql.Database("muc-mssql-2", "Datahub"),
    pub_dim_date = Source{[Schema="pub",Item="dim_date"]}[Data]
in
    pub_dim_date
```


## Table: v_km_ll_answer_text


```m
let
    Source = Sql.Database("muc-mssql-2", "Datahub"),
    rep_v_km_ll_answer_text = Source{[Schema="rep",Item="v_km_ll_answer_text"]}[Data]
in
    rep_v_km_ll_answer_text
```


## Table: v_km_proCLIENT_project_unpivot


```m
let
    Source = Sql.Database("muc-mssql-2", "Datahub"),
    rep_v_km_proCLIENT_project = Source{[Schema="rep",Item="v_km_proCLIENT_project"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_km_proCLIENT_project, each true),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"answer_q1", "answer_q2", "answer_q3", "answer_q4", "answer_q5", "answer_q6", "answer_q7", "answer_q8", "answer_q9", "answer_q10", "answer_q11"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"ID", "project_number", "project_title", "account", "feedback_requested_date", "feedback_recieved_date", "industry_cc", "functional_cc", "responsible_unit", "responsible_unit_new", "delivery_manager_cc", "delivery_manager_cc_new", "delivery_manager_country_code", "delivery_manager", "project_manager"}, "Attribute", "Value")
in
    #"Unpivoted Columns"
```


## Table: nps_calculation


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlDSAeJYnWglQyBL1xDMNEIwjRFMEwTTFME0QzDN4WZZwFmWQBZE1tAAwowFAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [score_id = _t, score_value = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"score_id", Int64.Type}, {"score_value", Int64.Type}})
in
    #"Changed Type"
```


## Table: rep v_km_ll_country_to_region


```m
let
    Source = Sql.Database("muc-mssql-2", "Datahub"),
    rep_v_km_ll_country_to_region = Source{[Schema="rep",Item="v_km_ll_country_to_region"]}[Data]
in
    rep_v_km_ll_country_to_region
```


## Table: rep v_km_proCLIENT_feedback


```m
let
    Source = Sql.Database("muc-mssql-2", "Datahub"),
    rep_v_km_proCLIENT_feedback = Source{[Schema="rep",Item="v_km_proCLIENT_feedback"]}[Data]
in
    rep_v_km_proCLIENT_feedback
```


## Table: rep ll_km_cc


```m
let
    Source = Sql.Database("muc-mssql-2", "Datahub"),
    rep_ll_km_cc = Source{[Schema="rep",Item="ll_km_cc"]}[Data]
in
    rep_ll_km_cc
```

