



# M Code

|Dataset|[ICA](./../ICA.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: FC_DATA


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_DATA_SUM = Corima{[Schema="dbo",Item="V_DW_LIP_DATA_SUM"]}[Data],
    #"Filtered Plan Variant" = Table.SelectRows(dbo_V_DW_LIP_DATA_SUM, each [PLAN_VARIANT_ID] > 79),
    #"Inserted Week of Year" = Table.AddColumn(#"Filtered Plan Variant", "Week of Year", each Date.WeekOfYear([PERIODE_DATE],2), Int64.Type),
    #"Removed Columns" = Table.RemoveColumns(#"Inserted Week of Year",{"PERIOD"}),
    #"Inserted Day of Week" = Table.AddColumn(#"Removed Columns", "Day of Week", each Date.DayOfWeek([PERIODE_DATE]), Int64.Type),
    #"Inserted Year" = Table.AddColumn(#"Inserted Day of Week", "Year", each Date.Year([PERIODE_DATE]), Int64.Type),
    #"Inserted End of Month" = Table.AddColumn(#"Inserted Year", "End of Month", each Date.EndOfMonth([PERIODE_DATE]), type date),
    #"Added Custom" = Table.AddColumn(#"Inserted End of Month", "Days to Month End", each [End of Month] - [PERIODE_DATE]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Days to Month End", type number}}),
    #"Added Conditional Column" = Table.AddColumn(#"Changed Type", "Weekbreak_ID", each if ([Days to Month End]) >= 6 then 1 else 0 ),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "Weekbreak_ID_2", each if [PERIODE_DATE] = #date(2021, 12, 27) then 1 else [Weekbreak_ID]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Conditional Column1",{{"Weekbreak_ID", type number}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type1", "Week of Year( Leading Zero) ", each Number.ToText( [Week of Year], "D2")),
    #"Inserted Merged Column" = Table.AddColumn(#"Added Custom1", "YearWeekOfYear", each Text.Combine({Text.From([Year], "de-DE"), Text.From([Week of Year], "de-DE")}, ""), type text),
    #"Inserted Merged Column1" = Table.AddColumn(#"Inserted Merged Column", "YearWeekOfYear(LeadingZero)", each Text.Combine({Text.From([Year], "de-DE"), [#"Week of Year( Leading Zero) "]}, ""), type text),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Merged Column1", each true),
    #"Changed Type2" = Table.TransformColumnTypes(#"Filtered Rows",{{"YearWeekOfYear(LeadingZero)", Int64.Type}})
in
    #"Changed Type2"
```


## Table: RB_COMPANIES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_RB_COMPANIES = ByD_ODP{[Schema="dbo",Item="BYD_RB_COMPANIES"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_BYD_RB_COMPANIES, each true),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows", "Merged", each Text.Combine({[COUNTRY_ISO3], [ORGANIZATIONAL_CCENTER_ID]}, " ("), type text),
    #"Added Suffix" = Table.TransformColumns(#"Inserted Merged Column", {{"Merged", each _ & ")", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Added Suffix",{{"Merged", "Company_Slicer"}})
in
    #"Renamed Columns"
```


## Table: 1_Measure_FC


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: ZZ_RollingCalender


```m
let
    Source = #date(2019,01,01),
    Custom1 = List.Dates (Source, Number.From(Date.AddDays(DateTime.LocalNow(), 110)) - Number.From(Source), #duration(1,0,0,0)),
    #"Converted to Table" = Table.FromList(Custom1, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Changed Type" = Table.TransformColumnTypes(#"Converted to Table",{{"Column1", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Date"}}),
    #"Inserted Month Name" = Table.AddColumn(#"Renamed Columns", "Month Name", each Date.MonthName([Date]), type text),
    #"Extracted First Characters" = Table.TransformColumns(#"Inserted Month Name", {{"Month Name", each Text.Start(_, 3), type text}}),
    #"Inserted Year" = Table.AddColumn(#"Extracted First Characters", "Year", each Date.Year([Date]), Int64.Type),
    #"Extracted Last Characters" = Table.TransformColumns(#"Inserted Year", {{"Year", each Text.End(Text.From(_, "de-DE"), 2), type text}}),
    #"Merged Columns" = Table.CombineColumns(#"Extracted Last Characters",{"Month Name", "Year"},Combiner.CombineTextByDelimiter("-", QuoteStyle.None),"Date_short"),
    #"Inserted Year1" = Table.AddColumn(#"Merged Columns", "Year", each Date.Year([Date]), Int64.Type),
    #"Multiplied Column" = Table.TransformColumns(#"Inserted Year1", {{"Year", each _ * 100, type number}}),
    #"Inserted Month" = Table.AddColumn(#"Multiplied Column", "Month", each Date.Month([Date]), Int64.Type),
    #"Inserted Addition" = Table.AddColumn(#"Inserted Month", "Addition", each [Year] + [Month], type number),
    #"Renamed Columns1" = Table.RenameColumns(#"Inserted Addition",{{"Addition", "Date_sort"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns1", "0", each 0),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"0"}),
    #"Inserted Week of Year" = Table.AddColumn(#"Removed Columns", "Week of Year", each Date.WeekOfYear([Date]), Int64.Type),
    #"Inserted Week of Year1" = Table.AddColumn(#"Inserted Week of Year", "Week of Year.1", each Date.WeekOfYear([Date]), Int64.Type),
    #"Inserted Year2" = Table.AddColumn(#"Inserted Week of Year1", "Year.1", each Date.Year([Date]), Int64.Type),
    #"Extracted Last Characters1" = Table.TransformColumns(#"Inserted Year2", {{"Year.1", each Text.End(Text.From(_, "de-DE"), 2), type text}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Extracted Last Characters1",{"Date", "Date_short", "Year", "Month", "Date_sort", "Week of Year", "Year.1", "Week of Year.1"}),
    #"Merged Columns1" = Table.CombineColumns(Table.TransformColumnTypes(#"Reordered Columns", {{"Week of Year.1", type text}}, "de-DE"),{"Year.1", "Week of Year.1"},Combiner.CombineTextByDelimiter("-", QuoteStyle.None),"Year_Cw"),
    #"Renamed Columns2" = Table.RenameColumns(#"Merged Columns1",{{"Year_Cw", "Year_CW"}}),
    #"Inserted Year3" = Table.AddColumn(#"Renamed Columns2", "Year.1", each Date.Year([Date]), Int64.Type),
    #"Reordered Columns1" = Table.ReorderColumns(#"Inserted Year3",{"Date", "Year.1", "Month", "Week of Year", "Date_short", "Year", "Date_sort", "Year_CW"}),
    #"Renamed Columns3" = Table.RenameColumns(#"Reordered Columns1",{{"Year", "Year_adj"}, {"Year.1", "Year"}}),
    #"Duplicated Column" = Table.AddColumn(#"Renamed Columns3", "Subtraction", each [Week of Year] - 1, type number),
    #"Renamed Columns4" = Table.RenameColumns(#"Duplicated Column",{{"Subtraction", "Week_of_Year_Interim"}}),
    #"Added Conditional Column" = Table.AddColumn(#"Renamed Columns4", "Calendar Week", each if [Week_of_Year_Interim] = 0 then 52 else [Week_of_Year_Interim]),
    #"Inserted Merged Column" = Table.AddColumn(#"Added Conditional Column", "Y-CW_long", each Text.Combine({Text.From([Year], "de-DE"), Text.From([Week of Year], "de-DE")}, "/"), type text),
    #"CW for ActulasLQ" = Table.AddColumn(#"Inserted Merged Column", "Calendar Week(ActualLQ)", each if [Date] = #date(2022, 1, 1) then null else if [Date] = #date(2022, 1, 2) then null else [Calendar Week]),
    #"Removed Columns1" = Table.RemoveColumns(#"CW for ActulasLQ",{"Calendar Week(ActualLQ)"})
in
    #"Removed Columns1"
```


## Table: 1_Measure_LQ


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: MD_BANK ACCOUNTS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_MDM_ACCOUNT_IF_SET = Corima{[Schema="dbo",Item="V_DW_MDM_ACCOUNT_IF_SET"]}[Data]
in
    dbo_V_DW_MDM_ACCOUNT_IF_SET
```


## Table: MD_BANKS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_MDM_PARTNER = Corima{[Schema="dbo",Item="V_DW_MDM_PARTNER"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_MDM_PARTNER, each ([PARTNER_TYPE] = "External"))
in
    #"Filtered Rows"
```


## Table: MD_CURRENCY


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_DW_CIB_BALANCES = Corima{[Schema="dbo",Item="DW_CIB_BALANCES"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_DW_CIB_BALANCES, each [DATUM] > #datetime(2018, 12, 31, 0, 0, 0)),
    #"Inserted Year" = Table.AddColumn(#"Filtered Rows", "Year", each Date.Year([DATUM]), Int64.Type),
    #"Inserted Month" = Table.AddColumn(#"Inserted Year", "Month", each Date.Month([DATUM]), Int64.Type),
    #"Inserted Week of Year" = Table.AddColumn(#"Inserted Month", "Week of Year", each Date.WeekOfYear([DATUM]), Int64.Type),
    #"Inserted Day of Week" = Table.AddColumn(#"Inserted Week of Year", "Day of Week", each Date.DayOfWeek([DATUM]), Int64.Type),
    #"Changed Type" = Table.TransformColumnTypes(#"Inserted Day of Week",{{"DATUM", type date}, {"VALUE_DATE_UNTIL", type date}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"ACCOUNT_ID", Order.Ascending}, {"DATUM", Order.Ascending}}),
    CURRENCY1 = #"Sorted Rows"[CURRENCY],
    #"Converted to Table" = Table.FromList(CURRENCY1, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Removed Duplicates" = Table.Distinct(#"Converted to Table"),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates",{{"Column1", "CURRENCIES"}})
in
    #"Renamed Columns"
```


## Table: RB_CORIMA_VALUE DATES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_COPS_LIP_CARDINAL_IMPORT = Corima{[Schema="dbo",Item="V_COPS_LIP_CARDINAL_IMPORT"]}[Data],
    #"Filtered Rows1" = Table.SelectRows(dbo_V_COPS_LIP_CARDINAL_IMPORT, each ([PLAN_VARIANT_SHORT_NAME] <> null) and ([AMOUNT_EUR] <> null)),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows1", "Planvariant_Note", each Text.Combine({[NOTE], [PLAN_VARIANT_SHORT_NAME]}, "_"), type text),
    #"Merged Queries1" = Table.NestedJoin(#"Inserted Merged Column", {"Planvariant_Note"}, FC_CARDINAL_ADJ, {"Planvariant_Note"}, "FC_CARDINAL_ADJ", JoinKind.LeftOuter),
    #"Expanded FC_CARDINAL_ADJ1" = Table.ExpandTableColumn(#"Merged Queries1", "FC_CARDINAL_ADJ", {"CLIENT_SHORT_NAME"}, {"CLIENT_SHORT_NAME"}),
    #"Inserted Division" = Table.AddColumn(#"Expanded FC_CARDINAL_ADJ1", "Division", each [AMOUNT_EUR] / 1000, type number),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Division", each ([PLAN_VARIANT_SHORT_NAME] <> null)),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"Division", "Amount_EURk"}}),
    #"Filtered Rows2" = Table.SelectRows(#"Renamed Columns", each [UNIQUE_IDENTIFIER] <> "DH Diagnostics, LLC // CP10077: Multiple Myeloma Dx Market Study / SE-150-202110512.0000")
in
    #"Filtered Rows2"
```


## Table: FC_CARDINAL_ADJ


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_COPS_LIP_IMPORT_DATE_ADJ = Corima{[Schema="dbo",Item="COPS_LIP_IMPORT_DATE_ADJ"]}[Data],
    #"Inserted Merged Column" = Table.AddColumn(dbo_COPS_LIP_IMPORT_DATE_ADJ, "Planvariant_Note", each Text.Combine({[NOTE], [PLAN_VARIANT_SHORT_NAME]}, "_"), type text)
in
    #"Inserted Merged Column"
```


## Table: ZZ_DateLastRefresh


```m
let
    Source = "let#(cr)#(lf)#(cr)#(lf)Source = #table(type table[Date Last Refreshed=datetime], {{DateTime.LocalNow()}})#(cr)#(lf)#(cr)#(lf)in#(cr)#(lf)#(cr)#(lf)Source",
    #"Converted to Table" = let

Source = #table(type table[Date Last Refreshed=datetime], {{DateTime.LocalNow()}})

in

Source
in
    #"Converted to Table"
```


## Table: FC_CATEGORIES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_CATEGORY = Corima{[Schema="dbo",Item="V_DW_LIP_CATEGORY"]}[Data],
    #"Sorted Rows" = Table.Sort(dbo_V_DW_LIP_CATEGORY,{{"SORT_VALUE", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: ZZ_Measure_FC_Legacy


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: FC_IC_MATCHING


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_IC_ABGLEICH = Corima{[Schema="dbo",Item="V_DW_LIP_IC_ABGLEICH"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_IC_ABGLEICH, each ([Gesellschaft_1] <> "Asia") and ([Gesellschaft_2] <> "Asia" and [Gesellschaft_2] <> "NE/USA" and [Gesellschaft_2] <> "RBG")),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows", "ENTITY_COMBI", each Text.Combine({[Gesellschaft_2], [Gesellschaft_1]}, "|"), type text),
    #"Appended Query" = Table.Combine({#"Inserted Merged Column", #"FC_IC_MATCHING (2)"})
in
    #"Appended Query"
```


## Table: RB_User_Roles


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WCM_SECURITY_ADJUSTMENTS = WorkingCapitalMgmt{[Schema="dbo",Item="WCM_SECURITY_ADJUSTMENTS"]}[Data]
in
    dbo_WCM_SECURITY_ADJUSTMENTS
```


## Table: RB_User


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WCM_SECURITY_ADJUSTMENTS = WorkingCapitalMgmt{[Schema="dbo",Item="WCM_SECURITY_ADJUSTMENTS"]}[Data],
    #"Removed Duplicates" = Table.Distinct(dbo_WCM_SECURITY_ADJUSTMENTS, {"EMPLOYEE_ID"})
in
    #"Removed Duplicates"
```


## Table: RB_IC PAY


```m
let
    Source = Table.Combine({RB_MIS_INTERCOMPANY_RECEIVABLES, RB_BYD_INTERCOMPANY_RECEIVABLES}),
    #"Multiplied Column" = Table.TransformColumns(Source, {{"BALANCE_EUR", each _ * -1, type number}}),
    #"Inserted Age" = Table.AddColumn(#"Multiplied Column", "Age", each Date.From(DateTime.LocalNow()) - [POSTING_DATE], type duration),
    #"Added Conditional Column" = Table.AddColumn(#"Inserted Age", "AGE_ID", each if [Age] > #duration(90, 0, 0, 0) then 1 else 0),
    #"Renamed Columns" = Table.RenameColumns(#"Added Conditional Column",{{"Age", "AGE"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each true),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"AGE", type number}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Custom", each if [AGE]  <= 14 then "0-14"
else if [AGE] >=15 and [AGE] <= 30 then "15-30"
else if [AGE] >=31 and [AGE] <= 60 then "31-60"
else if [AGE] >=61 and [AGE] <= 90 then "61-90"
else if [AGE] >=91 and [AGE] <= 180 then "91-180"
else if [AGE] >=181 and [AGE] <270 then "181-270"
else if [AGE] >=271 and [AGE] <=360 then "271-360"
else "361+"),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"Custom", "Age Cluster"}})
in
    #"Renamed Columns1"
```


## Table: RB_IC REC


```m
let
    Source = Table.Combine({RB_BYD_INTERCOMPANY_RECEIVABLES, RB_MIS_INTERCOMPANY_RECEIVABLES}),
    #"Inserted Age" = Table.AddColumn(Source, "Age", each Date.From(DateTime.LocalNow()) - [POSTING_DATE], type duration),
    #"Changed Type" = Table.TransformColumnTypes(#"Inserted Age",{{"Age", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Age", "AGE"}}),
    #"Added Conditional Column" = Table.AddColumn(#"Renamed Columns", "Custom", each if [AGE] > 90 then 1 else 0),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Conditional Column",{{"Custom", "AGE ID"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns1",{{"AGE", type number}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type1", "Custom", each if [AGE]  <= 14 then "0-14"
else if [AGE] >=15 and [AGE] <= 30 then "15-30"
else if [AGE] >=31 and [AGE] <= 60 then "31-60"
else if [AGE] >=61 and [AGE] <= 90 then "61-90"
else if [AGE] >=91 and [AGE] <= 180 then "91-180"
else if [AGE] >=181 and [AGE] <270 then "181-270"
else if [AGE] >=271 and [AGE] <=360 then "271-360"
else "361+"),
    #"Renamed Columns2" = Table.RenameColumns(#"Added Custom",{{"Custom", "Age Clusters"}})
in
    #"Renamed Columns2"
```


## Table: RB_MIS_INTERCOMPANY_RECEIVABLES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    InterCompRcvblPaybl = Source{[Name="InterCompRcvblPaybl"]}[Data],
    dbo_MIS_INTERCOMPANY_RECEIVABLES = InterCompRcvblPaybl{[Schema="dbo",Item="MIS_INTERCOMPANY_RECEIVABLES"]}[Data],
    #"Added Conditional Column" = Table.AddColumn(dbo_MIS_INTERCOMPANY_RECEIVABLES, "Open_Amount_TC", each if [OPEN_AMOUNT_VOUCHER_CUR] = 0 then [OPEN_AMOUNT_COMP_CUR] else [OPEN_AMOUNT_VOUCHER_CUR]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Conditional Column",{{"Open_Amount_TC", type number}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Changed Type1",{{"COMPANY_ID", Int64.Type}, {"PARTNER_COMPANY_ID", Int64.Type}}),
    #"Removed Errors" = Table.RemoveRowsWithErrors(#"Changed Type", {"COMPANY_ID"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Errors",{{"DOCUMENT_DATE", "POSTING_DATE"}, {"OPEN_AMOUNT_EUR", "BALANCE_EUR"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each  ([PARTNER_COMPANY] <> "Argentina") and ([COMPANY] <> "Argentina")),
    #"Renamed Columns1" = Table.RenameColumns(#"Filtered Rows",{{"VOUCHER_CURRENCY", "TC_Currency"}, {"OPEN_AMOUNT_VOUCHER_CUR", "TC_Amount"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns1","invoice","MIS- Invoice",Replacer.ReplaceText,{"DOCUMENT_TYPE"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","credit note","MIS-Credit note",Replacer.ReplaceText,{"DOCUMENT_TYPE"})
in
    #"Replaced Value1"
```


## Table: RB_BYD_INTERCOMPANY_RECEIVABLES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    InterCompRcvblPaybl = Source{[Name="InterCompRcvblPaybl"]}[Data],
    dbo_BYD_INTERCOMPANY_RECEIVABLES = InterCompRcvblPaybl{[Schema="dbo",Item="BYD_INTERCOMPANY_RECEIVABLES"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(dbo_BYD_INTERCOMPANY_RECEIVABLES,{"ACCOUNT_ID", "ACCOUNT"}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Removed Columns", "BALANCE_TC", "BALANCE_TC - Copy"),
    #"Renamed Columns2" = Table.RenameColumns(#"Duplicated Column",{{"BALANCE_TC - Copy", "Open_Amount_TC"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns2",{{"COMPANY_ID", Int64.Type}, {"PARTNER_COMPANY_ID", Int64.Type}, {"GL_ACCOUNT_ID", Int64.Type}, {"JOURNAL_ENTRY_TYPE_ID", Int64.Type}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type",{{"BALANCE_TC", "TC_Amount"}, {"BALANCE_TC_CUR", "TC_Currency"}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Renamed Columns1",{ "JOURNAL_ENTRY", "BALANCE_CC", "BALANCE_CC_CUR", "BALANCE_EXCHANGE_RATE", "CREDIT_CC", "CREDIT_CC_CUR", "CREDIT_LC", "CREDIT_LC_CUR", "CREDIT_TC", "CREDIT_TC_CUR", "DEBIT_CC", "DEBIT_CC_CUR", "DEBIT_LC", "DEBIT_LC_CUR", "DEBIT_TC", "DEBIT_TC_CUR", "EXPORTED_ON", "GL_ACCOUNT_ID", "GL_ACCOUNT", "JOURNAL_ENTRY_TYPE_ID"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns1", each [JOURNAL_ENTRY_TYPE] <> "Foreign Currency Remeasurement"),
    #"Filtered Rows" = Table.SelectRows(#"Filtered Rows1", each true),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"SOURCE_DOCUMENT_ID", "DOCUMENT_ID"}, {"SOURCE_DOCUMENT_EXTERNAL_REFERENCE", "DESCRIPTION"}, {"JOURNAL_ENTRY_TYPE", "DOCUMENT_TYPE"}}),
    #"Filtered Rows2" = Table.SelectRows(#"Renamed Columns", each true)
in
    #"Filtered Rows2"
```


## Table: RB_WIP


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_WORK_IN_PROGRESS = WorkingCapitalMgmt{[Schema="dbo",Item="WORK_IN_PROGRESS"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_WORK_IN_PROGRESS, each ([PROJECT_FOR_CALCULATION] <> "No"))
in
    #"Filtered Rows"
```


## Table: RB_RECEIVABLES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    WorkingCapitalMgmt = Source{[Name="WorkingCapitalMgmt"]}[Data],
    dbo_RECEIVABLES = WorkingCapitalMgmt{[Schema="dbo",Item="RECEIVABLES"]}[Data]
in
    dbo_RECEIVABLES
```


## Table: RB_CORIMA_CUSTOMER_LIST


```m
let
    Source = Table.Combine({RB_WIP, #"RB_CORIMA_VALUE DATES"}),
    #"Filtered Rows" = Table.SelectRows(Source, each ([EMPLOYEE_RESPONSIBLE_ID] <> null)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"EMPLOYEE_RESPONSIBLE_ID", "EMPLOYEE_RESPONSIBLE", "PROJECT_ID", "PROJECT", "PROJECT_STATUS", "AGE_CLUSTER", "AGE_OF_WIP", "LAST_INVOICE_DATE", "PROJECT_START", "INVOICING_SUGGESTED", "OPEN_WIP", "PAYMENT_PROPOSAL", "BUDGET_FEE", "BUDGET_IE", "INVOICED_FEE", "INVOICED_IE", "PROJECT_COMPLETION_FEE", "PROJECT_COMPLETION", "COST_ESTIMATE_FEE", "COST_ESTIMATE_IE", "INCURRED_COSTS_FEE", "INCURRED_COSTS_IE", "DELTA_INVOICING", "LOCAL_CURRENCY", "OPEN_WIP_LC", "PAYMENT_PROPOSAL_LC", "BUDGET_FEE_LC", "BUDGET_IE_LC", "INVOICED_FEE_LC", "INVOICED_IE_LC", "COST_ESTIMATE_FEE_LC", "COST_ESTIMATE_IE_LC", "INCURRED_COSTS_FEE_LC", "INCURRED_COSTS_IE_LC", "DELTA_INVOICING_LC", "UPCOMING_INVOICE_DATE", "SALES_ORDER_ID", "FEES_TO_BE_INVOICED_EUR", "UPCOMING_INVOICE_CURRENCY", "FEES_TO_BE_INVOICED_LC", "SOURCE", "TO_BE_INVOICED_IN", "TO_BE_INVOICED_IN_CLUSTER", "INVOICING_SCHEDULE_EXISTS", "PROJECT_FOR_CALCULATION", "INVOICE_SCHEDULE_MISSING_AMOUNT", "INVOICE_SCHEDULE_MISSING_AMOUNT_LC", "INVOICING_SCHEDULE_AMOUNT_TOTAL", "INVOICING_SCHEDULE_AMOUNT_TOTAL_LC", "PROJECT_BUDGET_FULLY_SCHEDULED", "OVERDUE_WIP", "OVERDUE_WIP_LC", "UPCOMING_WIP", "UPCOMING_WIP_LC", "PROJECT_COMPANY_ID", "PROJECT_COMPANY", "EMPLOYEE_RESPONSIBLE_STATUS", "FUNCTIONAL_UNIT_RESPONSIBLE_ID", "FUNCTIONAL_UNIT_RESPONSIBLE", "EMPLOYEE_RESPONSIBLE_ID_OLD", "EMPLOYEE_RESPONSIBLE_OLD", "CUSTOMER_INVOICE_ID", "AMOUNT_EUR", "AMOUNT_LC", "UNIQUE_IDENTIFIER", "IMPORT_DATE", "PLAN_VARIANT_SHORT_NAME", "NOTE", "VALUE_DATE", "Planvariant_Note", "CLIENT_SHORT_NAME", "Amount_EURk"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns", {"CUSTOMER_ID"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Duplicates", each true)
in
    #"Filtered Rows1"
```


## Table: FC_PLANS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_PLAN = Corima{[Schema="dbo",Item="V_DW_LIP_PLAN"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_PLAN, each ([PLAN_START_PERIODE] = "2022"))
in
    #"Filtered Rows"
```


## Table: MD_PARTNER


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_MDM_PARTNER = Corima{[Schema="dbo",Item="V_DW_MDM_PARTNER"]}[Data]
in
    dbo_V_DW_MDM_PARTNER
```


## Table: FC_ACTUALS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_DATA_DETAIL = Corima{[Schema="dbo",Item="V_DW_LIP_DATA_DETAIL"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_DATA_DETAIL, each ([CATEGORY_SHORT_NAME] <> "Balance import" and [CATEGORY_SHORT_NAME] <> "CP_Last Balance" and [CATEGORY_SHORT_NAME] <> "Statement cashflows")),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows",{{"PERIOD_NR", type text}, {"COUNTERPARTY_ID", type text}, {"BRANCH_ORIGIN_ID", type text}})
in
    #"Changed Type"
```


## Table: FC_CATEGORIES_CHARTS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_CATEGORY = Corima{[Schema="dbo",Item="V_DW_LIP_CATEGORY"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_CATEGORY, each ([DESCRIPTION_EN] <> null and [DESCRIPTION_EN] <> "")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"EDIT_MODE", "ALLOW_EDIT_INIT_PERIOD", "ALLOWED_VALUES", "ALLOWED_PARTNER", "IS_PARTNER_REQUIRED", "FIXED_PARTNER_ID", "FIXED_PARTNER_SHORT_NAME", "MULTI_CURRENCY", "LINE_TYPE", "VALUE_DATE_CREATION_RULE", "HIDE_ZERO_VALUES", "DISPLAY_INIT_PERIOD", "DISPLAY_SUM_PREV_YEAR", "ALLOW_IMPORT_FROM_FILE", "FONT_STYLE_ID", "PERCENTAGE_INPUT", "FINANCIAL_CONTROLLER_ONLY", "STATUS", "PLANNED_FORMULA", "ACTUAL_FORMULA", "ACTIVE_SINCE", "ACTIVE_TILL", "REC_ID", "MASTERPLAN_ID", "MASTERPLAN_SHORT_NAME"}),
    #"Sorted Rows" = Table.Sort(#"Removed Columns",{{"SORT_VALUE", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: ACTUAL_FX_RATES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_DW_CIB_BALANCES = Corima{[Schema="dbo",Item="DW_CIB_BALANCES"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_DW_CIB_BALANCES, each [DATUM] > #datetime(2018, 12, 31, 0, 0, 0)),
    #"Inserted Year" = Table.AddColumn(#"Filtered Rows", "Year", each Date.Year([DATUM]), Int64.Type),
    #"Inserted Month" = Table.AddColumn(#"Inserted Year", "Month", each Date.Month([DATUM]), Int64.Type),
    #"Inserted Week of Year" = Table.AddColumn(#"Inserted Month", "Week of Year", each Date.WeekOfYear([DATUM]), Int64.Type),
    #"Inserted Day of Week" = Table.AddColumn(#"Inserted Week of Year", "Day of Week", each Date.DayOfWeek([DATUM]), Int64.Type),
    #"Changed Type" = Table.TransformColumnTypes(#"Inserted Day of Week",{{"DATUM", type date}, {"VALUE_DATE_UNTIL", type date}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"ACCOUNT_ID", Order.Ascending}, {"DATUM", Order.Ascending}}),
    #"Removed Columns" = Table.RemoveColumns(#"Sorted Rows",{"ACCOUNT_ID", "SHORT_NAME", "VALUE_DATE_UNTIL", "PLANNED_SUM", "RECONCILIATED_SUM", "TOTAL_SUM", "TOTAL_SUM_EUR", "LEGAL_ENTITY_ID", "COUNTRY_ISO3", "ZONE", "Year", "Month", "Week of Year", "Day of Week"}),
    #"Inserted Merged Column" = Table.AddColumn(#"Removed Columns", "Unique_ID", each Text.Combine({[CURRENCY], Text.From([DATUM], "de-DE"), Text.From([RATES_VALUE], "de-DE")}, ""), type text),
    #"Removed Duplicates" = Table.Distinct(#"Inserted Merged Column", {"Unique_ID"}),
    #"Sorted Rows1" = Table.Sort(#"Removed Duplicates",{{"DATUM", Order.Ascending}}),
    #"Inserted Merged Column1" = Table.AddColumn(#"Sorted Rows1", "Merged", each Text.Combine({[CURRENCY], Text.From([DATUM], "de-DE")}, "_"), type text),
    #"Renamed Columns" = Table.RenameColumns(#"Inserted Merged Column1",{{"Merged", "Remove_Duplicates"}}),
    #"Removed Duplicates1" = Table.Distinct(#"Renamed Columns", {"Remove_Duplicates"})
in
    #"Removed Duplicates1"
```


## Table: FC_IC_MATCHING_FILTER


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_IC_ABGLEICH = Corima{[Schema="dbo",Item="V_DW_LIP_IC_ABGLEICH"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_IC_ABGLEICH, each ([Gesellschaft_1] <> "Asia") and ([Gesellschaft_2] <> "Asia" and [Gesellschaft_2] <> "NE/USA" and [Gesellschaft_2] <> "RBG")),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows", "Entity_IDs", each Text.Combine({[Gesellschaft_2], [Gesellschaft_1]}, "|"), type text),
    #"Inserted Merged Column1" = Table.AddColumn(#"Inserted Merged Column", "Entity_IDs_2", each Text.Combine({[Gesellschaft_1], [Gesellschaft_2]}, "|"), type text),
    #"Removed Columns" = Table.RemoveColumns(#"Inserted Merged Column1",{"PLANVARIANTE", "PLANVARIANTEN_ID", "IC_ID", "VALUTA_DATUM", "IC_STATUS_ID", "Gesellschaft_1", "Gesellschaft_2", "IC_STATUS_GESELLSCHAFT_1", "Status_Gesellschaft_1", "IC_STATUS_GESELLSCHAFT_2", "Status_Gesellschaft_2", "Short_Kategorie_Gesellschaft_1", "Kategorie_Gesellschaft_1_DE", "Kategorie_Gesellschaft_1_EN", "Short_Kategorie_Gesellschaft_2", "Kategorie_Gesellschaft_2_DE", "Kategorie_Gesellschaft_2_EN", "AMOUNT", "WAEHRUNG", "MASTERPLAN_ID", "Entity_IDs"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Entity_IDs_2", "ENTITY_COMBI"}}),
    #"Appended Query" = Table.Combine({#"Renamed Columns", FC_IC_MATCHING}),
    #"Removed Columns1" = Table.RemoveColumns(#"Appended Query",{"PLANVARIANTE", "PLANVARIANTEN_ID", "IC_ID", "VALUTA_DATUM", "IC_STATUS_ID", "Gesellschaft_1", "Gesellschaft_2", "IC_STATUS_GESELLSCHAFT_1", "Status_Gesellschaft_1", "IC_STATUS_GESELLSCHAFT_2", "Status_Gesellschaft_2", "Short_Kategorie_Gesellschaft_1", "Kategorie_Gesellschaft_1_DE", "Kategorie_Gesellschaft_1_EN", "Short_Kategorie_Gesellschaft_2", "Kategorie_Gesellschaft_2_DE", "Kategorie_Gesellschaft_2_EN", "AMOUNT", "WAEHRUNG", "MASTERPLAN_ID"}),
    #"Inserted Text Before Delimiter" = Table.AddColumn(#"Removed Columns1", "Text Before Delimiter", each Text.BeforeDelimiter([ENTITY_COMBI], "|"), type text),
    #"Removed Duplicates" = Table.Distinct(#"Inserted Text Before Delimiter", {"ENTITY_COMBI"})
in
    #"Removed Duplicates"
```


## Table: FC_IC_MATCHING (2)


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_IC_ABGLEICH = Corima{[Schema="dbo",Item="V_DW_LIP_IC_ABGLEICH"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_IC_ABGLEICH, each ([Gesellschaft_1] <> "Asia") and ([Gesellschaft_2] <> "Asia" and [Gesellschaft_2] <> "NE/USA" and [Gesellschaft_2] <> "RBG")),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows", "ENTITY_COMBI", each Text.Combine({[Gesellschaft_1], [Gesellschaft_2]}, "|"), type text)
in
    #"Inserted Merged Column"
```


## Table: 1_Measure_Actuals


```m
let
    Source = ""
in
    Source
```


## Table: FC_RESPONSE_A


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_PTR_PLANA = Corima{[Schema="dbo",Item="V_DW_LIP_PTR_PLANA"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_PTR_PLANA, each ([PERIOD_NR] <> 100))
in
    #"Filtered Rows"
```


## Table: FC_RESPONSE_FC


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_PTR_PLANP = Corima{[Schema="dbo",Item="V_DW_LIP_PTR_PLANP"]}[Data]
in
    dbo_V_DW_LIP_PTR_PLANP
```


## Table: ZZ_RollingCalendar_From_FC_Plans


```m
let
    Source = FC_PLANS,
    #"Filtered Rows" = Table.SelectRows(Source, each ([PLAN_STATUS] = 1)),
    Source_date = Table.RemoveColumns(#"Filtered Rows",{"PLAN_ID", "MASTERPLAN_ID", "PLAN_SHORT_NAME", "PLAN_STATUS", "PLAN_START_PERIODE", "ACTUAL_PROJECTED", "ACTUAL_PERIOD_COUNT", "ACTUAL_MAX_PERIOD", "ACTUAL_DISPLAY_PREV_PERIOD_COUNT", "ACTUAL_ACTIVE_PERIOD_COUNT", "ACTUAL_ACTIVE_PERIOD", "PROJECTED_PERIOD_COUNT", "PROJECTED_SHOW_YEAR_SUM", "PROJECTED_SUM_COLUMNS1", "PROJECTED_SUM_COLUMNS2", "MASTERPLAN_SHORT_NAME", "MASTERPLAN_PERIOD_TYPE", "MASTERPLAN_STATUS"}),
    #"Last day of FC" = Table.AddColumn(Source_date, "Custom.1", each List.Dates([PLAN_START], 105, #duration(1, 0, 0, 0))),
    #"Expanded Custom.2" = Table.ExpandListColumn(#"Last day of FC", "Custom.1"),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Custom.2",{{"Custom.1", "Plan_Date"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Plan_Date", type date}}),
    #"Inserted Month Name" = Table.AddColumn(#"Changed Type", "Month Name", each Date.MonthName([Plan_Date]), type text),
    #"Extracted First Characters" = Table.TransformColumns(#"Inserted Month Name", {{"Month Name", each Text.Start(_, 3), type text}}),
    #"Inserted Year" = Table.AddColumn(#"Extracted First Characters", "Year", each Date.Year([Plan_Date]), Int64.Type),
    #"Extracted Last Characters" = Table.TransformColumns(#"Inserted Year", {{"Year", each Text.End(Text.From(_, "de-DE"), 2), type text}}),
    #"Merged Columns" = Table.CombineColumns(#"Extracted Last Characters",{"Year", "Month Name"},Combiner.CombineTextByDelimiter("-", QuoteStyle.None),"Merged"),
    #"Inserted Year1" = Table.AddColumn(#"Merged Columns", "Year", each Date.Year([Plan_Date]), Int64.Type),
    #"Multiplied Column" = Table.TransformColumns(#"Inserted Year1", {{"Year", each _ * 100, type number}}),
    #"Inserted Month" = Table.AddColumn(#"Multiplied Column", "Month", each Date.Month([Plan_Date]), Int64.Type),
    #"Inserted Addition" = Table.AddColumn(#"Inserted Month", "Addition", each [Month] + [Year], type number),
    #"Renamed Columns1" = Table.RenameColumns(#"Inserted Addition",{{"Addition", "Date_Sort"}}),
    #"Inserted Week of Year" = Table.AddColumn(#"Renamed Columns1", "Week of Year", each Date.WeekOfYear([Plan_Date]), Int64.Type),
    #"Inserted Year2" = Table.AddColumn(#"Inserted Week of Year", "Year.1", each Date.Year([Plan_Date]), Int64.Type),
    #"Renamed Columns2" = Table.RenameColumns(#"Inserted Year2",{{"Year", "Year_adj"}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Renamed Columns2",{"PLAN_START", "Plan_Date", "Merged", "Month", "Week of Year", "Date_Sort", "Year_adj", "Year.1"}),
    #"Extracted Last Characters1" = Table.TransformColumns(#"Reordered Columns", {{"Year.1", each Text.End(Text.From(_, "de-DE"), 2), type text}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Extracted Last Characters1", "Merged.1", each Text.Combine({[Year.1], Text.From([Week of Year], "de-DE")}, "-"), type text),
    #"Renamed Columns3" = Table.RenameColumns(#"Inserted Merged Column",{{"Merged.1", "YW-CW"}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Renamed Columns3", "Week of Year", "Week of Year - Copy"),
    Custom1 = Table.AddColumn(#"Renamed Columns3", "Subtraction", each [Week of Year] - 1, type number),
    #"Renamed Columns4" = Table.RenameColumns(Custom1,{{"Subtraction", "Week_of_Year_Interim"}}),
    #"Added Conditional Column" = Table.AddColumn(#"Renamed Columns4", "CW", each if [Week_of_Year_Interim] = 0 then 52 else [Week_of_Year_Interim]),
    #"Removed Columns" = Table.RemoveColumns(#"Added Conditional Column",{"YW-CW"}),
    #"Inserted Merged Column1" = Table.AddColumn(#"Removed Columns", "Y-CW", each Text.Combine({[Year.1], Text.From([CW], "de-DE")}, "-"), type text),
    #"Inserted Last Characters" = Table.AddColumn(#"Inserted Merged Column1", "Last Characters", each Text.End(Text.From([Plan_Date], "de-DE"), 4), type text),
    #"Merged Columns1" = Table.CombineColumns(Table.TransformColumnTypes(#"Inserted Last Characters", {{"Week_of_Year_Interim", type text}}, "de-DE"),{"Last Characters", "Week_of_Year_Interim"},Combiner.CombineTextByDelimiter("/", QuoteStyle.None),"Merged.1"),
    #"Renamed Columns5" = Table.RenameColumns(#"Merged Columns1",{{"Merged.1", "Y-CW_long"}, {"Year.1", "Year_short"}, {"Y-CW", "Y-CW_short"}}),
    #"Sorted Rows" = Table.Sort(#"Renamed Columns5",{{"Plan_Date", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: ZZ_RollingCalendar_From_FC_Plans- For rolling CW


```m
let
    Source = ZZ_RollingCalendar_From_FC_Plans,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"CW", "PLAN_START", "Plan_Date", "Y-CW_long"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Other Columns",{"PLAN_START", "Plan_Date", "Y-CW_long", "CW"}),
    #"Removed Duplicates" = Table.Distinct(#"Reordered Columns", {"CW"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Duplicates",{{"CW", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"CW", "Calendar Week"}}),
    #"Added Index" = Table.AddIndexColumn(#"Renamed Columns", "Index", 1, 1, Int64.Type),
    #"Duplicated Column" = Table.DuplicateColumn(#"Added Index", "Calendar Week", "Calendar Week - Copy"),
    #"Renamed Columns1" = Table.RenameColumns(#"Duplicated Column",{{"Calendar Week - Copy", "Calendar Week -type Number"}}),
    #"Inserted Month" = Table.AddColumn(#"Renamed Columns1", "Month", each Date.Month([Plan_Date]), Int64.Type),
    #"Renamed Columns2" = Table.RenameColumns(#"Inserted Month",{{"Month", "Month- week start"}}),
    #"Inserted Day" = Table.AddColumn(#"Renamed Columns2", "Day", each Date.Day([Plan_Date]), Int64.Type),
    #"Renamed Columns3" = Table.RenameColumns(#"Inserted Day",{{"Day", "Day- week start"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns3", "Month- week start(with leading zero)", each Text.PadStart(Text.From( [#"Month- week start"]), 2,"0")),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Day- weekstart( leading zero)", each Text.PadStart(Text.From( [#"Day- week start"]), 2,"0")),
    #"Inserted Merged Column" = Table.AddColumn(#"Added Custom1", "Date- week start", each Text.Combine({[#"Day- weekstart( leading zero)"], [#"Month- week start(with leading zero)"]}, "."), type text),
    #"Added Custom2" = Table.AddColumn(#"Inserted Merged Column", "Plan_EndDate", each Date.AddDays([Plan_Date],6)),
    #"Inserted Month1" = Table.AddColumn(#"Added Custom2", "Month", each Date.Month([Plan_EndDate]), Int64.Type),
    #"Inserted Day1" = Table.AddColumn(#"Inserted Month1", "Day", each Date.Day([Plan_EndDate])),
    #"Renamed Columns4" = Table.RenameColumns(#"Inserted Day1",{{"Month", "Month- week end"}, {"Day", "Day- week end"}}),
    #"Added Custom3" = Table.AddColumn(#"Renamed Columns4", "Month- week end( leading zero) ", each Text.PadStart(Text.From( [#"Month- week end"]), 2,"0")),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "Day- week end(leading zero)", each Text.PadStart(Text.From( [#"Day- week end"]), 2,"0")),
    #"Inserted Merged Column1" = Table.AddColumn(#"Added Custom4", "Date- week end", each Text.Combine({[#"Day- week end(leading zero)"], [#"Month- week end( leading zero) "]}, "."), type text),
    #"Inserted Merged Column2" = Table.AddColumn(#"Inserted Merged Column1", "Merged week", each Text.Combine({[#"Date- week start"], [#"Date- week end"]}, "-"), type text),
    #"Duplicated Column1" = Table.DuplicateColumn(#"Inserted Merged Column2", "Calendar Week", "Calendar Week - Copy"),
    #"Renamed Columns5" = Table.RenameColumns(#"Duplicated Column1",{{"Calendar Week - Copy", "Calendar Week - For Marge week"}}),
    #"Added Custom5" = Table.AddColumn(#"Renamed Columns5", "merged week 2", each "("&[Merged week]&")"),
    #"Added Custom6" = Table.AddColumn(#"Added Custom5", "Calendar Week - For Marge week(leading zero)", each Text.PadStart(Text.From( [#"Calendar Week - For Marge week"]), 2,"0")),
    #"Inserted Merged Column3" = Table.AddColumn(#"Added Custom6", "Calendar week(Period)", each Text.Combine({[#"Calendar Week - For Marge week(leading zero)"], [merged week 2]}, ""), type text)
in
    #"Inserted Merged Column3"
```


## Table: MD_Netting_Countries


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_MDM_PARTNER = Corima{[Schema="dbo",Item="V_DW_MDM_PARTNER"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_MDM_PARTNER, each ([REGISTRED_OFFICE] = "Netting"))
in
    #"Filtered Rows"
```


## Table: Age clusters


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("PY7LDcAwCEN34doixfmQMEuU/ddoMFIv8GxLmL2lKLq8ou5+Fxly3i0Y2kqocQep0m9QC9VwRxJ9g3ooC5/U6TsUK6RHkDiyYUHrZMeKLNmY1QltvH4pOsgzPzA8v+X5+JJzPg==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Age Cluster" = _t, #"Min Bracket" = _t, #"Max Bracket" = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Age Cluster", type text}, {"Min Bracket", Int64.Type}, {"Max Bracket", Int64.Type}, {"Column1", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1", "Sorting"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","361+","360+",Replacer.ReplaceText,{"Age Cluster"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",9999,50000,Replacer.ReplaceValue,{"Max Bracket"}),
    #"Sorted Rows" = Table.Sort(#"Replaced Value1",{{"Sorting", Order.Ascending}}),
    #"Replaced Value2" = Table.ReplaceValue(#"Sorted Rows","360+","361+",Replacer.ReplaceText,{"Age Cluster"})
in
    #"Replaced Value2"
```


## Table: FC_IC_MATCHING_NEW


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_LIP_IC_ABGLEICH = Corima{[Schema="dbo",Item="V_DW_LIP_IC_ABGLEICH"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_LIP_IC_ABGLEICH, each ([Gesellschaft_1] <> "Asia") and ([Gesellschaft_2] <> "Asia" and [Gesellschaft_2] <> "NE/USA" and [Gesellschaft_2] <> "RBG")),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows", "ENTITY_COMBI", each Text.Combine({[Gesellschaft_2], [Gesellschaft_1]}, "|"), type text),
    #"Appended Query" = Table.Combine({#"Inserted Merged Column", #"FC_IC_MATCHING (2)"})
in
    #"Appended Query"
```


## Table: ZZ_RollingCalendar for FC over FC with Last Actual week


```m
let
    Source = FC_PLANS,
    #"Filtered Rows" = Table.SelectRows(Source, each ([PLAN_STATUS] = 1)),
    Source_date = Table.RemoveColumns(#"Filtered Rows",{"PLAN_ID", "MASTERPLAN_ID", "PLAN_SHORT_NAME", "PLAN_STATUS", "PLAN_START_PERIODE", "ACTUAL_PROJECTED", "ACTUAL_PERIOD_COUNT", "ACTUAL_MAX_PERIOD", "ACTUAL_DISPLAY_PREV_PERIOD_COUNT", "ACTUAL_ACTIVE_PERIOD_COUNT", "ACTUAL_ACTIVE_PERIOD", "PROJECTED_PERIOD_COUNT", "PROJECTED_SHOW_YEAR_SUM", "PROJECTED_SUM_COLUMNS1", "PROJECTED_SUM_COLUMNS2", "MASTERPLAN_SHORT_NAME", "MASTERPLAN_PERIOD_TYPE", "MASTERPLAN_STATUS"}),
    #"Added Custom" = Table.AddColumn(Source_date, "LastActualWeekStartDate", each Date.AddDays([PLAN_START], -7)),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Custom.1", each List.Dates([LastActualWeekStartDate], 105, #duration(1, 0, 0, 0))),
    #"Expanded Custom.2" = Table.ExpandListColumn(#"Added Custom1", "Custom.1"),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Custom.2",{{"Custom.1", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Custom.1", "Days"}}),
    #"Inserted Week of Year" = Table.AddColumn(#"Renamed Columns", "Week of Year", each Date.WeekOfYear([Days]), Int64.Type),
    #"Removed Duplicates" = Table.Distinct(#"Inserted Week of Year", {"Week of Year"}),
    #"Inserted Year" = Table.AddColumn(#"Removed Duplicates", "Year", each Date.Year([Days]), Int64.Type),
    #"Inserted Merged Column" = Table.AddColumn(#"Inserted Year", "Y_CW_long", each Text.Combine({Text.From([Year], "de-DE"), Text.From([Week of Year], "de-DE")}, "/"), type text),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"LastActualWeekStartDate", type date}})
in
    #"Changed Type1"
```


## Table: Query1


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    InterCompRcvblPaybl = Source{[Name="InterCompRcvblPaybl"]}[Data],
    dbo_BYD_INTERCOMPANY_RECEIVABLES = InterCompRcvblPaybl{[Schema="dbo",Item="BYD_INTERCOMPANY_RECEIVABLES"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(dbo_BYD_INTERCOMPANY_RECEIVABLES,{"ACCOUNT_ID", "ACCOUNT"}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Removed Columns", "BALANCE_TC", "BALANCE_TC - Copy"),
    #"Renamed Columns2" = Table.RenameColumns(#"Duplicated Column",{{"BALANCE_TC - Copy", "Open_Amount_TC"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns2",{{"COMPANY_ID", Int64.Type}, {"PARTNER_COMPANY_ID", Int64.Type}, {"GL_ACCOUNT_ID", Int64.Type}, {"JOURNAL_ENTRY_TYPE_ID", Int64.Type}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type",{{"BALANCE_TC", "TC_Amount"}, {"BALANCE_TC_CUR", "TC_Currency"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns1", each true),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"SOURCE_DOCUMENT_ID", "DOCUMENT_ID"}, {"SOURCE_DOCUMENT_EXTERNAL_REFERENCE", "DESCRIPTION"}, {"JOURNAL_ENTRY_TYPE", "DOCUMENT_TYPE"}}),
    #"Filtered Rows2" = Table.SelectRows(#"Renamed Columns", each true)
in
    #"Filtered Rows2"
```

