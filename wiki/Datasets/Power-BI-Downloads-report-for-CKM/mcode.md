



# M Code

|Dataset|[Power BI Downloads report for CKM](./../Power-BI-Downloads-report-for-CKM.md)|
| :--- | :--- |
|Workspace|[Intranet usage](../../Workspaces/Intranet-usage.md)|

## Table: Confidential


```m
let
    Source = Folder.Files("C:\Users\amalia_martin\Roland Berger Holding GmbH\CKM - General\Projects 2023\Confidential"),
    #"Filtered Hidden Files1" = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File", each #"Transform File"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File", Table.ColumnNames(#"Transform File"(#"Sample File"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"CreationTime", type datetime}, {"SiteUrl", type text}, {"SourceFileName", type text}, {"Operation", type text}, {"Position", type text}, {"Department 1", type text}, {"Department 2", type any}, {"Country", type text}})
in
    #"Changed Type"
```


## Parameter: Parameter1


```m
#"Sample File" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File", Type="Binary", IsParameterQueryRequired=true]
```

