



# M Code

|Dataset|[Dataflow Snapshot Analysis](./../Dataflow-Snapshot-Analysis.md)|
| :--- | :--- |
|Workspace|[Dataflow Snapshots](../../Workspaces/Dataflow-Snapshots.md)|

## Table: Profiles Numeric Columns


```m
let
    Source = Profiles,
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Min", type number}, {"Max", type number}, {"Average", type number}, {"Stdev", type number}, {"Count", Int64.Type}, {"Null Count", Int64.Type}, {"Distinct Count", Int64.Type}}),
    #"Removed Errors" = Table.RemoveRowsWithErrors(#"Changed Type", {"Min"}),
    #"Removed Errors1" = Table.RemoveRowsWithErrors(#"Removed Errors", {"Max"}),
    #"Removed Columns" = Table.RemoveColumns(#"Removed Errors1",{"Date modified"}),
    #"Inserted Merged Column" = Table.AddColumn(#"Removed Columns", "Table / Column", each Text.Combine({[Table], [Column]}, " / "), type text),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"Column", type text}, {"Filename", type text}})
in
    #"Changed Type1"
```


## Table: Profiles Non-Numeric Columns


```m
let
    Source = Profiles,
    #"Added Custom" = Table.AddColumn(Source, "Custom", each if [Min] is number then 0 else 1),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom", each ([Custom] = 1)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Average", "Stdev", "Date modified", "Custom"}),
    #"Inserted Merged Column" = Table.AddColumn(#"Removed Columns", "Table/Column", each Text.Combine({[Table], [Column]}, " / "), type text),
    #"Changed Type" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"Count", Int64.Type}, {"Null Count", Int64.Type}, {"Distinct Count", Int64.Type}})
in
    #"Changed Type"
```


## Table: Diffs


```m
let
    Source = #"Snapshots - Base Combined",
    #"Removed Columns" = Table.RemoveColumns(Source,{"Snapshot", "Diff", "Size"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each [Diff Count] > 0),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"Diff Count", Int64.Type}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Changed Type",{"Date modified", "Table"})
in
    #"Removed Columns1"
```


## Table: Diffs Details


```m
let
    Source = #"Diffs Details - Base",
    DiffDetailsNoRowIndex = Table.SelectRows(Source, each ([Column] <> "DataChantIndex")),
    
    DiffDetailsRowIndexOnly = Table.SelectRows(Source, each ([Column] = "DataChantIndex")),

    #"Merged Queries" = Table.NestedJoin(DiffDetailsNoRowIndex, {"Table", "Filename", "Row"}, DiffDetailsRowIndexOnly, {"Table", "Filename", "Row"}, "Row Changes", JoinKind.LeftOuter),
    #"Expanded Row Changes" = Table.ExpandTableColumn(#"Merged Queries", "Row Changes", {"Change"}, {"Row Changes"})
in
    #"Expanded Row Changes"
```


## Table: Snapshots


```m
let
    Source = #"Snapshots - Base Combined",
    #"Removed Columns" = Table.RemoveColumns(Source,{"Snapshot", "Diff", "Diff Count"}),
    #"Inserted Date" = Table.AddColumn(#"Removed Columns", "Date", each DateTime.Date([Date modified]), type date),

    #"Grouped Rows" = Table.Group(#"Inserted Date", {"Table"}, {{"Data", each Table.AddIndexColumn(Table.Sort(_,{{"Date modified", Order.Ascending}}), "Index", 0, 1, Int64.Type), type table [Table=text, Filename=text, Date modified=nullable datetime, Size=nullable number, Date=date, Index=number]}}),
    #"Expanded Data" = Table.ExpandTableColumn(#"Grouped Rows", "Data", {"Filename", "Date modified", "Size", "Date", "Index"}, {"Filename", "Date modified", "Size", "Date", "Index"}),
    #"Removed Duplicates1" = Table.Distinct(#"Expanded Data", {"Filename"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates1",{{"Index", "Refresh Number"}})
in
    #"Renamed Columns"
```


## Table: Tables


```m
let
    Source = Keys,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"Table"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns")
in
    #"Removed Duplicates"
```


## Table: Workspace Name


```m
"Test Workspace" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Table: Dataflow Name


```m
"Test Dataflow" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Table: Profiles Numeric Unpivot


```m
let
    Source = #"Profiles Numeric Columns",
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(Source, {"Table", "Filename", "Column", "Table / Column"}, "Metric", "Value")
in
    #"Unpivoted Other Columns"
```


## Parameter: ADLS Gen2 Account Name


Your Azure Storage Account Name of your ADLS Gen2 connected to the monitored workspace

```m
"MyDatalake" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Parameter: Table Keys Path


The full path for the Excel file with the definition of keys per table. Learn more here: https://datachant.com/dataflow-snapshot-analysis/

```m
"https://company.sharepoint.com/.../DataflowTableKeys.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Parameter: Top Rows


Select the maximal number of rows to keep in each snapshot. For performance reasons, it is advised to monitor small tables.

```m
"1000" meta [IsParameterQuery=true, List={"10000", "1000", "100", "10", "No Limit"}, DefaultValue="1000", Type="Text", IsParameterQueryRequired=true]
```


## Parameter: Max Recent Snapshots


Select the maximal number of latest snapshots to monitor. For performance reasons, it is advised to monitor a small number of snapshots.

```m
"5" meta [IsParameterQuery=true, List={"20", "10", "5", "2", "No Limit"}, DefaultValue="5", Type="Text", IsParameterQueryRequired=true]
```


## Parameter: Show Only Changes


Select "Yes" to look only for changes and ignore new and missing records.

```m
"No" meta [IsParameterQuery=true, List={"Yes", "No"}, DefaultValue="No", Type="Text", IsParameterQueryRequired=true]
```

