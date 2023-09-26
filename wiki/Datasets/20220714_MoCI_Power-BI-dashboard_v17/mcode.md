



# M Code

|Dataset|[20220714_MoCI_Power BI dashboard_v17](./../20220714_MoCI_Power-BI-dashboard_v17.md)|
| :--- | :--- |
|Workspace|[APS Team](../../Workspaces/APS-Team.md)|

## Table: CPI_Monthly_Qatar_Sector


```m
let
    Quelle = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    Sheet1_Sheet = Quelle{[Item="CPI Qatar sectors",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Sorted Rows1" = Table.Sort(#"Höher gestufte Header",{{"Year-Month Date", Order.Descending}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Sorted Rows1",{{"Year-Month Date", type date}}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Changed Type1", "Benutzerdefiniert", each Date.AddYears([#"Year-Month Date"],-1)),
    #"Umbenannte Spalten3" = Table.RenameColumns(#"Hinzugefügte benutzerdefinierte Spalte",{{"Benutzerdefiniert", "Reference Year-Month Date"}}),
    #"Merged Queries" = Table.NestedJoin(#"Umbenannte Spalten3", {"INDICATOR", "Reference Year-Month Date"}, #"Umbenannte Spalten3", {"INDICATOR", "Year-Month Date"}, "Umbenannte Spalten3", JoinKind.LeftOuter),
    #"Expanded Umbenannte Spalten3" = Table.ExpandTableColumn(#"Merged Queries", "Umbenannte Spalten3", {"CPI Value"}, {"Umbenannte Spalten3.CPI Value"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Umbenannte Spalten3",{{"Umbenannte Spalten3.CPI Value", "Reference CPI Value"}}),
    #"Hinzugefügte benutzerdefinierte Spalte1" = Table.AddColumn(#"Renamed Columns", "Reference Change Year-to-Year", each ([CPI Value]-[Reference CPI Value])),
    #"Filtered Rows" = Table.SelectRows(#"Hinzugefügte benutzerdefinierte Spalte1", each ([#"Reference Change Year-to-Year"] <> null)),
    #"Sorted Rows" = Table.Sort(#"Filtered Rows",{{"Year-Month Date", Order.Ascending}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Sorted Rows",{{"Reference Change Year-to-Year", type number}, {"Reference CPI Value", type number}, {"CPI Value", type number}, {"Year-Month Date", type date}}),
    #"Merged Queries1" = Table.NestedJoin(#"Changed Type", {"Year-Month Date"}, CPI_Monthly_Qatar_All, {"Year-Month Date"}, "CPI_Monthly_Qatar_All", JoinKind.LeftOuter),
    #"Expanded CPI_Monthly_Qatar_All" = Table.ExpandTableColumn(#"Merged Queries1", "CPI_Monthly_Qatar_All", {"CPI Value"}, {"CPI_Monthly_Qatar_All.CPI Value"}),
    #"Merged Queries0" = Table.NestedJoin(#"Expanded CPI_Monthly_Qatar_All", {"Sector", "Year-Month Date"}, #"CPI Qatar sector weights", {"Sector", "Year-Month Date"}, "CPI Qatar sector weights", JoinKind.LeftOuter),
    #"Expanded CPI_Monthly_Qatar_Sector weights" = Table.ExpandTableColumn(#"Merged Queries0", "CPI Qatar sector weights", {"CPI sector weight"}, {"CPI_Monthly_Qatar_Sector weights.CPI sector weight"}),
    #"Added Custom" = Table.AddColumn(#"Expanded CPI_Monthly_Qatar_Sector weights", "Sector contribution", each ([CPI_Monthly_Qatar_Sector weights.CPI sector weight]*[CPI Value])/[CPI_Monthly_Qatar_All.CPI Value]),
    #"Changed Type0" = Table.TransformColumnTypes(#"Added Custom",{{"Sector contribution", type number}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type0", "Sector contribution in percent", each [Sector contribution]/100),
    #"Changed Type11" = Table.TransformColumnTypes(#"Added Custom1",{{"Sector contribution in percent", Percentage.Type}}),
    #"Added Custom2" = Table.AddColumn(#"Changed Type11", "Sector CPI weighted", each [CPI Value]*[CPI_Monthly_Qatar_Sector weights.CPI sector weight]/100),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom2",{{"Sector CPI weighted", type number}}),
    #"Added Custom3" = Table.AddColumn(#"Changed Type2", "Contribution to inflation", each [#"Reference Change Year-to-Year"]*[Sector contribution in percent]),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Custom3",{{"Contribution to inflation", Percentage.Type}}),
    #"Changed Type4" = Table.TransformColumnTypes(#"Changed Type3",{{"CPI Value", type number}}),
     #"Merged Queries2" = Table.NestedJoin(#"Changed Type4", {"Year-Month Date"}, CPI_Monthly_Qatar_All, {"Year-Month Date"}, "CPI_Monthly_Qatar_All", JoinKind.LeftOuter),
    #"Expanded CPI_Monthly_Qatar_All1" = Table.ExpandTableColumn(#"Merged Queries2", "CPI_Monthly_Qatar_All", {"Reference CPI Value", "Reference Change Year-to-Year"}, {"CPI_Monthly_Qatar_All.Reference CPI Value", "CPI_Monthly_Qatar_All.Reference Change Year-to-Year"}),
    #"Changed Type5" = Table.TransformColumnTypes(#"Expanded CPI_Monthly_Qatar_All1",{{"CPI Value", type number}}),
    #"Added Custom4" = Table.AddColumn(#"Changed Type5", "Contribution to inflation aggregated", each ([CPI_Monthly_Qatar_Sector weights.CPI sector weight]*[#"Reference Change Year-to-Year"])/([CPI_Monthly_Qatar_All.Reference CPI Value]*100)),
    #"Changed Type6" = Table.TransformColumnTypes(#"Added Custom4",{{"Sector CPI weighted", type number}, {"CPI_Monthly_Qatar_All.Reference CPI Value", type number}, {"CPI_Monthly_Qatar_All.Reference Change Year-to-Year", type number}, {"Contribution to inflation aggregated", type number}, {"Sector contribution", type number}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type6",{{"Reference Change Year-to-Year", "Reference Change Year-to-Year (first diff)"}}),
    #"Added Custom5" = Table.AddColumn(#"Renamed Columns1", "Reference Change Year-to-Year", each ([CPI Value]-[Reference CPI Value])/[Reference CPI Value]),
    #"Changed Type7" = Table.TransformColumnTypes(#"Added Custom5",{{"Reference Change Year-to-Year", type number}})
in
    #"Changed Type7"
```


