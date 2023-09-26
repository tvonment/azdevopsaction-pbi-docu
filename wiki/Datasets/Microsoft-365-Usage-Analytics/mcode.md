



# M Code

|Dataset|[Microsoft 365 Usage Analytics](./../Microsoft-365-Usage-Analytics.md)|
| :--- | :--- |
|Workspace|[Microsoft 365 Usage Analytics](../../Workspaces/Microsoft-365-Usage-Analytics.md)|

## Table: TenantClientUsage


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantClientUsage_table = Source{[Name="TenantClientUsage",Signature="table"]}[Data]
in
    TenantClientUsage_table
```


## Table: TenantMailboxUsage


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantMailboxUsage_table = Source{[Name="TenantMailboxUsage",Signature="table"]}[Data]
in
    TenantMailboxUsage_table
```


## Table: TenantOfficeActivation


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantOfficeActivation_table = Source{[Name="TenantOfficeActivation",Signature="table"]}[Data],
    #"Expanded ServicePlans" = Table.ExpandListColumn(TenantOfficeActivation_table, "ServicePlans"),
    #"Expanded ServicePlans1" = Table.ExpandRecordColumn(#"Expanded ServicePlans", "ServicePlans", {"ServicePlanName", "TotalEnabled", "TotalActivated", "TotalCount", "AndroidCount", "iOSCount", "MacCount", "PcCount", "WinRtCount"}, {"ServicePlanName", "TotalEnabled", "TotalActivated", "TotalCount", "AndroidCount", "iOSCount", "MacCount", "PcCount", "WinRtCount"}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Expanded ServicePlans1", "Licenses", "Licenses - Copy"),
    #"Removed Columns" = Table.RemoveColumns(#"Duplicated Column",{"Licenses - Copy", "Licenses"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"TotalCount", "TotalActivations"}, {"TotalActivated", "TotalActivatedUsers"}})
in
    #"Renamed Columns"
```


## Table: TenantOneDriveUsage


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantOneDriveUsage_table = Source{[Name="TenantOneDriveUsage",Signature="table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(TenantOneDriveUsage_table,{{"DiskQuota", Int64.Type}})
in
    #"Changed Type"
```


