



# M Code

|Dataset|[SAP ByD Status Reporting V2](./../SAP-ByD-Status-Reporting-V2.md)|
| :--- | :--- |
|Workspace|[SAP Business ByDesign](../../Workspaces/SAP-Business-ByDesign.md)|

## Table: Status Report


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/SAPBusinessByDesign-ProjectManagement", [ApiVersion = 15]),
    #"1ffdb220-1c72-4d55-8718-79319eecb32e" = Source{[Id="1ffdb220-1c72-4d55-8718-79319eecb32e"]}[Items],
    #"Removed Columns" = Table.RemoveColumns(#"1ffdb220-1c72-4d55-8718-79319eecb32e",{"FileSystemObjectType", "ServerRedirectedEmbedUri", "ServerRedirectedEmbedUrl", "ContentTypeId", "Title", "ComplianceAssetId", "Modified", "Created", "AuthorId", "EditorId", "OData__UIVersionString", "Attachments", "GUID", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "FieldValuesAsText", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions", "Rollout Project", "Author", "Editor", "ID"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns", "H_TOTAL", each [Total Hours Fit_x002]+[Total Hours Realize]+[Total Hours Verify]+[Total Hours Accept]+[Total Hours Cutover]+[Total Hours Hypercar]+[Total Hours Project_], type number),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Date", type date}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type", {"Rollout ProjectId"}, #"Rollout Projects", {"ROLLOUT_PROJECT_ID"}, "Rollout Projects", JoinKind.LeftOuter),
    #"Expanded Rollout Projects" = Table.ExpandTableColumn(#"Merged Queries", "Rollout Projects", {"DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "H_TOTAL_ROLLOUT_BUDGET"}, {"DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "H_TOTAL_ROLLOUT_BUDGET"}),
    #"Added Custom1" = Table.AddColumn(#"Expanded Rollout Projects", "PERCENT_PROJECT_PROGRESS", each ([Date]-[DATE_ROLLOUT_START])/([DATE_ROLLOUT_END]-[DATE_ROLLOUT_START]), Percentage.Type),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "H_CURRENT_PLAN", each [H_TOTAL_ROLLOUT_BUDGET]*[PERCENT_PROJECT_PROGRESS], type number),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom2",{{"Id", "STATUS_REPORT_ID"}, {"Date", "DATE_STATUS_REPORT"}, {"Rollout ProjectId", "ROLLOUT_PROJECT_ID"}, {"Total Hours Fit_x002", "H_FITGAP"}, {"Total Hours Realize", "H_REALIZE"}, {"Total Hours Verify", "H_VERIFY"}, {"Total Hours Accept", "H_ACCEPT"}, {"Total Hours Cutover", "H_CUTOVER"}, {"Total Hours Hypercar", "H_HYPERCARE"}, {"Total Hours Project_", "H_PROJECTMANAGEMENT"}, {"Deliverable Status F", "STATUS_1-FGA"}, {"Deliverable Status F0", "STATUS_2-FGA"}, {"Deliverable Status R", "STATUS_1-REA"}, {"Deliverable Status R0", "STATUS_2-REA"}, {"Deliverable Status R1", "STATUS_3-REA"}, {"Deliverable Status R2", "STATUS_4-REA"}, {"Deliverable Status V", "STATUS_1-VER"}, {"Deliverable Status V0", "STATUS_2-VER"}, {"Deliverable Status A", "STATUS_1-ACC"}, {"Deliverable Status A0", "STATUS_2-ACC"}, {"Deliverable Status A1", "STATUS_3-ACC"}, {"Deliverable Status C", "STATUS_1-CUT"}, {"Deliverable Status C0", "STATUS_2-CUT"}, {"Deliverable Status C1", "STATUS_3-CUT"}, {"Deliverable Status C2", "STATUS_4-CUT"}, {"Recent Achievements", "HTML_ACHIEVEMENTS"}, {"Decisions", "HTML_DECISIONS"}, {"Next Steps", "HTML_NEXTSTEPS"}, {"Manual Status Budget", "STATUS_BUDGET"}, {"Manual Status Time", "STATUS_TIME"}, {"Manual Status Qualit", "STATUS_QUALITY"}, {"Risks", "HTML_RISKS"}, {"Manual Overall Statu", "STATUS_OVERALL"}, {"TotalHoursOther", "H_OTHER"}, {"Deliverable Status C3", "STATUS_5-CUT"}, {"DeliverableStatusFGA-3", "STATUS_3-FGA"}, {"DeliverableStatusFGA-4", "STATUS_4-FGA"}, {"DeliverableStatusFGA-5", "STATUS_5-FGA"}, {"Deliverable FGA-6", "STATUS_6-FGA"}, {"Deliverable FGA-7", "STATUS_7-FGA"}, {"H_CURRENT_PLAN", "H_ROLLOUT_CURRENT_PLAN"}, {"H_TOTAL", "H_ROLLOUT_CURRENT_ACTUAL"}}),
    #"Added Custom3" = Table.AddColumn(#"Renamed Columns", "H_ROLLOUT_REMAINING", each [H_TOTAL_ROLLOUT_BUDGET]-[H_ROLLOUT_CURRENT_ACTUAL]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom3",{{"H_ROLLOUT_REMAINING", type number}})
