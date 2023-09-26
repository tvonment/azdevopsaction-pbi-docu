



# M Code

|Dataset|[Always On iNorm Speciality](./../Always-On-iNorm-Speciality.md)|
| :--- | :--- |
|Workspace|[Project Evolve](../../Workspaces/Project-Evolve.md)|

## Table: wipes_dim Wide


```m
let
    Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="SELECT * FROM#(lf)(select * , ROW_NUMBER() OVER(PARTITION BY [Product Key] ORDER BY [Product Key]) AS DUPLICATE_CNT from #(lf)(select  #(lf)[Product] as 'Product',#(lf)[Clorox_Category_Value] as 'Clorox Category Value',#(lf)[Clorox_Sub_Category_Value] as 'Sub_Cat_IRI',#(lf)[Clorox_Segment_Value] as 'Clorox Segment Value',#(lf)[Clorox_Manufacturer_Value] as 'Clorox Manufacturer Value',#(lf)[Clorox_Brand_Value] as 'Clorox Brand Value',#(lf)[Clorox_SubBrand_Value] as 'Clorox SubBrand Value',#(lf)[Clorox_Type_Value] as 'Clorox Type Value',#(lf)[Clorox_Sub_Type_Value] as 'Clorox Sub Type Value',#(lf)[Clorox_Pack_Type_Value] as 'Clorox Pack Type Value',#(lf)[Clorox_Size_Value] as 'Size_IRI',#(lf)[Clorox_Deal_Pack_Value] as 'Clorox Deal Pack Value',#(lf)[EAN_14] as 'EAN_14',#(lf)[Product_Key] as 'Product Key',#(lf)[Category] as 'Clorox Sub Category Value',#(lf)[Size_Final] as 'Clorox Size Value',#(lf)[Pack_Size_Range] as 'Clorox Size Range Value',#(lf)[Pack_Size_Range_idx] as 'Index size range',#(lf)[Data_Source] as 'Data Source',#(lf)[Channel] as 'Channel',#(lf)[Refresh_Period2] as 'Refresh_Period2', #(lf)[BU] as 'BU', #(lf)[Size_Calc] as 'Size Calc',#(lf)dense_rank() over(order by CAST(substring (Refresh_Period2,3,2) as int)*100+CAST(substring (Refresh_Period2,6,2) as int) desc) AS rank_x#(lf)from nrm.POS_DIM_TEST#(lf))A#(lf)where  A.rank_x <=3 AND [BU] IN ('BRITA',#(lf)'CAT LITTER' ,#(lf)'FOOD',#(lf)'GRILLING',#(lf)'TRASH AND FOOD STORAGE')#(lf))B#(lf)WHERE B.DUPLICATE_CNT = 1", CreateNavigationProperties=false, CommandTimeout=#duration(0, 1, 0, 0)])
,
   #"Changed Type1" = Table.TransformColumnTypes(#"Source",{{"Product", type text}, {"Clorox Category Value", type text}, {"Clorox Sub Category Value", type text}, {"Clorox Segment Value", type text}, {"Clorox Manufacturer Value", type text}, {"Clorox Brand Value", type text}, {"Clorox SubBrand Value", type text}, {"Clorox Type Value", type text}, {"Clorox Sub Type Value", type text}, {"Clorox Pack Type Value", type text}, {"Clorox Size Value", type text}, {"Clorox Deal Pack Value", type text}, {"Clorox Size Range Value", type text}, {"Product Key", type text}}),
    #"Inserted Text Before Delimiter" = Table.AddColumn(#"Changed Type1", "Text Before Delimiter", each Text.BeforeDelimiter([Clorox Size Value], " "), type text),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Text Before Delimiter",{{"Text Before Delimiter", "SizeCalcOld"}}),
    #"Replaced Val" = Table.ReplaceValue(#"Renamed Columns","ALL",null,Replacer.ReplaceValue,{"SizeCalcOld"}),
   #"Added Conditional Column" = Table.AddColumn(#"Replaced Val", "New Clorox Brand Value", each if [Clorox Manufacturer Value] = "CLOROX COMPANY" then "CLOROX" else [Clorox Brand Value]),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Conditional Column",{{"Index size range", Int64.Type}, {"Size Calc", type number}}),
#"Added Custom" = Table.AddColumn(#"Changed Type3", "test_brand", each if[Clorox Sub Category Value]="DILUTABLES" and [Clorox Brand Value]="PINE SOL" then "CLOROX" else if 
[Clorox Sub Category Value]="THROUGH THE WASH STAIN REMOVE" and [Clorox Brand Value]="CLOROX 2" then "CLOROX"
else if 
[BU]="BRITA" and [Clorox Brand Value]="BRITA" then "CLOROX"
else if 
[BU]="TRASH AND FOOD STORAGE" and [Clorox Brand Value]="GLAD" then "CLOROX"
else if 
[BU]="GRILLING" and [Clorox Brand Value]="KINGSFORD" then "CLOROX"
else if 
[BU]="CAT LITTER" and [Clorox Brand Value]="FRESH STEP" then "CLOROX"
else if 
([Clorox Sub Category Value] ="AO Dressing" or [Clorox Sub Category Value] = "DRY SALAD DRESSING" or [Clorox Sub Category Value] = "DRY DIPS" or [Clorox Sub Category Value] = "AO DIPS" or [Clorox Sub Category Value] = "SS DIPS" )and [Clorox Brand Value]= "HIDDEN VALLEY" then "CLOROX"
else if 
[Clorox Sub Category Value]="AO Food" and [Clorox Brand Value]= "HIDDEN VALLEY" then "CLOROX"
else if 
[Clorox Sub Category Value]="SS BOTTLED/POURABLE" and [Clorox Brand Value]= "HIDDEN VALLEY" then "CLOROX"
else if 
[Clorox Sub Category Value]="BARBECUE SAUCE" and [Clorox Brand Value]= "K C MASTERPIECE" then "CLOROX"

else if 
([BU]="FACIAL CLEANSERS" or
[BU]="FACIAL MASKS" or
[BU]="FACIAL TONERS" or
[BU]="ACNE CARE" or
[BU]="FACIAL MOISTURIZERS AND TREATMENTS" or
[BU]="FACIAL TOWELETTES" or
[BU]="LIP CARE" or
[BU]="COLD SORE" or
[BU]="LIP COMBO" or
[BU]="LIP GLOSS" or
[BU]="LIP LINER" or
[BU]="LIPSTICK" or
[BU]="TINTED LIP BALM" or
[BU]="LIQUID LIPSTICK/STAIN" or
[BU]="COSMETIC LIP TREATMENT" or
[BU]="TINTED LIP OIL"
 )and [Clorox Brand Value]= "BURTS BEES" then "CLOROX"




else [Clorox Brand Value]),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"New Clorox Brand Value", "test brand"}, {"test_brand", "New Clorox Brand Value"}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Renamed Columns1", "Clorox Brand Value", "Clorox Brand Value - Copy"),
    #"Renamed Columns2" = Table.RenameColumns(#"Duplicated Column",{{"Clorox Brand Value - Copy", "Brand Universal"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns2",each [Clorox Brand Value],each if [BU]= "AO Food" and [Clorox Brand Value]=  "HIDDEN VALLEY" or [Clorox Brand Value]=  "K C MASTERPIECE" or [Clorox Brand Value]= "KC MASTERPIECE" or [Clorox Brand Value]= "SOY VAY"   then "HIDDEN VALLEY" else [Clorox Brand Value],Replacer.ReplaceText,{"Clorox Brand Value"}),
    #"Added Custom1" = Table.AddColumn(#"Replaced Value", "Division", each if  
([BU]="FACIAL CLEANSERS" or
[BU]="FACIAL MASKS" or
[BU]="FACIAL TONERS" or
[BU]="ACNE CARE" or
[BU]="FACIAL MOISTURIZERS AND TREATMENTS" or
[BU]="FACIAL TOWELETTES" or
[BU]="LIP CARE" or
[BU]="COLD SORE" or
[BU]="LIP COMBO" or
[BU]="LIP GLOSS" or
[BU]="LIP LINER" or
[BU]="LIPSTICK" or
[BU]="TINTED LIP BALM" or
[BU]="LIQUID LIPSTICK/STAIN" or
[BU]="COSMETIC LIP TREATMENT" or
[BU]="TINTED LIP OIL") then "BURTS BEES"
else if 
([BU]="LAUNDRY" or
[BU]="TOTAL HOME CLEANING")
then "CLEANING"
else "SPECIALTY")
in
    #"Added Custom1"
```


