



# M Code

|Dataset|[Napta Report V1](./../Napta-Report-V1.md)|
| :--- | :--- |
|Workspace|[Napta [Prod]](../../Workspaces/Napta-[Prod].md)|

## Table: v_napta_employee_unique


```m
let
    Quelle = Sql.Databases("muc-mssql-2"),
    datahub = Quelle{[Name="datahub"]}[Data],
    rep_v_napta_employee = datahub{[Schema="rep",Item="v_napta_employee"]}[Data],
    #"Sortierte Zeilen" = Table.Sort(rep_v_napta_employee,{{"last_hire_date", Order.Ascending}}),
    #"Entfernte Duplikate" = Table.Distinct(#"Sortierte Zeilen", {"emp_id"}),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Entfernte Duplikate",{{"full_name_display", "full_name"}}),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Umbenannte Spalten", {"cost_center_id"}, v_napta_permission_bu_cc_filter, {"key_id"}, "v_napta_permission_business_units", JoinKind.LeftOuter),
    #"Expanded v_napta_permission_business_units" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "v_napta_permission_business_units", {"business_unit"}, {"business_unit"}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Expanded v_napta_permission_business_units", each ([business_unit] <> null))
in
    #"Gefilterte Zeilen"
```


## Table: v_napta_employee_target_hours_week


```m
let
    Quelle = Sql.Databases("muc-mssql-2"),
    datahub = Quelle{[Name="datahub"]}[Data],
    rep_v_napta_employee_target_hours = datahub{[Schema="rep",Item="v_napta_employee_target_hours"]}[Data],
    #"Inserted Year" = Table.AddColumn(rep_v_napta_employee_target_hours, "Year", each Date.Year([calendar_day]), Int64.Type),
    #"Changed Type2" = Table.TransformColumnTypes(#"Inserted Year",{{"Year", type text}}),
    #"Inserted Week of Year1" = Table.AddColumn(#"Changed Type2", "Week of Year", each Date.WeekOfYear([calendar_day]), Int64.Type),
    #"Changed Type3" = Table.TransformColumnTypes(#"Inserted Week of Year1",{{"Week of Year", type text}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type3", "Week", each if Text.Length([Week of Year]) = 1 then "0" & [Week of Year] else [Week of Year]),
    #"Changed Type4" = Table.TransformColumnTypes(#"Added Custom1",{{"Week", type text}}),
    #"Removed Columns2" = Table.RemoveColumns(#"Changed Type4",{"Week of Year"}),
    #"Added Custom2" = Table.AddColumn(#"Removed Columns2", "staffing_week", each [Year] & "-W" & [Week]),
    #"Changed Type5" = Table.TransformColumnTypes(#"Added Custom2",{{"staffing_week", type text}}),
    #"Removed Columns3" = Table.RemoveColumns(#"Changed Type5",{"Year", "Week"}),
    #"Grouped Rows" = Table.Group(#"Removed Columns3", {"emp_id", "staffing_week"}, {{"target_hours_week", each List.Sum([target_hours]), type nullable number}}),
    #"Added Custom" = Table.AddColumn(#"Grouped Rows", "emp_id_week", each [emp_id] & " " & [staffing_week]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{{"emp_id_week", type text}})
in
    #"Changed Type1"
```


## Table: pub dim_date


```m
let
    Quelle = Sql.Databases("muc-mssql-2"),
    datahub = Quelle{[Name="datahub"]}[Data],
    pub_dim_date = datahub{[Schema="pub",Item="dim_date"]}[Data],
    #"Andere entfernte Spalten" = Table.SelectColumns(pub_dim_date,{"DateKey", "Date", "Day", "WeekDayName", "WeekOfYear", "Year"}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Andere entfernte Spalten",{{"WeekOfYear", type text}}),
    #"Added Custom1" = Table.AddColumn(#"Geänderter Typ", "WeekNr", each if Text.Length([WeekOfYear]) = 1 then "0" & [WeekOfYear] else [WeekOfYear]),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Added Custom1",{{"WeekNr", type text}, {"Year", type text}}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Geänderter Typ1", "Week", each [Year] & "-W" & [WeekNr]),
    #"Geänderter Typ2" = Table.TransformColumnTypes(#"Hinzugefügte benutzerdefinierte Spalte",{{"Week", type text}}),
    #"Entfernte Spalten" = Table.RemoveColumns(#"Geänderter Typ2",{"WeekNr"}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Entfernte Spalten", each Date.IsInPreviousNWeeks([Date], 12) or Date.IsInCurrentWeek([Date]) or Date.IsInNextNWeeks([Date], 8)),
    #"Removed Bottom Rows" = Table.RemoveLastN(#"Gefilterte Zeilen",1),
    #"Hinzugefügte benutzerdefinierte Spalte1" = Table.AddColumn(#"Removed Bottom Rows", "WeekSelection", each if Date.IsInCurrentWeek([Date]) then "Current week" else [Week], type text)
in
    #"Hinzugefügte benutzerdefinierte Spalte1"
```


