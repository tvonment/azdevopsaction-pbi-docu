



# M Code

|Dataset|[New Work Dashboard - Napta](./../New-Work-Dashboard---Napta.md)|
| :--- | :--- |
|Workspace|[New Work [Prod]](../../Workspaces/New-Work-[Prod].md)|

## Table: DailyTimeRecording


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TimeRecordingPilot", [Implementation="2.0", ViewMode="Default"]),
    #"a6b042c6-26b0-43c1-9237-a3d0e09a5d44" = Source{[Id="a6b042c6-26b0-43c1-9237-a3d0e09a5d44"]}[Items],
    #"Lowercased Text" = Table.TransformColumns(#"a6b042c6-26b0-43c1-9237-a3d0e09a5d44",{{"Mail", Text.Lower, type text}})
in
    #"Lowercased Text"
```


## Table: Q3 DidYouWorkLessThan12Hours


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TimeRecordingPilot", [Implementation="2.0", ViewMode="Default"]),
    #"0f1e5eac-451b-44dd-8594-6e93750f1559" = Source{[Id="0f1e5eac-451b-44dd-8594-6e93750f1559"]}[Items],
    #"Lowercased Text" = Table.TransformColumns(#"0f1e5eac-451b-44dd-8594-6e93750f1559",{{"Mail", Text.Lower, type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Lowercased Text", each [Reference Date] >= #datetime(2022, 2, 23, 0, 0, 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"ID", "Reference Date", "Mail", "Created", "Did you work less than 12 hours yesterday?"})
in
    #"Removed Other Columns"
```


## Table: Q2 DidYouWorkOnTheWeekend


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TimeRecordingPilot", [Implementation="2.0", ViewMode="Default"]),
    #"ef749ebb-530a-4d44-a9a6-76fc470b9a73" = Source{[Id="ef749ebb-530a-4d44-a9a6-76fc470b9a73"]}[Items],
    #"Lowercased Text" = Table.TransformColumns(#"ef749ebb-530a-4d44-a9a6-76fc470b9a73",{{"Mail", Text.Lower, type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Lowercased Text", each [Reference Date] >= #datetime(2022, 2, 23, 0, 0, 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"ID", "Reference Date", "Mail", "Created", "Was your last weekend and any holidays last week completely free of work?"})
in
    #"Removed Other Columns"
```


## Table: Q1 WereWorkingHoursWithinLimits


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TimeRecordingPilot", [Implementation="2.0", ViewMode="Default"]),
    #"b4b0c716-50f3-4256-ba3a-d06c5761d55d" = Source{[Id="b4b0c716-50f3-4256-ba3a-d06c5761d55d"]}[Items],
    #"Lowercased Text" = Table.TransformColumns(#"b4b0c716-50f3-4256-ba3a-d06c5761d55d",{{"Mail", Text.Lower, type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Lowercased Text", each [Reference Date] >= #datetime(2022, 2, 23, 0, 0, 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"ID", "Reference Date", "Mail", "Created", "Did your working hours this week stay within weekly limits?"})
in
    #"Removed Other Columns"
```


## Table: Q4 WorkloadNext2Weeks


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TimeRecordingPilot", [Implementation="2.0", ViewMode="Default"]),
    #"9823b883-727f-4d57-9235-eee3d66ff282" = Source{[Id="9823b883-727f-4d57-9235-eee3d66ff282"]}[Items],
    #"Lowercased Text" = Table.TransformColumns(#"9823b883-727f-4d57-9235-eee3d66ff282",{{"Mail", Text.Lower, type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Lowercased Text", each [Reference Date] >= #datetime(2022, 2, 23, 0, 0, 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"ID", "Reference Date", "Mail", "Created", "WeekAfterNextWeek", "NextWeek"})
in
    #"Removed Other Columns"