## Table: CPI_Monthly_Qatar_All


```m
let
     Source = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    #"CPI Qatar" = Source{[Item="CPI Qatar",Kind="Sheet"]}[Data],
    #"Höher gestufte Header" = Table.PromoteHeaders(#"CPI Qatar", [PromoteAllScalars=true]),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Höher gestufte Header", "Benutzerdefiniert", each Date.AddYears([#"Year-Month Date"],-1)),
    #"Umbenannte Spalten3" = Table.RenameColumns(#"Hinzugefügte benutzerdefinierte Spalte",{{"Benutzerdefiniert", "Reference Year-Month Date"}}),
    #"Merged Queries" = Table.NestedJoin(#"Umbenannte Spalten3", {"INDICATOR", "Reference Year-Month Date"}, #"Umbenannte Spalten3", {"INDICATOR", "Year-Month Date"}, "Umbenannte Spalten3", JoinKind.LeftOuter),
    #"Expanded Umbenannte Spalten3" = Table.ExpandTableColumn(#"Merged Queries", "Umbenannte Spalten3", {"CPI Value"}, {"Umbenannte Spalten3.CPI Value"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Umbenannte Spalten3",{{"Umbenannte Spalten3.CPI Value", "Reference CPI Value"}}),
    #"Hinzugefügte benutzerdefinierte Spalte1" = Table.AddColumn(#"Renamed Columns", "Reference Change Year-to-Year", each ([CPI Value]-[Reference CPI Value])/[Reference CPI Value]),
    #"Filtered Rows" = Table.SelectRows(#"Hinzugefügte benutzerdefinierte Spalte1", each ([#"Reference Change Year-to-Year"] <> null)),
    #"Sorted Rows" = Table.Sort(#"Filtered Rows",{{"Year-Month Date", Order.Ascending}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Sorted Rows",{{"Reference Change Year-to-Year", type number}, {"Reference CPI Value", type number}, {"CPI Value", type number}, {"Year-Month Date", type date}})
in
    #"Changed Type"
```


