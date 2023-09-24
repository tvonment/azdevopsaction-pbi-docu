



# M Code

|Dataset|[test - Kopie](./../test---Kopie.md)|
| :--- | :--- |
|Workspace|[Power BI Report Documentation Test Workspace PremiumPB](../../Workspaces/Power-BI-Report-Documentation-Test-Workspace-PremiumPB.md)|

## Table: Population


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\Population.xlsx"), null, false),
    Population_sheet = Source{[Item="Sheet Population",Kind="Sheet"]}[Data],
    FilterNullAndWhitespace = each List.Select(_, each _ <> null and (not (_ is text) or Text.Trim(_) <> "")),
    #"Removed Top Rows" = Table.Skip(Population_sheet, each try List.IsEmpty(List.Skip(FilterNullAndWhitespace(Record.FieldValues(_)), 1)) otherwise false),
    #"Removed Blank Rows" = Table.SelectRows(#"Removed Top Rows", each not List.IsEmpty(FilterNullAndWhitespace(Record.FieldValues(_)))),
    #"Removed Top Rows1" = Table.Skip(#"Removed Blank Rows",2),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Top Rows1", [PromoteAllScalars=true]),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Promoted Headers", {"Country"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Other Columns",{{"Attribute", "Year"}, {"Value", "Population"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Population", Int64.Type}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: Calendar


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Calendar_Table = Source{[Item="Calendar",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Calendar_Table,{{"Date", type date}, {"Day", Int64.Type}, {"Month", type text}, {"Month Nr.", Int64.Type}, {"Quarter", type text}, {"Year", Int64.Type}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: Geo


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Geo_Table = Source{[Item="Geo",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Geo_Table,{{"Postalcode", type text}, {"City", type text}, {"State", type text}, {"Region", type text}, {"District", type text}, {"Country", type text}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: Manufacturers


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Manufacturers_Table = Source{[Item="Manufacturers",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Manufacturers_Table,{{"Manufacturer ID", Int64.Type}, {"Manufacturer Name", type text}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: Products


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\boesc\Corporate Software AG\Coso-Kursunterlagen - Documents\General\CorporateSoftware-Kursunterlagen\PowerBI\MPBI01\MPBI01 - English\MPBI01 Übungen EN 2023\TN\Data\AccessDB.xlsx"), null, true),
    Products_Table = Source{[Item="Products",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Products_Table,{{"Product ID", Int64.Type}, {"Name", type text}, {"Category", type text}, {"Segment", type text}, {"Manufacturer ID", Int64.Type}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: Sales


```m
let
    Source = Table.Combine({#"US Sales", #"International Sales"}),
    #"Added Custom" = Table.AddColumn(Source, "Country name", each if [Country] = null then "USA" else [Country]),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"Country"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"Country name", type text}, {"Amount", Int64.Type}, {"Product ID", Int64.Type}, {"Postalcode", type text}, {"Revenue", type number}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Parameter: Parameter1


```m
#"Sample File" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File", Type="Binary", IsParameterQueryRequired=true]
```

OpenAI API Key is not configured