



# M Code

## Table: Einwohnerzahlen


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\Einwohnerzahlen.xlsx"), null, false),
    Einwohnerzahlen_sheet = Quelle{[Item="Einwohnerzahlen",Kind="Sheet"]}[Data],
    #"Entfernte oberste Zeilen" = Table.Skip(Einwohnerzahlen_sheet,4),
    #"Höher gestufte Header" = Table.PromoteHeaders(#"Entfernte oberste Zeilen", [PromoteAllScalars=true]),
    #"Entpivotierte andere Spalten" = Table.UnpivotOtherColumns(#"Höher gestufte Header", {"Land"}, "Attribut", "Wert"),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Entpivotierte andere Spalten",{{"Attribut", "Jahr"}, {"Wert", "Einwohnerzahl"}}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Umbenannte Spalten", "Berechnete Spalte in M", each if [Land] = "Deutschland" then "DACH" else "-"),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Hinzugefügte benutzerdefinierte Spalte",{{"Einwohnerzahl", Int64.Type}, {"Jahr", Int64.Type}, {"Berechnete Spalte in M", type text}})
in
    #"Geänderter Typ"
```
## Table: Geo


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\AccessDB.xlsx"), null, true),
    Geo_Table = Quelle{[Item="Geo",Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(Geo_Table,{{"PLZ", type text}, {"Stadt", type text}, {"Staat", type text}, {"Region", type text}, {"Distrikt", type text}, {"Land", type text}})
in
    #"Geänderter Typ"
```
## Parameter: Parameter_SingleValue


Parameter mit einem Wert

```m
"Parameterwert als Text" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```
## Parameter: Parameter_List


Parameter mit Liste von Werten die ausgewählt werden können

```m
#date(2023, 1, 1) meta [IsParameterQuery=true, List={#date(2023, 1, 1), #date(2022, 1, 1), #date(2021, 1, 1)}, DefaultValue=#date(2023, 1, 1), Type="Date", IsParameterQueryRequired=true]
```