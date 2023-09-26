



# M Code

|Dataset|[DM_Dashboard_v5](./../DM_Dashboard_v5.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Segment_Age


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_age_det_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"CUST_SEG", Int64.Type}, {"INTERVAL", Int64.Type}, {"CUST_SEG_NAME", type text}, {"AVG_AGE_CUT", type text}, {"AVG_AGE_ABS", Int64.Type}, {"AVG_AGE_PCT", type number}, {"AVG_AGE_IDX", type number}}),
    #"Filled Down" = Table.FillDown(#"Changed Type",{"CUST_SEG"})
in
    #"Filled Down"
```


## Table: Segment_Warenwelt


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_kpi_assoc_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"CUST_SEG_NAME", type text}, {"Körperreinigung_REV_ABS", type number}, {"Körperreinigung_REV_PCT", type number}, {"Körperreinigung_REV_IDX", type number}, {"Körperpflege_REV_ABS", type number}, {"Körperpflege_REV_PCT", type number}, {"Körperpflege_REV_IDX", type number}, {"Haar_REV_ABS", type number}, {"Haar_REV_PCT", type number}, {"Haar_REV_IDX", type number}, {"Dekorative Kosmetik_REV_ABS", type number}, {"Dekorative Kosmetik_REV_PCT", type number}, {"Dekorative Kosmetik_REV_IDX", type number}, {"Duft_REV_ABS", type number}, {"Duft_REV_PCT", type number}, {"Duft_REV_IDX", type number}, {"Baby_REV_ABS", type number}, {"Baby_REV_PCT", type number}, {"Baby_REV_IDX", type number}, {"Kindertextil_REV_ABS", type number}, {"Kindertextil_REV_PCT", type number}, {"Kindertextil_REV_IDX", type number}, {"Pharma_REV_ABS", type number}, {"Pharma_REV_PCT", type number}, {"Pharma_REV_IDX", type number}, {"Ernährung_REV_ABS", type number}, {"Ernährung_REV_PCT", type number}, {"Ernährung_REV_IDX", type number}, {"Haushalt_REV_ABS", type number}, {"Haushalt_REV_PCT", type number}, {"Haushalt_REV_IDX", type number}, {"Saisonartikel_REV_ABS", type number}, {"Saisonartikel_REV_PCT", type number}, {"Saisonartikel_REV_IDX", type number}, {"Accessoires_REV_ABS", type number}, {"Accessoires_REV_PCT", type number}, {"Accessoires_REV_IDX", type number}, {"Foto_REV_ABS", type number}, {"Foto_REV_PCT", type number}, {"Foto_REV_IDX", type number}, {"Tier_REV_ABS", type number}, {"Tier_REV_PCT", type number}, {"Tier_REV_IDX", type number}}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"Column1", "CUST_SEG_NAME"}, "Attribute", "Value"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Unpivoted Columns", "Attribute", Splitter.SplitTextByEachDelimiter({"_"}, QuoteStyle.Csv, true), {"Attribute.1", "Attribute.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Attribute.1", type text}, {"Attribute.2", type text}}),
    #"Pivoted Column" = Table.Pivot(#"Changed Type1", List.Distinct(#"Changed Type1"[Attribute.2]), "Attribute.2", "Value", List.Sum),
    #"Renamed Columns" = Table.RenameColumns(#"Pivoted Column",{{"Attribute.1", "Warenwelt"}}),
    #"Split Column by Delimiter1" = Table.SplitColumn(#"Renamed Columns", "Warenwelt", Splitter.SplitTextByDelimiter("_", QuoteStyle.Csv), {"Warenwelt.1", "Warenwelt.2"}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Split Column by Delimiter1",{{"Warenwelt.1", type text}, {"Warenwelt.2", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type2",{"Warenwelt.2"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns",{{"Warenwelt.1", "Warenwelt"}})
in
    #"Renamed Columns1"
```


