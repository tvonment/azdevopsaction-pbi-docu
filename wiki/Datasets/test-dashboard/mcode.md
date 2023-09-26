



# M Code

|Dataset|[test dashboard](./../test-dashboard.md)|
| :--- | :--- |
|Workspace|[Test Dashboards for tutorial](../../Workspaces/Test-Dashboards-for-tutorial.md)|

## Table: Table1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M714156\Desktop\test for country groups.xlsx"), null, true),
    Table1_Table = Source{[Item="Table1",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Table1_Table,{{"CreationTime", type datetime}, {"SiteUrl", type text}, {"SourceFileName", type text}, {"Operation", type text}, {"Position", type text}, {"Department 1", type text}, {"Department 2", type any}, {"Country groups", type text}, {"Country", type text}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type", {"Country"}, #"groups table", {"Country"}, "groups table", JoinKind.LeftOuter),
    #"Expanded groups table" = Table.ExpandTableColumn(#"Merged Queries", "groups table", {"Country Groups"}, {"groups table.Country Groups"})
in
    #"Expanded groups table"
```


## Table: groups table


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("jZPBbsIwDIZfJeqZA9ph98IYbAy00bEL42Aar1hrk8ptxODp56ZFgqpFXNrk+//EcexsNsGI4URpMAjCDJliKILtYBOMwYCGNl1HYRst8I9i26ahK0qmav1TOJ55FB2oPCGnYPQlniJnYI6XaOZMAlyhCRQlslETxzZHL66s2P3OXaIrij5t/ctABrvFZwYTV1o9UN9uOHx4VAvLNpbsfKLN+JZnvCdThZ8ygoRQ9dznZE2i5vLpVF8hByOK/583nlvxnScvRlPt9XigVpi7XUqxsj93LqxH93mjXO5KvAvUJEeVhBGuLuzdcukSSG95XkpIj7cMI9hzE4e0TlFVlfHKG+7A2C7lA0rgDh6B06RChp1Psi2vjRxBe11NMmIpQNFhG2GakMtEWUqC+1aXLLFCVQcXPY7ogBpNj9icYU4m0bYvhtTAGqy7OJqEdetBCsdrFMkmkEvxLtjnHqh5Xmf0RViqJWRntP0H", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Country = _t, #"Country Groups" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Country", type text}, {"Country Groups", type text}})
in
    #"Changed Type"
```


## Table: activeKBases table


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("ndTBasMwDAbgd8m51Pfduiwto5SFJt2llOE6WiNwrCArhb79zPYC63+2v9/Ckn0+V6PZnF+c0yvpjXSdR680CydbB5lcZqPsatFZ1BvVkoySuWpVVZfVf/Vnfg7sFh4ocqIn3f7VZ/raLCaTGN8J0fXuCLGRJg4+QhXXIyePwDe+sfmI0CaVLQ9EbkuxKbCPHemdA9akrZYMqEHv6Vt9Nl2CLYoltB3EIHXgYYjUlIohLSohCEI/ZiovliVlALdlaYJGsl2ukUNHwUQRf2x7hHXNBmH9ATqtL9Oby49ovxeMJJz2f+ryAw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [SiteUrl = _t, #"Operation (count)" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"SiteUrl", type text}, {"Operation (count)", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Operation (count)"})
in
    #"Removed Columns"
```


## Roles

### Automotive


Model Permission: Read

Table1

```m
[SiteUrl] == "https://rberger.sharepoint.com/sites/KBase_Automotive/"
```