## Table: Rebased CPI Value 2018


```m
let
   Source = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    #"CPI rebased_Sheet" = Source{[Item="CPI rebased",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"CPI rebased_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"INDICATOR", type text}, {"CPI Value", type number}, {"Index", type text}, {"Country", type text}, {"Sector", type text}, {"Year", Int64.Type}, {"Month", Int64.Type}, {"Year-Month String", type date}, {"Year-Month Date", type date}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type","General Index","Consumer Price Index, All items",Replacer.ReplaceText,{"Sector"}),
    #"Filtered Rows3" = Table.SelectRows(#"Replaced Value", each ([Sector] <> null)),
    #"Replaced Value1" = Table.ReplaceValue(#"Filtered Rows3","","CPI Monthly",Replacer.ReplaceValue,{"Index"}),
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Replaced Value1", "Benutzerdefiniert", each Date.AddYears([#"Year-Month Date"],-1)),
    #"Renamed Columns1" = Table.RenameColumns(#"Hinzugefügte benutzerdefinierte Spalte",{{"Benutzerdefiniert", "Reference Year-Month Date"}}),
    #"Zusammengeführte Abfragen" = Table.NestedJoin(#"Renamed Columns1", {"Index", "Country", "Sector", "Reference Year-Month Date"}, #"Renamed Columns1", {"Index", "Country", "Sector", "Year-Month Date"}, "Umbenannte Spalten3", JoinKind.Inner),
    #"Erweiterte Umbenannte Spalten3" = Table.ExpandTableColumn(#"Zusammengeführte Abfragen", "Umbenannte Spalten3", {"CPI Value"}, {"Umbenannte Spalten3.CPI Value"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Erweiterte Umbenannte Spalten3",{{"Umbenannte Spalten3.CPI Value", "Reference CPI Value"}}),
    #"Hinzugefügte benutzerdefinierte Spalte1" = Table.AddColumn(#"Renamed Columns2", "Reference Change Year-to-Year", each ([CPI Value]-[Reference CPI Value])/[Reference CPI Value]),
    #"Filtered Rows" = Table.SelectRows(#"Hinzugefügte benutzerdefinierte Spalte1", each ([Country] <> " China" and [Country] <> " Germany" and [Country] <> " India")),
    #"Changed Type1" = Table.TransformColumnTypes(#"Filtered Rows",{{"Reference Change Year-to-Year", Percentage.Type}}),
    #"Appended Query" = Table.Combine({#"Changed Type1", CPI_Monthly_Qatar_Sector, CPI_Monthly_Qatar_All}),
    #"Filtered Rows1" = Table.SelectRows(#"Appended Query", each ([#"Year-Month Date"] <> #date(2010, 1, 1) and [#"Year-Month Date"] <> #date(2010, 2, 1) and [#"Year-Month Date"] <> #date(2010, 3, 1) and [#"Year-Month Date"] <> #date(2010, 4, 1) and [#"Year-Month Date"] <> #date(2010, 5, 1) and [#"Year-Month Date"] <> #date(2010, 6, 1) and [#"Year-Month Date"] <> #date(2010, 7, 1) and [#"Year-Month Date"] <> #date(2010, 8, 1) and [#"Year-Month Date"] <> #date(2010, 9, 1) and [#"Year-Month Date"] <> #date(2010, 10, 1) and [#"Year-Month Date"] <> #date(2010, 11, 1) and [#"Year-Month Date"] <> #date(2010, 12, 1))),
    #"Changed Type2" = Table.TransformColumnTypes(#"Filtered Rows1",{{"CPI Value", type number}}),
    #"Removed Duplicates" = Table.Distinct(#"Changed Type2", {"Country", "Sector", "Year-Month Date", "CPI Value"}),
    #"Appended Query1" = Table.Combine({#"Removed Duplicates", CPI_Monthly_Qatar_Sector}),
    #"Changed Type3" = Table.TransformColumnTypes(#"Appended Query1",{{"Reference Change Year-to-Year", type number}})
in
    #"Changed Type3"
```


