



# M Code

|Dataset|[PLZ_Berlin_Test](./../PLZ_Berlin_Test.md)|
| :--- | :--- |
|Workspace|[Biomethan-Anlagenregister](../../Workspaces/Biomethan-Anlagenregister.md)|

## Table: Sheet1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M711492\OneDrive - Roland Berger Holding GmbH\development\Biomethan-Anlagenregister\PLZ_Berlin_Test.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"PLZ", Int64.Type}, {"Ort", type text}, {"Ortsteil", type text}, {"Landkreis", type text}, {"Bundesland", type text}, {"CAGR", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"PLZ", "postcode"}})
in
    #"Renamed Columns"
```

