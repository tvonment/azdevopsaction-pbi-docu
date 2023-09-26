



# M Code

|Dataset|[Gateway_Test](./../Gateway_Test.md)|
| :--- | :--- |
|Workspace|[Sawaher-Test](../../Workspaces/Sawaher-Test.md)|

## Table: Sheet1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\vishn\OneDrive\Documents\Market_Radar_Attributes.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Sheet1_Sheet,{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}})
in
    #"Changed Type"
```

