



# M Code

|Dataset|[GPP test 1](./../GPP-test-1.md)|
| :--- | :--- |
|Workspace|[Test GPP](../../Workspaces/Test-GPP.md)|

## Table: Query1


```m
let
    Source = SharePoint.Contents("https://rberger.sharepoint.com/sites/MUC_Teams_CKM", [ApiVersion = 15]),
    #"Shared Documents" = Source{[Name="Shared Documents"]}[Content],
    #"GPP Excel" = #"Shared Documents"{[Name="GPP Excel"]}[Content],
    #"Filtered Hidden Files1" = Table.SelectRows(#"GPP Excel", each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File", each #"Transform File"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File", Table.ColumnNames(#"Transform File"(#"Sample File"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"Platform", type text}, {"Opportunity ID", type any}, {"OpportunityID", type text}, {"Account", type text}, {"Employee Responsible", type text}, {"Status of request", type text}, {"Email to ER date", type datetime}, {"Lifecycle Status", type text}, {"Sales Phase", type text}, {"Reply received", type logical}, {"Outcome", type text}, {"Proposal shared with", type text}, {"Reply received date", type datetime}, {"Reply mail subject", type text}, {"Reply mail body", type text}, {"Reply sent by", type text}, {"Industry", type text}, {"Industry ID", type text}, {"Function", type text}, {"Function ID", type text}, {"Created", type datetime}, {"Modified", type datetime}, {"Created On", type datetime}, {"Employee Responsible ID", type text}, {"ER company", type any}, {"Master Opportunity ID", Int64.Type}, {"Region", type text}, {"Remarks", type any}, {"Sales Unit", type text}, {"Sector", type text}, {"Status change date", type datetime}, {"Theme", type text}, {"App Created By", type any}, {"Created By", type text}, {"ID", Int64.Type}, {"Modified By", type text}, {"Oppportunity description", type text}, {"Project number", type any}, {"Sales Phase Id", Int64.Type}, {"Sector ID", Int64.Type}, {"Statussince", type any}, {"Theme ID", Int64.Type}, {"Title", type text}, {"Item Type", type text}, {"Path", type text}, {"Country/Region (Groups)", type text}})
in
    #"Changed Type"
```


## Parameter: Parameter1


```m
#"Sample File" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File", Type="Binary", IsParameterQueryRequired=true]
```