## Table: Segment_Tag


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_kpi_day_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"CUST_SEG_NAME", type text}, {"MO_ABS", Int64.Type}, {"MO_PCT", type number}, {"MO_IDX", type number}, {"DI_ABS", Int64.Type}, {"DI_PCT", type number}, {"DI_IDX", type number}, {"MI_ABS", Int64.Type}, {"MI_PCT", type number}, {"MI_IDX", type number}, {"DO_ABS", Int64.Type}, {"DO_PCT", type number}, {"DO_IDX", type number}, {"FR_ABS", Int64.Type}, {"FR_PCT", type number}, {"FR_IDX", type number}, {"SA_ABS", Int64.Type}, {"SA_PCT", type number}, {"SA_IDX", type number}, {"SO_ABS", Int64.Type}, {"SO_PCT", type number}, {"SO_IDX", type number}}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"Column1", "CUST_SEG_NAME"}, "Attribute", "Value"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Unpivoted Columns", "Attribute", Splitter.SplitTextByDelimiter("_", QuoteStyle.Csv), {"Attribute.1", "Attribute.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Attribute.1", type text}, {"Attribute.2", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"Attribute.1", "Day"}}),
    #"Pivoted Column" = Table.Pivot(#"Renamed Columns", List.Distinct(#"Renamed Columns"[Attribute.2]), "Attribute.2", "Value", List.Sum)
in
    #"Pivoted Column"