in
    #"Changed Type1"
```


## Table: Phase Plans


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/SAPBusinessByDesign-ProjectManagement", [ApiVersion = 15]),
    #"183195cd-e50c-48e7-88f2-b438094d18ae" = Source{[Id="183195cd-e50c-48e7-88f2-b438094d18ae"]}[Items],
    #"Expanded Rollout Project" = Table.ExpandRecordColumn(#"183195cd-e50c-48e7-88f2-b438094d18ae", "Rollout Project", {"t8mx", "jfym"}, {"Rollout Project.t8mx", "Rollout Project.jfym"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded Rollout Project",{"FileSystemObjectType", "ServerRedirectedEmbedUri", "ServerRedirectedEmbedUrl", "ContentTypeId", "Title", "ComplianceAssetId", "Modified", "Created", "AuthorId", "EditorId", "OData__UIVersionString", "Attachments", "GUID", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "FieldValuesAsText", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions",  "Project Phase", "Author", "Editor", "ID"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns", "PHASE_PASSED", each if Date.From([Start Date]) <= Date.From(DateTime.LocalNow()) then true else false),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Start Date", type date}, {"End Date", type date}, {"ActualEnd", type date}, {"Rollout Project.t8mx", type date}, {"Rollout Project.jfym", type date}, {"Duration in weeks", type number}, {"Duration", type number}, {"Budget in h", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Id", "PLANNING_ID"}, {"Rollout ProjectId", "ROLLOUT_PROJECT_ID"}, {"Project PhaseId", "ROLLOUT_PHASE_ID"}, {"Start Date", "DATE_PHASE_PLANNED_START"}, {"End Date", "DATE_PHASE_PLANNED_END"}, {"Budget in h", "H_PHASE_BUDGET"}, {"ActualEnd", "DATE_PHASE_ACTUAL_END"}, {"Duration", "DURATION_DAYS_IN_PHASE"}, {"Duration in weeks", "DURATION_WEEKS_IN_PHASE"}, {"Rollout Project.t8mx", "DATE_ROLLOUT_START"}, {"Rollout Project.jfym", "DATE_ROLLOUT_END"}})
in
    #"Renamed Columns"
```


## Table: Rollout Projects


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/SAPBusinessByDesign-ProjectManagement", [ApiVersion = 15]),
    #"9a56b55f-46d7-4ec5-af32-eb26ccb90434" = Source{[Id="9a56b55f-46d7-4ec5-af32-eb26ccb90434"]}[Items],
    #"Removed Columns" = Table.RemoveColumns(#"9a56b55f-46d7-4ec5-af32-eb26ccb90434",{"FileSystemObjectType", "ServerRedirectedEmbedUri", "ServerRedirectedEmbedUrl", "ContentTypeId", "ComplianceAssetId", "ID", "Modified", "Created", "AuthorId", "EditorId", "OData__UIVersionString", "Attachments", "GUID", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "FieldValuesAsText", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions", "Responsible Partner", "Author", "Editor", "Responsible PartnerId", "ProjectLead", "ProjectLeadId", "ProjectLeadStringId"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"Id"}, #"HIDDEN Total Budget", {"ROLLOUT_PROJECT_ID"}, "TMP Rollout Totals", JoinKind.LeftOuter),
    #"Expanded TMP Rollout Totals" = Table.ExpandTableColumn(#"Merged Queries", "TMP Rollout Totals", {"H_ROLLOUT_BUDGET"}, {"TMP Rollout Totals.H_ROLLOUT_BUDGET"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded TMP Rollout Totals", each ([RolloutStatus] <> "1-Planned")),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"t8mx", type date}, {"jfym", type date}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "DURATION_DAYS", each Number.From([jfym]-[t8mx])),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "DURATION_CURRENT", each if Number.From(Date.From(DateTime.LocalNow()) - [t8mx]) > [DURATION_DAYS] then [DURATION_DAYS] else Number.From(Date.From(DateTime.LocalNow()) - [t8mx])),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom1",{{"Id", "ROLLOUT_PROJECT_ID"}, {"Title", "ROLLOUT_PROJECT_TITLE"}, {"t8mx", "DATE_ROLLOUT_START"}, {"jfym", "DATE_ROLLOUT_END"}, {"RolloutStatus", "STATUS_ROLLOUT"}, {"Wave", "WAVE"}, {"TMP Rollout Totals.H_ROLLOUT_BUDGET", "H_TOTAL_ROLLOUT_BUDGET"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"DURATION_DAYS", type number}, {"DURATION_CURRENT", type number}})
