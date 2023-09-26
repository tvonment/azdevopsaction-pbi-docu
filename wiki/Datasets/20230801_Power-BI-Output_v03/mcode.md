



# M Code

|Dataset|[20230801_Power BI Output_v03](./../20230801_Power-BI-Output_v03.md)|
| :--- | :--- |
|Workspace|[1,000 Assets](../../Workspaces/1,000-Assets.md)|

## Table: Asset


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\m711272\Roland Berger Holding GmbH\Decarbonize 1000 emittents - General\01_Analyses\06_Power BI\20230731_Power BI Output_v02.xlsx"), null, true),
    Asset_Sheet = Quelle{[Item="Asset",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Asset_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Ranking", Int64.Type}, {"Name", type text}, {"Latitude", type number}, {"Longitude", type number}, {"Region", type text}, {"Country", type text}, {"Sector", type text}, {"Asset type", type text}, {"Lifetime", type number}, {"CO2 intensity", type number}, {"Full load hours ", type number}, {"CO2 emission [m t]", type number}, {"Energy generation", type number}, {"Capacity", type number}}),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Geänderter Typ", {"Ranking"}, Solutions, {"Ranking"}, "Soltuion", JoinKind.FullOuter)
in
    #"Zusammengeführte Abfragen"
```


## Table: Solutions


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\m711272\Roland Berger Holding GmbH\Decarbonize 1000 emittents - General\01_Analyses\06_Power BI\20230731_Power BI Output_v02.xlsx"), null, true),
    Soltuion_Sheet = Quelle{[Item="Soltuion",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Soltuion_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Ranking", Int64.Type}, {"Name", type text}, {"Solution", type text}, {"CO2 reduction [%]", Percentage.Type}, {"CO2 reduction", type number}, {"Residue CO2", type number}, {"Lifetime", type number}, {"Equivalent capacity ratio", type number}, {"CAPEX, disc.", type number}, {"OPEX, disc.", type number}, {"Fuel cost, disc.", type number}, {"TOTEX, disc.", type number}, {"Integration cost, disc.", type number}, {"System costs, disc.", type number}, {"CO2 abatement costs w/o decarbonization", type number}, {"CO2 abatement costs after decarbonization", type number}, {"Total costs of CO2 avoided", type number}, {"Total costs of CO2 avoided per t", type number}, {"Applicability", type text}, {"Required Installed Capacity", type number}})
in
    #"Geänderter Typ"
```


## Table: Sort Solutions


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUXJ2VorViVYyAjLdE4vBbGMg2680OSc1sQjMNwHyg1LzUssTk3JSgUpiAQ==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Sort Order" = _t, Value = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Sort Order", Int64.Type}, {"Value", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Value", "Solution sorted"}})
in
    #"Renamed Columns"
```


## Table: Images


```m
let
    Source = SharePoint.Files("https://rberger.sharepoint.com/sites/1000AssetsResearch/", [ApiVersion = 15]),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Folder Path] = "https://rberger.sharepoint.com/sites/1000AssetsResearch/Shared Documents/General/01_Asset pictures/")),
    #"Added Custom1" = Table.AddColumn(#"Filtered Rows", "ImageURL", each [Folder Path]&[Name]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom1",{{"ImageURL", type text}}),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Changed Type", "Name", Splitter.SplitTextByDelimiter("_", QuoteStyle.None), {"Name.1", "Name.2"}),
    #"Renamed Columns" = Table.RenameColumns(#"Split Column by Delimiter",{{"Name.1", "Ranking"}})
in
    #"Renamed Columns"
```


## Table: Metadata


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m711272\Roland Berger Holding GmbH\Decarbonize 1000 emittents - General\01_Analyses\06_Power BI\20230731_Power BI Output_v02.xlsx"), null, true),
    Metadata_Sheet = Source{[Item="Metadata",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Metadata_Sheet, [PromoteAllScalars=true]),
    #"Replaced Value2" = Table.ReplaceValue(#"Promoted Headers",null,"n/a",Replacer.ReplaceValue,{"Net-zero plan [Y/N]"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Replaced Value2",{{"Share, parent 1", Percentage.Type}, {"Share, parent 2", Percentage.Type}, {"Share, parent 3", Percentage.Type}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",null,0,Replacer.ReplaceValue,{"Share, parent 2"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"Share, parent 3"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Value1",{{"Share, parent 3", Percentage.Type}, {"Share, parent 2", Percentage.Type}}),
    #"Replaced Value3" = Table.ReplaceValue(#"Changed Type1",null,"n/a",Replacer.ReplaceValue,{"Parent company 2"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3",null,"n/a",Replacer.ReplaceValue,{"Parent company 3"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4",null,"n/a",Replacer.ReplaceValue,{"Refurbishments/updates_1"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5",null,"n/a",Replacer.ReplaceValue,{"Net-zero plan"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value6",null,"n/a",Replacer.ReplaceValue,{"Decommissioning_2"})
in
    #"Replaced Value7"
```


## Table: Assumptions


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m711272\Roland Berger Holding GmbH\Decarbonize 1000 emittents - General\01_Analyses\06_Power BI\20230731_Power BI Output_v02.xlsx"), null, true),
    Assumptions_Sheet = Source{[Item="Assumptions",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Assumptions_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Ranking", Int64.Type}, {"Region", type text}, {"Country", type text}, {"Interest rate", type number}, {"CO2 abatement costs", type number}, {"Green H2 price", type number}, {"Natural gas price", type number}, {"National CO2 neutrality target", type number}})
in
    #"Changed Type"
```

