



# M Code

|Dataset|[farewell_V03](./../farewell_V03.md)|
| :--- | :--- |
|Workspace|[Farewell](../../Workspaces/Farewell.md)|

## Table: Source


```m
let
    Quelle = Source_GroupFormExcel,
    #"Umbenannte Spalten" = Table.RenameColumns(Quelle,{{"Please select your current level", "level"}})
in
    #"Umbenannte Spalten"
```


## Table: _measures


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [delete = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"delete", type text}})
in
    #"Geänderter Typ"
```


## Table: Alumni Team career services


```m
let
    Quelle = Source,
    #"Andere entfernte Spalten" = Table.SelectColumns(Quelle,{"ID", "Quality of jobs on Pathfinder job board", "Interaction with Career Advisory (only in DACH region)", "Tips / templates / support provided"}),
    #"Entpivotierte Spalten" = Table.UnpivotOtherColumns(#"Andere entfernte Spalten", {"ID"}, "Attribut", "Wert")
in
    #"Entpivotierte Spalten"
```


## Table: Next career moves


```m
let
    Quelle = Source,
    #"Andere entfernte Spalten" = Table.SelectColumns(Quelle,{"ID", "What does your next career move look like?"}),
    #"Spalte nach Trennzeichen teilen" = Table.ExpandListColumn(Table.TransformColumns(#"Andere entfernte Spalten", {{"What does your next career move look like?", Splitter.SplitTextByDelimiter(";", QuoteStyle.Csv), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "What does your next career move look like?"),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Spalte nach Trennzeichen teilen",{{"What does your next career move look like?", type text}}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Geänderter Typ", each [#"What does your next career move look like?"] <> null and [#"What does your next career move look like?"] <> ""),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Gefilterte Zeilen", "original value", each [#"What does your next career move look like?"], type text),
    #"Ersetzter Wert" = Table.ReplaceValue(#"Hinzugefügte benutzerdefinierte Spalte",each  [original value]
,each if List.Contains({
  "I will pursue my career further in industry",
  "I will work for a client",
  "I will take a role in my family business",
  "I will found or join a start-up/scale-up",
  "I will join a competitor, such as e.g. McK, Bain, BCG, Kearney or Oliver Wyman",
  "I will join a smaller or more specialized consulting firm",
  "I will pursue further my academic career/education",
  "I don't have concrete plans yet and want to take time for re-orientation"
},
Text.Trim([original value])
) then [original value] else "other"

 ,Replacer.ReplaceText,{"What does your next career move look like?"})
in
    #"Ersetzter Wert"
```


## Table: Core motivation to leave


```m
let
    Quelle = Source,
    #"Andere entfernte Spalten" = Table.SelectColumns(Quelle,{"ID", "Project work", "Leadership", "Work-life balance", "Career perspectives", "Compensation", "New opportunity to grow further"}),
    #"Entpivotierte Spalten" = Table.UnpivotOtherColumns(#"Andere entfernte Spalten", {"ID"}, "Attribut", "Wert")
in
    #"Entpivotierte Spalten"
```


## Table: With whom did you discuss


```m
let
    Quelle = Source,
    #"Andere entfernte Spalten" = Table.SelectColumns(Quelle,{"ID", "With whom did you discuss alternative career paths internally?"}),
    #"Spalte nach Trennzeichen teilen" = Table.ExpandListColumn(Table.TransformColumns(#"Andere entfernte Spalten", {{"With whom did you discuss alternative career paths internally?", Splitter.SplitTextByDelimiter(";", QuoteStyle.Csv), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "With whom did you discuss alternative career paths internally?"),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Spalte nach Trennzeichen teilen",{{"With whom did you discuss alternative career paths internally?", type text}}),
    #"Gefilterte Zeilen" = Table.SelectRows(#"Geänderter Typ", each [#"With whom did you discuss alternative career paths internally?"] <> null and [#"With whom did you discuss alternative career paths internally?"] <> ""),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Gefilterte Zeilen", {"With whom did you discuss alternative career paths internally?"}, #"Discuss Partners", {"With whom did you discuss alternative career paths internally?"}, "Discuss Partners", JoinKind.LeftOuter),
    #"Erweiterte Discuss Partners" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "Discuss Partners", {"With whom did you discuss alternative career paths internally?"}, {"whom"}),
    #"Ersetzter Wert" = Table.ReplaceValue(#"Erweiterte Discuss Partners",null,"Other",Replacer.ReplaceValue,{"whom"}),
    #"Ersetzter Wert1" = Table.ReplaceValue(#"Ersetzter Wert",each [#"With whom did you discuss alternative career paths internally?"],each [whom],Replacer.ReplaceText,{"With whom did you discuss alternative career paths internally?"}),
    #"Entfernte Spalten" = Table.RemoveColumns(#"Ersetzter Wert1",{"whom"})
in
    #"Entfernte Spalten"
