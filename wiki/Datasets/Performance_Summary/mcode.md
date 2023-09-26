



# M Code

|Dataset|[Performance_Summary](./../Performance_Summary.md)|
| :--- | :--- |
|Workspace|[Test_4_Michael_Mueller](../../Workspaces/Test_4_Michael_Mueller.md)|

## Table: Sheet1


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M711087\Desktop\PowerBI Dummies.xlsx"), null, true),
    Sheet1_Sheet = Quelle{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Employee", type text}, {"Platform", type text}, {"Country", type text}, {"Rank", type text}, {"Utilization target", type number}, {"Utilization_week 0", type number}})
in
    #"Geänderter Typ"
```

