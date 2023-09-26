



# M Code

|Dataset|[Access_test_1](./../Access_test_1.md)|
| :--- | :--- |
|Workspace|[HR_Analytics_and_Statistics](../../Workspaces/HR_Analytics_and_Statistics.md)|

## Table: rep v_hr_employee_active


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_active = Source{[Schema="rep",Item="v_hr_employee_active"]}[Data]
in
    rep_v_hr_employee_active
```


## Table: active users


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee_active = Source{[Schema="rep",Item="v_hr_employee_active"]}[Data]
in
    rep_v_hr_employee_active
```


## Roles

### Austria


Model Permission: Read

rep v_hr_employee_active

```m
[company] = "Austria"
```


### Country1


Model Permission: Read

rep v_hr_employee_active

```m
[company] = USERPRINCIPALNAME()
```


### Country_dim


Model Permission: Read
### Country_dim2


Model Permission: Read

active users

```m
[email] = USERPRINCIPALNAME()
```