in
    #"Changed Type1"
```


## Table: Project Phases


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/SAPBusinessByDesign-ProjectManagement", [ApiVersion = 15]),
    #"f0a6d657-1669-4492-8b34-f570fc861cd7" = Source{[Id="f0a6d657-1669-4492-8b34-f570fc861cd7"]}[Items],
    #"Removed Columns" = Table.RemoveColumns(#"f0a6d657-1669-4492-8b34-f570fc861cd7",{"FileSystemObjectType", "ServerRedirectedEmbedUri", "ServerRedirectedEmbedUrl", "ContentTypeId", "ComplianceAssetId", "ID", "Modified", "Created", "AuthorId", "EditorId", "FieldValuesAsText", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions", "TaxCatchAll", "Author", "Editor", "GUID", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "OData__UIVersionString", "Attachments"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Id", "PROJECT_PHASE_ID"}, {"Title", "PROJECT_PHASE_TITLE"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","0-ProjectManagement","7-ProjectManagement",Replacer.ReplaceText,{"PROJECT_PHASE_TITLE"})
in
    #"Replaced Value"
```


## Table: Deliverables


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/SAPBusinessByDesign", [ApiVersion = 15]),
    #"43198703-d9db-4e7d-9a6c-cbc53d5cd038" = Source{[Id="43198703-d9db-4e7d-9a6c-cbc53d5cd038"]}[Items],
    #"Removed Columns" = Table.RemoveColumns(#"43198703-d9db-4e7d-9a6c-cbc53d5cd038",{"FileSystemObjectType", "ServerRedirectedEmbedUri", "ServerRedirectedEmbedUrl", "ContentTypeId", "ComplianceAssetId", "ID", "Modified", "Created", "AuthorId", "EditorId", "OData__UIVersionString", "Attachments", "GUID", "FirstUniqueAncestorSecurableObject", "RoleAssignments", "AttachmentFiles", "ContentType", "GetDlpPolicyTip", "FieldValuesAsHtml", "FieldValuesAsText", "FieldValuesForEdit", "File", "Folder", "LikedByInformation", "ParentList", "Properties", "Versions", "Author", "Editor"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Phase", "ROLLOUT_PHASE_TITLE"}, {"Id", "ITEM_ID"}, {"Title", "DELIVERABLE_TITLE"}, {"Input", "DELIVERABLE_INPUT"}, {"Output", "DELIVERABLE_OUTPUT"}, {"DeliverableID", "DELIVERABLE_ID"}}),
    #"Sorted Rows" = Table.Sort(#"Renamed Columns",{{"ROLLOUT_PHASE_TITLE", Order.Ascending}, {"DELIVERABLE_ID", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: TMP Status Report - Traffic Lights


```m
let
    Source = #"Status Report",
    #"Removed Columns" = Table.RemoveColumns(Source,{"H_FITGAP", "H_REALIZE", "H_VERIFY", "H_ACCEPT", "H_CUTOVER", "H_HYPERCARE", "H_PROJECTMANAGEMENT","H_ROLLOUT_REMAINING", "STATUS_1-FGA", "STATUS_2-FGA", "STATUS_1-REA", "STATUS_2-REA", "STATUS_3-REA", "STATUS_4-REA", "STATUS_1-VER", "STATUS_2-VER", "STATUS_1-ACC", "STATUS_2-ACC", "STATUS_3-ACC", "STATUS_1-CUT", "STATUS_2-CUT", "STATUS_3-CUT", "STATUS_4-CUT", "HTML_ACHIEVEMENTS", "HTML_DECISIONS", "HTML_NEXTSTEPS", "HTML_RISKS", "H_OTHER", "STATUS_5-CUT", "STATUS_3-FGA", "STATUS_4-FGA", "STATUS_5-FGA", "STATUS_6-FGA", "STATUS_7-FGA", "PERCENT_PROJECT_PROGRESS", "H_ROLLOUT_CURRENT_ACTUAL", "DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "H_TOTAL_ROLLOUT_BUDGET", "H_ROLLOUT_CURRENT_PLAN", "DATE_STATUS_REPORT", "ROLLOUT_PROJECT_ID"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"STATUS_REPORT_ID"}, "Attribute", "Value"),
    #"Replaced Value6" = Table.ReplaceValue(#"Unpivoted Columns","Yellow","2",Replacer.ReplaceText,{"Value"}),
    #"Replaced Value" = Table.ReplaceValue(#"Replaced Value6","Green","1",Replacer.ReplaceText,{"Value"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value","Red","3",Replacer.ReplaceText,{"Value"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value7","STATUS_BUDGET","2-Budget",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","STATUS_TIME","3-Time",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","STATUS_QUALITY","4-Quality",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","STATUS_OVERALL","1-Overall",Replacer.ReplaceText,{"Attribute"}),
    #"Renamed Columns" = Table.RenameColumns(#"Replaced Value4",{{"Attribute", "DIMENSION"}, {"Value", "VALUE"}})
in
    #"Renamed Columns"
```


