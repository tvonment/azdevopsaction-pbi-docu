



# M Code

|Dataset|[Test 2 in PowerBI with new data](./../Test-2-in-PowerBI-with-new-data.md)|
| :--- | :--- |
|Workspace|[Intranet usage](../../Workspaces/Intranet-usage.md)|

## Table: Table1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\amalia_martin\Documents\Less_used\Confidential\TDR\To be used in powerBI\Downloads January 2023 FINAL.xlsx"), null, true),
    Table1_Table = Source{[Item="Table1",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Table1_Table,{{"CreationTime", type datetime}, {"SiteUrl", type text}, {"SourceFileName", type text}, {"Operation", type text}, {"Position", type any}, {"Department 1", type text}, {"Department 2", type any}, {"Country", type text}}),
    #"Appended Query" = Table.Combine({#"Changed Type", #"Table1 (2)", #"Table1 (3)", #"Table1 (4)"}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Appended Query", "CreationTime", "CreationTime - Copy"),
    #"Extracted Month" = Table.TransformColumns(#"Duplicated Column",{{"CreationTime - Copy", Date.Month, Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Extracted Month",{{"CreationTime - Copy", "Month"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"Month", type text}})
in
    #"Changed Type1"
```


## Table: Table1 (2)


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\amalia_martin\Documents\Less_used\Confidential\TDR\To be used in powerBI\Downloads February 2023 FINAL.xlsx"), null, true),
    Table1_Table = Source{[Item="Table1",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Table1_Table,{{"CreationTime", type datetime}, {"SiteUrl", type text}, {"SourceFileName", type text}, {"Operation", type text}, {"Position", type any}, {"Department 1", type text}, {"Department 2", type any}, {"Country", type text}})
in
    #"Changed Type"
```


## Table: Table1 (3)


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\amalia_martin\Documents\Less_used\Confidential\TDR\To be used in powerBI\Downloads March 2023 FINAL.xlsx"), null, true),
    Table1_Table = Source{[Item="Table1",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Table1_Table,{{"CreationTime", type datetime}, {"SiteUrl", type text}, {"SourceFileName", type text}, {"Operation", type text}, {"Position", type text}, {"Department 1", type text}, {"Department 2", type any}, {"Country", type text}})
in
    #"Changed Type"
```


## Table: Table1 (4)


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\amalia_martin\Documents\Less_used\Confidential\TDR\To be used in powerBI\Downloads April 2023 FINAL.xlsx"), null, true),
    Table1_Table = Source{[Item="Table1",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Table1_Table,{{"CreationTime", type datetime}, {"SiteUrl", type text}, {"SourceFileName", type text}, {"Operation", type text}, {"Position", type text}, {"Department 1", type text}, {"Department 2", type any}, {"Country", type text}})
in
    #"Changed Type"
```