```


## Table: Segment_Detail/Rabatt


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_kpi_det_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"CUST_SEG", Int64.Type}, {"INTERVAL", Int64.Type}, {"CUST_SEG_NAME", type text}, {"Artikelrabatt_REV_SHR_CUT", type text}, {"Artikelrabatt_REV_SHR_ABS", Int64.Type}, {"Artikelrabatt_REV_SHR_PCT", type number}, {"Artikelrabatt_REV_SHR_IDX", type number}, {"Bonrabatt_REV_SHR_CUT", type text}, {"Bonrabatt_REV_SHR_ABS", Int64.Type}, {"Bonrabatt_REV_SHR_PCT", type number}, {"Bonrabatt_REV_SHR_IDX", type number}, {"Wert_Artikelpunkte_REV_SHR_CUT", type text}, {"Wert_Artikelpunkte_REV_SHR_ABS", Int64.Type}, {"Wert_Artikelpunkte_REV_SHR_PCT", type number}, {"Wert_Artikelpunkte_REV_SHR_IDX", type number}, {"Wert_Bonsonderpunkte_REV_SHR_CUT", type text}, {"Wert_Bonsonderpunkte_REV_SHR_ABS", Int64.Type}, {"Wert_Bonsonderpunkte_REV_SHR_PCT", type number}, {"Wert_Bonsonderpunkte_REV_SHR_IDX", type number}, {"ONLINE_REV_SHR_CUT", type text}, {"ONLINE_REV_SHR_ABS", Int64.Type}, {"ONLINE_REV_SHR_PCT", type number}, {"ONLINE_REV_SHR_IDX", type number}, {"PROMO_REV_SHR_CUT", type text}, {"PROMO_REV_SHR_ABS", Int64.Type}, {"PROMO_REV_SHR_PCT", type number}, {"PROMO_REV_SHR_IDX", type number}, {"NURONLINEKZ_REV_SHR_CUT", type text}, {"NURONLINEKZ_REV_SHR_ABS", Int64.Type}, {"NURONLINEKZ_REV_SHR_PCT", type number}, {"NURONLINEKZ_REV_SHR_IDX", type number}, {"DM_MARKE_KZ_REV_SHR_CUT", type text}, {"DM_MARKE_KZ_REV_SHR_ABS", Int64.Type}, {"DM_MARKE_KZ_REV_SHR_PCT", type number}, {"DM_MARKE_KZ_REV_SHR_IDX", type number}, {"MARKE_REV_SHR_CUT", type text}, {"MARKE_REV_SHR_ABS", Int64.Type}, {"MARKE_REV_SHR_PCT", type number}, {"MARKE_REV_SHR_IDX", type number}, {"DM_BALEA_REV_SHR_CUT", type text}, {"DM_BALEA_REV_SHR_ABS", Int64.Type}, {"DM_BALEA_REV_SHR_PCT", type number}, {"DM_BALEA_REV_SHR_IDX", type number}, {"BIOARTIKELKZ_REV_SHR_CUT", type text}, {"BIOARTIKELKZ_REV_SHR_ABS", Int64.Type}, {"BIOARTIKELKZ_REV_SHR_PCT", type number}, {"BIOARTIKELKZ_REV_SHR_IDX", type number}, {"VEGANKZ_REV_SHR_CUT", type text}, {"VEGANKZ_REV_SHR_ABS", Int64.Type}, {"VEGANKZ_REV_SHR_PCT", type number}, {"VEGANKZ_REV_SHR_IDX", type number}, {"GLUTENFREIKZ_REV_SHR_CUT", type text}, {"GLUTENFREIKZ_REV_SHR_ABS", Int64.Type}, {"GLUTENFREIKZ_REV_SHR_PCT", type number}, {"GLUTENFREIKZ_REV_SHR_IDX", type number}, {"LEBENSMITTELKZ_REV_SHR_CUT", type text}, {"LEBENSMITTELKZ_REV_SHR_ABS", Int64.Type}, {"LEBENSMITTELKZ_REV_SHR_PCT", type number}, {"LEBENSMITTELKZ_REV_SHR_IDX", type number}, {"Artikelrabatt_BON_SHR_CUT", type text}, {"Artikelrabatt_BON_SHR_ABS", Int64.Type}, {"Artikelrabatt_BON_SHR_PCT", type number}, {"Artikelrabatt_BON_SHR_IDX", type number}, {"Bonrabatt_BON_SHR_CUT", type text}, {"Bonrabatt_BON_SHR_ABS", Int64.Type}, {"Bonrabatt_BON_SHR_PCT", type number}, {"Bonrabatt_BON_SHR_IDX", type number}, {"Wert_Artikelpunkte_BON_SHR_CUT", type text}, {"Wert_Artikelpunkte_BON_SHR_ABS", Int64.Type}, {"Wert_Artikelpunkte_BON_SHR_PCT", type number}, {"Wert_Artikelpunkte_BON_SHR_IDX", type number}, {"Wert_Bonsonderpunkte_BON_SHR_CUT", type text}, {"Wert_Bonsonderpunkte_BON_SHR_ABS", Int64.Type}, {"Wert_Bonsonderpunkte_BON_SHR_PCT", type number}, {"Wert_Bonsonderpunkte_BON_SHR_IDX", type number}, {"ONLINE_BON_SHR_CUT", type text}, {"ONLINE_BON_SHR_ABS", Int64.Type}, {"ONLINE_BON_SHR_PCT", type number}, {"ONLINE_BON_SHR_IDX", type number}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Artikelrabatt_REV_SHR_CUT", "Artikelrabatt_REV_SHR_ABS", "Artikelrabatt_REV_SHR_PCT", "Artikelrabatt_REV_SHR_IDX", "Bonrabatt_REV_SHR_CUT", "Bonrabatt_REV_SHR_ABS", "Bonrabatt_REV_SHR_PCT", "Bonrabatt_REV_SHR_IDX", "Wert_Artikelpunkte_REV_SHR_CUT", "Wert_Artikelpunkte_REV_SHR_ABS", "Wert_Artikelpunkte_REV_SHR_PCT", "Wert_Artikelpunkte_REV_SHR_IDX", "Wert_Bonsonderpunkte_REV_SHR_CUT", "Wert_Bonsonderpunkte_REV_SHR_ABS", "Wert_Bonsonderpunkte_REV_SHR_PCT", "Wert_Bonsonderpunkte_REV_SHR_IDX", "ONLINE_REV_SHR_CUT", "ONLINE_REV_SHR_ABS", "ONLINE_REV_SHR_PCT", "ONLINE_REV_SHR_IDX", "PROMO_REV_SHR_CUT", "PROMO_REV_SHR_ABS", "PROMO_REV_SHR_PCT", "PROMO_REV_SHR_IDX", "NURONLINEKZ_REV_SHR_CUT", "NURONLINEKZ_REV_SHR_ABS", "NURONLINEKZ_REV_SHR_PCT", "NURONLINEKZ_REV_SHR_IDX", "MARKE_REV_SHR_CUT", "MARKE_REV_SHR_ABS", "MARKE_REV_SHR_PCT", "MARKE_REV_SHR_IDX", "DM_BALEA_REV_SHR_CUT", "DM_BALEA_REV_SHR_ABS", "DM_BALEA_REV_SHR_PCT", "DM_BALEA_REV_SHR_IDX", "VEGANKZ_REV_SHR_CUT", "VEGANKZ_REV_SHR_ABS", "VEGANKZ_REV_SHR_PCT", "VEGANKZ_REV_SHR_IDX", "GLUTENFREIKZ_REV_SHR_CUT", "GLUTENFREIKZ_REV_SHR_ABS", "GLUTENFREIKZ_REV_SHR_PCT", "GLUTENFREIKZ_REV_SHR_IDX", "Artikelrabatt_BON_SHR_CUT", "Artikelrabatt_BON_SHR_ABS", "Artikelrabatt_BON_SHR_PCT", "Artikelrabatt_BON_SHR_IDX", "Bonrabatt_BON_SHR_CUT", "Bonrabatt_BON_SHR_ABS", "Bonrabatt_BON_SHR_PCT", "Bonrabatt_BON_SHR_IDX", "Wert_Artikelpunkte_BON_SHR_CUT", "Wert_Artikelpunkte_BON_SHR_ABS", "Wert_Artikelpunkte_BON_SHR_PCT", "Wert_Artikelpunkte_BON_SHR_IDX", "Wert_Bonsonderpunkte_BON_SHR_CUT", "Wert_Bonsonderpunkte_BON_SHR_ABS", "Wert_Bonsonderpunkte_BON_SHR_PCT", "Wert_Bonsonderpunkte_BON_SHR_IDX", "ONLINE_BON_SHR_CUT", "ONLINE_BON_SHR_ABS", "ONLINE_BON_SHR_PCT", "ONLINE_BON_SHR_IDX"}),
    #"Filled Down" = Table.FillDown(#"Removed Columns",{"CUST_SEG"})
in
    #"Filled Down"
```