## Table: TMP Status Report - Budget


```m
let
    Source = #"Status Report",
    #"Removed Columns" = Table.RemoveColumns(Source,{"STATUS_1-FGA", "STATUS_2-FGA", "STATUS_1-REA", "STATUS_2-REA", "STATUS_3-REA", "STATUS_4-REA", "STATUS_1-VER", "STATUS_2-VER", "STATUS_1-ACC", "H_ROLLOUT_REMAINING", "STATUS_2-ACC", "STATUS_3-ACC", "STATUS_1-CUT", "STATUS_2-CUT", "STATUS_3-CUT", "STATUS_4-CUT", "HTML_ACHIEVEMENTS", "HTML_DECISIONS", "HTML_NEXTSTEPS", "STATUS_BUDGET", "STATUS_TIME", "STATUS_QUALITY", "HTML_RISKS", "STATUS_OVERALL", "STATUS_5-CUT", "STATUS_3-FGA", "STATUS_4-FGA", "STATUS_5-FGA", "STATUS_6-FGA", "STATUS_7-FGA", "H_ROLLOUT_CURRENT_ACTUAL", "DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "PERCENT_PROJECT_PROGRESS", "H_TOTAL_ROLLOUT_BUDGET", "H_ROLLOUT_CURRENT_PLAN"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"STATUS_REPORT_ID", "DATE_STATUS_REPORT", "ROLLOUT_PROJECT_ID"}, "Attribute", "Value"),
    #"Replaced Value" = Table.ReplaceValue(#"Unpivoted Columns","H_FITGAP","1-FitGap",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","H_REALIZE","2-Realize",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","H_VERIFY","3-Verify",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","H_ACCEPT","4-Acceptance",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","H_CUTOVER","5-Cutover",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","H_HYPERCARE","6-Hypercare",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5", "H_PROJECTMANAGEMENT","7-ProjectManagement",Replacer.ReplaceText,{"Attribute"}),
    #"Replaced Value8" = Table.ReplaceValue(#"Replaced Value6","H_OTHER","8-Other",Replacer.ReplaceText,{"Attribute"}),
    #"Merged Queries" = Table.NestedJoin(#"Replaced Value8", {"Attribute"}, #"Project Phases", {"PROJECT_PHASE_TITLE"}, "Project Phases", JoinKind.LeftOuter),
    #"Expanded Project Phases" = Table.ExpandTableColumn(#"Merged Queries", "Project Phases", {"PROJECT_PHASE_ID"}, {"PROJECT_PHASE_ID"}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded Project Phases", {"ROLLOUT_PROJECT_ID", "PROJECT_PHASE_ID"}, #"Phase Plans", {"ROLLOUT_PROJECT_ID", "ROLLOUT_PHASE_ID"}, "Project Planning Parameters", JoinKind.LeftOuter),
    #"Expanded Project Planning Parameters" = Table.ExpandTableColumn(#"Merged Queries1", "Project Planning Parameters", {"H_PHASE_BUDGET"}, {"H_PHASE_BUDGET"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Expanded Project Planning Parameters",null,0,Replacer.ReplaceValue,{"H_PHASE_BUDGET"}),
    #"Added Custom" = Table.AddColumn(#"Replaced Value7", "H_BUDGET_DELTA", each [H_PHASE_BUDGET] - [Value]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "SORT_ORDER", each Text.At([Attribute],0)),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom1",{{"H_BUDGET_DELTA", type number}}),
    #"Added Custom2" = Table.AddColumn(#"Changed Type1", "PERCENTAGE_BUDGET_CONSUMPTION", each if [H_PHASE_BUDGET] = 0 then 1 else [Value]/[H_PHASE_BUDGET]),
    #"Merged Queries2" = Table.NestedJoin(#"Added Custom2", {"ROLLOUT_PROJECT_ID"}, #"Rollout Projects", {"ROLLOUT_PROJECT_ID"}, "Rollout Projects", JoinKind.LeftOuter),
    #"Expanded Rollout Projects" = Table.ExpandTableColumn(#"Merged Queries2", "Rollout Projects", {"DATE_ROLLOUT_START", "DATE_ROLLOUT_END"}, {"DATE_ROLLOUT_START", "DATE_ROLLOUT_END"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Rollout Projects",{{"Value", type number}, {"PERCENTAGE_BUDGET_CONSUMPTION", type number}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"STATUS_REPORT_ID", Order.Descending}, {"Attribute", Order.Ascending}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Sorted Rows",{{"SORT_ORDER", type number}})
in
    #"Changed Type2"
```


