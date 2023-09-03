



# M Code

## Table: Hersteller


```m
let
    Quelle = Excel.Workbook(File.Contents(Pfad & "AccessDB.xlsx"), null, true),
    _Hersteller = Quelle{[Item="Hersteller", Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(_Hersteller,{{"Hersteller ID", Int64.Type}, {"Hersteller Name", type text}})
in
    #"Geänderter Typ"
```
## Table: Kalender


```m
let
    Quelle = Excel.Workbook(File.Contents(Pfad & "AccessDB.xlsx"), null, true),
    _Kalender = Quelle{[Item="Kalender",Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(_Kalender,{{"Jahr", Int64.Type}, {"Datum", type date}, {"Tag", Int64.Type}, {"Monat ", type text}, {"Monat Nr", Int64.Type}, {"Quartal", type text}})
in
    #"Geänderter Typ"
```
## Table: Produkte


```m
let
    Quelle = Excel.Workbook(File.Contents(Pfad & "AccessDB.xlsx"), null, true),
    _Produkte = Quelle{[Item="Produkte", Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(_Produkte,{{"Produkt ID", Int64.Type}, {"Produktname", type text}, {"Kategorie", type text}, {"Segment", type text}, {"Hersteller ID", Int64.Type}, {"Hersteller Name", type text}})
in
    #"Geänderter Typ"
```
## Table: Geo


```m
let
    Quelle = Excel.Workbook(File.Contents(Pfad & "AccessDB.xlsx"), null, true),
    _Geo = Quelle{[Item="Geo", Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(_Geo,{{"Stadt", type text}, {"Staat", type text}, {"Region", type text}, {"Distrikt", type text}, {"Land", type text}}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Geänderter Typ", each true)
in
    #"Gefilterte Zeilen"
```
## Table: Sales


```m
let
    Quelle = Table.Combine({#"US Sales", #"International Sales"}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(Quelle, "Ländername", each if [Land] = null then "USA" else [Land]),
    #"Entfernte Spalten" = Table.RemoveColumns(#"Hinzugefügte benutzerdefinierte Spalte",{"Land"})
in
    #"Entfernte Spalten"
```
## Table: StatDatum


```m
#date(2019, 1, 1) meta [IsParameterQuery=true, Type="Date", IsParameterQueryRequired=true]
```
## Table: Einwohnerzahlen


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\Einwohnerzahlen.xlsx"), null, false),
    Einwohnerzahlen_sheet = Quelle{[Item="Einwohnerzahlen",Kind="Sheet"]}[Data],
    #"Entfernte oberste Zeilen" = Table.Skip(Einwohnerzahlen_sheet,4),
    #"Höher gestufte Header" = Table.PromoteHeaders(#"Entfernte oberste Zeilen", [PromoteAllScalars=true]),
    #"Entpivotierte andere Spalten" = Table.UnpivotOtherColumns(#"Höher gestufte Header", {"Land"}, "Attribut", "Wert"),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Entpivotierte andere Spalten",{{"Attribut", "Jahr"}, {"Wert", "Einwohnerzahl"}}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Umbenannte Spalten",{{"Jahr", Int64.Type}, {"Einwohnerzahl", Int64.Type}})
in
    #"Geänderter Typ"
```
## Parameter: Parameter1


```m
Beispieldatei meta [IsParameterQuery=true, BinaryIdentifier=Beispieldatei, Type="Binary", IsParameterQueryRequired=true]
```
## Parameter: Pfad


```m
"C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\" meta [IsParameterQuery=true, List={"C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\"}, DefaultValue="C:\Users\boesc\OneDrive\Desktop\Power BI Demo Content\Demo Data\", Type="Text", IsParameterQueryRequired=true]
```