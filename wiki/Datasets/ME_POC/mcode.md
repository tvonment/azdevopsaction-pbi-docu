



# M Code

|Dataset|[ME_POC](./../ME_POC.md)|
| :--- | :--- |
|Workspace|[ME-Management-Dashboard](../../Workspaces/ME-Management-Dashboard.md)|

## Table: Query1


```m
let
    Source = AzureStorage.DataLake("https://powerbistoragesawprodv1.dfs.core.windows.net/2023-04-me-mgmt-dashboard"),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "BS result_1.xlsx")),
    #"Filtered Hidden Files1" = Table.SelectRows(#"Filtered Rows", each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File", each #"Transform File"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File", Table.ColumnNames(#"Transform File"(#"Sample File"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"Project", type text}, {"Project1", type any}, {"Project2", type any}, {"Project3", type any}, {"Project4", type any}, {"Project5", type any}, {"Project6", type any}, {"Project7", type any}, {"Project8", type any}, {"Project9", type any}, {"Project10", type any}, {"Project11", type any}, {"Project12", type any}, {"Project13", type any}, {"Project14", type any}, {"Project15", type any}, {"Project16", type any}, {"Project17", type any}, {"Project18", type any}, {"Project19", type any}, {"Project20", type any}, {"Project21", type any}, {"Project22", type any}, {"Project23", type any}, {"Project24", type any}, {"Column26", type number}, {"Column27", type number}, {"Column28", type number}, {"Column29", type number}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Source.Name", "Column26", "Column27", "Column28", "Column29"}),
    #"Demoted Headers" = Table.DemoteHeaders(#"Removed Columns"),
    #"Changed Type1" = Table.TransformColumnTypes(#"Demoted Headers",{{"Column1", type text}, {"Column2", type any}, {"Column3", type any}, {"Column4", type any}, {"Column5", type any}, {"Column6", type any}, {"Column7", type any}, {"Column8", type any}, {"Column9", type any}, {"Column10", type any}, {"Column11", type any}, {"Column12", type any}, {"Column13", type any}, {"Column14", type any}, {"Column15", type any}, {"Column16", type any}, {"Column17", type any}, {"Column18", type any}, {"Column19", type any}, {"Column20", type any}, {"Column21", type any}, {"Column22", type any}, {"Column23", type any}, {"Column24", type any}, {"Column25", type any}}),
    #"Transposed Table" = Table.Transpose(#"Changed Type1"),
    #"Promoted Headers" = Table.PromoteHeaders(#"Transposed Table", [PromoteAllScalars=true]),
    #"Changed Type2" = Table.TransformColumnTypes(#"Promoted Headers",{{"Project", type text}, {"Client", type text}, {"Over Draft", type number}, {"Avg Daily Rate", type number}, {"Currency", type text}, {"Office", type text}, {"Industry Platform", type text}, {"Sub Industry Platform", type text}, {"Functional Platform", type text}, {"Sub Functional Platform", type text}, {"Client Budget", type number}, {"ME 2022-07", type number}, {"ME 2022-08", type number}, {"ME 2022-09", type number}, {"ME 2022-10", type number}, {"ME 2022-11", type number}, {"ME 2022-12", type number}, {"ME 2023-01", type number}, {"ME 2023-02", type number}, {"ME 2023-03", type number}, {"ME 2023-04", type number}, {"ME 2023-05", type number}, {"ME 2023-06", type number}, {"ME 2023-07", type number}, {"ME 2023-08", type number}, {"ME 2023-09", type number}, {"ME 2023-10", type number}, {"ME 2023-11", type number}, {"ME 2023-12", type number}, {"ME 2024-01", type number}, {"ME 2024-02", type number}, {"ME 2024-03", type number}, {"ME 2024-04", type number}, {"ME 2024-05", type number}, {"ME 2024-06", type number}, {"ME 2024-07", type number}, {"ME 2024-08", type number}, {"ME 2024-09", type number}, {"ME 2024-10", type number}, {"ME 2024-11", type number}, {"ME 2024-12", type number}, {"Gross 2022-07", type number}, {"Gross 2022-08", type number}, {"Gross 2022-09", type number}, {"Gross 2022-10", type number}, {"Gross 2022-11", type number}, {"Gross 2022-12", type number}, {"Gross 2023-01", type number}, {"Gross 2023-02", type number}, {"Gross 2023-03", type number}, {"Gross 2023-04", type number}, {"Gross 2023-05", type number}, {"Gross 2023-06", type number}, {"Gross 2023-07", type number}, {"Gross 2023-08", type number}, {"Gross 2023-09", type number}, {"Gross 2023-10", type number}, {"Gross 2023-11", type number}, {"Gross 2023-12", type number}, {"Gross 2024-01", type number}, {"Gross 2024-02", type number}, {"Gross 2024-03", type number}, {"Gross 2024-04", type number}, {"Gross 2024-05", type number}, {"Gross 2024-06", type number}, {"Gross 2024-07", type number}, {"Gross 2024-08", type number}, {"Gross 2024-09", type number}, {"Gross 2024-10", type number}, {"Gross 2024-11", type number}, {"Gross 2024-12", type number}, {"Total ME", type number}, {"Total Gross", type number}})
in
    #"Changed Type2"
```


