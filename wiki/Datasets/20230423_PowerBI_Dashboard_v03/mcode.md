



# M Code

|Dataset|[20230423_PowerBI_Dashboard_v03](./../20230423_PowerBI_Dashboard_v03.md)|
| :--- | :--- |
|Workspace|[MAN \| Fixkostenreduktion](../../Workspaces/MAN-\|-Fixkostenreduktion.md)|

## Table: DetailedAnalysis_cobra_20230425_2


```m
let
    Source = Csv.Document(File.Contents("C:\Users\M710216\Documents\3 - Projekte\b - extern\2023\20230411_MAN\01_Rproject_MAN\03_Output\04_detailed_analysis\DetailedAnalysis_cobra_20230425_2.csv"),[Delimiter=";", Columns=15, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"year", Int64.Type}, {"RESSORT_mod", type text}, {"TEXT", type text}, {"RESSORT", type text}, {"GESELLSCHAFT_ID", type text}, {"GESELLSCHAFT_TEXT", type text}, {"VALUE_EUR", type number}, {"filter_kag", Int64.Type}, {"filter_ges", Int64.Type}, {"filter_bin", Int64.Type}, {"VALUE_EUR_2", type number}, {"VALUE_UMSATZ", Int64.Type}, {"MA_GESAMT", Int64.Type}, {"MA_LEIHARBEITER", Int64.Type}, {"MA_GESAMT_LEIHARBEITER", Int64.Type}}),
    #"Rounded Off" = Table.TransformColumns(#"Changed Type",{{"VALUE_EUR_2", each Number.Round(_, 0), type number}})
in
    #"Rounded Off"
```


## Table: DetailedAnalysis_bi_20230425


```m
let
    Source = Csv.Document(File.Contents("C:\Users\M710216\Documents\3 - Projekte\b - extern\2023\20230411_MAN\01_Rproject_MAN\03_Output\04_detailed_analysis\DetailedAnalysis_bi_20230425.csv"),[Delimiter=";", Columns=37, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"KOSTENART", Int64.Type}, {"TYPE", type text}, {"TEXT", type text}, {"RESSORT", type text}, {"GESELLSCHAFT_ID", type text}, {"GESELLSCHAFT_TEXT", type text}, {"WAEHRUNG", type text}, {"VALUE_IST", type number}, {"VALUE_EUR_SIM", type number}, {"year", Int64.Type}, {"GROUP13", type text}, {"GROUP12", type text}, {"GROUP11", type text}, {"GROUP10", type text}, {"GROUP9", type text}, {"GROUP8", type text}, {"GROUP7", type text}, {"GROUP6", type text}, {"GROUP6_TEXT", type text}, {"GROUP7_TEXT", type text}, {"GROUP8_TEXT", type text}, {"GROUP9_TEXT", type text}, {"GROUP10_TEXT", type text}, {"GROUP11_TEXT", type text}, {"GROUP12_TEXT", type text}, {"GROUP13_TEXT", type text}, {"SOURCE", type text}, {"GROUPAGG", type text}, {"GROUPAGG_TEXT", type text}, {"RESSORT_mod", type text}, {"filter_kag", Int64.Type}, {"filter_ges", Int64.Type}, {"filter_bin", Int64.Type}, {"var_focus_1", Int64.Type}, {"var_focus_2", Int64.Type}, {"GROUPAGG_TEXT_group", type text}, {"var_adressable", Int64.Type}})
in
    #"Changed Type"
```


## Table: DetailedAnalysis_cobra_20230425_3


```m
let
    Source = Csv.Document(File.Contents("C:\Users\M710216\Documents\3 - Projekte\b - extern\2023\20230411_MAN\01_Rproject_MAN\03_Output\04_detailed_analysis\DetailedAnalysis_cobra_20230425_3.csv"),[Delimiter=";", Columns=16, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"year", Int64.Type}, {"RESSORT_mod", type text}, {"TEXT", type text}, {"RESSORT", type text}, {"GESELLSCHAFT_ID", type text}, {"GESELLSCHAFT_TEXT", type text}, {"VALUE_EUR", type number}, {"filter_kag", Int64.Type}, {"filter_ges", Int64.Type}, {"filter_bin", Int64.Type}, {"VALUE_EUR_2", type number}, {"VALUE_UMSATZ", Int64.Type}, {"MA_GESAMT", Int64.Type}, {"MA_LEIHARBEITER", Int64.Type}, {"MA_GESAMT_LEIHARBEITER", Int64.Type}, {"VALUE_UMSATZ_SHARE", Int64.Type}})
in
    #"Changed Type"
```

