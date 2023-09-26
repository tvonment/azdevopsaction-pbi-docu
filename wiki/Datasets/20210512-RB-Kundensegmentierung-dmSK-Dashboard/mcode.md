



# M Code

|Dataset|[20210512 RB Kundensegmentierung dmSK Dashboard](./../20210512-RB-Kundensegmentierung-dmSK-Dashboard.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: Segment_Age


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\SK_DESCR_df_age_det_C10_S95_v003.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"CUST_SEG", Int64.Type}, {"INTERVAL", Int64.Type}, {"CUST_SEG_NAME", type text}, {"AVG_AGE_CUT", type text}, {"AVG_AGE_ABS", Int64.Type}, {"AVG_AGE_PCT", type number}, {"AVG_AGE_IDX", type number}}),
    #"Filled Down" = Table.FillDown(#"Changed Type",{"CUST_SEG"}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Filled Down",{{"AVG_AGE_PCT", type number}})
in
    #"Geänderter Typ"
```


## Table: Segment_Warenwelt


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\SK_DESCR_df_kpi_assoc_C10_S95_v003.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Promoted Headers", {"Column1", "CUST_SEG_NAME"}, "Attribute", "Value"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Unpivoted Columns", "Attribute", Splitter.SplitTextByEachDelimiter({"_"}, QuoteStyle.Csv, true), {"Attribute.1", "Attribute.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Attribute.1", type text}, {"Attribute.2", type text}}),
    #"Pivoted Column" = Table.Pivot(#"Changed Type1", List.Distinct(#"Changed Type1"[Attribute.2]), "Attribute.2", "Value", List.Sum),
    #"Renamed Columns" = Table.RenameColumns(#"Pivoted Column",{{"Attribute.1", "Warenwelt"}}),
    #"Split Column by Delimiter1" = Table.SplitColumn(#"Renamed Columns", "Warenwelt", Splitter.SplitTextByDelimiter("_", QuoteStyle.Csv), {"Warenwelt.1", "Warenwelt.2"}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Split Column by Delimiter1",{{"Warenwelt.1", type text}, {"Warenwelt.2", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type2",{"Warenwelt.2"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns",{{"Warenwelt.1", "Warenwelt"}}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Renamed Columns1",{{"PCT", type number}, {"ABS", Int64.Type}, {"IDX", type number}})
in
    #"Geänderter Typ"
```


## Table: Segment_Tag


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\SK_DESCR_df_kpi_day_C10_S95_v003.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Column1", Int64.Type}, {"CUST_SEG_NAME", type text}, {"MO_ABS", Int64.Type}, {"MO_PCT", type number}, {"MO_IDX", type number}, {"DI_ABS", Int64.Type}, {"DI_PCT", type number}, {"DI_IDX", type number}, {"MI_ABS", Int64.Type}, {"MI_PCT", type number}, {"MI_IDX", type number}, {"DO_ABS", Int64.Type}, {"DO_PCT", type number}, {"DO_IDX", type number}, {"FR_ABS", Int64.Type}, {"FR_PCT", type number}, {"FR_IDX", type number}, {"SA_ABS", Int64.Type}, {"SA_PCT", type number}, {"SA_IDX", type number}, {"SO_ABS", Int64.Type}, {"SO_PCT", type number}, {"SO_IDX", type number}}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"Column1", "CUST_SEG_NAME"}, "Attribute", "Value"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Unpivoted Columns", "Attribute", Splitter.SplitTextByDelimiter("_", QuoteStyle.Csv), {"Attribute.1", "Attribute.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Attribute.1", type text}, {"Attribute.2", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"Attribute.1", "Day"}}),
    #"Pivoted Column" = Table.Pivot(#"Renamed Columns", List.Distinct(#"Renamed Columns"[Attribute.2]), "Attribute.2", "Value", List.Sum),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Pivoted Column",{{"PCT", type number}, {"IDX", Int64.Type}}),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Geänderter Typ",{{"PCT", type number}})
in
    #"Geänderter Typ1"
```


## Table: Segment_Detail/Rabatt


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\SK_DESCR_df_kpi_det_C10_S95_v003.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Filled Down" = Table.FillDown(#"Promoted Headers",{"CUST_SEG"}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Filled Down",{{"Artikelrabatt_REV_SHR_PCT", type number}, {"Artikelrabatt_REV_SHR_IDX", type number}, {"Artikelrabatt_REV_SHR_ABS", type number}, {"Wert_Artikelpunkte_BON_SHR_ABS", type number}, {"Wert_Artikelpunkte_BON_SHR_IDX", type number}, {"Wert_Artikelpunkte_BON_SHR_PCT", type number}, {"DM_MARKE_KZ_REV_SHR_PCT", type number}, {"DM_MARKE_KZ_REV_SHR_IDX", type number}, {"BIOARTIKELKZ_REV_SHR_PCT", type number}, {"BIOARTIKELKZ_REV_SHR_IDX", type number}, {"LEBENSMITTELKZ_REV_SHR_PCT", type number}, {"LEBENSMITTELKZ_REV_SHR_IDX", type number}})
in
    #"Geänderter Typ"
```


## Table: Segment_Filialtyp


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Output1_SK_prep.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Promoted Headers",{{"PCT", type number}, {"IDX", type number}}),
    #"Neu angeordnete Spalten" = Table.ReorderColumns(#"Geänderter Typ",{"F1", "CUST_SEG_NAME", "FIL_TIP", "Column3", "PCT", "IDX"})
in
    #"Neu angeordnete Spalten"