## Table: TMP Phase Plans - Budget per Phase


```m
let
    Source = #"Phase Plans",
    #"Filtered Rows" = Table.SelectRows(Source, each ([PHASE_PASSED] = true)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"DATE_PHASE_ACTUAL_END", "DURATION_WEEKS_IN_PHASE", "DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "DURATION_DAYS_IN_PHASE",  "PHASE_PASSED", "PLANNING_ID"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"ROLLOUT_PROJECT_ID", "ROLLOUT_PHASE_ID"}, #"HIDDEN Actual Budget per Phase", {"ROLLOUT_PROJECT_ID", "PHASE_ID"}, "TMP - Actual Budget per Phase", JoinKind.RightOuter),
    #"Expanded TMP - Actual Budget per Phase" = Table.ExpandTableColumn(#"Merged Queries", "TMP - Actual Budget per Phase", {"DATE_STATUS_REPORT", "STATUS_REPORT_ID", "Value"}, {"DATE_STATUS_REPORT", "STATUS_REPORT_ID", "Value"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Expanded TMP - Actual Budget per Phase",{"STATUS_REPORT_ID", "ROLLOUT_PROJECT_ID", "ROLLOUT_PHASE_ID", "H_PHASE_BUDGET", "Value"}),
    #"Sorted Rows" = Table.Sort(#"Reordered Columns",{{"STATUS_REPORT_ID", Order.Ascending}, {"ROLLOUT_PROJECT_ID", Order.Ascending}, {"ROLLOUT_PHASE_ID", Order.Ascending}}),
    #"Renamed Columns" = Table.RenameColumns(#"Sorted Rows",{{"Value", "H_PHASE_ACTUAL"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "PHASE_ACTIVE", each [DATE_PHASE_PLANNED_START] <= [DATE_STATUS_REPORT] and [DATE_PHASE_PLANNED_END] >= [DATE_STATUS_REPORT]),
    #"Filtered Rows1" = Table.SelectRows(#"Added Custom", each ([ROLLOUT_PROJECT_ID] <> null) and ([PHASE_ACTIVE] = true) and ([ROLLOUT_PHASE_ID] <> 7) and ([ROLLOUT_PHASE_ID] <> 8)),
    #"Added Custom1" = Table.AddColumn(#"Filtered Rows1", "H_PHASE_REMAINING", each [H_PHASE_BUDGET]-[H_PHASE_ACTUAL]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom1",{{"H_PHASE_REMAINING", type number}}),
    #"Sorted Rows1" = Table.Sort(#"Changed Type",{{"STATUS_REPORT_ID", Order.Ascending}})
in
    #"Sorted Rows1"
```


## Table: HIDDEN Total Budget


```m
let
    Source = #"Phase Plans",
    #"Grouped Rows" = Table.Group(Source, {"ROLLOUT_PROJECT_ID"}, {{"H_ROLLOUT_BUDGET", each List.Sum([H_PHASE_BUDGET]), type number}})
in
    #"Grouped Rows"
```


## Table: TMP Status Report - Deliverables


