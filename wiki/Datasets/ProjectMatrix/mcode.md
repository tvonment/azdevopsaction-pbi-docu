



# M Code

|Dataset|[ProjectMatrix](./../ProjectMatrix.md)|
| :--- | :--- |
|Workspace|[Public](../../Workspaces/Public.md)|

## Table: rep v_fc_project_data


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_fc_project_data = Source{[Schema="rep",Item="v_fc_project_data"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_fc_project_data, each ([project_status] = "Released")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"project_startdate", "project_enddate", "project_closedate", "responsible_accounting_emp_id", "responsible_accounting", "is_master", "source", "sales_order_id", "function_id", "industry_id", "has_success_fee"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"project_number", "Project number"}, {"project_name", "Project"}, {"project_client", "Client"}, {"dm_cc", "Platform"}, {"delivery_manager", "Delivery manager"}, {"project_manager", "Project manager"}, {"project_status", "Project status"}, {"responsible_unit_cou", "Company"}, {"responsible_unit_byd_id", "Company id"}})
in
    #"Renamed Columns"
```

