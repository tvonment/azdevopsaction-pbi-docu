



# M Code

|Dataset|[20210621_FWP Reporting_v33_basis mit Slide 3 _ online datasource](./../20210621_FWP-Reporting_v33_basis-mit-Slide-3-_-online-datasource.md)|
| :--- | :--- |
|Workspace|[FWP Support](../../Workspaces/FWP-Support.md)|

## Table: Calculated_KPIs (2)


```m
let
    Quelle = File_Dataset,
    Calculated_KPIs_Sheet = Quelle{[Item="Calculated_KPIs",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Calculated_KPIs_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"ID", type text}, {"Reportingperiode", type text}, {"KW", type text}, {"00_7_BU/PC [31.01.]", type any}, {"00_1_2Employee ID", type any}, {"00_4_Org.-unit#(lf)[31.01.21]", type any}, {"00_5_1. OrgEinh-Kürzel [31.01.]", type any}, {"Org_Unit_1", type text}, {"Org_Unit_2", type text}, {"Org_Unit_3", type text}, {"Org_Unit_all", type text}, {"Ziel", Int64.Type}, {"Kandidaten_Laufende_Gespräche_Org", Int64.Type}, {"Annahmewahrscheinlichkeit_Org", type number}, {"Bestätigter_Austritt_Org", Int64.Type}, {"Zielerreichung_Lücke", type number}, {"Ziellücke_Org", type number}, {"KPI_1_Zielerreichung_Org_Unit_3", type number}, {"KPI_1_MinWert", Int64.Type}, {"KPI_1_Mid1Wert", type number}, {"KPI_1_Mid2Wert", Int64.Type}, {"KPI_1_MaxWert", type number}, {"Anzahl_Gespräche_KW23", Int64.Type}, {"Anzahl_Gespräche_KW25", Int64.Type}, {"Anzahl_Gespräche_KW27", Int64.Type}, {"Anzahl_Gespräche_KW29", Int64.Type}, {"Anzahl_Gespräche_KW31", Int64.Type}, {"Anzahl_Gespräche_KW33", Int64.Type}, {"Anzahl_Gespräche_KW35", Int64.Type}, {"Anzahl_Gespräche_Geplant_KW23", Int64.Type}, {"Anzahl_Gespräche_Geplant_KW25", Int64.Type}, {"Anzahl_Gespräche_Geplant_KW27", Int64.Type}, {"Anzahl_Gespräche_Geplant_KW29", Int64.Type}, {"Anzahl_Gespräche_Geplant_KW31", Int64.Type}, {"Anzahl_Gespräche_Geplant_KW33", Int64.Type}, {"Anzahl_Gespräche_Geplant_KW35", Int64.Type}, {"Anzahl_Annahmen_KW23", Int64.Type}, {"Anzahl_Annahmen_KW25", Int64.Type}, {"Anzahl_Annahmen_KW27", Int64.Type}, {"Anzahl_Annahmen_KW29", Int64.Type}, {"Anzahl_Annahmen_KW31", Int64.Type}, {"Anzahl_Annahmen_KW33", Int64.Type}, {"Anzahl_Annahmen_KW35", Int64.Type}, {"KPI_1_Zielerreichung_Org_Unit_1", type number}, {"KPI_1_Zielerreichung_Org_Unit_2", type number}}),
    #"Geänderter Typ mit Gebietsschema" = Table.TransformColumnTypes(#"Geänderter Typ", {{"KPI_1_Zielerreichung_Org_Unit_1", type number}}, "de-DE"),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Geänderter Typ mit Gebietsschema",{{"Zielerreichung_Lücke", type number}, {"Ziellücke_Org", type number}, {"KPI_1_Zielerreichung_Total", type number}})
in
    #"Geänderter Typ1"
```


## Table: Processed_data (2)


