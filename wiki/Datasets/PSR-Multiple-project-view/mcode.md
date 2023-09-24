



# M Code

|Dataset|[PSR Multiple project view](./../PSR-Multiple-project-view.md)|
| :--- | :--- |
|Workspace|[IFRS_Reporting [QA]](../../Workspaces/IFRS_Reporting-[QA].md)|

## Table: dim_employee


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_employee = Source{[Schema="rep",Item="v_fc_psr_employee"]}[Data],
    #"Appended Query" = Table.Combine({rep_v_fc_psr_employee, PlannedForUnknownEmployee}),
    #"Sorted Rows" = Table.Sort(#"Appended Query",{{"last_name", Order.Ascending}, {"first_name", Order.Ascending}}),
    #"Added Index" = Table.AddIndexColumn(#"Sorted Rows", "SortByNameIndex", 0, 1)
in
    #"Added Index"
```

OpenAI API Key is not configured
## Table: dim_project


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_project_data = Source{[Schema="rep",Item="v_fc_psr_project_data"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(rep_v_fc_psr_project_data,{{"is_master", "is_master (wrong)"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","Released MIS","Released",Replacer.ReplaceText,{"project_status"})
in
    #"Replaced Value"
```

OpenAI API Key is not configured
## Table: dim_project_hierarchy


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_project_hierarchy = Source{[Schema="rep",Item="v_fc_psr_project_hierarchy_test"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(rep_v_fc_psr_project_hierarchy,{{"is_master", type logical}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: fact_project_invoices_ppo


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_project_invoices_ppo = Source{[Schema="rep",Item="v_fc_psr_project_invoices_ppo"]}[Data]
in
    rep_v_fc_psr_project_invoices_ppo
```

OpenAI API Key is not configured
## Table: fact_project_oview_budget_costs


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_project_oview_budget_costs = Source{[Schema="rep",Item="v_fc_psr_project_oview_budget_costs"]}[Data]
in
    rep_v_fc_psr_project_oview_budget_costs
```

OpenAI API Key is not configured
## Table: fact_project_time_recording


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_project_recording = Source{[Schema="rep",Item="v_fc_psr_time_recording"]}[Data]
in
    rep_v_fc_psr_project_recording
```

OpenAI API Key is not configured
## Table: fact_project_time_planned


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_project_time_planned = Source{[Schema="rep",Item="v_fc_psr_project_time_planned"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(rep_v_fc_psr_project_time_planned,null,"-999",Replacer.ReplaceValue,{"emp_id"}),
    #"Filtered Rows" = Table.SelectRows(#"Replaced Value", each [estimated_work_days] > 0)
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: fact_sales_order_items


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_sales_order_items = Source{[Schema="rep",Item="v_fc_psr_sales_order_items"]}[Data]
in
    rep_v_fc_psr_sales_order_items
```

OpenAI API Key is not configured
## Table: _Project Measures (budget/cost)


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Spalte ""1""" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Spalte ""1""", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Spalte ""1"""})
in
    #"Removed Columns"
```

OpenAI API Key is not configured
## Table: DisplayProjectTableData


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("dZRPj4IwEMW/SkOyNw8Crn+Oq7iJh41GMXswe2hgdLspranFxG+/BVppSz0QE97PeTNvWk6n6BMALevyAjIaRbF69E8c/YxO0Wbdi4kv5lxi2uupenJRg8M05TfszkkBpXo5CRhY8nvYwiKmr0yOt1afBQy0NA8X1+riVeGPQtYK22bNW6tBU93Rp57eWTjIzDV6+qx4daUgCWdN1olXaEcxY1CqGkjBjTIJ1HHiQjtMmsniebApQx3ZVXMLj9tegaHvzU47JmNP73ZbkgJLcge0hzuwrh+LtNYcIgcnzjQXgpPQjnJS+eHF0WBLLpAOARMwYegN8bOZeTIk9TY90D8ZO8H/oJDoC4sLaU39s2GITaYvlx5t7AM5kdSOddzyDbGqb5JXIPT5dTTz74PEsr7pq2OXV4KQKMMS+nvzFNesNNLck/bLNk3MHv0Xoy+KKdzQVpQgusFSD+hzYfjSdh4nfusZULV58bChdDA7Z1JwSgm7mOvg6IPTWWHCNGztP9ZBCgGseDQLtUaInl+sZ/+qpApd9XalWJ65qNwQ0s67ZkVz1mwo8aGDioELN6JOyX+hAtdbCT//", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Field = _t, Sort = _t, IsTotal = _t, Type = _t, Part = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"IsTotal", type logical}, {"Sort", Int64.Type}, {"Type", Int64.Type}, {"Part", Int64.Type}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: rep v_fc_psr_permisson


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_fc_psr_permisson = datahub{[Schema="rep",Item="v_fc_psr_permisson"]}[Data]
in
    rep_v_fc_psr_permisson
```

OpenAI API Key is not configured
## Table: rep v_fc_psr_permisson_admin


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_fc_psr_permisson_admin = datahub{[Schema="rep",Item="v_fc_psr_permisson_admin"]}[Data]
in
    rep_v_fc_psr_permisson_admin
```

OpenAI API Key is not configured
## Table: _progressMeasures by status date


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```

OpenAI API Key is not configured
## Table: rep v_fc_psr_invoice


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_psr_invoice = Source{[Schema="rep",Item="v_fc_psr_invoice"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(rep_v_fc_psr_invoice,null,0,Replacer.ReplaceValue,{"CLEARED_AMOUNT_TC"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"AMOUNT_TC"})
in
    #"Replaced Value1"
```

OpenAI API Key is not configured
## Table: ProjectStatus


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCkrNSU0sTk1R0lEyVIrViVZyzsmHcI0g3PzcgpzUErCIMVgkuCS/oADMN1GKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Status = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Status", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: pub ll_fc_data_explanation


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    pub_ll_fc_data_explanation = datahub{[Schema="pub",Item="ll_fc_data_explanation"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_ll_fc_data_explanation, each ([IsActive] = true))
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: dim_service


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_report_type_byd_service = Source{[Schema="rep",Item="v_ll_report_type_byd_service"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_ll_report_type_byd_service, each [report_id] = 100),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"service_description", "service_desc"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"sort_id", Int64.Type}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"sort_id", Order.Ascending}})
in
    #"Sorted Rows"
```

OpenAI API Key is not configured
## Table: v_fc_psr_byd_project_internal_incurred_costs


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_report_type_byd_service = Source{[Schema="rep",Item="v_fc_psr_byd_project_internal_incurred_costs"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(rep_v_ll_report_type_byd_service,{ "category", "sort_id"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns",null,100,Replacer.ReplaceValue,{"category_id"})
in
    #"Replaced Value"
```

OpenAI API Key is not configured
## Table: v_fc_psr_byd_sales_order_acquisition_performance


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_fc_psr_byd_sales_order_acquisition_performance = datahub{[Schema="rep",Item="v_fc_psr_byd_sales_order_acquisition_performance"]}[Data]
in
    rep_v_fc_psr_byd_sales_order_acquisition_performance
```

OpenAI API Key is not configured
## Table: ll_fc_ie_cost_category


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_report_type_byd_service = Source{[Schema="pub",Item="ll_fc_ie_cost_category"]}[Data]
in
    rep_v_ll_report_type_byd_service
```

OpenAI API Key is not configured
## Roles

### PM


Model Permission: Read

rep v_fc_psr_permisson

```m
or([email] = userprincipalname(), CONTAINS('rep v_fc_psr_permisson_admin','rep v_fc_psr_permisson_admin'[email], USERPRINCIPALNAME(), 'rep v_fc_psr_permisson_admin'[report_id],100))
```

OpenAI API Key is not configured
### ADMIN


Model Permission: Read
### Test eric


Model Permission: Read

rep v_fc_psr_permisson

```m
[email] = "eric.kirstetter@rolandberger.com"
```

OpenAI API Key is not configured