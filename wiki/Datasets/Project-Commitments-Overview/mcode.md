



# M Code

|Dataset|[Project Commitments Overview](./../Project-Commitments-Overview.md)|
| :--- | :--- |
|Workspace|[Project Commitments [Prod]](../../Workspaces/Project-Commitments-[Prod].md)|

## Table: DimDate


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    pub_dim_date = Source{[Schema="pub",Item="dim_date"]}[Data],
    #"Replaced Value" = Table.ReplaceValue(pub_dim_date,"-W","-CW",Replacer.ReplaceText,{"ISOWeekOfYearNameInCal"})
in
    #"Replaced Value"
```


## Table: DimProjectSurvey


```m
let
    Source = ProjectSurvey,
    #"Renamed Columns" = Table.RenameColumns(Source,{{"ID", "ProjectSurveyID"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"ProjectStartDate", "ProjectEndDate", "EmployeeIDPM", "LastModifiedBy", "LastModifiedAt", "InvitationSent", "CreatedByUserID", "CanBeDeleted"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each ([RelevantForPCsYesNo] = null or [RelevantForPCsYesNo] = true)),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"ProjectSurveyID"}, tmpResponsibleConcat, {"ProjectSurveyID"}, "tmpResponsibleConcat", JoinKind.LeftOuter),
    #"Expanded tmpResponsibleConcat" = Table.ExpandTableColumn(#"Merged Queries", "tmpResponsibleConcat", {"PMs"}, {"PMs"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Expanded tmpResponsibleConcat",{{"SurveyTypeName", "Survey Type"}})
in
    #"Renamed Columns1"
```


## Table: DimParticipants


```m
let
    Source = SurveyParticipant,
    #"Renamed Columns" = Table.RenameColumns(Source,{{"ID", "SurveyParticipantID"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{ "LastModifiedBy", "LastModifiedAt", "ADUserID", "EmailSent", "EmailSentAt", "CommitmentModifiedAt", "CommitmentModifiedBy", "ProjectSurvey"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each ([OrgResponsiblePMEmail] <> null and [OrgResponsiblePMEmail] <> [EmployeeEmail])),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"OrgResponsiblePMEmail"}, DimPMs, {"ResponsiblePMEmail"}, "DimPMs", JoinKind.LeftOuter),
    #"Expanded DimPMs" = Table.ExpandTableColumn(#"Merged Queries", "DimPMs", {"Name"}, {"Project manager"}),
    #"Merged Queries1" = Table.NestedJoin(#"Expanded DimPMs", {"EmployeeID"}, #"rep v_hr_employee", {"emp_id"}, "rep v_hr_employee", JoinKind.LeftOuter),
    #"Expanded rep v_hr_employee" = Table.ExpandTableColumn(#"Merged Queries1", "rep v_hr_employee", {"jobcode"}, {"jobcode"})
in
    #"Expanded rep v_hr_employee"
```


## Table: RLS Measures


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Column1"})
in
    #"Removed Columns"
```


## Table: Values


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSK1YlWMgKTxmDSRCk2FgA=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Values = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Values", Int64.Type}})
in
    #"Changed Type"
```


## Table: FactSurveyQ


```m
let
    Source = FactSurvey,
    #"Expanded SurveyCampaign" = Table.ExpandRecordColumn(Source, "SurveyCampaign", {"ProjectSurveyID"}, {"ProjectSurveyID"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded SurveyCampaign",{"C1", "C2", "Comment1", "Comment2", "Comment3", "Commitment1", "Commitment2", "LastModifiedBy", "LastModifiedAt"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"ID", "SurveyCampaignID", "SurveyParticipantID", "SurveyTypeID", "DateKey", "ProjectSurveyID"}, "Question", "Value")
in
    #"Unpivoted Columns"
```


## Table: FactSurveyC


```m
let
    Source = FactSurvey,
    #"Removed Columns" = Table.RemoveColumns(Source,{ "Comment3", "LastModifiedBy", "LastModifiedAt", "SurveyCampaign", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6"}),
    #"Unpivoted Columns" = Table.UnpivotOtherColumns(#"Removed Columns", {"ID", "SurveyCampaignID", "SurveyParticipantID", "SurveyTypeID", "DateKey", "Commitment1", "Commitment2","Comment1", "Comment2"}, "Attribute", "Value012"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Columns",{{"Attribute", "Commitment"}}),
    #"correct non existing commitment" = Table.AddColumn(#"Renamed Columns", "CorrectedValue012", each if  [Commitment] ="C1" then 
