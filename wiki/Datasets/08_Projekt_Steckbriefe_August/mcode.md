



# M Code

|Dataset|[08_Projekt_Steckbriefe_August](./../08_Projekt_Steckbriefe_August.md)|
| :--- | :--- |
|Workspace|[EnBW Prio. -Logik](../../Workspaces/EnBW-Prio.--Logik.md)|

## Table: Steckbrief_Data


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M713614\Roland Berger Holding GmbH\ENBW - Wachstumsplattform Wind Onshore - General\06_Phase 2E\03_Neue Priorisierungslogik\01_Regeliterationen\09_September_Iteration\2_Schieberegler\230905_Schieberegler_Sep_v31.xlsx"), null, true),
    Table19_Table = Quelle{[Item="Steckbrief_Data",Kind="Table"]}[Data],
    #"Entfernte leere Zeilen" = Table.SelectRows(Table19_Table, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Entfernte leere Zeilen",{{"ProjectID", type text}, {"Projektname", type text}, {"Projektleiter/in", type text}, {"Aktueller RG", type text}, {"Datum akt. RG", type date}, {"FC nächster RG", type date}, {"Geplante IBN", type date}, {"Aktueller NPV", type number}, {"IRR", Currency.Type}, {"WACC", Currency.Type}, {"Anzahl WEAS", Int64.Type}, {"WEA Anlagentyp", type text}, {"Leistung", type number}, {"Bundesland", type text}, {"Wirt_comment_1", type text}, {"Wirt_comment_2", type text}, {"Pl_comment_1", type text}, {"Pl_comment_2", type text}, {"Wirtschaftlichkeitsampel", Int64.Type}, {"Planungsrechtampel ", Int64.Type}, {"Zeitplanampel", Int64.Type}, {"ZP_comment_1", type text}, {"ZP_comment_2", type text}, {"CR_comment_1", type text}, {"Ab1_WTräger", type text}, {"Ab1_text", type text}, {"Ab2_WTräger", type text}, {"Ab2_text", type text}, {"kalk. laufzeit", type text}}),
    #"Entfernte Fehler" = Table.RemoveRowsWithErrors(#"Geänderter Typ", {"kalk. laufzeit"})
in
    #"Entfernte Fehler"
```


## Table: Data_Tank


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M713614\Roland Berger Holding GmbH\ENBW - Wachstumsplattform Wind Onshore - General\06_Phase 2E\03_Neue Priorisierungslogik\01_Regeliterationen\09_September_Iteration\2_Schieberegler\230905_Schieberegler_Sep_v31.xlsx"), null, true),
    Data_Tank_Table = Quelle{[Item="Data_Tank",Kind="Table"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(Data_Tank_Table,{{"Projektname", type text}, {"AbweichungID", Int64.Type}, {"Aktueller RG", type number}, {"Projektleiter", type text}, {"Team", type text}, {"Red Flag", type any}, {"Abweichung SR", type text}, {"Abweichung ZP", type any}, {"Forecast_RG7", type any}, {"Ist_Abweichung", type text}, {"Einschätzung", type any}, {"Regler Wert", type any}, {"In PBI", type text}, {"Bucket Berechnet", type text}, {"Abweichung neu?", type text}, {"helper", type any}, {"ID_Data_Tank", type text}, {"Monat", type date}, {"Einschätzung durch", type text}, {"Schieberegler", Int64.Type}, {"Begründung Regler", type text}, {"Grundlage", type text}, {"Planungsrecht", type text}, {"Begründung PR", type text}, {"NPV", type text}, {"IRR", type text}, {"WACC", type text}, {"Kalk Laufzeit", type text}, {"WindBG", type text}, {"Wirtschaftlichkeitskommentar", type text}, {"Zeitplan", type text}, {"Begründung Zeitplan", type text}, {"Chancen & Risiken", type text}, {"Aktuelle Bearbeitung", type text}})
in
    #"Geänderter Typ"
```