## Table: wipes_val Wide


```m
let

    Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[BU] as 'BU',#(lf)[Refresh_Period] as 'Refreshed Period',#(lf)[Periodicity] as 'Periodicity',#(lf)[Geography] as 'Retailer',#(lf)[Dollar_Sales] as '$',#(lf)[Baseline_Dollars] as 'Base $',#(lf)[Volume_Sales] as 'Volume IRI',#(lf)[Baseline_Volume] as 'Baseline Volume',#(lf)[Unit_Sales] as 'Units',#(lf)[Baseline_Units] as 'Base Units',#(lf)[Average_Weekly_ACV_Distribution] as '%ACV',#(lf)[Average_Weekly_Total_Points_of_Distribution] as 'TDP',#(lf)[Avg_Items_per_Store_Selling] as 'Avg # of Items',#(lf)[Dollars_per_$MM_ACV] as 'Dollars per $MM ACV',#(lf)[Units_per_Store_Selling] as 'Units / Store',#(lf)[Avg_Weekly_Units_per_Store_Selling] as 'Units / Store Weeks Selling',#(lf)[Dollars_Any_Merch] as 'Any Promo $',#(lf)[Dollars_PrcRed_Only] as 'Price Decr $',#(lf)[Dollars_Feature_Only] as 'Feat w/o Disp $',#(lf)[Dollars_Display_Only] as 'Disp w/o Feat $',#(lf)[Dollars_Feature_Display] as 'Dollars, Feature & Display',#(lf)[Units_Any_Merch] as 'Any Promo Units',#(lf)[Units_PrcRed_Only] as 'Price Decr Units',#(lf)[Units_Feature_Only] as 'Feat w/o Disp Units',#(lf)[Units_Display_Only] as 'Disp w/o Feat Units',#(lf)[Units_Feature_Display] as 'Units, Feature & Display',#(lf)[Product_Key] as 'Product Key',#(lf)[Time] as 'Time',#(lf)[Dol_per_unit] as '$/unit',#(lf)[Size2] as 'SKU Size',#(lf)[Vol2] as 'Volume Sales',#(lf)[Dol_per_vol] as '$ / oz_All SKUs',#(lf)[Promo_Vol] as 'Promo Volume',#(lf)[Promo_Dol_per_Vol] as 'Promo $ / oz',#(lf)[Promo_Dol_per_Unit] as 'Promo $ / unit',#(lf)[NPromo_Vol] as 'NP Volume',#(lf)[NPromo_Dol_per_Vol] as 'NP $ / oz',#(lf)[NPromo_Unit] as 'NP Units',#(lf)[NPromo_Dol_per_Unit] as 'NP $ / unit',#(lf)[Velocity_P] as 'Vel IRI',#(lf)[Price_per_pack_rng] as 'Price per pack rng',#(lf)[Price_per_pack_rng_idx] as 'Index P range',#(lf)[Price_per_vol_rng] as 'Price per vol rng',#(lf)[Price_per_vol_rng_idx] as 'Price per vol rng idx',#(lf)[Refresh_Period2] as 'Refresh Period 2'#(lf)from (select *,#(lf)dense_rank() over(#(lf)order by CAST(substring (Refresh_Period2,3,2) as int)*100+CAST(substring (Refresh_Period2,6,2) as int) desc) AS rank_x#(lf)from nrm.POS_VAL_TEST ) ranks#(lf)where rank_x<=3 AND [BU] IN ('BRITA',#(lf)'CAT LITTER' ,#(lf)'FOOD',#(lf)'GRILLING',#(lf)'TRASH AND FOOD STORAGE')#(lf)", CreateNavigationProperties=false, CommandTimeout=#duration(0, 1, 0, 0)]),
    #"Changed Type" = Table.TransformColumnTypes(#"Source",{{"Refreshed Period", type text}, {"Time", type text}, {"Retailer", type text}, {"$", type number}, {"Base $", type number}, {"Volume Sales", type number}, {"Baseline Volume", type number}, {"Units", type number}, {"Base Units", type number}, {"%ACV", type number}, {"TDP", type number}, {"Avg # of Items", type number}, {"Dollars per $MM ACV", type number}, {"Units / Store", type number}, {"Units / Store Weeks Selling", type number}, {"Any Promo $", type number}, {"Price Decr $", type number}, {"Feat w/o Disp $", type number}, {"Disp w/o Feat $", type number}, {"Dollars, Feature & Display", type number}, {"Any Promo Units", type number}, {"Price Decr Units", type number}, {"Feat w/o Disp Units", type number}, {"Disp w/o Feat Units", type number}, {"Units, Feature & Display", type number}, {"Product Key", type text}, {"SKU Size", type number}, {"$/unit", type number}, {"$ / oz_All SKUs", type number}, {"Promo Volume", type number}, {"Promo $ / oz", type number}, {"Promo $ / unit", type number}, {"NP Volume", type number}, {"NP Units", type number}, {"NP $ / unit", type number}, {"NP $ / oz", type number}}),
    #"Inserted date from Time column" = Table.AddColumn(#"Changed Type", "Date", each Text.End([Time], 8), type text),
    #"Changed Type with Locale" = Table.TransformColumnTypes(#"Inserted date from Time column", {{"Date", type date}}, "en-US"),
    #"Inserted Year" = Table.AddColumn(#"Changed Type with Locale", "Year", each Date.Year([Date]), Int64.Type),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Year",{{"Year", Int64.Type}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Changed Type1", "Merged", each Text.Combine({[Retailer], "_", [Time],"_",[Product Key],"_",[Refresh Period 2]})),
    #"Changed Type2" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"Index P range", Int64.Type}}),
    #"Changed Type3" = Table.TransformColumnTypes(#"Changed Type2",{{"Price per vol rng idx", Int64.Type}})
in
    #"Changed Type3"
```