```m
let
    Quelle = File_Dataset,
    Processed_data_Sheet = Quelle{[Item="Processed_data",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Processed_data_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"ID", type text}, {"Reportingperiode", type text}, {"KW", type text}, {"00_1_Employee ID", type text}, {"00_1_2Employee ID", type text}, {"00_2_Vorname", type text}, {"00_3_Nachname", type text}, {"00_4_Org.-unit#(lf)[31.01.21]", type text}, {"00_5_1. OrgEinh-Kürzel [31.01.]", type text}, {"00_7_BU/PC [31.01.]", type text}, {"Org_Unit_1", type text}, {"Org_Unit_2", type text}, {"Org_Unit_3", type text}, {"Org_Unit_all", type text}, {"PMO_check", Int64.Type}, {"Gespräch_01", Int64.Type}, {"Gespräch_02", Int64.Type}, {"Gespräch_03", Int64.Type}, {"Gespräch_04", Int64.Type}, {"Gespräch_05", Int64.Type}, {"Gespräch_06", Int64.Type}, {"Anzahl_Gespräche", Int64.Type}, {"Status", type text}, {"Annahmewahrscheinlichkeit", type number}, {"Überwiegender_Ablehnungsgrund", type text}, {"Austrittsdatum", type date}, {"Nächstes Gespräch", type date}, {"Annahmedatum", type date}, {"Kandidat_counter", Int64.Type}, {"Phasenstatus", type text}, {"Pipeline_Umsetzungswahrscheinlichkeit", type text}, {"Unterschrieben", Int64.Type}, {"Bestätigter_Austritt", Int64.Type}, {"Reifegrad_Individuell", Int64.Type}, {"Reifegrad_Max", Int64.Type}, {"Reifegrad_KPI", Int64.Type}, {"Ziel", Int64.Type}}),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Geänderter Typ",{{"00_1_Employee ID", type text}, {"00_1_2Employee ID", type text}}),
    #"Duplizierte Spalte" = Table.DuplicateColumn(#"Geänderter Typ1", "Status", "Status - Kopie"),
    #"Ersetzter Wert" = Table.ReplaceValue(#"Duplizierte Spalte","Identifiziert","01_Identifiziert",Replacer.ReplaceText,{"Status - Kopie"}),
    #"Ersetzter Wert1" = Table.ReplaceValue(#"Ersetzter Wert","Angebot übergeben","02_Angebot übergeben",Replacer.ReplaceText,{"Status - Kopie"}),
    #"Ersetzter Wert2" = Table.ReplaceValue(#"Ersetzter Wert1","Aufhebungsvertrag übergeben","03_Aufhebungsvertrag übergeben",Replacer.ReplaceText,{"Status - Kopie"}),
    #"Ersetzter Wert3" = Table.ReplaceValue(#"Ersetzter Wert2","Abgeschlossen: Annahme","04_Abgeschlossen: Annahme",Replacer.ReplaceText,{"Status - Kopie"}),
    #"Ersetzter Wert4" = Table.ReplaceValue(#"Ersetzter Wert3","Abgeschlossen: Ablehnung","05_Abgeschlossen: Ablehnung",Replacer.ReplaceText,{"Status - Kopie"}),
    #"Pivotierte Spalte" = Table.Pivot(#"Ersetzter Wert4", List.Distinct(#"Ersetzter Wert4"[Status]), "Status", "Status", List.Count),
    #"Umbenannte Spalten" = Table.RenameColumns(#"Pivotierte Spalte",{{"0", "Status: 0"}, {"Angebot übergeben", "Status: Angebot übergeben"}, {"Aufhebungsvertrag übergeben", "Status: Aufhebungsvertrag übergeben"}, {"Identifiziert", "Status: Identifiziert"}, {"Abgeschlossen: Ablehnung", "Status: Abgeschlossen: Ablehnung"}, {"Abgeschlossen: Annahme", "Staus: Abgeschlossen: Annahme"}, {"Unterschrieben", "Dummy_Unterschrieben"}}),
    #"Duplizierte Spalte1" = Table.DuplicateColumn(#"Umbenannte Spalten", "Phasenstatus", "Phasenstatus - Kopie"),
    #"Pivotierte Spalte1" = Table.Pivot(#"Duplizierte Spalte1", List.Distinct(#"Duplizierte Spalte1"[Phasenstatus]), "Phasenstatus", "Phasenstatus", List.Count),
    #"Duplizierte Spalte2" = Table.DuplicateColumn(#"Pivotierte Spalte1", "Pipeline_Umsetzungswahrscheinlichkeit", "Pipeline_Umsetzungswahrscheinlichkeit - Kopie"),
    #"Umbenannte Spalten1" = Table.RenameColumns(#"Duplizierte Spalte2",{{"0", "Phases: 0"}}),
    #"Pivotierte Spalte2" = Table.Pivot(#"Umbenannte Spalten1", List.Distinct(#"Umbenannte Spalten1"[Pipeline_Umsetzungswahrscheinlichkeit]), "Pipeline_Umsetzungswahrscheinlichkeit", "Pipeline_Umsetzungswahrscheinlichkeit", List.Count),
    #"Umbenannte Spalten2" = Table.RenameColumns(#"Pivotierte Spalte2",{{"0", "Pipeline_0"}}),
    #"Duplizierte Spalte3" = Table.DuplicateColumn(#"Umbenannte Spalten2", "Überwiegender_Ablehnungsgrund", "Überwiegender_Ablehnungsgrund - Kopie"),
    #"Pivotierte Spalte3" = Table.Pivot(#"Duplizierte Spalte3", List.Distinct(#"Duplizierte Spalte3"[Überwiegender_Ablehnungsgrund]), "Überwiegender_Ablehnungsgrund", "Überwiegender_Ablehnungsgrund", List.Count),
    #"Summe eingefügt" = Table.AddColumn(#"Pivotierte Spalte3", "Addition", each List.Sum({[#"Status: Angebot übergeben"], [#"Status: Aufhebungsvertrag übergeben"], [#"Status: Identifiziert"], [#"Status: Abgeschlossen: Ablehnung"], [#"Staus: Abgeschlossen: Annahme"]}), type number),
    #"Geänderter Typ2" = Table.TransformColumnTypes(#"Summe eingefügt",{{"Annahmewahrscheinlichkeit", type number}})
in
    #"Geänderter Typ2"
```


