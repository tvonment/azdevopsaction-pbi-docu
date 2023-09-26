



# M Code

|Dataset|[MIRIAM](./../MIRIAM.md)|
| :--- | :--- |
|Workspace|[IT_Infrastructure](../../Workspaces/IT_Infrastructure.md)|

## Table: miriam v_emp_miriam_combined


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "Staging"),
    miriam_v_emp_miriam_combined = Source{[Schema="miriam",Item="v_emp_miriam_combined"]}[Data]
in
    miriam_v_emp_miriam_combined
```