## Table: continue_BItable


```m
let
    Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[Year] as 'Year',#(lf)[Time] as 'Time',#(lf)[Retailer] as 'Retailer',#(lf)[Product_Key] as 'Product Key',#(lf)[PY] as 'PY',#(lf)[PY-1] as 'PY-1'#(lf), #(lf)[Refresh_Period] as 'Refresh_Period2'#(lf) from (select *,#(lf)dense_rank() over(#(lf)order by CAST(substring (Refresh_Period,3,2) as int)*100+CAST(substring (Refresh_Period,6,2) as int) desc) AS rank_x#(lf)from nrm.POS_CONTINUE_FLG_TEST) ranks#(lf)where rank_x<=3#(lf)", CreateNavigationProperties=false, CommandTimeout=#duration(0, 1, 0, 0)]),
    #"Changed Type" = Table.TransformColumnTypes(#"Source",{{"Time", type text}, {"Retailer", type text}, {"Product Key", type text}, {"PY", type text}, {"PY-1", type text}, {"Year", Int64.Type}}),
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


## Table: date_table_1


```m
let
    Source = #"wipes_val Wide",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"Year"}),
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

    Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[Category] as 'Clorox Sub Category Value',#(lf)[Geography] as 'Retailer',#(lf)[Clorox_Brand_Value] as 'Clorox Brand Value',#(lf)[BU] as 'BU'#(lf)from nrm.POS_SWOT_TEST where [BU] IN ('BRITA',#(lf)'CAT LITTER' ,#(lf)'FOOD',#(lf)'GRILLING',#(lf)'TRASH AND FOOD STORAGE') #(lf)", CommandTimeout=#duration(0, 1, 0, 0)]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Source",{{"Clorox Sub Category Value", type text}, {"Retailer", type text}, {"Clorox Brand Value", type text}})
