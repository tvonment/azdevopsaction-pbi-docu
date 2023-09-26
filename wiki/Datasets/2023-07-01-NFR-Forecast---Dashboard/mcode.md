



# M Code

|Dataset|[2023-07-01 NFR Forecast - Dashboard](./../2023-07-01-NFR-Forecast---Dashboard.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: PREP_NFR_Projection_All


```m
let
    Source = Table.Combine({SRC_Subitems}),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Subitem.person] <> "")),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"Subitem.projectCode"}, SRC_OD, {"Project Code"}, "Project Overdrafts", JoinKind.LeftOuter),
    #"Expanded Project Overdrafts" = Table.ExpandTableColumn(#"Merged Queries", "Project Overdrafts", {"OD", "Discounted price (%)"}, {"Project Overdrafts.OD", "Project Overdrafts.Discounted price (%)"}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded Project Overdrafts", {"Subitem.person"}, SRC_Team, {"Concat3"}, "Team", JoinKind.LeftOuter),
    #"Expanded Team" = Table.ExpandTableColumn(#"Merged Queries1", "Team", {"M-Nummer", "Vorname", "Name", "Rolle", "Firma", "Team", "Status"}, {"Team.M-Nummer", "Team.Vorname", "Team.Name", "Team.Rolle", "Team.Firma", "Team.Team", "Team.Status"}),
    #"Merged Queries2" = Table.NestedJoin(#"Expanded Team", {"Team.Rolle"}, SRC_DailyRates, {"Level"}, "Daily", JoinKind.LeftOuter),
    #"Expanded Daily" = Table.ExpandTableColumn(#"Merged Queries2", "Daily", {"Daily NFR"}, {"Daily.Daily NFR"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Daily", "NFR", each [Subitem.days]*[Daily.Daily NFR]),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"NFR"}),
    #"Added Custom1" = Table.AddColumn(#"Removed Columns", "NFR", each [Subitem.days]*[#"Project Overdrafts.Discounted price (%)"]*[Daily.Daily NFR]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom1",{{"NFR", type number}}),
    #"Merged Queries3" = Table.NestedJoin(#"Changed Type", {"Subitem.projectType"}, SRC_ProjectTypes, {"Subitem.projectType"}, "SRC_ProjectTypes", JoinKind.LeftOuter),
    #"Expanded SRC_ProjectTypes" = Table.ExpandTableColumn(#"Merged Queries3", "SRC_ProjectTypes", {"Availability", "Billable"}, {"SRC_ProjectTypes.Availability", "SRC_ProjectTypes.Billable"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded SRC_ProjectTypes",{{"SRC_ProjectTypes.Availability", "ProjectTypes.Availability"}, {"SRC_ProjectTypes.Billable", "ProjectTypes.Billable"}}),
    #"Added Custom2" = Table.AddColumn(#"Renamed Columns", "Subitem.projectTimelineStart", each Text.Range([Subitem.projectTimeline],0,4) & "-" &Text.Range([Subitem.projectTimeline],5,2)& "-" &Text.Range([Subitem.projectTimeline],8,2)),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Added Custom2", {{"Subitem.projectTimelineStart", ""}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Errors",{{"Subitem.projectTimelineStart", type date}}),
    #"Added Custom3" = Table.AddColumn(#"Changed Type1", "Subitem.projectTimelineEnd", each Text.Range([Subitem.projectTimeline],11,4) & "-" &Text.Range([Subitem.projectTimeline],16,2)& "-" &Text.Range([Subitem.projectTimeline],19,2)),
    #"Replaced Errors1" = Table.ReplaceErrorValues(#"Added Custom3", {{"Subitem.projectTimelineEnd", ""}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Replaced Errors1",{{"Subitem.projectTimelineEnd", type date}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type2",{{"NFR", "NFR Plan"}}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Renamed Columns1", "Subitem.projectYearWeek", each Number.ToText([Subitem.projectYear])&"-"&Text.End("0"&Number.ToText(Date.WeekOfYear([Subitem.projectTimelineStart])-1),2)),
    #"Renamed Columns2" = Table.RenameColumns(#"Hinzugefügte benutzerdefinierte Spalte",{{"NFR Plan", "NFR Projection"}})
in
    #"Renamed Columns2"
```


## Table: SRC_Subitems


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"Filtered Rows" = Table.SelectRows(Source, each Text.StartsWith([Name], "part-")), //[Name] = "part-00000-tid-5258741896492417233-20aa3300-abdd-4f67-8a5e-0cdb47da80a0-8-1.c000.snappy.parquet")),
    #"Filtered Hidden Files1" = Table.SelectRows(#"Filtered Rows", each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File", each #"Transform File"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File"}),
    #"Transform File1" = #"Removed Other Columns1"{0}[Transform File],
    #"Changed Type" = Table.TransformColumnTypes(#"Transform File1",{{"Item.id", Int64.Type}, {"Item.name", type text}, {"Subitem.id", Int64.Type}, {"Subitem.name", type text}, {"Subitem.person", type text}, {"Subitem.projectYearMonth", type text}, {"Subitem.projectYear", Int64.Type}, {"Subitem.projectMonth", Int64.Type}, {"Subitem.days", type text}, {"Subitem.projectCode", type text}, {"Subitem.projectType", type text}, {"Subitem.projectTimeline", type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",".",",",Replacer.ReplaceText,{"Subitem.days"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Value",{{"Subitem.days", type number}})
in
    #"Changed Type1"
```


## Table: SRC_DailyRates


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - Daily Rates xlsx" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/",Name="2023-01-01 NFR Forecast - Daily Rates.xlsx"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - Daily Rates xlsx"),
    Daily_Sheet = #"Imported Excel Workbook"{[Item="Daily",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Daily_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Level", type text}, {"Daily NFR", type number}, {"Level relevant?", Int64.Type}, {"Relevant Daily NFR", type number}})
in
    #"Changed Type"
```


## Table: SRC_OD


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - Project Overdrafts xlsx" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/",Name="2023-01-01 NFR Forecast - Project Overdrafts.xlsx"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - Project Overdrafts xlsx"),
    #"Project Overdrafts_Sheet" = #"Imported Excel Workbook"{[Item="Project Overdrafts",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Project Overdrafts_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Project Code", type text}, {"Project Name", type text}, {"OD", Percentage.Type}, {"Discounted price (%)", Percentage.Type}})
in
    #"Changed Type"
```


## Table: SRC_Team


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 APS - Team - without birthday xlsx" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/",Name="2023-01-01 APS - Team - without birthday.xlsx"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 APS - Team - without birthday xlsx"),
    Team_Sheet = #"Imported Excel Workbook"{[Item="Team",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Team_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"M-Nummer", type text}, {"Vorname", type text}, {"Name", type text}, {"Rolle", type text}, {"Level", type text}, {"Rank", Int64.Type}, {"Level (Pyramid)", type text}, {"Firma", type text}, {"Team", type text}, {"Büro", type text}, {"Mentor", type text}, {"Status", type text}, {"Letzter Eintritt", type date}, {"Austritt", type date}, {"Wiederstart", type date}, {"Concat1", type text}, {"Concat2", type text}, {"Concat3", type text}, {"M-Nummer Lookup", type text}, {"RB Level", type text}, {"Company", type text}, {"Fallback M-Nummer", type text}, {"Fallback Role", type text}, {"Fallback Company", type text}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Changed Type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
in
    #"Removed Blank Rows"
```


## Table: SRC_Budget


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - NFR Budget xlsx" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/",Name="2023-01-01 NFR Forecast - NFR Budget.xlsx"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - NFR Budget xlsx"),
    #"NFR Budget_Sheet" = #"Imported Excel Workbook"{[Item="NFR Budget",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"NFR Budget_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Year", Int64.Type}, {"Month", Int64.Type}, {"Year-Month", type text}, {"NFR Budget", type number}, {"NFR SAP", type number}})
in
    #"Changed Type"
```


## Table: SRC_ProjectTypes


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - Project Types xlsx" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/",Name="2023-01-01 NFR Forecast - Project Types.xlsx"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - Project Types xlsx"),
    #"Project Types_Sheet" = #"Imported Excel Workbook"{[Item="Project Types",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Project Types_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Subitem.projectType", type text}, {"Availability", type text}, {"Billable", type text}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Changed Type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
in
    #"Removed Blank Rows"
```


## Table: SRC_NFR_Expected


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - NFR Real xlsx" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/",Name="2023-01-01 NFR Forecast - NFR Real.xlsx"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - NFR Real xlsx"),
    #"NFR Budget_Sheet" = #"Imported Excel Workbook"{[Item="NFR Budget",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"NFR Budget_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Year", Int64.Type}, {"Month", Int64.Type}, {"Year-Month", type text}, {"Person (SAP)", type text}, {"Person (APS)", type text}, {"NFR Real", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"NFR Real", "NFR Expected"}})
in
    #"Renamed Columns"
```


## Table: SRC_YearMonth


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - NFR Budget xlsx" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/",Name="2023-01-01 NFR Forecast - NFR Budget.xlsx"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - NFR Budget xlsx"),
    #"NFR Budget_Sheet" = #"Imported Excel Workbook"{[Item="NFR Budget",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"NFR Budget_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Year", Int64.Type}, {"Month", Int64.Type}, {"Year-Month", type text}, {"NFR Budget", type number}, {"NFR SAP", type number}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{ "Month", "NFR Budget", "NFR SAP"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"Year-Month"}, SRC_NFR_Actuals, {"Year-Month"}, "SRC_History", JoinKind.LeftOuter),
    #"Expanded SRC_History" = Table.ExpandTableColumn(#"Merged Queries", "SRC_History", {"NFR History"}, {"NFR History"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Expanded SRC_History",{"NFR History"})
in
    #"Removed Columns1"
```


## Table: SRC_NFR_Actuals


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/"),
    #"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - NFR Budget xlsx" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-01-nfrdashboard/",Name="2023-06-15 NFR Forecast - NFR History.xlsx"]}[Content],
    #"Imported Excel Workbook" = Excel.Workbook(#"https://powerbistoragesawprodv1 dfs core windows net/2023-01-nfrdashboard/_2023-01-01 NFR Forecast - NFR Budget xlsx"),
    #"NFR History_Sheet" = #"Imported Excel Workbook"{[Item="NFR History",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"NFR History_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Year", Int64.Type}, {"Month", Int64.Type}, {"Year-Month", type text}, {"NFR History", type number}, {"NFR SAP", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"NFR History", "NFR Actuals"}})
in
    #"Renamed Columns"
```


## Table: PREP_NFR_Projection_Aggregated


```m
let
    Source = Table.Combine({SRC_Subitems}),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Subitem.person] <> "")),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"Subitem.projectCode"}, SRC_OD, {"Project Code"}, "Project Overdrafts", JoinKind.LeftOuter),
    #"Expanded Project Overdrafts" = Table.ExpandTableColumn(#"Merged Queries", "Project Overdrafts", {"OD", "Discounted price (%)"}, {"Project Overdrafts.OD", "Project Overdrafts.Discounted price (%)"}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded Project Overdrafts", {"Subitem.person"}, SRC_Team, {"Concat3"}, "Team", JoinKind.LeftOuter),
    #"Expanded Team" = Table.ExpandTableColumn(#"Merged Queries1", "Team", {"M-Nummer", "Vorname", "Name", "Rolle", "Firma", "Team", "Status"}, {"Team.M-Nummer", "Team.Vorname", "Team.Name", "Team.Rolle", "Team.Firma", "Team.Team", "Team.Status"}),
    #"Merged Queries2" = Table.NestedJoin(#"Expanded Team", {"Team.Rolle"}, SRC_DailyRates, {"Level"}, "Daily", JoinKind.LeftOuter),
    #"Expanded Daily" = Table.ExpandTableColumn(#"Merged Queries2", "Daily", {"Daily NFR"}, {"Daily.Daily NFR"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Daily", "NFR", each [Subitem.days]*[Daily.Daily NFR]),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"NFR"}),
    #"Added Custom1" = Table.AddColumn(#"Removed Columns", "NFR", each [Subitem.days]*[#"Project Overdrafts.Discounted price (%)"]*[Daily.Daily NFR]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom1",{{"NFR", type number}}),
    #"Merged Queries3" = Table.NestedJoin(#"Changed Type", {"Subitem.projectType"}, SRC_ProjectTypes, {"Subitem.projectType"}, "SRC_ProjectTypes", JoinKind.LeftOuter),
    #"Expanded SRC_ProjectTypes" = Table.ExpandTableColumn(#"Merged Queries3", "SRC_ProjectTypes", {"Availability", "Billable"}, {"SRC_ProjectTypes.Availability", "SRC_ProjectTypes.Billable"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded SRC_ProjectTypes",{{"SRC_ProjectTypes.Availability", "ProjectTypes.Availability"}, {"SRC_ProjectTypes.Billable", "ProjectTypes.Billable"}}),
    #"Added Custom2" = Table.AddColumn(#"Renamed Columns", "Subitem.projectTimelineStart", each Text.Range([Subitem.projectTimeline],0,4) & "-" &Text.Range([Subitem.projectTimeline],5,2)& "-" &Text.Range([Subitem.projectTimeline],8,2)),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Added Custom2", {{"Subitem.projectTimelineStart", ""}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Errors",{{"Subitem.projectTimelineStart", type date}}),
    #"Added Custom3" = Table.AddColumn(#"Changed Type1", "Subitem.projectTimelineEnd", each Text.Range([Subitem.projectTimeline],11,4) & "-" &Text.Range([Subitem.projectTimeline],16,2)& "-" &Text.Range([Subitem.projectTimeline],19,2)),
    #"Replaced Errors1" = Table.ReplaceErrorValues(#"Added Custom3", {{"Subitem.projectTimelineEnd", ""}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Replaced Errors1",{{"Subitem.projectTimelineEnd", type date}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type2",{{"NFR", "NFR Plan"}}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Renamed Columns1", "Subitem.projectYearWeek", each Number.ToText([Subitem.projectYear])&"-"&Text.End("0"&Number.ToText(Date.WeekOfYear([Subitem.projectTimelineStart])-1),2)),
    #"Filtered Rows1" = Table.SelectRows(#"Hinzugefügte benutzerdefinierte Spalte", each ([Team.Team] = "APS DACH Consulting" or [Team.Team] = "APS DACH Management" or [Team.Team] = "APS Global" or [Team.Team] = "ONE DACH Consulting")),
    #"Grouped Rows" = Table.Group(#"Filtered Rows1", {"Subitem.projectYearMonth"}, {{"NFR Projection", each List.Sum([NFR Plan]), type nullable number}}),
    #"Sorted Rows" = Table.Sort(#"Grouped Rows",{{"Subitem.projectYearMonth", Order.Ascending}}),
    #"Renamed Columns2" = Table.RenameColumns(#"Sorted Rows",{{"NFR Projection", "NFR Projection"}})
