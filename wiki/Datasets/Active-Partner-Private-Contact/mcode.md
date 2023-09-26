



# M Code

|Dataset|[Active Partner Private Contact](./../Active-Partner-Private-Contact.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_employee_home_address_active


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_home_address_active = Source{[Schema="rep",Item="v_hr_employee_home_address_active"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_hr_employee_home_address_active, each ([jobcode] = "Partner" or [jobcode] = "Partner 1" or [jobcode] = "Partner 2" or [jobcode] = "Partner 3"))
in
    #"Filtered Rows"
```


## Table: rep v_hr_employee_birthday


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_birthday = Source{[Schema="rep",Item="v_hr_employee_birthday"]}[Data]
in
    rep_v_hr_employee_birthday
```

