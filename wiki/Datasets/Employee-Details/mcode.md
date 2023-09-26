



# M Code

|Dataset|[Employee Details](./../Employee-Details.md)|
| :--- | :--- |
|Workspace|[Employee details](../../Workspaces/Employee-details.md)|

## Table: Employees


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="SELECT * FROM [datahub].[rep].[v_hr_employee_active]#(lf)UNION#(lf)SELECT * FROM [datahub].[rep].[v_hr_employee_future]"])
in
    Source
```


## Table: Birthdays


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_birthday = Source{[Schema="rep",Item="v_hr_employee_birthday"]}[Data]
in
    rep_v_hr_employee_birthday
```


## Table: Addresses


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_home_address = Source{[Schema="rep",Item="v_hr_employee_home_address"]}[Data]
in
    rep_v_hr_employee_home_address
```