## Table: v_napta_permission


```m
let
    Quelle = Sql.Databases("muc-mssql-2"),
    datahub = Quelle{[Name="datahub"]}[Data],
    rep_v_napta_permission = datahub{[Schema="rep",Item="v_napta_permission"]}[Data]
in
    rep_v_napta_permission
```


## Table: pub dim_date_relative_weeks


```m
let
    Quelle = Sql.Databases("muc-mssql-2"),
    datahub = Quelle{[Name="datahub"]}[Data],
    pub_dim_date = datahub{[Schema="pub",Item="dim_date"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_dim_date, each Date.IsInPreviousNWeeks([Date], 12) or Date.IsInCurrentWeek([Date]) or Date.IsInNextNWeeks([Date], 8)),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each ([WeekDayName] = "Wednesday")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows1",{"DateKey", "Date"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "Week+0", each Date.AddWeeks([Date], 0), type date),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Week+1", each Date.AddWeeks([Date], 1), type date),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "Week+2", each Date.AddWeeks([Date], 2), type date),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "Week+3", each Date.AddWeeks([Date], 3), type date),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "Week+4", each Date.AddWeeks([Date], 4), type date),
    #"Added Custom5" = Table.AddColumn(#"Added Custom4", "Week+5", each Date.AddWeeks([Date], 5), type date),
    #"Inserted Year" = Table.AddColumn(#"Added Custom5", "Year", each Date.Year([Date])),
    #"Inserted Week of Year" = Table.AddColumn(#"Inserted Year", "Week of Year", each Date.WeekOfYear([Date])),
    #"Added Custom6" = Table.AddColumn(#"Inserted Week of Year", "Week", each Text.Combine({Text.PadEnd(Text.From([Year], "de-DE"), 5, "-"), "W", Text.PadStart(Text.From([Week of Year], "de-DE"), 2, "0")}), type text),
    #"Added Custom7" = Table.AddColumn(#"Added Custom6", "WeekSelection", each if Date.IsInCurrentWeek(Date.AddWeeks([Date],2)) then "Current week -2" else [Week], type text),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom7",{"Date", "Year", "Week of Year", "Week"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Columns",{"WeekSelection", "Week+0", "Week+1", "Week+2", "Week+3", "Week+4", "Week+5"}),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Reordered Columns", {"DateKey", "WeekSelection"}, "Attribute", "Value"),
    #"Removed Columns1" = Table.RemoveColumns(#"Unpivoted Other Columns",{"Attribute"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns1",{{"Value", "RelatedDates"}})
in
    #"Renamed Columns"
```


## Table: v_napta_staffing_days_per_week


```m
let
    Source = Table.Combine({v_napta_staffing_days_per_week_original, v_napta_staffing_days_per_week_free_all}),
    #"Replaced Value1" = Table.ReplaceValue(Source,"Free","Acquisition, free and internal activity",Replacer.ReplaceText,{"staffing_category"}),
    #"Replaced Value" = Table.ReplaceValue(#"Replaced Value1","Acquisition or internal activity","Acquisition, free and internal activity",Replacer.ReplaceText,{"staffing_category"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value","Day off - part-time block model","Sickness and leave",Replacer.ReplaceText,{"staffing_category"})
in
    #"Replaced Value2"
```


## Table: v_napta_employee_unique_bu_filter


```m
let
    Source = v_napta_employee_unique,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"email", "business_unit"})
in
    #"Removed Other Columns"
```


## Table: v_napta_permission_bu_cc_filter


```m
let
    Quelle = Sql.Databases("muc-mssql-2"),
    datahub = Quelle{[Name="datahub"]}[Data],
    rep_v_napta_permission = datahub{[Schema="rep",Item="v_napta_permission"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(rep_v_napta_permission, each ([type] = "BU") and ([key_field] = "cost_center_id")),
    #"Removed Columns" = Table.RemoveColumns(#"Gefilterte Zeilen",{"type", "key_field"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"key_description", "business_unit"}})
in
    #"Renamed Columns"
```


## Table: v_napta_user_groups


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_napta_user_groups = datahub{[Schema="rep",Item="v_napta_user_groups"]}[Data]
in
    rep_v_napta_user_groups
```


## Roles

### Admin


Model Permission: Read
### Business Unit


Model Permission: Read

v_napta_user_groups

```m
[email] = userprincipalname()
```


### France


Model Permission: Read

v_napta_employee_unique

```m
[business_unit] = "France"
```


### Middle East


Model Permission: Read

v_napta_employee_unique

```m
[business_unit] = "Middle East"
```


### Digital DACH


Model Permission: Read

v_napta_employee_unique

```m
[business_unit] = "Digital DACH"
```