## Table: Monthly


```m
let
    Source = AzureStorage.DataLake("https://powerbistoragesawprodv1.dfs.core.windows.net/2023-04-me-mgmt-dashboard"),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "Monthly.csv")),
    #"Filtered Hidden Files1" = Table.SelectRows(#"Filtered Rows", each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File (3)", each #"Transform File (3)"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File (3)"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File (3)", Table.ColumnNames(#"Transform File (3)"(#"Sample File (3)"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"", Int64.Type}, {"Name", type text}, {"Dummy2.xlsx", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Source.Name", ""}),
    #"Transposed Table" = Table.Transpose(#"Removed Columns"),
    #"Promoted Headers" = Table.PromoteHeaders(#"Transposed Table", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"Project", type text}, {"Client", type text}, {"Over Draft", type number}, {"Avg Daily Rate", type number}, {"Currency", type text}, {"Office", type text}, {"Industry Platform", type text}, {"Sub Industry Platform", type text}, {"Functional Platform", type text}, {"Sub Functional Platform", type text}, {"Client Budget", type number}, {"ProjectName", type text}, {"ME 2023-01", type number}, {"ME 2023-02", type number}, {"ME 2023-03", type number}, {"ME 2023-04", type number}, {"ME 2023-05", type number}, {"ME 2023-06", type number}, {"Gross 2023-01", type number}, {"Gross 2023-02", type number}, {"Gross 2023-03", type number}, {"Gross 2023-04", type number}, {"Gross 2023-05", type number}, {"Gross 2023-06", type number}, {"Total ME", type number}, {"Total Gross", type number}})
in
    #"Changed Type1"
```


## Table: Weekly


