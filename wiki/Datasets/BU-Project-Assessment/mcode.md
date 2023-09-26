



# M Code

|Dataset|[BU Project Assessment](./../BU-Project-Assessment.md)|
| :--- | :--- |
|Workspace|[BU Project Assessment [Dev]](../../Workspaces/BU-Project-Assessment-[Dev].md)|

## Table: rep v_hr_employee


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Source{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Lowercased Text" = Table.TransformColumns(rep_v_hr_employee,{{"email", Text.Lower, type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Lowercased Text", each ([emp_status] = "A") and ([email] <> null) and [email]<> "no_mail@rolandberger.com" and [email] <> "nomail@rolandberger.com"  ),
    #"Lowercased Text1" = Table.TransformColumns(#"Filtered Rows",{{"email", Text.Lower, type text}}),
    #"Removed Duplicates" = Table.Distinct(#"Lowercased Text1", {"email"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"mentor_emp_id"}, #"Removed Duplicates", {"emp_id"}, "Removed Duplicates", JoinKind.LeftOuter),
    #"Expanded Removed Duplicates" = Table.ExpandTableColumn(#"Merged Queries", "Removed Duplicates", {"email"}, {"mentor_email"}),
    #"Lowercased Text2" = Table.TransformColumns(#"Expanded Removed Duplicates",{{"email", Text.Lower, type text}}),
    #"Merged Queries1" = Table.NestedJoin(#"Lowercased Text2", {"emp_id"}, v_hr_mentor_to_practice_group, {"emp_id"}, "v_hr_mentor_to_practice_group", JoinKind.LeftOuter),
    #"Expanded rls clientteam" = Table.ExpandTableColumn(#"Merged Queries1", "v_hr_mentor_to_practice_group", {"practice_group"}, {"conf_practice_group"}),
    #"Added Custom" = Table.AddColumn(#"Expanded rls clientteam", "practice_group", each if [conf_practice_group] = null and ([country_code] = "DEU" or [country_code] = "AUT" or [country_code] = "CHE") then [cost_center] else [conf_practice_group], type text),
    #"Replaced Value" = Table.ReplaceValue(#"Added Custom",each [full_name],each [full_name_display],Replacer.ReplaceText,{"full_name"})
in
    #"Replaced Value"
```


## Table: _Measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: Bottom Up


```m
let
    Source = BottomUp,
    #"Added Index" = Table.AddIndexColumn(Source, "Index", 0, 1, Int64.Type),
    #"Merged Queries" = Table.NestedJoin(#"Added Index", {"ID_ASSESSEE"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.Inner)
in
    #"Merged Queries"
```


## Table: Bottom Up Questions


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("hVdrb9tGEPwrBxcFbEBK7TzdflNkOUkjRYKsNgXiwDiRS+nq4x3LO0pWfn1nl6RMP2IDfsjkPWZ2Z2fX374dzEr/LyVRBYr9qjjoHczm0z9Hw8XVxWg8xp8XZG1QcU2qaFZuTVyrxJIuVUh8YdxKaZeqlKzZUKmXlni9jkpb67eytXm3Uz57eBQ/cJRQCBorSgq+KvEX7j7pfDMOXHXwvfcU5sXg/JwXR51lj6DmB0sKUUXSuYq+BfZwpXZKJwkVkfmorS+vrdcpjn7ZxcTXPAtqOJ1M8OeQI2Z3KvF5XjmT6Eh3EXIwqYf3Likp0p2A9iTEfusU3RRYrKPxLigEuaa0Ms5xIu7F9/Dy4Nok132fZZcHRwDxqoN+uAeCs56J61+z2WzBjKui8GWsgc8mgopj2eMrNyYFpVAhJokhF9WqMql2CanMl2q9Kzx2BRNkF2hGXpPShqwvcnyuSe4P4viHwFkCTQQPaTs9/hUUsz7O6Yc12UzCUUYTCOBed1NTA1WHzT1HzxAcTmejwdl9hiITQWuFkIEq0jWVHGrg4iV6VRKld5MomDfepKpyt8rmcyq3rNIVspuKpnDfm8dAyyk15K+30vs6nX8eTwdnV7Px4AuDtxoa2MsWCwWg2updpwA7TO4JvjSrNXMK/BsS264NtC7AmeDz2N926qENbQFQrq2Jx8APhsORaGnkQlXeqwGIo0HIt6AQmdCjpSiaupMjLIVDUF2/1ifaKsoL63d5q0Xi92ws7zrAzxpv+ing+ejD8ONnPJnTqrJ1Da8puQ7Kuz2Cy+r4+OW7cAtPKkNfg1/iK0iwzKFg4btdk4PhUQqKh/Ri9aIH0ytK40sTzQ8sKDTr724pozbSNPAPw+UKbnuj5Lo+7RBqOdQon6A1XHyajIRXYE8JODLxYtPR5E0c96V3cqzWuE9wpWxEsubQeYVAW6gnZ6msAB95oX6ujQ1HHKEt0XWqd2xh4A4Xr3/TNbkUDzc6ac2Mi79aWpPgJmt4Dy+FXxYWqkPYM5Sa3AvQv3cYz7u494RFA+JtLevh1WI++Hs0li1plbD4Sg3/kYLlJtTqPTfO5JVUTI6Ar2DWav6+TXKiyyWYZd5H5M1FhnHccddFfWjJd+zN9WeQ5qPJdDGqKyj33BQySzem1TpXYu4h3aCWu9ptxOgdjufldd1DUyW04kPgjQzjpIPnXA401sTdk1DOx6N/Pr0fjzrFuceiy9JsILu61bNE8V4CLhYNmUYuYM6DE18JlkiGg1o2ovpuqZf0X2X4Cu/6wUR+QYHQLRj0y4fRlKsE/twDj8SEEzkdI4Bno/HV+wFscSjgb7jwTWaoLsg+PqNLaivNqKk5jmbHyxsfl+7CN/VgJpt2trnt2RJ7qP/xHB3JapAAZamFO9ZbN4ygRb8nrzod64P32HajWelPUewkaN+nHiBBprRbEbteuNtRvWwBkbgT++Rq7C9FTxpC3UDpWNXEh1OMPl7UnGGutfzfouoRJIkbghT4xJ5ak7Zx3VOZzo1t/INi8uJIMcPXHaoN7qdYclPmoelT3SWANGlCWQVqffFy33F4jjFR6F4eqLSqM9pRGseg3Ht35uuuWBWtf0N3lUWs9iNiPdj8hgi1R3AOmcCbDpNH7n+K1eDs42jOmRuw6pqq4WYJ1eVEEuUAy04rHqAZs3Ti0L5sxiY2W6UzNBR1qooc2brh3ohC/gNJwmOnmwaBIUcOrfuhLlcYKQ1njosscEYlTT+8Y7WLHtYmWdd6zSlfEso2r+D9SxIXJhd0bPpyvRdC4O5z8rYTlknD5dl6xcTFU8ywJBmFuc3H3IdCrEzml8yHyCAwDDlgD0kFf2tbRWgLQKuMuLPX02/JgOtxILFVQGsHPfln4l0H5GB/kyBsRImYXiS+5PLkiXc6X4zmPBpK2njnaTOw3eqY5J+g5pgvFQeNYegQcGutCfjvdD65qLf1T9of+PpFdk15yLccm9tP+DpuvjvPv3//Hw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Group = _t, Question = _t, #"Question Text" = _t, Sort = _t, GroupSort = _t, InOverall = _t, QuestionShort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Group", type text}, {"Question", type text}, {"Question Text", type text}, {"Sort", Int64.Type}, {"GroupSort", Int64.Type}, {"InOverall", Int64.Type}})
in
    #"Changed Type"
```


