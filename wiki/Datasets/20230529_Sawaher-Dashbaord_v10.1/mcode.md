



# M Code

|Dataset|[20230529_Sawaher Dashbaord_v10.1](./../20230529_Sawaher-Dashbaord_v10.1.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Project


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m800177\Roland Berger Holding GmbH\SCAI_Sawaher - 70_Reporting\Nina's Work\Input Data.xlsx"), null, true),
    Project_Sheet = Source{[Item="Project",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Project_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Project #", Int64.Type}, {"Project", type text}, {"Start", type date}, {"End", type date}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Changed Type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Blank Rows",{{"Progress", Percentage.Type}, {"Progress Target", Percentage.Type}, {"Progress Status", type number}})
in
    #"Changed Type1"
```


## Table: Stream


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m800177\Roland Berger Holding GmbH\SCAI_Sawaher - 70_Reporting\Nina's Work\Input Data.xlsx"), null, true),
    Stream_Sheet = Source{[Item="Stream",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Stream_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Stream #", type text}, {"Project #", Int64.Type}, {"Project", type text}, {"Start", type date}, {"End", type date}, {"Actual Days", type number}, {"Stream Length", Int64.Type}, {"Length to Date", Int64.Type}, {"Progress Status", type number}, {"Planned Days", Int64.Type}})
in
    #"Changed Type"
```


## Table: Task


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m800177\Roland Berger Holding GmbH\SCAI_Sawaher - 70_Reporting\Nina's Work\Input Data.xlsx"), null, true),
    Task_Sheet = Source{[Item="Task",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Task_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Task #", type text}, {"Task", type text}, {"Stream #", type text}, {"Milestone", type text}, {"Start", type date}, {"End", type date}, {"Progress", Percentage.Type}, {"Actual Days", type number}, {"Task Length", Int64.Type}, {"Length to Date", Int64.Type}, {"Progress Target", Percentage.Type}, {"Progress Status", type number}})
in
    #"Changed Type"
```


## Table: TaskLog


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m800177\Roland Berger Holding GmbH\SCAI_Sawaher - 70_Reporting\Nina's Work\Input Data.xlsx"), null, true),
    TaskLog_Sheet = Source{[Item="TaskLog",Kind="Sheet"]}[Data],
    #"Removed Blank Rows" = Table.SelectRows(TaskLog_Sheet, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Blank Rows", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"#", Int64.Type}, {"Status", type text}, {"Responsible", type text}, {"Entity", type text},{"Project", type text}, {"Topic", type text}, {"Task Description", type text}, {"Entry Date", type date}, {"Due date", type date}, {"Updated Due Date", type date}, {"Closing date", type date}, {"Comments", type text}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type", {"Entity"}, #"Master - Entity Sort Order", {"Entity"}, "Master - Entity Sort Order", JoinKind.LeftOuter),
    #"Expanded Master - Entity Sort Order" = Table.ExpandTableColumn(#"Merged Queries", "Master - Entity Sort Order", {"Sort Order"}, {"Sort Order"})
in
    #"Expanded Master - Entity Sort Order"
```


## Table: Master - Tasklog Status


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m800177\Roland Berger Holding GmbH\SCAI_Sawaher - 70_Reporting\Nina's Work\Input Data.xlsx"), null, true),
    #"Master - Tasklog Status _Sheet" = Source{[Item="Master - Tasklog Status ",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Master - Tasklog Status _Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Status name", type text}, {"Status Category", type text}, {"half category", type text}})
in
    #"Changed Type"
```


## Table: Risk


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m800177\Roland Berger Holding GmbH\SCAI_Sawaher - 70_Reporting\Nina's Work\Input Data.xlsx"), null, true),
    Risk_Sheet = Source{[Item="Risk",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Risk_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date Raised", type date}, {"Id - Risk Identifier", Int64.Type}, {"Reporter Name", type text}, {"Project #", Int64.Type}, {"Stream #", type text}, {"Risk Topic", type text}, {"Risk Description", type text}, {"Risk Status", type text}, {"Risk Impact", type text}, {"Risk Probability", type text}, {"Key", type text}, {"Risk Rating/ Criticality", type text}, {"Impacted Milestone", type text}, {"Root Cause ", Int64.Type}, {"Risk Response Owner ", type text}, {"Risk Response Strategy", type text}, {"Resolution Action", type text}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Changed Type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
in
    #"Removed Blank Rows"
```


## Table: Issue


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m800177\Roland Berger Holding GmbH\SCAI_Sawaher - 70_Reporting\Nina's Work\Input Data.xlsx"), null, true),
    Issue_Sheet = Source{[Item="Issue",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Issue_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date Raised", type date}, {"Id - Issue Identifier", Int64.Type}, {"Reporter Name", type text}, {"Project #", Int64.Type}, {"Stream #", type text}, {"Risk #", Int64.Type}, {"Issue Topic", type text}, {"Issue Description", type text}, {"Issue Status", type text}, {"Issue Rating/ Criticality", type text}, {"Issue Impact", type text}, {"Impacted Milestone", type text}, {"Root Cause ", Int64.Type}, {"Issue Response Owner ", type text}, {"Issue Response Strategy", type text}, {"Resolution Action", type text}})
in
    #"Changed Type"
```


## Table: Master - Entity Sort Order


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m800177\Roland Berger Holding GmbH\SCAI_Sawaher - 70_Reporting\Nina's Work\Input Data.xlsx"), null, true),
    #"Master - Entity Sort Order_Sheet" = Source{[Item="Master - Entity Sort Order",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Master - Entity Sort Order_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Entity", type text}, {"Sort Order", Int64.Type}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Changed Type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
in
    #"Removed Blank Rows"
```

