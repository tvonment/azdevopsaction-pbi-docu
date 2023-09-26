



# M Code

|Dataset|[WeeklyReport - TEAM](./../WeeklyReport---TEAM.md)|
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
    #"Expanded SurveyType" = Table.ExpandRecordColumn(#"Renamed Columns", "SurveyType", {"SurveyTypeName"}, {"SurveyType"}),
    #"Appended Query" = Table.Combine({#"Expanded SurveyType", #"dummy project selection"}),
    #"Filtered Rows" = Table.SelectRows(#"Appended Query", each [SurveyEndDate] > Date.From( Date.AddWeeks(DateTime.LocalNow(), -52))),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows",each [ProjectName], each Text.Combine({[ProjectNumber], " - ", [ProjectName]} ) ,Replacer.ReplaceText,{"ProjectName"}),
    #"Filtered Rows1" = Table.SelectRows(#"Replaced Value", each ([RelevantForPCsYesNo] = true))
in
    #"Filtered Rows1"
```


## Table: DimParticipants


```m
let
    Source = SurveyParticipant,
    #"Renamed Columns" = Table.RenameColumns(Source,{{"ID", "SurveyParticipantID"}}),
    #"Inserted Merged Column" = Table.AddColumn(#"Renamed Columns", "Name", each Text.Combine({[LastName], [FirstName]}, ", "), type text),
    #"Added Custom" = Table.AddColumn(#"Inserted Merged Column", "IsReponsiblePm", each if  [ResponsiblePMEmail] = null or [ResponsiblePMEmail] = [EmployeeEmail] then true else false, Logical.Type)
in
    #"Added Custom"
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
    #"Replaced Value2" = Table.ReplaceValue(#"Renamed Columns1","C1","Commitment1",Replacer.ReplaceValue,{"Commitment"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","C2","Commitment2",Replacer.ReplaceValue,{"Commitment"})
in
    #"Replaced Value3"
```


## Table: Auswertung nach KWs (Row)


```m
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WUtJRcswrSc3MUYhR8kqMUVKKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [#"Auswertung nach KWs" = _t, Anteil = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Auswertung nach KWs", type text}, {"Anteil", type text}})
in
    #"Changed Type"
```


## Table: FactSurveyComments


```m
let
    Source = FactSurvey,
    #"Expanded SurveyCampaign" = Table.ExpandRecordColumn(Source, "SurveyCampaign", {"ProjectSurveyID"}, {"ProjectSurveyID"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded SurveyCampaign",{"C1", "C2", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Comment1", "Comment2", "Commitment1", "Commitment2", "LastModifiedBy", "LastModifiedAt", "SurveyTypeID"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Comment3", "Comment"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each [Comment] <> null)
in
    #"Filtered Rows"
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


## Roles

### ParticipantOrResponsiblePM


Model Permission: Read

CheckMemberOfRlsAdminGroup

```m
[IsAdmin] = 0
```



DimProjectSurvey

```m

if([RLS IS Admin],True(),
if(DimProjectSurvey[ProjectSurveyID] = "8547e559-3c0b-431c-a730-a4b7ae29a994", True(),
//current user is in team

if(LOOKUPVALUE( DimParticipants[EmployeeEmail],DimParticipants[EmployeeEmail], [RLS Current User Mail], DimParticipants[ProjectSurveyID], DimProjectSurvey[ProjectSurveyID],  Blank()) <> Blank(), True(), False())
))
```



FactSurveyC

```m

if([RLS IS Admin],True(),

//user is this participant or responsible PM

if( or (  RELATED(DimParticipants[EmployeeEmail]) = [RLS Current User Mail], RELATED(DimParticipants[ResponsiblePMEmail]) = [RLS Current User Mail]),True(),False()) 
)
```



FactSurveyComments

```m

if([RLS IS Admin],True(),

//user is in team

if(LOOKUPVALUE( DimParticipants[EmployeeEmail],DimParticipants[EmployeeEmail], [RLS Current User Mail], DimParticipants[ProjectSurveyID], FactSurveyComments[ProjectSurveyID],  Blank()) <> Blank(), True(), False())
)
```



FactSurveyQ

```m

if([RLS IS Admin],True(),

//current user is in team

if(LOOKUPVALUE( DimParticipants[EmployeeEmail],DimParticipants[EmployeeEmail], [RLS Current User Mail], DimParticipants[ProjectSurveyID], FactSurveyQ[ProjectSurveyID],  Blank()) <> Blank(), True(), False())
)
```



Teams

```m
if(Teams[EmployeeMail] = [RLS Current User Mail],True(), False)
```


### Admin


Model Permission: Read