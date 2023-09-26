



# M Code

|Dataset|[RAR](./../RAR.md)|
| :--- | :--- |
|Workspace|[Regional Attractivator](../../Workspaces/Regional-Attractivator.md)|

## Table: Analysis


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M711492\OneDrive - Roland Berger Holding GmbH\Documents\RAR-RegionalAttractivator\20221208_test_data_v2.xlsx"), null, true),
    Analysis_Sheet = Quelle{[Item="Analysis",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Analysis_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Country name", type text}, {"Country Code", type text}, {"Cluster", type text}, {"KPI", type text}, {"Average wage per hour value", type number}, {"Unit", type text}, {"Year", Int64.Type}, {"Average wage per hour score", type number}, {"Cluster_1", type text}, {"KPI_2", type text}, {"Average wage per hour in manufacturing value", type number}, {"Unit_3", type text}, {"Year_4", Int64.Type}, {"Average wage per hour (USD) in manufacturing score", type number}, {"Cluster_5", type text}, {"KPI_6", type text}, {"Minimum wage per hour value", type number}, {"Unit_7", type text}, {"Year_8", Int64.Type}, {"Minimum wage per hour (USD) score", type number}, {"Cluster_9", type text}, {"KPI_10", type text}, {"Population density value", type number}, {"Unit_11", type text}, {"Year_12", Int64.Type}, {"Population density score", type number}, {"Cluster_13", type text}, {"KPI_14", type text}, {"Unemployement rate total value", type number}, {"Unit_15", type text}, {"Year_16", Int64.Type}, {"Unemployment score", type number}, {"Cluster_17", type text}, {"KPI_18", type text}, {"Total labor force value", Int64.Type}, {"Unit_19", type text}, {"Year_20", Int64.Type}, {"Total labor force score", type number}, {"Cluster_21", type text}, {"LPI score value", Int64.Type}, {"Unit_22", type text}, {"Year_23", Int64.Type}, {"KPI_24", type text}, {"LPI score score", type number}, {"Cluster_25", type text}, {"KPI_26", type text}, {"Industry electricity price per MWh Value", type number}, {"Unit_27", type text}, {"Year_28", Int64.Type}, {"Industry electricity price per MWh (USD) score", type number}, {"Cluster_29", type text}, {"KPI_30", type text}, {"Density of road nework value", type number}, {"Unit_31", type text}, {"Year_32", Int64.Type}, {"Density of road nework (km/ sq km) score", type number}})
in
    #"Geänderter Typ"
```

