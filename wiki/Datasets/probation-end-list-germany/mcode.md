



# M Code

|Dataset|[probation end list germany](./../probation-end-list-germany.md)|
| :--- | :--- |
|Workspace|[HR_Payroll](../../Workspaces/HR_Payroll.md)|

## Table: rep v_employee_probation_end


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_employee_probation_end_all = Source{[Schema="rep",Item="v_employee_probation_end"]}[Data]
in
    rep_v_employee_probation_end_all
```