```


## Table: Exit process


```m
let
    Quelle = Source,
    #"Andere entfernte Spalten" = Table.SelectColumns(Quelle,{"ID", "How did your mentor interact with you in your last weeks?", "How was the communication of your exit handled?", "How was the support from the HR department?", "How was your interaction with the Alumni Team?"}),
    #"Entpivotierte Spalten" = Table.UnpivotOtherColumns(#"Andere entfernte Spalten", {"ID"}, "Attribut", "Wert")
in
    #"Entpivotierte Spalten"
```


## Table: Recommend as employer


```m
let
    Quelle = Source,
    #"Andere entfernte Spalten" = Table.SelectColumns(Quelle,{"ID", "How likely is it that you recommend Roland Berger as employer to a friend or colleague?"}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Andere entfernte Spalten", "Type", each if [#"How likely is it that you recommend Roland Berger as employer to a friend or colleague?"] <= 6 then "Detractors" else if [#"How likely is it that you recommend Roland Berger as employer to a friend or colleague?"] >= 9 then "Promoters" else "Passives", type text)
in
    #"Hinzugefügte benutzerdefinierte Spalte"
```


## Table: Recommend as client


```m
let
    Quelle = Source,
    #"Andere entfernte Spalten" = Table.SelectColumns(Quelle,{"ID", "How likely is it that you recommend Roland Berger as a company to work with as a client?"}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Andere entfernte Spalten", "Type", each if [#"How likely is it that you recommend Roland Berger as a company to work with as a client?"] <= 6 then "Detractors" else if [#"How likely is it that you recommend Roland Berger as a company to work with as a client?"] >= 9 then "Promoters" else "Passives")
in
    #"Hinzugefügte benutzerdefinierte Spalte"
```


## Table: Exit process ratings


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WyssvUUjPz09RSCxRSMzJUdJRMlSK1UGIAwWMwAJQjjGYU5ZaVAmTNoGo10vUA3JMlWJjAQ==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Rating = _t, Sort = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Rating", type text}, {"Sort", Int64.Type}})
in
    #"Geänderter Typ"
```


## Table: alumni team ratings


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WyssvUUjPz09RSCxRSMzJUdJRMlSK1UGIAwWMwAJQjjGYU5ZaVAmTNoGo10vUA3JMlWJjAQ==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Rating = _t, Sort = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Rating", type text}, {"Sort", Int64.Type}})
in
    #"Geänderter Typ"
```


## Table: Core motivation ratings


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WyssvUShKzUktS8wrUdJRMlCK1YlWKkosyUgtQhY3BovnpZaWFCXmAPlGYH5GZnpGTiWyOhNk/WhmGyrFxgIA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Rating = _t, Sort = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Rating", type text}, {"Sort", Int64.Type}})
in
    #"Geänderter Typ"
```


## Table: Months ahead


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMtY1U8jNzyvJKFbSUTJSitWJVoopNTAwTjZGCBuChc10DY0QYsYIpanI4iZg8bzSnBwgx0ApNhYA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Months ahead" = _t, Sort = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Months ahead", type text}})
in
    #"Geänderter Typ"
```


## Table: Core motivations


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("Jcw9DsIwDIbhq1iey8DvBVgRYmOIMoTi0kCJLccl4vZYZX0ffw4BL8pP6g0a6ws7XGPsAp4o3UnrmMXTZklX99WUB4JbmlLpyWW7yDEpkYL4QPxT/lB12/2N30KlJstcPO6XeKYGLMJqc8n2BWN4KDcYZrWR1O8OGOMP", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Motivation = _t, Sort = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Motivation", type text}, {"Sort", Int64.Type}})
in
    #"Geänderter Typ"
```


## Table: Working time


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlbQVTBVqExNLCpW0lEyVorViVYyBIoZwcWMwGIxpQYGxskKhmBhoKghQjQVyQATpdhYAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Years = _t, Sort = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Years", type text}})
in
    #"Geänderter Typ"
```


## Table: Levels


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("Zcu7CgIxEIXhVxmmXhDvtdoJgrBlSDEsYRkJJ5JJCt9+17gWYvv95zjHlwSrsShGOkHiywqt6FxNEcy+xB2v2XeOrxWaMi0nwbtsWvmhbaM+/I93rdxzeoSh0E0gY8iz7xdXDPqUOMvhI5IL2uLI3k8=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Level = _t, Sort = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"Level", type text}, {"Sort", Int64.Type}})
in
    #"Geänderter Typ"
```


## Table: Discuss Partners


```m
let
    Quelle = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("RY49C4MwEIb/ypGpBaHWfs3WDnZqkUIH6xD0qIHkIskp5N83pINww/G897xc24q34hFMAIPE1kGcp3RM6EQm9qLL1osJ0flIi5Vq20sNdRPpYaXNFUo9G1LwQml2lXTRhHJYlLcuwOZWVjU4/CpLYEmHbdSPSb/DoAb6zHleXDjuvp+9B6kZHUlWC0L/L5skjx4UpUDrEBtOqeHBY3r9LLruBw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"With whom did you discuss alternative career paths internally?" = _t, Sort = _t]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{"With whom did you discuss alternative career paths internally?", type text}, {"Sort", Int64.Type}})
in
    #"Geänderter Typ"
```