## Table: Status


```m
let
    Quelle = File_data_helper,
    Status_Sheet = Quelle{[Item="Status",Kind="Sheet"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(Status_Sheet,{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}}),
    #"Höher gestufte Header" = Table.PromoteHeaders(#"Geänderter Typ", [PromoteAllScalars=true]),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Status", type text}, {"Phasenstatus", type text}, {"Pipeline_Umsetzungswahrscheinlichkeit", type text}}),
    #"Ersetzter Wert" = Table.ReplaceValue(#"Geänderter Typ1",null,"0",Replacer.ReplaceValue,{"Pipeline_Umsetzungswahrscheinlichkeit"})
in
    #"Ersetzter Wert"
```


## Table: Überwiegender Ablehnungsgrund


```m
let
    Quelle = File_data_helper,
    #"Überwiegender Ablehnungsgrund_Sheet" = Quelle{[Item="Überwiegender Ablehnungsgrund",Kind="Sheet"]}[Data],
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Überwiegender Ablehnungsgrund_Sheet",{{"Column1", type text}}),
    #"Höher gestufte Header" = Table.PromoteHeaders(#"Geänderter Typ", [PromoteAllScalars=true]),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Überwiegender Ablehnungsgrund", type text}})
in
    #"Geänderter Typ1"
```


## Table: Reportingperiode


```m
let
    Quelle = File_data_helper,
    Reportingperiode_Sheet = Quelle{[Item="Reportingperiode",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Reportingperiode_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"KW", type text}, {"Reportingperiode", type text}, {"Timeline_Filter", type text}})
in
    #"Geänderter Typ"
```


## Table: Seite2_Anzahl_Annahmen


```m
let
    Quelle = File_data_helper,
    Seite2_Anzahl_Annahmen_Sheet = Quelle{[Item="Seite2_Anzahl_Annahmen",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Seite2_Anzahl_Annahmen_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Timeline_Filter_KW_Annahmen", type text}, {"Shown_on_Chart_Anzahl_Annahmen", type text}})
in
    #"Geänderter Typ"
```


## Table: Seite3_Anzahl_Gespräche_Geplant


```m
let
    Quelle = File_data_helper,
    Seite3_Anzahl_Gespräche_Geplant_Sheet = Quelle{[Item="Seite3_Anzahl_Gespräche_Geplant",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Seite3_Anzahl_Gespräche_Geplant_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Timeline_Filter_KW_Anzahl_Gespräche", type text}, {"Shown_on_Chart_Anzahl_Gespräche_Geplant", type text}})
in
    #"Geänderter Typ"
```


## Table: Seite3_Anzahl_Gespräche


```m
let
    Quelle = File_data_helper,
    Seite3_Anzahl_Gespräche_Sheet = Quelle{[Item="Seite3_Anzahl_Gespräche",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Seite3_Anzahl_Gespräche_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Timeline_Filter_KW_Anzahl_Gespräche", type text}})
in
    #"Geänderter Typ"
```


## Parameter: FileName_dataset


i.e. 20210613_Dataset.xlsx

```m
"20210613_Dataset.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Parameter: FileName_helper_data


i. e. Helper_data_v4.xlsx

```m
"Helper_data_v4.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

