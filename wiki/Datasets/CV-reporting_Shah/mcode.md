



# M Code

|Dataset|[CV reporting_Shah](./../CV-reporting_Shah.md)|
| :--- | :--- |
|Workspace|[Intranet usage](../../Workspaces/Intranet-usage.md)|

## Table: CV LCM


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/CVs/", [Implementation="2.0", ViewMode="All"]),
    #"e5b90f8e-49b6-4130-ac4e-5e2ecf630ce8" = Source{[Id="e5b90f8e-49b6-4130-ac4e-5e2ecf630ce8"]}[Items],
    #"Filtered Rows" = Table.SelectRows(#"e5b90f8e-49b6-4130-ac4e-5e2ecf630ce8", each true),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Flow", "Content Type", "Created By", "Modified By", "Version", "Attachments", "Edit", "Type", "Item Child Count", "Folder Child Count", "Label setting", "Retention label", "Retention label Applied", "Label applied by", "App Created By", "App Modified By", "Compliance Asset Id", "Color Tag", "Item is a Record"}),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Removed Columns", "Department", Splitter.SplitTextByDelimiter("/", QuoteStyle.Csv), {"Department.1", "Department.2"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Department.1", type text}, {"Department.2", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Department.1", "Platform"}}),
    #"Trimmed Text" = Table.TransformColumns(#"Renamed Columns",{{"Platform", Text.Trim, type text}, {"Department.2", Text.Trim, type text}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Trimmed Text",{{"Platform", "Platform (primary)"}, {"Department.2", "Platform (secondary)"}}),
    #"Merged Queries" = Table.NestedJoin(#"Renamed Columns1", {"RB Office"}, #"RB countries and regions", {"RB Office"}, "RB countries and regions", JoinKind.LeftOuter),
    #"Expanded RB countries and regions" = Table.ExpandTableColumn(#"Merged Queries", "RB countries and regions", {"RB Regions", "Regions"}, {"RB countries and regions.RB Regions", "RB countries and regions.Regions"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Expanded RB countries and regions",{{"RB countries and regions.RB Regions", "RB country"}, {"RB countries and regions.Regions", "RB regions"}}),
    #"Added CV availability" = Table.AddColumn(#"Renamed Columns2", "CV availability", each if [CVs Count] = "0" then 0 else 1)
in
    #"Added CV availability"
```


## Table: RB countries and regions


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("dVTLctswDPwVjc/5CT+SOLGVcSO3M20mB1iERVQU4aHIusrXF6Rkp7HlG4kFAXCBxdvb5AehtTC5m0xD6x3F02I6X07e794mOVhoomUG2gFZOeWklMHsHlqfXGZILngB1rgDy2MuC9Yxxjfw4EbgV+pAaQFWZCvFTcb7rICgKJs62KWCriKGHZDYv1vyqJJfdt+QA4/tWI0utC2aCM3QVBQaOSWkAM42EAxHyMEHmUhEg45KaHsK2HqHEO1zYUPBpcOWnbjwTXwDjmLmBwe2xFPiGTqT+HxE14Dt/md9ETCWq9jtxx1iqHofnB+Hl9DsgqvGwTxYKvU4VvjgfQW34kqrf0uLIiiMeHTZXFManT4t2ypb8W2HQoOtdGrcKL4FOuBN9DHI6w/N4ZbDLCg4YBuLXwYr3+hOSB6afl6erErzVNxPE/CCx2yBRo9hm2BxxPwMtRAEPcIW2y9oTgZiV588mHP6V27w0rbluosz8wyH9CAZVwEMZOvQHEISity6i/j4l0rO5uRjpP52OXBzaGEnZZRJOTKdZfJJ2E/hsNdoB7ZJcjyFnjatUKogauMFvZYBBava08s1tbv0csPOhyoJYqC91OB63uWnYOnckZzbko/RLvojsNkDKhSREp+/XMhAwYFdJOjLeahqBq5Ew6nLxaFfQcNqUo7UpfWRpXA7TH9xlHSfmTyXtWbTXCG/guslURzJf/T//jL3QlrNtZi2Mr0Deipw1dGfuInquB/P8l5zHI7PDTWstjNn3PoeLqZX7dNyrHgcXKB3TH4cXHIURJaT1acJkeXuLXyuO+QQG1dw8Fq0KjI6l2SYmz3J2smWZNKu7FMMexLc1U6ZvL//Aw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"RB Office" = _t, #"RB Regions" = _t, Regions = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"RB Office", type text}, {"RB Regions", type text}, {"Regions", type text}})
in
    #"Changed Type"
```


## Table: Employees by Platform


```m
let
    Source = #"CV LCM",
    #"Grouped Rows" = Table.Group(Source, {"Platform (primary)"}, {{"Employees by platform", each Table.RowCount(_), Int64.Type}}),
    #"Sorted Rows" = Table.Sort(#"Grouped Rows",{{"Employees by platform", Order.Descending}})
in
    #"Sorted Rows"
```


## Table: Employees by country


```m
let
    Source = #"CV LCM",
    #"Grouped Rows" = Table.Group(Source, {"RB country"}, {{"Employees (country)", each Table.RowCount(_), Int64.Type}})
in
    #"Grouped Rows"
```

