



# M Code

|Dataset|[2023-07-gubor-chock](./../2023-07-gubor-chock.md)|
| :--- | :--- |
|Workspace|[2023-07-gubor-chock](../../Workspaces/2023-07-gubor-chock.md)|

## Table: Query1


```m
let
    Source = AzureStorage.DataLake("https://powerbistoresawprodv1.dfs.core.windows.net/2023-07-gubor-chock-pbi"),
    #"https://powerbistoresawprodv1 dfs core windows net/2023-07-gubor-chock-pbi/_Output csv" = Source{[#"Folder Path"="https://powerbistoresawprodv1.dfs.core.windows.net/2023-07-gubor-chock-pbi/",Name="Output.csv"]}[Content],
    #"Imported CSV" = Csv.Document(#"https://powerbistoresawprodv1 dfs core windows net/2023-07-gubor-chock-pbi/_Output csv",[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"", Int64.Type}, {"Kreditor", Int64.Type}, {"Name", type text}, {"Nettofälligkeit", type text}, {"Betrag in €", type number}, {"FileName", type text}})
in
    #"Changed Type"
```

