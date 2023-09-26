



# M Code

|Dataset|[Projekt_Steckbriefe](./../Projekt_Steckbriefe.md)|
| :--- | :--- |
|Workspace|[EnBW Prio. -Logik](../../Workspaces/EnBW-Prio.--Logik.md)|

## Table: Table19 (2)


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M714518\Roland Berger Holding GmbH\ENBW - Wachstumsplattform Wind Onshore - General\05_Phase 2D\04_Presentations\02_Neue Priologik\04_Skalierung\2_Schieberegler\230524_Schieberegler_4_v7.xlsx"), null, true),
    Table19_Table = Quelle{[Item="Table19",Kind="Table"]}[Data],
    #"Entfernte leere Zeilen" = Table.SelectRows(Table19_Table, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Entfernte Fehler" = Table.RemoveRowsWithErrors(#"Entfernte leere Zeilen", {"ProjectID"}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Entfernte Fehler",{{"ProjectID", type text}, {"Projektname", type text}, {"Projektleiter/in", type text}, {"Aktueller RG", type text}, {"Datum akt. RG", type date}, {"FC nächster RG", type date}, {"Geplante IBN", type date}, {"Aktueller NPV", type number}, {"IRR", Currency.Type}, {"WACC", Currency.Type}, {"Anzahl WEAS", Int64.Type}, {"WEA Anlagentyp", type text}, {"Leistung", type number}, {"Bundesland", type text}, {"Wirt_comment_1", type text}, {"Wirt_comment_2", type text}, {"Pl_comment_1", type text}, {"Pl_comment_2", type text}, {"Wirtschaftlichkeitsampel", Int64.Type}, {"Planungsrechtampel ", Int64.Type}, {"Zeitplanampel", Int64.Type}, {"ZP_comment_1", type text}, {"ZP_comment_2", type text}, {"CR_comment_1", type text}, {"Ab1_WTräger", type text}, {"Ab1_text", type text}, {"Ab2_WTräger", type text}, {"Ab2_text", type text}, {"kalk. laufzeit", Int64.Type}})
in
    #"Geänderter Typ"
```


## Table: Data_Tank


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M714518\Roland Berger Holding GmbH\ENBW - Wachstumsplattform Wind Onshore - General\05_Phase 2D\04_Presentations\02_Neue Priologik\04_Skalierung\2_Schieberegler\230524_Schieberegler_4_v7.xlsx"), null, true),
    Data_Tank_Table = Quelle{[Item="Data_Tank",Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(Data_Tank_Table,{{"Projektname", type text}, {"AbweichungID", Int64.Type}, {"Aktueller RG", type number}, {"Projektleiter", type text}, {"Team", type text}, {"Red Flag", type any}, {"Abweichung SR", type text}, {"Abweichung ZP", type any}, {"Forecast_RG7", type any}, {"Ist_Abweichung", type text}, {"Einschätzung", type any}, {"Regler Wert", type any}, {"helper", type any}, {"ID", type text}, {"Monat", type date}, {"Einschätzung durch", type text}, {"Schieberegler", Int64.Type}, {"Begründung Regler", type text}, {"Planungsrecht", type text}, {"Begründung PR", type text}, {"NPV", type text}, {"Begründung NPV", type any}, {"IRR", type text}, {"Begründung IRR", type any}, {"Zeitplan", type text}, {"Begründung Zeitplan", type text}, {"QG", type any}, {"Begründung QG Sprung", Int64.Type}, {"WACC", type any}, {"Begründung WACC", type any}, {"Aktuelle Bearbeitung", type text}})
in
    #"Geänderter Typ"
```

