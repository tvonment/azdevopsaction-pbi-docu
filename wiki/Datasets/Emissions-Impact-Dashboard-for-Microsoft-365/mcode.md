



# M Code

|Dataset|[Emissions Impact Dashboard for Microsoft 365](./../Emissions-Impact-Dashboard-for-Microsoft-365.md)|
| :--- | :--- |
|Workspace|[Emissions Impact Dashboard for Microsoft 365](../../Workspaces/Emissions-Impact-Dashboard-for-Microsoft-365.md)|

## Table: TenantEmission


```m
let
    Source = OData.Feed("https://iks-powerbi.ideas.microsoft.com/api/connector/SustainabilityCalculator/v2.0.0/" & TenantID & "/", null, [Implementation="2.0"]),
    TenantEmission_table = Source{[Name="TenantEmission",Signature="table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(TenantEmission_table,{{"DateId", type text}}),
    #"Filtered out M365 rows" = Table.SelectRows(#"Changed Type", each not Text.Contains([ApplicationName], "M365")),
    #"Added Custom2" = Table.AddColumn(#"Filtered out M365 rows", "Date", each Date.From([DateId])),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom2",{{"Date", type datetime}})
in
    #"Changed Type2"
```


## Table: TenantUsage


```m
let
    Source = OData.Feed("https://iks-powerbi.ideas.microsoft.com/api/connector/SustainabilityCalculator/v2.0.0/" & TenantID & "/", null, [Implementation="2.0"]),
    TenantUsage_table = Source{[Name="TenantUsage",Signature="table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(TenantUsage_table,{{"DateId", type text}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Date", each Date.From([DateId])),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{{"Date", type date}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type1", each true)
in
    #"Filtered Rows"
```


## Table: LastRefreshTable


```m
let
Source = #table(type table[LastRefresh=datetime], {{DateTime.LocalNow()}})
in
    Source
```


## Table: Efficiency sort


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUfLJL1eK1YlWMgKyfVNTMktzwVxjINcjMz1DKTYWAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Order = _t, Efficiency = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Order", Int64.Type}, {"Efficiency", type text}})
in
    #"Changed Type"
```


## Table: DateTable


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMjDUByIjAwMDJR0lQyN9YxDHxFIpNhYA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [StartDate = _t, EndDate = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"StartDate", type date}, {"EndDate", type date}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Dates", each {Number.From([StartDate])..Number.From([EndDate])}),
    #"Expanded Dates" = Table.ExpandListColumn(#"Added Custom", "Dates"),
    #"Removed Other Columns" = Table.SelectColumns(#"Expanded Dates",{"Dates"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Other Columns",{{"Dates", type date}}),
    #"Inserted Year" = Table.AddColumn(#"Changed Type1", "Year", each Date.Year([Dates]), Int64.Type),
    #"Inserted Month" = Table.AddColumn(#"Inserted Year", "Month", each Date.Month([Dates]), Int64.Type),
    #"Inserted Month Name" = Table.AddColumn(#"Inserted Month", "Month Name", each Date.MonthName([Dates]), type text),
    #"Inserted Quarter" = Table.AddColumn(#"Inserted Month Name", "Quarter", each Date.QuarterOfYear([Dates]), Int64.Type),
    #"Inserted Week of Year" = Table.AddColumn(#"Inserted Quarter", "Week of Year", each Date.WeekOfYear([Dates]), Int64.Type),
    #"Inserted Day Name" = Table.AddColumn(#"Inserted Week of Year", "Day Name", each Date.DayOfWeekName([Dates]), type text),
    #"Inserted Day" = Table.AddColumn(#"Inserted Day Name", "Day", each Date.Day([Dates]), Int64.Type),
    #"Inserted Day of Year" = Table.AddColumn(#"Inserted Day", "Day of Year", each Date.DayOfYear([Dates]), Int64.Type),
    #"Added Custom1" = Table.AddColumn(#"Inserted Day of Year", "Day Short Name", each Text.Start([Day Name], 3)),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom1",{{"Day Short Name", type text}}),
    #"Added Custom2" = Table.AddColumn(#"Changed Type2", "Month Short Name", each Text.Start([Month Name], 3)),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Custom2",{{"Month Short Name", type text}}),
    #"Added Custom3" = Table.AddColumn(#"Changed Type3", "Month Year", each [Month Short Name]&" "&Text.From([Year])),
    #"Changed Type4" = Table.TransformColumnTypes(#"Added Custom3",{{"Month Year", type text}}),
    #"Added Custom4" = Table.AddColumn(#"Changed Type4", "DateID", each Date.ToText([Dates],"YYYYMMDD")),
    #"Changed Type5" = Table.TransformColumnTypes(#"Added Custom4",{{"DateID", type text}})
in
    #"Changed Type5"
```


## Table: Distance Convert Table


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8vVRitWJVvL2VYqNBQA=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Distance = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Distance", type text}})
in
    #"Changed Type"
```


## Table: MetricToolTips


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("lZG9CoNAEIRfZThIZ6M+ggSSQsRaLM5jo1u4F2414NuniPkhXCDXf/Mxs9t1prJh8ILjzKrsRZEXJeqmPsD5+WoDqxeTmWqyMhJY4B4BegZMn0UtSRLkGYpP01kWEuVl+0fDL3jYsKodKV7q4gMmHifSBUrhxo7QNu2X/rQT73I7+2Np4tC4JfFcRdyS9jmUpu/v", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [MetricName = _t, Title = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"MetricName", type text}, {"Title", type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type","Change in carbon emissions 1, 2","Change in carbon emissions scope 1 and 2",Replacer.ReplaceText,{"Title"})
in
    #"Replaced Value"
```


## Table: ScopeMethodology


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUfJNLMpOLdFNSixOTVGK1YlWMgIK+uQnJ5Zk5ufBhGMB", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [#"Methodology Index" = _t, Methodology = _t]),
    #"Changed Type1" = Table.TransformColumnTypes(Source,{{"Methodology Index", Int64.Type}})
in
    #"Changed Type1"
```


## Table: EmissionsSavingsMultiplier


```m
let
    Source = OData.Feed("https://iks-powerbi.ideas.microsoft.com/api/connector/SustainabilityCalculator/v2.0.0/" & TenantID & "/", null, [Implementation="2.0"]),
    EmissionsSavingsMultiplier_table = Source{[Name="EmissionsSavingsMultiplier",Signature="table"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(EmissionsSavingsMultiplier_table,{{"SavingsMultiplier", "Value"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "SavingsMultiplier", each 1/(1-[Value])),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"SavingsMultiplier", type number}})
in
    #"Changed Type"
```


## Parameter: TenantID


Please provide your TenantID here.

```m
"72f988bf-86f1-41af-91ab-2d7cd011db47" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

