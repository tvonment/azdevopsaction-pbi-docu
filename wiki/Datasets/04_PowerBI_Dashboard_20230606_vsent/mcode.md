



# M Code

|Dataset|[04_PowerBI_Dashboard_20230606_vsent](./../04_PowerBI_Dashboard_20230606_vsent.md)|
| :--- | :--- |
|Workspace|[MAN \| Fixkostenreduktion](../../Workspaces/MAN-\|-Fixkostenreduktion.md)|

## Table: DetailedAnalysis_bi_20230426


```m
let
    Source = Csv.Document(File.Contents("C:\Users\M710216\Documents\3 - Projekte\b - extern\2023\20230411_MAN\01_Rproject_MAN\03_Output\04_detailed_analysis\DetailedAnalysis_bi_20230426.csv"),[Delimiter=";", Columns=39, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"KOSTENART", Int64.Type}, {"TYPE", type text}, {"TEXT", type text}, {"RESSORT", type text}, {"GESELLSCHAFT_ID", type text}, {"GESELLSCHAFT_TEXT", type text}, {"WAEHRUNG", type text}, {"VALUE_IST", type number}, {"VALUE_EUR_SIM", type number}, {"year", Int64.Type}, {"GROUP13", type text}, {"GROUP12", type text}, {"GROUP11", type text}, {"GROUP10", type text}, {"GROUP9", type text}, {"GROUP8", type text}, {"GROUP7", type text}, {"GROUP6", type text}, {"GROUP6_TEXT", type text}, {"GROUP7_TEXT", type text}, {"GROUP8_TEXT", type text}, {"GROUP9_TEXT", type text}, {"GROUP10_TEXT", type text}, {"GROUP11_TEXT", type text}, {"GROUP12_TEXT", type text}, {"GROUP13_TEXT", type text}, {"SOURCE", type text}, {"GROUPAGG", type text}, {"GROUPAGG_TEXT", type text}, {"RESSORT_mod", type text}, {"filter_kag", Int64.Type}, {"filter_ges", Int64.Type}, {"filter_bin", Int64.Type}, {"var_focus_1", Int64.Type}, {"var_focus_2", Int64.Type}, {"GROUPAGG_TEXT_group", type text}, {"var_adressable", Int64.Type}, {"bin_is_hq", Int64.Type}, {"RESSORT_mod_2", type text}})
in
    #"Changed Type"
```


## Table: DetailedAnalysis_cobra_20230426


```m
let
    Source = Csv.Document(File.Contents("C:\Users\M710216\Documents\3 - Projekte\b - extern\2023\20230411_MAN\01_Rproject_MAN\03_Output\04_detailed_analysis\DetailedAnalysis_cobra_20230426.csv"),[Delimiter=";", Columns=21, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"year", Int64.Type}, {"RESSORT_mod", type text}, {"GESELLSCHAFT_ID", type text}, {"TEXT", type text}, {"RESSORT", type text}, {"GESELLSCHAFT_TEXT", type text}, {"VALUE_EUR", type number}, {"filter_kag", Int64.Type}, {"filter_ges", Int64.Type}, {"filter_bin", Int64.Type}, {"VALUE_EUR_2", type number}, {"VALUE_UMSATZ", type number}, {"VALUE_UMSATZ_bin", Int64.Type}, {"VALUE_UMSATZ_GS", type number}, {"VALUE_UMSATZ_SHARE", type number}, {"VALUE_UMSATZ_SHARE_GS", type number}, {"VALUE_UMSATZ__bin_isvertrieb", Int64.Type}, {"MA_GESAMT", Int64.Type}, {"MA_LEIHARBEITER", Int64.Type}, {"MA_GESAMT_LEIHARBEITER", Int64.Type}, {"bin_is_hq", Int64.Type}})
in
    #"Changed Type"
```


## Table: MA_Zahlen


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M710216\Documents\3 - Projekte\b - extern\2023\20230411_MAN\01_Rproject_MAN\01_Data\02_Analysis\Mitarbeiterzahlen\20230419_MA_Zahlen_PowerBI.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"JAHR", Int64.Type}, {"RESSORT", type text}, {"MA_GESAMT", Int64.Type}, {"MA_DIREKT", Int64.Type}, {"MA_INDIREKT", Int64.Type}, {"MA_LEIHARBEITER", Int64.Type}, {"MA_LEIHARBEITER_DIREKT", Int64.Type}, {"MA_LEIHARBEITER_INDIREKT", Int64.Type}})
in
    #"Changed Type"