```m
let
    Source = AzureStorage.DataLake("https://powerbistoragesawprodv1.dfs.core.windows.net/2023-04-me-mgmt-dashboard"),
    #"Filtered Rows" = Table.SelectRows(Source, each [Name] = "Weekly.csv"),
    #"Filtered Hidden Files1" = Table.SelectRows(#"Filtered Rows", each [Attributes]?[Hidden]? <> true),
    #"Filtered Hidden Files2" = Table.SelectRows(#"Filtered Hidden Files1", each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files2", "Transform File (5)", each #"Transform File (5)"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File (5)"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File (5)", Table.ColumnNames(#"Transform File (5)"(#"Sample File (5)"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"", Int64.Type}, {"Name", type text}, {"Dummy_Weekly.xlsx", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Source.Name", ""}),
    #"Transposed Table" = Table.Transpose(#"Removed Columns"),
    #"Promoted Headers" = Table.PromoteHeaders(#"Transposed Table", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"FileName", type text}, {"Project", type text}, {"Client", type text}, {"Over Draft", type number}, {"Avg Daily Rate", type number}, {"Currency", type text}, {"Office", type text}, {"Industry Platform", type text}, {"Sub Industry Platform", type text}, {"Functional Platform", type text}, {"Sub Functional Platform", type text}, {"Client Budget", type number}, {"ProjectName", type text}, {"ME 09-Jan-2023", type number}, {"ME 10-Jan-2023", type number}, {"ME 11-Jan-2023", type number}, {"ME 12-Jan-2023", type number}, {"ME 13-Jan-2023", type number}, {"ME 16-Jan-2023", type number}, {"ME 17-Jan-2023", type number}, {"ME 18-Jan-2023", type number}, {"ME 19-Jan-2023", type number}, {"ME 20-Jan-2023", type number}, {"ME 23-Jan-2023", type number}, {"ME 24-Jan-2023", type number}, {"ME 25-Jan-2023", type number}, {"ME 26-Jan-2023", type number}, {"ME 27-Jan-2023", type number}, {"ME 30-Jan-2023", type number}, {"ME 31-Jan-2023", type number}, {"ME 01-Feb-2023", type number}, {"ME 02-Feb-2023", type number}, {"ME 03-Feb-2023", type number}, {"ME 06-Feb-2023", type number}, {"ME 07-Feb-2023", type number}, {"ME 08-Feb-2023", type number}, {"ME 09-Feb-2023", type number}, {"ME 10-Feb-2023", type number}, {"ME 13-Feb-2023", type number}, {"ME 14-Feb-2023", type number}, {"ME 15-Feb-2023", type number}, {"ME 16-Feb-2023", type number}, {"ME 17-Feb-2023", type number}, {"ME 20-Feb-2023", type number}, {"ME 21-Feb-2023", type number}, {"ME 22-Feb-2023", type number}, {"ME 23-Feb-2023", type number}, {"ME 24-Feb-2023", type number}, {"ME 27-Feb-2023", type number}, {"ME 28-Feb-2023", type number}, {"ME 01-Mar-2023", type number}, {"ME 02-Mar-2023", type number}, {"ME 03-Mar-2023", type number}, {"ME 06-Mar-2023", type number}, {"ME 07-Mar-2023", type number}, {"ME 08-Mar-2023", type number}, {"ME 09-Mar-2023", type number}, {"ME 10-Mar-2023", type number}, {"ME 13-Mar-2023", type number}, {"ME 14-Mar-2023", type number}, {"ME 15-Mar-2023", type number}, {"ME 16-Mar-2023", type number}, {"ME 17-Mar-2023", type number}, {"ME 20-Mar-2023", type number}, {"ME 21-Mar-2023", type number}, {"ME 22-Mar-2023", type number}, {"ME 23-Mar-2023", type number}, {"ME 24-Mar-2023", type number}, {"ME 27-Mar-2023", type number}, {"ME 28-Mar-2023", type number}, {"ME 29-Mar-2023", type number}, {"ME 30-Mar-2023", type number}, {"ME 31-Mar-2023", type number}, {"ME 03-Apr-2023", type number}, {"ME 04-Apr-2023", type number}, {"ME 05-Apr-2023", type number}, {"ME 06-Apr-2023", type number}, {"ME 07-Apr-2023", type number}, {"ME 10-Apr-2023", type number}, {"ME 11-Apr-2023", type number}, {"ME 12-Apr-2023", type number}, {"ME 13-Apr-2023", type number}, {"ME 14-Apr-2023", type number}, {"ME 17-Apr-2023", Int64.Type}, {"ME 18-Apr-2023", Int64.Type}, {"ME 19-Apr-2023", Int64.Type}, {"ME 20-Apr-2023", Int64.Type}, {"ME 21-Apr-2023", Int64.Type}, {"ME 24-Apr-2023", type number}, {"ME 25-Apr-2023", type number}, {"ME 26-Apr-2023", type number}, {"ME 27-Apr-2023", type number}, {"ME 28-Apr-2023", type number}, {"ME 01-May-2023", type number}, {"ME 02-May-2023", type number}, {"ME 03-May-2023", type number}, {"ME 04-May-2023", type number}, {"ME 05-May-2023", type number}, {"ME 08-May-2023", type number}, {"ME 09-May-2023", type number}, {"ME 10-May-2023", type number}, {"ME 11-May-2023", type number}, {"ME 12-May-2023", type number}, {"ME 15-May-2023", type number}, {"ME 16-May-2023", type number}, {"ME 17-May-2023", type number}, {"ME 18-May-2023", type number}, {"ME 19-May-2023", type number}, {"ME 22-May-2023", type number}, {"ME 23-May-2023", type number}, {"ME 24-May-2023", type number}, {"ME 25-May-2023", type number}, {"ME 26-May-2023", type number}, {"ME 29-May-2023", type number}, {"ME 30-May-2023", type number}, {"ME 31-May-2023", type number}, {"ME 01-Jun-2023", type number}, {"ME 02-Jun-2023", type number}, {"ME 05-Jun-2023", Int64.Type}, {"ME 06-Jun-2023", Int64.Type}, {"ME 07-Jun-2023", Int64.Type}, {"ME 08-Jun-2023", Int64.Type}, {"ME 09-Jun-2023", Int64.Type}, {"ME 12-Jun-2023", Int64.Type}, {"ME 13-Jun-2023", Int64.Type}, {"ME 14-Jun-2023", Int64.Type}, {"ME 15-Jun-2023", Int64.Type}, {"ME 16-Jun-2023", Int64.Type}, {"ME 19-Jun-2023", Int64.Type}, {"ME 20-Jun-2023", Int64.Type}, {"ME 21-Jun-2023", Int64.Type}, {"ME 22-Jun-2023", Int64.Type}, {"ME 23-Jun-2023", Int64.Type}, {"ME 26-Jun-2023", Int64.Type}, {"ME 27-Jun-2023", Int64.Type}, {"ME 28-Jun-2023", Int64.Type}, {"ME 29-Jun-2023", Int64.Type}, {"ME 30-Jun-2023", Int64.Type}, {"ME 03-Jul-2023", Int64.Type}, {"ME 04-Jul-2023", Int64.Type}, {"ME 05-Jul-2023", Int64.Type}, {"ME 06-Jul-2023", Int64.Type}, {"ME 07-Jul-2023", Int64.Type}, {"ME 10-Jul-2023", Int64.Type}, {"ME 11-Jul-2023", Int64.Type}, {"ME 12-Jul-2023", Int64.Type}, {"ME 13-Jul-2023", Int64.Type}, {"ME 14-Jul-2023", Int64.Type}, {"ME 17-Jul-2023", Int64.Type}, {"ME 18-Jul-2023", Int64.Type}, {"ME 19-Jul-2023", Int64.Type}, {"ME 20-Jul-2023", Int64.Type}, {"ME 21-Jul-2023", Int64.Type}, {"ME 24-Jul-2023", Int64.Type}, {"ME 25-Jul-2023", Int64.Type}, {"ME 26-Jul-2023", Int64.Type}, {"ME 27-Jul-2023", Int64.Type}, {"ME 28-Jul-2023", Int64.Type}, {"ME 31-Jul-2023", Int64.Type}, {"ME 01-Aug-2023", Int64.Type}, {"ME 02-Aug-2023", Int64.Type}, {"ME 03-Aug-2023", Int64.Type}, {"ME 04-Aug-2023", Int64.Type}, {"Gross 09-Jan-2023", type number}, {"Gross 10-Jan-2023", type number}, {"Gross 11-Jan-2023", type number}, {"Gross 12-Jan-2023", type number}, {"Gross 13-Jan-2023", type number}, {"Gross 16-Jan-2023", type number}, {"Gross 17-Jan-2023", type number}, {"Gross 18-Jan-2023", type number}, {"Gross 19-Jan-2023", type number}, {"Gross 20-Jan-2023", type number}, {"Gross 23-Jan-2023", type number}, {"Gross 24-Jan-2023", type number}, {"Gross 25-Jan-2023", type number}, {"Gross 26-Jan-2023", type number}, {"Gross 27-Jan-2023", type number}, {"Gross 30-Jan-2023", type number}, {"Gross 31-Jan-2023", type number}, {"Gross 01-Feb-2023", type number}, {"Gross 02-Feb-2023", type number}, {"Gross 03-Feb-2023", type number}, {"Gross 06-Feb-2023", type number}, {"Gross 07-Feb-2023", type number}, {"Gross 08-Feb-2023", type number}, {"Gross 09-Feb-2023", type number}, {"Gross 10-Feb-2023", type number}, {"Gross 13-Feb-2023", type number}, {"Gross 14-Feb-2023", type number}, {"Gross 15-Feb-2023", type number}, {"Gross 16-Feb-2023", type number}, {"Gross 17-Feb-2023", type number}, {"Gross 20-Feb-2023", type number}, {"Gross 21-Feb-2023", type number}, {"Gross 22-Feb-2023", type number}, {"Gross 23-Feb-2023", type number}, {"Gross 24-Feb-2023", type number}, {"Gross 27-Feb-2023", type number}, {"Gross 28-Feb-2023", type number}, {"Gross 01-Mar-2023", type number}, {"Gross 02-Mar-2023", type number}, {"Gross 03-Mar-2023", type number}, {"Gross 06-Mar-2023", type number}, {"Gross 07-Mar-2023", type number}, {"Gross 08-Mar-2023", type number}, {"Gross 09-Mar-2023", type number}, {"Gross 10-Mar-2023", type number}, {"Gross 13-Mar-2023", type number}, {"Gross 14-Mar-2023", type number}, {"Gross 15-Mar-2023", type number}, {"Gross 16-Mar-2023", type number}, {"Gross 17-Mar-2023", type number}, {"Gross 20-Mar-2023", type number}, {"Gross 21-Mar-2023", type number}, {"Gross 22-Mar-2023", type number}, {"Gross 23-Mar-2023", type number}, {"Gross 24-Mar-2023", type number}, {"Gross 27-Mar-2023", type number}, {"Gross 28-Mar-2023", type number}, {"Gross 29-Mar-2023", type number}, {"Gross 30-Mar-2023", type number}, {"Gross 31-Mar-2023", type number}, {"Gross 03-Apr-2023", type number}, {"Gross 04-Apr-2023", type number}, {"Gross 05-Apr-2023", type number}, {"Gross 06-Apr-2023", type number}, {"Gross 07-Apr-2023", type number}, {"Gross 10-Apr-2023", type number}, {"Gross 11-Apr-2023", type number}, {"Gross 12-Apr-2023", type number}, {"Gross 13-Apr-2023", type number}, {"Gross 14-Apr-2023", type number}, {"Gross 17-Apr-2023", Int64.Type}, {"Gross 18-Apr-2023", Int64.Type}, {"Gross 19-Apr-2023", Int64.Type}, {"Gross 20-Apr-2023", Int64.Type}, {"Gross 21-Apr-2023", Int64.Type}, {"Gross 24-Apr-2023", type number}, {"Gross 25-Apr-2023", type number}, {"Gross 26-Apr-2023", type number}, {"Gross 27-Apr-2023", type number}, {"Gross 28-Apr-2023", type number}, {"Gross 01-May-2023", type number}, {"Gross 02-May-2023", type number}, {"Gross 03-May-2023", type number}, {"Gross 04-May-2023", type number}, {"Gross 05-May-2023", type number}, {"Gross 08-May-2023", type number}, {"Gross 09-May-2023", type number}, {"Gross 10-May-2023", type number}, {"Gross 11-May-2023", type number}, {"Gross 12-May-2023", type number}, {"Gross 15-May-2023", type number}, {"Gross 16-May-2023", type number}, {"Gross 17-May-2023", type number}, {"Gross 18-May-2023", type number}, {"Gross 19-May-2023", type number}, {"Gross 22-May-2023", type number}, {"Gross 23-May-2023", type number}, {"Gross 24-May-2023", type number}, {"Gross 25-May-2023", type number}, {"Gross 26-May-2023", type number}, {"Gross 29-May-2023", type number}, {"Gross 30-May-2023", type number}, {"Gross 31-May-2023", type number}, {"Gross 01-Jun-2023", type number}, {"Gross 02-Jun-2023", type number}, {"Gross 05-Jun-2023", Int64.Type}, {"Gross 06-Jun-2023", Int64.Type}, {"Gross 07-Jun-2023", Int64.Type}, {"Gross 08-Jun-2023", Int64.Type}, {"Gross 09-Jun-2023", Int64.Type}, {"Gross 12-Jun-2023", Int64.Type}, {"Gross 13-Jun-2023", Int64.Type}, {"Gross 14-Jun-2023", Int64.Type}, {"Gross 15-Jun-2023", Int64.Type}, {"Gross 16-Jun-2023", Int64.Type}, {"Gross 19-Jun-2023", Int64.Type}, {"Gross 20-Jun-2023", Int64.Type}, {"Gross 21-Jun-2023", Int64.Type}, {"Gross 22-Jun-2023", Int64.Type}, {"Gross 23-Jun-2023", Int64.Type}, {"Gross 26-Jun-2023", Int64.Type}, {"Gross 27-Jun-2023", Int64.Type}, {"Gross 28-Jun-2023", Int64.Type}, {"Gross 29-Jun-2023", Int64.Type}, {"Gross 30-Jun-2023", Int64.Type}, {"Gross 03-Jul-2023", Int64.Type}, {"Gross 04-Jul-2023", Int64.Type}, {"Gross 05-Jul-2023", Int64.Type}, {"Gross 06-Jul-2023", Int64.Type}, {"Gross 07-Jul-2023", Int64.Type}, {"Gross 10-Jul-2023", Int64.Type}, {"Gross 11-Jul-2023", Int64.Type}, {"Gross 12-Jul-2023", Int64.Type}, {"Gross 13-Jul-2023", Int64.Type}, {"Gross 14-Jul-2023", Int64.Type}, {"Gross 17-Jul-2023", Int64.Type}, {"Gross 18-Jul-2023", Int64.Type}, {"Gross 19-Jul-2023", Int64.Type}, {"Gross 20-Jul-2023", Int64.Type}, {"Gross 21-Jul-2023", Int64.Type}, {"Gross 24-Jul-2023", Int64.Type}, {"Gross 25-Jul-2023", Int64.Type}, {"Gross 26-Jul-2023", Int64.Type}, {"Gross 27-Jul-2023", Int64.Type}, {"Gross 28-Jul-2023", Int64.Type}, {"Gross 31-Jul-2023", Int64.Type}, {"Gross 01-Aug-2023", Int64.Type}, {"Gross 02-Aug-2023", Int64.Type}, {"Gross 03-Aug-2023", Int64.Type}, {"Gross 04-Aug-2023", Int64.Type}, {"Total ME", type number}, {"Total Gross", type number}})
in
    #"Changed Type1"
```


## Parameter: Parameter1


```m
#"Sample File" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File", Type="Binary", IsParameterQueryRequired=true]
```


## Parameter: Parameter2


```m
#"Sample File (3)" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File (3)", Type="Binary", IsParameterQueryRequired=true]
```


## Parameter: Parameter3


```m
#"Sample File (5)" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File (5)", Type="Binary", IsParameterQueryRequired=true]
```

