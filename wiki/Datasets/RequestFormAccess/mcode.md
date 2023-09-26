



# M Code

|Dataset|[RequestFormAccess](./../RequestFormAccess.md)|
| :--- | :--- |
|Workspace|[Central Graphics](../../Workspaces/Central-Graphics.md)|

## Table: Logging


```m
let
    Source = SharePoint.Tables("https://rberger.sharepoint.com/sites/GGPRequestForm"),
    Logging1 = Source{[Name="Logging"]}[Content],
    #"Filtered Rows" = Table.SelectRows(Logging1, each ([System] = "PROD")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"Id", "Modified", "Title", "Message", "AppUser", "System"})
in
    #"Removed Other Columns"
```