```


## Table: rep v_hr_employee


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_hr_employee = Source{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Lowercased Text" = Table.TransformColumns(rep_v_hr_employee,{{"email", Text.Lower, type text}}),
    #"Removed Other Columns" = Table.SelectColumns(#"Lowercased Text",{"emp_id", "full_name", "jobcode", "mentor_emp_id", "emp_status", "email", "country_code", "country", "platform_1_id", "platform_1_name", "cost_center", "full_name_display"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([emp_status] = "A") and ([email] <> null) and [email]<> "no_mail@rolandberger.com" and [email] <> "nomail@rolandberger.com"  ),
    #"Lowercased Text1" = Table.TransformColumns(#"Filtered Rows",{{"email", Text.Lower, type text}}),
    #"Removed Duplicates" = Table.Distinct(#"Lowercased Text1", {"email"})
    , res = Table.Buffer(#"Removed Duplicates"),
    #"Merged mentor practice_group" = Table.NestedJoin(res, {"mentor_emp_id"}, v_hr_mentor_to_practice_group, {"emp_id"}, "v_hr_mentor_to_practice_group", JoinKind.LeftOuter),
    #"Expanded v_hr_mentor_to_practice_group" = Table.ExpandTableColumn(#"Merged mentor practice_group", "v_hr_mentor_to_practice_group", {"practice_group"}, {"mentor_practice_group"}),
    practice_group = Table.AddColumn(#"Expanded v_hr_mentor_to_practice_group", "practice_group", each if [mentor_practice_group] = null and 
([country_code] = "DEU" or [country_code] = "AUT" or [country_code] = "CHE") then [cost_center] else [mentor_practice_group], type text),
    #"Replaced Value" = Table.ReplaceValue(practice_group, each [full_name], each [full_name_display] , Replacer.ReplaceText,{"full_name"}),
    #"Removed Columns" = Table.RemoveColumns(#"Replaced Value",{"full_name_display"})
in
    #"Removed Columns"
```


## Table: _Measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: FromIntervals


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlVw9FVIzEtRSE0syslMLVLSUTJUitWJVkpKTcsvSlUwB8oDxYzAYiCOQn6RQk5iCVilMVg0Lx9oQHE5WMREKTYWAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"From Interval" = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"From Interval", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```


## Table: EndIntervals


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WslAI8FVIzEtRSE0syslMLVLSUTJUitWJVspJLEktUijJSMxTAKkBihuBxQ0NYDrAKoDixhBxIwVHVHETsHhePlCwuBwsYqoUGwsA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"End Interval" = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"End Interval", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```


