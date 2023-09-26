



# M Code

|Dataset|[1.0.0_performance_summary](./../1.0.0_performance_summary.md)|
| :--- | :--- |
|Workspace|[MSR Navigation](../../Workspaces/MSR-Navigation.md)|

## Table: msr v_byd_daily_rates


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    msr_v_byd_daily_rates = datahub{[Schema="msr",Item="v_byd_daily_rates"]}[Data]
in
    msr_v_byd_daily_rates
```


## Table: msr v_employee_utilization


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    msr_v_employee_utilization = datahub{[Schema="msr",Item="v_employee_utilization"]}[Data],
    #"Filtered Rows" = Table.SelectRows(msr_v_employee_utilization, each Date.IsInCurrentYear([calendar_day])),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"calendar_day", "emp_id"}, #"msr v_hr_employee_job_matrix", {"key_date", "emp_id"}, "msr v_hr_employee_job_matrix", JoinKind.LeftOuter),
    #"Expanded msr v_hr_employee_job_matrix" = Table.ExpandTableColumn(#"Merged Queries", "msr v_hr_employee_job_matrix", {"toe_description", "cost_center_id", "company_id_byd", "office", "platform_1_id", "country_code_iso3", "job.Im Scope", "job.Bezeichnung", "job.Kurz-Bezeichnung", "job.JobGroup"}, {"toe_description", "cost_center_id", "company_id_byd", "office", "platform_1_id", "country_code_iso3", "job.Im Scope", "job.Bezeichnung", "job.Kurz-Bezeichnung", "job.JobGroup"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded msr v_hr_employee_job_matrix", each ([job.Im Scope] = "x"))
in
    #"Filtered Rows1"
```


## Table: msr v_hr_employee_job_matrix


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    msr_v_hr_employee_job_matrix = datahub{[Schema="msr",Item="v_hr_employee_job_matrix"]}[Data],
    #"Filtered Rows" = Table.SelectRows(msr_v_hr_employee_job_matrix, each Date.IsInCurrentYear([key_date])),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"job_code"}, Jobcodes, {"Jobcode"}, "Jobcodes", JoinKind.LeftOuter),
    #"Expanded Jobcodes" = Table.ExpandTableColumn(#"Merged Queries", "Jobcodes", {"Im Scope", "Bezeichnung", "Kurz-Bezeichnung", "JobGroup"}, {"job.Im Scope", "job.Bezeichnung", "job.Kurz-Bezeichnung", "job.JobGroup"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded Jobcodes", each ([job.Im Scope] = "x"))
in
    #"Filtered Rows1"
```


## Table: rep v_hr_employee


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_hr_employee = datahub{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_hr_employee, each [ter_max_date] > #date(2022, 12, 31))
in
    #"Filtered Rows"
```


## Table: pub dim_date


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    pub_dim_date = datahub{[Schema="pub",Item="dim_date"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_dim_date, each Date.IsInCurrentYear([Date])),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"DateKey", "Date", "Day", "Weekday", "WeekDayName", "WeekOfYear", "Month", "MonthName", "Year", "YearMonthnumber", "FirstDayOfMonth", "YearMonthShort", "ISOWeekOfYearNameInCal"})
in
    #"Removed Other Columns"
```

