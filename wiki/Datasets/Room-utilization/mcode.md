



# M Code

|Dataset|[Room utilization](./../Room-utilization.md)|
| :--- | :--- |
|Workspace|[MUC Office utilization](../../Workspaces/MUC-Office-utilization.md)|

## Table: RoomBookings


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\laurentiu_lungu\Documents\Projects\PowerBI\MUC room utilization\RoomBookings.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Removed Columns1" = Table.RemoveColumns(#"Promoted Headers",{"Booking Duration"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns1","/",".",Replacer.ReplaceText,{"Start Date", "End Date"}),
    #"Changed Type with Locale" = Table.TransformColumnTypes(#"Replaced Value", {{"Start Date", type datetime}, {"End Date", type datetime}}, "de-DE"),
    #"Changed Type" = Table.TransformColumnTypes(#"Changed Type with Locale",{{"End Time", type time}, {"Start Time", type time}, {"Start Date", type date}, {"End Date", type date}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Changed Type",{"Start Date", "Start Time", "End Date", "End Time", "Floor", "Room"}),
    #"Added Conditional Column" = Table.AddColumn(#"Reordered Columns", "End Time Adj", each if [End Time] > EOB_Time then EOB_Time else [End Time]),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "Start Time Adj", 
each if [Start Time] < SOB_Time then SOB_Time 
else if [Start Time] > EOB_Time then EOB_Time else [Start Time]),
    #"Removed Columns" = Table.RemoveColumns(#"Added Conditional Column1",{"Start Time", "End Time"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Start Time Adj", "Start Time"}, {"End Time Adj", "End Time"}}),
    #"Reordered Columns1" = Table.ReorderColumns(#"Renamed Columns",{"Start Date", "Start Time", "End Date", "End Time", "Floor", "Room"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Reordered Columns1",{{"Start Date", Int64.Type}, {"End Date", Int64.Type}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type1", "Dates", each {[Start Date]..[End Date]}),
    #"Expanded Dates" = Table.ExpandListColumn(#"Added Custom", "Dates"),
    #"Changed Type2" = Table.TransformColumnTypes(#"Expanded Dates",{{"Start Date", type date}, {"End Date", type date}, {"Dates", type date}}),
    #"Added Conditional Column2" = Table.AddColumn(#"Changed Type2", "Duration", 
each if ([Start Date] = [Dates] and [End Date] = [Dates]) then Duration.TotalMinutes([End Time]-[Start Time]) 
else if ([Start Date] = [Dates] and [End Date] <> [Dates]) then Duration.TotalMinutes(#"EOB_Time"-[Start Time]) 
else if ([Start Date] <> [Dates] and [End Date] = [Dates]) then Duration.TotalMinutes([End Time]-#"SOB_Time")
else Duration.TotalMinutes(#"EOB_Time"-#"SOB_Time")),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Conditional Column2",{{"Duration", Int64.Type}})
in
    #"Changed Type3"
```


## Table: PublicHolidays


```m
let
    Source = Sql.Database("muc-mssql-2", "datahub", [Query="SELECT [location_code]#(lf)      ,[calendar_date]#(lf)      ,[description]#(lf)      ,[hours]#(lf)      ,[comment]#(lf)       FROM [datahub].[pub].[ll_location_public_holiday]#(lf)       where [location_code] ='MUC'", CreateNavigationProperties=false]),
    #"Removed Columns" = Table.RemoveColumns(Source,{"hours", "comment"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"calendar_date", type date}})
in
    #"Changed Type"
```


## Table: WorkdayDuration


```m
let
    Source = #table({"Duration"},{{Duration.TotalMinutes(#"EOB_Time"-#"SOB_Time")}}),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Duration", Int64.Type}})
in
    #"Changed Type"
```


## Table: AvailableDesks


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlLSUTI1VYrViVYyBjJNLMBMExDTDMw0BTFNwEwzEBOoNhYA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Floor = _t, TotalDesks = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Floor", Int64.Type}, {"TotalDesks", Int64.Type}})
in
    #"Changed Type"
```


## Table: DeskBookings


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\laurentiu_lungu\Documents\Projects\PowerBI\MUC room utilization\DeskreservierungMUC.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type with Locale" = Table.TransformColumnTypes(#"Promoted Headers", {{"Start Date", type datetime}}, "de-DE"),
    #"Parsed Date" = Table.TransformColumns(#"Changed Type with Locale",{{"Start Date", each Date.From(DateTimeZone.From(_)), type date}}),
    #"Removed Duplicates" = Table.Distinct(#"Parsed Date"),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Duplicates",{{"Floor", Int64.Type}})
in
    #"Changed Type"
```


## Table: AvailableDesksCorona


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlLSUTK2VIrViVYyBjJNzMFMExDTCMw0BTENwUwzENNYKTYWAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Floor = _t, TotalDesks = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Floor", Int64.Type}, {"TotalDesks", Int64.Type}})
in
    #"Changed Type"
```


## Table: DeskBookingsCorona


```m
let
    Source = Excel.Workbook(File.Contents("C:\Users\laurentiu_lungu\Documents\Projects\PowerBI\MUC room utilization\DeskreservierungMUC.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type with Locale" = Table.TransformColumnTypes(#"Promoted Headers", {{"Start Date", type datetime}}, "de-DE"),
    #"Parsed Date" = Table.TransformColumns(#"Changed Type with Locale",{{"Start Date", each Date.From(DateTimeZone.From(_)), type date}}),
    #"Removed Duplicates" = Table.Distinct(#"Parsed Date"),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Duplicates",{{"Floor", Int64.Type}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([Allocated to] <> " "))
in
    #"Filtered Rows"
```


## Parameter: EOB_Time


```m
#time(18, 0, 0) meta [IsParameterQuery=true, Type="Time", IsParameterQueryRequired=true]
```


## Parameter: SOB_Time


```m
#time(8, 0, 0) meta [IsParameterQuery=true, Type="Time", IsParameterQueryRequired=true]
```