## Table: Participants


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TimeRecordingPilot", [Implementation="2.0", ViewMode="All"]),
    #"3a610a45-99a1-4582-b192-01b42c82383c" = Source{[Id="3a610a45-99a1-4582-b192-01b42c82383c"]}[Items],
    #"Removed Other Columns" = Table.SelectColumns(#"3a610a45-99a1-4582-b192-01b42c82383c",{"EMail", "Reference Date"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Other Columns",{{"Reference Date", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"EMail", "participant_email"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"participant_email", type text}}),
    #"Lowercased Text" = Table.TransformColumns(#"Changed Type",{{"participant_email", Text.Lower, type text}})
    , res = Table.Buffer(#"Lowercased Text")
in
    res
```


## Table: MatrixColumns


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("jZJfa8IwFMW/yqXPirbWP3sUN9jDGAQGexAZVW/XzDYpSYr67XdvTbe2SPHhFpJ7zq8nN9lug+dE5lcII8hAG8jR2mAUvCXWQQxnbU5SfcMxufJu6GtGNaUSs2A32gYvlxIPLnFSK0iJ4TKEtHKVQdIovDg4I54YEPmKPUjENeBTukyqWkVRcllIx+qSQ/BmyxF6ggiHnLyGPVIYjjD3nse87qxvef8BC3/mPoBUqI52kulc8ohAp2kv97JlY4SIBq3d4KvWyB4w30n+5J09wkdiSaUrZ+URoTT6hy6Q2q+6MhZsiYpX4dSHn/sSi4lYQi0axLxXxR4NpQKDttTKYv16mjl0cRtd0d8Ytz7wE6LGmKu57fHfR6y+wq6QO82A7ug2uihuRwGGNW9g4Yt0NI7dLw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Group = _t, Interval = _t, Sort = _t, IdInGroup = _t, GroupId = _t, GroupSortId = _t, Question = _t]),
    #"Changed Type1" = Table.TransformColumnTypes(Source,{{"GroupSortId", Int64.Type}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Changed Type1",{{"Group", type text}, {"Interval", type text}, {"Sort", Int64.Type}, {"IdInGroup", Int64.Type}, {"GroupId", Int64.Type}})
in
    #"Changed Type"
```


## Table: RefreshDate


```m
let
    Source = Date.From(DateTime.LocalNow()),
    #"Converted to Table" = #table(1, {{Source}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Converted to Table",{{"Column1", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "RefreshDate"}})
in
    #"Renamed Columns"
```


## Table: Mentors


```m
let
    Source = #"employees with data",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"mentor_emp_id"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Other Columns", each ([mentor_emp_id] <> " " and [mentor_emp_id] <> "" and [mentor_emp_id] <> null)),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows1"),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"mentor_emp_id"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee" = Table.ExpandTableColumn(#"Merged Queries", "rep v_hr_employee", {"full_name", "email"}, {"Mentor", "Mail"})
in
    #"Expanded rep v_hr_employee"
```


## Table: Projetcs


```m
let
    Source = v_new_work_dashboard_staffing,
    #"Filtered Rows" = Table.SelectRows(Source, each ([Status] = 1)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"ProjectName", "Client", "ProjectNumber", "ProjectEndDate", "EmployeeIDDM", "EmployeeIDPM"}),
    #"Appended Query" = Table.Combine({#"Removed Other Columns", #"No Project Assignment"}),
    #"Grouped Rows" = Table.Group(#"Appended Query", {"ProjectNumber"}, {{"ProjectName", each List.Max([ProjectName]), type nullable text}, {"Client", each List.Max([Client]), type nullable text}, {"ProjectEndDate", each List.Max([ProjectEndDate]), type nullable date}, {"EmployeeIDDM", each List.Max([EmployeeIDDM]), type nullable text}, {"EmployeeIDPM", each List.Max([EmployeeIDPM]), type nullable text}}),
    #"Removed Duplicates" = Table.Distinct(#"Grouped Rows"),
    #"Added Custom" = Table.AddColumn(#"Removed Duplicates", "Project", each [ProjectNumber] & " - " & [Client]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Project", type text}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type", {"EmployeeIDDM"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee" = Table.ExpandTableColumn(#"Merged Queries", "rep v_hr_employee", {"platform_1_name", "full_name"}, {"Platform", "DM"})
in
    #"Expanded rep v_hr_employee"
```


## Table: Staffing


```m
let
    Source = v_new_work_dashboard_staffing,
    #"Filtered Rows" = Table.SelectRows(Source, each ([Status] = 1)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"EmployeeID", "Subject", "StartDate", "EndDate", "DaysAssigned", "ProjectNumber", "StaffingInfo", "EmployeeIDDM", "EmployeeIDPM"})
in
    #"Removed Other Columns"
```


## Table: Q6 HoursSpentOutsideProjectWorkdays


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TimeRecordingPilot", [Implementation="2.0", ViewMode="Default"]),
    #"9823b883-727f-4d57-9235-eee3d66ff282" = Source{[Id="efc87ae6-64a2-4078-933c-71f4feddea53"]}[Items],
    #"Lowercased Text" = Table.TransformColumns(#"9823b883-727f-4d57-9235-eee3d66ff282",{{"Mail", Text.Lower, type text}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Lowercased Text",{{"Hours", type number}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each [Reference Date] >= #datetime(2022, 2, 23, 0, 0, 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"ID", "Hours", "Reference Date", "Mail", "Created"})
in
    #"Removed Other Columns"
```


## Table: Q7 HoursSpentOutsideProjectWeekend


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/TimeRecordingPilot", [Implementation="2.0", ViewMode="Default"]),
    #"9823b883-727f-4d57-9235-eee3d66ff282" = Source{[Id="76b281fd-9e40-418f-994b-f1bc7121eeff"]}[Items],
    #"Lowercased Text" = Table.TransformColumns(#"9823b883-727f-4d57-9235-eee3d66ff282",{{"Mail", Text.Lower, type text}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Lowercased Text",{{"Hours", type number}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each [Reference Date] >= #datetime(2022, 2, 23, 0, 0, 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"ID", "Hours", "Reference Date", "Mail", "Created"})
in
    #"Removed Other Columns"
```


## Table: Project2Employee


```m
let
    Source = Staffing,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"ProjectNumber", "EmployeeID"})
in
    #"Removed Other Columns"
```


## Table: rls country


```m
let
    Source = #"rep v_new_work_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "country"))
in
    #"Filtered Rows1"
```


## Table: Q3 12h States


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8s0vLsmpVKhMLVbSUTIEYmVzYydzM0OlWB2gZGZFagpQzAgk7ursbGFiBhGHaMrLB4obg+TcXMyMTF3Bcp55xaVpaZnJmal5JQopiSWJQHkTkBonYxAEq8nTB4magnWCgVJsLAA=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [State = _t, Sort = _t, StateColor = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"State", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```


## Table: StaffingRLS_DM


```m
let
    Source = StaffingRLSBase,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"EmployeeID", "EmployeeIDDM"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([EmployeeIDDM] <> "")),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows"),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"EmployeeIDDM"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee" = Table.ExpandTableColumn(#"Merged Queries", "rep v_hr_employee", {"email"}, {"email"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded rep v_hr_employee", each ([email] <> null))
in
    #"Filtered Rows1"
```


## Table: StaffingRLS_PM


```m
let
    Source = StaffingRLSBase,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"EmployeeIDPM", "EmployeeID"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each ([EmployeeIDPM] <> "")),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows"),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"EmployeeIDPM"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee" = Table.ExpandTableColumn(#"Merged Queries", "rep v_hr_employee", {"email"}, {"email"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded rep v_hr_employee", each ([email] <> null))
in
    #"Filtered Rows1"
```


## Table: Roles


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WcvFV0lFSitWJVgqAs3xT80ryi4A8QzDXMSU3Mw/Oc84vzSspqkTi5xWX5pQk5pXADcpJLEnLL8qFKwnIzMkvQWjIyQSarxuSmpiLbqh/Xg7U4FgA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Role = _t, CanSeeDetails = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Role", type text}, {"CanSeeDetails", Int64.Type}})
in
    #"Changed Type"
```


## Table: Q8 CounterActions


```m
let
    Source = #"Q8 CounterActions PROD",
    #"Lowercased Text" = Table.TransformColumns(#"Source",{{"Mail", Text.Lower, type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Lowercased Text", each [Reference Date] >= #datetime(2022, 2, 23, 0, 0, 0)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"Reference Date", "Mail", "Counteraction needed", "Comment", "ID"})
in
    #"Removed Other Columns"
```


## Table: FilterCounterAction


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WUlSK1YlWqlCKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [CA = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"CA", type text}})
in
    #"Changed Type"