```


## Table: Segment_KPIs


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\SK_DESCR_df_kpi_main_C10_S95_v003.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Entfernte untere Zeilen" = Table.RemoveLastN(#"Promoted Headers",1),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Entfernte untere Zeilen",{{"SIZE_PCT", type number}, {"AVG_AGE_ABS", type number}, {"AVG_AGE_IDX", type number}, {"SIZE_ABS", type number}, {"SIZE_IDX", type number}, {"AVG_FEMALE_PCT", type number}, {"AVG_FEMALE_IDX", type number}, {"AVG_MALE_PCT", type number}, {"AVG_MALE_IDX", type number}, {"REV_SHR_PCT", type number}, {"REV_SHR_IDX", type number}, {"AVG_BON_EUR_ABS", type number}, {"AVG_BON_EUR_IDX", type number}, {"FREQ_ABS", type number}, {"FREQ_IDX", type number}, {"Artikelrabatt_REV_SHR_PCT", type number}, {"Artikelrabatt_REV_SHR_IDX", type number}, {"Bonrabatt_REV_SHR_PCT", type number}, {"Bonrabatt_REV_SHR_IDX", type number}, {"Wert_Artikelpunkte_REV_SHR_PCT", type number}, {"Wert_Artikelpunkte_REV_SHR_IDX", type number}, {"Wert_Bonsonderpunkte_REV_SHR_PCT", type number}, {"Wert_Bonsonderpunkte_REV_SHR_IDX", type number}, {"ONLINE_REV_SHR_PCT", type number}, {"ONLINE_REV_SHR_IDX", type number}, {"PROMO_REV_SHR_PCT", type number}, {"PROMO_REV_SHR_IDX", type number}, {"DM_MARKE_KZ_REV_SHR_PCT", type number}, {"DM_MARKE_KZ_REV_SHR_IDX", type number}, {"MARKE_REV_SHR_PCT", type number}, {"MARKE_REV_SHR_IDX", type number}, {"DM_BALEA_REV_SHR_PCT", type number}, {"DM_BALEA_REV_SHR_IDX", type number}, {"BIOARTIKELKZ_REV_SHR_PCT", type number}, {"BIOARTIKELKZ_REV_SHR_IDX", type number}, {"GLUTENFREIKZ_REV_SHR_PCT", type number}, {"GLUTENFREIKZ_REV_SHR_IDX", type number}, {"LEBENSMITTELKZ_REV_SHR_PCT", type number}, {"LEBENSMITTELKZ_REV_SHR_IDX", type number}, {"Artikelrabatt_BON_SHR_PCT", type number}, {"Artikelrabatt_BON_SHR_IDX", type number}, {"Bonrabatt_BON_SHR_PCT", type number}, {"Bonrabatt_BON_SHR_IDX", type number}, {"Wert_Artikelpunkte_BON_SHR_PCT", type number}, {"Wert_Artikelpunkte_BON_SHR_IDX", type number}, {"Wert_Bonsonderpunkte_BON_SHR_PCT", type number}, {"Wert_Bonsonderpunkte_BON_SHR_IDX", type number}, {"ONLINE_BON_SHR_PCT", type number}, {"ONLINE_BON_SHR_IDX", type number}})
in
    #"Geänderter Typ"
```


## Table: Segment_RFM


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\SK_DESCR_df_kpi_rfm_C10_S95_v003.xlsx"), null, true),
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
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\SK_DESCR_df_pf_revenue_db_C10_S95_v003.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"PCT", type number}, {"IDX", type number}}),
    #"Filled Down" = Table.FillDown(#"Changed Type",{"Column1"}),
    #"Renamed Columns" = Table.RenameColumns(#"Filled Down",{{"Column2", "Produktfaktor"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","Schönheitskundinnen","Schönheitskundinnen mit Eigenmarkenfokus",Replacer.ReplaceText,{"Column1"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Grundversorger mit Fokus Bio","Grundversorger LOHAS",Replacer.ReplaceText,{"Column1"}),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Replaced Value1",{{"PCT", type number}})
in
    #"Geänderter Typ"
```


## Table: Top Produkte


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\SK_DESCR_df_top_pg_db_C10_S95_v003.xlsx"), null, true),
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


## Table: Intervall_Bio


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Intervalle.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Intervall", type text}, {"Name", type text}, {"Sort_num", Int64.Type}})
in
    #"Changed Type"
```


## Table: Intervall_DM_Marke


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Intervalle_equal.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Intervall", type text}, {"Name", type text}, {"Sort_num", Int64.Type}})
in
    #"Changed Type"
```


## Table: Intervall_Lebensmittel


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Intervall_Lebensmittel.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Intervall", type text}, {"Name", type text}, {"Sort_num", Int64.Type}})
in
    #"Changed Type"
```


## Table: Tage_sort


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Tage_sort.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Tag", type text}, {"Sort_num", Int64.Type}})
in
    #"Changed Type"
```


## Table: Alter


```m
let
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Alter.xlsx"), null, true),
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
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Filialtyp.xlsx"), null, true),
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
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Warenwelt_sort.xlsx"), null, true),
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
    Source = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Produltfaktor_sort.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Produktfaktor", type text}, {"Produktfaktor_sort", Int64.Type}, {"Column3", type any}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column3"})
in
    #"Removed Columns"
```


## Table: Segmente


```m
let
    Quelle = Excel.Workbook(File.Contents("\\rolandberger.net\DFS\MUC\services4\bits\analytics_tools\02_Projects\dm 2021\02_Unterlagen\SK\07_Dashboard\Input\Segmente.xlsx"), null, true),
    Sheet1_Sheet = Quelle{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Geänderter Typ" = Table.TransformColumnTypes(#"Höher gestufte Header",{{"Segmente_nr", Int64.Type}, {"Segmente", type text}, {"Segmente Namen neu", type text}})
in
    #"Geänderter Typ"
```

