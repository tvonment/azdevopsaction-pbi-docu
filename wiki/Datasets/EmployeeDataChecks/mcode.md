



# M Code

|Dataset|[EmployeeDataChecks](./../EmployeeDataChecks.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_check


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check = Quelle{[Schema="rep",Item="v_hr_check"]}[Data]
in
    rep_v_hr_check
```


## Table: rep v_hr_check_accounting_catagory_vs_platform


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_accounting_catagory_vs_platform = Quelle{[Schema="rep",Item="v_hr_check_accounting_catagory_vs_platform"]}[Data]
in
    rep_v_hr_check_accounting_catagory_vs_platform
```


## Table: rep v_hr_check_ca_jc_c_1_2


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_ca_jc_c_1_2 = Quelle{[Schema="rep",Item="v_hr_check_ca_jc_c_1_2"]}[Data]
in
    rep_v_hr_check_ca_jc_c_1_2
```


## Table: rep v_hr_check_cc_cons_func_cons


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_cc_cons_func_cons = Quelle{[Schema="rep",Item="v_hr_check_cc_cons_func_cons"]}[Data]
in
    rep_v_hr_check_cc_cons_func_cons
```


## Table: rep v_hr_check_cc_serv_func_serv


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_cc_serv_func_serv = Quelle{[Schema="rep",Item="v_hr_check_cc_serv_func_serv"]}[Data]
in
    rep_v_hr_check_cc_serv_func_serv
```


## Table: rep v_hr_check_costcenter_vs_platform


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_costcenter_vs_platform = Quelle{[Schema="rep",Item="v_hr_check_costcenter_vs_platform"]}[Data]
in
    rep_v_hr_check_costcenter_vs_platform
```


## Table: rep v_hr_check_doublet_people


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_doublet_people = Quelle{[Schema="rep",Item="v_hr_check_doublet_people"]}[Data]
in
    rep_v_hr_check_doublet_people
```


## Table: rep v_hr_check_job_polarix


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_job_polarix = Quelle{[Schema="rep",Item="v_hr_check_job_polarix"]}[Data]
in
    rep_v_hr_check_job_polarix
```


## Table: rep v_hr_check_missing


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_missing = Quelle{[Schema="rep",Item="v_hr_check_missing"]}[Data]
in
    rep_v_hr_check_missing
```

