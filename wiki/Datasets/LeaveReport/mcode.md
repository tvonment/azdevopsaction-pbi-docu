



# M Code

|Dataset|[LeaveReport](./../LeaveReport.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_employee


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Quelle{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Andere entfernte Spalten" = Table.SelectColumns(rep_v_hr_employee,{"emp_id", "last_name", "first_name", "full_name", "last_hire_date", "ter_max_date", "jobcode_id", "jobcode", "work_location", "company_id", "company", "country_code", "platform_1_id", "platform_1_name", "cost_center", "region","toe_id_ps","accounting_category"}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Andere entfernte Spalten", each [ter_max_date] >= #date(2019, 1, 1))
in
    #"Gefilterte Zeilen"
```


## Table: rep v_hr_employee_future


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_future = Quelle{[Schema="rep",Item="v_hr_employee_future"]}[Data],
    #"Andere entfernte Spalten" = Table.SelectColumns(rep_v_hr_employee_future,{"emp_id", "last_name", "first_name", "full_name", "last_hire_date", "ter_max_date", "jobcode_id", "jobcode", "work_location", "company_id", "company", "country_code", "platform_1_id", "platform_1_name", "cost_center", "region","toe_id_ps","accounting_category"})
in
    #"Andere entfernte Spalten"
```


## Table: rep v_hr_employee_toe_history


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_toe_history = Quelle{[Schema="rep",Item="v_hr_employee_toe_history"]}[Data],
    #"Entfernte Spalten" = Table.RemoveColumns(rep_v_hr_employee_toe_history,{"toe_id"}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Entfernte Spalten", each ([toe_category] = "leave")),
    #"Gefilterte Zeilen1" = Table.SelectRows(#"Gefilterte Zeilen", each [valid_from] < #date(2019, 1, 1) and [valid_to] >= #date(2019, 1, 1) or [valid_from] >= #date(2019, 1, 1)),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Gefilterte Zeilen1", {"emp_id"}, #"rep v_hr_employee_birthday", {"emp_id"}, "rep v_hr_employee_birthday", JoinKind.LeftOuter),
    #"Erweiterte rep v_hr_employee_birthday" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "rep v_hr_employee_birthday", {"birthdate"}, {"birthdate"})
in
    #"Erweiterte rep v_hr_employee_birthday"
```


## Table: employee_all


```m
let
    Quelle = Table.Combine({#"rep v_hr_employee", #"rep v_hr_employee_future"}),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(Quelle, {"emp_id"}, #"rep v_hr_employee_birthday", {"emp_id"}, "rep v_hr_employee_birthday", JoinKind.LeftOuter),
    #"Erweiterte rep v_hr_employee_birthday" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "rep v_hr_employee_birthday", {"birthdate"}, {"rep v_hr_employee_birthday.birthdate"}),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Erweiterte rep v_hr_employee_birthday",{{"rep v_hr_employee_birthday.birthdate", "birthdate"}})
in
    #"Umbenannte Spalten"
```


## Table: pub dim_date


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    pub_dim_date = Quelle{[Schema="pub",Item="dim_date"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(pub_dim_date, each [Date] >= #date(2019, 1, 1) and [Date] <= #date(2024, 12, 31))
in
    #"Gefilterte Zeilen"
```


## Table: rep v_hr_employee_birthday


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_birthday = Quelle{[Schema="rep",Item="v_hr_employee_birthday"]}[Data],
    #"Entfernte Spalten" = Table.RemoveColumns(rep_v_hr_employee_birthday,{"birthplace"})
in
    #"Entfernte Spalten"
```


## Table: rep v_hr_ll_age_cluster


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_ll_age_cluster = Quelle{[Schema="rep",Item="v_hr_ll_age_cluster"]}[Data]
in
    rep_v_hr_ll_age_cluster
```


## Table: rep v_hr_employee_job_history


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_job_history = Quelle{[Schema="rep",Item="v_hr_employee_job_history"]}[Data],
    #"Gefilterte Zeilen1" = Table.SelectRows(rep_v_hr_employee_job_history, each [valid_to] >= #date(2019, 1, 1))
in
    #"Gefilterte Zeilen1"
```


## Table: rep v_hr_employee_platform1_history


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_platform1_history = Quelle{[Schema="rep",Item="v_hr_employee_platform1_history"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(rep_v_hr_employee_platform1_history, each [valid_to] >= #date(2019, 1, 1))
in
    #"Gefilterte Zeilen"
```


## Table: rep v_hr_employee_platform2_history


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_platform2_history = Quelle{[Schema="rep",Item="v_hr_employee_platform2_history"]}[Data],
    #"Gefilterte Zeilen1" = Table.SelectRows(rep_v_hr_employee_platform2_history, each [valid_to] >= #date(2019, 1, 1))
in
    #"Gefilterte Zeilen1"
```


## Table: rep v_hr_employee_office_history


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_office_history = Quelle{[Schema="rep",Item="v_hr_employee_office_history"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(rep_v_hr_employee_office_history, each [valid_to] >= #date(2019, 1, 1))
in
    #"Gefilterte Zeilen"
```


## Table: rep v_hr_employee_costcenterassignment_history


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_costcenterassignment_history = Quelle{[Schema="rep",Item="v_hr_employee_costcenterassignment_history"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(rep_v_hr_employee_costcenterassignment_history, each [valid_to] >= #date(2019, 1, 1))
in
    #"Gefilterte Zeilen"
```


## Table: rep v_hr_employee_companyassignment_history


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_companyassignment_history = Quelle{[Schema="rep",Item="v_hr_employee_companyassignment_history"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(rep_v_hr_employee_companyassignment_history, each [valid_to] >= #date(2019, 1, 1))
in
    #"Gefilterte Zeilen"
```