```m
let
    Source = #"Status Report",
    #"Removed Columns" = Table.RemoveColumns(Source,{"H_FITGAP", "H_REALIZE", "H_VERIFY", "H_ACCEPT", "H_CUTOVER", "H_HYPERCARE", "H_PROJECTMANAGEMENT","H_ROLLOUT_REMAINING", "HTML_ACHIEVEMENTS", "HTML_DECISIONS", "HTML_NEXTSTEPS", "STATUS_BUDGET", "STATUS_TIME", "STATUS_QUALITY", "HTML_RISKS", "STATUS_OVERALL", "H_OTHER", "H_ROLLOUT_CURRENT_ACTUAL", "DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "PERCENT_PROJECT_PROGRESS", "H_TOTAL_ROLLOUT_BUDGET", "H_ROLLOUT_CURRENT_PLAN", "DATE_STATUS_REPORT", "ROLLOUT_PROJECT_ID"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"STATUS_REPORT_ID"}, "Attribute", "Value"),
    #"Replaced Value" = Table.ReplaceValue(#"Unpivoted Columns","STATUS_","",Replacer.ReplaceText,{"Attribute"}),
    #"Renamed Columns" = Table.RenameColumns(#"Replaced Value",{{"Attribute", "Deliverable"}, {"Value", "Status"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Status", type number}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type", {"Deliverable"}, Deliverables, {"DELIVERABLE_ID"}, "Deliverables", JoinKind.LeftOuter),
    #"Expanded Deliverables" = Table.ExpandTableColumn(#"Merged Queries", "Deliverables", {"ROLLOUT_PHASE_TITLE"}, {"ROLLOUT_PHASE_TITLE"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Deliverables", "ROLLOUT_PHASE_ID", each Text.BeforeDelimiter([ROLLOUT_PHASE_TITLE], "-")),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{{"ROLLOUT_PHASE_ID", type number}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type1",{{"STATUS_REPORT_ID", Order.Ascending}, {"ROLLOUT_PHASE_ID", Order.Ascending}, {"Deliverable", Order.Ascending}}),
    #"Added Custom1" = Table.AddColumn(#"Sorted Rows", "DELIVERABLE_LEFT_ID", each Text.BeforeDelimiter([Deliverable], "-")),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "SORT_ORDER", each Text.From([ROLLOUT_PHASE_ID]) & "-" & Text.From([DELIVERABLE_LEFT_ID])),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom2",{{"SORT_ORDER", type text}}),
    #"Merged Queries1" = Table.NestedJoin(#"Changed Type2", {"STATUS_REPORT_ID"}, #"Status Report", {"STATUS_REPORT_ID"}, "Status Report", JoinKind.LeftOuter),
    #"Expanded Status Report" = Table.ExpandTableColumn(#"Merged Queries1", "Status Report", {"ROLLOUT_PROJECT_ID"}, {"ROLLOUT_PROJECT_ID"})
in
    #"Expanded Status Report"
```


## Table: TMP Phase Plans - Duration per Phase


```m
let
    Source = #"Phase Plans",
    #"Merged Queries" = Table.NestedJoin(Source, {"ROLLOUT_PROJECT_ID"}, #"Status Report", {"ROLLOUT_PROJECT_ID"}, "Status Report", JoinKind.LeftOuter),
    #"Expanded Status Report" = Table.ExpandTableColumn(#"Merged Queries", "Status Report", {"STATUS_REPORT_ID", "DATE_STATUS_REPORT"}, {"STATUS_REPORT_ID", "DATE_STATUS_REPORT"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Status Report", "PHASE_ACTIVE", each [DATE_PHASE_PLANNED_START] <= [DATE_STATUS_REPORT] and [DATE_PHASE_PLANNED_END] >= [DATE_STATUS_REPORT]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "DURATION_DAYS_CURRENT", each [DATE_STATUS_REPORT]-[DATE_PHASE_PLANNED_START]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom1",{{"PHASE_ACTIVE", type logical}, {"DURATION_DAYS_CURRENT", type number}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([PHASE_ACTIVE] = true)),
    #"Sorted Rows" = Table.Sort(#"Filtered Rows",{{"STATUS_REPORT_ID", Order.Ascending}}),
    #"Filtered Rows1" = Table.SelectRows(#"Sorted Rows", each ([ROLLOUT_PHASE_ID] <> 7 and [ROLLOUT_PHASE_ID] <> 8)),
    #"Reordered Columns" = Table.ReorderColumns(#"Filtered Rows1",{"PLANNING_ID", "ROLLOUT_PROJECT_ID", "ROLLOUT_PHASE_ID", "STATUS_REPORT_ID", "DATE_PHASE_PLANNED_START", "DATE_PHASE_PLANNED_END", "DATE_STATUS_REPORT", "H_PHASE_BUDGET", "DATE_PHASE_ACTUAL_END", "DURATION_DAYS_IN_PHASE", "DURATION_WEEKS_IN_PHASE", "DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "PHASE_PASSED", "PHASE_ACTIVE", "DURATION_DAYS_CURRENT"}),
    #"Added Custom2" = Table.AddColumn(#"Reordered Columns", "DURATION_REMAINING", each Number.From([DURATION_DAYS_IN_PHASE]-[DURATION_DAYS_CURRENT])),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom2",{{"DURATION_REMAINING", type number}}),
    #"Added Custom3" = Table.AddColumn(#"Changed Type1", "PERCENTAGE_PHASE_PROGRESS", each ([DATE_STATUS_REPORT]-[DATE_PHASE_PLANNED_START])/([DATE_PHASE_PLANNED_END]-[DATE_PHASE_PLANNED_START])),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom3",{{"PERCENTAGE_PHASE_PROGRESS", type number}}),
    #"Merged Queries1" = Table.NestedJoin(#"Changed Type2", {"ROLLOUT_PHASE_ID"}, #"Project Phases", {"PROJECT_PHASE_ID"}, "Project Phases", JoinKind.LeftOuter),
    #"Expanded Project Phases" = Table.ExpandTableColumn(#"Merged Queries1", "Project Phases", {"PROJECT_PHASE_TITLE"}, {"PROJECT_PHASE_TITLE"})
in
    #"Expanded Project Phases"
```