```


## Table: ParticipantsAndStaffing


```m
let
    Source = Participants,
    #"Merged Queries" = Table.NestedJoin(Source, {"participant_email"}, #"rep v_hr_employee", {"email"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee" = Table.ExpandTableColumn(#"Merged Queries", "rep v_hr_employee", {"country", "country_code", "emp_id", "mentor_emp_id", "platform_1_id", "platform_1_name", "practice_group"}, {"country", "country_code", "emp_id", "mentor_emp_id", "platform_1_id", "platform_1_name", "practice_group"}),
    fnFilter = (_tbl as table, _date as date) =>
        let
            _filtered = Table.SelectRows(_tbl, each _date <= [EndDate] and _date >= [StartDate])
        in  _filtered,

    #"Merged Queries1" = Table.NestedJoin(#"Expanded rep v_hr_employee", {"emp_id"}, Staffing, {"EmployeeID"}, "Staffing", JoinKind.LeftOuter),

    #"Added Custom" = Table.AddColumn(#"Merged Queries1", "FilteredStaffing", each fnFilter([Staffing], [Reference Date] )),

     


    #"Expanded Staffing" = Table.ExpandTableColumn(#"Added Custom", "FilteredStaffing", {"StartDate", "EndDate", "ProjectNumber", "EmployeeIDDM", "EmployeeIDPM"}, {"StartDate", "EndDate", "ProjectNumber", "EmployeeIDDM", "EmployeeIDPM"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Staffing", each ([ProjectNumber] = null or (   [EndDate] >= [Reference Date] and [StartDate] <=[Reference Date])  )),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows",null,"no project assignment",Replacer.ReplaceValue,{"ProjectNumber"}),
    #"Merged Queries2" = Table.NestedJoin(#"Replaced Value", {"mentor_emp_id"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee1" = Table.ExpandTableColumn(#"Merged Queries2", "rep v_hr_employee", {"email"}, {"email_mentor"}),
    #"Merged Queries3" = Table.NestedJoin(#"Expanded rep v_hr_employee1", {"EmployeeIDDM"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee2" = Table.ExpandTableColumn(#"Merged Queries3", "rep v_hr_employee", {"email"}, {"email_dm"}),
    #"Merged Queries4" = Table.NestedJoin(#"Expanded rep v_hr_employee2", {"EmployeeIDPM"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee3" = Table.ExpandTableColumn(#"Merged Queries4", "rep v_hr_employee", {"email"}, {"email_pm"}),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Expanded rep v_hr_employee3", {"participant_email", "Reference Date"}, #"rls pilot group patricipants", {"participant_email", "reference_date"}, "rls pilot group patricipants", JoinKind.LeftOuter),
    #"Erweiterte rls pilot group patricipants" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "rls pilot group patricipants", {"participant_group"}, {"pilot_group"})
