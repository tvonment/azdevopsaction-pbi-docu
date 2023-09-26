



# M Code

|Dataset|[SAMI_AAI_Dashboard](./../SAMI_AAI_Dashboard.md)|
| :--- | :--- |
|Workspace|[SAMI ERP](../../Workspaces/SAMI-ERP.md)|

## Table: Master progress


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIAAIDashboard/Shared%20Documents/General/01-Source_File/SAMI_AAI_Dashboard_DB.xlsx"), null, true),
    #"Master progress_Sheet" = Source{[Item="Master progress",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Master progress_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{ {"Column2", type any}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}, {"Column6", type text}, {"Column7", type any}, {"Column8", type any}, {"Column9", type text}, {"Column10", type any}, {"Column11", type text}, {"Column12", type text}, {"Column13", type any}, {"Column14", type text}, {"Column15", type text}}),
    #"Removed Top Rows" = Table.Skip(#"Changed Type",3),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers1",{{"Stream #", Int64.Type}, {"Stream", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Action #", type text}, {"Action", type text}, {"Start date", type date}, {"Closed date", type date}, {"Status", type text}, {"Progress (%)", Int64.Type}, {"Owner name", type text}, {"Comment", type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type1", each ([#"Stream #"] <> null)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Column19"})
in
    #"Removed Columns"
```


## Table: Issues & risks tracker


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIAAIDashboard/Shared%20Documents/General/01-Source_File/SAMI_AAI_Dashboard_DB.xlsx"), null, true),
    #"Issues & risks tracker_Sheet" = Source{[Item="Issues & risks tracker",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Issues & risks tracker_Sheet", [PromoteAllScalars=true]),
    #"Removed Top Rows" = Table.Skip(#"Promoted Headers",2),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers1",{{"Risk Ratings [1-5]", "Risk Ratings"}, {"Likelihood [1-5]", "Likelihood"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"Issue or risks #", Int64.Type}, {"Flag (1-issue, 2-risk)", Int64.Type}, {"Description", type text}, {"Date raised", type date}, {"Reporter name", type text}, {"Status", type text}, {"Risk Ratings", type text}, {"Likelihood", type text}, {"Action #", type text}, {"Action", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Stream #", Int64.Type}, {"Stream", type text}, {"Impact (H/M/L)", type text}, {"Impact description", type text}, {"Root Cause ", type text}, {"Risk Response Owner ", type text}, {"Risk Response Strategy", type text}, {"Resolution Action", type text}, {"Comment", type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type1", each ([#"Issue or risks #"] <> null))
in
    #"Filtered Rows"
```


## Table: RIsk_Impact_Master


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIAAIDashboard/Shared%20Documents/General/01-Source_File/SAMI_AAI_Dashboard_DB.xlsx"), null, true),
    #"Issues & risks tracker_Sheet" = Source{[Item="Issues & risks tracker",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Issues & risks tracker_Sheet", [PromoteAllScalars=true]),
    #"Removed Top Rows" = Table.Skip(#"Promoted Headers",2),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers1",{{"Risk Ratings [1-5]", "Risk Ratings"}, {"Likelihood [1-5]", "Likelihood"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"Issue or risks #", Int64.Type}, {"Flag (1-issue, 2-risk)", Int64.Type}, {"Description", type text}, {"Date raised", type date}, {"Reporter name", type text}, {"Status", type text}, {"Risk Ratings", type text}, {"Likelihood", type text}, {"Action #", type text}, {"Action", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Stream #", Int64.Type}, {"Stream", type text}, {"Impact (H/M/L)", type text}, {"Impact description", type text}, {"Root Cause ", type text}, {"Risk Response Owner ", type text}, {"Risk Response Strategy", type text}, {"Resolution Action", type text}, {"Comment", type text}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type1",{"Impact (H/M/L)"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each ([#"Impact (H/M/L)"] <> null))
in
    #"Filtered Rows"
```


## Table: RIsk_Response_Owner _Master


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIAAIDashboard/Shared%20Documents/General/01-Source_File/SAMI_AAI_Dashboard_DB.xlsx"), null, true),
    #"Issues & risks tracker_Sheet" = Source{[Item="Issues & risks tracker",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Issues & risks tracker_Sheet", [PromoteAllScalars=true]),
    #"Removed Top Rows" = Table.Skip(#"Promoted Headers",2),
    #"Promoted Headers1" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(#"Promoted Headers1",{{"Risk Ratings [1-5]", "Risk Ratings"}, {"Likelihood [1-5]", "Likelihood"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"Issue or risks #", Int64.Type}, {"Flag (1-issue, 2-risk)", Int64.Type}, {"Description", type text}, {"Date raised", type date}, {"Reporter name", type text}, {"Status", type text}, {"Risk Ratings", type text}, {"Likelihood", type text}, {"Action #", type text}, {"Action", type text}, {"Milestone #", type text}, {"Milestone", type text}, {"Stream #", Int64.Type}, {"Stream", type text}, {"Impact (H/M/L)", type text}, {"Impact description", type text}, {"Root Cause ", type text}, {"Risk Response Owner ", type text}, {"Risk Response Strategy", type text}, {"Resolution Action", type text}, {"Comment", type text}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Changed Type1",{"Risk Response Owner "}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each ([#"Risk Response Owner "] <> null))
in
    #"Filtered Rows"
```


## Table: Stream_Master


```m
let
    Source = #"Master progress",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"Stream #", "Stream"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns")
in
    #"Removed Duplicates"
```


## Table: Date_Master


```m
let
    Source = #"Master progress",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"Start date"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Other Columns",{{"Start date", "Date"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns"),
    #"Inserted Start of Month" = Table.AddColumn(#"Removed Duplicates", "Start of Month", each Date.StartOfMonth([Date]), type date),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Start of Month", each ([Date] <> null))
in
    #"Filtered Rows"
```


## Table: Action_Status_Master


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/SAMIAAIDashboard/Shared%20Documents/General/01-Source_File/SAMI_AAI_Dashboard_DB.xlsx"), null, true),
    Action_Status_Master_Sheet = Source{[Item="Action_Status_Master",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Action_Status_Master_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Status_ID", Int64.Type}, {"Status", type text}})
in
    #"Changed Type"
```

