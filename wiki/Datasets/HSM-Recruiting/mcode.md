



# M Code

|Dataset|[HSM Recruiting](./../HSM-Recruiting.md)|
| :--- | :--- |
|Workspace|[Global Recruiting](../../Workspaces/Global-Recruiting.md)|

## Table: CurrentYear


```m
let
    Source = 2021 //Date.Year (RefreshDate)

in
    Source
```


## Table: CurrentMonth


```m
let
    Source = 7 // Date.Month (RefreshDate)

in
    Source
```


## Table: dim region country


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_diversity_ll_region_country = Source{[Schema="rep",Item="v_diversity_ll_region_country"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(rep_v_diversity_ll_region_country,{{"country_company", "country"}})
in
    #"Renamed Columns"
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
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "SmartRecruiters"),
    dbo_v_rep_data_diverstiy = Source{[Schema="dbo",Item="v_rep_data_diverstiy"]}[Data],
    #"Merged Queries" = Table.NestedJoin(dbo_v_rep_data_diverstiy, {"HR country (access rights)"}, ll_country_region, {"HR_Country"}, "ll_country_region", JoinKind.LeftOuter),
    #"Expanded ll_country_region" = Table.ExpandTableColumn(#"Merged Queries", "ll_country_region", {"Country_Code"}, {"Country_Code"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded ll_country_region",{{"Application Creation Date", type date}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each [Application Creation Date] >= #date(2020, 9, 1))
in
    #"Filtered Rows"
```


## Table: ll_funnel_status


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "SmartRecruiters"),
    dbo_ll_funnel_status = Source{[Schema="dbo",Item="ll_funnel_status"]}[Data]
in
    dbo_ll_funnel_status
```


## Table: ll_target_university


```m
let
    Source = Sql.Databases("muc-mssql-2.rolandberger.net"),
    SmartRecruiters = Source{[Name="SmartRecruiters"]}[Data],
    dbo_ll_target_university = SmartRecruiters{[Schema="dbo",Item="ll_target_university"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_ll_target_university, each ([Target_Uni_Focus] = "DACH"))
in
    #"Filtered Rows"
```


## Table: ll_ats_status


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "smartrecruiters"),
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


## Table: v_rep_education


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "SmartRecruiters"),
    dbo_v_rep_education = Source{[Schema="dbo",Item="v_rep_education"]}[Data]
in
    dbo_v_rep_education
```