## Table: Segment_Filialtyp


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_kpi_fil_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"CUST_SEG_NAME", type text}, {"FIL_LOC_ONLINE_PCT", type number}, {"FIL_LOC_ONLINE_IDX", type number}, {"FIL_LOC_INNENSTADT_PCT", type number}, {"FIL_LOC_INNENSTADT_IDX", type number}, {"FIL_LOC_STADTTEIL_PCT", type number}, {"FIL_LOC_STADTTEIL_IDX", type number}, {"FIL_LOC_STADTRAND_PCT", type number}, {"FIL_LOC_STADTRAND_IDX", type number}, {"FIL_POP_1_max10k_PCT", type number}, {"FIL_POP_1_max10k_IDX", type number}, {"FIL_POP_2_10k_20k_PCT", type number}, {"FIL_POP_2_10k_20k_IDX", type number}, {"FIL_POP_3_20k_100k_PCT", type number}, {"FIL_POP_3_20k_100k_IDX", type number}, {"FIL_POP_4_min100k_PCT", type number}, {"FIL_POP_4_min100k_IDX", type number}, {"FIL_TYP_FGZ_PCT", type number}, {"FIL_TYP_FGZ_IDX", type number}, {"FIL_TYP_GES_PCT", type number}, {"FIL_TYP_GES_IDX", type number}, {"FIL_TYP_FMV_PCT", type number}, {"FIL_TYP_FMV_IDX", type number}, {"FIL_TYP_FMZ_PCT", type number}, {"FIL_TYP_FMZ_IDX", type number}, {"FIL_TYP_EKZ_PCT", type number}, {"FIL_TYP_EKZ_IDX", type number}, {"FIL_TYP_NVZ_PCT", type number}, {"FIL_TYP_NVZ_IDX", type number}, {"FIL_TYP_FMA_PCT", type number}, {"FIL_TYP_FMA_IDX", type number}, {"FIL_TYP_BHF_PCT", type number}, {"FIL_TYP_BHF_IDX", type number}, {"FIL_TYP_SOL_PCT", type number}, {"FIL_TYP_SOL_IDX", type number}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"FIL_LOC_ONLINE_PCT", "FIL_LOC_ONLINE_IDX", "FIL_LOC_INNENSTADT_PCT", "FIL_LOC_INNENSTADT_IDX", "FIL_LOC_STADTTEIL_PCT", "FIL_LOC_STADTTEIL_IDX", "FIL_LOC_STADTRAND_PCT", "FIL_LOC_STADTRAND_IDX", "FIL_POP_1_max10k_PCT", "FIL_POP_1_max10k_IDX", "FIL_POP_2_10k_20k_PCT", "FIL_POP_2_10k_20k_IDX", "FIL_POP_3_20k_100k_PCT", "FIL_POP_3_20k_100k_IDX", "FIL_POP_4_min100k_PCT", "FIL_POP_4_min100k_IDX"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"Column1", "CUST_SEG_NAME"}, "Attribute", "Value"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Unpivoted Columns", "Attribute", Splitter.SplitTextByEachDelimiter({"_"}, QuoteStyle.Csv, true), {"Attribute.1", "Attribute.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Attribute.1", type text}, {"Attribute.2", type text}}),
    #"Pivoted Column" = Table.Pivot(#"Changed Type1", List.Distinct(#"Changed Type1"[Attribute.2]), "Attribute.2", "Value", List.Sum),
    #"Renamed Columns" = Table.RenameColumns(#"Pivoted Column",{{"Attribute.1", "FIL_TYP"}}),
    #"Split Column by Delimiter1" = Table.SplitColumn(#"Renamed Columns", "FIL_TYP", Splitter.SplitTextByEachDelimiter({"_"}, QuoteStyle.Csv, true), {"FIL_TYP.1", "FIL_TYP.2"}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Split Column by Delimiter1",{{"FIL_TYP.1", type text}, {"FIL_TYP.2", type text}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Changed Type2",{"FIL_TYP.1"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns1",{{"FIL_TYP.2", "FIL_TYP"}})
