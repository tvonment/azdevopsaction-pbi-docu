



# M Code

|Dataset|[Amazon iNorm Dashboard](./../Amazon-iNorm-Dashboard.md)|
| :--- | :--- |
|Workspace|[Clorox Data](../../Workspaces/Clorox-Data.md)|

## Table: wipes_dim Wide


```m
let
   Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select * from (select  #(lf)[Product] as 'Product',#(lf)[Business_Unit] as 'Business_Unit',#(lf)[Clorox_Category_Value] as 'BU',#(lf)[Clorox_Sub_Category_Value] as 'Clorox Sub Category Value',#(lf)[Clorox_Brand_Value] as 'Clorox Brand Value',#(lf)[Product_Key] as 'Product Key',#(lf)[Size_Final] as 'Clorox Size Value',#(lf)[Pack_Size_Range] as 'Clorox Size Range Value',#(lf)[Pack_Size_Range_idx] as 'Index size range',#(lf)[Refresh_Period2] as 'Refresh_Period2',  #(lf)[Size_Calc]#(lf) as 'Size Calc',#(lf)row_number() over (partition by [Product_Key] order by [Product_Key]) as rn#(lf)from nrm.POS_DIM_TEST_AMAZON) A#(lf)where A.rn = 1"]),
    #"Changed Type" = Table.TransformColumnTypes(#"Source",{{"BU", type text}, {"Product", type text}, {"Clorox Sub Category Value", type text}, {"Clorox Brand Value", type text}, {"Product Key", type text}, {"Clorox Size Value", type text}, {"Clorox Size Range Value", type text}, {"Index size range", Int64.Type}, {"Refresh_Period2", type text}, {"Size Calc", type number}}),
    #"Inserted Text Before Delimiter" = Table.AddColumn(#"Changed Type", "Text Before Delimiter", each Text.BeforeDelimiter([Clorox Size Value], " "), type text),
    #"Renamed Columns1" = Table.RenameColumns(#"Inserted Text Before Delimiter",{{"Text Before Delimiter", "SizeCalcOld"}}),
    #"Replaced Val" = Table.ReplaceValue(#"Renamed Columns1","ALL",null,Replacer.ReplaceValue,{"SizeCalcOld"}),
   #"Changed Type3" = Table.TransformColumnTypes(#"Replaced Val",{{"Index size range", Int64.Type}, {"Size Calc", type number}}),
#"Added Custom" = Table.AddColumn(#"Changed Type3", "test_brand", each if(  ( [BU]="Lip Care"  or [BU]="Lip Color" or [BU]="Facial Skin Care" or [BU]= "Cat Litter & Housebreaking" or [BU]="Beauty Brushes, Accessories & Tools" or [BU]="Eye Care & Treatments") and ( [Clorox Brand Value]= "Burt's Bees" or [Clorox Brand Value]="Fresh Step" )) then "Clorox"
 else if ([BU] = "Condiments & Salad Dressings" or [BU]="Hydration & Filtration" or [BU]= "Water Filtration & Softeners" or [BU]= "Minerals" or [BU]= "Sauces & Gravies"or [BU]="Supplements") and ([Clorox Brand Value] =
         "Hidden Valley" or [Clorox Brand Value] = "Brita" or  [Clorox Brand Value] = "Natural Vitality" or [Clorox Brand Value] = "Soy Vay" or  [Clorox Brand Value] = "Renew Life") then "Clorox"
else if ([BU] = "Food Storage"or [BU]=  "Grilling & Outdoor Fuels" ) and ([Clorox Brand Value] = "Glad" or [Clorox Brand Value] = "Kingsford") then "Clorox"
else if ([Clorox Sub Category Value] ="All-Purpose Cleaners" or [Clorox Sub Category Value] ="Bathroom Cleaners" or [Clorox Sub Category Value] = "Household Disinfectant Wipes" or [Clorox Sub Category Value] = "Household Drain Openers" or [Clorox Sub Category Value] = "Household Kitchen Cleaners" or [Clorox Sub Category Value]="Liquid Toilet Cleaners" or [Clorox Sub Category Value] ="Toilet Cleaning Systems" or [Clorox Sub Category Value] = "Toilet Cleaning Tablets" or [Clorox Sub Category Value] ="Cleaning Cloths" or [Clorox Sub Category Value] = "Household Scouring Pads & Sticks") and ([Clorox Brand Value] = "Pine-Sol" or [Clorox Brand Value] ="Clorox")then "Clorox"
else if ([Clorox Sub Category Value]="Household Floor Cleaners" or [Clorox Sub Category Value]= "Household Glass Cleaners" or [Clorox Sub Category Value]="Other Disinfecting Wipes" or [Clorox Sub Category Value]=
"Cleaning Brushes" or [Clorox Sub Category Value]="Household Sponges") and( [Clorox Brand Value] = "Pine-Sol") then "Clorox"
else if ([Clorox Sub Category Value]= "Compost Bags" or [Clorox Sub Category Value]= "Trash Bags" or [Clorox Sub Category Value]= "Trash Compactors & Compactor Bags") and ([Clorox Brand Value] = "Glad") then "Clorox"
else if [Clorox Brand Value] = "CLOROX" then "Clorox"       
else [Clorox Brand Value]),
    #"Renamed Columns2" = Table.RenameColumns(#"Added Custom",{ {"test_brand", "New Clorox Brand Value"}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Renamed Columns2", "Clorox Brand Value", "Clorox Brand Value - Copy"),
    #"Renamed Columns3" = Table.RenameColumns(#"Duplicated Column",{{"Clorox Brand Value - Copy", "Brand Universal"}}),
    #"Added Custom1" = Table.AddColumn(#"Renamed Columns3", "Division", each [Business_Unit])
in
    #"Added Custom1"
```


