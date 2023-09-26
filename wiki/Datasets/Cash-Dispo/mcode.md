



# M Code

|Dataset|[Cash Dispo](./../Cash-Dispo.md)|
| :--- | :--- |
|Workspace|[FC_Cash_Management](../../Workspaces/FC_Cash_Management.md)|

## Table: RB_COMPANIES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    ByD_ODP = Source{[Name="ByD_ODP"]}[Data],
    dbo_BYD_RB_COMPANIES = ByD_ODP{[Schema="dbo",Item="BYD_RB_COMPANIES"]}[Data]
in
    dbo_BYD_RB_COMPANIES
```


## Table: ACTUAL_BALANCES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_DW_CIB_BALANCES = Corima{[Schema="dbo",Item="DW_CIB_BALANCES"]}[Data],
    #"Inserted Merged Column" = Table.AddColumn(dbo_DW_CIB_BALANCES, "Unique_Name_Datum", each Text.Combine({[SHORT_NAME], Text.From([DATUM], "de-DE")}, "_"), type text),
    #"Added Custom" = Table.AddColumn(#"Inserted Merged Column", "Custom", each Date.AddDays([DATUM],(-1))),
    #"Inserted Merged Column1" = Table.AddColumn(#"Added Custom", "Unique_Name&priviousDay", each Text.Combine({[SHORT_NAME], Text.From([Custom], "de-DE")}, "_"), type text),
    #"Reordered Columns" = Table.ReorderColumns(#"Inserted Merged Column1",{"ACCOUNT_ID", "SHORT_NAME", "CURRENCY", "DATUM", "VALUE_DATE_UNTIL", "PLANNED_SUM", "RECONCILIATED_SUM", "TOTAL_SUM", "RATES_VALUE", "TOTAL_SUM_EUR", "LEGAL_ENTITY_ID", "COUNTRY_ISO3", "ZONE", "Custom", "Unique_Name_Datum", "Unique_Name&priviousDay"}),
    #"UCB RBH EUR null" = Table.ReplaceValue(#"Reordered Columns",null,"12000000",Replacer.ReplaceValue,{"LEGAL_ENTITY_ID"})
in
    #"UCB RBH EUR null"
```


## Table: MD_BANK ACCOUNTS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_MDM_ACCOUNT_IF_SET = Corima{[Schema="dbo",Item="V_DW_MDM_ACCOUNT_IF_SET"]}[Data],
    #"Added Custom" = Table.AddColumn(dbo_V_DW_MDM_ACCOUNT_IF_SET, "Euro and Non Euro", each if [CURRENCY] = "EUR" then "EUR" else "Non EUR"),
    #"Inserted First Characters" = Table.AddColumn(#"Added Custom", "First Characters", each Text.Start([SHORT_NAME], 3), type text),
    #"Added Custom1" = Table.AddColumn(#"Inserted First Characters", "CP account Status", each if [First Characters] = "CP_" then "CP account" else "Non CP Account"),
    #"Added Conditional Column" = Table.AddColumn(#"Added Custom1", "CashPooling RB AC", each if [SHORT_NAME] = "DB RB EUR" then 1 else if [SHORT_NAME] = "COBA RB EUR" then 1 else if [SHORT_NAME] = "HSBC RB EUR" then 1 else if [SHORT_NAME] = "LBBW RB EUR" then 1 else if [SHORT_NAME] = "UCB RB EUR" then 1 else 0),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "CashPooing RBH AC", each if [SHORT_NAME] = "COBA RBH EUR" then 1 else if [SHORT_NAME] = "DB RBH EUR" then 1 else if [SHORT_NAME] = "HSBC RBH EUR" then 1 else if [SHORT_NAME] = "UCB RBH EUR" then 1 else if [SHORT_NAME] = "LBBW RBH EUR" then 1 else 0)
in
    #"Added Conditional Column1"
```


## Table: MD_PAYMENT_REASONS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_COPS_CM_PAYMENT_REASON = Corima{[Schema="dbo",Item="V_COPS_CM_PAYMENT_REASON"]}[Data]
in
    dbo_V_COPS_CM_PAYMENT_REASON
```


