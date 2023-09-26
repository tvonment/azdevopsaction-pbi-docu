



# M Code

|Dataset|[Test Dataset](./../Test-Dataset.md)|
| :--- | :--- |
|Workspace|[Test FZr - DEV](../../Workspaces/Test-FZr---DEV.md)|

## Table: Table


```m
let
  Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
  #"Changed column type" = Table.TransformColumnTypes(Source, {{"Column1", type number}})
in
  #"Changed column type"

```

