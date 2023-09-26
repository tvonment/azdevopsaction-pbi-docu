



# M Code

|Dataset|[International iNorm](./../International-iNorm.md)|
| :--- | :--- |
|Workspace|[Clorox Data](../../Workspaces/Clorox-Data.md)|

## Table: wipes_dim Wide


```m
let
    Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="SELECT * FROM#(lf)(select * , ROW_NUMBER() OVER(PARTITION BY [Product Key] ORDER BY [Product Key]) AS DUPLICATE_CNT from #(lf)(select  #(lf)[Product] as 'Product',#(lf)[Country] as 'Country',#(lf)[Business_Unit] as 'Business_Unit',#(lf)[Clorox_Category_Value] as 'BU',#(lf)[Clorox_Sub_Category_Value] as 'Clorox Sub Category Value',#(lf)[Clorox_Segment_Value] as 'Clorox Segment Value',#(lf)[Clorox_Manufacturer_Value] as 'Clorox Manufacturer Value',#(lf)[Clorox_Brand_Value] as 'Clorox Brand Value',#(lf)[Clorox_SubBrand_Value] as 'Clorox SubBrand Value',#(lf)[Clorox_Type_Value] as 'Clorox Type Value',#(lf)[Clorox_Sub_Type_Value] as 'Clorox Sub Type Value',#(lf)[Product_Key] as 'Product Key',#(lf)[Size_Final] as 'Clorox Size Value',#(lf)[Pack_Size_Range] as 'Clorox Size Range Value',#(lf)[Pack_Size_Range_idx] as 'Index size range',#(lf)[Refresh_Period2] as 'Refresh_Period2', #(lf)[Size_Calc] as 'Size Calc',#(lf)dense_rank() over(order by CAST(substring (Refresh_Period2,3,2) as int)*100+CAST(substring (Refresh_Period2,6,2) as int) desc) AS rank_x#(lf)from nrm.POS_DIM_TEST_INTL#(lf))A#(lf)where  A.rank_x <=3 #(lf))B#(lf)WHERE B.DUPLICATE_CNT = 1"]),
    #"Changed Type" = Table.TransformColumnTypes(#"Source",{{"BU", type text}, {"Product", type text}, {"Clorox Sub Category Value", type text}, {"Clorox Segment Value", type text}, {"Clorox Manufacturer Value", type text}, {"Clorox Brand Value", type text}, {"Clorox SubBrand Value", type text}, {"Clorox Type Value", type text}, {"Clorox Sub Type Value", type text},{"Product Key", type text}, {"Clorox Size Value", type text}, {"Clorox Size Range Value", type text}, {"Index size range", Int64.Type}, {"Refresh_Period2", type text}, {"Size Calc", type number}}),
    #"Inserted Text Before Delimiter" = Table.AddColumn(#"Changed Type", "Text Before Delimiter", each Text.BeforeDelimiter([Clorox Size Value], " "), type text),
    #"Renamed Columns1" = Table.RenameColumns(#"Inserted Text Before Delimiter",{{"Text Before Delimiter", "SizeCalcOld"}}),
    #"Replaced Val" = Table.ReplaceValue(#"Renamed Columns1","ALL",null,Replacer.ReplaceValue,{"SizeCalcOld"}),
   #"Added Conditional Column" = Table.AddColumn(#"Replaced Val", "New Clorox Brand Value", each if [Clorox Manufacturer Value] = "CLOROX" then "Clorox" else [Clorox Brand Value]),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Conditional Column",{{"Index size range", Int64.Type}, {"Size Calc", type number}}),
#"Added Custom" = Table.AddColumn(#"Changed Type3", "test_brand", each if([Country]="HKG" or [Country]="MYS" or[Country]="SKR")  and( [BU]="BLEACH"  or [BU]="LA"  or [BU]= "CW" or [BU]="FP" ) and ( [Clorox Brand Value]= "Clorox" or [Clorox Brand Value] = "Glad" or [Clorox Brand Value] = "Rox" or [Clorox Brand Value]= "Yuhangen") then "Clorox"
 else if 
([Country]="ARG" or [Country]="CHI" or[Country]="PAN" or [Country]="PER" or [Country]="PUR")  and([Clorox Sub Category Value] ="Color LA" or [Clorox Sub Category Value] = "Disinfecting CW" or [Clorox Sub Category Value] = "Disinfecting Sprays" or [Clorox Sub Category Value] = "Gel Bleach" or [Clorox Sub Category Value] = "Heavy-Duty (HD) LSC" or [Clorox Sub Category Value] = "Light-Duty (LD) LSC" or [Clorox Sub Category Value] = "Liquid Bleach" or [Clorox Sub Category Value] = "White LA"  ) and ( [Clorox Brand Value]="Ayudin" or [Clorox Brand Value]="Poett" or [Clorox Brand Value]="Pine Sol" or [Clorox Brand Value]= "Mistolin" or [Clorox Brand Value]= "Clorox Clorogel") then "Clorox"
else if 
([Country]="COL" or [Country]="CHI" or[Country]="PAN" or [Country]="PER" or [Country]="CRC" or [Country]="ECU")  and ([Clorox Sub Category Value] ="Color LA" or [Clorox Sub Category Value] = "Disinfecting CW" or [Clorox Sub Category Value] = "Gel Bleach" or [Clorox Sub Category Value] = "Liquid Bleach" or [Clorox Sub Category Value] = "White LA"  ) and ( [Clorox Brand Value]="Clorox" or [Clorox Brand Value]="Clorox Ropa Blanca" or [Clorox Brand Value]="Clorox Cloro Gel") then "Clorox"
else if 
([Country]="MEX")  and([Clorox Sub Category Value] ="Color LA" or [Clorox Sub Category Value] = "Disinfecting CW" or [Clorox Sub Category Value] = "Non-Disinfecting CW" or [Clorox Sub Category Value] = "Gel Bleach" or [Clorox Sub Category Value] = "Heavy-Duty (HD) LSC" or [Clorox Sub Category Value] = "Light-Duty (LD) LSC" or [Clorox Sub Category Value] = "Liquid Bleach" or [Clorox Sub Category Value] = "White LA"  ) and ( [Clorox Brand Value]="Clorox" or [Clorox Brand Value]="Poett" or [Clorox Brand Value]="Green Works") then "Clorox"
else if 
([Country]="PUR")  and([Clorox Sub Category Value] ="Color LA" or [Clorox Sub Category Value] = "Disinfecting CW" or [Clorox Sub Category Value] = "Non-Disinfecting CW" or [Clorox Sub Category Value] = "Liquid Bleach" or [Clorox Sub Category Value] = "White LA"  ) and ( [Clorox Brand Value]="Clorox") then "Clorox"
else if
[Business_Unit] ="AMEA" and ([Clorox Brand Value] ="Chux" or [Clorox Brand Value]="Glad To Be Green" or [Clorox Brand Value] ="Clorox" or [Clorox Brand Value]="Glad") then "Clorox"
else if 
[Country]="CND" and ([Clorox Brand Value]="Pine Sol" or [Clorox Brand Value]="Brita" or [Clorox Brand Value] ="Clorox") then "Clorox"
else [Clorox Brand Value]),
    #"Renamed Columns2" = Table.RenameColumns(#"Added Custom",{{"New Clorox Brand Value", "test brand"}, {"test_brand", "New Clorox Brand Value"}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Renamed Columns2", "Clorox Brand Value", "Clorox Brand Value - Copy"),
    #"Renamed Columns3" = Table.RenameColumns(#"Duplicated Column",{{"Clorox Brand Value - Copy", "Brand Universal"}}),
    #"Added Custom1" = Table.AddColumn(#"Renamed Columns3", "Division", each [Business_Unit]),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Custom1", "Country-Name", each if [Country] = "UK" then "United Kingdom" else if [Country] = "CHI" then "Chile" else if [Country] = "COL" then "Colombia" else if [Country] = "ECU" then "Ecuador" else if [Country] = "MEX" then "Mexico" else if [Country] = "PAN" then "Panama" else if [Country] = "PER" then "Peru" else if [Country] = "PUR" then "Puerto Rico" else if [Country] = "RSA" then "South Africa" else if [Country] = "SKR" then "South Korea" else if [Country] = "ARG" then "Argentina" else if [Country] = "AUS" then "Australia" else if [Country] = "CND" then "Canada" else if [Country] = "CRC" then "Costa Rica" else if [Country] = "HKG" then "Hong Kong" else if [Country] = "KSA" then "Saudi Arabia" else if [Country] = "NZL" then "New Zealand" else if [Country] = "UAE" then "United Arab Emirates" else if [Country] = "MYS" then "Malaysia" else if [Country] = "CHN" then "China" else [Country]),
    #"Added Custom2" = Table.AddColumn(#"Added Conditional Column1", "Size_range Key", each Text.Combine({[Country], "-", [BU], "-", [Clorox Sub Category Value],"-",[Clorox Size Range Value]})),
    #"Merged Queries" = Table.NestedJoin(#"Added Custom2", {"Size_range Key"}, Pack_Size_Range_description, {"size_Key "}, "Pack_Size_Range_description", JoinKind.LeftOuter),
    #"Expanded Pack_Size_Range_description" = Table.ExpandTableColumn(#"Merged Queries", "Pack_Size_Range_description", {"Description"}, {"Description"})
in
    #"Expanded Pack_Size_Range_description"
```