in
    #"Renamed Columns1"
```


## Table: Segment_KPIs


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_kpi_main_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"CUST_SEG_NAME", type text}, {"SIZE_ABS", type number}, {"SIZE_PCT", type number}, {"SIZE_IDX", type number}, {"AVG_AGE_ABS", type number}, {"AVG_AGE_IDX", type number}, {"AVG_FEMALE_PCT", type number}, {"AVG_FEMALE_IDX", type number}, {"AVG_MALE_PCT", type number}, {"AVG_MALE_IDX", type number}, {"REV_SHR_PCT", type number}, {"REV_SHR_IDX", type number}, {"AVG_BON_EUR_ABS", type number}, {"AVG_BON_EUR_IDX", type number}, {"FREQ_ABS", type number}, {"FREQ_IDX", type number}, {"Artikelrabatt_REV_SHR_PCT", type number}, {"Artikelrabatt_REV_SHR_IDX", type number}, {"Bonrabatt_REV_SHR_PCT", type number}, {"Bonrabatt_REV_SHR_IDX", type number}, {"Wert_Artikelpunkte_REV_SHR_PCT", type number}, {"Wert_Artikelpunkte_REV_SHR_IDX", type number}, {"Wert_Bonsonderpunkte_REV_SHR_PCT", type number}, {"Wert_Bonsonderpunkte_REV_SHR_IDX", type number}, {"ONLINE_REV_SHR_PCT", type number}, {"ONLINE_REV_SHR_IDX", type number}, {"PROMO_REV_SHR_PCT", type number}, {"PROMO_REV_SHR_IDX", type number}, {"NURONLINEKZ_REV_SHR_PCT", type number}, {"NURONLINEKZ_REV_SHR_IDX", type number}, {"DM_MARKE_KZ_REV_SHR_PCT", type number}, {"DM_MARKE_KZ_REV_SHR_IDX", type number}, {"MARKE_REV_SHR_PCT", type number}, {"MARKE_REV_SHR_IDX", type number}, {"DM_BALEA_REV_SHR_PCT", type number}, {"DM_BALEA_REV_SHR_IDX", type number}, {"BIOARTIKELKZ_REV_SHR_PCT", type number}, {"BIOARTIKELKZ_REV_SHR_IDX", type number}, {"VEGANKZ_REV_SHR_PCT", type number}, {"VEGANKZ_REV_SHR_IDX", type number}, {"GLUTENFREIKZ_REV_SHR_PCT", type number}, {"GLUTENFREIKZ_REV_SHR_IDX", type number}, {"LEBENSMITTELKZ_REV_SHR_PCT", type number}, {"LEBENSMITTELKZ_REV_SHR_IDX", type number}, {"Artikelrabatt_BON_SHR_PCT", type number}, {"Artikelrabatt_BON_SHR_IDX", type number}, {"Bonrabatt_BON_SHR_PCT", type number}, {"Bonrabatt_BON_SHR_IDX", type number}, {"Wert_Artikelpunkte_BON_SHR_PCT", type number}, {"Wert_Artikelpunkte_BON_SHR_IDX", type number}, {"Wert_Bonsonderpunkte_BON_SHR_PCT", type number}, {"Wert_Bonsonderpunkte_BON_SHR_IDX", type number}, {"ONLINE_BON_SHR_PCT", type number}, {"ONLINE_BON_SHR_IDX", type number}})
in
    #"Changed Type"
```