in
    #"Erweiterte rls pilot group patricipants"
```


## Table: rls pilot group permission


```m
let
    Quelle = #"rep v_new_work_dashboard_permission",
    #"Gefilterte Zeilen" = Table.SelectRows(Quelle, each ([user_role] = "pilot"))
in
    #"Gefilterte Zeilen"
```


## Table: rls platform


```m
let
    Source = #"rep v_new_work_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "platform"))
in
    #"Filtered Rows1"
```


## Table: rls clientteam


```m
let
    Source = #"rep v_new_work_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "clientteam"))
in
    #"Filtered Rows1"
```


## Table: StaffingAll


```m
let
    Source = v_new_work_dashboard_staffing,
    Custom1 = Table.SelectColumns(Source,{"EmployeeID", "Subject", "StartDate", "EndDate", "DaysAssigned", "ProjectNumber", "StaffingInfo", "EmployeeIDDM", "EmployeeIDPM"})
in
    Custom1
```


## Table: rls platform DACH


```m
let
    Source = #"rep v_new_work_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "platformDACH"))
in
    #"Filtered Rows1"
```


## Table: rls countryOnly


```m
let
    Source = #"rep v_new_work_dashboard_permission",
    #"Filtered Rows1" = Table.SelectRows(Source, each ([user_role] = "countryOnly"))
in
    #"Filtered Rows1"
```


## Table: WeeklyLimitRanges


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCs8sycjMUyhPTc3OqVTIyczNLClW0lEyVIrViVZyTMovS8WQMwLLuVaUFKXmpgIlErGqMgarystXSMwrLk8tAoqYKMXGAgA=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Range = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Range", type text}, {"Sort", Int64.Type}})
in
    #"Changed Type"
```


## Roles

### Admin


Model Permission: Read

Roles

```m
[Role] = "Admin"
```


### Country


Model Permission: Read

ParticipantsAndStaffing

```m
var _user_country = lookupvalue('rep v_hr_employee'[country_code],'rep v_hr_employee'[email], userprincipalname()) 

var _empCountry = [country_code]

return 
_empCountry = _user_country
||
(
calculate(CountRows('rls country'), 'rls country'[permission_to] = _empCountry && 'rls country'[email] = userprincipalname() ) > 0
)
```



Projetcs