```


## Table: EDV_Costs_bi_20230504


```m
let
    Source = Csv.Document(File.Contents("C:\Users\M710216\Documents\3 - Projekte\b - extern\2023\20230411_MAN\01_Rproject_MAN\01_Data\11_EDV\04_Output_Dashboard\EDV_Costs_bi_20230504.csv"),[Delimiter=";", Columns=50, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"KOSTENART_classification", type text}, {"year", Int64.Type}, {"KOSTENART", Int64.Type}, {"TYPE", type text}, {"TEXT", type text}, {"RESSORT", type text}, {"GESELLSCHAFT_ID", Int64.Type}, {"GESELLSCHAFT_TEXT", type text}, {"WAEHRUNG", type text}, {"VALUE_IST", type number}, {"VALUE_EUR_SIM", type number}, {"GROUP13", type text}, {"GROUP12", type text}, {"GROUP11", type text}, {"GROUP10", type text}, {"GROUP9", type text}, {"GROUP8", type text}, {"GROUP7", type text}, {"GROUP6", type text}, {"GROUP6_TEXT", type text}, {"GROUP7_TEXT", type text}, {"GROUP8_TEXT", type text}, {"GROUP9_TEXT", type text}, {"GROUP10_TEXT", type text}, {"GROUP11_TEXT", type text}, {"GROUP12_TEXT", type text}, {"GROUP13_TEXT", type text}, {"SOURCE", type text}, {"GROUPAGG", type text}, {"GROUPAGG_TEXT", type text}, {"RESSORT_mod", type text}, {"filter_kag", Int64.Type}, {"filter_ges", Int64.Type}, {"filter_bin", Int64.Type}, {"var_focus_1", Int64.Type}, {"var_focus_2", Int64.Type}, {"GROUPAGG_TEXT_group", type text}, {"var_adressable", Int64.Type}, {"bin_is_hq", Int64.Type}, {"RESSORT_mod_2", Int64.Type}, {"PSP-Element", type text}, {"BusinessService_Objektbezeichnung", type text}, {"Bezeichnung des Gegenkontos", type text}, {"Wert/KWähr", type number}, {"source", type text}, {"value_perc", type number}, {"value_perc_toBI", type number}, {"value_class", Int64.Type}, {"value_perc_class", type number}, {"value_perc_toBI_class", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"source", "source.1"}})
in
    #"Renamed Columns"
```


## Table: DetailedAnalysis_bi_20230505


```m
let
    Source = Csv.Document(File.Contents("C:\Users\M710216\Documents\3 - Projekte\b - extern\2023\20230411_MAN\01_Rproject_MAN\03_Output\04_detailed_analysis\DetailedAnalysis_bi_20230505.csv"),[Delimiter=";", Columns=45, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"GESELLSCHAFT_ID", type text}, {"year", Int64.Type}, {"KOSTENART", Int64.Type}, {"TYPE", type text}, {"TEXT", type text}, {"RESSORT", type text}, {"GESELLSCHAFT_TEXT", type text}, {"WAEHRUNG", type text}, {"VALUE_IST", type number}, {"VALUE_EUR_SIM", type number}, {"GROUP13", type text}, {"GROUP12", type text}, {"GROUP11", type text}, {"GROUP10", type text}, {"GROUP9", type text}, {"GROUP8", type text}, {"GROUP7", type text}, {"GROUP6", type text}, {"GROUP6_TEXT", type text}, {"GROUP7_TEXT", type text}, {"GROUP8_TEXT", type text}, {"GROUP9_TEXT", type text}, {"GROUP10_TEXT", type text}, {"GROUP11_TEXT", type text}, {"GROUP12_TEXT", type text}, {"GROUP13_TEXT", type text}, {"SOURCE", type text}, {"GROUPAGG", type text}, {"GROUPAGG_TEXT", type text}, {"RESSORT_mod", type text}, {"filter_kag", Int64.Type}, {"filter_ges", Int64.Type}, {"filter_bin", Int64.Type}, {"var_focus_1", Int64.Type}, {"var_focus_2", Int64.Type}, {"GROUPAGG_TEXT_group", type text}, {"var_adressable", Int64.Type}, {"bin_is_hq", Int64.Type}, {"RESSORT_mod_2", type text}, {"VALUE_UMSATZ", type number}, {"VALUE_UMSATZ_bin", Int64.Type}, {"VALUE_UMSATZ_GS", type number}, {"VALUE_UMSATZ_SHARE", type number}, {"VALUE_UMSATZ_SHARE_GS", type number}, {"VALUE_UMSATZ__bin_isvertrieb", Int64.Type}})
in
    #"Changed Type"
```

