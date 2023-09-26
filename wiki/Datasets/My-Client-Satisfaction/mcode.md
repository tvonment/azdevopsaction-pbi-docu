



# M Code

|Dataset|[My Client Satisfaction](./../My-Client-Satisfaction.md)|
| :--- | :--- |
|Workspace|[CRM](../../Workspaces/CRM.md)|

## Table: msfp_surveyresponses


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_surveyresponses_table = Source{[Name="msfp_surveyresponses",Signature="table"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(msfp_surveyresponses_table,{{"createdon", type date}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each [createdon] >= #date(2022, 10, 1))
in
    #"Filtered Rows"
```


## Table: msfp_questionresponses


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_questionresponses",Signature="table"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(msfp_questionresponses_table, "Not at all satisfied (1/5)","1 - Not at all satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Dissatisfied (2/5)","2 - Dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","Neutral (3/5)","3 - Neutral",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","Satisfied (4/5)","4 - Satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","Completely satisfied (5/5)","5 - Completely satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","Very dissatisfied","1 - Not at all satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5","Rather dissatisfied","2 - Dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value6","Neutral","3 - Neutral",Replacer.ReplaceValue,{"msfp_response"}),
    #"Replaced Value8" = Table.ReplaceValue(#"Replaced Value7","Fairly satisfied","4 - Satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value9" = Table.ReplaceValue(#"Replaced Value8","Very satisfied","5 - Completely satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value10" = Table.ReplaceValue(#"Replaced Value9","(e.g. Senior Vice President Operations, Acme Inc.)","",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value11" = Table.ReplaceValue(#"Replaced Value10","(e.g. Jane Doe, Vice President Operations, Acme Inc.)","",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value12" = Table.ReplaceValue(#"Replaced Value11"," Please select your prefered option below.","",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value13" = Table.ReplaceValue(#"Replaced Value12"," (please specify your preferred option in the question that will appear below)","",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value14" = Table.ReplaceValue(#"Replaced Value13"," (please specify your preferred option in the question that will appear below)","",Replacer.ReplaceText,{"msfp_response"}),
    #"Trimmed Text" = Table.TransformColumns(#"Replaced Value14",{{"msfp_response", Text.Trim, type text}}),
    #"Added Custom" = Table.AddColumn(#"Trimmed Text", "msfp_response_numeric", each try Number.From([msfp_response]) otherwise try Number.From(Text.At([msfp_response], 0)) otherwise null)
in
    #"Added Custom"
```


## Table: msfp_surveyinvites


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_surveyinvites",Signature="table"]}[Data]
in
    msfp_questionresponses_table
```


## Table: msfp_surveies


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_surveies_table = Source{[Name="msfp_surveies",Signature="table"]}[Data]
in
    msfp_surveies_table
```


## Table: msfp_questions


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_questions",Signature="table"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(msfp_questionresponses_table,"Why did you initially decide to conduct this project with Roland Berger?","Approach & presentation",Replacer.ReplaceText,{"msfp_name"})
in
    #"Replaced Value"
```


## Table: msfp_questionresponses_individual


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_questionresponses",Signature="table"]}[Data],
    #"Split Column by Delimiter" = Table.ExpandListColumn(Table.TransformColumns(msfp_questionresponses_table, {{"msfp_response", Splitter.SplitTextByDelimiter(",", QuoteStyle.Csv), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "msfp_response"),
    #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"msfp_response", type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type", "Not at all satisfied (1/5)","1 - Not at all satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","Dissatisfied (2/5)","2 - Dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","Neutral (3/5)","3 - Neutral",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","Satisfied (4/5)","4 - Satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","Completely satisfied (5/5)","5 - Completely satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","Very dissatisfied","1 - Not at all satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value6" = Table.ReplaceValue(#"Replaced Value5","Rather dissatisfied","2 - Dissatisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value7" = Table.ReplaceValue(#"Replaced Value6","Neutral","3 - Neutral",Replacer.ReplaceValue,{"msfp_response"}),
    #"Replaced Value8" = Table.ReplaceValue(#"Replaced Value7","Fairly satisfied","4 - Satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Replaced Value9" = Table.ReplaceValue(#"Replaced Value8","Very satisfied","5 - Completely satisfied",Replacer.ReplaceText,{"msfp_response"}),
    #"Added Custom" = Table.AddColumn(#"Replaced Value9", "msfp_response_numeric", each try Number.From([msfp_response]) otherwise try Number.From(Text.At([msfp_response], 0)) otherwise null)
in
    #"Added Custom"
```


## Table: nxtgn_projects


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_projects_table = Source{[Name="nxtgn_projects",Signature="table"]}[Data],
    #"Added Custom" = Table.AddColumn(nxtgn_projects_table, "statuscode_meta", each Value.Metadata([statuscode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "statecode_meta", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "_nxtgn_accountid_value_meta", each if [_nxtgn_accountid_value] is null then "" else Value.Metadata([_nxtgn_accountid_value])[OData.Community.Display.V1.FormattedValue]),
    #"Removed Other Columns" = Table.SelectColumns(#"Added Custom2",{"nxtgn_projectid", "nxtgn_projecttitleorig", "_nxtgn_deliverymanagerid_value", "_nxtgn_projectmanagerid_value", "_nxtgn_accountid_value_meta", "nxtgn_accountname", "nxtgn_project_planned_enddate"}),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Removed Other Columns", {{"_nxtgn_accountid_value_meta", ""}})
in
    #"Replaced Errors"
```


## Table: systemusers


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers_table = Source{[Name="systemusers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(systemusers_table,{"_nxtgn_platformid_value", "_nxtgn_lookupcountryid_value", "fullname", "systemuserid", "internalemailaddress"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupplatforms


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupplatforms_table = Source{[Name="nxtgn_lookupplatforms",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupplatforms_table, each ([statuscode] = 1)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_name", "nxtgn_lookupplatformid"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_lookupcountries


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_lookupcountries_table = Source{[Name="nxtgn_lookupcountries",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(nxtgn_lookupcountries_table, each ([statuscode] = 1)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"nxtgn_lookupcountryid", "nxtgn_name"})
in
    #"Removed Other Columns"
```


## Table: nxtgn_customersurveytriggers


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_customersurveytriggers_table = Source{[Name="nxtgn_customersurveytriggers",Signature="table"]}[Data],
    #"Added Custom" = Table.AddColumn(nxtgn_customersurveytriggers_table, "nxtgn_surveystatus_meta", each Value.Metadata([nxtgn_surveystatus])[OData.Community.Display.V1.FormattedValue]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "nxtgn_reasonforcancelation_meta", each if [nxtgn_reasonforcancelation] is null then "" else Value.Metadata([nxtgn_reasonforcancelation])[OData.Community.Display.V1.FormattedValue]),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom1", each true),
    #"Expanded nxtgn_surveyrecipientid" = Table.ExpandRecordColumn(#"Filtered Rows", "nxtgn_surveyrecipientid", {"fullname"}, {"nxtgn_surveyrecipientid.fullname"}),
    #"Added Conditional Column" = Table.AddColumn(#"Expanded nxtgn_surveyrecipientid", "nxtgn_surveystatus_meta_grouped", each if [nxtgn_surveystatus_meta] = "Open" then "Due" else if [nxtgn_surveystatus_meta] = "Sent" then "Requested" else if [nxtgn_surveystatus_meta] = "Received" then "Received" else "Handled (not sent)", type text),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "nxtgn_surveystatus_meta_grouped_sort", each if [nxtgn_surveystatus_meta_grouped] = "Handled (not sent)" then 2 else if [nxtgn_surveystatus_meta_grouped] = "Due" then 1 else if [nxtgn_surveystatus_meta_grouped] = "Requested" then 3 else if [nxtgn_surveystatus_meta_grouped] = "Received" then 4 else null, type number)
in
    #"Added Conditional Column1"
```


## Table: Switch NPS Benchmark


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45Wcs/JT0rMUdJRMlSK1YlWCshJLEnLL8oFChiBBSLzS4sUAorys1KTS4qBosZgUef80rySokog30QpNhYA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Axis = _t, ID = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Axis", type text}, {"ID", Int64.Type}})
in
    #"Changed Type"
```


## Table: msfp_questions_individual


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_questions",Signature="table"]}[Data],
    #"Filtered Rows" = Table.SelectRows(msfp_questionresponses_table, each ([msfp_sourcesurveyidentifier] = "grsOch9IU0q3yppscaDiS6C8hKLxjGJMjqBtk69Wb4JUREMwTTFNSlo0SkwxQ0VOVzROWVRVNFc1OS4u")),
    #"Split Column by Delimiter" = Table.TransformColumns(#"Filtered Rows", {"msfp_questionchoices", each if _ <> null then Table.AddIndexColumn(Table.FromList(Text.Split(_, ","), Splitter.SplitByNothing()), "Index", 1, 1) else null}),
    #"Expanded msfp_questionchoices" = Table.ExpandTableColumn(#"Split Column by Delimiter", "msfp_questionchoices", {"Column1", "Index"}, {"msfp_questionchoices.Column1", "msfp_questionchoices.Index"}),
    #"Replaced Value" = Table.ReplaceValue(#"Expanded msfp_questionchoices","""","",Replacer.ReplaceText,{"msfp_questionchoices.Column1"}),
    #"Renamed Columns" = Table.RenameColumns(#"Replaced Value",{{"msfp_questionchoices.Column1", "msfp_questionchoices"}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Renamed Columns", "msfp_questionchoices_order", each Text.Combine({Text.From([msfp_order], "de-DE"), Text.From([msfp_questionchoices.Index], "de-DE")}), type text),
    #"Removed Columns" = Table.RemoveColumns(#"Inserted Merged Column",{"msfp_questionchoices.Index"})
in
    #"Removed Columns"
```


## Table: systemusers (2)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers_table = Source{[Name="systemusers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(systemusers_table,{"_nxtgn_lookupcountryid_value", "fullname", "systemuserid", "internalemailaddress"})
in
    #"Removed Other Columns"
```


## Table: NPS Benchmark LTM


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0"]),
    msfp_questionresponses_table = Source{[Name="msfp_questionresponses",Signature="table"]}[Data],
    #"Filtered Rows3" = Table.SelectRows(msfp_questionresponses_table, each ([msfp_sourcesurveyidentifier] = "grsOch9IU0q3yppscaDiS6C8hKLxjGJMjqBtk69Wb4JUREMwTTFNSlo0SkwxQ0VOVzROWVRVNFc1OS4u")),
    #"Filtered Rows2" = Table.SelectRows(#"Filtered Rows3", each [createdon] >= #datetimezone(2022, 10, 1, 0, 0, 0, 2, 0)),
    #"Filtered Rows" = Table.SelectRows(#"Filtered Rows2", each ([_msfp_questionid_value] = "6c39951c-6dfb-ec11-82e5-000d3a449610")),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each Date.IsInPreviousNMonths([createdon], 11) or Date.IsInCurrentMonth([createdon])),
    #"Expanded msfp_surveyresponseid" = Table.ExpandRecordColumn(#"Filtered Rows1", "msfp_surveyresponseid", {"regardingobjectid_nxtgn_project"}, {"msfp_surveyresponseid.regardingobjectid_nxtgn_project"}),
    #"Expanded msfp_surveyresponseid.regardingobjectid_nxtgn_project" = Table.ExpandRecordColumn(#"Expanded msfp_surveyresponseid", "msfp_surveyresponseid.regardingobjectid_nxtgn_project", {"nxtgn_deliverymanagerid"}, {"msfp_surveyresponseid.regardingobjectid_nxtgn_project.nxtgn_deliverymanagerid"}),
    #"Expanded msfp_surveyresponseid.regardingobjectid_nxtgn_project.nxtgn_deliverymanagerid" = Table.ExpandRecordColumn(#"Expanded msfp_surveyresponseid.regardingobjectid_nxtgn_project", "msfp_surveyresponseid.regardingobjectid_nxtgn_project.nxtgn_deliverymanagerid", {"_nxtgn_platformid_value", "_nxtgn_lookupcountryid_value"}, {"msfp_surveyresponseid.regardingobjectid_nxtgn_project.nxtgn_deliverymanagerid._nxtgn_platformid_value", "msfp_surveyresponseid.regardingobjectid_nxtgn_project.nxtgn_deliverymanagerid._nxtgn_lookupcountryid_value"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded msfp_surveyresponseid.regardingobjectid_nxtgn_project.nxtgn_deliverymanagerid",{{"msfp_surveyresponseid.regardingobjectid_nxtgn_project.nxtgn_deliverymanagerid._nxtgn_platformid_value", "nxtgn_deliverymanagerid._nxtgn_platformid_value"}, {"msfp_surveyresponseid.regardingobjectid_nxtgn_project.nxtgn_deliverymanagerid._nxtgn_lookupcountryid_value", "nxtgn_deliverymanagerid._nxtgn_lookupcountryid_value"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"_msfp_questionid_value", "_ownerid_value", "createdon", "msfp_sourcesurveyidentifier", "_owningbusinessunit_value", "msfp_name", "statuscode", "msfp_otherproperties", "msfp_keyphrases", "importsequencenumber", "overriddencreatedon", "utcconversiontimezonecode", "_createdonbehalfby_value", "versionnumber", "_owningteam_value", "_modifiedonbehalfby_value", "msfp_sourceresponseidentifier", "_createdby_value", "timezoneruleversionnumber", "msfp_sentimentvalue", "statecode", "_owninguser_value", "createdby", "createdonbehalfby", "modifiedby", "modifiedonbehalfby", "owninguser", "owningteam", "ownerid", "owningbusinessunit", "msfp_questionresponse_SyncErrors", "msfp_questionresponse_DuplicateMatchingRecord", "msfp_questionresponse_DuplicateBaseRecord", "msfp_questionresponse_AsyncOperations", "msfp_questionresponse_MailboxTrackingFolders", "msfp_questionresponse_ProcessSession", "msfp_questionresponse_BulkDeleteFailures", "msfp_questionresponse_PrincipalObjectAttributeAccesses", "msfp_questionid"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"msfp_response", Int64.Type}})
in
    #"Changed Type"
```


## Table: nxtgn_projects_delivery_manager_project_manager


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_projects_table = Source{[Name="nxtgn_projects",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(nxtgn_projects_table,{"nxtgn_projectid", "_nxtgn_deliverymanagerid_value", "_nxtgn_projectmanagerid_value"}),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Removed Other Columns", {"nxtgn_projectid"}, "Role", "_nxtgn_systemuserid_value"),
    #"Replaced Value" = Table.ReplaceValue(#"Unpivoted Other Columns","_nxtgn_deliverymanagerid_value","Delivery Manager",Replacer.ReplaceText,{"Role"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","_nxtgn_projectmanagerid_value","Project Manager",Replacer.ReplaceText,{"Role"})
in
    #"Replaced Value1"
```


## Table: systemusers (3)


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    systemusers_table = Source{[Name="systemusers",Signature="table"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(systemusers_table,{"_nxtgn_platformid_value", "fullname", "systemuserid", "internalemailaddress"})
in
    #"Removed Other Columns"
```


## Table: Project Status Benchmark LTM


```m
let
    Source = OData.Feed("https://rolandberger.crm4.dynamics.com/api/data/v9.1", null, [Implementation="2.0", IncludeAnnotations="OData.Community.Display.V1.FormattedValue"]),
    nxtgn_customersurveytriggers_table = Source{[Name="nxtgn_customersurveytriggers",Signature="table"]}[Data],
    #"Added Custom" = Table.AddColumn(nxtgn_customersurveytriggers_table, "nxtgn_surveystatus_meta", each Value.Metadata([nxtgn_surveystatus])[OData.Community.Display.V1.FormattedValue]),
    #"Removed Other Columns" = Table.SelectColumns(#"Added Custom",{"nxtgn_customersurveytriggerid", "nxtgn_surveystatus_meta", "nxtgn_projectid"}),
    #"Expanded nxtgn_projectid" = Table.ExpandRecordColumn(#"Removed Other Columns", "nxtgn_projectid", {"nxtgn_project_planned_enddate"}, {"nxtgn_projectid.nxtgn_project_planned_enddate"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded nxtgn_projectid", each Date.IsInPreviousNMonths([nxtgn_projectid.nxtgn_project_planned_enddate], 11) or Date.IsInCurrentMonth([nxtgn_projectid.nxtgn_project_planned_enddate])),
    #"Added Conditional Column" = Table.AddColumn(#"Filtered Rows", "nxtgn_surveystatus_meta_grouped", each if [nxtgn_surveystatus_meta] = "Open" then "Due" else if [nxtgn_surveystatus_meta] = "Sent" then "Requested" else if [nxtgn_surveystatus_meta] = "Received" then "Received" else "Handled (not sent)", type text),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "nxtgn_surveystatus_meta_grouped_sort", each if [nxtgn_surveystatus_meta_grouped] = "Handled (not sent)" then 2 else if [nxtgn_surveystatus_meta_grouped] = "Due" then 1 else if [nxtgn_surveystatus_meta_grouped] = "Requested" then 3 else if [nxtgn_surveystatus_meta_grouped] = "Received" then 4 else null, type number)
in
    #"Added Conditional Column1"
```


## Roles

### Own Projects only


Model Permission: Read

systemusers

```m
[internalemailaddress] = USERPRINCIPALNAME()
```


### proClient Admin


Model Permission: Read
### Country Head


Model Permission: Read

systemusers (2)

```m
[internalemailaddress] = USERPRINCIPALNAME()
```


### Platform Head


Model Permission: Read

systemusers (3)

```m
[internalemailaddress] = USERPRINCIPALNAME()
```