## Table: wipes_val Wide


```m
let

    Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[Clorox_Category_Value] as 'BU',#(lf)[Refresh_Period] as 'Refreshed Period',#(lf)[Periodicity] as 'Periodicity',#(lf)[Geography] as 'Retailer',#(lf)[Dollar_Sales] as '$',#(lf)[Volume_Sales] as 'Volume Sales',#(lf)[Unit_Sales] as 'Units',#(lf)[Average_Weekly_Total_Points_of_Distribution] as 'TDP',#(lf)[Product_Key] as 'Product Key',#(lf)[Time] as 'Time',#(lf)[Dol_per_vol] as '$ / oz_All SKUs',#(lf)[Price_per_vol_rng] as 'Price per vol rng',#(lf)[Price_per_vol_rng_idx] as 'Price per vol rng idx',#(lf)[Refresh_Period2] as 'Refresh Period 2'#(lf)from (select *,#(lf)dense_rank() over(#(lf)order by CAST(substring (Refresh_Period2,3,2) as int)*100+CAST(substring (Refresh_Period2,6,2) as int) desc) AS rank_x#(lf)from nrm.POS_VAL_TEST_INTL) ranks#(lf)where rank_x<=3#(lf)"]),
    #"Changed Type" = Table.TransformColumnTypes(#"Source",{{"BU", type text}, {"Refreshed Period", type text}, {"Periodicity", type text}, {"Retailer", type text}, {"$", type number}, {"Volume Sales", type number}, {"Units", type number},{"TDP", Int64.Type},{"Product Key", type text}, {"Time", type text}, {"$ / oz_All SKUs", type number}, {"Price per vol rng", type text}, {"Price per vol rng idx", type text}, {"Refresh Period 2", type text}}),
    #"Inserted date from Time column" = Table.AddColumn(#"Changed Type", "Date", each Text.End([Time], 8), type text),
    #"Changed Type with Locale" = Table.TransformColumnTypes(#"Inserted date from Time column", {{"Date", type date}}, "en-US"),
    #"Inserted Year" = Table.AddColumn(#"Changed Type with Locale", "Year", each Date.Year([Date]), Int64.Type),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Year",{{"Year", Int64.Type}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Changed Type1", "Merged", each Text.Combine({[Retailer], "_", [Time],"_",[Product Key],"_",[Refresh Period 2]})),
    #"Added Conditional Column" = Table.AddColumn(#"Inserted Merged Column", "Retailer Rank", each if [Retailer] = "MT" then 1 else if [Retailer] = "TT" then 2 else if [Retailer] = "Total" then 3 else 4),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Conditional Column",{{"Retailer Rank", Int64.Type}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type2", "RP sort rank", each (Number.From (Text.Middle([Refresh Period 2], 2, 2))as number)*100 + (Number.From (Text.Middle([Refresh Period 2], 5,2
))as number) ++ (Number.From (Text.Middle([Refreshed Period], 7,2
))as number)),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Custom",{{"RP sort rank", Int64.Type}})
in
    #"Changed Type3"
```