## Table: TenantProductActivity


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantProductActivity_table = Source{[Name="TenantProductActivity",Signature="table"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(TenantProductActivity_table,{{"UserCount", "ActiveUserCount"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"TimeFrame", type date}}),
    #"Replaced Sum/Org" = Table.ReplaceValue(#"Changed Type","Summary/OrganizeConference","Summary/Conference Organizer",Replacer.ReplaceText,{"Activity"}),
    #"Replace Sum/P2P" = Table.ReplaceValue(#"Replaced Sum/Org","Summary/PeerSession","Summary/Peer-to-Peer",Replacer.ReplaceText,{"Activity"}),
    #"Replaced Sum/Part" = Table.ReplaceValue(#"Replace Sum/P2P","Summary/ParticipateConference","Summary/Conference Participant",Replacer.ReplaceText,{"Activity"})
in
    #"Replaced Sum/Part"
```


## Table: TenantProductUsage


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantProductUsage_table = Source{[Name="TenantProductUsage",Signature="table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(TenantProductUsage_table,{{"TimeFrame", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"LicensedUsers", "EnabledUsers"}, {"MOMReturningUsers", "MoMReturningUsers"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"TimeFrame", type date}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type1",{{"ActiveUsers", "Active Users"}, {"EnabledUsers", "Enabled Users"}})
in
    #"Renamed Columns1"
```


## Table: TenantSharePointUsage


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantSharePointUsage_table = Source{[Name="TenantSharePointUsage",Signature="table"]}[Data]
in
    TenantSharePointUsage_table
```


## Table: UserActivity


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    UserActivity_table = Source{[Name="UserActivity",Signature="table"]}[Data]
in
    UserActivity_table
```


## Table: UserState


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    UserState_table = Source{[Name="UserState",Signature="table"]}[Data]
in
    UserState_table
```


## Table: TenantOfficeLicenses


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantOfficeActivation_table = Source{[Name="TenantOfficeActivation",Signature="table"]}[Data],
    #"Expanded Licenses" = Table.ExpandListColumn(TenantOfficeActivation_table, "Licenses"),
    #"Expanded Licenses1" = Table.ExpandRecordColumn(#"Expanded Licenses", "Licenses", {"LicenseName", "AssignedCount"}, {"LicenseName", "AssignedCount"}),
    #"Removed Other Columns" = Table.SelectColumns(#"Expanded Licenses1",{"TimeFrame", "LicenseName", "AssignedCount"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Other Columns",{{"TimeFrame", type date}}),
	
    TenantOfficeActivation_table_1 = Source{[Name="TenantOfficeActivation",Signature="table"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(TenantOfficeActivation_table_1,{"ServicePlans"}),
    #"Expanded Licenses2" = Table.ExpandListColumn(#"Removed Columns", "Licenses"),
    #"Expanded Licenses3" = Table.ExpandRecordColumn(#"Expanded Licenses2", "Licenses", {"LicenseName", "AssignedCount"}, {"Licenses.LicenseName", "Licenses.AssignedCount"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Expanded Licenses3",{"TimeFrame", "Licenses.LicenseName", "Licenses.AssignedCount", "ContentDate"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Reordered Columns",{"ContentDate"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns1",{{"Licenses.LicenseName", "LicenseName"}, {"Licenses.AssignedCount", "AssignedCount"}}),
	#"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each ([LicenseName] = "Any")),
	#"Pivoted Column" = Table.Pivot(#"Filtered Rows", List.Distinct(#"Filtered Rows"[LicenseName]), "LicenseName", "AssignedCount", List.Sum),
    #"Renamed Columns1" = Table.RenameColumns(#"Pivoted Column",{{"Any", "AssignedLicense"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns1",{{"TimeFrame", type date}}),
	
	#"Merged Queries" = Table.NestedJoin(#"Changed Type",{"TimeFrame"},#"Changed Type1" ,{"TimeFrame"},"NewColumn",JoinKind.LeftOuter),
    #"Expanded NewColumn1" = Table.ExpandTableColumn(#"Merged Queries", "NewColumn", {"AssignedLicense"}, {"NewColumn.AssignedLicense"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Expanded NewColumn1",{{"NewColumn.AssignedLicense", "AssignedLicense"}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Renamed Columns2",{{"AssignedLicense", type text}, {"AssignedCount", Int64.Type}})
in
    #"Changed Type2"
```


## Table: SPO-UserActivity


```m
let
    Source = UserActivity,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"TimeFrame", "UserId", "SPO_TeamFileViewedModified", "SPO_TeamFileSynched", "SPO_TeamFileSharedInternally", "SPO_TeamFileSharedExternally", "SPO_TeamAccessedByOwner", "SPO_TeamAccessedByOthers", "SPO_GroupFileViewedModified", "SPO_GroupFileSynched", "SPO_GroupFileSharedInternally", "SPO_GroupFileSharedExternally", "SPO_GroupAccessedByOwner", "SPO_GroupAccessedByOthers"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Other Columns", {"TimeFrame", "UserId"}, "Attribute", "Value"),
    #"Changed Type" = Table.TransformColumnTypes(#"Unpivoted Columns",{{"Value", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Attribute", "Activity"}, {"Value", "Count"}})
in
    #"Renamed Columns"
```


## Table: TenantOneDrive-Activity


```m
let
    Source = TenantOneDriveUsage,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"SiteType", "ActivityType", "ActivityTotalSites", "SitesWithOwnerActivities", "SitesWithNonOwnerActivities", "TimeFrame", "ContentDate"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Other Columns",{{"TimeFrame", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"ActivityTotalSites", "ActivityTotalAccounts"}, {"SiteType", "Product"}, {"SitesWithNonOwnerActivities", "ODB-CollaboratedbyOthers"}, {"SitesWithOwnerActivities", "ODB-CollaboratedbyOwner"}})
in
    #"Renamed Columns"
```


## Table: TenantOneDrive-Usage


```m
let
    Source = TenantOneDriveUsage,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"SiteType", "DiskUsed", "DiskQuota", "DocumentCount", "TotalSites", "TimeFrame", "ContentDate"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates",{{"SiteType", "Product"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"TimeFrame", type date}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type",{{"TotalSites", "TotalAccounts"}})
in
    #"Renamed Columns1"
```


## Table: TenantSharePoint-Activity


```m
let
    Source = TenantSharePointUsage,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"SiteType", "ActivityType", "ActivityTotalSites", "SitesWithOwnerActivities", "SitesWithNonOwnerActivities", "TimeFrame", "ContentDate"}),
    #"Added Custom" = Table.AddColumn(#"Removed Other Columns", "Product", each "SharePoint"),
    #"Reordered Columns" = Table.ReorderColumns(#"Added Custom",{"TimeFrame", "Product", "SiteType", "ActivityType", "ActivityTotalSites", "SitesWithOwnerActivities", "SitesWithNonOwnerActivities"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Reordered Columns",{{"TimeFrame", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"SitesWithOwnerActivities", "SPO-CollaboratedbyOwner"}, {"SitesWithNonOwnerActivities", "SPO-CollaboratedbyOthers"}})
in
    #"Renamed Columns"
```


## Table: TenantSharePoint-Usage


```m
let
    Source = TenantSharePointUsage,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"SiteType", "DiskUsed", "DiskQuota", "DocumentCount", "TotalSites", "TimeFrame", "ContentDate"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Duplicates",{{"TimeFrame", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"TotalSites", "TotalSites"}})
in
    #"Renamed Columns"
```


## Table: ODBActive-Sites/Users/Docs


```m
let
    Source = #"TenantOneDrive-Activity",
    #"Filtered Rows" = Table.SelectRows(Source, each Text.Contains([ActivityType], "Any")),
    #"Removed Other Columns1" = Table.SelectColumns(#"Filtered Rows",{"Product", "ActivityType", "ActivityTotalAccounts", "TimeFrame", "ContentDate"}),
    TenantProductUsage_table = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]){[Name="TenantProductUsage",Signature="table"]}[Data],
    Change_TimeFrametype_to_Date = Table.TransformColumnTypes(TenantProductUsage_table,{{"TimeFrame", type date}}),
    #"Renamed Columns1" = Table.RenameColumns(Change_TimeFrametype_to_Date,{{"LicensedUsers", "EnabledUsers"}, {"MOMReturningUsers", "MoMReturningUsers"}}),
    Merge_OneDriveActivity_ProductUsage = Table.NestedJoin(#"Removed Other Columns1",{"Product", "TimeFrame"},#"Renamed Columns1",{"Product", "TimeFrame"},"NewColumn",JoinKind.Inner),
    #"Expanded NewColumn" = Table.ExpandTableColumn(Merge_OneDriveActivity_ProductUsage, "NewColumn", {"EnabledUsers", "ActiveUsers"}, {"NewColumn.EnabledUsers", "NewColumn.ActiveUsers"}),
   
    TenantOneDriveUsage_table = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]){[Name="TenantOneDriveUsage",Signature="table"]}[Data],
    #"Removed Other Columns2" = Table.SelectColumns(TenantOneDriveUsage_table ,{"SiteType", "DiskUsed", "DocumentCount", "TotalSites", "TimeFrame", "ContentDate"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns2"),
    #"Renamed Columns2" = Table.RenameColumns(#"Removed Duplicates",{{"SiteType", "Product"}, {"TotalSites", "TotalAccounts"}}),
    #"Changed Type3" = Table.TransformColumnTypes(#"Renamed Columns2",{{"TimeFrame", type date}}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded NewColumn",{"Product", "TimeFrame"},#"Changed Type3",{"Product", "TimeFrame"},"NewColumn",JoinKind.Inner),
    #"Expanded NewColumn1" = Table.ExpandTableColumn(#"Merged Queries1", "NewColumn", {"DocumentCount", "TotalAccounts"}, {"DocumentCount", "TotalAccounts"}),
   
    TenantProductActivity_table = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]){[Name="TenantProductActivity",Signature="table"]}[Data],
    #"Renamed Columns4" = Table.RenameColumns(TenantProductActivity_table,{{"UserCount", "ActiveUserCount"}}),
    #"Changed Type4" = Table.TransformColumnTypes(#"Renamed Columns4",{{"TimeFrame", type date}}),
    #"Replaced Sum/Org" = Table.ReplaceValue(#"Changed Type4","Summary/OrganizeConference","Summary/Conference Organizer",Replacer.ReplaceText,{"Activity"}),
    #"Replace Sum/P2P" = Table.ReplaceValue(#"Replaced Sum/Org","Summary/PeerSession","Summary/Peer-to-Peer",Replacer.ReplaceText,{"Activity"}),
    #"Replaced Sum/Part" = Table.ReplaceValue(#"Replace Sum/P2P","Summary/ParticipateConference","Summary/Conference Participant",Replacer.ReplaceText,{"Activity"}),
    #"Merged Queries2" = Table.NestedJoin(#"Expanded NewColumn1",{"ActivityType", "Product", "TimeFrame"},#"Replaced Sum/Part",{"Activity", "Product", "TimeFrame"},"NewColumn",JoinKind.Inner),
    #"Expanded NewColumn2" = Table.ExpandTableColumn(#"Merged Queries2", "NewColumn", {"ActivityCount"}, {"ActivityCount"}),
    #"Renamed Columns5" = Table.RenameColumns(#"Expanded NewColumn2",{{"NewColumn.EnabledUsers", "EnabledUsers"}, {"NewColumn.ActiveUsers", "ActiveUsers"}, {"ActivityCount", "ActiveFiles"}, {"TotalAccounts", "TotalSites"}, {"ActivityTotalAccounts", "ActiveSites"}, {"DocumentCount", "TotalFiles"}})
in
    #"Renamed Columns5"
```


## Table: SPO-SiteType


```m
let
    Source = TenantSharePointUsage,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"SiteType"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Sorted Rows" = Table.Sort(#"Removed Duplicates",{{"SiteType", Order.Ascending}})
in
    #"Sorted Rows"
```


## Table: SPOActive-Sites/Users/Docs


```m
let
    Source = #"TenantSharePoint-Activity",
    #"Filtered Rows2" = Table.SelectRows(Source, each Text.Contains([ActivityType], "Any")),
    #"Added Custom" = Table.AddColumn(#"Filtered Rows2", "SiteActivityType", each [SiteType] & "/" & [ActivityType]),
    #"Reordered Columns" = Table.ReorderColumns(#"Added Custom",{"TimeFrame", "Product", "SiteType", "ActivityType", "SiteActivityType", "ActivityTotalSites", "SPO-CollaboratedbyOwner", "SPO-CollaboratedbyOthers"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Reordered Columns",{{"SiteActivityType", type text}}),
    TenantProductActivity_table = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]){[Name="TenantProductActivity",Signature="table"]}[Data],
    #"Renamed Columns1" = Table.RenameColumns(TenantProductActivity_table,{{"UserCount", "ActiveUserCount"}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Renamed Columns1",{{"TimeFrame", type date}}),
    #"Replaced Sum/Org" = Table.ReplaceValue(#"Changed Type2","Summary/OrganizeConference","Summary/Conference Organizer",Replacer.ReplaceText,{"Activity"}),
    #"Replace Sum/P2P" = Table.ReplaceValue(#"Replaced Sum/Org","Summary/PeerSession","Summary/Peer-to-Peer",Replacer.ReplaceText,{"Activity"}),
    #"Replaced Sum/Part" = Table.ReplaceValue(#"Replace Sum/P2P","Summary/ParticipateConference","Summary/Conference Participant",Replacer.ReplaceText,{"Activity"}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type1",{"TimeFrame", "Product", "SiteActivityType"},#"Replaced Sum/Part" ,{"TimeFrame", "Product", "Activity"},"NewColumn",JoinKind.Inner),
    #"Expanded NewColumn" = Table.ExpandTableColumn(#"Merged Queries", "NewColumn", {"ActivityCount"}, {"ActivityCount"}),
    TenantProductUsage_table = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]){[Name="TenantProductUsage",Signature="table"]}[Data],
    #"Changed Type3" = Table.TransformColumnTypes(TenantProductUsage_table,{{"TimeFrame", type date}}),
    #"Renamed Columns3" = Table.RenameColumns(#"Changed Type3",{{"LicensedUsers", "EnabledUsers"}, {"MOMReturningUsers", "MoMReturningUsers"}}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded NewColumn",{"TimeFrame", "Product"},#"Renamed Columns3",{"TimeFrame", "Product"},"NewColumn",JoinKind.Inner),
    #"Expanded NewColumn1" = Table.ExpandTableColumn(#"Merged Queries1", "NewColumn", {"EnabledUsers", "ActiveUsers"}, {"EnabledUsers", "ActiveUsers"}),
    TenantSharePointUsage_table = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]){[Name="TenantSharePointUsage",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(TenantSharePointUsage_table,{"SiteType", "DiskUsed", "DiskQuota", "DocumentCount", "TotalSites", "TimeFrame", "ContentDate"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Changed Type4" = Table.TransformColumnTypes(#"Removed Duplicates",{{"TimeFrame", type date}}),
    #"Renamed Columns2" = Table.RenameColumns(#"Changed Type4",{{"TotalSites", "TotalSites"}}),
    #"Merged Queries2" = Table.NestedJoin(#"Expanded NewColumn1",{"SiteType", "TimeFrame"},#"Renamed Columns2",{"SiteType", "TimeFrame"},"NewColumn",JoinKind.Inner),
    #"Expanded NewColumn2" = Table.ExpandTableColumn(#"Merged Queries2", "NewColumn", {"DocumentCount", "TotalSites"}, {"DocumentCount", "TotalSites"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded NewColumn2",{{"ActivityCount", "ActiveFiles"}, {"ActivityTotalSites", "ActiveSites"}, {"DocumentCount", "TotalFiles"}})
in
    #"Renamed Columns"
```


## Table: RegionActivity


```m
let
    Source = UserActivity,
    #"Removed Columns" = Table.RemoveColumns(Source,{"IdType"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"TimeFrame", "UserId"}, "Attribute", "Value"),
    #"Sorted Rows" = Table.Sort(#"Unpivoted Columns",{{"Value", Order.Descending}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Sorted Rows",{{"TimeFrame", type date}, {"Value", Int64.Type}}),
    #"Sorted Rows1" = Table.Sort(#"Changed Type",{{"UserId", Order.Descending}}),
    #"Renamed Columns" = Table.RenameColumns(#"Sorted Rows1",{{"Attribute", "Activity"}, {"Value", "ActivityCount"}}),
    #"Added Conditional Column" = Table.AddColumn(#"Renamed Columns", "Product", each if Text.Contains([Activity], "SPO") then "SharePoint" else if Text.Contains([Activity], "EXO") then "Exchange" else if Text.Contains([Activity], "ODB") then "OneDrive" else if Text.Contains([Activity], "SFB") then "Skype" else if Text.Contains([Activity], "Teams") then "Teams" else if Text.Contains([Activity], "YAM") then "Yammer" else "blank()" ),
    #"Reordered Columns" = Table.ReorderColumns(#"Added Conditional Column",{"TimeFrame", "UserId", "Activity", "Product", "ActivityCount"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Reordered Columns",{"Activity"}),
    #"Grouped Rows" = Table.Group(#"Removed Columns1", {"TimeFrame", "UserId", "Product"}, {{"TotalActivityCount", each List.Sum([ActivityCount]), type number}}),
    #"Sorted Rows2" = Table.Sort(#"Grouped Rows",{{"UserId", Order.Ascending}})
in
    #"Sorted Rows2"
```


## Table: TopN


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlbSUQrJL1AwVorViVYyhfJMwTxDAygXyADzYdKGEHkjmLwRRN4IJm8EkTeFyZtC9RsgDASKxAIA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [TopNValues = _t, TopN = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"TopNValues", Int64.Type}, {"TopN", type text}})
in
    #"Changed Type"