## Table: Rebased CPI Value 2018 - All


```m
let
    Source = #"Rebased CPI Value 2018",
    #"Filtered Rows1" = Table.SelectRows(Source, each true),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows1",{{"CPI Value", type number}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Changed Type",{{"Reference Change Year-to-Year", type number}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type1", each ([Sector] = " Consumer Price Index, All items"))
in
    #"Filtered Rows"
```


## Table: Rebased CPI Value 2018 - sector


```m
let
    Source = #"Rebased CPI Value 2018",
    #"Filtered Rows" = Table.SelectRows(Source, each ([Sector] <> " Consumer Price Index, All items")),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"Reference Change Year-to-Year", type number}, {"CPI Value", type number}}),
    #"Removed Duplicates" = Table.Distinct(#"Changed Type", {"CPI Value", "Country", "Sector", "Year-Month Date"})
in
    #"Removed Duplicates"
```


## Table: Rebased PPI Value 2018


```m
let
   Source = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    #"PPI rebased_Sheet" = Source{[Item="PPI rebased",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"PPI rebased_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Year-Month Date", type date}, {"CPI Value", type number}})
in
    #"Changed Type"
```


## Table: Rebased PPI Value 2018 - year on year


```m
let
    Source = #"Rebased PPI Value 2018",
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Rebased PPI Value 2018", "Benutzerdefiniert", each Date.AddYears([#"Year-Month Date"],-1)),
    #"Umbenannte Spalten3" = Table.RenameColumns(#"Hinzugefügte benutzerdefinierte Spalte",{{"Benutzerdefiniert", "Reference Year-Month Date"}}),
    #"Merged Queries" = Table.NestedJoin(#"Umbenannte Spalten3", {"Reference Year-Month Date"}, #"Umbenannte Spalten3", {"Year-Month Date"}, "Removed Columns", JoinKind.LeftOuter),
    #"Expanded Removed Columns1" = Table.ExpandTableColumn(#"Merged Queries", "Removed Columns", {"CPI Value"}, {"Removed Columns.CPI Value"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Removed Columns1", "Reference Change Year-to-Year", each ([CPI Value]-[Removed Columns.CPI Value])/[Removed Columns.CPI Value]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"Removed Columns.CPI Value", "Reference CPI Value"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"Reference Change Year-to-Year", Percentage.Type}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type1","","Qatar",Replacer.ReplaceValue,{"Country"}),
    #"Filtered Rows" = Table.SelectRows(#"Replaced Value", each ([Year] <> 2013))
in
    #"Filtered Rows"
```


## Table: Rebased PPI Value 2018 - sector


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="PPI sector rebased",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Replaced Value" = Table.ReplaceValue(#"Promoted Headers","","Qatar",Replacer.ReplaceValue,{"Country"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Replaced Value",{{"CPI Value", type number}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Changed Type",{{"Year-Month Date", type date}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type1", each ([Sector] <> "Printing And Reproduction Of Recorded Media") and ([Year] <> 2013))
in
    #"Filtered Rows"
