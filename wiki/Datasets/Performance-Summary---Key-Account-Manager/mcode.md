



# M Code

|Dataset|[Performance Summary - Key Account Manager](./../Performance-Summary---Key-Account-Manager.md)|
| :--- | :--- |
|Workspace|[IFRS_Reporting [QA]](../../Workspaces/IFRS_Reporting-[QA].md)|

## Table: msr v_employee_utilization


```m
let
    Source = #"msr v_employee_utilization_T",
    Publish = Source
in
    Publish
```


## Table: msr v_hr_employee_job_matrix


```m
let
    Source = #"msr v_hr_employee_job_matrix_T",
    Publish = Source
in
    Publish
```


## Table: rep v_hr_employee


```m
let
    Source = #"rep v_hr_employee_T",
    Publish = Source
in
    Publish
```


## Table: pub dim_date


```m
let
    Source = Sql.Databases("muc-mssql-2"),
    datahub = Source{[Name="datahub"]}[Data],
    pub_dim_date = datahub{[Schema="pub",Item="dim_date"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_dim_date, each Date.IsInCurrentYear([Date]) or Date.IsInPreviousYear([Date])),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"DateKey", "Date", "Day", "Weekday", "WeekDayName", "WeekOfYear", "Month", "MonthName", "Year", "YearMonthnumber", "FirstDayOfMonth", "YearMonthShort", "ISOWeekOfYearNameInCal"}),
    #"Inserted Text After Delimiter" = Table.AddColumn(#"Removed Other Columns", "MonthNameShort", each Text.AfterDelimiter(Text.Proper([YearMonthShort]), "/"), type text)
in
    #"Inserted Text After Delimiter"
```


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


## Table: utilization_budgets


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/Reports-Utilization/Shared%20Documents/Report_Utilization/Data/utilization_budgets.xlsx"), null, true),
    utilization_budgets_Table = Source{[Item="utilization_budgets",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(utilization_budgets_Table,{{"country_code_iso3", type text}, {"jobcode_id", type text}, {"jobcode", type text}, {"job_short", type text}, {"utilization_target", type number}})
in
    #"Changed Type"
```


## Table: msr v_fc_order_income_accumulated


```m
let
    Source = #"msr v_fc_order_income_accumulated_T"
in
    Source
```


## Table: OI_Budget_Countries


```m
let
    Source = OI_Budget_Countries_T
in
    Source
```


## Table: OI_Budget_Platforms_Function


```m
let
    Source = OI_Budget_Platforms_T,
    #"Filtered Rows" = Table.SelectRows(Source, each ([Platform] <> "Health & Consumer" and [Platform] <> "Industrials" and [Platform] <> "Regulated & Infrastructure" and [Platform] <> "Services"))
in
    #"Filtered Rows"
```


## Table: pub v_ll_company_to_region


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    pub_v_ll_company_to_region = Source{[Schema="pub",Item="v_ll_company_to_region"]}[Data],
    #"Filtered Rows" = Table.SelectRows(pub_v_ll_company_to_region, each ([company_id] <> "77"))
in
    #"Filtered Rows"
```


## Table: Dim_Industries


```m
let
    Source = #"msr v_fc_order_income_accumulated_E",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"industry"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each ([industry] <> "Not assigned"))
in
    #"Filtered Rows"
```


## Table: Dim_Functions


```m
let
    Source = #"msr v_fc_order_income_accumulated_E",
    #"Removed Other Columns" = Table.SelectColumns(Source,{"function"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each ([function] <> "Not assigned"))
in
    #"Filtered Rows"
```


## Table: OI_Budget_Platforms_Industry


```m
let
    Source = OI_Budget_Platforms_T,
    #"Filtered Rows" = Table.SelectRows(Source, each ([Platform] = "Health & Consumer" or [Platform] = "Industrials" or [Platform] = "Regulated & Infrastructure" or [Platform] = "Services"))
in
    #"Filtered Rows"
```

