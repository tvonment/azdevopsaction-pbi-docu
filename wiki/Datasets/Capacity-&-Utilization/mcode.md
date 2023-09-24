



# M Code

|Dataset|[Capacity & Utilization](./../Capacity-&-Utilization.md)|
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

OpenAI API Key is not configured
## Table: msr v_hr_employee_job_matrix


```m
let
    Source = #"msr v_hr_employee_job_matrix_T",
    Publish = Source
in
    Publish
```

OpenAI API Key is not configured
## Table: rep v_hr_employee


```m
let
    Source = #"rep v_hr_employee_T",
    Publish = Source
in
    Publish
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
    #"Inserted Text After Delimiter" = Table.AddColumn(#"Removed Other Columns", "MonthNameShort", each Text.AfterDelimiter(Text.Proper([YearMonthShort]), "/"), type text)
in
    #"Inserted Text After Delimiter"
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
## Table: xlsx utilization_targets


```m
let
    Source = #"xlsx utilization_targets_T",
    Publish = Source
in
    Publish
```

OpenAI API Key is not configured
## Table: msr v_employee_project_hours


```m
let
    Source = #"msr v_employee_project_hours_T",
    Publish = Source
in
    Publish
```

OpenAI API Key is not configured
## Table: utilization_budgets


```m
let
    Source = Excel.Workbook(Web.Contents("https://rberger.sharepoint.com/sites/Reports-Utilization/Shared%20Documents/Report_Utilization/Data/utilization_budgets.xlsx"), null, true),
    utilization_budgets_Table = Source{[Item="utilization_budgets",Kind="Table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(utilization_budgets_Table,{{"country_code_iso3", type text}, {"jobcode_id", type text}, {"jobcode", type text}, {"job_short", type text}, {"utilization_target", type number}})
in
    #"Changed Type"
```

OpenAI API Key is not configured
## Table: rep v_ll_head_platform


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_head_platform = Source{[Schema="rep",Item="v_ll_head_platform"]}[Data]
in
    rep_v_ll_head_platform
```

OpenAI API Key is not configured
## Table: rep v_ll_head_platform_DACH


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub"),
    rep_v_ll_head_platform_DACH = Source{[Schema="rep",Item="v_ll_head_platform_DACH"]}[Data]
in
    rep_v_ll_head_platform_DACH
```

OpenAI API Key is not configured
## Table: rep v_II_head_region_country


```m
let
    Source = Table.Combine({#"rep v_ll_head_region", #"rep v_ll_head_country"})
in
    Source
```

OpenAI API Key is not configured
## Roles

### Admin


Model Permission: Read
### RLS restricted


Model Permission: Read

rep v_II_head_region_country

```m
[email] = username()
```

OpenAI API Key is not configured

rep v_ll_head_platform

```m
[email] = username()
```

OpenAI API Key is not configured

rep v_ll_head_platform_DACH

```m
[email] = username()
```

OpenAI API Key is not configured