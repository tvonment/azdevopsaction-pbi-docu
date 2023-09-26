



# M Code

|Dataset|[Portfolio_Dashboard_Juli](./../Portfolio_Dashboard_Juli.md)|
| :--- | :--- |
|Workspace|[EnBW Prio. -Logik](../../Workspaces/EnBW-Prio.--Logik.md)|

## Table: 1a_Kalk_Liste_Hard_Copy_PBI


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M800281\Roland Berger Holding GmbH\ENBW - Wachstumsplattform Wind Onshore - General\06_Phase 2E\03_Neue Priorisierungslogik\01_Regeliterationen\02_ Juli_Iteration\2_Schieberegler\230704_Schieberegler_6_v17.xlsx"), null, true),
    #"1_Kalk_Liste_Sheet" = Quelle{[Item="1a_Kalk_Liste_Hard_Copy_PBI",Kind="Sheet"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(#"1_Kalk_Liste_Sheet",{{"Column1", type any}, {"Column2", type any}, {"Column3", type any}, {"Column4", type any}, {"Column5", type text}, {"Column6", type any}, {"Column7", type any}, {"Column8", type text}, {"Column9", type text}, {"Column10", type any}, {"Column11", type any}, {"Column12", type any}, {"Column13", type any}, {"Column14", type any}, {"Column15", type any}, {"Column16", type any}, {"Column17", type text}, {"Column18", type any}, {"Column19", type any}, {"Column20", type any}, {"Column21", type any}, {"Column22", type any}, {"Column23", type any}, {"Column24", type any}, {"Column25", type text}, {"Column26", type text}, {"Column27", type text}, {"Column28", type text}, {"Column29", type text}, {"Column30", type text}, {"Column31", type any}, {"Column32", type any}, {"Column33", type any}, {"Column34", type text}, {"Column35", type text}, {"Column36", type text}, {"Column37", type text}, {"Column38", type any}, {"Column39", type any}, {"Column40", type any}, {"Column41", type text}, {"Column42", type any}, {"Column43", type any}, {"Column44", type any}, {"Column45", type text}, {"Column46", type any}, {"Column47", type any}, {"Column48", type any}, {"Column49", type text}, {"Column50", type text}, {"Column51", type text}, {"Column52", type any}, {"Column53", type text}, {"Column54", type text}, {"Column55", type text}, {"Column56", type any}, {"Column57", type text}, {"Column58", type text}, {"Column59", type text}, {"Column60", type any}, {"Column61", type text}, {"Column62", type text}, {"Column63", type text}, {"Column64", type any}, {"Column65", type text}, {"Column66", type text}, {"Column67", type text}, {"Column68", type any}, {"Column69", Int64.Type}, {"Column70", type any}, {"Column71", type any}, {"Column72", type any}, {"Column73", type text}, {"Column74", type text}, {"Column75", type any}, {"Column76", type any}, {"Column77", type any}, {"Column78", type any}, {"Column79", type any}}),
    #"Entfernte oberste Zeilen" = Table.Skip(#"Geänderter Typ",6),
    #"Entfernte Spalten" = Table.RemoveColumns(#"Entfernte oberste Zeilen",{"Column69"}),
    #"Höher gestufte Header" = Table.PromoteHeaders(#"Entfernte Spalten", [PromoteAllScalars=true]),
    #"Geänderter Typ2" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Realisierungs.-P", Percentage.Type}}),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Geänderter Typ2",{{"RG Ganz", "RG_Ganzzahl"}}),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Umbenannte Spalten",{{"Kalk. Wert", Int64.Type}, {"NPV", Int64.Type}, {"Plan Abschluss", type date}, {"Leistung", type number}, {"IRR", type number}, {"WACC", type number}, {"WEA", Int64.Type}}),
    #"Ersetzte Fehler" = Table.ReplaceErrorValues(#"Geänderter Typ1", {{"Region2", "O"}})
in
    #"Ersetzte Fehler"
```

