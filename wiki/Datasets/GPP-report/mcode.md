



# M Code

|Dataset|[GPP report](./../GPP-report.md)|
| :--- | :--- |
|Workspace|[Test GPP](../../Workspaces/Test-GPP.md)|

## Table: Opportunities


```m
let
    Source = SharePoint.Tables("https://sharepoint.rolandberger.net/sites/ProposalDocumentation/", [ApiVersion = 15]),
    #"86710604-4aff-401c-9e46-f28dc767d850" = Source{[Id="86710604-4aff-401c-9e46-f28dc767d850"]}[Items],
    #"Renamed Columns" = Table.RenameColumns(#"86710604-4aff-401c-9e46-f28dc767d850",{{"ID", "ID.1"}})
in
    #"Renamed Columns"
```

