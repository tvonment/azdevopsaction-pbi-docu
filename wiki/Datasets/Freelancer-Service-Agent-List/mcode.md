



# M Code

|Dataset|[Freelancer Service Agent List](./../Freelancer-Service-Agent-List.md)|
| :--- | :--- |
|Workspace|[HR_Freelancer](../../Workspaces/HR_Freelancer.md)|

## Table: rep v_hr_freelancer_sa


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_freelancer_sa = Source{[Schema="rep",Item="v_hr_freelancer_sa"]}[Data]
in
    rep_v_hr_freelancer_sa
```