if [Commitment1] = null then 0 
else [Value012] 
else if  [Commitment] ="C2" then 
if [Commitment2] = null then 0 
else [Value012] 
else [Value012]),
    #"Added Conditional Column" = Table.AddColumn(#"correct non existing commitment", "Value", each if [CorrectedValue012] = 2 then -1 else [CorrectedValue012], type number),
    #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "Custom", each if [Commitment] = "C1" then [Comment1] else if [Commitment] = "C2" then [Comment2] else null),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Conditional Column1",{{"Custom", type text}}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Changed Type", "Commitment", "CommitmentSort"),
    #"Replaced Value" = Table.ReplaceValue(#"Duplicated Column","C1", each  [Commitment1],Replacer.ReplaceText,{"Commitment"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","C2",each [Commitment2],Replacer.ReplaceText,{"Commitment"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Replaced Value1",{"Commitment1", "Commitment2", "Comment1", "Comment2"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns1",{{"Custom", "Comment"}}),
    #"Removed not defined commitments" = Table.SelectRows(#"Renamed Columns1", each ([Commitment] <> "C1" and [Commitment] <> "C2")),
    #"Replaced Value2" = Table.ReplaceValue(#"Removed not defined commitments","C1","Commitment1",Replacer.ReplaceValue,{"Commitment"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","C2","Commitment2",Replacer.ReplaceValue,{"Commitment"}),
    #"Removed Columns2" = Table.RemoveColumns(#"Replaced Value3",{"Value012"})
in
    #"Removed Columns2"
```


## Table: Auswertung nach KWs (Row)


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WUtJRcswrSc3MUYhR8kqMUVKKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Auswertung nach KWs" = _t, Anteil = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Auswertung nach KWs", type text}, {"Anteil", type text}})
in
    #"Changed Type"
```


## Table: WeekFilterParameter


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45Wci4tKkrNK1EIT03NVorViVbySSyG8WIB", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [FilterParam = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"FilterParam", type text}})
in
    #"Changed Type"
```


## Table: Calculation


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45W8i9LLUrMyVGK1YlWCklNzFWKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Mode = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Mode", type text}})
in
    #"Changed Type"
```


## Table: CheckMemberOfRlsAdminGroup


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUSrJyCxWSM0rKapUKM7IL81JUcjPy6lUKMsszkzKSVVIyy9SSEzJzcxTCPIJVijKz0lVio0FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [IsAdmin = _t, Column1 = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"IsAdmin", Int64.Type}, {"Column1", type text}})
in
    #"Changed Type"
```


## Table: DimPMs


```m
let
    Source = SurveyParticipant,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"OrgResponsiblePMEmail"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns"),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates",{{"OrgResponsiblePMEmail", "ResponsiblePMEmail"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each [ResponsiblePMEmail] <> null and [ResponsiblePMEmail] <> ""),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows", {"ResponsiblePMEmail"}, SurveyParticipant, {"EmployeeEmail"}, "DimParticipants", JoinKind.LeftOuter),
    #"Expanded DimParticipants" = Table.ExpandTableColumn(#"Merged Queries", "DimParticipants", {"Name"}, {"Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Expanded DimParticipants",{"Name", "ResponsiblePMEmail"}),
    #"Removed Duplicates1" = Table.Distinct(#"Removed Other Columns1"),
    #"Removed Duplicates2" = Table.Distinct(#"Removed Duplicates1", {"ResponsiblePMEmail"})
in
    #"Removed Duplicates2"
```


## Table: DimProjects


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_project_data = Source{[Schema="rep",Item="v_fc_project_data"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(rep_v_fc_project_data,{"project_number", "project_name", "project_client", "project_startdate", "project_enddate", "project_planned_end", "dm_cc_id", "dm_emp_id", "delivery_manager", "pm_emp_id", "project_manager", "sales_unit_cou_country"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Other Columns", {"dm_emp_id"}, #"rep v_hr_employee", {"emp_id"}, "dm", JoinKind.LeftOuter),
    #"Expanded dm" = Table.ExpandTableColumn(#"Merged Queries", "dm", {"cc_id", "cc_name", "country_code"}, {"CCID", "CCName", "CountryCode"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded dm", each Text.StartsWith([project_number], "CP") or (Text.StartsWith([project_number], "P") and not Text.StartsWith([project_number], "P8") and not Text.StartsWith([project_number], "P9")) or (Text.StartsWith([project_number], "A") and not Text.StartsWith([project_number], "A8") and not Text.StartsWith([project_number], "A9") and not Text.StartsWith([project_number], "ACQ"))),
    #"Duplicated Column" = Table.DuplicateColumn(#"Filtered Rows", "project_name", "Project title"),
    #"Replaced Value" = Table.ReplaceValue(#"Duplicated Column",each [project_name], each Text.Combine({[project_number], " - ", [project_name]} ) ,Replacer.ReplaceText,{"project_name"}),
    #"Added Conditional Column" = Table.AddColumn(#"Replaced Value", "ProjectNumber_adj", each if Text.StartsWith([project_number], "A") and not Text.StartsWith([project_number], "ACQ") then Text.Combine({"P-", [project_number]} ) else [project_number]),
    #"Replaced Value1" = Table.ReplaceValue(#"Added Conditional Column","P-A","P",Replacer.ReplaceText,{"ProjectNumber_adj"}),
    #"Merged Queries1" = Table.NestedJoin(#"Replaced Value1", {"ProjectNumber_adj"}, DimProjectSurvey, {"projectnumber_adj"}, "DimProjectSurvey", JoinKind.Inner),
    #"Removed Columns" = Table.RemoveColumns(#"Merged Queries1",{"DimProjectSurvey"})
in

    #"Removed Columns"
```


## Table: FactSurvey


```m
let
    Source = Survey,
    #"Added Custom Column" = Table.AddColumn(Source, "DateKey", each Text.Combine({DateTime.ToText([LastModifiedAt], "yyyy"), DateTime.ToText([LastModifiedAt], "MM"), DateTime.ToText([LastModifiedAt], "dd")}), type text),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom Column",{{"DateKey", Int64.Type}})
in
    #"Changed Type1"
```


## Table: PM2Survey


```m
let
    Source = DimParticipants,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"ProjectSurveyID", "ResponsiblePMEmail"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Other Columns")
in
    #"Removed Duplicates"
```


## Table: RLS_Country


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "app_ProjectCommitments"),
    dbo_RLS_Overview_Country = Source{[Schema="dbo",Item="RLS_Overview_Country"]}[Data],
    #"Lowercased Text" = Table.TransformColumns(dbo_RLS_Overview_Country,{{"UserMail", Text.Lower, type text}})