## Table: MD_PAYMENT_REASONS_HIERARCHY


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_COPS_CM_PAYMENT_REASON = Corima{[Schema="dbo",Item="V_COPS_CM_PAYMENT_REASON"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_COPS_CM_PAYMENT_REASON, each [STATUS] = 1),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows", "SHORT_NAME + DESCRIPTION", each Text.Combine({[SHORT_NAME], [DESCRIPTION]}, ","), type text),
    #"SHORT_NAME + DESCRIPTION" = #"Inserted Merged Column"[#"SHORT_NAME + DESCRIPTION"],
    #"Converted to Table" = Table.FromList(#"SHORT_NAME + DESCRIPTION", Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Converted to Table", "Column1", Splitter.SplitTextByDelimiter(",", QuoteStyle.Csv), {"Column1.1", "Column1.2", "Column1.3", "Column1.4", "Column1.5", "Column1.6", "Column1.7"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Column1.1", type text}, {"Column1.2", type text}, {"Column1.3", type text}, {"Column1.4", type text}, {"Column1.5", type text}, {"Column1.6", type text}, {"Column1.7", type text}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"Column1.1", Order.Ascending}}),
    #"Renamed Columns" = Table.RenameColumns(#"Sorted Rows",{{"Column1.1", "PAYMENT_REASON"}, {"Column1.2", "AGG LEVEL 1"}, {"Column1.3", "AGG LEVEL 2"}, {"Column1.4", "AGG LEVEL 3"}, {"Column1.5", "AGG LEVEL 4"}, {"Column1.6", "AGG LEVEL 5"}, {"Column1.7", "AGG_DIPSO"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "AGG LEVEL NO Blank", each if[AGG LEVEL 3] = "" then [AGG LEVEL 2] else [AGG LEVEL 3]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "AGG LEVEL 4 NO Blank", each if[AGG LEVEL 4] = "" then [AGG LEVEL NO Blank] else [AGG LEVEL 4]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "AGG LEVEL 5 No Blank", each if[AGG LEVEL 5] = "" then [AGG LEVEL 4 NO Blank] else [AGG LEVEL 5]),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "Agg LEVEL 3 No Blank", each if[AGG LEVEL 3] = "" then [AGG LEVEL 2] else [AGG LEVEL 3]),
    #"Reordered Columns" = Table.ReorderColumns(#"Added Custom3",{"PAYMENT_REASON", "AGG LEVEL 1", "AGG LEVEL 2", "AGG LEVEL 3", "AGG LEVEL 4", "AGG LEVEL 5", "AGG_DIPSO", "AGG LEVEL NO Blank", "Agg LEVEL 3 No Blank", "AGG LEVEL 4 NO Blank", "AGG LEVEL 5 No Blank"}),
    #"Removed Columns" = Table.RemoveColumns(#"Reordered Columns",{"AGG LEVEL NO Blank"})
in
    #"Removed Columns"
```


## Table: ACTUAl_CASH_FLOWS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_CM_CFL = Corima{[Schema="dbo",Item="V_DW_CM_CFL"]}[Data],
    #"Inserted Text Before Delimiter" = Table.AddColumn(dbo_V_DW_CM_CFL, "Text Before Delimiter", each Text.BeforeDelimiter([PAYMENT_REFERENCE], "//"), type text),
    #"Replaced Null Value PaymentReference" = Table.ReplaceValue(#"Inserted Text Before Delimiter",null,"",Replacer.ReplaceValue,{"PAYMENT_REFERENCE"}),
    #"Replaced Value PaymentReferencePlanned" = Table.ReplaceValue(#"Replaced Null Value PaymentReference",null,"",Replacer.ReplaceValue,{"PAYMENT_REFERENCE_PLANNED"}),
    #"IfPaymentReferencehas//" = Table.AddColumn(#"Replaced Value PaymentReferencePlanned", "IfPaymentReferencehasDelimt", each if not Text.Contains([PAYMENT_REFERENCE], "//") then 0 else 1),
    IfPaymentReferencePlannedNotEmpty = Table.AddColumn(#"IfPaymentReferencehas//", "IfPaymentReferencePlannedNotEmpty1", each if Text.Trim([PAYMENT_REFERENCE_PLANNED]) = "" then 0 
else 1),
    #"Added Custom1" = Table.AddColumn(IfPaymentReferencePlannedNotEmpty, "PaymentReference0&PlannednotEmpty", each if [IfPaymentReferencehasDelimt] = 0 and [IfPaymentReferencePlannedNotEmpty1] = 1 then 1 else 0),
    CommentNew2 = Table.AddColumn(#"Added Custom1", "Comments New2", each if[PAYMENT_REASON]= "D1.1 A-Shares - sale" and [STATUS] = 1 then [PAYMENT_REFERENCE_PLANNED]
else if[PAYMENT_REASON]= "D1.1 A-Shares - sale" and [STATUS] <> 1 then [PAYMENT_REFERENCE]

else if[PAYMENT_REASON]= "D3.4 Guarantee provision" and [STATUS] = 1 then [PAYMENT_REFERENCE_PLANNED]
else if[PAYMENT_REASON]= "D3.4 Guarantee provision" and [STATUS] <> 1 then [PAYMENT_REFERENCE]

else if[IfPaymentReferencehasDelimt]= 1 then [Text Before Delimiter] 
else if [IfPaymentReferencehasDelimt] = 0 and [IfPaymentReferencePlannedNotEmpty1] = 1 then [PAYMENT_REFERENCE_PLANNED]
else [PAYMENT_REFERENCE]),
    #"Renamed Columns" = Table.RenameColumns(CommentNew2,{{"Text Before Delimiter", "INTERIM_COLUMN"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Custom", 
each if [PAYMENT_REASON] = "A1 Receivables - clients" then [INTERIM_COLUMN] 
else if [PAYMENT_REASON] = "A2 IC - incoming payment" then [INTERIM_COLUMN] 
else if [PAYMENT_REASON] = "D3.4 Guarantee provision" then [INTERIM_COLUMN]
else if [PAYMENT_REASON] = "D5.1 Investment into RBH - incoming" then [INTERIM_COLUMN]  
else if [PAYMENT_REASON] = "D1.1 A-Shares - sale" then [INTERIM_COLUMN] 
else [PAYMENT_REFERENCE_PLANNED]),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"Custom", "COMMENT"}}),
    #"Extracted Date" = Table.TransformColumns(#"Renamed Columns1",{{"PLANNING_DATE", DateTime.Date, type date}, {"VALUE_DATE", DateTime.Date, type date}, {"VALUE_DATE_PLANNED", DateTime.Date, type date}, {"RECONCILIATION_DATE", DateTime.Date, type date}, {"STATEMENT_DATE", DateTime.Date, type date}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Extracted Date", "STMNT_PAYMENT_INFORMATION", "STMNT_PAYMENT_INFORMATION - Copy"),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Duplicated Column", "STMNT_PAYMENT_INFORMATION - Copy", Splitter.SplitTextByEachDelimiter({"//"}, QuoteStyle.Csv, true), {"STMNT_PAYMENT_INFORMATION - Copy.1", "STMNT_PAYMENT_INFORMATION - Copy.2"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"STMNT_PAYMENT_INFORMATION - Copy.1", type text}, {"STMNT_PAYMENT_INFORMATION - Copy.2", type text}}),
    #"Remove Test entry in Comment" = Table.SelectRows(#"Changed Type", each ([COMMENT] <> "test" and [COMMENT] <> "Test Kundeneingang" and [COMMENT] <> "TEST LIQUIPLANUNG" and [COMMENT] <> "TEST VAT für LQ Forecast")),
    #"Duplicated Column1" = Table.DuplicateColumn(#"Remove Test entry in Comment", "VALUE_DATE", "VALUE_DATE - Copy"),
    #"Extracted Year" = Table.TransformColumns(#"Duplicated Column1",{{"VALUE_DATE - Copy", Date.Year, Int64.Type}}),
    #"Duplicated Column2" = Table.DuplicateColumn(#"Extracted Year", "VALUE_DATE", "VALUE_DATE - Copy.1"),
    #"Extracted Month" = Table.TransformColumns(#"Duplicated Column2",{{"VALUE_DATE - Copy.1", Date.Month, Int64.Type}}),
    #"Filtered Rows" = Table.SelectRows(#"Extracted Month", each [VALUE_DATE] > #date(2020, 12, 1) or Date.IsInNextNYears([VALUE_DATE], 5)),
    #"Added Conditional Column" = Table.AddColumn(#"Filtered Rows", "STMNT_PAYMENT_INFO&PAYMENT_REFERENCE", each if [STMNT_PAYMENT_INFORMATION] = null then [PAYMENT_REFERENCE] else [STMNT_PAYMENT_INFORMATION])
in
    #"Added Conditional Column"
```


## Table: MD_CURRENCY


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_DW_CIB_BALANCES = Corima{[Schema="dbo",Item="DW_CIB_BALANCES"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_DW_CIB_BALANCES, each [DATUM] > #datetime(2018, 12, 31, 0, 0, 0)),
    #"Inserted Year" = Table.AddColumn(#"Filtered Rows", "Year", each Date.Year([DATUM]),Int64.Type),
    #"Inserted Month" = Table.AddColumn(#"Inserted Year", "Month", each Date.Month([DATUM]), Int64.Type),
    #"Inserted Day of Year" = Table.AddColumn(#"Inserted Month", "Week of Year", each Date.WeekOfYear([DATUM]), Int64.Type),
    #"Insearted Day of Week" = Table.AddColumn(#"Inserted Day of Year", "Day of Week", each Date.DayOfWeek([DATUM]), Int64.Type),
    #"Changed Type" = Table.TransformColumnTypes(#"Insearted Day of Week",{{"VALUE_DATE_UNTIL", type date}, {"DATUM", type date}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"ACCOUNT_ID", Order.Ascending}, {"DATUM", Order.Ascending}}),
    #"Transposed Table" = #"Sorted Rows"[CURRENCY],
    #"Converted to Table" = Table.FromList(#"Transposed Table", Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Removed Duplicates" = Table.Distinct(#"Converted to Table"),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates",{{"Column1", "CURRENCIES"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Custom", each if [CURRENCIES] = "EUR" then "EUR" else "Non EUR"),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"Custom", "EUR_NonEUR"}})
in
    #"Renamed Columns1"
```


## Table: MD_PARTNERS


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_DW_MDM_PARTNER = Corima{[Schema="dbo",Item="V_DW_MDM_PARTNER"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_DW_MDM_PARTNER, each ([PARTNER_NAME] <> "Dummy"))
in
    #"Filtered Rows"
```


## Table: MD_PAYMENT_REASONS_DISPO


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_V_COPS_CM_PAYMENT_REASON = Corima{[Schema="dbo",Item="V_COPS_CM_PAYMENT_REASON"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_V_COPS_CM_PAYMENT_REASON, each ([STATUS] = 1)),
    #"Inserted Merged Column" = Table.AddColumn(#"Filtered Rows", "SHORT_NAME + DESCRIPTION", each Text.Combine({[SHORT_NAME], [DESCRIPTION]}, ","), type text),
    #"SHORT_NAME + DESCRIPTION1" = #"Inserted Merged Column"[#"SHORT_NAME + DESCRIPTION"],
    #"Converted to Table" = Table.FromList(#"SHORT_NAME + DESCRIPTION1", Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Converted to Table", "Column1", Splitter.SplitTextByDelimiter(",", QuoteStyle.Csv), {"Column1.1", "Column1.2", "Column1.3", "Column1.4", "Column1.5", "Column1.6", "Column1.7"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Column1.1", type text}, {"Column1.2", type text}, {"Column1.3", type text}, {"Column1.4", type text}, {"Column1.5", type text}, {"Column1.6", type text}, {"Column1.7", type text}}),
    #"Sorted Rows" = Table.Sort(#"Changed Type",{{"Column1.1", Order.Ascending}}),
    #"Renamed Columns" = Table.RenameColumns(#"Sorted Rows",{{"Column1.1", "PAYMENT_REASON"}, {"Column1.2", "AGG LEVEL 1"}, {"Column1.3", "AGG LEVEL 2"}, {"Column1.4", "AGG LEVEL 3"}, {"Column1.5", "AGG LEVEL 4"}, {"Column1.6", "AGG LEVEL 5"}, {"Column1.7", "AGG_DIPSO"}}),
    AGG_DIPSO1 = #"Renamed Columns"[AGG_DIPSO],
    #"Converted to Table1" = Table.FromList(AGG_DIPSO1, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Renamed Columns1" = Table.RenameColumns(#"Converted to Table1",{{"Column1", "DISPO FILTERS"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns1"),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Duplicates", each ([DISPO FILTERS] <> null)),
    #"Sorted Rows1" = Table.Sort(#"Filtered Rows1",{{"DISPO FILTERS", Order.Ascending}})
in
    #"Sorted Rows1"
```


## Table: ZZ_Measure_FC_Legacy


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: ZZ_RollingCalender_Workdays


```m
let
    Source = #date(2016, 1, 1),
    Custom1 = List.Dates (Source, Number.From(Date.AddDays(DateTime.LocalNow(), 365)) - Number.From(Source), #duration(1,0,0,0)),
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
    #"Inserted Day of Week" = Table.AddColumn(#"Renamed Columns3", "Day of Week", each Date.DayOfWeek([Date]), Int64.Type),
    #"Added Conditional Column" = Table.AddColumn(#"Inserted Day of Week", "If_Work_Day", each if [Day of Week] <= 4 then 1 else null),
    #"Inserted Day Name" = Table.AddColumn(#"Added Conditional Column", "Day Name", each Date.DayOfWeekName([Date]), type text),
    #"Merged Queries1" = Table.NestedJoin(#"Inserted Day Name", {"Date"}, ZZ_ECB_Excel_Holidays, {"Date"}, "Excel_Holidays", JoinKind.LeftOuter),
    #"Expanded ECB_Holiday_Calendar" = Table.ExpandTableColumn(#"Merged Queries1", "ZZ_ECB_Holiday_Calendar", {"Name_OF_Holiday"}, {"ZZ_ECB_Holiday_Calendar.Name_OF_Holiday"}),
    #"Expanded Excel_Holidays" = Table.ExpandTableColumn(#"Merged Queries1", "Excel_Holidays", {"Name_OF_Holiday", "Date", "Day Name"}, {"Excel_Holidays.Name_OF_Holiday", "Excel_Holidays.Date", "Excel_Holidays.Day Name"}),
    #"Removed Columns2" = Table.RemoveColumns(#"Expanded Excel_Holidays",{"Excel_Holidays.Day Name", "Excel_Holidays.Name_OF_Holiday"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns2", each ([If_Work_Day] = 1) and ([Excel_Holidays.Date] = null))
in
    #"Filtered Rows"
```


## Table: ZZ_DateLastRefresh


```m
let


date = DateTime.LocalNow()
in
    date
```


## Table: LQ_Negative_Interest


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Corima_PowerBi_Additional%20Data.xlsx"), null, true),
    Negative_Interest_Sheet = Source{[Item="Negative_Interest",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Negative_Interest_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Bank", type text}, {"Bank ID", Int64.Type}, {"SAP ID", Int64.Type}, {"Gesellschaft", type text}, {"Konto", type text}, {"From", type date}, {"To", type date}, {"Threshold", Int64.Type}})
in
    #"Changed Type"
```


## Table: _LQ_Measure


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})
in
    #"Changed Type"
```


## Table: _Title_Measure


```m
let
    Source = ""
in
    Source
```


## Table: ZZ_RollingCalender


```m
let
    Source = #date(2016, 1, 1),
    Custom1 = List.Dates (Source, Number.From(Date.AddDays(DateTime.LocalNow(), 7300)) - Number.From(Source), #duration(1,0,0,0))

// Calender date for next 7300 days( 20 years)
,
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
    #"Duplicated Column" = Table.DuplicateColumn(#"Renamed Columns3", "Date", "Date - Copy"),
    #"Reordered Columns2" = Table.ReorderColumns(#"Duplicated Column",{"Date", "Date - Copy", "Year", "Month", "Week of Year", "Date_short", "Year_adj", "Date_sort", "Year_CW"}),
    #"Renamed Columns4" = Table.RenameColumns(#"Reordered Columns2",{{"Date - Copy", "Date Hierarchy"}}),
    #"Sorted Rows" = Table.Sort(#"Renamed Columns4",{{"Date", Order.Ascending}}),
    #"Added Index" = Table.AddIndexColumn(#"Sorted Rows", "Index", 1, 1, Int64.Type)
in
    #"Added Index"
```


## Table: Credit_Line_Guarantees


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/20200907_Eventualverbindlichkeiten%20%C3%9Cbersicht%20NEU.xlsm"), null, true),
    #"Guarantee timeline_Sheet" = Source{[Item="Output",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Guarantee timeline_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Bank", type text}, {"Bank_ID", Int64.Type}, {"Gurantee_Type", type text}, {"Entity", type text}, {"Entity_ID", Int64.Type}, {"Amount", type number}, {"Currency", type text}})
in
    #"Changed Type"
```


## Table: Credit_Line_RCF


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Corima_PowerBi_Credit_Lines.xlsx"), null, true),
    RCF_Sheet = Source{[Item="RCF",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(RCF_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"ID", Int64.Type}, {"Entity", Int64.Type}, {"Currency", type text}, {"Amount", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Entity", "Entity_ID"}}),
    #"Filtered entity 0" = Table.SelectRows(#"Renamed Columns", each ([Entity_ID] <> 0))
in
    #"Filtered entity 0"
```


## Table: Credit_Line_Ancillary


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Corima_PowerBi_Credit_Lines.xlsx"), null, true),
    Ancillary_Sheet = Source{[Item="Ancillary",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Ancillary_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"ID", Int64.Type}, {"Entity", Int64.Type}, {"Currency", type text}, {"Amount", Int64.Type}, {"Bank", type text}, {"Bank_ID", Int64.Type}, {"Account_ID", type text}})
in
    #"Changed Type"
```


## Table: Credit_Line_Term Loan


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Corima_PowerBi_Credit_Lines.xlsx"), null, true),
    #"Term Loan_Sheet" = Source{[Item="Term Loan",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Term Loan_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"ID", Int64.Type}, {"Entity", Int64.Type}, {"Currency", type text}, {"Amount", Int64.Type}})
in
    #"Changed Type"
```


## Table: ZZ_ECB_Excel_Holidays


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Holidays.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Holiday", type text}, {"Date", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Holiday", "Name_OF_Holiday"}}),
    #"Inserted Day Name" = Table.AddColumn(#"Renamed Columns", "Day Name", each Date.DayOfWeekName([Date]), type text)
in
    #"Inserted Day Name"
```


## Table: MD_BANKS


```m
let
    Source = MD_PARTNERS,
    #"Filtered Rows" = Table.SelectRows(Source, each ([PARTNER_TYPE] = "External") and ([INTERNET_ADDRESS] <> null)),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"INTERNET_ADDRESS", "BANK_NAME"}})
in
    #"Renamed Columns"
```


## Table: Credit_Line_RoW


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Corima_PowerBi_Additional%20Data_RoWCreditLines.xlsx"), null, true),
    #"RoW Credit Lines_Sheet" = Source{[Item="RoW Credit Lines",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"RoW Credit Lines_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Entity ID", Int64.Type}, {"Amount", Int64.Type}, {"Currency", type text}, {"Bank Account Short Name", type text}}),
    #"Inserted Year" = Table.AddColumn(#"Changed Type", "Year", each Date.Year([Date]), Int64.Type),
    #"Inserted Week of Year" = Table.AddColumn(#"Inserted Year", "Week of Year", each Date.WeekOfYear([Date]), Int64.Type),
    #"Inserted Day of Week" = Table.AddColumn(#"Inserted Week of Year", "Day of Week", each Date.DayOfWeek([Date]), Int64.Type),
    #"Inserted Day Name" = Table.AddColumn(#"Inserted Day of Week", "Day Name", each Date.DayOfWeekName([Date]), type text),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Day Name",{{"Entity ID", type text}})
in
    #"Changed Type1"
```


## Table: ACTUAL_FX_RATES


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_DW_CIB_BALANCES = Corima{[Schema="dbo",Item="DW_CIB_BALANCES"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_DW_CIB_BALANCES, each [DATUM] > #datetime(2016, 09, 30, 0, 0, 0)),
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
    #"Removed Duplicates1" = Table.Distinct(#"Renamed Columns", {"Remove_Duplicates"}),
    #"Sorted Rows2" = Table.Sort(#"Removed Duplicates1",{{"DATUM", Order.Descending}})
in
    #"Sorted Rows2"
```


## Table: Sheet1


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Holidays.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Holiday", type text}, {"Date", type date}})
in
    #"Changed Type"
```


## Table: ACTUAL_CF_Status


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlDQVfDTd1SK1YlWMgSy3VMLchLzSsB8IyDfMSk9tbgkMzcXImQMFAouyS/Ky0wtgoiYAEVci6pSS9MhfFMgPyy/KBFVn64hyKKQ1NyC/KLDS4oUUkqLkjNAhuekZiZnFKWmp+ZA1Rkiq0stUggAOkfXObE4Iy0nvxyqxghiB1y/UmwsAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Changed Type", "Column1", Splitter.SplitTextByEachDelimiter({" "}, QuoteStyle.Csv, false), {"Column1.1", "Column1.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Column1.1", Int64.Type}, {"Column1.2", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"Column1.1", "Status"}, {"Column1.2", "Stauts_Name"}}),
    #"Split Column by Position" = Table.SplitColumn(#"Renamed Columns", "Stauts_Name", Splitter.SplitTextByPositions({0, 1}, false), {"Stauts_Name.1", "Stauts_Name.2"}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Split Column by Position",{{"Stauts_Name.1", type text}, {"Stauts_Name.2", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type2",{"Stauts_Name.1"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Removed Columns",{{"Stauts_Name.2", "Status_Name"}})
in
    #"Renamed Columns2"
```


## Table: ACTUAL_CF_Source


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("VZBNbsIwEIWvEmXdSokJ0Gyhi0ZtpEiBDRGLgZomwowr2xGoZ+lR2HGxjn9wxW7eN57xe9N1aZY8J2vc8SMgmnT71KU5kRpw5EI4zUi/SzQSRv0zfjk2IbYAPN6uO66MAk8Lok3dunpK9RJ0fxDynLRcDdzhGeF23yMt5+oAWo/oZ+fUqN4WccbBlwAbKcUQHpbEXj8ab9W6b0F8cnzcludhcjOgJoucvow99h+QJxvoRezYWA/AJqpNWWRe2lD1qiyYlzOX8WSyaQDzCCYe3AOs4OKBdV8tw42YtV+dvqXyl2d317ffeNbtHw==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Changed Type", "Column1", Splitter.SplitTextByDelimiter("-", QuoteStyle.Csv), {"Column1.1", "Column1.2"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Column1.1", Int64.Type}, {"Column1.2", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"Column1.1", "Source"}, {"Column1.2", "Status_Name"}}),
    #"Split Column by Delimiter1" = Table.SplitColumn(#"Renamed Columns", "Status_Name", Splitter.SplitTextByEachDelimiter({" "}, QuoteStyle.Csv, false), {"Status_Name.1", "Status_Name.2"}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Split Column by Delimiter1",{{"Status_Name.1", type text}, {"Status_Name.2", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type2",{"Status_Name.1"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns",{{"Status_Name.2", "Source_Name"}})
in
    #"Renamed Columns1"
```


## Table: Credit_Line_Avl Credit Line


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Corima_PowerBi_Credit_Lines.xlsx"), null, true),
    #"Credit Line_Sheet" = Source{[Item="Credit Line",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Credit Line_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"ID", Int64.Type}, {"Entity", Int64.Type}, {"Currency", type text}, {"Amount", Int64.Type}, {"Description", type text}})
in
    #"Changed Type"
```


## Table: Credit_Line_Mezzanine_Financing


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Corima_PowerBi_Credit_Lines.xlsx"), null, true),
    Mezzanine_Financing_Sheet = Source{[Item="Mezzanine_Financing",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Mezzanine_Financing_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"ID", Int64.Type}, {"Entity", Int64.Type}, {"Mezz_Finance_Type", type text}, {"Currency", type text}, {"Amount", Int64.Type}})
in
    #"Changed Type"
```


## Table: Credit_Line_Cash_Reserve


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/CashManagement/Shared%20Documents/General/Power%20BI%20Excel/Corima_PowerBi_Credit_Lines.xlsx"), null, true),
    Cash_Reserve_Sheet = Source{[Item="Cash_Reserve",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Cash_Reserve_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Entity", Int64.Type}, {"Currency", type text}, {"Amount", Int64.Type}})
in
    #"Changed Type"
```


## Table: ZZ_RollingCalender_Workdays_Future


```m
let
    Source = #date(2016, 1, 1),
    Custom1 = List.Dates (Source, Number.From(Date.AddDays(DateTime.LocalNow(), 365)) - Number.From(Source), #duration(1,0,0,0)),
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
    #"Inserted Day of Week" = Table.AddColumn(#"Renamed Columns3", "Day of Week", each Date.DayOfWeek([Date]), Int64.Type),
    #"Added Conditional Column" = Table.AddColumn(#"Inserted Day of Week", "If_Work_Day", each if [Day of Week] <= 4 then 1 else null),
    #"Inserted Day Name" = Table.AddColumn(#"Added Conditional Column", "Day Name", each Date.DayOfWeekName([Date]), type text),
    #"Merged Queries1" = Table.NestedJoin(#"Inserted Day Name", {"Date"}, ZZ_ECB_Excel_Holidays, {"Date"}, "Excel_Holidays", JoinKind.LeftOuter),
    #"Expanded ECB_Holiday_Calendar" = Table.ExpandTableColumn(#"Merged Queries1", "ZZ_ECB_Holiday_Calendar", {"Name_OF_Holiday"}, {"ZZ_ECB_Holiday_Calendar.Name_OF_Holiday"}),
    #"Expanded Excel_Holidays" = Table.ExpandTableColumn(#"Merged Queries1", "Excel_Holidays", {"Name_OF_Holiday", "Date", "Day Name"}, {"Excel_Holidays.Name_OF_Holiday", "Excel_Holidays.Date", "Excel_Holidays.Day Name"}),
    #"Removed Columns2" = Table.RemoveColumns(#"Expanded Excel_Holidays",{"Excel_Holidays.Day Name", "Excel_Holidays.Name_OF_Holiday"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns2", each ([If_Work_Day] = 1) and ([Excel_Holidays.Date] = null)),
    #"Inserted Age" = Table.AddColumn(#"Filtered Rows", "Age", each Date.From(DateTime.LocalNow()) - [Date], type duration),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Age",{{"Age", type number}}),
    #"Filtered Rows1" = Table.SelectRows(#"Changed Type1", each [Age] < 2)
in
    #"Filtered Rows1"
```


## Table: DW_CM_STMNT


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_DW_CM_STMNT = Corima{[Schema="dbo",Item="DW_CM_STMNT"]}[Data]
in
    dbo_DW_CM_STMNT
```


## Table: RB_CP_CASH_POOL_BALANCES


```m
let
    Source = Sql.Database("muc-mssql-1a.rolandberger.net", "RB_Treasury"),
    dbo_CP_CASH_POOL_BALANCES = Source{[Schema="dbo",Item="CP_CASH_POOL_BALANCES"]}[Data]
in
    dbo_CP_CASH_POOL_BALANCES
```


## Table: CIB LastRefresh


```m
let
    Source = Sql.Databases("muc-mssql-1a.rolandberger.net"),
    Corima = Source{[Name="Corima"]}[Data],
    dbo_DW_CIB_BALANCES = Corima{[Schema="dbo",Item="DW_CIB_BALANCES"]}[Data],
    #"Inserted Merged Column" = Table.AddColumn(dbo_DW_CIB_BALANCES, "Unique_Name_Datum", each Text.Combine({[SHORT_NAME], Text.From([DATUM], "de-DE")}, "_"), type text),
    #"Added Custom" = Table.AddColumn(#"Inserted Merged Column", "Custom", each Date.AddDays([DATUM],(-1))),
    #"Inserted Merged Column1" = Table.AddColumn(#"Added Custom", "Unique_Name&priviousDay", each Text.Combine({[SHORT_NAME], Text.From([Custom], "de-DE")}, "_"), type text),
    #"Reordered Columns" = Table.ReorderColumns(#"Inserted Merged Column1",{"ACCOUNT_ID", "SHORT_NAME", "CURRENCY", "DATUM", "VALUE_DATE_UNTIL", "PLANNED_SUM", "RECONCILIATED_SUM", "TOTAL_SUM", "RATES_VALUE", "TOTAL_SUM_EUR", "LEGAL_ENTITY_ID", "COUNTRY_ISO3", "ZONE", "Custom", "Unique_Name_Datum", "Unique_Name&priviousDay"}),
    #"Removed Columns" = Table.RemoveColumns(#"Reordered Columns",{"ACCOUNT_ID", "SHORT_NAME", "CURRENCY", "DATUM", "VALUE_DATE_UNTIL", "PLANNED_SUM", "RECONCILIATED_SUM", "TOTAL_SUM", "RATES_VALUE", "TOTAL_SUM_EUR", "LEGAL_ENTITY_ID", "COUNTRY_ISO3", "ZONE", "Custom", "Unique_Name_Datum", "Unique_Name&priviousDay"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns"),
    #"Sorted Rows" = Table.Sort(#"Removed Duplicates",{{"EXPORTED_ON", Order.Descending}}),
    #"Kept First Rows" = Table.FirstN(#"Sorted Rows",1)
in
    #"Kept First Rows"
```