## Table: TMP Status Report Progress Rate


```m
let
    Source = #"TMP Status Report - Budget",
    #"Removed Columns" = Table.RemoveColumns(Source,{"SORT_ORDER", "DATE_ROLLOUT_START", "DATE_ROLLOUT_END"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns","1-FitGap","1-Fit-Gap",Replacer.ReplaceText,{"Attribute"}),
    #"Merged Queries" = Table.NestedJoin(#"Replaced Value", {"ROLLOUT_PROJECT_ID", "PROJECT_PHASE_ID"}, #"Phase Plans", {"ROLLOUT_PROJECT_ID", "ROLLOUT_PHASE_ID"}, "Phase Plans", JoinKind.LeftOuter),
    #"Expanded Phase Plans" = Table.ExpandTableColumn(#"Merged Queries", "Phase Plans", {"DATE_PHASE_PLANNED_START", "DATE_PHASE_PLANNED_END", "DURATION_DAYS_IN_PHASE"}, {"DATE_PHASE_PLANNED_START", "DATE_PHASE_PLANNED_END", "DURATION_DAYS_IN_PHASE"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Phase Plans", "PERCENTAGE_TIME_CONSUMPTION", each if [Attribute] = "8-Other" then null else if Number.From(([DATE_STATUS_REPORT]-[DATE_PHASE_PLANNED_START]) / ([DATE_PHASE_PLANNED_END]-[DATE_PHASE_PLANNED_START])) < 0 then 0 

else if Number.From(([DATE_STATUS_REPORT]-[DATE_PHASE_PLANNED_START]) / ([DATE_PHASE_PLANNED_END]-[DATE_PHASE_PLANNED_START])) > 1 then 1 else Number.From(([DATE_STATUS_REPORT]-[DATE_PHASE_PLANNED_START]) / ([DATE_PHASE_PLANNED_END]-[DATE_PHASE_PLANNED_START]))),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"PERCENTAGE_TIME_CONSUMPTION", type number}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Changed Type",{"Value", "PROJECT_PHASE_ID", "H_BUDGET_DELTA", "DATE_PHASE_PLANNED_START", "DATE_PHASE_PLANNED_END", "DURATION_DAYS_IN_PHASE"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns1", each [Attribute] <> "H_ROLLOUT_REMAINING"),
    #"Merged Queries1" = Table.NestedJoin(#"Filtered Rows", {"STATUS_REPORT_ID", "Attribute"}, #"HIDDEN Total Deliverable Status", {"STATUS_REPORT_ID", "ROLLOUT_PHASE_TITLE"}, "HIDDEN Total Deliverable Status", JoinKind.LeftOuter),
    #"Expanded HIDDEN Total Deliverable Status" = Table.ExpandTableColumn(#"Merged Queries1", "HIDDEN Total Deliverable Status", {"PERCENTAGE_DELIVERABLE_PROGRESS"}, {"PERCENTAGE_DELIVERABLE_PROGRESS"})
in
    #"Expanded HIDDEN Total Deliverable Status"
```


## Table: HIDDEN Total Deliverable Status


```m
let
    Source = #"TMP Status Report - Deliverables",
    #"Removed Columns" = Table.RemoveColumns(Source,{"Deliverable", "ROLLOUT_PHASE_ID", "DELIVERABLE_LEFT_ID", "SORT_ORDER", "ROLLOUT_PROJECT_ID"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Status", "STATUS"}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Renamed Columns",{"STATUS_REPORT_ID", "ROLLOUT_PHASE_TITLE", "STATUS"}),
    #"Grouped Rows" = Table.Group(#"Reordered Columns", {"STATUS_REPORT_ID", "ROLLOUT_PHASE_TITLE"}, {{"STATUS", each List.Average([STATUS]), type number}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Grouped Rows",{{"STATUS", "PERCENTAGE_DELIVERABLE_PROGRESS"}})
in
    #"Renamed Columns1"
```


## Table: TMPStatus Report -Current Duration


