



# M Code

|Dataset|[Dashboard_BI_ESG-Banking_v11](./../Dashboard_BI_ESG-Banking_v11.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: df_summary_NACE1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_summary_NACE1.xlsx"), null, true),
    df_summary_NACE1_Sheet = Source{[Item="df_summary_NACE1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(df_summary_NACE1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"sector", type text}, {"DarlehenID", Int64.Type}, {"Umsatz[€]", type number}, {"Saldo[€]", type number}, {"Bilanzsumme[€]", type number}, {"Scope 1-Emissionen[tCO2e]", type number}, {"Scope 2-Emissionen[tCO2e]", type number}, {"Scope 3-Emissionen[tCO2e]", type number}, {"Summe Emissionen[tCO2e]", type number}, {"Finanzierte Scope 1-Emissionen[tCO2e]", type number}, {"Finanzierte Scope 2-Emissionen[tCO2e]", type number}, {"Finanzierte Scope 3-Emissionen[tCO2e]", type number}, {"Summe finanzierte Emissionen[tCO2e]", type number}, {"Emission_Antel_der_Branche", Percentage.Type}, {"Saldo_Anteil_der_Branche", Percentage.Type}})
in
    #"Changed Type"
```


## Table: Emission_zu_Saldo_Total1


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\Emission_zu_Saldo_Total1.xlsx"), null, true),
    Emission_zu_Saldo_Total1_Sheet = Source{[Item="Emission_zu_Saldo_Total1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Emission_zu_Saldo_Total1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"GLS", type number}, {"Ihre Bank", type number}, {"Differenz%", Percentage.Type}})
in
    #"Changed Type"
```


## Table: Emission_zu_Saldo_Total2


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\Emission_zu_Saldo_Total2.xlsx"), null, true),
    Emission_zu_Saldo_Total2_Sheet = Source{[Item="Emission_zu_Saldo_Total2",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Emission_zu_Saldo_Total2_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Banks", type text}, {"Emission_zu_Saldo", type number}})
in
    #"Changed Type"
```


## Table: df_ghg_intensity_DE


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_ghg_intensity_DE.xlsx"), null, true),
    df_ghg_intensity_DE_Sheet = Source{[Item="df_ghg_intensity_DE",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(df_ghg_intensity_DE_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"region", type text}, {"sector", type text}, {"GHG_emissions", type number}, {"Value Added", type number}, {"Output", type number}, {"GHG_intensity (Output)", type number}, {"GHG_intensity (Value Added)", type number}, {"sector_Adj", type text}, {"Emission_Rank", Int64.Type}})
in
    #"Changed Type"
```


## Table: df_final_ghg_intensity


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_final_ghg_intensity.xlsx"), null, true),
    df_final_ghg_intensity_Sheet = Source{[Item="df_final_ghg_intensity",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(df_final_ghg_intensity_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"sector", type text}, {"Scope 1-Intensität", type number}, {"Scope 2-Intensität", type number}, {"Scope 3-Intensität", type number}, {"Gesamtintensität", type number}})
in
    #"Changed Type"
```


## Table: df_summary_NACE2


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_summary_NACE2.xlsx"), null, true),
    df_summary_NACE2_Sheet = Source{[Item="df_summary_NACE2",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(df_summary_NACE2_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"sector_Adj", type text}, {"DarlehenID", Int64.Type}, {"Umsatz[€]", type number}, {"Saldo[€]", type number}, {"Bilanzsumme[€]", type number}, {"Scope 1-Emissionen[tCO2e]", type number}, {"Scope 2-Emissionen[tCO2e]", type number}, {"Scope 3-Emissionen[tCO2e]", type number}, {"Summe Emissionen[tCO2e]", type number}, {"Finanzierte Scope 1-Emissionen[tCO2e]", type number}, {"Finanzierte Scope 2-Emissionen[tCO2e]", type number}, {"Finanzierte Scope 3-Emissionen[tCO2e]", type number}, {"Summe finanzierte Emissionen[tCO2e]", type number}, {"Emission_Rank", Int64.Type}, {"Emission_Antel_der_Branche", type number}, {"Saldo_Anteil_der_Branche", type number}, {"Anteil finanzierter Emissionen Scope 1 an Gesamtemissionen", type number}})
in
    #"Changed Type"
```


## Table: df_branche_companies_emissionen


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_branche_companies_emissionen.xlsx"), null, true),
    df_branche_companies_emissionen_Sheet = Source{[Item="df_branche_companies_emissionen",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(df_branche_companies_emissionen_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"region", type text}, {"sector", type text}, {"GHG_emissions", type number}, {"Value Added", type number}, {"Output", type number}, {"GHG_intensity (Output)", type number}, {"GHG_intensity (Value Added)", type number}, {"sector_Adj", type text}, {"Emission_Rank", Int64.Type}, {"Scope 1-Emissionen[tCO2e]", type number}, {"Scope 2-Emissionen[tCO2e]", type number}, {"Scope 3-Emissionen[tCO2e]", type number}, {"Summe Emissionen[tCO2e]", type number}})
in
    #"Changed Type"
```


## Table: df_darlehen_portfolio


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_darlehen_portfolio.xlsx"), null, true),
    df_darlehen_portfolio_Sheet = Source{[Item="df_darlehen_portfolio",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(df_darlehen_portfolio_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"sector", type text}, {"DarlehenID", Int64.Type}, {"Umsatz[€]", type number}, {"Saldo[€]", type number}, {"Bilanzsumme[€]", type number}, {"Anteil[%]", type number}, {"Scope 1-Intensität", type number}, {"Scope 2-Intensität", type number}, {"Scope 3-Intensität", type number}, {"Gesamtintensität", type number}, {"Code", type text}, {"Scope 1-Emissionen[tCO2e]", type number}, {"Scope 2-Emissionen[tCO2e]", type number}, {"Scope 3-Emissionen[tCO2e]", type number}, {"Summe Emissionen[tCO2e]", type number}, {"Finanzierte Scope 1-Emissionen[tCO2e]", type number}, {"Finanzierte Scope 2-Emissionen[tCO2e]", type number}, {"Finanzierte Scope 3-Emissionen[tCO2e]", type number}, {"Summe finanzierte Emissionen[tCO2e]", type number}, {"Branche", type text}, {"Description", type text}, {"Bezeichnung", type text}, {"sector_Adj", type text}})
in
    #"Changed Type"
```


## Table: df_indicator_dictionary


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_indicator_dictionary.xlsx"), null, true),
    df_indicator_dictionary_Sheet = Source{[Item="df_indicator_dictionary",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(df_indicator_dictionary_Sheet,{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"Level", type text}, {"Indicator", type text}, {"Definition", type text}})
in
    #"Changed Type1"
```


## Table: df_benchmark_dictionary


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_benchmark_dictionary.xlsx"), null, true),
    df_benchmark_dictionary_Sheet = Source{[Item="df_benchmark_dictionary",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(df_benchmark_dictionary_Sheet,{{"Column1", type text}, {"Column2", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"Benchmark", type text}, {"Definition", type text}})
in
    #"Changed Type1"
```


## Table: df_summary_NACE2_Timeseries


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_summary_NACE2_Timeseries.xlsx"), null, true),
    df_summary_NACE2_Timeseries_Sheet = Source{[Item="df_summary_NACE2_Timeseries",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(df_summary_NACE2_Timeseries_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"sector", type text}, {"DarlehenID", Int64.Type}, {"Umsatz[€]", type number}, {"Saldo[€]", type number}, {"Bilanzsumme[€]", type number}, {"Scope 1-Emissionen[tCO2e]", type number}, {"Scope 2-Emissionen[tCO2e]", type number}, {"Scope 3-Emissionen[tCO2e]", type number}, {"Summe Emissionen[tCO2e]", type number}, {"Finanzierte Scope 1-Emissionen[tCO2e]", type number}, {"Finanzierte Scope 2-Emissionen[tCO2e]", type number}, {"Finanzierte Scope 3-Emissionen[tCO2e]", type number}, {"Summe finanzierte Emissionen[tCO2e]", type number}, {"Emission_Rank", Int64.Type}, {"sector_Adj", type text}, {"Branche", type text}, {"Description", type text}, {"Bezeichnung", type text}, {"Emission_Antel_der_Branche", type number}, {"Saldo_Anteil_der_Branche", type number}, {"Anteil finanzierter Emissionen Scope 1 an Gesamtemissionen", type number}, {"Jahr", Int64.Type}, {"Land", type text}, {"Finanzierte CO2-Emissionen zu Kreditsaldo [tCO2/EUR Mio]", type number}})
in
    #"Changed Type"
```


## Table: df_summary_NACE2_Time_total


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712715\Desktop\Climate Impact Assessment-Dashboard\df_summary_NACE2_Time_total.xlsx"), null, true),
    df_summary_NACE2_Time_total_Sheet = Source{[Item="df_summary_NACE2_Time_total",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(df_summary_NACE2_Time_total_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Jahr", Int64.Type}, {"Summe finanzierte Emissionen[tCO2e]", type number}, {"Saldo[€]", type number}, {"Gesamte Finanzierte CO2-Emissionen zu Kreditsaldo [tCO2/EUR Mio]", type number}})
in
    #"Changed Type"
```

