



# M Code

|Dataset|[OD_Report](./../OD_Report.md)|
| :--- | :--- |
|Workspace|[F&C](../../Workspaces/F&C.md)|

## Table: NFR


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    sec_imp_fc_project_nfr_bridge = Source{[Schema="sec",Item="imp_fc_project_nfr_bridge"]}[Data]
in
    sec_imp_fc_project_nfr_bridge
```


## Table: Company_to_subregion


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_ll_company_to_subregion = Source{[Schema="pub",Item="ll_company_to_subregion"]}[Data]
in
    pub_ll_company_to_subregion
```

