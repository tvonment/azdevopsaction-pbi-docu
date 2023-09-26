



# M Code

|Dataset|[IMF Weo Dashboard_v2](./../IMF-Weo-Dashboard_v2.md)|
| :--- | :--- |
|Workspace|[RBI's Dashboards](../../Workspaces/RBI's-Dashboards.md)|

## Table: Sheet1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M710294\Documents\Steffen Geering\Full time\Projekte\Macro & Trends\Economic Indicators\2022_04_Apr\Dashboard\Dashboard_v2.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Country (Group) Name", type text}, {"Subject Descriptor", type text}, {"Subject Descriptor_New", type text}, {"Subject Notes", type text}, {"Units", type text}, {"Scale", type text}, {"Time", Int64.Type}, {"Value", type any}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type","n/a","",Replacer.ReplaceValue,{"Value"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Value",{{"Value", type number}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type1", "date new", each "1/1"),
    #"Merged Columns" = Table.CombineColumns(Table.TransformColumnTypes(#"Added Custom", {{"Time", type text}}, "de-DE"),{"date new", "Time"},Combiner.CombineTextByDelimiter("/", QuoteStyle.None),"Date"),
    #"Replaced Value1" = Table.ReplaceValue(#"Merged Columns","/",".",Replacer.ReplaceText,{"Date"}),
    #"Parsed Date" = Table.TransformColumns(#"Replaced Value1",{{"Date", each Date.From(DateTimeZone.From(_)), type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Parsed Date",{{"Scale", "Scale_orig"}})
in
    #"Renamed Columns"
```

