



# M Code

|Dataset|[project status report_TC](./../project-status-report_TC.md)|
| :--- | :--- |
|Workspace|[FC_PSR](../../Workspaces/FC_PSR.md)|

## Table: dim_employee


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_psr_employee = Source{[Schema="rep",Item="v_fc_psr_employee"]}[Data],
    #"Appended Query" = Table.Combine({rep_v_fc_psr_employee, PlannedForUnknownEmployee}),
    #"Sorted Rows" = Table.Sort(#"Appended Query",{{"last_name", Order.Ascending}, {"first_name", Order.Ascending}}),
    #"Added Index" = Table.AddIndexColumn(#"Sorted Rows", "SortByNameIndex", 0, 1)
in
    #"Added Index"
```


## Table: dim_project


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub", [Query="SELECT *#(lf)  FROM [datahub].[rep].[v_fc_psr_project_data] where project_startdate >'2021-12-31'#(lf)  and project_number like 'CP%' or project_number like 'ICP%'"]),
    #"Renamed Columns" = Table.RenameColumns(Source,{{"is_master", "is_master (wrong)"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","Released MIS","Released",Replacer.ReplaceText,{"project_status"})
in
    #"Replaced Value"
```


## Table: dim_project_hierarchy


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_psr_project_hierarchy = Source{[Schema="rep",Item="v_fc_psr_project_hierarchy_test"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(rep_v_fc_psr_project_hierarchy,{{"is_master", type logical}})
in
    #"Changed Type"
```


## Table: fact_project_invoices_ppo


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_psr_project_invoices_ppo = Source{[Schema="rep",Item="v_fc_psr_project_invoices_ppo"]}[Data]
in
    rep_v_fc_psr_project_invoices_ppo
```


## Table: fact_project_oview_budget_costs


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_psr_project_oview_budget_costs = Source{[Schema="rep",Item="v_fc_psr_project_oview_budget_costs"]}[Data]
in
    rep_v_fc_psr_project_oview_budget_costs
```


## Table: fact_project_time_recording


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_psr_project_recording = Source{[Schema="rep",Item="v_fc_psr_time_recording"]}[Data]
in
    rep_v_fc_psr_project_recording
```


## Table: fact_project_time_planned


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_psr_project_time_planned = Source{[Schema="rep",Item="v_fc_psr_project_time_planned"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(rep_v_fc_psr_project_time_planned,null,"-999",Replacer.ReplaceValue,{"emp_id"}),
    #"Filtered Rows" = Table.SelectRows(#"Replaced Value", each [estimated_work_days] > 0)
in
    #"Filtered Rows"
```


## Table: fact_sales_order_items


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_psr_sales_order_items = Source{[Schema="rep",Item="v_fc_psr_sales_order_items"]}[Data]
in
    rep_v_fc_psr_sales_order_items
```


## Table: _Project Measures (budget/cost)


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Spalte ""1""" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Spalte ""1""", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Spalte ""1"""})
in
    #"Removed Columns"
```


## Table: DisplayProjectTableData


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("dZQxb4MwEIX/ioXULUOAtE3HpqQSQ5WopeoQdbDgmroyNnJMpPz72mAH2zgDisT7cu/unc3hkLwCoE3fHEEmiyRVj/lJk+/FISm3k5iFYsUlppOeq6cSPXiMLl+yMyc1NOrlKmLgyPdxC4d4uGXyeRr0x4iBkdbx4kZ9ulX4uZa9wnaFfus0aKt7+kOgjxYe8ugbXX1eeNtRkIQznXUWFNpTzBg0qgZSsFZWkTpeXGiPiZ4sXUebstQn6wz3FHC7Dhj6KvfGMVsG+rjbhtRYkjOgdzgDG/txSGfNMXJ24mxzMTiL7agibRhemsy25AP5HLABE4buEP+xM6/mpNlmAIYnYy/4H9QSvWFxJINpeDYsURbmcpnRliFQEUndWJcDr4mX/iR5C8KcX0+z//6QWPYnc3Xc8koQEhVYwnRvruKWNVZaB9L7ZkgTs8v0xZiKYgontBMNiHGwPACmXBg+Dp2nedh6AVRtXlxcKJvNzpkUnFLCjvY6ePrsdLaYMAM7+09NkEIAqy96oc4IyfWLde1flVShq946iuUPF61mnMXko3nPan3YPCoLqQ8VBB9M0lCqfqHV4a9yT/n+Bw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Field = _t, Sort = _t, IsTotal = _t, Type = _t, Part = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"IsTotal", type logical}, {"Sort", Int64.Type}, {"Type", Int64.Type}, {"Part", Int64.Type}})
in
    #"Changed Type"
```


## Table: rep v_fc_psr_permisson


```m
let
    Source = Sql.Databases("muc-mssql-2.rolandberger.net"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_fc_psr_permisson = datahub{[Schema="rep",Item="v_fc_psr_permisson"]}[Data]
in
    rep_v_fc_psr_permisson
```


## Table: rep v_fc_psr_permisson_admin


```m
let
    Source = Sql.Databases("muc-mssql-2.rolandberger.net"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_fc_psr_permisson_admin = datahub{[Schema="rep",Item="v_fc_psr_permisson_admin"]}[Data]
in
    rep_v_fc_psr_permisson_admin
```


## Table: _progressMeasures by status date


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: rep v_fc_psr_invoice


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_psr_invoice = Source{[Schema="rep",Item="v_fc_psr_invoice"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(rep_v_fc_psr_invoice,null,0,Replacer.ReplaceValue,{"CLEARED_AMOUNT_TC"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"AMOUNT_TC"})
in
    #"Replaced Value1"
```


## Table: ProjectStatus


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCkrNSU0sTk1R0lEyVIrViVZyzsmHcI0g3PzcgpzUErCIMVgkuCS/oADMN1GKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Status = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Status", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```


## Table: pub ll_fc_data_explanation


```m
let
    Source = Sql.Databases("muc-mssql-2.rolandberger.net"),
    datahub = Source{[Name="datahub"]}[Data],
    pub_ll_fc_data_explanation = datahub{[Schema="pub",Item="ll_fc_data_explanation"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_ll_fc_data_explanation, each ([IsActive] = true))
in
    #"Filtered Rows"
```


## Table: dim_service


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_ll_report_type_byd_service = Source{[Schema="rep",Item="v_ll_report_type_byd_service"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_ll_report_type_byd_service, each [report_id] = 100),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"service_description", "service_desc"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"sort_id", Int64.Type}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"sort_id", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: v_fc_psr_byd_project_internal_incurred_costs


```m
let
   
    rep_v_fc_psr_byd_project_internal_incurred_costs_tc = Sql.Database("muc-mssql-2.rolandberger.net", "datahub", [Query="SELECT *#(lf)  FROM [datahub].[rep].[v_fc_psr_byd_project_internal_incurred_costs]#(lf)  where [sales_order_currency] is not null"]),
    #"Removed Columns" = Table.RemoveColumns(rep_v_fc_psr_byd_project_internal_incurred_costs_tc,{ "category", "sort_id"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns",null,100,Replacer.ReplaceValue,{"category_id"})
in
    #"Replaced Value"
```


## Table: v_fc_psr_byd_sales_order_acquisition_performance


```m
let
    Source = Sql.Databases("muc-mssql-2.rolandberger.net"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_fc_psr_byd_sales_order_acquisition_performance = datahub{[Schema="rep",Item="v_fc_psr_byd_sales_order_acquisition_performance"]}[Data]
in
    rep_v_fc_psr_byd_sales_order_acquisition_performance
```


## Table: ll_fc_ie_cost_category


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_ll_report_type_byd_service = Source{[Schema="pub",Item="ll_fc_ie_cost_category"]}[Data]
in
    rep_v_ll_report_type_byd_service
```


## Table: rep v_fc_psr_down_payment


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    v_fc_psr_down_payment = Source{[Schema="rep",Item="v_fc_psr_down_payment"]}[Data]

in
    #"v_fc_psr_down_payment"
```


## Table: rep_v_fc_byd_customer_project_overview


```m
let
    Source = Sql.Databases("muc-mssql-2.rolandberger.net"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_fc_byd_customer_project_overview = datahub{[Schema="rep",Item="v_fc_byd_customer_project_overview"]}[Data]
in
    rep_v_fc_byd_customer_project_overview
```


## Roles

### PM


Model Permission: Read

rep v_fc_psr_permisson

```m
or([email] = userprincipalname(), CONTAINS('rep v_fc_psr_permisson_admin','rep v_fc_psr_permisson_admin'[email], USERPRINCIPALNAME(), 'rep v_fc_psr_permisson_admin'[report_id],100))
```


### ADMIN


Model Permission: Read
### Test eric


Model Permission: Read

rep v_fc_psr_permisson

```m
[email] = "eric.kirstetter@rolandberger.com"
```

