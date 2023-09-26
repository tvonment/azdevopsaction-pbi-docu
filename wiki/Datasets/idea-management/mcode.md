



# M Code

|Dataset|[idea management](./../idea-management.md)|
| :--- | :--- |
|Workspace|[Test FZr - APP](../../Workspaces/Test-FZr---APP.md)|

## Table: New Requests


```m
let
    Source = #"New Requests (Backup SP List)"
in
    Source
```


## Table: DimCategory


```m
let
    Source = #"DimCategory (Backup)"
in
    Source
```


## Table: RequestsToCategory


```m
let
    Source = #"RequestsToCategory (backup)"
in
    Source
```


## Table: DimDataSecurity


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8ssvUSguSSwqSU1RitWJVvLMUygoyk8vSi0uBvNdyxJzShNhsqV5eanJQKnEokql2FgA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Data Security" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Data Security", type text}})
in
    #"Changed Type"
```


## Table: DimITSecurity


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8ssvUSguSSwqSU1RitWJVvLMUygoyk8vSi0uBvNdyxJzShNhsoGlmcnZyRmpydlQgdK8vNRkoNrEokql2FgA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"IT Security" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"IT Security", type text}})
in
    #"Changed Type"
```


## Table: DimInfrastructure


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8ssvUSguSSwqSU1RitWJVvLMUygoyk8vSi0uBvNdyxJzShNhsqV5eanJQKnEokql2FgA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Infrastructure = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Infrastructure", type text}})
in
    #"Changed Type"
```


## Table: DimClassification


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCs1LzkksLs5My0xNUYrViVZyzMnJL09NUSjNKy4tKMgvKkETRxV1yUzPLEnMUQjPL8ouyElMToWIpuaBjYsFAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Classification = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Classification", type text}})
in
    #"Changed Type"
```


## Table: Suggestions


```m
let
    Source = #"Suggestions (Backup)"
in
    Source
```