```m
let
    Source = #"Status Report",
    #"Removed Columns" = Table.RemoveColumns(Source,{"H_FITGAP", "H_REALIZE", "H_VERIFY", "H_ACCEPT", "H_CUTOVER", "H_HYPERCARE", "H_PROJECTMANAGEMENT", "STATUS_1-FGA", "STATUS_2-FGA", "STATUS_1-REA", "STATUS_2-REA", "STATUS_3-REA", "STATUS_4-REA", "STATUS_1-VER", "STATUS_2-VER", "STATUS_1-ACC", "STATUS_2-ACC", "STATUS_3-ACC", "STATUS_1-CUT", "STATUS_2-CUT", "STATUS_3-CUT", "STATUS_4-CUT", "HTML_ACHIEVEMENTS", "HTML_DECISIONS", "HTML_NEXTSTEPS", "STATUS_BUDGET", "STATUS_TIME", "STATUS_QUALITY", "HTML_RISKS", "STATUS_OVERALL", "H_OTHER", "STATUS_5-CUT", "STATUS_3-FGA", "STATUS_4-FGA", "STATUS_5-FGA", "STATUS_6-FGA", "STATUS_7-FGA", "H_ROLLOUT_CURRENT_ACTUAL", "DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "H_TOTAL_ROLLOUT_BUDGET", "PERCENT_PROJECT_PROGRESS", "H_ROLLOUT_CURRENT_PLAN", "H_ROLLOUT_REMAINING"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"ROLLOUT_PROJECT_ID"}, #"Rollout Projects", {"ROLLOUT_PROJECT_ID"}, "Rollout Projects", JoinKind.LeftOuter),
    #"Expanded Rollout Projects" = Table.ExpandTableColumn(#"Merged Queries", "Rollout Projects", {"DATE_ROLLOUT_START", "DATE_ROLLOUT_END"}, {"DATE_ROLLOUT_START", "DATE_ROLLOUT_END"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Rollout Projects", "DURATION_SINCE_START", each [DATE_STATUS_REPORT] - [DATE_ROLLOUT_START]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "DURATION_PROJECT_TOTAL", each [DATE_ROLLOUT_END]-[DATE_ROLLOUT_START]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom1",{{"DURATION_SINCE_START", type number}, {"DURATION_PROJECT_TOTAL", type number}}),
    #"Added Custom2" = Table.AddColumn(#"Changed Type", "DURATION_REMAINING", each [DURATION_PROJECT_TOTAL]-[DURATION_SINCE_START]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom2",{{"DURATION_REMAINING", type number}})
in
    #"Changed Type1"
```


## Table: HIDDEN Actual Budget per Phase


```m
let
    Source = #"Status Report",
    #"Removed Columns" = Table.RemoveColumns(Source,{  "STATUS_1-FGA", "STATUS_2-FGA", "STATUS_1-REA", "STATUS_2-REA", "STATUS_3-REA", "STATUS_4-REA", "STATUS_1-VER", "STATUS_2-VER", "STATUS_1-ACC", "STATUS_2-ACC", "STATUS_3-ACC", "STATUS_1-CUT", "STATUS_2-CUT", "STATUS_3-CUT", "STATUS_4-CUT", "HTML_ACHIEVEMENTS", "HTML_DECISIONS", "HTML_NEXTSTEPS", "STATUS_BUDGET", "STATUS_TIME", "STATUS_QUALITY", "HTML_RISKS", "STATUS_OVERALL", "STATUS_5-CUT", "STATUS_3-FGA", "STATUS_4-FGA", "STATUS_5-FGA", "STATUS_6-FGA", "STATUS_7-FGA", "H_ROLLOUT_CURRENT_ACTUAL", "DATE_ROLLOUT_START", "DATE_ROLLOUT_END", "H_TOTAL_ROLLOUT_BUDGET", "PERCENT_PROJECT_PROGRESS", "H_ROLLOUT_CURRENT_PLAN", "H_ROLLOUT_REMAINING"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"DATE_STATUS_REPORT", "ROLLOUT_PROJECT_ID", "STATUS_REPORT_ID"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Columns",{{"Attribute", "PHASE_ID"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","H_FITGAP","1",Replacer.ReplaceText,{"PHASE_ID"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","H_REALIZE","2",Replacer.ReplaceText,{"PHASE_ID"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","H_VERIFY","3",Replacer.ReplaceText,{"PHASE_ID"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","H_ACCEPT","4",Replacer.ReplaceText,{"PHASE_ID"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","H_CUTOVER","5",Replacer.ReplaceText,{"PHASE_ID"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","H_HYPERCARE","6",Replacer.ReplaceText,{"PHASE_ID"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5","H_PROJECTMANAGEMENT","7",Replacer.ReplaceText,{"PHASE_ID"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value6","H_OTHER","8",Replacer.ReplaceText,{"PHASE_ID"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Replaced Value7",{{"PHASE_ID", type number}, {"Value", type number}})
in
    #"Changed Type"
```


## Table: UPDATE_TIME


```m
let
    Source = DateTime.LocalNow()
in
    Source
```

