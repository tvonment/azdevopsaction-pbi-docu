



# M Code

|Dataset|[Personal Assistant Statistics](./../Personal-Assistant-Statistics.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: Assistants


```m
let
    Source = AllData,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"Secretary ID", "Secretary Last Name", "Secretary First Name"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([Secretary ID] <> null)),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows", {"Secretary ID"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"Secretary ID"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee" = Table.ExpandTableColumn(#"Merged Queries", "rep v_hr_employee", {"work_location", "cost_center_id"}, {"work_location", "cost_center_id"}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded rep v_hr_employee", {"Secretary ID"}, #"rep v_employee_target_hours_adjusted_per_month", {"emp_id"}, "rep v_employee_target_hours_adjusted_per_month", JoinKind.LeftOuter),
    #"Expanded rep v_employee_target_hours_adjusted_per_month" = Table.ExpandTableColumn(#"Merged Queries1", "rep v_employee_target_hours_adjusted_per_month", {"target_hours", "absence_hrs", "target_hours_adj", "target_hours_fte"}, {"target_hours", "absence_hrs", "target_hours_adj", "target_hours_fte"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded rep v_employee_target_hours_adjusted_per_month", each true),
    #"Added Custom" = Table.AddColumn(#"Filtered Rows1", "Secretary FTE", each [target_hours_adj] / [target_hours_fte], type number),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"target_hours", "absence_hrs", "target_hours_adj", "target_hours_fte"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"work_location", "Secretary Location"}})
in
    #"Renamed Columns"
```


## Table: AllData


```m
let
    Source = ParPri,
    #"Replaced Value" = Table.ReplaceValue(Source,null, each [Platform] ,Replacer.ReplaceValue,{"platform_DACH_name"})
in
    #"Replaced Value"
```


## Table: ParPri wo Assistant


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Source{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_hr_employee, each  [jobcode] = "Partner 1" or [jobcode] = "Partner 2" or [jobcode] = "Partner 3" or [jobcode] = "Principal" ),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each ([emp_status] = "A") and ([pa_emp_id] = null or [pa_emp_id] = "")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows1",{"emp_id", "last_name", "first_name", "last_hire_date", "jobcode", "jobfunction", "work_location", "company", "cc_id", "cc_name", "mentor_last_name", "pa_emp_id", "pa_emp_last_name", "email", "country_code", "cost_center_id", "platform_1_id", "platform_1_name", "platform_2_id", "platform_2_name", "platform_DACH_name"}),
    #"Exception Replaced Platrorm" = Table.ReplaceValue(#"Removed Other Columns",null,each if [emp_id] = "M063539" or [emp_id]="M709142" or [emp_id]="M064421" then "Regulated" else null ,Replacer.ReplaceValue,{"platform_DACH_name"}),
    #"Renamed Columns" = Table.RenameColumns(#"Exception Replaced Platrorm",{{"platform_1_id", "Platform ID"}, {"platform_1_name", "Platform"}}),
    #"Merged Queries" = Table.NestedJoin(#"Renamed Columns", {"pa_emp_id"}, #"rep v_hr_employee", {"emp_id"}, "assistant", JoinKind.LeftOuter),
    #"Expanded assistant" = Table.ExpandTableColumn(#"Merged Queries", "assistant", {"emp_id", "last_name", "first_name", "full_name", "work_location", "country_code", "platform_DACH_id", "platform_DACH_name"}, {"assistant.emp_id", "assistant.last_name", "assistant.first_name", "assistant.full_name", "assistant.work_location", "assistant.country_code", "assistant.platform_DACH_id", "assistant.platform_DACH_name"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Expanded assistant",{{"assistant.work_location", "Secretary work location"}, {"assistant.full_name", "PA"}, {"assistant.first_name", "Secretary First Name"}, {"assistant.last_name", "Secretary Last Name"}, {"assistant.emp_id", "Secretary ID"}, {"emp_id", "ID"}, {"last_name", "Last"}, {"jobcode", "Function"}}),
    #"Filtered Rows2" = Table.SelectRows(#"Renamed Columns1", each ([country_code] = "AUT" or [country_code] = "CHE" or [country_code] = "DEU"))
in
    #"Filtered Rows2"
```

