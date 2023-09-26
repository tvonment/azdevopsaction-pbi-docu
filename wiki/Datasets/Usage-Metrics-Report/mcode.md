



# M Code

|Dataset|[Usage Metrics Report](./../Usage-Metrics-Report.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: Report views


```m
let
    Source = UsageMetricsDataConnector.GetMetricsData(BaseUrl & "/metadata/v201906/metrics/workspace/" & WorkspaceId & "/reportviews"),
    metricsTable = Table.FromRecords(Source),
    checkForEmptyTable = if Table.IsEmpty(metricsTable) then
                        Table.FromRows
                        (
                            {
                            },
                            {
                                "ReportId", "ReportType", "ReportName", "AppName", "UserKey", "UserId", "UserAgent", "DatasetName", "DistributionMethod", "CapacityId", "CapacityName", "CreationTime", "ConsumptionMethod"
                            }
                        )
                        else
                        metricsTable,
    finalTable = Table.TransformColumnTypes(checkForEmptyTable, {{"CreationTime", type datetime}}),
    #"Renamed Columns" = Table.RenameColumns(finalTable,{{"ConsumptionMethod", "OriginalConsumptionMethod"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","Apps","App",Replacer.ReplaceText,{"DistributionMethod"})
in
    #"Replaced Value"
```


## Table: Model measures


```m
let
    Source = Table.FromList({}),
    AddWorkspaceId = Table.AddColumn(Source, "WorkspaceId", each WorkspaceId),
    AddBaseUrl = Table.AddColumn(AddWorkspaceId, "BaseUrl", each BaseUrl),
    #"Removed Columns" = Table.RemoveColumns(AddBaseUrl,{"WorkspaceId", "BaseUrl"})
in
    #"Removed Columns"
```


## Table: Report rank


```m
let
    Source = UsageMetricsDataConnector.GetMetricsData(BaseUrl & "/metadata/v201906/metrics/workspace/" & WorkspaceId & "/reportrank"),
    metricsTable = Table.FromRecords(Source),
    checkForEmptyTable = if Table.IsEmpty(metricsTable) then
                            Table.FromRows
                            (
                                {
                                },
                                {
                                    "ReportId", "WorkspaceId", "ReportViewCount", "ReportRank", "TotalReportCount", "TenantId"
                                }
                            )
                         else
                            metricsTable,
    finalTable = Table.TransformColumnTypes(checkForEmptyTable,{{"ReportRank", Int64.Type}, {"TotalReportCount", Int64.Type}, {"ReportViewCount", Int64.Type}})
in
    finalTable
```


## Table: Report page views


```m
let
    Source = UsageMetricsDataConnector.GetMetricsData(BaseUrl & "/metadata/v201906/metrics/workspace/" & WorkspaceId & "/reportpagesectionviews"),
    #"metricsTable" = Table.FromRecords(Source),
    checkForEmptyTable = if Table.IsEmpty(#"metricsTable") then
                            Table.FromRows
                            (
                                {
                                },
                                {
                                    "Timestamp", "PbiCluster", "AppName", "TenantId", "UserId", "ReportId", "OriginalReportId", "GroupId", "OriginalGroupId", "AppGuid", "SectionId", "Client", "SessionSource", "DeviceOSVersion", "DeviceBrowserVersion", "UserKey"
                                }
                            )
                         else
                            #"metricsTable",
    #"Removed Columns" = Table.RemoveColumns(checkForEmptyTable,{"PbiCluster"}),
    finalTable = Table.TransformColumnTypes(#"Removed Columns", {{"Timestamp", type datetime}}),
    #"Renamed Columns" = Table.RenameColumns(finalTable,{{"GroupId", "WorkspaceId"}, {"OriginalGroupId", "OriginalWorkspaceId"}})
in
    #"Renamed Columns"
```


## Table: Report load times


```m
let 
    Source = UsageMetricsDataConnector.GetMetricsData(BaseUrl & "/metadata/v201906/metrics/workspace/" & WorkspaceId & "/reportloads"),
    metricsTable = Table.FromRecords(Source),
    checkForEmptyTable = if Table.IsEmpty(metricsTable) then
                            Table.FromRows
                            (
                                {
                                },
                                {
                                    "AppGuid","AppName","Client","DeviceBrowserVersion","DeviceOSVersion","EndTime","GroupId","LocationCity","LocationCountry","OriginalGroupId","OriginalReportId","PbiCluster","ReportId","StartTime","TenantId","Timestamp","UserId","SessionSource"
                                }
                            )
                         else
                            metricsTable,
    finalTable = Table.TransformColumnTypes(checkForEmptyTable, {{"Timestamp", type datetimezone}, {"StartTime", type datetimezone}, {"EndTime", type datetimezone}}),
    #"Renamed Columns" = Table.RenameColumns(finalTable,{{"LocationCountry", "Country"}})
in
    #"Renamed Columns"
```


## Table: Report pages


```m
let
    Source = UsageMetricsDataConnector.GetMetricsData(BaseUrl & "/metadata/v201906/metrics/workspace/" & WorkspaceId & "/reportpagesectionmetadata"),
    #"metricsTable" = Table.FromRecords(Source),
    checkForEmptyTable = if Table.IsEmpty(#"metricsTable") then
                            Table.FromRows
                            (
                                {
                                },
                                {
                                    "ReportId", "SectionId", "SectionName", "WorkspaceId"
                                }
                            )
                         else
                            #"metricsTable",
    #"Filtered Rows1" = Table.SelectRows(checkForEmptyTable, each ([SectionId] <> null)),
    #"Filtered Rows" = Table.SelectRows(#"Filtered Rows1", each ([ReportId] <> null))
in
    #"Filtered Rows"
```


## Table: Reports


```m
let
    Source = UsageMetricsDataConnector.GetMetricsData(BaseUrl & "/metadata/v201906/metrics/workspace/" & WorkspaceId & "/reportmetadata"),
    #"metricsTable" = Table.FromRecords(Source),
    checkForEmptyTable = if Table.IsEmpty(metricsTable) then
                            Table.FromRows
                            (
                                {
                                },
                                {
                                    "OrganizationId", "ReportId", "ReportName", "WorkspaceId", "IsUsageMetricsReport"
                                }
                            )
                         else
                            metricsTable,
    #"Filtered Rows" = Table.SelectRows(checkForEmptyTable, each [ReportId] <> null and [ReportId] <> ""),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows",{{"ReportId", "ReportGuid"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"IsUsageMetricsReport", type logical}})
in
    #"Changed Type"
```


## Table: Refresh Stats


```m
let
    Source = DateTime.LocalNow() // DateTime.LocalNow()
,
    #"Converted to Table" = #table(1, {{Source}}),
    #"Renamed Columns" = Table.RenameColumns(#"Converted to Table",{{"Column1", "Last Refresh"}})
in
    #"Renamed Columns"
```


## Parameter: WorkspaceId


```m
"db7b74ff-7568-48d5-a6bb-77c4b871daf2" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=false]
```


## Parameter: BaseUrl


```m
"https://WABI-NORTH-EUROPE-redirect.analysis.windows.net" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

