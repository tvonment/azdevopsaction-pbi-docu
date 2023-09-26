



# M Code

|Dataset|[diversity](./../diversity.md)|
| :--- | :--- |
|Workspace|[HR Head](../../Workspaces/HR-Head.md)|

## Table: fact hr statistics


```m
let
    Source = #"rep v_hr_statistic",
    Custom1 = Table.SelectRows
(
Source, each ([validfrom_date] < #date(CurrentYear, 1, 1) and Date.Month([validfrom_date]) = 12) //december of prev years 
                    or ([validfrom_date] > #date(CurrentYear, 12, 1) and Date.Month([validfrom_date]) = 1) //january of following years
                    or (Date.Year ([validfrom_date]) = CurrentYear and Date.Month ([validfrom_date]) = CurrentMonth ) // current month values of current year
)
in
    Custom1
```


## Table: CurrentYear


```m
let
    Source = 2023 //Date.Year (RefreshDate)

in
    Source
```


## Table: fact entry exit


```m
let
    Source = #"imp hr entry exit"
in
    Source
```


## Table: CurrentMonth


```m
let
    Source = 6 // Date.Month (RefreshDate)

in
    Source
```


## Table: fact utilization by month


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="SELECT #(lf)[emp_id]#(lf), year([report_month]) as year #(lf), month([report_month]) as month #(lf),[productive_hours_utilization] as productive_hours#(lf),[target_hours_utilization] as target_hours_adj#(lf),target_hours_fte #(lf)FROM [datahub].[rep].[v_employee_utilization_incl_mis_cy]", CreateNavigationProperties=false]),
    #"Replaced Value" = Table.ReplaceValue(Source,null,0,Replacer.ReplaceValue,{"productive_hours"}),
    #"Filtered Rows" = Table.SelectRows(#"Replaced Value", each ([target_hours_adj] <> 0)),
    #"Added Custom1" = Table.AddColumn(#"Filtered Rows", "FirstOfMonth", each #date([year],[month],1), Date.Type),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom1",{"year", "month"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"emp_id", "FirstOfMonth"}, #"rep v_hr_statistic", {"emp_id", "validfrom_date"}, "rep v_hr_statistic", JoinKind.LeftOuter),
    #"Expanded rep v_hr_statistic" = Table.ExpandTableColumn(#"Merged Queries", "rep v_hr_statistic", {"cc_id", "sex", "country_company", "TOEGroupIndex", "FunctionGroupIndex", "StatisticalRelevantIndex", "GradeIndex"}, {"cc_id", "sex", "country_company", "TOEGroupIndex", "FunctionGroupIndex", "StatisticalRelevantIndex", "GradeIndex"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded rep v_hr_statistic", each [country_company] <> null and [country_company] <> "")
in
    #"Filtered Rows1"
```


## Table: dim region country


```m
let
    Source = #"country statistics",
    #"Appended Query" = Table.Combine({Source, #"country hr entry exit", #"country hr employee"}),
    #"Removed Duplicates" = Table.Distinct(#"Appended Query"),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each ([region] <> null and [region] <> "Not Assigned"))
in
    #"Filtered Rows"
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


## Table: DimTOEGrouping


```m
let
    Source = #"Mapping TOE2Grouping",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"TOE Group"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Added Index" = Table.AddIndexColumn(#"Removed Duplicates", "Index", 0, 1, Int64.Type)
in
    #"Added Index"
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


## Table: DimStatisticalRelevant


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WKikqTVWK1YlWSkvMKQayYgE=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [statistic_relevant = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"statistic_relevant", type logical}}),
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


## Table: project_assessment


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    dbo_project_assessment = Source{[Schema="rep",Item="div_project_assessment"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(dbo_project_assessment, each ([submit_date] <> null)),
    #"Replaced Value" = Table.ReplaceValue(#"Gefilterte Zeilen","USA","United States of America",Replacer.ReplaceText,{"country"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Russia","Russian Federation",Replacer.ReplaceText,{"country"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","Netherland","Netherlands",Replacer.ReplaceText,{"country"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","Korea","Korea, Republic of",Replacer.ReplaceText,{"country"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3",null,"N/A",Replacer.ReplaceValue,{"country"}),
    #"Merged Queries" = Table.NestedJoin(#"Replaced Value4", {"country"}, #"pub v_ll_rb_country", {"country"}, "pub v_ll_rb_country", JoinKind.LeftOuter),
    #"Expanded pub v_ll_rb_vountry" = Table.ExpandTableColumn(#"Merged Queries", "pub v_ll_rb_country", {"country_code_iso3"}, {"country_code_iso3"})
in
    #"Expanded pub v_ll_rb_vountry"
```