in
    #"Lowercased Text"
```


## Table: RLS_CC


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "app_ProjectCommitments"),
    dbo_RLS_Overview_CC = Source{[Schema="dbo",Item="RLS_Overview_CC"]}[Data],
    #"Lowercased Text" = Table.TransformColumns(dbo_RLS_Overview_CC,{{"UserMail", Text.Lower, type text}})
in
    #"Lowercased Text"
```


## Table: DimCountry


```m
let
    Source = DimProjects,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"CountryCode"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each [CountryCode] <> null and [CountryCode] <> ""),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows")
in
    #"Removed Duplicates"
```


## Table: DimCC


```m
let
    Source = DimProjects,
    #"Removed Other Columns" = Table.SelectColumns(Source,{"CCID", "CCName"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Other Columns", each [CCID] <> null and [CCID] <> ""),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows")
in
    #"Removed Duplicates"
```


## Table: SurveyCampaign


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "app_ProjectCommitments"),
    dbo_SurveyCampaign = Source{[Schema="dbo",Item="SurveyCampaign"]}[Data],
    #"Merged Queries" = Table.NestedJoin(dbo_SurveyCampaign, {"SurveyTypeID"}, SurveyType, {"ID"}, "SurveyType", JoinKind.LeftOuter),
    #"Expanded SurveyType" = Table.ExpandTableColumn(#"Merged Queries", "SurveyType", {"SurveyTypeName"}, {"Survey Type"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded SurveyType",{{"CreatedAt", type date}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"NumberOfActiveParticipants", "NumberOfActiveParticipants_bak"}, {"NumberOfActiveCommitments", "NumberOfActiveCommitments_bak"}})
in
    #"Renamed Columns"
```


## Table: BarometerCluster


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WCkpNUdJRMgViQxDWMVWK1YlW8i9KzEtPBQqYQAV1lIzAEpGpOTn55UCuMVgIRIOEfTLTM0oU3ItSU/Pg4kAMNQ0mbggVAxqrY2AIlUqsBPLNgNgAjGNjAQ==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Cluster = _t, Sort = _t, From = _t, To = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Cluster", type text}, {"Sort", Int64.Type}, {"From", type number}, {"To", type number}})
in
    #"Changed Type"
```


