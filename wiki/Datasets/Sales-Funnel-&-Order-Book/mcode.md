



# M Code

|Dataset|[Sales Funnel & Order Book](./../Sales-Funnel-&-Order-Book.md)|
| :--- | :--- |
|Workspace|[IFRS_Reporting [QA]](../../Workspaces/IFRS_Reporting-[QA].md)|

## Table: msr v_hr_employee_job_matrix


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    msr_v_hr_employee_job_matrix = datahub{[Schema="msr",Item="v_hr_employee_job_matrix"]}[Data],
    #"Filtered Rows" = Table.SelectRows(msr_v_hr_employee_job_matrix, each Date.IsInCurrentYear([key_date]))
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: rep v_hr_employee


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    rep_v_hr_employee = datahub{[Schema="rep",Item="v_hr_employee"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_hr_employee, each [ter_max_date] > #date(2022, 12, 31))
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: pub dim_date


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    pub_dim_date = datahub{[Schema="pub",Item="dim_date"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_dim_date, each Date.IsInCurrentYear([Date]) or Date.IsInPreviousYear([Date])),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"DateKey", "Date", "Day", "Weekday", "WeekDayName", "WeekOfYear", "Month", "MonthName", "Year", "YearMonthnumber", "FirstDayOfMonth", "YearMonthShort", "ISOWeekOfYearNameInCal"}),
    #"Inserted First Characters" = Table.AddColumn(#"Removed Other Columns", "MonthNameShort", each Text.Start([MonthName], 3), type text),
    #"Inserted Quarter" = Table.AddColumn(#"Inserted First Characters", "QuarterNr", each Date.QuarterOfYear([Date]), type text),
    #"Inserted Merged Column" = Table.AddColumn(#"Inserted Quarter", "Quarter", each Text.Combine({"Q", Text.From([QuarterNr], "de-DE")}), type text),
    #"Changed Type" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"QuarterNr", Int64.Type}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: msr v_fc_order_income_accumulated


```m
let
    Source = #"msr v_fc_order_income_accumulated_source",
    #"Filtered Rows" = Table.SelectRows(Source, each ([industry] <> "Not assigned")),
    #"Inserted Month" = Table.AddColumn(#"Filtered Rows", "Month", each Date.Month([report_month]), Int64.Type),
    #"Removed Columns" = Table.RemoveColumns(#"Inserted Month",{"Month"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns", "report_month_previous", each Date.AddMonths([report_month], -1), type date),
    #"Inserted Text After Delimiter" = Table.AddColumn(#"Added Custom", "report_month_previous_id", each Text.AfterDelimiter(Text.From([report_month_previous], "de-DE"), "."), type text),
    #"Merged Queries" = Table.NestedJoin(#"Inserted Text After Delimiter", {"project_number", "industry", "function", "company_name", "report_month_previous_id"}, #"msr v_fc_order_income_accumulated_source", {"project_number", "industry", "function", "company_name", "report_month_id"}, "msr v_fc_order_income_accumulated_source", JoinKind.LeftOuter),
    #"Expanded msr v_fc_order_income_accumulated_source" = Table.ExpandTableColumn(#"Merged Queries", "msr v_fc_order_income_accumulated_source", {"order_income"}, {"order_income_previous"}),
    #"Replaced Value" = Table.ReplaceValue(#"Expanded msr v_fc_order_income_accumulated_source",null,0,Replacer.ReplaceValue,{"order_income_previous"}),
    #"Added Custom1" = Table.AddColumn(#"Replaced Value", "order_income_current", each [order_income] - [order_income_previous], type number),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom1",{{"order_income", "order_income_total"}}),
    #"Replaced Value1" = Table.ReplaceValue(#"Renamed Columns","Not assigned","Not Assigned",Replacer.ReplaceText,{"industry"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","Not assigned","Not Assigned",Replacer.ReplaceText,{"function"}),
    #"Merged Queries1" = Table.NestedJoin(#"Replaced Value2", {"industry"}, platform_sort, {"platform_1_name"}, "platform_sort", JoinKind.LeftOuter),
    #"Expanded platform_sort2" = Table.ExpandTableColumn(#"Merged Queries1", "platform_sort", {"platform_1_sort", "platform_1_name_short"}, {"platform_1_sort", "platform_1_name_short"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Expanded platform_sort2",{{"platform_1_sort", "industry_sort"}, {"platform_1_name_short", "industry_name_short"}}),
    #"Merged Queries2" = Table.NestedJoin(#"Renamed Columns2", {"function"}, platform_sort, {"platform_1_name"}, "platform_sort", JoinKind.LeftOuter),
    #"Expanded platform_sort" = Table.ExpandTableColumn(#"Merged Queries2", "platform_sort", {"platform_1_sort", "platform_1_name_short"}, {"platform_1_sort", "platform_1_name_short"}),
    #"Renamed Columns3" = Table.RenameColumns(#"Expanded platform_sort",{{"platform_1_sort", "function_sort"}, {"platform_1_name_short", "function_name_short"}}),
    #"Merged Queries3" = Table.NestedJoin(#"Renamed Columns3", {"project_number", "report_month_id"}, #"sec acp_orderIncome_byMonth", {"project_number", "report_month_id"}, "sec acp_orderIncome_byMonth", JoinKind.LeftOuter),
    #"Expanded sec acp_orderIncome_byMonth" = Table.ExpandTableColumn(#"Merged Queries3", "sec acp_orderIncome_byMonth", {"orderIncome"}, {"orderIncome"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Expanded sec acp_orderIncome_byMonth",{{"orderIncome", "order_income_GROSS"}}),
    #"Replaced Value3" = Table.ReplaceValue(#"Renamed Columns1","Hongkong","Hong Kong",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","Middle East Bahr.","Bahrain",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","PX America","PXNorth America",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5","PX Engineers","PXEngineering",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value6","PX Partner","PXPartner",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value8" = Table.ReplaceValue(#"Replaced Value7","Rep. of Korea","South Korea",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value9" = Table.ReplaceValue(#"Replaced Value8","Singapur","Singapore",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value10" = Table.ReplaceValue(#"Replaced Value9","TMG","Turnaround Management GmbH",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value11" = Table.ReplaceValue(#"Replaced Value10","UK","United Kingdom",Replacer.ReplaceText,{"company_name"}),
    #"Merged Queries4" = Table.NestedJoin(#"Replaced Value11", {"industry_subject"}, subplatforms_industry, {"industry_subject"}, "subplatforms_industry", JoinKind.LeftOuter),
    #"Expanded subplatforms_industry" = Table.ExpandTableColumn(#"Merged Queries4", "subplatforms_industry", {"industry_subplatform"}, {"industry_subplatform"}),
    #"Replaced Value12" = Table.ReplaceValue(#"Expanded subplatforms_industry","Turnaround Management GmbH","TMG",Replacer.ReplaceText,{"company_name"}),
    #"Replaced Value13" = Table.ReplaceValue(#"Replaced Value12","test12345","test54321",Replacer.ReplaceText,{"project_number"})
in
    #"Replaced Value13"
```

OpenAI API Key is not configured
## Table: Temp_values


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMjQAAaXYWAA=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Net_order_income = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Net_order_income", Int64.Type}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: Refresh_Timestamp


```m
let
    StandardOffset = #duration(0, 1, 0, 0),
    DaylightSavingTimeOffset = #duration(0, 2, 0, 0),

    // get start and end of daylight saving time
    // this code implements the rules of EU counties
    // if it doesn't fill your expectations, visit https://en.wikipedia.org/wiki/Daylight_saving_time_by_country and implement your own function
    fnDaylightSavingTimePeriod = (
        now as datetime
    ) as record => 
        let
            // the daylight saving time starts on the last Sunday of March at 1am UTC
            LastDayOfMarch = #date(Date.Year(now), 3, 31),
            StartOfDaylightSavingTime = Date.AddDays(LastDayOfMarch, -Date.DayOfWeek(LastDayOfMarch)) & #time(1, 0, 0),
            // the daylight saving time ends on the last Sunday in October at 1am UTC
            LastDayOfOctober = #date(Date.Year(now), 10, 31),
            EndOfDaylightSavingTime = Date.AddDays(LastDayOfOctober, -Date.DayOfWeek(LastDayOfOctober)) & #time(1, 0, 0)
        in
            [From = StartOfDaylightSavingTime, To = EndOfDaylightSavingTime],

    // get a timestamp in UTC (with offset 00:00 all year long)
    UtcNow = DateTimeZone.UtcNow(),
    // convert UTC datetime with offset to datetime
    UtcNowWithoutZone = DateTimeZone.RemoveZone(UtcNow),

    // get daylight saving time period
    DaylightSavingTimePeriod = fnDaylightSavingTimePeriod(UtcNowWithoutZone),

    // convert UTC time to the local time with respect to current offset
    LocalTimeWithOffset = 
        if UtcNowWithoutZone >= DaylightSavingTimePeriod[From] and UtcNowWithoutZone <= DaylightSavingTimePeriod[To] then
            DateTimeZone.SwitchZone(
                UtcNow, 
                Duration.Hours(DaylightSavingTimeOffset), 
                Duration.Minutes(DaylightSavingTimeOffset)
            )
        else
            DateTimeZone.SwitchZone(
                UtcNow, 
                Duration.Hours(StandardOffset), 
                Duration.Minutes(StandardOffset)
            ),
    
    // current date time without offset
    LocalTime = DateTimeZone.RemoveZone(LocalTimeWithOffset),

    // result table
    Result = #table(
        type table
        [
            #"UTC timestamp" = datetime, 
            #"UTC date" = date,
            #"Local timestamp with offset" = datetimezone,
            #"Local timestamp without offset" = datetime
        ], 
        {
            {
            UtcNowWithoutZone,
            DateTime.Date(UtcNowWithoutZone),
            LocalTimeWithOffset,
            LocalTime
            }
        }
    ),
    #"Inserted Date" = Table.AddColumn(Result, "Last_refresh_local", each DateTime.Date([Local timestamp without offset]), type date),
    #"Removed Columns" = Table.RemoveColumns(#"Inserted Date",{"UTC date", "Local timestamp without offset"})
in
    #"Removed Columns"
```

OpenAI API Key is not configured
## Table: Temp_values_slicer


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45Wcs4vzSspqlQoy0wtV9JRMlSK1YlWCshJLEnLL8qFiRpBRIvys1KTS2CCxmBBx6RiBX9PINcEzPX3VChILVIIAAqYggXOTXEKdVEFcs2g3IBIEM9cKTYWAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Peergroup_Comparison_Slicer = _t, Sort = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Peergroup_Comparison_Slicer", type text}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: OI_Budget_Countries


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/Reports-Report_OI/Shared%20Documents/Report_OI/Data/OI%20Budgets_monthly_vPowerBI.xlsx")),
    #"OI Budget Countries_sheet" = Source{[Item="OI Budget Countries",Kind="Sheet"]}[Data],
    #"Removed Top Rows" = Table.Skip(#"OI Budget Countries_sheet", 6),
    #"Removed Bottom Rows" = Table.RemoveLastN(#"Removed Top Rows", 29),
    #"Removed Other Columns" = Table.SelectColumns(#"Removed Bottom Rows", {"Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30", "Column31", "Column32", "Column33", "Column34", "Column35", "Column36", "Column37", "Column38", "Column39", "Column40", "Column41", "Column42", "Column43", "Column44", "Column45", "Column46", "Column47", "Column48", "Column49", "Column50", "Column51", "Column52", "Column53", "Column54", "Column55", "Column56", "Column57", "Column58", "Column59", "Column60", "Column61", "Column62"}),
    FilterNullAndWhitespace = each List.Select(_, each _ <> null and (not (_ is text) or Text.Trim(_) <> "")),
    #"Removed Blank Rows" = Table.SelectRows(#"Removed Other Columns", each not List.IsEmpty(FilterNullAndWhitespace(Record.FieldValues(_)))),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Blank Rows", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Country", type text}, {"BEL", type number}, {"ME", type number}, {"QAT", type number}, {"BHR/KSA/UAE", type number}, {"BHR", type number}, {"KSA", type number}, {"UAE", Int64.Type}, {"CIS", Int64.Type}, {"RUS", Int64.Type}, {"UKR", Int64.Type}, {"DACH", type number}, {"GER", type number}, {"AUT", Int64.Type}, {"CHE", Int64.Type}, {"OLD CHE", Int64.Type}, {"ESP", type number}, {"FRA", Int64.Type}, {"HUN", Int64.Type}, {"ITA", Int64.Type}, {"MOR", Int64.Type}, {"PRT", type number}, {"NLD", type number}, {"NOR", Int64.Type}, {"ROU", type number}, {"UK", type number}, {"CEE", Int64.Type}, {"CZE", Int64.Type}, {"CRO", Int64.Type}, {"POL", Int64.Type}, {"EMEA", type number}, {"BRA", type number}, {"CAN", type number}, {"USA", type number}, {"MEX", type number}, {"Americas", type number}, {"CHN", type number}, {"CHN_1", type number}, {"HKG", type number}, {"IND", type number}, {"JPN", type number}, {"KOR", type number}, {"SEA", type number}, {"IDN", type number}, {"MMR", type number}, {"MYS", type number}, {"SGP", type number}, {"THA", type number}, {"VNM", type number}, {"Asia", type number}, {"Polarix", type number}, {"PX Partner", type number}, {"PX Engineers", type number}, {"PX America", type number}, {"TMG", type number}, {"Other RB companies", type number}, {"Subtotal", type number}, {"HOL", type number}, {"Subtotal_2", type number}, {"Column60", type number}, {"Total", type number}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type",{{"Country", "Period"}, {"Column60", "Global Adjustment"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns1",{"BHR/KSA/UAE", "OLD CHE", "EMEA", "Americas", "CHN_1", "HKG", "Asia", "Other RB companies", "Subtotal", "HOL", "Subtotal_2", "Total", "ME", "SEA", "DACH"}),
    #"Removed Bottom Rows1" = Table.RemoveLastN(#"Removed Columns",1),
    #"Added Year" = Table.AddColumn(#"Removed Bottom Rows1", "Year", each Text.BeforeDelimiter([Period], "_"), type text),
    #"Added MonthName" = Table.AddColumn(#"Added Year", "MonthName", each Text.BetweenDelimiters([Period], "_", "_", 1, 0), type text),
    #"Added Month" = Table.AddColumn(#"Added MonthName", "Month", each if [MonthName] = "Jan" then 1 else if [MonthName] = "Feb" then 2 else if [MonthName] = "Mar" then 3 else if [MonthName] = "Apr" then 4 else if [MonthName] = "May" then 5 else if [MonthName] = "Jun" then 6 else if [MonthName] = "Jul" then 7 else if [MonthName] = "Aug" then 8 else if [MonthName] = "Sep" then 9 else if [MonthName] = "Oct" then 10 else if [MonthName] = "Nov" then 11 else if [MonthName] = "Dec" then 12 else null, type number),
    #"Inserted Merged Column" = Table.AddColumn(#"Added Month", "FirstDayOfMonth", each Text.Combine({"1/", Text.From([Month], "en-CH"), "/", [Year]}), type text),
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"FirstDayOfMonth", type date}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Changed Type1",{"Period", "Year", "MonthName", "Month"}),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Removed Columns1", {"FirstDayOfMonth"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Other Columns",{{"Attribute", "Country"}, {"Value", "OI_Budget"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","GER","DEU",Replacer.ReplaceText,{"Country"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","UK","GBR",Replacer.ReplaceValue,{"Country"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","UAE","ARE",Replacer.ReplaceText,{"Country"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","MOR","MAR",Replacer.ReplaceText,{"Country"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","KSA","SAU",Replacer.ReplaceText,{"Country"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","NOR","SWE",Replacer.ReplaceText,{"Country"})
in
    #"Replaced Value5"
```

OpenAI API Key is not configured
## Table: pub v_ll_company_to_region


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_v_ll_company_to_region = Source{[Schema="pub",Item="v_ll_company_to_region"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_v_ll_company_to_region, each ([company_id] <> "77")),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows","polariXpartner","PXPartner",Replacer.ReplaceText,{"region_reporting_level3"}),
    #"Added Conditional Column" = Table.AddColumn(#"Replaced Value", "region_reporting_level1_sort", each if [region_reporting_level1] = "EMEA" then 1 else if [region_reporting_level1] = "Non-operational companies" then 6 else if [region_reporting_level1] = "Holding" then 5 else if [region_reporting_level1] = "Other RB companies" then 4 else if [region_reporting_level1] = "Americas" then 2 else if [region_reporting_level1] = "Asia" then 3 else if [region_reporting_level1] = "RUS" then 7 else null, type number)
in
    #"Added Conditional Column"
```

OpenAI API Key is not configured
## Table: msr v_fc_project_data


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    msr_v_fc_project_data = Source{[Schema="msr",Item="v_fc_project_data"]}[Data],
    #"Added Custom Column" = Table.AddColumn(msr_v_fc_project_data, "delivery_manager_short", each let splitdeliverymanager = Splitter.SplitTextByDelimiter(" ", QuoteStyle.None)([delivery_manager]), splitdeliverymanager2 = Splitter.SplitTextByDelimiter(", ", QuoteStyle.None)([delivery_manager]) in Text.Combine({splitdeliverymanager{0}?, " ", Text.Start(splitdeliverymanager2{1}?, 1), "."}), type text),
    #"Replaced Value" = Table.ReplaceValue(#"Added Custom Column",".","",Replacer.ReplaceText,{"delivery_manager_short"})
in
    #"Replaced Value"
```

OpenAI API Key is not configured
## Table: OI_Budget_Platforms_Function


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/Reports-Report_OI/Shared%20Documents/Report_OI/Data/OI%20Budgets_monthly_vPowerBI.xlsx")),
    #"OI Budget Countries_sheet" = Source{[Item="OI Budget Platforms",Kind="Sheet"]}[Data],
    #"Removed Top Rows" = Table.Skip(#"OI Budget Countries_sheet",3),
    #"Removed Bottom Rows" = Table.RemoveLastN(#"Removed Top Rows", 17),
    #"Removed Alternate Rows" = Table.AlternateRows(#"Removed Bottom Rows",2,1,1),
    #"Filtered Rows" = Table.SelectRows(#"Removed Alternate Rows", each ([Column2] <> "Total")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"Column2", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16"}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Other Columns", [PromoteAllScalars=true]),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Promoted Headers", {"[EUR m]"}, "Attribute", "Value"),
    #"Changed Type" = Table.TransformColumnTypes(#"Unpivoted Other Columns",{{"Value", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"[EUR m]", "Platform"}, {"Attribute", "MonthName"}, {"Value", "OI_Budget"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Year", each 2023, Int64.Type),
    #"Added Month" = Table.AddColumn(#"Added Custom", "Month", each if [MonthName] = "Jan" then 1 else if [MonthName] = "Feb" then 2 else if [MonthName] = "Mar" then 3 else if [MonthName] = "Apr" then 4 else if [MonthName] = "May" then 5 else if [MonthName] = "Jun" then 6 else if [MonthName] = "Jul" then 7 else if [MonthName] = "Aug" then 8 else if [MonthName] = "Sep" then 9 else if [MonthName] = "Oct" then 10 else if [MonthName] = "Nov" then 11 else if [MonthName] = "Dec" then 12 else null, type number),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Month",{{"Year", type text}, {"Month", type text}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Changed Type1", "FirstDayOfMonth", each Text.Combine({"1/", Text.From([Month], "en-CH"), "/", [Year]}), type text),
    #"Changed Type2" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"FirstDayOfMonth", type date}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Changed Type2",{"FirstDayOfMonth", "Platform", "MonthName", "OI_Budget", "Year", "Month"}),
    #"Removed Columns" = Table.RemoveColumns(#"Reordered Columns",{"MonthName", "Year", "Month"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns", each ([Platform] <> "Health & Consumer" and [Platform] <> "Industrials" and [Platform] <> "Regulated & Infrastructure" and [Platform] <> "Services"))
in
    #"Filtered Rows1"
```

OpenAI API Key is not configured
## Table: sec acp_orderIncome_byMonth


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    sec_acp_orderIncome_byMonth = Source{[Schema="msr",Item="v_fc_order_income_byMonth"]}[Data],
    #"Added Custom Column" = Table.AddColumn(sec_acp_orderIncome_byMonth, "report_month_id", each Text.Combine({Text.PadStart(Text.From([month], "de-DE"), 2, "0"), ".", Text.From([year], "de-DE")}), type text),
    #"Inserted Merged Column" = Table.AddColumn(#"Added Custom Column", "report_month", each Text.Combine({"01.", [report_month_id]}), type text),
    #"Changed Type" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"report_month", type date}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: rep v_ll_head_region


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_head_region = Source{[Schema="rep",Item="v_ll_head_region"]}[Data]
in
    rep_v_ll_head_region
```

OpenAI API Key is not configured
## Table: rep v_ll_head_platform_DACH_industry


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_head_platform_DACH = Source{[Schema="rep",Item="v_ll_head_platform_DACH"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_ll_head_platform_DACH, each ([platform] = "Health & Consumer" or [platform] = "Industrials" or [platform] = "Regulated & Infrastructure" or [platform] = "Services"))
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: rep v_ll_head_platform_industry


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_head_platform = Source{[Schema="rep",Item="v_ll_head_platform"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_ll_head_platform, each ([platform_name] = "Health & Consumer" or [platform_name] = "Industrials" or [platform_name] = "Regulated & Infrastructure" or [platform_name] = "Services"))
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: rep v_ll_head_country


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_head_country = Source{[Schema="rep",Item="v_ll_head_country"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(rep_v_ll_head_country,{{"emp_id_head", "emp_id"}, {"email_head", "email"}})
in
    #"Renamed Columns"
```

OpenAI API Key is not configured
## Table: msr v_fc_order_income_budget_orgunit


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    msr_v_fc_order_income_budget_orgunit = Source{[Schema="msr",Item="v_fc_order_income_budget_orgunit"]}[Data],
    #"Filtered Rows" = Table.SelectRows(msr_v_fc_order_income_budget_orgunit, each true)
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: msr v_fc_order_income_budget_platform


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    msr_v_fc_order_income_budget_platform = Source{[Schema="msr",Item="v_fc_order_income_budget_platform"]}[Data]
in
    msr_v_fc_order_income_budget_platform
```

OpenAI API Key is not configured
## Table: RLS_active_role


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45Wyk1R0lEyBGIQitWJVipKTc/MzwPyjCCCKal5mcV6KakF+aUVDkX5OYl5KUmpRempRXrJ+blgHcn5pXklRZVAtcYE1UMtKchJLEnLLwLxTZDshgnHpyQmZwAFTZHkshNBqs1gIrEA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [role_name = _t, role_id = _t, country_mapping = _t, region_mapping = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"role_name", type text}, {"role_id", Int64.Type}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: OI_Budget_Platforms_Industry


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/Reports-Report_OI/Shared%20Documents/Report_OI/Data/OI%20Budgets_monthly_vPowerBI.xlsx")),
    #"OI Budget Countries_sheet" = Source{[Item="OI Budget Platforms",Kind="Sheet"]}[Data],
    #"Removed Top Rows" = Table.Skip(#"OI Budget Countries_sheet",3),
    #"Removed Bottom Rows" = Table.RemoveLastN(#"Removed Top Rows", 17),
    #"Removed Alternate Rows" = Table.AlternateRows(#"Removed Bottom Rows",2,1,1),
    #"Filtered Rows" = Table.SelectRows(#"Removed Alternate Rows", each ([Column2] <> "Total")),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"Column2", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16"}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Other Columns", [PromoteAllScalars=true]),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Promoted Headers", {"[EUR m]"}, "Attribute", "Value"),
    #"Changed Type" = Table.TransformColumnTypes(#"Unpivoted Other Columns",{{"Value", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"[EUR m]", "Platform"}, {"Attribute", "MonthName"}, {"Value", "OI_Budget"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Year", each 2023, Int64.Type),
    #"Added Month" = Table.AddColumn(#"Added Custom", "Month", each if [MonthName] = "Jan" then 1 else if [MonthName] = "Feb" then 2 else if [MonthName] = "Mar" then 3 else if [MonthName] = "Apr" then 4 else if [MonthName] = "May" then 5 else if [MonthName] = "Jun" then 6 else if [MonthName] = "Jul" then 7 else if [MonthName] = "Aug" then 8 else if [MonthName] = "Sep" then 9 else if [MonthName] = "Oct" then 10 else if [MonthName] = "Nov" then 11 else if [MonthName] = "Dec" then 12 else null, type number),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Month",{{"Year", type text}, {"Month", type text}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Changed Type1", "FirstDayOfMonth", each Text.Combine({"1/", Text.From([Month], "en-CH"), "/", [Year]}), type text),
    #"Changed Type2" = Table.TransformColumnTypes(#"Inserted Merged Column",{{"FirstDayOfMonth", type date}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Changed Type2",{"FirstDayOfMonth", "Platform", "MonthName", "OI_Budget", "Year", "Month"}),
    #"Removed Columns" = Table.RemoveColumns(#"Reordered Columns",{"MonthName", "Year", "Month"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns", each ([Platform] = "Health & Consumer" or [Platform] = "Industrials" or [Platform] = "Regulated & Infrastructure" or [Platform] = "Services"))
in
    #"Filtered Rows1"
```

OpenAI API Key is not configured
## Table: platforms_industry


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/Reports-Utilization/Shared%20Documents/Report_Utilization/Data/platform_sort.xlsx"), null, true),
    platform_sort_Table = Source{[Item="platform_sort",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(platform_sort_Table,{{"platform_1_name", type text}, {"platform_1_id", type text}, {"platform_1_sort", Int64.Type}, {"platform_1_name_short", type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([platform_1_name] = "Health & Consumer" or [platform_1_name] = "Industrials" or [platform_1_name] = "Regulated & Infrastructure" or [platform_1_name] = "Services")),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows", {"platform_1_name"})
in
    #"Removed Duplicates"
```

OpenAI API Key is not configured
## Table: platforms_function


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/Reports-Utilization/Shared%20Documents/Report_Utilization/Data/platform_sort.xlsx"), null, true),
    platform_sort_Table = Source{[Item="platform_sort",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(platform_sort_Table,{{"platform_1_name", type text}, {"platform_1_id", type text}, {"platform_1_sort", Int64.Type}, {"platform_1_name_short", type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([platform_1_name] = "Digital" or [platform_1_name] = "Investor Support" or [platform_1_name] = "Operations" or [platform_1_name] = "RPT" or [platform_1_name] = "Strategy & Others")),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows", {"platform_1_name"})
in
    #"Removed Duplicates"
```

OpenAI API Key is not configured
## Table: rep v_ll_head_platform_DACH_function


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_head_platform_DACH = Source{[Schema="rep",Item="v_ll_head_platform_DACH"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_ll_head_platform_DACH, each ([platform] = "Digital" or [platform] = "Investor Support" or [platform] = "Operations" or [platform] = "RPT"))
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: rep v_ll_head_platform_function


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_head_platform = Source{[Schema="rep",Item="v_ll_head_platform"]}[Data],
    #"Filtered Rows" = Table.SelectRows(rep_v_ll_head_platform, each ([platform_name] <> "Health & Consumer" and [platform_name] <> "Industrials" and [platform_name] <> "Regulated & Infrastructure" and [platform_name] <> "Services")),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows","General","Strategy & Others",Replacer.ReplaceText,{"platform_name"})
in
    #"Replaced Value"
```

OpenAI API Key is not configured
## Table: rep v_II_head_region_country


```m
let
    Source = Table.Combine({#"rep v_ll_head_region", #"rep v_ll_head_country"}),
    #"Filtered Rows" = Table.SelectRows(Source, each true)
in
    #"Filtered Rows"
```

OpenAI API Key is not configured
## Table: nxtgn_opportunityregistrations


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    nxtgn_opportunityregistrations_table = Source{[Name="nxtgn_opportunityregistrations",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_opportunityregistrations_table,{"nxtgn_probability", "nxtgn_salesteam_concatinate", "createdon", "nxtgn_deliverystartdate", "nxtgn_actualclosedate", "_nxtgn_accountid_value", "_nxtgn_keyaccount_value", "nxtgn_clusterexpertteams_calc", "_nxtgn_sectorsapid_value", "nxtgn_opportunityregistrationid", "_transactioncurrencyid_value", "nxtgn_topic", "nxtgn_innovationtopics", "nxtgn_deliveryenddate", "statuscode", "nxtgn_estclosedate", "nxtgn_multiplesapplatformid", "nxtgn_multiplesapfunctionid", "nxtgn_estrevenue", "_nxtgn_salesunitid_value", "nxtgn_FunctionCCId", "nxtgn_IndustryCCId", "nxtgn_ThemeSAPId", "nxtgn_SectorSAPId"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Other Columns",{"nxtgn_opportunityregistrationid", "_nxtgn_accountid_value", "_nxtgn_keyaccount_value", "nxtgn_topic", "nxtgn_salesteam_concatinate", "statuscode", "nxtgn_estrevenue", "nxtgn_probability", "nxtgn_estclosedate", "nxtgn_deliverystartdate", "nxtgn_actualclosedate", "nxtgn_clusterexpertteams_calc", "_nxtgn_sectorsapid_value", "_transactioncurrencyid_value", "nxtgn_innovationtopics", "nxtgn_deliveryenddate", "nxtgn_multiplesapplatformid", "nxtgn_multiplesapfunctionid", "_nxtgn_salesunitid_value", "nxtgn_IndustryCCId", "nxtgn_SectorSAPId", "nxtgn_FunctionCCId", "nxtgn_ThemeSAPId", "createdon"}),
    #"Expanded nxtgn_IndustryCCId" = Table.ExpandRecordColumn(#"Reordered Columns", "nxtgn_IndustryCCId", {"new_code_string_industrycc", "nxtgn_name"}, {"nxtgn_IndustryCCId.new_code_string_industrycc", "nxtgn_IndustryCCId.nxtgn_name"}),
    #"Expanded nxtgn_SectorSAPId" = Table.ExpandRecordColumn(#"Expanded nxtgn_IndustryCCId", "nxtgn_SectorSAPId", {"nxtgn_name", "nxtgn_code"}, {"nxtgn_SectorSAPId.nxtgn_name", "nxtgn_SectorSAPId.nxtgn_code"}),
    #"Expanded nxtgn_FunctionCCId" = Table.ExpandRecordColumn(#"Expanded nxtgn_SectorSAPId", "nxtgn_FunctionCCId", {"nxtgn_name", "new_code_string"}, {"nxtgn_FunctionCCId.nxtgn_name", "nxtgn_FunctionCCId.new_code_string"}),
    #"Expanded nxtgn_ThemeSAPId" = Table.ExpandRecordColumn(#"Expanded nxtgn_FunctionCCId", "nxtgn_ThemeSAPId", {"nxtgn_name", "nxtgn_code"}, {"nxtgn_ThemeSAPId.nxtgn_name", "nxtgn_ThemeSAPId.nxtgn_code"}),
    #"Inserted Text Before Delimiter" = Table.AddColumn(#"Expanded nxtgn_ThemeSAPId", "Industry Platform (Datahub)", each Text.BeforeDelimiter([nxtgn_IndustryCCId.nxtgn_name], " ("), type text),
    #"Inserted Text Before Delimiter1" = Table.AddColumn(#"Inserted Text Before Delimiter", "Functional Platform (Datahub)", each Text.BeforeDelimiter([nxtgn_FunctionCCId.nxtgn_name], " ("), type text)
in
    #"Inserted Text Before Delimiter1"
```

OpenAI API Key is not configured
## Table: nxtgn_shareofwallets


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    nxtgn_shareofwallets_table = Source{[Name="nxtgn_shareofwallets",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_shareofwallets_table, each ([nxtgn_iscountry] = true)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_rblegalunit", "_nxtgn_salesleadid_value", "nxtgn_shareofwalletid", "nxtgn_countrypercentage", "nxtgn_rblegalunitccid"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Other Columns",{"_nxtgn_salesleadid_value", "nxtgn_shareofwalletid", "nxtgn_rblegalunit", "nxtgn_rblegalunitccid", "nxtgn_countrypercentage"})
in
    #"Reordered Columns"
```

OpenAI API Key is not configured
## Table: transactioncurrencies


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    transactioncurrencies_table = Source{[Name="transactioncurrencies",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(transactioncurrencies_table,{"isocurrencycode", "currencyname", "exchangerate", "currencysymbol", "transactioncurrencyid"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Other Columns",{"transactioncurrencyid", "isocurrencycode", "currencyname", "currencysymbol", "exchangerate"})
in
    #"Reordered Columns"
```

OpenAI API Key is not configured
## Roles

### Admin


Model Permission: Read
### RLS restricted


Model Permission: Read

rep v_ll_head_platform_industry

```m
[email] = username()
```

OpenAI API Key is not configured

rep v_ll_head_platform_DACH_industry

```m
[email] = username()
```

OpenAI API Key is not configured

rep v_ll_head_platform_DACH_function

```m
[email] = username()
```

OpenAI API Key is not configured

rep v_ll_head_platform_function

```m
[email] = username()
```

OpenAI API Key is not configured

rep v_II_head_region_country

```m
[email] = username()
```

OpenAI API Key is not configured