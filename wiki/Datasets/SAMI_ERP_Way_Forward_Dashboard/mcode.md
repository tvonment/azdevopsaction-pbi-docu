



# M Code

|Dataset|[SAMI_ERP_Way_Forward_Dashboard](./../SAMI_ERP_Way_Forward_Dashboard.md)|
| :--- | :--- |
|Workspace|[SAMI ERP](../../Workspaces/SAMI-ERP.md)|

## Table: Master progress


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIERPTransformation/Shared%20Documents/General/03_RB_Project_Management/20_BI%20Dashboard/20230810_SAMI%20ERP_Dashboard%20DB_V2.xlsx"), null, true),
    #"Master progress_Sheet" = Source{[Item="Master progress",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Master progress_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{ {"Column2", type any}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}, {"Column6", type text}, {"Column7", type any}, {"Column8", type any}, {"Column9", type text}, {"Column10", type any}, {"Column11", type text}, {"Column12", type text}, {"Column13", type any}, {"Column14", type text}, {"Column15", type text}}),
    #"Removed Top Rows" = Table.Skip(#"Changed Type",3),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers1",{{"Stream #", Int64.Type}, {"Stream", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Action #", type text}, {"Action", type text}, {"Start date", type date}, {"Planned due date", type date}, {"Updated due date", type text}, {"Closed date", type date}, {"Status", type text}, {"Issue/Risk", type text}, {"Progress (%)", Int64.Type}, {"Owner name", type text}, {"Comment", type text}})
in
    #"Changed Type1"
```


## Table: Issues & risks tracker


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIERPTransformation/Shared%20Documents/General/03_RB_Project_Management/20_BI%20Dashboard/20230810_SAMI%20ERP_Dashboard%20DB_V2.xlsx"), null, true),
    #"Issues & risks tracker_Sheet" = Source{[Item="Issues & risks tracker",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Issues & risks tracker_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Issue & risks tracker", type any}, {"Column2", type any}, {"Column3", type text}, {"Column4", type any}, {"Column5", type text}, {"Column6", type text}, {"Column7", type text}, {"Column8", type text}, {"Column9", type text}, {"Column10", type text}, {"Column11", type text}, {"Column12", type text}, {"Column13", type text}, {"Column14", type text}, {"Column15", type text}, {"Column16", type text}, {"Column17", type text}, {"Column18", type text}, {"Column19", type text}, {"Column20", type text}, {"Column21", type text}}),
    #"Removed Top Rows" = Table.Skip(#"Changed Type",3),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers1",{{"Issue or risks #", Int64.Type}, {"Flag (1-issue, 2-risk)", Int64.Type}, {"Description", type text}, {"Date raised", type date}, {"Reporter name", type text}, {"Status", type text}, {"Risk Ratings", type text}, {"Likelihood", type text}, {"Action #", type text}, {"Action", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Stream #", Int64.Type}, {"Stream", type text}, {"Impact (H/M/L)", type text}, {"Impact description", type text}, {"Root Cause ", type text}, {"Risk Response Owner ", type text}, {"Risk Response Strategy", type text}, {"Resolution Action", type text}, {"Comment", type text}})
in
    #"Changed Type1"
```


## Table: RIsk_Impact_Master


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIERPTransformation/Shared%20Documents/General/03_RB_Project_Management/20_BI%20Dashboard/20230810_SAMI%20ERP_Dashboard%20DB_V2.xlsx"), null, true),
    #"Issues & risks tracker_Sheet" = Source{[Item="Issues & risks tracker",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Issues & risks tracker_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Issue & risks tracker", type any}, {"Column2", type any}, {"Column3", type text}, {"Column4", type any}, {"Column5", type text}, {"Column6", type text}, {"Column7", type text}, {"Column8", type text}, {"Column9", type text}, {"Column10", type text}, {"Column11", type text}, {"Column12", type text}, {"Column13", type text}, {"Column14", type text}, {"Column15", type text}, {"Column16", type text}, {"Column17", type text}, {"Column18", type text}, {"Column19", type text}, {"Column20", type text}, {"Column21", type text}}),
    #"Removed Top Rows" = Table.Skip(#"Changed Type",3),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers1",{{"Issue or risks #", Int64.Type}, {"Flag (1-issue, 2-risk)", Int64.Type}, {"Description", type text}, {"Date raised", type date}, {"Reporter name", type text}, {"Status", type text}, {"Risk Ratings", type text}, {"Likelihood", type text}, {"Action #", type text}, {"Action", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Stream #", Int64.Type}, {"Stream", type text}, {"Impact (H/M/L)", type text}, {"Impact description", type text}, {"Root Cause ", type text}, {"Risk Response Owner ", type text}, {"Risk Response Strategy", type text}, {"Resolution Action", type text}, {"Comment", type text}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type1",{"Impact (H/M/L)"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each ([#"Impact (H/M/L)"] <> null))
in
    #"Filtered Rows"