## Table: DimRegion


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_pc_region = Source{[Schema="rep",Item="v_pc_region"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(rep_v_pc_region,{{"country_code", "CountryCode"}, {"region", "Region"}})
in
    #"Renamed Columns"
```


## Table: DimRejected


```m
let
    Source = ProjectSurvey,
    #"Renamed Columns" = Table.RenameColumns(Source,{{"ID", "ProjectSurveyID"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"ProjectStartDate", "ProjectEndDate", "EmployeeIDPM", "LastModifiedBy",  "InvitationSent", "CreatedByUserID", "CanBeDeleted"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each ([RelevantForPCsYesNo] = false)),
    #"Renamed Columns1" = Table.RenameColumns(#"Filtered Rows",{{"SurveyTypeName", "Survey Type"}})
in
    #"Renamed Columns1"
```


## Table: SurveyReasonForNoUse


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "app_ProjectCommitments"),
    dbo_SurveyReasonForNoUse = Source{[Schema="dbo",Item="SurveyReasonForNoUse"]}[Data]
in
    dbo_SurveyReasonForNoUse
```


## Table: DimProjectsRejected


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "datahub"),
    rep_v_fc_project_data = Source{[Schema="rep",Item="v_fc_project_data"]}[Data],
    #"Removed Other Columns" = Table.SelectColumns(rep_v_fc_project_data,{"project_number", "project_name", "project_client", "project_startdate", "project_enddate", "project_planned_end", "dm_cc_id", "dm_emp_id", "delivery_manager", "pm_emp_id", "project_manager", "sales_unit_cou_country"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Other Columns", {"dm_emp_id"}, #"rep v_hr_employee", {"emp_id"}, "dm", JoinKind.LeftOuter),
    #"Expanded dm" = Table.ExpandTableColumn(#"Merged Queries", "dm", {"cc_id", "cc_name", "country_code"}, {"CCID", "CCName", "CountryCode"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded dm", each Text.StartsWith([project_number], "CP") or (Text.StartsWith([project_number], "P") and not Text.StartsWith([project_number], "P8") and not Text.StartsWith([project_number], "P9")) or (Text.StartsWith([project_number], "A") and not Text.StartsWith([project_number], "A8") and not Text.StartsWith([project_number], "A9") and not Text.StartsWith([project_number], "ACQ"))),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows",each [project_name], each Text.Combine({[project_number], " - ", [project_name]} ) ,Replacer.ReplaceText,{"project_name"}),
    #"Added Conditional Column" = Table.AddColumn(#"Replaced Value", "ProjectNumber_adj", each if Text.StartsWith([project_number], "A") and not Text.StartsWith([project_number], "ACQ") then Text.Combine({"P-", [project_number]} ) else [project_number]),
    #"Replaced Value1" = Table.ReplaceValue(#"Added Conditional Column","P-A","P",Replacer.ReplaceText,{"ProjectNumber_adj"}),
    #"Merged Queries1" = Table.NestedJoin(#"Replaced Value1", {"ProjectNumber_adj"}, DimRejected, {"projectnumber_adj"}, "DimRejected", JoinKind.Inner),
    #"Removed Columns" = Table.RemoveColumns(#"Merged Queries1",{"DimRejected"})
in

    #"Removed Columns"
```


## Table: SurveyCampaignNumOfParticipantsPerPM


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "app_ProjectCommitments"),
    dbo_SurveyCampaignNumOfParticipantsPerPM = Source{[Schema="dbo",Item="SurveyCampaignNumOfParticipantsPerPM"]}[Data]
in
    dbo_SurveyCampaignNumOfParticipantsPerPM
```


## Table: SurveyParticipantsPerCampaign


```m
let
    Source = Sql.Database("muc-mssql-2.rolandberger.net", "app_ProjectCommitments"),
    dbo_SurveyParticipantsPerCampaign = Source{[Schema="dbo",Item="SurveyParticipantsPerCampaign"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(dbo_SurveyParticipantsPerCampaign,{{"CreatedAt", type date}})
in
    #"Changed Type"
```


## Roles

### ByCountryOrCC


Model Permission: Read

CheckMemberOfRlsAdminGroup

```m
[IsAdmin] = 0
```



DimProjects

```m
var curCountry = DimProjects[CountryCode]
var curCC = DimProjects[CCID]
var cu = [RLS Current User Mail]

return 
    if( [RLS Has Filter] 
            , if([RLS Country Has Filter] && calculate(COUNTROWS(RLS_Country), RLS_Country[CountryCode] = curCountry, RLS_Country[UserMail] = cu ) > 0
                , TRUE()
                ,  if([RLS CC Has Filter] && calculate(COUNTROWS(RLS_CC), RLS_CC[CCID] = curCC, RLS_CC[UserMail] = cu) > 0
                    , TRUE()                    
                    , FALSE()
                    )
                ) 
            , FALSE() // no config for user 
    )
```



DimProjectSurvey

```m
 
var curCountry = DimProjectSurvey[CountryCode]
var curCC = DimProjectSurvey[CCID]
var cu = [RLS Current User Mail]

return 
    if( [RLS Has Filter] 
            , if([RLS Country Has Filter] && calculate(COUNTROWS(RLS_Country), RLS_Country[CountryCode] = curCountry, RLS_Country[UserMail] = cu ) > 0
                , TRUE()
                ,  if([RLS CC Has Filter] && calculate(COUNTROWS(RLS_CC), RLS_CC[CCID] = curCC, RLS_CC[UserMail] = cu) > 0
                    , TRUE()                    
                    , FALSE()
                    )
                ) 
            , FALSE() // no config for user 
    )
```



RLS_CC

```m
[UserMail] = [RLS Current User Mail]
```



RLS_Country

```m
[UserMail] = [RLS Current User Mail]
```


### Admin


Model Permission: Read