```m
var _user_country = lookupvalue('rep v_hr_employee'[country_code],'rep v_hr_employee'[email], userprincipalname())

var _countries = 
Union(
calculatetable(values('rls country'[permission_to]), 'rls country'[email] = userprincipalname())
,
Row("permission_to", _user_country)
)

var _pn = [ProjectNumber]

var _projects = calculatetable(values(ParticipantsAndStaffing[ProjectNumber])
	, ParticipantsAndStaffing[ProjectNumber] = _pn 
	, Treatas(_countries, ParticipantsAndStaffing[country_code])
	)

return countrows(_projects) > 0
```



rep v_hr_employee

```m
var _user_country = lookupvalue('rep v_hr_employee'[country_code],'rep v_hr_employee'[email], userprincipalname())

var _countries = 
Union(
calculatetable(values('rls country'[permission_to]), 'rls country'[email] = userprincipalname())
,
Row("permission_to", _user_country)
)

var _emp = [emp_id]

var _emps = calculatetable(values(ParticipantsAndStaffing[emp_id])
	, ParticipantsAndStaffing[emp_id] = _emp 
	, Treatas(_countries, ParticipantsAndStaffing[country_code])
	)

return countrows(_emps) > 0 || [email] = userprincipalname()

```



Roles

```m
[Role] = "Country"
```



rls country

```m
[email] = userprincipalname()
```



rls clientteam

```m
false
```



rls countryOnly

```m
false
```



rls pilot group permission

```m
false
```



rls platform

```m
false
```



rls platform DACH

```m
false
```


### Consultant


Model Permission: Read

ParticipantsAndStaffing

```m
[email_dm] = userprincipalname() 
|| 
[email_pm] = userprincipalname() 
||
[email_mentor] = userprincipalname() 
|| 
[participant_email] = userprincipalname()
```



Projetcs

```m
var _pn = [ProjectNumber]

var _projects = calculatetable(values(ParticipantsAndStaffing[ProjectNumber])
	, ParticipantsAndStaffing[ProjectNumber] = _pn 
	&& 
	(
		ParticipantsAndStaffing[email_dm] = userprincipalname() 
	|| 
		ParticipantsAndStaffing[email_pm] = userprincipalname() 
	||
		ParticipantsAndStaffing[email_mentor] = userprincipalname() 
	|| 
		ParticipantsAndStaffing[participant_email] = userprincipalname()
	)
)

return countrows(_projects) > 0
```



rep v_hr_employee

```m
var _emp = [emp_id]

var _emps = calculatetable(values(ParticipantsAndStaffing[emp_id])
	, ParticipantsAndStaffing[emp_id] = _emp
	&& 
	(
		ParticipantsAndStaffing[email_dm] = userprincipalname() 
	|| 
		ParticipantsAndStaffing[email_pm] = userprincipalname() 
	||
		ParticipantsAndStaffing[email_mentor] = userprincipalname() 
	|| 
		ParticipantsAndStaffing[participant_email] = userprincipalname()
	)
)

return countrows(_emps) > 0
```



Roles

```m
[Role] = "Consultant"
```



rls clientteam

```m
false
```



rls country

```m
false
```



rls countryOnly

```m
false
```



rls pilot group permission

```m
false
```



rls platform

```m
false
```



rls platform DACH

```m
false
```


### Platform


Model Permission: Read

Roles

```m
[Role] = "Platform"
```



rep v_hr_employee

```m
var _user_platform= lookupvalue('rep v_hr_employee'[platform_1_id],'rep v_hr_employee'[email], userprincipalname()) 


var _platforms = union(calculatetable(values('rls platform'[permission_to]), 'rls platform'[email] = userprincipalname())
,
{
{_user_platform}
}        
)

var _emp = [emp_id]

var _emps = calculatetable(values(ParticipantsAndStaffing[emp_id])
	, ParticipantsAndStaffing[emp_id] = _emp 
	, Treatas(_platforms, ParticipantsAndStaffing[platform_1_id])
	)

return countrows(_emps) > 0 || [email] = userprincipalname()
```



ParticipantsAndStaffing

