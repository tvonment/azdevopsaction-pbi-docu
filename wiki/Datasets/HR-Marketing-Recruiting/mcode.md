



# M Code

|Dataset|[HR Marketing Recruiting](./../HR-Marketing-Recruiting.md)|
| :--- | :--- |
|Workspace|[Global Recruiting](../../Workspaces/Global-Recruiting.md)|

## Table: time recording


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    sec_imp_fc_project_time_recording = Source{[Schema="rep",Item="v_fc_hsm_time_recording"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(sec_imp_fc_project_time_recording,{{"calendar_day", "day_of_work"}, {"recorded_time", "actual_work"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each [day_of_work] >= #date(2021, 1, 1)),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"project_number"}, Projekte, {"Projektnummer"}, "Projekte", JoinKind.RightOuter),
    #"Filtered Rows1" = Table.SelectRows(#"Merged Queries", each ([project_number] <> null))
in
    #"Filtered Rows1"
```


## Table: employee


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    sec_imp_hr_employee = Source{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(sec_imp_hr_employee,{"emp_id", "last_name", "first_name", "jobcode", "work_location", "platform_1_name", "platform_DACH_name"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Other Columns",{{"platform_1_name", "Platform"}, {"platform_DACH_name", "Platform DACH"}}),
    #"Merged Columns" = Table.CombineColumns(#"Renamed Columns",{"last_name", "first_name"},Combiner.CombineTextByDelimiter(", ", QuoteStyle.None),"Employee")
in
    #"Merged Columns"
```


## Table: Projekte


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("jdPRTsIwFAbgV2l2BYEB2wC9R8KImRo2QgLZRVmO7GRbR7oOo1e+g4kv5Jv4JK7DqCidvfqbtvlydtaz2RhuHsVFFJdpRnkCAtnO6Bruwh5YMv8ckgVgAay/BhSkddU2wq7ScCynyiXDA/ACxSPxvpQZMOA0JX4UPwA+NStDlVJtkrWrh4xUiOvP9IRLlTAN9GqwR3WS9+eXunSPMrqDDJggk7TckrfXQgDngFHc7FzI9L0amuT5vmqlwJyR+eT2xtdnBgqmqu0+5xHoSV5wbTtHyTzbnt3nv9bWhk1asDRXCExfGzdpK4W2gIiX+GMaZK/mLM7LAkx52Ku7Ns32aY+0Ak4PkJIOCTCD9jnAsewqvzdP3suvu+PTm/+WJuU7ThOBSc/ksrb+cUg7ckirj/NQUL6Va26E4Qc=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Typ = _t, Projektnummer = _t, Projekt = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Typ", type text}, {"Projektnummer", type text}, {"Projekt", type text}})
in
    #"Changed Type"
```