## Table: continue_BItable


```m
let
     Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[Year] as 'Year',#(lf)[Business_Unit] as 'Business Unit',#(lf)[Country] as 'Country',#(lf)[Clorox_Category_Value] as 'Clorox Category Value',#(lf)[Clorox_Sub_Category_Value] as 'Clorox Sub Category Value',#(lf)#(lf)[Time] as 'Time',#(lf)[Retailer] as 'Retailer',#(lf)[Product_Key] as 'Product Key',#(lf)[PY] as 'PY',#(lf)[PY-1] as 'PY-1', #(lf)[Refresh_Period] as 'Refresh_Period2'#(lf) from (select *,#(lf)dense_rank() over(#(lf)order by CAST(substring (Refresh_Period,3,2) as int)*100+CAST(substring (Refresh_Period,6,2) as int) desc) AS rank_x#(lf)from nrm.POS_CONTINUE_FLG_TEST_INTL) ranks#(lf)where rank_x<=3#(lf)"]),
    #"Changed Type" = Table.TransformColumnTypes(#"Source",{{"Year", Int64.Type}, {"Time", type text}, {"Retailer", type text}, {"Product Key", type text}, {"PY", type text}, {"PY-1", type text}, {"Refresh_Period2", type text}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Changed Type", "Merged", each Text.Combine({[Retailer], "_", [Time],"_",[Product Key],"_",[Refresh_Period2]}))
in
    #"Inserted Merged Column"
```


