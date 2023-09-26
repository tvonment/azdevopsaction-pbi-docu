



# M Code

|Dataset|[Active Employee Private Contact](./../Active-Employee-Private-Contact.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_employee_home_address_active


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_home_address_active = Source{[Schema="rep",Item="v_hr_employee_home_address_active"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_hr_employee_home_address_active, each ([company_id] = "01" or [company_id] = "12"))
in
    #"Filtered Rows"
```