```


## Table: TenantO365GroupsUsage


```m
let
    Source = OData.Feed("https://reports.office.com/pbi/v1.0/" & TenantID,null,[ODataVersion=4]),
    TenantO365GroupsActivity_table = Source{[Name="TenantO365GroupsActivity",Signature="table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(TenantO365GroupsActivity_table,{{"GroupType", type text}, {"TotalGroups", Int64.Type}, {"ActiveGroups", Int64.Type}, {"MBX_TotalGroups", Int64.Type}, {"MBX_ActiveGroups", Int64.Type}, {"MBX_TotalActivities", Int64.Type}, {"MBX_TotalItems", Int64.Type}, {"MBX_StorageUsed", Int64.Type}, {"SPO_TotalGroups", Int64.Type}, {"SPO_ActiveGroups", Int64.Type}, {"SPO_FileAccessedActiveGroups", Int64.Type}, {"SPO_FileSyncedActiveGroups", Int64.Type}, {"SPO_FileSharedInternallyActiveGroups", Int64.Type}, {"SPO_FileSharedExternallyActiveGroups", Int64.Type}, {"SPO_TotalActivities", Int64.Type}, {"SPO_FileAccessedActivities", Int64.Type}, {"SPO_FileSyncedActivities", Int64.Type}, {"SPO_FileSharedInternallyActivities", Int64.Type}, {"SPO_FileSharedExternallyActivities", Int64.Type}, {"SPO_TotalFiles", Int64.Type}, {"SPO_ActiveFiles", Int64.Type}, {"SPO_StorageUsed", Int64.Type}, {"YAM_TotalGroups", Int64.Type}, {"YAM_ActiveGroups", Int64.Type}, {"YAM_LikedActiveGroups", Int64.Type}, {"YAM_PostedActiveGroups", Int64.Type}, {"YAM_ReadActiveGroups", Int64.Type}, {"YAM_TotalActivities", Int64.Type}, {"YAM_LikedActivities", Int64.Type}, {"YAM_PostedActivties", Int64.Type}, {"YAM_ReadActivites", Int64.Type}, {"TimeFrame", type date}, {"ContentDate", type datetime}})
in
    #"Changed Type"
```


## Parameter: TenantID


```m
"720ebb82-481f-4a53-b7ca-9a6c71a0e24b" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