```


## Table: Rebased PPI Value 2018 - sector year-on-year


```m
let
    Source = #"Rebased PPI Value 2018 - sector",
    #"Hinzugefügte benutzerdefinierte Spalte" = Table.AddColumn(#"Rebased PPI Value 2018 - sector", "Benutzerdefiniert1", each Date.AddYears([#"Year-Month Date"],-1)),
    #"Umbenannte Spalten3" = Table.RenameColumns(#"Hinzugefügte benutzerdefinierte Spalte",{{"Benutzerdefiniert1", "Reference Year-Month Date"}}),
    #"Merged Queries" = Table.NestedJoin(#"Umbenannte Spalten3", {"Reference Year-Month Date"}, #"Umbenannte Spalten3", {"Year-Month Date"}, "Removed Columns", JoinKind.LeftOuter),
    #"Expanded Removed Columns1" = Table.ExpandTableColumn(#"Merged Queries", "Removed Columns", {"CPI Value"}, {"Removed Columns.CPI Value"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Removed Columns1", "Reference Change Year-to-Year", each ([CPI Value]-[Removed Columns.CPI Value])/[Removed Columns.CPI Value]),
    #"Merged Queries1" = Table.NestedJoin(#"Added Custom", {"Year-Month Date"}, #"Rebased PPI Value 2018", {"Year-Month Date"}, "CPI_Monthly_Qatar_All", JoinKind.LeftOuter),
    #"Expanded CPI_Monthly_Qatar_All" = Table.ExpandTableColumn(#"Merged Queries1", "CPI_Monthly_Qatar_All", {"CPI Value"}, {"CPI_Monthly_Qatar_All.CPI Value"}),
    #"Added Custom1" = Table.AddColumn(#"Expanded CPI_Monthly_Qatar_All", "Reference Change Year-to-Year CPI total base", each ([CPI Value]-[Removed Columns.CPI Value])/[CPI_Monthly_Qatar_All.CPI Value]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom1",{{"Removed Columns.CPI Value", "Reference CPI Value"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","","Qatar",Replacer.ReplaceValue,{"Country"}),
    #"Filtered Rows" = Table.SelectRows(#"Replaced Value", each ([Year] <> 2013)),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"Reference Change Year-to-Year", type number}, {"Reference Change Year-to-Year CPI total base", type number}})
in
    #"Changed Type"
```


## Table: Invoked Function


```m
let
    Source = #"English x-axis"(#date(2010, 1, 1), #date(2023, 1, 1), "EN"),
    #"Renamed Columns" = Table.RenameColumns(Source,{{"Date", "Year-Month Date"}}),
    #"Added Index" = Table.AddIndexColumn(#"Renamed Columns", "Index", 0, 1, Int64.Type),
    #"Filtered Rows" = Table.SelectRows(#"Added Index", each ([DayOfMonth] = 1) and ([Year] <> 2010)),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"Year", Int64.Type}, {"QuarterOfYear", Int64.Type}, {"MonthOfYear", Int64.Type}, {"DayOfMonth", Int64.Type}, {"DayInWeek", Int64.Type}, {"Index", Int64.Type}}),
    #"Filtered Rows1" = Table.SelectRows(#"Changed Type", each true),
    #"Duplicated Column" = Table.DuplicateColumn(#"Filtered Rows1", "MonthOfYear", "MonthOfYear - Copy"),
    #"Changed Type1" = Table.TransformColumnTypes(#"Duplicated Column",{{"MonthOfYear - Copy", type text}})
in
    #"Changed Type1"
```


## Table: CPI Monthly forecast


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    varsheet = Source{[Item="VAR",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(varsheet, [PromoteAllScalars=true])
 in
    #"Promoted Headers"
```


