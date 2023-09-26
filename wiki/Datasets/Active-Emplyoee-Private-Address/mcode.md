



# M Code

|Dataset|[Active Emplyoee Private Address](./../Active-Emplyoee-Private-Address.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_employee_home_address_active


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_home_address_active = Source{[Schema="rep",Item="v_hr_employee_home_address_active"]}[Data]
in
    rep_v_hr_employee_home_address_active
```