in
    #"Renamed Columns2"
```


## Table: PREP_NFR_Target_Aggregated


```m
let
    Source = Table.NestedJoin(SRC_YearMonth, {"Year-Month"}, SRC_NFR_Actuals, {"Year-Month"}, "SRC_History", JoinKind.LeftOuter),
    #"Expanded SRC_History" = Table.ExpandTableColumn(Source, "SRC_History", {"Year", "Month", "Year-Month", "NFR History", "NFR SAP"}, {"SRC_History.Year", "SRC_History.Month", "SRC_History.Year-Month", "SRC_History.NFR History", "SRC_History.NFR SAP"}),
    #"Merged Queries" = Table.NestedJoin(#"Expanded SRC_History", {"Year-Month"}, PREP_NFR_Projection_Aggregated, {"Subitem.projectYearMonth"}, "PREP_NFR (2)", JoinKind.LeftOuter),
    #"Expanded PREP_NFR (2)" = Table.ExpandTableColumn(#"Merged Queries", "PREP_NFR (2)", {"Subitem.projectYearMonth", "NFR Projection"}, {"PREP_NFR (2).Subitem.projectYearMonth", "PREP_NFR (2).NFR Projection"}),
    #"Sorted Rows" = Table.Sort(#"Expanded PREP_NFR (2)",{{"Year-Month", Order.Ascending}}),
    #"Merged Queries1" = Table.NestedJoin(#"Sorted Rows", {"Year-Month"}, SRC_Budget, {"Year-Month"}, "SRC_Budget", JoinKind.LeftOuter),
    #"Expanded SRC_Budget" = Table.ExpandTableColumn(#"Merged Queries1", "SRC_Budget", {"Year", "Month", "Year-Month", "NFR Budget", "NFR SAP"}, {"SRC_Budget.Year", "SRC_Budget.Month", "SRC_Budget.Year-Month", "SRC_Budget.NFR Budget", "SRC_Budget.NFR SAP"}),
    #"Added Custom" = Table.AddColumn(#"Expanded SRC_Budget", "Combined Curve", each DateTime.LocalNow),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"Combined Curve"}),
    #"Removed Top Rows" = Table.Skip(#"Removed Columns",12),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Top Rows",{{"SRC_Budget.NFR Budget", "NFR Budget"}, {"PREP_NFR (2).NFR Projection", "PREP_NFR.NFR Projection"}, {"SRC_History.Month", "SRC_Actuals.Month"}, {"SRC_History.NFR History", "SRC_Actuals.NFR Actuals"}, {"SRC_History.NFR SAP", "SRC_Actuals.NFR SAP"}, {"SRC_History.Year", "SRC_Actuals.Year"}, {"SRC_History.Year-Month", "SRC_Actuals.Year-Month"}, {"PREP_NFR (2).Subitem.projectYearMonth", "PREP_NFR.Subitem.projectYearMonth"}}),
    #"Merged Queries2" = Table.NestedJoin(#"Renamed Columns", {"Year-Month"}, SRC_NFR_Actuals, {"Year-Month"}, "SRC_NFR_Actuals", JoinKind.LeftOuter),
    #"Expanded SRC_NFR_Actuals" = Table.ExpandTableColumn(#"Merged Queries2", "SRC_NFR_Actuals", {"NFR Actuals"}, {"SRC_NFR_Actuals.NFR Actuals"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Expanded SRC_NFR_Actuals",{"SRC_Actuals.NFR Actuals"})
in
    #"Removed Columns1"
```


## Parameter: Parameter1


```m
#"Sample File" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File", Type="Binary", IsParameterQueryRequired=true]
```