## Table: wipes_val Wide


```m
let

   Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[Business_Unit] as 'Business_Unit',#(lf)[Clorox_Category_Value] as 'BU',#(lf)[Refresh_Period] as 'Refreshed Period',#(lf)[Periodicity] as 'Periodicity',#(lf)[Geography] as 'Retailer',#(lf)[Dollar_Sales] as '$',#(lf)[Volume_Sales] as 'Volume Sales',#(lf)[Unit_Sales] as 'Units',#(lf)[Average_Weekly_Total_Points_of_Distribution] as 'TDP',#(lf)[Product_Key] as 'Product Key',#(lf)[Time] as 'Time',#(lf)[Dol_per_vol] as '$ / oz_All SKUs',#(lf)[Dol_per_unit] as 'Dol per unit',#(lf)[Price_per_vol_rng] as 'Price per vol rng',#(lf)[Price_per_vol_rng_idx] as 'Price per vol rng idx',#(lf)[Price_per_pack_rng] as 'Price_per_pack_rng',#(lf)[Price_per_pack_rng_idx] as 'Price per pack rng idx',#(lf)[Refresh_Period2] as 'Refresh Period 2'#(lf)from (select *,#(lf)dense_rank() over(#(lf)order by CAST(substring (Refresh_Period2,3,2) as int)*100+CAST(substring (Refresh_Period2,6,2) as int) desc) AS rank_x#(lf)from [nrm].[POS_VAL_TEST_AMAZON] ) ranks#(lf)where rank_x<=3 ", CreateNavigationProperties=false, CommandTimeout=#duration(0, 1, 0, 0)]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Refreshed Period", type text}, {"Time", type text}, {"Retailer", type text}, {"$", type number}, {"Volume Sales", type number}, {"Units", type number}, {"TDP", type number}, {"Product Key", type text}, {"$ / oz_All SKUs", type number}, {"Price per vol rng idx", Int64.Type}}),
    #"Inserted date from Time column" = Table.AddColumn(#"Changed Type", "Date", each Text.End([Time], 8), type text),
    #"Changed Type with Locale" = Table.TransformColumnTypes(#"Inserted date from Time column", {{"Date", type date}}, "en-US"),
    #"Inserted Year" = Table.AddColumn(#"Changed Type with Locale", "Year", each Date.Year([Date]), Int64.Type),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Year",{{"Year", Int64.Type}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Changed Type1", "Merged", each Text.Combine({[Retailer], "_", [Time],"_",[Product Key],"_",[Refresh Period 2]}))
in
    #"Inserted Merged Column"
```


## Table: continue_BItable


```m
let
      Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[Year] as 'Year',#(lf)[Business_Unit] as 'Business Unit',#(lf)[Clorox_Category_Value] as 'Clorox Category Value',#(lf)[Clorox_Sub_Category_Value] as 'Clorox Sub Category Value',#(lf)[Time] as 'Time',#(lf)[Retailer] as 'Retailer',#(lf)[Product_Key] as 'Product Key',#(lf)[PY] as 'PY',#(lf)[PY-1] as 'PY-1', #(lf)[Refresh_Period] as 'Refresh_Period2'#(lf) from (select *,#(lf)dense_rank() over(#(lf)order by CAST(substring (Refresh_Period,3,2) as int)*100+CAST(substring (Refresh_Period,6,2) as int) desc) AS rank_x#(lf)from [nrm].[POS_CONTINUE_FLG_TEST_AMAZON]) ranks#(lf)where rank_x<=3"]),
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


## Table: date_table_1


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
 Source = Sql.Database("sql-ssemkt-selfserv01.database.windows.net", "SQLDB-SSEMKT-SELFSERV01", [Query="select  #(lf)[Clorox_Category_Value] as 'BU',#(lf)[Clorox_Sub_Category_Value] as 'Clorox Sub Category Value',#(lf)[Geography] as 'Retailer',#(lf)[Clorox_Brand_Value] as 'Clorox Brand Value',#(lf)[Business_Unit] as 'Business_Unit'#(lf)from [nrm].[POS_SWOT_TEST_AMAZON]"]),
    #"Removed Blank Rows" = Table.SelectRows(Source, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Blank Rows",{{"BU", type text}, {"Clorox Sub Category Value", type text}, {"Retailer", type text}, {"Clorox Brand Value", type text}})
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