## Table: flags


```m
let
    Source = #"pub ll_country_flag"
in
    Source
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


## Table: v_rep_data_diverstiy


```m
let
    Source = Sql.Database("muc-mssql-2", "SmartRecruiters"),
    dbo_v_rep_data_diverstiy = Source{[Schema="dbo",Item="v_rep_data_diverstiy"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(dbo_v_rep_data_diverstiy,{{"Invited to test", type text}, {"Successful test", type text}}),
    #"Merged Queries" = Table.NestedJoin(#"Geänderter Typ", {"HR country (access rights)"}, ll_country_region, {"HR_Country"}, "ll_country_region", JoinKind.LeftOuter),
    #"Expanded ll_country_region" = Table.ExpandTableColumn(#"Merged Queries", "ll_country_region", {"Country_Code"}, {"Country_Code"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded ll_country_region",{{"Application Creation Date", type date}}),
    #"Filtered CurrentYear" = Table.SelectRows(#"Changed Type", each Date.Year([Application Creation Date]) = CurrentYear)
in
    #"Filtered CurrentYear"
```


## Table: ll_funnel_status


```m
let
    Source = Sql.Database("muc-mssql-2", "SmartRecruiters"),
    dbo_ll_funnel_status = Source{[Schema="dbo",Item="ll_funnel_status"]}[Data]
in
    dbo_ll_funnel_status
```


## Table: peakon_mapping_country


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    dbo_peakon_mapping_country = Quelle{[Schema="pkn",Item="peakon_mapping_country"]}[Data]
in
    dbo_peakon_mapping_country
```


## Table: peakon_mapping_question


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    dbo_peakon_mapping_question = Quelle{[Schema="pkn",Item="peakon_mapping_question"]}[Data]
in
    dbo_peakon_mapping_question
```


## Table: peakon_results


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    dbo_peakon_results = Quelle{[Schema="pkn",Item="peakon_results"]}[Data]
in
    dbo_peakon_results
```


## Table: peakon_results_by_driver


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    dbo_peakon_results_by_driver = Quelle{[Schema="pkn",Item="peakon_results_by_driver"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(dbo_peakon_results_by_driver, each ([driver_id] = "accomplishment" or [driver_id] = "autonomy" or [driver_id] = "free_opinions" or [driver_id] = "goal_setting" or [driver_id] = "growth" or [driver_id] = "management_support" or [driver_id] = "meaningful_work" or [driver_id] = "organisational_fit" or [driver_id] = "peer_relationship" or [driver_id] = "recognition" or [driver_id] = "reward" or [driver_id] = "strategy" or [driver_id] = "workload"))
in
    #"Gefilterte Zeilen"
```


## Table: peakon_mapping_level


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    dbo_peakon_mapping_level = Quelle{[Schema="pkn",Item="peakon_mapping_level"]}[Data]
in
    dbo_peakon_mapping_level
```


## Table: peakon_results_by_question


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    dbo_peakon_results_by_question = Quelle{[Schema="pkn",Item="peakon_results_by_question"]}[Data]
in
    dbo_peakon_results_by_question
```


## Table: peakon_results_by_level


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    dbo_peakon_results_by_level = Quelle{[Schema="pkn",Item="peakon_results_by_level"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(dbo_peakon_results_by_level, each ([nps] <> null))
in
    #"Gefilterte Zeilen"
```


## Table: peakon_levels_for_report


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("dY8xD4MgEIX/imF2KKAos1NNTEgdjQOxpKEhYBD+f7lqTGvtcAncve+9u2FAbYNyhKEorgt6Sa82Wu181ji7RBOkDak3mbgE5dGYDwgIshPA/pX2DYxpqopzwsC9Vwf3DLzuKkhtNgYaxcaU1SmDvxnRQaNcGcYhUHj3VFPIOmnlQ/lfAlLYllKRE+Kwl7hdQb0fviLaTnqW5nC3SP/6rSSYcogW0gebph+68QU=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Level = _t, Sort = _t, segment_id = _t, Name = _t, #"type" = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Level", type text}, {"Sort", Int64.Type}, {"segment_id", Int64.Type}, {"Name", type text}, {"type", type text}})
in
    #"Geänderter Typ"
```


## Table: peakon_driver_displayNames


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("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", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [driver_id = _t, #"Short name" = _t, Description = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"driver_id", type text}, {"Short name", type text}, {"Description", type text}}),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Geänderter Typ",{{"Short name", "Driver"}})
in
    #"Umbenannte Spalten"
```