## Table: Segment_RFM


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_kpi_rfm_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"CUST_SEG_NAME", type text}, {"Topkunden_ABS", Int64.Type}, {"Topkunden_PCT", type number}, {"Topkunden_IDX", type number}, {"Stammkunden_ABS", Int64.Type}, {"Stammkunden_PCT", type number}, {"Stammkunden_IDX", type number}, {"Vorratskäufer_ABS", Int64.Type}, {"Vorratskäufer_PCT", type number}, {"Vorratskäufer_IDX", type number}, {"Geringer Bedarf_ABS", Int64.Type}, {"Geringer Bedarf_PCT", type number}, {"Geringer Bedarf_IDX", type number}, {"Ergänzungskäufer_ABS", Int64.Type}, {"Ergänzungskäufer_PCT", type number}, {"Ergänzungskäufer_IDX", type number}, {"Gelegenheitskunde_ABS", Int64.Type}, {"Gelegenheitskunde_PCT", type number}, {"Gelegenheitskunde_IDX", type number}, {"Zufallskunde_ABS", Int64.Type}, {"Zufallskunde_PCT", type number}, {"Zufallskunde_IDX", type number}}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"Column1", "CUST_SEG_NAME"}, "Attribute", "Value"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Unpivoted Columns", "Attribute", Splitter.SplitTextByDelimiter("_", QuoteStyle.Csv), {"Attribute.1", "Attribute.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Attribute.1", type text}, {"Attribute.2", type text}}),
    #"Pivoted Column" = Table.Pivot(#"Changed Type1", List.Distinct(#"Changed Type1"[Attribute.2]), "Attribute.2", "Value", List.Sum),
    #"Renamed Columns" = Table.RenameColumns(#"Pivoted Column",{{"Attribute.1", "RFM Sektor"}})
in
    #"Renamed Columns"
