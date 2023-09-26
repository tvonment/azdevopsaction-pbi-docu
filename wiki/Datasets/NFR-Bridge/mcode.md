



# M Code

|Dataset|[NFR Bridge](./../NFR-Bridge.md)|
| :--- | :--- |
|Workspace|[FC_NFR](../../Workspaces/FC_NFR.md)|

## Table: exchange rates


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    pub_v_ll_exchange_rates_monthly_avg = Quelle{[Schema="pub",Item="v_ll_exchange_rates_monthly_avg"]}[Data]
in
    pub_v_ll_exchange_rates_monthly_avg
```


## Table: _measures


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Spalte ""1""" = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Spalte ""1""", type text}}),
    #"Entfernte Spalten" = Table.RemoveColumns(#"Geänderter Typ",{"Spalte ""1"""})
in
    #"Entfernte Spalten"
```


## Table: currencies


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    pub_v_ll_exchange_rates_monthly_avg = Quelle{[Schema="pub",Item="v_ll_exchange_rates_monthly_avg"]}[Data],
    #"Andere entfernte Spalten" = Table.SelectColumns(pub_v_ll_exchange_rates_monthly_avg,{"target_currency"}),
    #"Entfernte Duplikate" = Table.Distinct(#"Andere entfernte Spalten"),
    #"Sortierte Zeilen" = Table.Sort(#"Entfernte Duplikate",{{"target_currency", Order.Ascending}})
in
    #"Sortierte Zeilen"
```


## Table: companies


```m
let
    Quelle = Sql.Database("muc-mssql-2", "datahub"),
    sec_imp_fc_project_nfr_bridge = Quelle{[Schema="sec",Item="imp_fc_project_nfr_bridge"]}[Data],
    #"Gefilterte Zeilen" = Table.SelectRows(sec_imp_fc_project_nfr_bridge, each ([reporting_line_unit_id] <> null and [reporting_line_unit_id] <> "") ),
    #"Removed Other Columns" = Table.SelectColumns(#"Gefilterte Zeilen",{"company", "reporting_line_unit_id"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    CompanyID = Table.AddColumn(#"Removed Duplicates", "CompanyID", each Text.Start([reporting_line_unit_id], 2), type text),
    #"Removed Columns" = Table.RemoveColumns(CompanyID,{"reporting_line_unit_id"}),
    #"Removed Duplicates1" = Table.Distinct(#"Removed Columns", {"CompanyID"}),
    #"join comp for currency" = Table.NestedJoin(#"Removed Duplicates1", {"CompanyID"}, #"rep v_ll_company", {"company_id"}, "rep v_ll_company", JoinKind.LeftOuter),
    #"Erweiterte rep v_ll_company" = Table.ExpandTableColumn(#"join comp for currency", "rep v_ll_company", {"currency"}, {"currency"}),
    #"Entfernte Duplikate" = Table.Distinct(#"Erweiterte rep v_ll_company")
in
    #"Entfernte Duplikate"
```


## Table: nfr absolut


```m
let
    Quelle = #"sec imp_fc_project_nfr_bridge",
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(Quelle, "prev_report_month", each if Date.Month([report_month])> 1 then Date.AddMonths([report_month], -1) else null, type date),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Hinzugefügte benutzerdefinierte Spalte", {"prev_report_month", "reporting_line_unit_id", "project_number", "emp_id", "jobcode_id"}, #"Hinzugefügte benutzerdefinierte Spalte", {"report_month", "reporting_line_unit_id", "project_number", "emp_id", "jobcode_id"}, "prev", JoinKind.LeftOuter),
    #"Erweiterte prev" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "prev", {"target_hours_adj", "hours_worked_on_client_projects", "hours_worked_on_other_projects", "pdr_lc", "target_time_lc", "leave_time_lc", "vacation_time_lc", "training_time_lc", "target_time_adj_lc", "internal_time_lc", "acquisition_time_lc", "client_time_lc", "diff_target_time_vs_booked_time_lc", "planned_od_lc", "add_od_lc", "sum_od_lc", "acc_nfr_lc"}, {"prev.target_hours_adj", "prev.hours_worked_on_client_projects", "prev.hours_worked_on_other_projects", "prev.pdr_lc", "prev.target_time_lc", "prev.leave_time_lc", "prev.vacation_time_lc", "prev.training_time_lc", "prev.target_time_adj_lc", "prev.internal_time_lc", "prev.acquisition_time_lc", "prev.client_time_lc", "prev.diff_target_time_vs_booked_time_lc", "prev.planned_od_lc", "prev.add_od_lc", "prev.sum_od_lc", "prev.acc_nfr_lc"})
in
    #"Erweiterte prev"
```


## Table: Formatting


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("bZFbT8MwDIX/StQnkKaOcudxXCYhIYom2Ms0VSb1RqBzujTtJn49TmjpsvFiJT5f7BOd2Sx6Hk/ECrZxNIiSEy585jqFosZoPphFTwgNDqcgh68GFMXiFipk4tTB73zOiqzJLF+88N8TRydcOrAf3i0XkH867Kx1kPE9AEdyXatKWaWpM3D+ZwCk3F2/wzrMbQa5DsY9kkVDUIiNNl+sXLhZanPgbWl0VXH30undpUdeCiDCXKT33L5yTJnpPDSe5/Gvfu102NfdFkIrpKaqLqyipTgaSRkLFo6ZvPGv/Af7R6n9QCPGiEKR1Cv02TlQL1QATrDUxrJDnuYgn7BpmwH5sC2RKhQGG6TaT/QJY8ad0DG73aF8ZHRApQ2a3MDC5Z34qPY+fgelrQ2KCVg/x0cgTcC8WVWob2iTTHwKNfd6aP4D", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Type = _t, Sort = _t, key = _t, ValType = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Type", type text}, {"Sort", Int64.Type}})
in
    #"Geänderter Typ"
```

