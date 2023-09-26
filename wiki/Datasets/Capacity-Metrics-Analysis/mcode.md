



# M Code

|Dataset|[Capacity Metrics Analysis](./../Capacity-Metrics-Analysis.md)|
| :--- | :--- |
|Workspace|[Premium Capacity Utilization And Metrics 22.12.2022 15:51:11](../../Workspaces/Premium-Capacity-Utilization-And-Metrics-22.12.2022-15:51:11.md)|

## Table: Operation Names


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("VZDNasMwEIRfZdE5hThp0vZosAOBhPz40ILJQZE3RKDIZiU57dtXXqhqHzXzza5m61qcAtKPmIlMXGa1KKSXDj0c7EuBD2kbOOON0N0jsWDia7/LoygbOHRI0uvWRm85SVfqjk0wOE6/MnFG2yDF5yoFbqZ9jrg1G/kWNsGqYTqUvTThb9Eb28dwNVrlnS6/u5Z81N9Zr8LVKdLdACfrg61NMCauGTQoH1IbGMPDAebMba2PteLmHtOELPuv/kna46R7tkhdYNc6B0fCHi3/vVKSkeW0bqEJlYd0+3icyy8=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [OperationName = _t, SortID = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"OperationName", type text}, {"SortID", Int64.Type}})
in
    #"Changed Type"
```


## Table: MAX_Memory_by_Artifact_and_10-minute


```m
let
    Source = fnGetData("MaxMemoryByArtifactAndTenMinutes"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: Interactive_CPU_by_Artifact_and_10-min


```m
let
   Source = fnGetData("InteractiveCpuByArtifactAndTenMinutes"),
   #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: Performance_by_Artifact_and_Hour


```m
let
    Source = fnGetData("PerformanceByArtifactAndHour"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: Metrics_by_Artifact_and_Operation_and_Hour


```m
let
    Source = fnGetData("MetricsByArtifactsAndOperationAndHour"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: Metrics_by_Artifact_and_Hour


```m
let
    Source = fnGetData("MetricsByArtifactsAndHour"),
   #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: Metrics_by_Artifact_and_Operation_and_Day


```m
let
    Source = fnGetData("MetricsByArtifactsAndOperationAndDay"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: All Measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", Int64.Type}})
in
    #"Changed Type"
```


## Table: Capacities


```m
let
    Source = try fnGetData("GetCapacities"),
    ValidateNoErros =
        if not (Source[HasError]) then
            Source[Value]
        else if Text.Contains(Source[Error][Message], "The column 'Column1' of the table wasn't found.") then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            error Source[Error][Message],
    SourceWithNull =
        if List.IsEmpty(ValidateNoErros[capacityId]) then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            ValidateNoErros,
    #"Filtered Rows" = Table.SelectRows(
        SourceWithNull,
        each ([sku] <> "PP3" and [sku] <> "SharedOnPremium")
    ),  // Handled for desktop mode                                                                                 
    #"reorderedColumns2" = Table.ReorderColumns(
        #"Filtered Rows",
        {
            "capacityId",
            "state",
            "source",
            "capacityPlan",
            "capacityNumberOfVCores",
            "capacityMemoryInGB",
            "o365AddonId",
            "region",
            "displayName",
            "sku",
            "creationDate",
            "Owners"
        }
    ),
    #"Renamed Columns" = Table.RenameColumns(reorderedColumns2, {{"displayName", "Capacity Name"}})
in
    #"Renamed Columns"
```


## Table: Metrics_by_Artifact_and_Day


```m
let
    Source = fnGetData("MetricsByArtifactAndDay"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: Performance_by_Hour


```m
let
    Source = fnGetData("PerformanceByHour"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"PremiumCapacityId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: MAX_Memory_by_Artifact_and_3-Hour


```m
let
    Source = fnGetData("MaxMemoryByArtifactAndThreeHour"),
   #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: MAX_Memory_by_Artifact


```m
let
    Source = fnGetData("MaxMemoryByArtifact"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: Utilization_by_Hour


```m
let
Source = fnGetData("UtilizationByHour")
in
    Source
```


## Table: Throttled_by_Artifact_and_Hour


```m
let
    Source = fnGetData("ThrottlerByArtifactAndHour"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: Throttler_by_Artifact_and_Hour


```m
let
    Source = fnGetData("ThrottledByArtifactAndHour"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: Throttling_by_Artifact


```m
let
    Source = fnGetData("ThrottlingByArtifacts"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: Failures_By_Utilization_Type


```m
let
   Source = fnGetData("FailuresByUtilizationType"),
   #"Uppercased Text" = Table.TransformColumns(Source,{{"WorkspaceId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: Metrics


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45Wcg4IVdJRMlSK1YlWciktSizJzM8DChiBBUKLU4uKgTxjMM87wBPEMQFz/AtSIYpBQqZKsbEA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Metric = _t, SortID = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Metric", type text}})
in
    #"Changed Type"
```


## Table: Artifacts


```m
let 
   Source = try fnGetData("GetCapacities"),
    ValidateNoErros =
        if not (Source[HasError]) then
            Source[Value]
        else if Text.Contains(Source[Error][Message], "The column 'Column1' of the table wasn't found.") then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            error Source[Error][Message],
    SourceWithNull =
        if List.IsEmpty(ValidateNoErros[capacityId]) then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            ValidateNoErros,
    #"Filtered Rows1" = Table.SelectRows(
        SourceWithNull,
        each ([sku] <> "PP3" and [sku] <> "SharedOnPremium")
    ),  // Handled for desktop mode    
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows1",{"capacityId"}),   
#"Invoked Custom Function" = Table.AddColumn(#"Removed Other Columns", "myCustomFunction",  each fnGetData("ArtifactsV2", [capacityId])),
#"Expanded myCustomFunction" = Table.ExpandTableColumn(#"Invoked Custom Function", "myCustomFunction", {"ArtifactId", "ArtifactKind", "ArtifactName", "dcount_Identity", "Timestamp", "WorkspaceId", "WorkspaceName"}, {"ArtifactId", "ArtifactKind", "ArtifactName", "dcount_Identity", "Timestamp", "WorkspaceId", "WorkspaceName"}),
    #"Uppercased Text1" = Table.TransformColumns(#"Expanded myCustomFunction",{{"WorkspaceId", Text.Upper, type text}}),   
#"Added Custom" = Table.AddColumn(#"Uppercased Text1", "Full ID", each [ArtifactName] & " \ " & [ArtifactKind] & " \ " & [WorkspaceName]),   
#"Uppercased Text" = Table.TransformColumns(#"Added Custom",{{"ArtifactId", Text.Upper, type text}}), 
#"Sorted Rows" = Table.Sort(#"Uppercased Text",{"Timestamp", Order.Descending}),    
#"Buffer" = Table.Buffer(#"Sorted Rows"),
#"Removed Duplicates" = Table.Distinct(#"Buffer", {"ArtifactId"}),    
#"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each [ArtifactId] <> null and [ArtifactId] <> ""),   
#"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"Full ID", "Artifact"}})
in   
#"Renamed Columns"
```


## Table: Performance_2day_Snapshot


```m
let
    Source = fnGetData("PerformanceTwoDaySnapshot"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: Refresh_by_Hour


```m
let
    Source = fnGetData("RefreshByHour"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: Metrics_All_Time


```m
let
Source = fnGetData("MetricsAllTime")
in
    Source
```


## Table: Performance_by_day


```m
let
    Source = fnGetData("PerformanceByDay"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: Refresh_Detail


```m
let
    Source = fnGetData("RefreshDetail"),
    #"Uppercased Text" = Table.TransformColumns(Source,{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: UtilizationTypes


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8swrSS1KTC7JLEtVitWJVnJKTM5OL8ovzUtRio0FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [UtilizationType = _t])
in
    Source
```


## Table: TimePoints


```m
let
    d = Date.AddDays(DateTime.From(DateTimeZone.UtcNow()),-20) ,
    d1 = #datetime(Date.Year(d),Date.Month(d),Date.Day(d),0,0,0),
    Source = List.DateTimes(d1, 20* 24* 60*4 , #duration(0, 0, 0, 30)),
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Renamed Columns" = Table.RenameColumns(#"Converted to Table",{{"Column1", "TimePoint"}}),
    #"Inserted Date" = Table.AddColumn(#"Renamed Columns", "Date", each DateTime.Date([TimePoint]), type date),
    #"Inserted Start of Hour" = Table.AddColumn(#"Inserted Date", "Start of Hour", each Time.StartOfHour([TimePoint]), type datetime),
    #"Added Custom" = Table.AddColumn(#"Inserted Start of Hour", "Next", each "Next"),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Previous", each "Previous"),
    #"Inserted Start of Hour1" = Table.AddColumn(#"Added Custom1", "15 Minute Bucket", each [TimePoint] + #duration(0,0,15- Number.Mod(Time.Minute([TimePoint]),15),0-Time.Second([TimePoint])))
in
    #"Inserted Start of Hour1"
```


## Table: TimePointBackgroundDetail


```m
let
Source = fnGetData("TimePointBackgroundDetail"),
r = Table.SelectRows(Source, each [WindowStartTime] <= TimePoint and [WindowEndTime] >= TimePoint),
    #"Changed Type" = Table.TransformColumnTypes(r,{{"CpuTimeMs", Currency.Type}, {"DurationMs", Currency.Type}, {"ThrottlingDelayMs", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Divided Column", {{"DurationMs", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"ThrottlingDelayMs", each _ / 1000, Currency.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Divided Column2",{{"CpuTimeMs", "Cpu (s)"}, {"DurationMs", "Duration (s)"}, {"ThrottlingDelayMs", "Throttling (s)"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"RandomGuid"}),
    #"Uppercased Text" = Table.TransformColumns(#"Removed Columns",{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: TimePointInteractiveDetail


```m
let
Source = fnGetData("TimePointInteractiveDetail"),
        t =TimePoint - #duration(0,0,0,30),
r = Table.SelectRows(Source, each [WindowStartTime] <= t and t <[WindowEndTime]),
    #"Changed Type" = Table.TransformColumnTypes(r,{{"CpuTimeMs", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Divided Column",{{"DurationMs", Currency.Type}, {"ThrottlingDelayMs", Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Changed Type1", {{"DurationMs", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"ThrottlingDelayMs", each _ / 1000, Currency.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Divided Column2",{{"CpuTimeMs", "CPU (s)"}, {"DurationMs", "Duration (s)"}, {"ThrottlingDelayMs", "Throttling (s)"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Custom", each Number.From([WindowEndTime]-[WindowStartTime])/300000000 ),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"Custom", "TimePoints"}}),
    #"Added Custom1" = Table.AddColumn(#"Renamed Columns1", "New CPU (s)", each [#"CPU (s)"] / [TimePoints]),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom1",{{"TimePoints", Int64.Type}, {"New CPU (s)", Currency.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type2",{"RandomGuid"}),
    #"Uppercased Text" = Table.TransformColumns(#"Removed Columns",{{"ArtifactId", Text.Upper, type text}})
in 
    #"Uppercased Text"
```


## Table: TimePointCPUDetail


```m
let
Source = fnGetData("TimePointCPUDetail"),
    #"Changed Type1" = Table.TransformColumnTypes(Source,{{"WindowStartTime", type datetime}, {"WindowEndTime", type datetime}}),
        begintime= TimePoint - #duration(0,0,30,0),
        endtime = TimePoint +  #duration(0,0,30,0),
r = Table.SelectRows(#"Changed Type1", each [WindowStartTime] >= begintime and endtime > [WindowEndTime]),
    #"Changed Type" = Table.TransformColumnTypes(r,{{"CpuTimeMs", Currency.Type}, {"Interactive", Currency.Type}, {"Background", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Divided Column", {{"Interactive", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"Background", each _ / 1000, Currency.Type}})

in
    #"Divided Column2"
```


## Table: TimePointCPUDetail2


```m
let
Source = fnGetData("TimePointCPUDetail"),
    #"Changed Type1" = Table.TransformColumnTypes(Source,{{"WindowStartTime", type datetime}, {"WindowEndTime", type datetime}}),
        // begintime= TimePoint - #duration(0,0,30,0),
        // endtime = TimePoint +  #duration(0,0,30,0),
//r = Table.SelectRows(#"Changed Type1", each [WindowStartTime] >= begintime and endtime > [WindowEndTime]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"CpuTimeMs", Currency.Type}, {"Interactive", Currency.Type}, {"Background", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Divided Column", {{"Interactive", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"Background", each _ / 1000, Currency.Type}}),
    #"Inserted Start of Hour" = Table.AddColumn(#"Divided Column2", "Start of Hour", each Time.StartOfHour([WindowStartTime]), type datetimezone),
    #"Added Custom" = Table.AddColumn(#"Inserted Start of Hour", "Custom", each [PeakHourInteractive] + [PeakHourBackground]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"Custom", "PeakHourInteractiveAndBackground"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns",0,null,Replacer.ReplaceValue,{"PeakHourInteractive"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",0,null,Replacer.ReplaceValue,{"PeakHourBackground"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1",0,null,Replacer.ReplaceValue,{"PeakHourInteractiveAndBackground"})

in
    #"Replaced Value2"
```


## Table: Refresh Status


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCi5NTk4tLlaK1YlWckvMzCktSlWKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Status = _t])
in
    Source
```


## Table: Metrics_by_7_day


```m
let 
   Source = try fnGetData("GetCapacities"),
    ValidateNoErros =
        if not (Source[HasError]) then
            Source[Value]
        else if Text.Contains(Source[Error][Message], "The column 'Column1' of the table wasn't found.") then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            error Source[Error][Message],
    SourceWithNull =
        if List.IsEmpty(ValidateNoErros[capacityId]) then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            ValidateNoErros,
    #"Filtered Rows" = Table.SelectRows(
        SourceWithNull,
        each ([sku] <> "PP3" and [sku] <> "SharedOnPremium")
    ),  // Handled for desktop mode    
   #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"capacityId"}),
    #"Invoked Custom Function" = Table.AddColumn(#"Removed Other Columns", "fnGetMetricsBy7Day", each fnGetData("MetricsBySevenDays", [capacityId])),
    #"Expanded fnGetMetricsBy7Day" = Table.ExpandTableColumn(#"Invoked Custom Function", "fnGetMetricsBy7Day", {"Weekly_Bucket", "cpu", "duration", "active_users", "active_artifacts", "PremiumCapacityId", "max_cores"}, {"Weekly_Bucket", "cpu", "duration", "active_users", "active_artifacts", "PremiumCapacityId", "max_cores"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded fnGetMetricsBy7Day",{{"cpu", Int64.Type}, {"duration", Int64.Type}, {"active_users", Int64.Type}, {"active_artifacts", Int64.Type}, {"max_cores", Int64.Type}, {"Weekly_Bucket", Int64.Type}})
in
    #"Changed Type"
```


## Table: Metrics_by_Artifact


```m
let 
   Source = try fnGetData("GetCapacities"),
    ValidateNoErros =
        if not (Source[HasError]) then
            Source[Value]
        else if Text.Contains(Source[Error][Message], "The column 'Column1' of the table wasn't found.") then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            error Source[Error][Message],
    SourceWithNull =
        if List.IsEmpty(ValidateNoErros[capacityId]) then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            ValidateNoErros,
    #"Filtered Rows" = Table.SelectRows(
        SourceWithNull,
        each ([sku] <> "PP3" and [sku] <> "SharedOnPremium")
    ),  // Handled for desktop mode    
   #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"capacityId"}),
    #"Invoked Custom Function" = Table.AddColumn(#"Removed Other Columns", "fnGetMetricsByArtifact",  each fnGetData("MetricsByArtifacts", [capacityId])),// each fnGetMetricsByArtifact([capacityId], UTC_offset)),
    #"Expanded fnGetMetricsByArtifact" = Table.ExpandTableColumn(#"Invoked Custom Function", "fnGetMetricsByArtifact", {"PremiumCapacityId", "ArtifactId", "sum_cpu", "sum_duration", "count_operations", "count_users", "percentile_DurationMs_50", "percentile_DurationMs_90", "avg_DurationMs"}, {"PremiumCapacityId", "ArtifactId", "sum_cpu", "sum_duration", "count_operations", "count_users", "percentile_DurationMs_50", "percentile_DurationMs_90", "avg_DurationMs"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded fnGetMetricsByArtifact",{"capacityId"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"sum_cpu", Int64.Type}, {"sum_duration", Int64.Type}, {"count_operations", Int64.Type}, {"count_users", Int64.Type}, {"percentile_DurationMs_50", Int64.Type}, {"percentile_DurationMs_90", Int64.Type}, {"avg_DurationMs", Int64.Type}}),
     #"Uppercased Text" = Table.TransformColumns(#"Changed Type",{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: Metrics_by_Artifact_and_Operation


```m
let 
   Source = try fnGetData("GetCapacities"),
    ValidateNoErros =
        if not (Source[HasError]) then
            Source[Value]
        else if Text.Contains(Source[Error][Message], "The column 'Column1' of the table wasn't found.") then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            error Source[Error][Message],
    SourceWithNull =
        if List.IsEmpty(ValidateNoErros[capacityId]) then
            error
                "No capacities found. You need to be a capacity admin of at least one or more capacities."
        else
            ValidateNoErros,
    #"Filtered Rows" = Table.SelectRows(
        SourceWithNull,
        each ([sku] <> "PP3" and [sku] <> "SharedOnPremium")
    ),  // Handled for desktop mode    
 #"Removed Other Columns" = Table.SelectColumns(SourceWithNull,{"capacityId"}),
    #"Invoked Custom Function" = Table.AddColumn(#"Removed Other Columns", "fnGetMetricsByArtifactAndOperation",  each fnGetData("MetricsByArtifactAndOperation", [capacityId])),//, each fnGetMetricsByArtifactAndOperation([capacityId], "0")),
    #"Expanded fnGetMetricsByArtifactAndOperation" = Table.ExpandTableColumn(#"Invoked Custom Function", "fnGetMetricsByArtifactAndOperation", {"OperationName", "PremiumCapacityId", "ArtifactId", "sum_cpu", "sum_duration", "count_operations", "count_users", "percentile_DurationMs_50", "percentile_DurationMs_90", "avg_DurationMs"}, {"OperationName", "PremiumCapacityId", "ArtifactId", "sum_cpu", "sum_duration", "count_operations", "count_users", "percentile_DurationMs_50", "percentile_DurationMs_90", "avg_DurationMs"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded fnGetMetricsByArtifactAndOperation",{"capacityId"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"sum_cpu", Int64.Type}, {"sum_duration", Int64.Type}, {"count_operations", Int64.Type}, {"count_users", Int64.Type}, {"percentile_DurationMs_50", Int64.Type}, {"percentile_DurationMs_90", Int64.Type}, {"avg_DurationMs", Int64.Type}}),
     #"Uppercased Text" = Table.TransformColumns(#"Changed Type",{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: TimePointBackgroundDetail (2)


```m
let
Source = fnGetData("TimePointBackgroundDetail"),
r = Table.SelectRows(Source, each [WindowStartTime] <= #"TimePoint2" and [WindowEndTime] >= #"TimePoint2"),
    #"Changed Type" = Table.TransformColumnTypes(r,{{"CpuTimeMs", Currency.Type}, {"DurationMs", Currency.Type}, {"ThrottlingDelayMs", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Divided Column", {{"DurationMs", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"ThrottlingDelayMs", each _ / 1000, Currency.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Divided Column2",{{"CpuTimeMs", "Cpu (s)"}, {"DurationMs", "Duration (s)"}, {"ThrottlingDelayMs", "Throttling (s)"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"RandomGuid"}),
      #"Uppercased Text" = Table.TransformColumns(#"Removed Columns",{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: TimePointInteractiveDetail (2)


```m
let
Source = fnGetData("TimePointInteractiveDetail"),
        t =#"TimePoint2" - #duration(0,0,0,30),
r = Table.SelectRows(Source, each [WindowStartTime] <= t and t <[WindowEndTime]),
    #"Changed Type" = Table.TransformColumnTypes(r,{{"CpuTimeMs", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Divided Column",{{"DurationMs", Currency.Type}, {"ThrottlingDelayMs", Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Changed Type1", {{"DurationMs", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"ThrottlingDelayMs", each _ / 1000, Currency.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Divided Column2",{{"CpuTimeMs", "CPU (s)"}, {"DurationMs", "Duration (s)"}, {"ThrottlingDelayMs", "Throttling (s)"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Custom", each Number.From([WindowEndTime]-[WindowStartTime])/300000000 ),
    #"Renamed Columns1" = Table.RenameColumns(#"Added Custom",{{"Custom", "TimePoints"}}),
    #"Added Custom1" = Table.AddColumn(#"Renamed Columns1", "New CPU (s)", each [#"CPU (s)"] / [TimePoints]),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom1",{{"TimePoints", Int64.Type}, {"New CPU (s)", Currency.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type2",{"RandomGuid"}),
     #"Uppercased Text" = Table.TransformColumns(#"Removed Columns",{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: TimePoints2


```m
let
    d = Date.AddDays(DateTime.From(DateTimeZone.UtcNow()),-20) ,
    d1 = #datetime(Date.Year(d),Date.Month(d),Date.Day(d),0,0,0),
    Source = List.DateTimes(d1, 20* 24* 60*4 , #duration(0, 0, 0, 30)),
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Renamed Columns" = Table.RenameColumns(#"Converted to Table",{{"Column1", "TimePoint"}}),
    #"Inserted Date" = Table.AddColumn(#"Renamed Columns", "Date", each DateTime.Date([TimePoint]), type date),
    #"Inserted Start of Hour" = Table.AddColumn(#"Inserted Date", "Start of Hour", each Time.StartOfHour([TimePoint]), type datetime),
    #"Changed Type" = Table.TransformColumnTypes(#"Inserted Start of Hour",{{"TimePoint", type datetime}})
in
    #"Changed Type"
```


## Table: TimePointCPUDetail (2)


```m
let
Source =  fnGetData("TimePointCPUDetail"),
    #"Changed Type1" = Table.TransformColumnTypes(Source,{{"WindowStartTime", type datetime}, {"WindowEndTime", type datetime}}),
        begintime= #"TimePoint2" - #duration(0,0,30,0),
        endtime = #"TimePoint2" +  #duration(0,0,30,0),
r = Table.SelectRows(#"Changed Type1", each [WindowStartTime] >= begintime and endtime > [WindowEndTime]),
    #"Changed Type" = Table.TransformColumnTypes(r,{{"CpuTimeMs", Currency.Type}, {"Interactive", Currency.Type}, {"Background", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Divided Column", {{"Interactive", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"Background", each _ / 1000, Currency.Type}}),
    #"Added Custom" = Table.AddColumn(#"Divided Column2", "Custom", each [PeakHourInteractive] + [PeakHourBackground]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"Custom", "PeakHourInteractiveAndBackground"}})

in
    #"Renamed Columns"
```


## Table: TimePointInteractiveDetail_nf


```m
let
Source = fnGetData("TimePointInteractiveDetail"),
        t =TimePoint - #duration(0,0,0,30),
r = Table.SelectRows(Source, each [WindowStartTime] <= t and t <[WindowEndTime]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"CpuTimeMs", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Divided Column",{{"DurationMs", Currency.Type}, {"ThrottlingDelayMs", Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Changed Type1", {{"DurationMs", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"ThrottlingDelayMs", each _ / 1000, Currency.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Divided Column2",{{"CpuTimeMs", "CPU (s)"}, {"DurationMs", "Duration (s)"}, {"ThrottlingDelayMs", "Throttling (s)"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"RandomGuid"}),
    #"Uppercased Text" = Table.TransformColumns(#"Removed Columns",{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Table: TimePointBackgroundDetail_nf


```m
let
Source = fnGetData("TimePointBackgroundDetail"),
r = Table.SelectRows(Source, each [WindowStartTime] <= TimePoint and [WindowEndTime] >= TimePoint),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"CpuTimeMs", Currency.Type}, {"DurationMs", Currency.Type}, {"ThrottlingDelayMs", Currency.Type}}),
    #"Divided Column" = Table.TransformColumns(#"Changed Type", {{"CpuTimeMs", each _ / 1000, Currency.Type}}),
    #"Divided Column1" = Table.TransformColumns(#"Divided Column", {{"DurationMs", each _ / 1000, Currency.Type}}),
    #"Divided Column2" = Table.TransformColumns(#"Divided Column1", {{"ThrottlingDelayMs", each _ / 1000, Currency.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Divided Column2",{{"CpuTimeMs", "Cpu (s)"}, {"DurationMs", "Duration (s)"}, {"ThrottlingDelayMs", "Throttling (s)"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"RandomGuid"}),
    #"Uppercased Text" = Table.TransformColumns(#"Removed Columns",{{"ArtifactId", Text.Upper, type text}})
in
    #"Uppercased Text"
```


## Parameter: CapacityID


```m
"A58B8154-A5DA-44CC-BC2E-3DCB22F05DD0" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Parameter: UTC_offset


```m
"+1" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```


## Parameter: TimePoint


```m
#datetime(2021, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
```


## Parameter: TimePoint2


```m
#datetime(2021, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
```