```


## Table: Segment_Produktfaktor


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_pf_revenue_db_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"PCT", type number}, {"IDX", type number}}),
    #"Filled Down" = Table.FillDown(#"Changed Type",{"Column1"}),
    #"Renamed Columns" = Table.RenameColumns(#"Filled Down",{{"Column2", "Produktfaktor"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","Schönheitskundinnen","Schönheitskundinnen mit Eigenmarkenfokus",Replacer.ReplaceText,{"Column1"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Grundversorger mit Fokus Bio","Grundversorger LOHAS",Replacer.ReplaceText,{"Column1"})
in
    #"Replaced Value1"
```


## Table: Top Produkte


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\DE_DESCR_df_top_pg_db_C11_S95_v002.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"IDX", type number}, {"PCT", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"level_0", "cust_segement"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"Column1"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns","Schönheitskundinnen","Schönheitskundinnen mit Eigenmarkenfokus",Replacer.ReplaceText,{"cust_segement"}),
    #"Filtered Rows" = Table.SelectRows(#"Replaced Value", each true),
    #"Replaced Value1" = Table.ReplaceValue(#"Filtered Rows","Grundversorger mit Fokus Bio","Grundversorger LOHAS",Replacer.ReplaceText,{"cust_segement"})
in
    #"Replaced Value1"
```


## Table: Segmente


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("hZK/bsIwEMZf5eSZAfq/I6gFRKg60C3K4MAlseLYyHYq8WJM3fJivTOFqg2Izf7u933ns52mYiQGIun2botuW2gsEVqzgZfuqwj4vySyQSpuSF20hsCESGWgUQES6xsMqi5s3frrAOfcErZaV93eVKiCryNr8IC/qhJNI12N5hg5kRrlwXpH25kjwyc6b12JDpbv8/HqksyeeyoeoV/1oW/h9lPuCXPZ+krqQMxpyaZHEqayUVphpCcy352TmH06U4C3OJjGHI0nMaCO8+W7wtoNLC0fJrqf+8f7CbtcYN9oyIHoA4z/jjRDTya+8OtADOLv8aHQnZ6nt8+ybw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Segemente_nr = _t, Segemente = _t, #"Segmente Namen neu" = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Segemente_nr", Int64.Type}, {"Segemente", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Segemente", "Segmente"}, {"Segemente_nr", "Segmente_nr"}})
in
    #"Renamed Columns"
```


## Table: Intervall_Bio


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\Intervalle.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Intervall", type text}, {"Name", type text}, {"Sort_num", Int64.Type}})
in
    #"Changed Type"
```


## Table: Intervall_DM_Marke


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\Intervalle_equal.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Intervall", type text}, {"Name", type text}, {"Sort_num", Int64.Type}})
in
    #"Changed Type"
```


## Table: Intervall_Lebensmittel


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\Intervall_Lebensmittel.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Intervall", type text}, {"Name", type text}, {"Sort_num", Int64.Type}})
in
    #"Changed Type"
```


## Table: Tage_sort


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\Tage_sort.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Tag", type text}, {"Sort_num", Int64.Type}})
in
    #"Changed Type"
```


## Table: Alter


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\Alter.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Intervall", type text}, {"Name", type text}, {"Sort_num", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Name", "Alterssegment"}})
in
    #"Renamed Columns"
```


## Table: Filialtyp


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\Filialtyp.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Sheet1_Sheet,{{"Column1", type text}, {"Column2", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"Fililaltyp Abbr", type text}, {"Fililaltyp Name", type text}})
in
    #"Changed Type1"
```


## Table: Warenwelt_sort


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\Warenwelt_sort.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Warenwelt", type text}, {"Warenwelt_sort", Int64.Type}, {"Column3", type any}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column3"})
in
    #"Removed Columns"
```


## Table: Produktfaktor_sort


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\m710321\01 Projects\dm\data\Produltfaktor_sort.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Produktfaktor", type text}, {"Produktfaktor_sort", Int64.Type}, {"Column3", type any}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column3"})
in
    #"Removed Columns"
```