in
    #"Changed Type1"
```


## Table: Measure Table 3


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Measure Table 3" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Measure Table 3", type text}})
in
    #"Changed Type"
```


## Table: Retailer Rank


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("dZHLTsMwEAB/xcq5lZI+4egmgASKWjWtOJQeHLq4hm2M/JAQX49j5+BW5roza1vjwyHbScOQ7BsyJrVFI8jaGgSTjbIiO46u+KOUJzef+PkrwwtThpRSfY+3NXV8GDll6pWXbUyH7ZlHdNWU6wSdB1rtG0oqwDMTv5DQFl5bPb/ZPJ8sdWyUaFtnLL3xJFhnyAPjmDrlzjs1iE9QCXzv8QbMu4zpJsTJA7Utip/EchHqNezy/xuLUHLHFIerkDXTuufTofQXfIDqUrfMoj/qtwjlXAFnBno6v/3BSlneg0WUmZ4lnlJnh4QUW1BGy06XMmW5iMc/", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Retailer = _t, Rank = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Retailer", type text}, {"Rank", Int64.Type}})
in
    #"Changed Type"
```


## Table: Legend Table


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45Wco5UKCtWiHRU0lEyVIrVgQkYwURiAQ==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Legend = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Legend", type text}, {"Column1", Int64.Type}})
in
    #"Changed Type"
```