```m
var _user_platform= lookupvalue('rep v_hr_employee'[platform_1_id],'rep v_hr_employee'[email], userprincipalname()) 


var _platforms = union(calculatetable(values('rls platform'[permission_to]), 'rls platform'[email] = userprincipalname())
,
{
{_user_platform}
}        
)

var _pid = [platform_1_id]


return _pid in _platforms
```



Projetcs

```m
var _user_platform= lookupvalue('rep v_hr_employee'[platform_1_id],'rep v_hr_employee'[email], userprincipalname()) 


var _platforms = union(calculatetable(values('rls platform'[permission_to]), 'rls platform'[email] = userprincipalname())
,
{
{_user_platform}
}        
)

var _pn = [ProjectNumber]

var _projects = calculatetable(values(ParticipantsAndStaffing[ProjectNumber])
	, ParticipantsAndStaffing[ProjectNumber] = _pn 	, Treatas(_platforms, ParticipantsAndStaffing[platform_1_id])
	)

return countrows(_projects ) > 0
```



rls platform

```m
[email] = userprincipalname()
```



rls clientteam

```m
false
```



rls country

```m
false
```



rls countryOnly

```m
false
```



rls pilot group permission

```m
false
```



rls platform DACH

```m
false
```


### Pilot Group


Model Permission: Read

Roles

```m
[Role] = "Pilot"
```



ParticipantsAndStaffing

```m
var _empGroup = [pilot_group]

return calculate(CountRows('rls pilot group permission'), 'rls pilot group permission'[permission_to] = _empGroup && 'rls pilot group permission'[email] = userprincipalname() ) > 0
```



Projetcs

```m
var _pilotGroups= calculatetable(values('rls pilot group permission'[permission_to]), 'rls country'[email] = userprincipalname())

var _pn = [ProjectNumber]

var _projects = calculatetable(values(ParticipantsAndStaffing[ProjectNumber])
	, ParticipantsAndStaffing[ProjectNumber] = _pn 
	, Treatas(_pilotGroups, ParticipantsAndStaffing[pilot_group])
	)

return countrows(_projects) > 0
```



rep v_hr_employee

```m
var _pilotGroups= calculatetable(values('rls pilot group permission'[permission_to]), 'rls pilot group permission'[email] = userprincipalname())

var _emp = [emp_id]

var _emps = calculatetable(values(ParticipantsAndStaffing[emp_id])
	, ParticipantsAndStaffing[emp_id] = _emp 
	, Treatas(_pilotGroups, ParticipantsAndStaffing[pilot_group])
	)

return countrows(_emps) > 0
```



rls clientteam

```m
false
```



rls country

```m
false
```



rls countryOnly

```m
false
```



rls platform

```m
false
```



rls platform DACH

```m
false
```


### Client-Team


Model Permission: Read

Roles

```m
[Role] = "Client-Team"
```



rls clientteam

```m
[email] = userprincipalname()
```



ParticipantsAndStaffing

```m
var _empPracticeGroup = [practice_group]

return calculate(CountRows('rls clientteam'), 'rls clientteam'[permission_to] = _empPracticeGroup && 'rls clientteam'[email] = userprincipalname() ) > 0
```



Projetcs

```m
var _clientteams = calculatetable(values('rls clientteam'[permission_to]), 'rls clientteam'[email] = userprincipalname())

var _pn = [ProjectNumber]

var _projects = calculatetable(values(ParticipantsAndStaffing[ProjectNumber])
	, ParticipantsAndStaffing[ProjectNumber] = _pn 
	, Treatas(_clientteams , ParticipantsAndStaffing[practice_group])
	)

return countrows(_projects) > 0
```



rep v_hr_employee

```m
var _clientteams = calculatetable(values('rls clientteam'[permission_to]), 'rls clientteam'[email] = userprincipalname())

var _emp = [emp_id]

var _emps = calculatetable(values(ParticipantsAndStaffing[emp_id])
	, ParticipantsAndStaffing[emp_id] = _emp 
	, Treatas(_clientteams , ParticipantsAndStaffing[practice_group])
	)

return countrows(_emps) > 0
```



rls country

```m
false
```



