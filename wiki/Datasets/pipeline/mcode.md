



# M Code

|Dataset|[pipeline](./../pipeline.md)|
| :--- | :--- |
|Workspace|[Global Recruiting](../../Workspaces/Global-Recruiting.md)|

## Table: dim region country


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_diversity_ll_region_country = Source{[Schema="rep",Item="v_diversity_ll_region_country"]}[Data]
in
    rep_v_diversity_ll_region_country
```


## Table: sec ll_jobcode_to_subcategory


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    sec_ll_jobcode_to_subcategory = Source{[Schema="sec",Item="ll_jobcode_to_subcategory"]}[Data],
    #"Merged Queries" = Table.NestedJoin(sec_ll_jobcode_to_subcategory, {"job_subcategory_id"}, #"sec ll_job_subcategory", {"job_subcategory_id"}, "sec ll_job_subcategory", JoinKind.LeftOuter),
    #"Expanded sec ll_job_subcategory" = Table.ExpandTableColumn(#"Merged Queries", "sec ll_job_subcategory", {"job_subcategory", "job_subcategory_short"}, {"job_subcategory", "job_subcategory_short"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded sec ll_job_subcategory", each ([job_subcategory_short] <> null))
in
    #"Filtered Rows"
```


## Table: DimFunctionGrouping


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45Wcs7PKy7NKUnMKylWitWJVgpOLSrLTE4FcmIB", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [FunctionGroup = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"FunctionGroup", type text}}),
    #"Added Index" = Table.AddIndexColumn(#"Changed Type", "Index", 0, 1, Int64.Type)
in
    #"Added Index"
```


## Table: DimGrade


```m
let
    Source = #"MappingJobcode2Grade",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"Grade"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Added Index" = Table.AddIndexColumn(#"Removed Duplicates", "Index", 0, 1, Int64.Type)
in
    #"Added Index"
```


## Table: RefreshInfo


```m
let
    Source = RefreshDate,
    #"Converted to Table" = #table(1, {{Source}}),
    #"Renamed Columns" = Table.RenameColumns(#"Converted to Table",{{"Column1", "RefreshDate"}}),
    #"Changed Type" = #table(
{"RefreshDate"},
{
  {RefreshDate}
}
),
    #"Changed Type1" = Table.TransformColumnTypes(#"Changed Type",{{"RefreshDate", type date}})
in
    #"Changed Type1"
```


## Table: v_rep_pipeline


```m
let
    Source = Sql.Database("muc-mssql-2", "SmartRecruiters"),
    dbo_v_rep_pipeline = Source{[Schema="dbo",Item="v_rep_pipeline"]}[Data],
    #"Merged Queries" = Table.NestedJoin(dbo_v_rep_pipeline, {"HR country (access rights)"}, ll_country_region, {"HR_Country"}, "ll_country_region", JoinKind.LeftOuter),
    #"Changed Type" = Table.TransformColumnTypes(#"Merged Queries",{{"Application Creation Date", type date}, {"Application Start Date", type date}})
in
    #"Changed Type"
```


## Table: ll_funnel_status


```m
let
    Source = Sql.Database("muc-mssql-2", "SmartRecruiters"),
    dbo_ll_funnel_status = Source{[Schema="dbo",Item="ll_funnel_status"]}[Data]
in
    dbo_ll_funnel_status
```


## Table: ll_target_university


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    SmartRecruiters = Source{[Name="SmartRecruiters"]}[Data],
    dbo_ll_target_university = SmartRecruiters{[Schema="dbo",Item="ll_target_university"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_ll_target_university, each ([Target_Uni_Focus] = "DACH"))
in
    #"Filtered Rows"
```


## Table: ll_ats_status


```m
let
    Source = Sql.Database("muc-mssql-2", "smartrecruiters"),
    dbo_ll_ats_status = Source{[Schema="dbo",Item="ll_ats_status"]}[Data]
in
    dbo_ll_ats_status
```


## Table: _Measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: ll_offer_level_category


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    SmartRecruiters = Source{[Name="SmartRecruiters"]}[Data],
    dbo_ll_offer_level_category = SmartRecruiters{[Schema="dbo",Item="ll_offer_level_category"]}[Data]
in
    dbo_ll_offer_level_category
```

