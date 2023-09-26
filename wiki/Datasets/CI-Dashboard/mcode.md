



# M Code

|Dataset|[CI Dashboard](./../CI-Dashboard.md)|
| :--- | :--- |
|Workspace|[CorporateInvestments](../../Workspaces/CorporateInvestments.md)|

## Table: Months


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSK1YlWMgKTxmDSBEyagkkzMGkOJi3ApCWYNDSAUBDdhkDtsQA=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Months = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Months", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Months", "Month"}})
in
    #"Renamed Columns"
```


## Table: _measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: fact cost ics


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    
    dbo_vExport_Ics_Costs = Source{[Schema="rep",Item="v_ics_export_ics_costs"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(dbo_vExport_Ics_Costs,{ {"RECHNUNGSDATUM", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"RECHNUNGSDATUM", "CostDate"}, {"GESAMTBETRAG", "Costs"}, {"ANZAHL", "Amount"}, {"EINZELPREIS", "Price"}, {"RECHNUNGSNUMMER", "InvoiceNumber"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"CIID", type text}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type1", "InternalId", each Text.From([CIID]), Text.Type),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom", each [CostDate] >= #date(2018, 1, 1)),
    #"Added Custom1" = Table.AddColumn(#"Filtered Rows", "project_id", each if [CIID] <> null and Text.Contains([CIID], "-") then Text.BeforeDelimiter([CIID], "-") else "", Text.Type),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "project_task_id", each if  [CIID] <> null and  Text.Contains ([CIID], "-") then Text.BeforeDelimiter([CIID], "-", 1) else "", Text.Type),
    #"Cleaned Text" = Table.TransformColumns(#"Added Custom2",{{"project_id", Text.Clean, type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Cleaned Text",{{"project_id", Text.Trim, type text}}),
    #"Cleaned Text1" = Table.TransformColumns(#"Trimmed Text",{{"project_task_id", Text.Clean, type text}}),
    #"Trimmed Text1" = Table.TransformColumns(#"Cleaned Text1",{{"project_task_id", Text.Trim, type text}}),
    #"Uppercased Text" = Table.TransformColumns(#"Trimmed Text1",{{"project_id", Text.Upper, type text}, {"project_task_id", Text.Upper, type text}}),
    #"Extracted Text Between Delimiters" = Table.TransformColumns(#"Uppercased Text", {{"project_task_id", each if Text.EndsWith(_, "-0") then Text.BeforeDelimiter(_, "-") else _ , type text}}),
    #"Filtered Rows1" = Table.SelectRows(#"Extracted Text Between Delimiters", each true),
    #"Added Index" = Table.AddIndexColumn(#"Filtered Rows1", "Index", 0, 1, Int64.Type)
in
    #"Added Index"
```


## Table: fact budget


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_ci_budget = Source{[Schema="rep",Item="ci_budget"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_ci_budget, each [month] <> null and [month] <> ""),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"ci_id", "CIID"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "ProjectNumber", each Text.BeforeDelimiter( [sap_project_task_id],"-"), Text.Type),
    #"Uppercased Text" = Table.TransformColumns(#"Added Custom",{{"sap_project_task_id", Text.Upper, type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Uppercased Text",{{"sap_project_task_id", Text.Trim, type text}}),
    #"Merged Queries" = Table.NestedJoin(#"Trimmed Text", {"contact"}, #"dim Contacts", {"contact"}, "dim Contacts", JoinKind.LeftOuter),
    #"Expanded dim Contacts" = Table.ExpandTableColumn(#"Merged Queries", "dim Contacts", {"Index"}, {"ContactId"}),
    #"Cleaned Text" = Table.TransformColumns(#"Expanded dim Contacts",{{"sap_project_task_id", Text.Clean, type text}}),
    #"Uppercased Text1" = Table.TransformColumns(#"Cleaned Text",{{"ProjectNumber", Text.Upper, type text}}),
    #"Trimmed Text1" = Table.TransformColumns(#"Uppercased Text1",{{"sap_project_task_id", Text.Trim, type text}, {"ProjectNumber", Text.Trim, type text}}),
    #"Cleaned Text1" = Table.TransformColumns(#"Trimmed Text1",{{"ProjectNumber", Text.Clean, type text}}),
    #"Uppercased Text2" = Table.TransformColumns(#"Cleaned Text1",{{"sap_project_task_id", Text.Upper, type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Uppercased Text2",null,"Planned",Replacer.ReplaceValue,{"status"})
in
    #"Replaced Value"
```


## Table: CIIDs


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_ci_budget = Source{[Schema="rep",Item="ci_budget"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_ci_budget, each [month] <> null and [month] <> ""),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"ci_id", "CIID"}}),
    CIID1 = #"Renamed Columns"[CIID],
    #"Converted to Table" = Table.FromList(CIID1, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Renamed Columns1" = Table.RenameColumns(#"Converted to Table",{{"Column1", "CIID"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns1",{{"CIID", type text}}),
    #"Appended Query" = Table.Combine({#"Changed Type", #"CIID from cost"}),
    #"Uppercased Text" = Table.TransformColumns(#"Appended Query",{{"CIID", Text.Upper, type text}}),
    #"Cleaned Text" = Table.TransformColumns(#"Uppercased Text",{{"CIID", Text.Clean, type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Cleaned Text",{{"CIID", Text.Trim, type text}}),
    #"Removed Duplicates" = Table.Distinct(#"Trimmed Text"),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Duplicates", each [CIID] <> null and [CIID] <> "")
in
    #"Filtered Rows1"
```