```


## Table: RIsk_Response_Owner _Master


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIERPTransformation/Shared%20Documents/General/03_RB_Project_Management/20_BI%20Dashboard/20230810_SAMI%20ERP_Dashboard%20DB_V2.xlsx"), null, true),
    #"Issues & risks tracker_Sheet" = Source{[Item="Issues & risks tracker",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Issues & risks tracker_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Issue & risks tracker", type any}, {"Column2", type any}, {"Column3", type text}, {"Column4", type any}, {"Column5", type text}, {"Column6", type text}, {"Column7", type text}, {"Column8", type text}, {"Column9", type text}, {"Column10", type text}, {"Column11", type text}, {"Column12", type text}, {"Column13", type text}, {"Column14", type text}, {"Column15", type text}, {"Column16", type text}, {"Column17", type text}, {"Column18", type text}, {"Column19", type text}, {"Column20", type text}, {"Column21", type text}}),
    #"Removed Top Rows" = Table.Skip(#"Changed Type",3),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers1",{{"Issue or risks #", Int64.Type}, {"Flag (1-issue, 2-risk)", Int64.Type}, {"Description", type text}, {"Date raised", type date}, {"Reporter name", type text}, {"Status", type text}, {"Risk Ratings", type text}, {"Likelihood", type text}, {"Action #", type text}, {"Action", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Stream #", Int64.Type}, {"Stream", type text}, {"Impact (H/M/L)", type text}, {"Impact description", type text}, {"Root Cause ", type text}, {"Risk Response Owner ", type text}, {"Risk Response Strategy", type text}, {"Resolution Action", type text}, {"Comment", type text}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type1",{"Risk Response Owner "}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each ([#"Risk Response Owner "] <> null))
in
    #"Filtered Rows"
```


## Table: Stream_Master


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIERPTransformation/Shared%20Documents/General/03_RB_Project_Management/20_BI%20Dashboard/20230810_SAMI%20ERP_Dashboard%20DB_V2.xlsx"), null, true),
    #"Master progress_Sheet" = Source{[Item="Master progress",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Master progress_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{ {"Column2", type any}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}, {"Column6", type text}, {"Column7", type any}, {"Column8", type any}, {"Column9", type text}, {"Column10", type any}, {"Column11", type text}, {"Column12", type text}, {"Column13", type any}, {"Column14", type text}, {"Column15", type text}}),
    #"Removed Top Rows" = Table.Skip(#"Changed Type",3),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers1",{{"Stream #", Int64.Type}, {"Stream", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Action #", type text}, {"Action", type text}, {"Start date", type date}, {"Planned due date", type date}, {"Updated due date", type text}, {"Closed date", type date}, {"Status", type text}, {"Issue/Risk", type text}, {"Progress (%)", Int64.Type}, {"Owner name", type text}, {"Comment", type text}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type1",{"Stream #", "Stream"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns")
in
    #"Removed Duplicates"
```


## Table: Date_Master


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIERPTransformation/Shared%20Documents/General/03_RB_Project_Management/20_BI%20Dashboard/20230810_SAMI%20ERP_Dashboard%20DB_V2.xlsx"), null, true),
    #"Master progress_Sheet" = Source{[Item="Master progress",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Master progress_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{ {"Column2", type any}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}, {"Column6", type text}, {"Column7", type any}, {"Column8", type any}, {"Column9", type text}, {"Column10", type any}, {"Column11", type text}, {"Column12", type text}, {"Column13", type any}, {"Column14", type text}, {"Column15", type text}}),
    #"Removed Top Rows" = Table.Skip(#"Changed Type",3),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers1",{{"Stream #", Int64.Type}, {"Stream", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Action #", type text}, {"Action", type text}, {"Start date", type date}, {"Planned due date", type date}, {"Updated due date", type text}, {"Closed date", type date}, {"Status", type text}, {"Issue/Risk", type text}, {"Progress (%)", Int64.Type}, {"Owner name", type text}, {"Comment", type text}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type1",{"Start date"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates",{{"Start date", "Date"}}),
    #"Inserted Start of Month" = Table.AddColumn(#"Renamed Columns", "Start of Month", each Date.StartOfMonth([Date]), type date),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Start of Month", each ([Date] <> null))
in
    #"Filtered Rows"
```


## Table: Milestone progress- required columns


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIERPTransformation/Shared%20Documents/General/03_RB_Project_Management/20_BI%20Dashboard/20230810_SAMI%20ERP_Dashboard%20DB_V2.xlsx"), null, true),
    #"Milestone progress_Sheet" = Source{[Item="Milestone progress",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Milestone progress_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.Profile( #"Milestone progress")[[Column],[Count],[NullCount]],
    #"Added Conditional Column" = Table.AddColumn(#"Changed Type", "NullFlag", each if [Count] = [NullCount] then 1 else 0),
    #"Filtered Rows" = Table.SelectRows(#"Added Conditional Column", each ([NullFlag] = 1))[Column],
    #"Required Columns" = Table.RemoveColumns(#"Milestone progress",#"Filtered Rows"),
    Custom1 = let cols = Table.ColumnNames(#"Required Columns") in Table.SelectColumns( #"Required Columns", List.FirstN(cols,4) & List.LastN(cols,2)),
    #"Renamed Columns" = Table.RenameColumns(#"Custom1",{{"ERP Way Forward milestone progress", "WBS#"}, {"Column2", "Activity"}, {"Column3", "Excel"}, {"Column4", "Weight"}, {Table.ColumnNames(#"Custom1"){4}, "Progress - Prev Week"},{Table.ColumnNames(#"Custom1"){5}, "Progress - Curr Week"}}),
    #"Removed Top Rows" = Table.Skip(#"Renamed Columns",5),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Top Rows", each ([Activity] <> null and [Activity] <> "Aggregate")),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows1","-","",Replacer.ReplaceText,{"WBS#"}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Replaced Value", "WBS#", "WBS# - Copy"),
    #"Renamed Columns1" = Table.RenameColumns(#"Duplicated Column",{{"WBS# - Copy", "Stream#"}}),
    #"Extracted Text Before Delimiter" = Table.TransformColumns(#"Renamed Columns1", {{"Stream#", each Text.BeforeDelimiter(_, "."), type text}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Extracted Text Before Delimiter",{{"Weight", type number}})
in
    #"Changed Type1"
```