rls countryOnly

```m
false
```



rls pilot group permission

```m
false
```



rls platform

```m
false
```



rls platform DACH

```m
false
```


### Platform DACH


Model Permission: Read

ParticipantsAndStaffing

```m
var _user_platform= lookupvalue('rep v_hr_employee'[platform_1_id],'rep v_hr_employee'[email], userprincipalname()) 


var _platforms = union(calculatetable(values('rls platform DACH'[permission_to]), 'rls platform DACH'[email] = userprincipalname())
,
{
{_user_platform}
}        
)

var _pid = [platform_1_id]
var _country = [country_code]

return _pid in _platforms && _country in {"DEU","AUT","CHE"}
```



Projetcs

```m
var _user_platform= lookupvalue('rep v_hr_employee'[platform_1_id],'rep v_hr_employee'[email], userprincipalname()) 


var _platforms = union(calculatetable(values('rls platform DACH'[permission_to]), 'rls platform DACH'[email] = userprincipalname())
,
{
{_user_platform}
}        
)

var _pn = [ProjectNumber]

var _projects = calculatetable(values(ParticipantsAndStaffing[ProjectNumber])
	, ParticipantsAndStaffing[ProjectNumber] = _pn 	, Treatas(_platforms, ParticipantsAndStaffing[platform_1_id])
, ParticipantsAndStaffing[Country_code] in {"DEU","AUT", "CHE"}
	)

return countrows(_projects ) > 0
```



rep v_hr_employee

```m
var _user_platform= lookupvalue('rep v_hr_employee'[platform_1_id],'rep v_hr_employee'[email], userprincipalname()) 


var _platforms = union(calculatetable(values('rls platform DACH'[permission_to]), 'rls platform DACH'[email] = userprincipalname())
,
{
{_user_platform}
}        
)

var _emp = [emp_id]

var _emps = calculatetable(values(ParticipantsAndStaffing[emp_id])
	, ParticipantsAndStaffing[emp_id] = _emp 
	, Treatas(_platforms, ParticipantsAndStaffing[platform_1_id])
, ParticipantsAndStaffing[Country_code] in {"DEU","AUT", "CHE"}
	)

return countrows(_emps) > 0 || [email] = userprincipalname()
```



rls platform

```m
false
```



Roles

```m
[Role] = "Platform"
```



rls platform DACH

```m
[email] = userprincipalname()
```



rls pilot group permission

```m
false
```



rls countryOnly

```m
false
```



rls country

```m
false
```



rls clientteam

```m
false
```


### Country Only


Model Permission: Read

ParticipantsAndStaffing

```m
var _empCountry = [country_code]

return 
(
calculate(CountRows('rls countryOnly'), 'rls countryOnly'[permission_to] = _empCountry && 'rls countryOnly'[email] = userprincipalname() ) > 0
)
```



Projetcs

```m
var _countries = 
calculatetable(values('rls countryOnly'[permission_to]), 'rls countryOnly'[email] = userprincipalname())


var _pn = [ProjectNumber]

var _projects = calculatetable(values(ParticipantsAndStaffing[ProjectNumber])
	, ParticipantsAndStaffing[ProjectNumber] = _pn 
	, Treatas(_countries, ParticipantsAndStaffing[country_code])
	)

return countrows(_projects) > 0
```



rep v_hr_employee

```m


var _countries = 

calculatetable(values('rls countryOnly'[permission_to]), 'rls countryOnly'[email] = userprincipalname())


var _emp = [emp_id]

var _emps = calculatetable(values(ParticipantsAndStaffing[emp_id])
	, ParticipantsAndStaffing[emp_id] = _emp 
	, Treatas(_countries, ParticipantsAndStaffing[country_code])
	)

return countrows(_emps) > 0 || [email] = userprincipalname()

```



rls country

```m
false
```



Roles

```m
[Role] = "CountryOnly"
```



rls countryOnly

```m
[email] = userprincipalname()
```



rls clientteam

```m
false
```



rls pilot group permission

```m
false
```



rls platform

```m
false
```



rls platform DACH

```m
false
```

