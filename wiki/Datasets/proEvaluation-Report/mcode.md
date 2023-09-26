



# M Code

|Dataset|[proEvaluation Report](./../proEvaluation-Report.md)|
| :--- | :--- |
|Workspace|[proEvaluation [Prod]](../../Workspaces/proEvaluation-[Prod].md)|

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
    #"Merged Queries" = Table.NestedJoin(#"Expanded v_napta_permission_business_units", {"emp_id"}, #"adm permission_proevaluation_emp_join", {"emp_id"}, "adm permission_proevaluation_emp_join", JoinKind.LeftOuter),
    #"Expanded adm permission_proevaluation_emp_join" = Table.ExpandTableColumn(#"Merged Queries", "adm permission_proevaluation_emp_join", {"region"}, {"region_rls"})
in
    #"Expanded adm permission_proevaluation_emp_join"
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
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Geänderter Typ1", "Week", each [Year] & "-W" & [WeekNr], type text),
    #"Removed Columns" = Table.RemoveColumns(#"Hinzugefügte benutzerdefinierte Spalte",{"WeekNr"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each Date.IsInPreviousYear([Date]) or Date.IsInCurrentYear([Date])),
    #"Hinzugefügte benutzerdefinierte Spalte1" = Table.AddColumn(#"Filtered Rows", "WeekSelection", each if Date.IsInCurrentWeek([Date]) then "Current week" else [Week], type text)
in
    #"Hinzugefügte benutzerdefinierte Spalte1"
```


## Table: v_napta_staffing_project_days_per_week


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_napta_staffing_project_days_per_week = datahub{[Schema="rep",Item="v_napta_staffing_project_days_per_week"]}[Data],
    #"Added Custom" = Table.AddColumn(rep_v_napta_staffing_project_days_per_week, "prolongation_expected", each "No", type text),
    #"Inserted Merged Column" = Table.AddColumn(#"Added Custom", "emp_project_key", each Text.Combine({[EmployeeID], " - ", [project_number]}), type text),
    #"Merged Queries" = Table.NestedJoin(#"Inserted Merged Column", {"EmployeeID", "project_number"}, v_napta_staffing_per_period, {"emp_id", "project_number"}, "v_napta_staffing_per_period", JoinKind.LeftOuter),
    #"Expanded v_napta_staffing_per_period" = Table.ExpandTableColumn(#"Merged Queries", "v_napta_staffing_per_period", {"min_staffing_start_date", "max_staffing_end_date"}, {"min_staffing_start_date", "max_staffing_end_date"})
in
    #"Expanded v_napta_staffing_per_period"
```


## Table: rep v_napta_staffing_project_days_per_week


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_napta_staffing_project_days_per_week = datahub{[Schema="rep",Item="v_napta_staffing_project_days_per_week"]}[Data]
in
    rep_v_napta_staffing_project_days_per_week
```


## Table: pub dim_date_assignments


```m
let
    Quelle = #"pub dim_date",
    #"Andere entfernte Spalten" = Table.SelectColumns(Quelle,{"Date"})
in
    #"Andere entfernte Spalten"
```


## Table: v_napta_staffing_per_period


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_napta_staffing_per_period = datahub{[Schema="rep",Item="v_napta_staffing_per_period"]}[Data],
    #"Inserted Merged Column" = Table.AddColumn(rep_v_napta_staffing_per_period, "emp_project_key", each Text.Combine({[emp_id], " - ", [project_number]}), type text),
    #"Grouped Rows" = Table.Group(#"Inserted Merged Column", {"emp_id", "emp_name", "project_number", "project_name", "project_client", "staffing_period_status", "emp_id_dm", "emp_id_pm", "staffing_type", "emp_project_key"}, {{"days_assigned", each List.Sum([days_assigned]), type nullable number}, {"min_staffing_start_date", each List.Min([min_staffing_start_date]), type date}, {"max_staffing_end_date", each List.Max([max_staffing_end_date]), type date}}),
    #"Filtered Rows" = Table.SelectRows(#"Grouped Rows", each ([staffing_type] = "real"))
in
    #"Filtered Rows"
```


## Table: adm permission_proevaluation


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    adm_permission_proevaluation = datahub{[Schema="adm",Item="permission_proevaluation"]}[Data],
    #"Filtered Rows" = Table.SelectRows(adm_permission_proevaluation, each [id_role_category] = 3 or [id_role_category] = 4)
in
    #"Filtered Rows"
```


## Roles

### proEvaluation Regions


Model Permission: Read

adm permission_proevaluation

```m
[email] = username()
```


### Admin


Model Permission: Read