## Table: py_table


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUQpOzE1VCEgtysxPUYhMTSxScEzPV4rViVYyQpM0AksXQ+RjAQ==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Value = _t, Period = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Value", Int64.Type}})
in
    #"Changed Type"
```


## Table: measures_table


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: date_table


```m
let
    Source = #"wipes_val Wide",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"Refreshed Period", "Year"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Duplicates",{{"Year", Int64.Type}})
in
    #"Changed Type"
```


## Table: Measure_Table2


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: Revenue Drivers


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8i9KT8zLTFYITsxJLVbwyUwrUYrViVYKKMpMTlXwzS9LzU3NKykGi/mllit4lqTmQniOxcX5RSUgWQXnjMS89FSIcFBqWWpeaapSbCwA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Drivers = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Drivers", type text}})
in
    #"Changed Type"
```


## Table: swot_data_nr


```m
let
 Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[Business_Unit] as 'Business Unit',#(lf)[Country] as 'Country',#(lf)[Clorox_Category_Value] as 'BU',#(lf)[Clorox_Sub_Category_Value] as 'Clorox Sub Category Value',#(lf)[Geography] as 'Retailer',#(lf)[Clorox_Brand_Value] as 'Clorox Brand Value'#(lf)from nrm.POS_SWOT_TEST_INTL#(lf)"]),
    #"Removed Blank Rows" = Table.SelectRows(Source, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Blank Rows",{{"BU", type text}, {"Clorox Sub Category Value", type text}, {"Retailer", type text}, {"Clorox Brand Value", type text}}),
    #"Added Conditional Column" = Table.AddColumn(#"Changed Type1", "Country-Name", each if [Country] = "UK" then "United Kingdom" else if [Country] = "CHI" then "Chile" else if [Country] = "COL" then "Colombia" else if [Country] = "ECU" then "Ecuador" else if [Country] = "MEX" then "Mexico" else if [Country] = "PAN" then "Panama" else if [Country] = "PER" then "Peru" else if [Country] = "PUR" then "Puerto Rico" else if [Country] = "RSA" then "South Africa" else if [Country] = "SKR" then "South Korea" else if [Country] = "ARG" then "Argentina" else if [Country] = "AUS" then "Australia" else if [Country] = "CND" then "Canada" else if [Country] = "CRC" then "Costa Rica" else if [Country] = "HKG" then "Hong Kong" else if [Country] = "KSA" then "Saudi Arabia" else if [Country] = "NZL" then "New Zealand" else if [Country] = "UAE" then "United Arab Emirates" else if [Country] = "MYS" then "Malaysia" else [Country])

    in
    #"Added Conditional Column"
```


## Table: Measure Table 3


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Measure Table 3" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Measure Table 3", type text}})
in
    #"Changed Type"
```


## Table: Pack_Size_Range_description


```m
let
    Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01"),
    nrm_Pack_Size_Range_description = Source{[Schema="nrm",Item="Pack_Size_Range_description"]}[Data],
 #"Inserted Merged Column" = Table.AddColumn(#"nrm_Pack_Size_Range_description", "size_Key ", each Text.Combine({[Country], "-", [Clorox_Category_Value], "-", [Clorox_Sub_Category_Value],"-",[Pack_Size_Range]})),
    #"Removed Duplicates" = Table.Distinct(#"Inserted Merged Column", {"size_Key "})
in
    #"Removed Duplicates"
```

