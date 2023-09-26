



# M Code

|Dataset|[NewEntriesWiithManagerLevel](./../NewEntriesWiithManagerLevel.md)|
| :--- | :--- |
|Workspace|[HR](../../Workspaces/HR.md)|

## Table: rep v_hr_check_new_entries_manager


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_check_new_entries_manager = Quelle{[Schema="rep",Item="v_hr_check_new_entries_manager"]}[Data]
in
    rep_v_hr_check_new_entries_manager
```