## Table: Inflation forecast


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    Uncertyoy = Source{[Item="uncert_index_yoy",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Uncertyoy, [PromoteAllScalars=true]),
    #"Removed Top Rows" = Table.Skip(#"Promoted Headers",12),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Top Rows",{{"cpi_yoy", type number}, {"date", type date}, {"pred_winner", type number}, {"upper", type number}, {"lower", type number}})
in
    #"Changed Type"
```


## Table: CPI forecast


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    Uncertsheet = Source{[Item="uncert_index_lvl",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Uncertsheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"date", type date}, {"upper", type number}, {"lower", type number}, {"cpi_lvl", type number}, {"pred_winner", type number}})
in
    #"Changed Type"
```


## Table: Monthly forecast - CPI sectors


```m
let
    Source = #"CPI Monthly forecast",
    #"Removed Columns" = Table.RemoveColumns(Source,{"PCPI_IX_lvl_VAR", "PCPIA_IX_lvl_VAR", "PCPIEC_IX_lvl_VAR", "PCPIED_IX_lvl_VAR", "PCPIFBT_IX_lvl_VAR", "PCPIF_IX_lvl_VAR", "PCPIHO_IX_lvl_VAR", "PCPIH_IX_lvl_VAR", "PCPIM_IX_lvl_VAR", "PCPIO_IX_lvl_VAR", "PCPIRE_IX_lvl_VAR", "PCPIR_IX_lvl_VAR", "PCPIT_IX_lvl_VAR", "PCPIT_IX_lvl_VAR_1", "PCPIA_IX_yoy_VAR", "PCPIEC_IX_yoy_VAR", "PCPIED_IX_yoy_VAR", "PCPIFBT_IX_yoy_VAR", "PCPIF_IX_yoy_VAR", "PCPIHO_IX_yoy_VAR", "PCPIH_IX_yoy_VAR", "PCPIM_IX_yoy_VAR", "PCPIO_IX_yoy_VAR", "PCPIRE_IX_yoy_VAR", "PCPIR_IX_yoy_VAR", "PCPIT_IX_yoy_VAR", "PCPI_IX_2022.03.01_lvl_VAR", "PCPIA_IX_2022.03.01_lvl_VAR", "PCPIEC_IX_2022.03.01_lvl_VAR", "PCPIED_IX_2022.03.01_lvl_VAR", "PCPIFBT_IX_2022.03.01_lvl_VAR", "PCPIF_IX_2022.03.01_lvl_VAR", "PCPIHO_IX_2022.03.01_lvl_VAR", "PCPIH_IX_2022.03.01_lvl_VAR", "PCPIM_IX_2022.03.01_lvl_VAR", "PCPIO_IX_2022.03.01_lvl_VAR", "PCPIRE_IX_2022.03.01_lvl_VAR", "PCPIR_IX_2022.03.01_lvl_VAR", "PCPIT_IX_2022.03.01_lvl_VAR", "PCPI_IX_2022.04.01_lvl_VAR", "PCPI_IX_2022.03.01_yoy_VAR", "PCPIA_IX_2022.03.01_yoy_VAR", "PCPIEC_IX_2022.03.01_yoy_VAR", "PCPIED_IX_2022.03.01_yoy_VAR", "PCPIFBT_IX_2022.03.01_yoy_VAR", "PCPIF_IX_2022.03.01_yoy_VAR", "PCPIHO_IX_2022.03.01_yoy_VAR", "PCPIH_IX_2022.03.01_yoy_VAR", "PCPIM_IX_2022.03.01_yoy_VAR", "PCPIO_IX_2022.03.01_yoy_VAR", "PCPIRE_IX_2022.03.01_yoy_VAR", "PCPIR_IX_2022.03.01_yoy_VAR", "PCPIT_IX_2022.03.01_yoy_VAR", "PCPI_IX_2022.04.01_yoy_VAR", "Clothing and footwear_2", "Communication_3", "Education_4", "Tobacco_5", "Food and non-alcoholic beverages_6", "Furnishings, household equipment and routine household maintenance_7", "Housing, Water, Electricity, Gas and Other Fuels_8", "Health_9", "Miscellaneous goods and services_10", "Restaurants and hotels_11", "Recreation and culture_12", "Transport_13"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"date"}, "Attribute", "Value"),
    #"Changed Type" = Table.TransformColumnTypes(#"Unpivoted Columns",{{"Value", type number}, {"date", type date}})
in
    #"Changed Type"
```


## Table: Monthly forecast - inflation sectors


```m
let
    Source = #"CPI Monthly forecast",
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"date", type date}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"PCPI_IX_lvl_VAR", "PCPIA_IX_lvl_VAR", "PCPIEC_IX_lvl_VAR", "PCPIED_IX_lvl_VAR", "PCPIFBT_IX_lvl_VAR", "PCPIF_IX_lvl_VAR", "PCPIHO_IX_lvl_VAR", "PCPIH_IX_lvl_VAR", "PCPIM_IX_lvl_VAR", "PCPIO_IX_lvl_VAR", "PCPIRE_IX_lvl_VAR", "PCPIR_IX_lvl_VAR", "PCPIT_IX_lvl_VAR", "PCPIT_IX_lvl_VAR_1", "PCPIA_IX_yoy_VAR", "PCPIEC_IX_yoy_VAR", "PCPIED_IX_yoy_VAR", "PCPIFBT_IX_yoy_VAR", "PCPIF_IX_yoy_VAR", "PCPIHO_IX_yoy_VAR", "PCPIH_IX_yoy_VAR", "PCPIM_IX_yoy_VAR", "PCPIO_IX_yoy_VAR", "PCPIRE_IX_yoy_VAR", "PCPIR_IX_yoy_VAR", "PCPIT_IX_yoy_VAR", "PCPI_IX_2022.03.01_lvl_VAR", "PCPIA_IX_2022.03.01_lvl_VAR", "PCPIEC_IX_2022.03.01_lvl_VAR", "PCPIED_IX_2022.03.01_lvl_VAR", "PCPIFBT_IX_2022.03.01_lvl_VAR", "PCPIF_IX_2022.03.01_lvl_VAR", "PCPIHO_IX_2022.03.01_lvl_VAR", "PCPIH_IX_2022.03.01_lvl_VAR", "PCPIM_IX_2022.03.01_lvl_VAR", "PCPIO_IX_2022.03.01_lvl_VAR", "PCPIRE_IX_2022.03.01_lvl_VAR", "PCPIR_IX_2022.03.01_lvl_VAR", "PCPIT_IX_2022.03.01_lvl_VAR", "PCPI_IX_2022.04.01_lvl_VAR", "Clothing and footwear", "Communication", "Education", "Tobacco", "Food and non-alcoholic beverages", "Furnishings, household equipment and routine household maintenance", "Housing, Water, Electricity, Gas and Other Fuels", "Health", "Miscellaneous goods and services", "Restaurants and hotels", "Recreation and culture", "Transport", "PCPI_IX_2022.03.01_yoy_VAR", "PCPIA_IX_2022.03.01_yoy_VAR", "PCPIEC_IX_2022.03.01_yoy_VAR", "PCPIED_IX_2022.03.01_yoy_VAR", "PCPIFBT_IX_2022.03.01_yoy_VAR", "PCPIF_IX_2022.03.01_yoy_VAR", "PCPIHO_IX_2022.03.01_yoy_VAR", "PCPIH_IX_2022.03.01_yoy_VAR", "PCPIM_IX_2022.03.01_yoy_VAR", "PCPIO_IX_2022.03.01_yoy_VAR", "PCPIRE_IX_2022.03.01_yoy_VAR", "PCPIR_IX_2022.03.01_yoy_VAR", "PCPIT_IX_2022.03.01_yoy_VAR", "PCPI_IX_2022.04.01_yoy_VAR"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"date"}, "Attribute", "Value"),
    #"Extracted Text Before Delimiter" = Table.TransformColumns(#"Unpivoted Columns", {{"Attribute", each Text.BeforeDelimiter(_, "_"), type text}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Extracted Text Before Delimiter",{{"Value", type number}})
in
    #"Changed Type1"
```


## Table: CPI Qatar sector weights


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\M712182\Roland Berger Holding GmbH\MoCI Inflation Study - General\07 Dashboards\MoCI Power BI MASTER data.xlsx"), null, true),
    #"CPI Qatar sector weights_Sheet" = Source{[Item="CPI Qatar sector weights",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"CPI Qatar sector weights_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Index", type text}, {"Country", type text}, {"Sector", type text}, {"INDICATOR", type text}, {"source", type text}, {"sdate", type date}, {"edate", type date}, {"dupl", Int64.Type}, {"Year", Int64.Type}, {"Month", Int64.Type}, {"CPI sector weight", type number}, {"Year-Month String", type date}, {"Year-Month Date", type date}})
in
    #"Changed Type"
```

