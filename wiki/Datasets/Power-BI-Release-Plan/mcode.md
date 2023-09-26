



# M Code

|Dataset|[Power BI Release Plan](./../Power-BI-Release-Plan.md)|
| :--- | :--- |
|Workspace|[Power BI Release Plan](../../Workspaces/Power-BI-Release-Plan.md)|

## Table: Features


```m
let
    Source = Products,
    #"Invoked Custom Function" = Table.AddColumn(Source, "fxFeatures", each fxFeatures([ProductId])),
    #"Removed Other Columns" = Table.SelectColumns(#"Invoked Custom Function",{"Product","fxFeatures"}),
    #"Expanded fxFeatures" = Table.ExpandTableColumn(#"Removed Other Columns", "fxFeatures", {"SnapshotId", "FeatureDetails", "FeatureName", "EnabledFor", "ReleaseWaveName", "LearnMore", "BlogURL", "DocsUrl"}, {"SnapshotId", "FeatureDetails", "FeatureName", "EnabledFor", "ReleaseWaveName", "LearnMore", "BlogURL", "DocsUrl"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded fxFeatures",{{"FeatureName", "Feature"}, {"DocsUrl", "Docs URL"}, {"EnabledFor", "Enabled for"}, {"FeatureDetails", "Description"}, {"LearnMore", "Learn More"}, {"BlogURL", "Blog URL"}}),
    #"Custom: Description text" = Table.TransformColumns( #"Renamed Columns" , {"Description", each Html.Table( _ , {{"Column1",":root"}})[Column1]{0} } ),
    #"Inserted Merged Column" = Table.AddColumn(#"Custom: Description text", "Feature Search", each Text.Combine({[Feature], [Description]}, " "), type text),
    #"Split Column by Delimiter" = Table.SplitColumn(#"Inserted Merged Column", "ReleaseWaveName", Splitter.SplitTextByDelimiter(" release wave ", QuoteStyle.Csv), {"Year", "ReleaseWave"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"SnapshotId", type text}, {"Feature", type text}, {"Description", type text}, {"Enabled for", type text}, {"Blog URL", type any}, {"Docs URL", type text}, {"Feature Search", type text}, {"Year", Int64.Type}, {"ReleaseWave", Int64.Type}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",".md","",Replacer.ReplaceText,{"Learn More"}),
    #"Custom: fxFeatureuRL" = Table.AddColumn(#"Replaced Value", "Feature URL", each fxFeatureURL([Year], [ReleaseWave], [Product], [Learn More]), Text.Type )
in
    #"Custom: fxFeatureuRL"
```


## Table: Calendar


```m
let
    startDate = #date(2019, 1, 1),
    startYear = Date.Year(startDate),
    nextYear = Date.Year(DateTime.FixedLocalNow()) + 1,
    yearDifference = nextYear - startYear + 1,
    endDate = Date.AddYears(startDate, yearDifference),
    totalDays = Duration.Days(endDate - startDate) + 1,
    fullList =
        List.Dates(
            startDate,
            totalDays,
            #duration(1, 0, 0, 0)
        ),
    calTable =
        Table.FromList(
            fullList,
            Splitter.SplitByNothing(),
            type table [Date = date]
        ),
    #"Inserted Start of Month" =
        Table.AddColumn(
            calTable,
            "Month",
            each Date.StartOfMonth([Date]),
            type date
        )
in
    #"Inserted Start of Month"
```


## Table: Measurements


```m
let
    Source = #table(type table [#"Refresh Time" = datetime], {{DateTime.FixedLocalNow()}})
in
    Source
```


## Table: Feature Dates


```m
let
    Source = Products,
    #"Invoked Custom Function" = Table.AddColumn(Source, "fxFeatures", each fxFeatures([ProductId])),
    #"Removed Other Columns" = Table.SelectColumns(#"Invoked Custom Function",{"fxFeatures"}),
    #"Expanded fxFeatures" = Table.ExpandTableColumn(#"Removed Other Columns", "fxFeatures", {"SnapshotId", "GADateValue", "PPDateValue", "GAStatus", "PPStatus"}, {"SnapshotId", "GADateValue", "PPDateValue", "GAStatus", "PPStatus"}),
    #"Custom: General Availability" = Table.AddColumn( #"Expanded fxFeatures"[[SnapshotId],[GADateValue],[GAStatus]] , "Availability", each "General Availability" ),
    #"Custom: GA Rename" = Table.RenameColumns(#"Custom: General Availability",{{"GADateValue", "Date"}, {"GAStatus", "Status"}}),
    #"Custom: Public Preview" = Table.AddColumn(#"Expanded fxFeatures"[[SnapshotId],[PPDateValue],[PPStatus]], "Availability", each "Public Preview" ),
    #"Custom: PP Rename" = Table.RenameColumns(#"Custom: Public Preview",{{"PPDateValue", "Date"}, {"PPStatus", "Status"}}),
    #"Append: PP and GA" = Table.Combine( { #"Custom: PP Rename", #"Custom: GA Rename" } ),
    #"Replace: ""-""" = Table.ReplaceValue(#"Append: PP and GA","-",null,Replacer.ReplaceValue,{"Date"}),
    #"Replace: ""To be announced""" = Table.ReplaceValue(#"Replace: ""-""","To be announced",null,Replacer.ReplaceValue,{"Date"}),
    #"Repalce: ""N/A""" = Table.ReplaceValue(#"Replace: ""To be announced""","N/A",null,Replacer.ReplaceValue,{"Availability"}),
    #"Remove: empty rows" = Table.SelectRows( #"Repalce: ""N/A""" , each [Date] <> null and [Availability] <> null ),
    #"Custom: Date value" = Table.TransformColumns( #"Remove: empty rows" , {"Date", each if Text.Contains( _ , ", " ) then _ else Date.From( _ ) } ),
    #"Added Custom" = Table.AddColumn(#"Custom: Date value", "Availability Sort", each if [Availability] = "Public Preview" then 0 else if [Availability] = "General Availability" then 1 else null),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Date", type date}, {"SnapshotId", type text}, {"Availability", type text}, {"Availability Sort", Int64.Type}, {"Status", type text}})
in
    #"Changed Type"
```


## Table: Change History


```m
let
    Source = Products,
    #"Invoked: fxChangeHistory" = Table.AddColumn(Source, "fxChangeHistory", each fxChangeHistory([ProductId])),
    #"Removed Other Columns" = Table.SelectColumns(#"Invoked: fxChangeHistory",{"fxChangeHistory"}),
    #"Expanded fxChangeHistory" = Table.ExpandTableColumn(#"Removed Other Columns", "fxChangeHistory", {"results"}, {"results"}),
    #"Expanded results" = Table.ExpandRecordColumn(#"Expanded fxChangeHistory", "results", { "snapshotID", "dateModified", "changeDescription" }, {"snapshotID", "Date Modified", "Change Description"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded results",{{"snapshotID", type text}, {"Date Modified", type date}, {"Change Description", type text}})
in
    #"Changed Type"
```