## Table: fact cost byd


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_imp_fc_byd_project_internal_incurred_costs = Source{[Schema="rep",Item="v_fc_ci_byd_project_internal_incurred_costs"]}[Data],
    #"F Supplier Invoice" = Table.SelectRows(rep_imp_fc_byd_project_internal_incurred_costs, each ([expense_type] <> "Service Expenses (Internal)") and ([business_transaction_type] = "Supplier Invoice")),
    #"F empty project id" = Table.SelectRows(#"F Supplier Invoice", each [project_id] <> null and [project_id] <> ""),
    #"F not CP* || ACP*" = Table.SelectRows(#"F empty project id", each not Text.StartsWith([project_id], "CP") and not Text.StartsWith([project_id], "ACQ")),
    #"F  2021" = Table.SelectRows(#"F not CP* || ACP*", each [posting_date] >= #datetime(2021, 1, 1, 0, 0, 0)),
    #"F empty task id" = Table.SelectRows(#"F  2021", each [project_task_id] <> null and [project_task_id] <> ""),
    #"Trimmed Text" = Table.TransformColumns(#"F empty task id",{{"project_task_id", Text.Trim, type text}}),
    #"Uppercased Text" = Table.TransformColumns(#"Trimmed Text",{{"project_task_id", Text.Upper, type text}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Uppercased Text",{{"posting_date", type date}}),
    #"Cleaned Text" = Table.TransformColumns(#"Changed Type",{{"project_task_id", Text.Clean, type text}}),
    #"Trimmed Text1" = Table.TransformColumns(#"Cleaned Text",{{"project_task_id", Text.Trim, type text}, {"project_id", Text.Trim, type text}}),
    #"Cleaned Text1" = Table.TransformColumns(#"Trimmed Text1",{{"project_id", Text.Clean, type text}}),
    #"Uppercased Text1" = Table.TransformColumns(#"Cleaned Text1",{{"project_task_id", Text.Upper, type text}, {"ic_source_project_id", Text.Upper, type text}}),
    Custom1 = Table.ReplaceValue(#"Uppercased Text1",each [amount_company], each if Text.StartsWith( [source_document_id], "C") then -1 * [amount_company] else [amount_company] ,Replacer.ReplaceValue,{"amount_company"}),
    #"Changed Type1" = Table.TransformColumnTypes(Custom1,{{"amount_company", type number}}),
    #"Added Index" = Table.AddIndexColumn(#"Changed Type1", "Index", 0, 1, Int64.Type)
in
    #"Added Index"
```


## Table: dim Contacts


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_ci_budget = Source{[Schema="rep",Item="ci_budget"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_ci_budget, each [month] <> null and [month] <> ""),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"contact"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Added Index" = Table.AddIndexColumn(#"Removed Duplicates", "Index", 0, 1, Int64.Type)
in
    #"Added Index"
```


## Table: project tasks


```m
let
    Source = #"project tasks byd",
    #"Appended Query" = Table.Combine({Source, #"project tasks ics"}),
    #"Removed Duplicates" = Table.Distinct(#"Appended Query"),
    #"Appended Query1" = Table.Combine({#"Removed Duplicates", #"project tasks budget"}),
    #"Cleaned Text" = Table.TransformColumns(#"Appended Query1",{{"project_task_id", Text.Clean, type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Cleaned Text",{{"project_task_id", Text.Trim, type text}}),
    #"Uppercased Text1" = Table.TransformColumns(#"Trimmed Text",{{"project_task_id", Text.Upper, type text}}),
    #"Uppercased Text" = Table.TransformColumns(#"Uppercased Text1",{{"project_id", Text.Upper, type text}}),
    #"Cleaned Text1" = Table.TransformColumns(#"Uppercased Text",{{"project_id", Text.Clean, type text}}),
    #"Trimmed Text1" = Table.TransformColumns(#"Cleaned Text1",{{"project_id", Text.Trim, type text}}),
    #"Removed Duplicates1" = Table.Distinct(#"Trimmed Text1"),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates1", each [project_task_id] <> null and [project_task_id] <> ""),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"project_task_id"}, #"rep v_byd_project_task_data", {"TASK_ID"}, "rep v_byd_project_task_data", JoinKind.LeftOuter),
    #"Expanded rep v_byd_project_task_data" = Table.ExpandTableColumn(#"Merged Queries", "rep v_byd_project_task_data", {"TASK"}, {"Task"}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded rep v_byd_project_task_data", {"project_id"}, #"rep v_byd_project_task_data projects", {"PROJECT_ID"}, "rep v_byd_project_task_data", JoinKind.LeftOuter),
    #"Expanded rep v_byd_project_task_data1" = Table.ExpandTableColumn(#"Merged Queries1", "rep v_byd_project_task_data", {"PROJECT_NAME"}, {"Project"})
in
    #"Expanded rep v_byd_project_task_data1"
```


## Table: FormatStackedColumns


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WcipNSU8tUdJRciwoKMovS01RiAxxAXINlWJ1sMmG5Jck5ijoQlUZoaoKyEnMy0tNAbKMwRLO+cVgzcklpYk5QIYJsmhQam5iZl5mXjqQbaoUGwsA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [ColumnType = _t, ValueType = _t, Sort = _t]),
    #"Changed Type1" = Table.TransformColumnTypes(Source,{{"Sort", Int64.Type}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Changed Type1",{{"ColumnType", type text}, {"ValueType", type text}})
in
    #"Changed Type"
```


## Table: contact to projects


```m
let
    Source = #"fact budget",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"contact", "ProjectNumber", "ContactId"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns")
in
    #"Removed Duplicates"
```


## Table: projects


```m
let
    Source = #"contact to projects",
    #"Removed Columns" = Table.RemoveColumns(Source,{"contact", "ContactId"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns")
in
    #"Removed Duplicates"
```


## Parameter: Year


```m
2021 meta [IsParameterQuery=true, Type="Any", IsParameterQueryRequired=true]
```

