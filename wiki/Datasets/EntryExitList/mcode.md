



# M Code

|Dataset|[EntryExitList](./../EntryExitList.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_employee_entry_exit


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_hr_employee_entry_exit = Source{[Schema="rep",Item="v_hr_employee_entry_exit"]}[Data]
in
    rep_v_hr_employee_entry_exit
```