## Table: Bottom Up Results


```m
let
    Source = #"Bottom Up",
    #"Removed Columns" = Table.RemoveColumns(Source,{"ASSESSEE_FIRST_NAME", "ASSESSEE_LAST_NAME", "CNT_DETRACTORS", "CNT_PASSIVES", "CNT_PROMOTORS"}),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"ID_ASSESSEE", "Index"}, "Attribute", "Value"),
    #"Duplicated Column" = Table.DuplicateColumn(#"Unpivoted Other Columns", "Attribute", "Attribute - Copy"),
    #"Renamed Columns" = Table.RenameColumns(#"Duplicated Column",{{"Attribute - Copy", "Question"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","SUM_","",Replacer.ReplaceText,{"Question"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","CNT_","",Replacer.ReplaceText,{"Question"}),
    #"Inserted Text Before Delimiter" = Table.AddColumn(#"Replaced Value1", "Text Before Delimiter", each Text.BeforeDelimiter([Attribute], "_"), type text),
    #"Renamed Columns1" = Table.RenameColumns(#"Inserted Text Before Delimiter",{{"Text Before Delimiter", "Aggregarion"}}),
    #"Pivoted Column" = Table.Pivot(#"Renamed Columns1", List.Distinct(#"Renamed Columns1"[Aggregarion]), "Aggregarion", "Value"),
    #"Grouped Rows" = Table.Group(#"Pivoted Column", {"Index", "ID_ASSESSEE", "Question"}, {{"Count", each List.Max([CNT]), type nullable number}, {"Sum", each List.Max([SUM]), type nullable number}}),
    #"Renamed Columns2" = Table.RenameColumns(#"Grouped Rows",{{"Count", "Column Count"}, {"Sum", "Column Sum"}})
in
    #"Renamed Columns2"
```


## Table: RefreshDate


```m
let
    Source = Date.From(DateTime.LocalNow()),
    #"Converted to Table" = #table(1, {{Source}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Converted to Table",{{"Column1", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "RefreshDate"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "BU End Month", each Date.AddMonths([RefreshDate], -1), Date.Type),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "BU Start Month", each Date.AddMonths([RefreshDate], -6), Date.Type)
in
    #"Added Custom1"
```


## Table: rep v_pc_region


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_pc_region = Source{[Schema="rep",Item="v_pc_region"]}[Data]
in
    rep_v_pc_region
```


## Table: rls country


```m
let
    Source = #"rep v_bottom_up_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "country")),
    #"Lowercased Text" = Table.TransformColumns(#"Filtered Rows1",{{"email", Text.Lower, type text}})
in
    #"Lowercased Text"
```


## Table: rls platform


```m
let
    Source = #"rep v_bottom_up_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "platform")),
    #"Lowercased Text" = Table.TransformColumns(#"Filtered Rows1",{{"email", Text.Lower, type text}})
in
    #"Lowercased Text"
```


## Table: rls clientteam


```m
let
    Source = #"rep v_bottom_up_dashboard_permission",
    #"Lowercased Text" = Table.TransformColumns(Source,{{"email", Text.Lower, type text}})
in
    #"Lowercased Text"
```


## Table: rls platform DACH


```m
let
    Source = #"rep v_bottom_up_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "platformDACH")),
    #"Lowercased Text" = Table.TransformColumns(#"Filtered Rows1",{{"email", Text.Lower, type text}})
in
    #"Lowercased Text"
```


## Table: rls countryOnly


```m
let
    Source = #"rep v_bottom_up_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "countryOnly")),
    #"Lowercased Text" = Table.TransformColumns(#"Filtered Rows1",{{"email", Text.Lower, type text}})
in
    #"Lowercased Text"
```

